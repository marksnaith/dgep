import dgdl
import ast
from components import *
import json
from handlers import *
import uuid
import sys
import pymongo
from bson.objectid import ObjectId

class Dialogue:
    """
    Class to represent and manage a dialogue based on a DGDL protocol
    """

    def __init__(self):
        #DGDL
        self.parser = dgdl.DGDLParser()
        self.game = None

        #meta-level stuff
        self.owner = None
        self.mongo = pymongo.MongoClient("mongodb://dgep_mongo:27017/")

        #Dialogue properties
        self.dialogueID = None
        self.protocol = None
        self.players = {}
        self.stores = {}
        self.turntaking = "strict"
        self.backtracking = False
        self.available_moves = {}
        self.current_speaker = None
        self.current_speakers = []
        self.runtimevars = {}
        self.dialogue_history = []

    def new_dialogue(self, protocol, data, owner):
        """
        Creates a new dialogue based on the given protocol
        :param str protocol: the protocol corresponding to a DGDL file
        :param dict data: the data to instantiate the protocol into a dialogue
        :owner the username of the owner of this dialogue

        :return dictionary representation of the dialogue
        :rtype dict
        """

        if owner is None:
            return None

        if data is None:
            data = {}

        self.owner = owner
        self.dialogueID = str(uuid.uuid4().hex)

        self.protocol = protocol.lower()
        dgdl = self.load_protocol(self.protocol)

        if dgdl is not None:
            self.game = self.parser.parse(input=dgdl)
            if isinstance(self.game, list):
                return {"errors": self.game}

            self.turntaking = self.game.turntaking
            self.backtracking = self.game.backtracking

            if "participants" in data:
                for participant in data["participants"]:
                    name = participant["name"]
                    player = participant["player"]
                    roles = [r for p in self.game.players for r in p.roles if p.playerID==player]

                    self.players[name] = Player(name, player, roles)
                    self.available_moves[name] = {"next":[], "future":[]}

            for store in self.game.stores:
                id = store.storeID
                self.stores[id] = Store(id, store.owner, store.structure, store.visibility, store.content)

            self.start()
            self.save()

            return self.json()
        else:
            return {"error":"Protocol " + self.protocol + " not found"}

    def start(self):
        """
        Starts this dialogue, executing all rules with "initial" scope
        """

        for rule in self.game.rules:
            if rule.scope == "initial":
                print("Handling initial effects")
                print(rule.effects)
                handle_effects(self, rule.effects)
                if rule.conditional is not None:
                    effects = handle_conditional(self, rule.conditional)
                    handle_effects(self, effects)

    def validate(self):
        ''' Checks that this dialogue satisfies the constraints of the
            game specification '''

        ''' TODO:
            - Check max + min participants
            - Check max + min participants in roles
        '''

        return

    def get_available_moves(self):
        """
        Returns the available moves based on 1) the current speaker(s) and 2)
            whether or not backtracking is allowed
        """
        response = {}
        if self.turntaking == "strict":
            if self.current_speaker in self.available_moves:
                moves = self.available_moves[self.current_speaker]

                if moves["next"]:
                    response[self.current_speaker] = moves["next"]
                elif self.backtracking:
                    response[self.current_speaker] = moves["future"]
                else:
                    response[self.current_speaker] = []
        else:
            for player, moves in self.available_moves.items():
                if moves["next"]:
                    response[player] = moves["next"]
                elif self.backtracking and moves["future"]:
                    response[player] = moves["future"]

        return response

    def perform_interaction(self, interactionID, data):
        """
        Performs the given interaction, based on the given data

        :param str interactionID: the interaction ID (move name)
        :param dict data: the data that instantiates the interaction
        :return the available moves following the interaction
        :rtype dict
        """

        '''data is expected in the following format:

           data = {
            "moveID": <moveID>,
            "target": <User>,
            "dialogueID": <dialogueID>,
            "speaker": <User>,
            "reply": {
                "p": "content",
                "q": "content",
                ...
            }
        }'''

        interaction = None

        for i in self.game.interactions:
            if i.id == interactionID:
                interaction = i
                break

        # empty everyone's "next" moves
        for k in list(self.available_moves.keys()):
            self.available_moves[k]["next"] = []

        if interaction is not None:
            print("Performing interaction effects")
            print(interaction.effects)
            if interaction.effects:
                handle_effects(self, interaction.effects, data)

            if interaction.conditional is not None:
                effects = handle_conditional(self, interaction.conditional, data)
                handle_effects(self, effects, data)

            self.dialogue_history.append(data)
            self.save()
            return self.get_available_moves()
        else:
            return "Interaction not found"

    def save(self):
        """
        Save the dialogue state to MongodB
        """
        db = self.mongo["dgep"]
        dialogues = db["dialogues"]

        query = {"dialogueID": self.dialogueID}

        if dialogues.find(query).count() > 0:
            d = {"$set" : {"dialogue": self.json()}}
            dialogues.update_one(query, d)
        else:
            store = {
                "dialogueID": self.dialogueID,
                "owner": self.owner,
                "dialogue": self.json()
            }
            dialogues.insert_one(store).inserted_id

    def load_protocol(self, protocol):
        """
        Load the given protocol dgdl from mongo
        :param str protocol: the name of the protocol to load
        :return the dgdl
        :rtype str
        """
        db = self.mongo["dgep"]
        protocols = db["protocols"]

        result = protocols.find_one({"name":self.protocol})

        if result is not None:
            return result["dgdl"].decode("utf-8")
        else:
            return None


    def load(self, dialogueID):
        """
        Load the dialogue with the given ID from mongoDB
        :param str dialogueID: the dialogueID to load
        :return the loaded Dialogue
        :rtype Dialogue
        """

        db = self.mongo["dgep"]
        dialogues = db["dialogues"]

        result = dialogues.find_one({"dialogue.dialogueID": dialogueID})

        if result is not None:
            self.owner = result["owner"]
            dialogue = result["dialogue"]

            self.dialogueID = dialogue["dialogueID"]
            self.protocol = dialogue["protocol"]
            self.game = self.parser.parse(input=self.load_protocol(self.protocol))
            self.available_moves = dialogue["available_moves"]
            self.current_speaker = dialogue["current_speaker"]
            self.backtracking = dialogue["backtracking"]

            for name, player in dialogue["players"].items():
                self.players[name] = Player(player["name"], player["player"], player["roles"])

            for name, store in dialogue["stores"].items():
                self.stores[name] = Store(store["id"], store["owner"], store["structure"],store["visibility"], store["content"])

            return self
        else:
            return None


        mock_json = '{"dialogueID":"abc","protocol":"testgame","backtracking": true, "available_moves": {"Bob": {"next": [{"reply": {"p": "$p"}, "moveID": "TestMove", "opener": ""}], "future": []}}, "current_speaker": "Bob", "players": {"Bob": {"roles": ["TestRole", "speaker"], "name": "Bob", "player": "Test2"}}, "stores": {"TestStore": {"visibility": "public", "content": ["c"], "id": "TestStore", "owner": ["Test"], "structure": "set"}}}'

        d = json.loads(mock_json)

        self.dialogueID = d["dialogueID"]
        self.protocol = d["protocol"]





        self.game = self.parser.parse("/app/assets/{protocol}.dgdl".format(protocol=self.protocol))
        self.available_moves = d["available_moves"]
        self.current_speaker = d["current_speaker"]
        self.backtracking = d["backtracking"]

        for name, player in d["players"].items():
            self.players[name] = Player(player["name"], player["player"], player["roles"])

        for name, store in d["stores"].items():
            self.stores[name] = Store(store["id"], store["owner"], store["structure"],store["visibility"], store["content"])

        return self.json()

    def json(self):
        ''' Get a JSON representation of this dialogue '''

        to_return = {
            "dialogueID": self.dialogueID,
            "protocol": self.protocol,
            "players": {key: value.__dict__ for key,value in self.players.items()},
            "turntaking": self.turntaking,
            "backtracking": self.backtracking,
            "stores": {key: value.__dict__ for key, value in self.stores.items()},
            "current_speaker": self.current_speaker,
            "available_moves": self.available_moves,
            "dialogue_history": self.dialogue_history
        }

        return to_return #json.dumps(to_return)
