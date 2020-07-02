from argtech import ws
import pymongo
from werkzeug.utils import secure_filename
import re
import dgdl
import json

_protocol_player_regex = re.compile(r"player\(([^\(\)]+)\)")
_protocol_player_spec_regex = re.compile(r"([^:{}, ]+):(?:([^:,{} ]+)|{([^{}]+)})")


_protocol_player_roles_regex = re.compile(r"{([^{}]+)}")

@ws.group
class Protocol:

    """Create and manage protocols"""

    @ws.method("/<protocol>")
    def get(self, protocol):
        """
        @/app/docs/protocol/get.yml
        """
        mongo = pymongo.MongoClient("mongodb://dgep_mongo:27017/")
        db = mongo["dgep"]
        protocols = db["protocols"]

        result = protocols.find_one({"name": protocol})

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
            p = {"players": self.get_players(str(protocol["dgdl"]))}

            to_return[protocol["name"]] = p

        return to_return, 200

    @ws.method("/new",methods=["PUT"])
    def new(self):
        """
        @/app/docs/protocol/new.yml
        """

        file = ws.request.files['dgdl_file']

        mongo = pymongo.MongoClient("mongodb://dgep_mongo:27017/")
        db = mongo["dgep"]
        protocols = db["protocols"]

        name = secure_filename(file.filename)
        name = name.split(".")[0]

        content = file.read()

        query = {"name": name}

        if protocols.find_one(query) is not None:
            protocols.update_one(query, {"$set": {"dgdl": content}})
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
            d = file.read().decode("utf-8")
            print(d)
            parser = dgdl.DGDLParser()
            game = parser.parse(input=d)

            if isinstance(game, list):
                return {"status":"error","errors": game}, 200
            else:
                return {"status":"OK"}, 200
        else:
            return "No file read", 500



    @ws.method("/test/<protocol>")
    def test(self, protocol):
        """
        @/app/docs/protocol/test.yml
        """

        return protocol



    def get_players(self, dgdl):
        matches = re.findall(_protocol_player_regex, dgdl)
        players = []

        for m in matches:
            if m.strip() != "":
                player = {}
                print(m)
                for p in re.findall(_protocol_player_spec_regex, m.strip()):
                    p = [x for x in p if x.strip() is not ""]
                    if p[0] == "roles":
                        player[p[0]] = [r.strip() for r in p[1].split(",")]
                    else:
                        player[p[0]] = p[1]



                players.append(player)

        return players
