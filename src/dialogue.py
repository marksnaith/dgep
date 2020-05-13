import dgdl
import ast
from components import *
import json
from handlers import *

import sys

from argtech import ws

@ws.endpoint
class Dialogue:

    def __init__(self):
        #DGDL
        self.parser = dgdl.DGDLParser()
        self.game = None

        #Dialogue properties
        self.dialogueID = None
        self.protocol = None
        self.players = {}
        self.stores = {}
        self.backtracking = False
        self.available_moves = {}
        self.current_speaker = None

    @ws.method("/new/<protocol>",methods=["POST"])
    def new_dialogue(self, protocol):
        """
        post:
            summary: Create a new dialogue
            responses:
                '200':
                    description: OK
                    schema:
                        type: object
                        properties:
                            foo:
                                type: string
                                example: bar
            parameters:
                - name: protocol
                  in: path
                  required: true
                  description: The name of the protocol

                - name: body
                  in: body
                  required: true
                  schema:
                      type: object
                      properties:
                          participants:
                              type: array
                              items:
                                  type: object
                                  properties:
                                      name:
                                          type: string
                                      player:
                                          type: string


        get:
            summary: Check a dialogue
            responses:
                '200':
                    description: OK
        """

        data = ws.request.get_json(force=True)

        if data is None:
            data = {}

        print(data, file=sys.stderr)

        self.protocol = protocol
        self.game = self.parser.parse("/app/assets/{protocol}.dgdl".format(protocol=protocol))
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

        print("returning json", file=sys.stderr)
        print(str(self.json()), file=sys.stderr)

        return self.json()

    def start(self):
        ''' Starts this dialogue, executing all rules with "initial" scope'''

        for rule in self.game.rules:
            if rule.scope == "initial":
                handle_effects(self, rule.effects)
                if rule.conditional is not None:
                    effects = handle_conditional(self, rule.conditional)
                    handle_effects(self, effects)

        self.dialogueID = self.save()

    def validate(self):
        ''' Checks that this dialogue satisfies the constraints of the
            game specification '''

        ''' TODO:
            - Check max + min participants
            - Check max + min participants in roles
        '''

        return

    def perform_interaction(self, data):

        ''' data = {
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

        if "moveID" in data:
            interactionID = data["moveID"]
            interaction = None

            for i in self.game.interactions:
                if i.id == interactionID:
                    interaction = i
                    break

            if interaction is not None:
                if interactions.effects:
                    handle_effects(self, interaction.effects, data)

                if interaction.conditional is not None:
                    effects = handle_conditional(self, interaction.conditional, data)

                return ast.literal_eval(str(interaction))
            else:
                return "Interaction not found"

        return "MoveID not found"

    def save(self):

        return

    def load(self, dialogueID):
        mock_json = '{"protocol":"testgame","backtracking": true, "available_moves": {"Bob": {"next": [{"reply": {"p": "$p"}, "moveID": "TestMove", "opener": ""}], "future": []}}, "current_speaker": "Bob", "players": {"Bob": {"roles": ["TestRole", "speaker"], "name": "Bob", "player": "Test2"}}, "stores": {"TestStore": {"visibility": "public", "content": ["c"], "id": "TestStore", "owner": ["Test"], "structure": "set"}}}'

        d = json.loads(mock_json)

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
            "protocol": self.protocol,
            "players": {key: value.__dict__ for key,value in self.players.items()},
            "backtracking": self.backtracking,
            "stores": {key: value.__dict__ for key, value in self.stores.items()},
            "current_speaker": self.current_speaker,
            "available_moves": self.available_moves
        }

        return to_return #json.dumps(to_return)
