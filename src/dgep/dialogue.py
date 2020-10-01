import dgdl
import ast
from .components import *
import json
from .handlers import *
import uuid
import sys
import pymongo
from bson.objectid import ObjectId

class Dialogue:
    """
    Class to represent and manage a dialogue based on a DGDL protocol
    """

    def __init__(self, dialogue=None):
        self.parser = dgdl.DGDLParser()

        if dialogue is not None:
            self.load(dialogue)
        else:
            self.dgdl = None
            self.game = None

            # dialogue properties
            self.players = {}
            self.stores = {}
            self.turntaking = "strict"
            self.backtracking = False
            self.available_moves = {}
            self.current_speaker = None
            self.current_speakers = []
            self.runtimevars = {}
            self.dialogue_history = []
            self.status = "inactive"


    def new_dialogue(self, dgdl, **data):
        """
        Creates a new dialogue based on the given game
        :param str protocol: the protocol corresponding to a DGDL file
        :param dict data: the data to instantiate the protocol into a dialogue

        :return dictionary representation of the dialogue
        :rtype dict
        """

        if data is None:
            data = {}

        if dgdl is not None:
            self.dgdl = dgdl
            self.game = self.parser.parse(input=dgdl)
            if isinstance(self.game, list):
                return {"errors": self.game}

            self.turntaking = self.game.turntaking
            self.backtracking = self.game.backtracking

            if "participants" in data:
                participantID = 1
                for participant in data["participants"]:
                    name = participant["name"]
                    player = participant["player"]
                    roles = [r for p in self.game.players for r in p.roles if p.playerID==player]

                    self.players[name] = Player(name, player, roles, participantID)
                    participantID = participantID + 1
                    self.available_moves[name] = {"next":[], "future":[]}

            for store in self.game.stores:
                id = store.storeID
                self.stores[id] = Store(id, store.owner, store.structure, store.visibility, store.content)

            self.start()
            return self.save()
        else:
            return {"error":"No game specification provided"}

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

        self.status = "active"

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

    def perform_interaction(self, interactionID, **data):
        """
        Performs the given interaction, based on the given data

        :param str interactionID: the interaction ID (move name)
        :param dict data: the data that instantiates the interaction
        :return the available moves following the interaction
        :rtype dict
        """

        '''data is expected in the following format:

           data = {
           "speaker": <User>,
            "target": <User>,
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
            # self.save()
            return self.get_available_moves()
        else:
            return "Interaction not found"

    def load(self, dialogue):
        """
        Load the dialogue with the given ID from mongoDB
        :param str dialogueID: the dialogueID to load
        :return the loaded Dialogue
        :rtype Dialogue
        """

        self.dgdl = dialogue["dgdl"]

        # self.dialogueID = dialogue["dialogueID"]
        self.game = self.parser.parse(input=self.dgdl)
        self.available_moves = dialogue["available_moves"]
        self.current_speaker = dialogue["current_speaker"]
        self.backtracking = dialogue["backtracking"]
        self.turntaking = dialogue["turntaking"]
        self.dialogue_history = dialogue["dialogue_history"]
        self.current_speakers = dialogue["current_speakers"]
        self.runtimevars = dialogue["runtimevars"]
        self.status = dialogue["status"]

        self.players = {}
        self.stores = {}

        for name, player in dialogue["players"].items():
            self.players[name] = Player(player["name"], player["player"], player["roles"])

        for name, store in dialogue["stores"].items():
            self.stores[name] = Store(store["id"], store["owner"], store["structure"],store["visibility"], store["content"])

        return self

    def save(self):
        ''' Get a dict representation of this dialogue '''

        to_return = {
            "dgdl": self.dgdl,
            "players": {key: value.__dict__ for key,value in self.players.items()},
            "turntaking": self.turntaking,
            "backtracking": self.backtracking,
            "stores": {key: value.__dict__ for key, value in self.stores.items()},
            "current_speaker": self.current_speaker,
            "available_moves": self.available_moves,
            "dialogue_history": self.dialogue_history,
            "current_speakers": self.current_speakers,
            "runtimevars": self.runtimevars,
            "status": self.status
        }

        return to_return
