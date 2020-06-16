''' Module for effect handlers

    Allows for easy development of new handlers if/when new effects are added
    to the DGDL spec

    All new effect handlers have the same basic signature:

    @effect_handler(<effect>)
    def handle_<effect>_effect(dialogue, effect, data)
'''

effect_handlers = {}

def effect_handler(effect):
    def wrapper(fn):
        effect_handlers[effect] = fn
        return fn
    return wrapper

def handle_effects(dialogue, effects, data=None):
    for effect in effects:
        if effect.type in effect_handlers:
            effect_handlers[effect.type](dialogue, effect, data)

# Concrete effect handlers below #

@effect_handler("assign")
def handle_assign_effect(dialogue, effect, data):
    ''' Handles assign effects '''

    if effect.type != "assign":
        return

    user = effect.user
    role = effect.role

    # resolve the user that is to be assigned
    if user == "Target":
        user = data["target"]
    elif user == "speaker":
        user = dialogue.current_speaker
    else:
        # need to extract player name based on player type
        for name,player in dialogue.players.items():
            if player.player == user:
                user = name
                break

    if user is not None and user in dialogue.players:
        if role == "speaker":
            # only one player can be speaker
            for name in dialogue.players:
                dialogue.players[name].remove_from_role(role)
            dialogue.current_speaker = user
        dialogue.players[user].roles.append(role)

@effect_handler("move")
def handle_move_effect(dialogue, effect, data=None):
    if effect.type != "move":
        return

    moveID = effect.moveID
    time = effect.time

    user = effect.user

    if data is None:
        data = {"reply":{}}

    # build the content, if any, based on the incoming interaction data
    content = {}
    if effect.content is not None:
        for c in effect.content:
            if c in data["reply"]:
                content[c] = data["reply"][c]
            else:
                content[c] = "$" + c

    addressees = []
    if effect.addressee is not None:
        addressee = effect.addressee[1:] # removes the '$'

        for name, player in dialogue.players.items():
            if player.player == addressee or addressee in player.roles:
                addressees.append(name)

    moves = []

    if addressees:
        for a in addressees:
            moves.append({"reply": content, "opener": "", "moveID": moveID, "target": a})
    else:
        moves.append({"reply": content, "opener": "", "moveID": moveID})

    if effect.action == "add":
        for name,player in dialogue.players.items():
            if player.player == user or user in player.roles:
                dialogue.available_moves[name][time].extend(moves)

@effect_handler("storeop")
def handle_store_effect(dialogue, effect, data=None):
    if effect.type != "storeop":
        return

    storeID = self.storeID
    action = effect.storeaction

    if storeID in dialogue.stores:
        owner = dialogue.stores[storeID].owner

        # check the speaker is an owner of the store
        if (isinstance(owner, list) and not owner.contains(data["speaker"])
                or owner is not None and data["speaker"] != dialogue.stores[storeID].owner):
            return

        if action == "empty":
            dialogue.stores[storeID].content = []
            return

        for c in effect.content:
            if c[0] == "$":
                var = c[1]

                for key, value in data["reply"].items():
                    if key == var:
                        if action == "add":
                            dialogue.stores[storeID].content.append(value)
                        elif action == "remove" and value in dialogue.stores[storeID].content:
                            dialogue.stores[storeID].content.remove(value)
            else:
                if action == "add":
                    dialogue.stores[storeID].content.append(c)
                elif action == "remove" and c in dialogue.stores[storeID].content:
                    dialogue.stores[storeID].content.remove(c)
