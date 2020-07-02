from argtech import ws
import pymongo
from werkzeug.utils import secure_filename
import re
import dgdl
import json
import ast

_protocol_player_regex = re.compile(r"player\(([^\(\)]+)\)")
_protocol_player_spec_regex = re.compile(r"([^:{}, ]+):(?:([^:,{} ]+)|{([^{}]+)})")
_protocol_description_regex = re.compile(r"\/\*[\s]+description:[\s]+(.*)\*\/",re.IGNORECASE)

@ws.group
class Protocol:

    """Create and manage protocols"""

    @ws.method("/<protocol>")
    def get(self, protocol):
        """
        @/app/docs/protocol/get.yml
        """
        result = self.get_protocol(protocol)

        if result is not None:
            dgdl = result["dgdl"]
            return dgdl, 200
        else:
            return "Protocol not found", 404

    @ws.method("/list")
    def list(self):
        """
        @/app/docs/protocol/list.yml
        """
        mongo = pymongo.MongoClient("mongodb://dgep_mongo:27017/")
        db = mongo["dgep"]
        protocols = db["protocols"]

        result = protocols.find()

        to_return = {}

        for protocol in result:
            to_return[protocol["name"]] = {
                    "players": self.get_players(protocol["dgdl"].decode("utf-8")),
                    "description": self.get_description(protocol["dgdl"].decode("utf-8"))
                }

        return to_return, 200

    @ws.method("/new",methods=["PUT"])
    def new(self):
        """
        @/app/docs/protocol/new.yml
        """
        file = ws.request.files['dgdl_file']
        name = secure_filename(file.filename)
        name = name.split(".")[0]
        content = file.read()

        mongo = pymongo.MongoClient("mongodb://dgep_mongo:27017/")
        db = mongo["dgep"]
        protocols = db["protocols"]

        if self.get_protocol(name) is not None:
            protocols.update_one({"name":name}, {"$set": {"dgdl": content}})
        else:
            protocols.insert_one({"name": name, "dgdl": content})

        return {"message":"saved","protocol":name}, 201


    @ws.method("/test",methods=["POST"])
    def test_file(self):
        """
        @/app/docs/protocol/test_protocol.yml
        """
        file = ws.request.files['dgdl_file']

        if file:
            return self.test_protocol(file=file), 200
        else:
            return "Error testing protocol", 500

    @ws.method("/test/<protocol>")
    def test(self, protocol):
        """
        @/app/docs/protocol/test.yml
        """
        return self.test_protocol(protocol=protocol)


    def test_protocol(self, file=None, protocol=None):
        """
        Test the given DGDL file (prioritised), or protocol
        """

        if file is not None:
            d = file.read().decode("utf-8")
        elif protocol is not None:
            d = self.get_protocol(protocol)
            if d is None:
                return "Protocol not found", 404
        else:
            return "Error testing protocol", 500

        game = dgdl.DGDLParser().parse(input=d)

        if isinstance(game, list):
            return {"status":"error","errors":game}
        else:
            return {"status":"OK", "game":ast.literal_eval(game.__repr__())}

    def get_protocol(self, protocol):
        """
        Get the given protocol from mongodb
        """
        mongo = pymongo.MongoClient("mongodb://dgep_mongo:27017/")
        db = mongo["dgep"]
        protocols = db["protocols"]

        result = protocols.find_one({"name": protocol})

        if result is not None:
            return result["dgdl"].decode("utf-8")
        else:
            return None

    def get_players(self, dgdl):
        """
        Extract the player specifications from the given dgdl
        """
        matches = re.findall(_protocol_player_regex, dgdl)
        players = []

        for m in matches:
            if m.strip() != "":
                player = {}
                for p in re.findall(_protocol_player_spec_regex, m.strip()):
                    p = [x for x in p if x.strip() != ""]
                    if p[0] == "roles":
                        player[p[0]] = [r.strip() for r in p[1].split(",")]
                    else:
                        player[p[0]] = p[1]
                players.append(player)

        return players

    def get_description(self, dgdl):
        """
        Extract the content of the 'description' keyword from the DGDL spec
        """
        matches = re.findall(_protocol_description_regex, dgdl)

        for m in matches:
            m = m.strip()
            if m != "":
                return m

        return ""
