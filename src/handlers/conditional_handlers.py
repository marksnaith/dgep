''' Module for handling conditionals

    Allows for easy development of new conditional requirements if/when new
    requirements are added to the DGDL spec

    All new requirement handlers have the same basic signature:

    @requirement_handler(<requirement>)
    def handle_<requirement>_effect(dialogue, requirement)

    This means all requirement handlers have access to the dialogue object to
    test dialogue properties (e.g. current speaker)
'''

requirement_handlers = {}

def requirement_handler(requirement):
    def wrapper(fn):
        requirement_handlers[requirement] = fn
        return fn
    return wrapper

def handle_conditional(dialogue, conditional, data=None):
    ''' Handler for conditionals

        If all requirements = True, conditional effects are returned
        If all requirements = False, then either elseif is evaluated (as a
        conditional), or "else" effects (if any) are returned
    '''
    outcome = True

    for requirement in conditional.requirements:
        if requirement.type in requirement_handlers:
            outcome = requirement_handlers[requirement.type](dialogue, requirement, data)
            if not outcome:
                break # no point in testing more if even one is false

    if outcome:
        return conditional.effects
    elif conditional.elseif is not None:
        return handle_conditional(conditional.elseif, data)
    else:
        return conditional.else_effects

# Requirement handlers below #

@requirement_handler("event")
def handle_event_requirement(dialogue, requirement, data):
    return True

@requirement_handler("inrole")
def handle_role_requirement(dialogue, requirement, data):
    playerID = requirement.playerID
    role = requirement.role

    if playerID == "speaker":
        playerID = dialogue.current_speaker

    outcome = False

    for name,player in dialogue.players.items():
        if player.player == playerID and player.in_role(role):
            outcome = True
            break

    if requirement.negative:
        return not outcome
    else:
        return outcome

@requirement_handler("inspect")
def handle_inspect_requirement(dialogue, requirement, data):
    storeID = requirement.storeID
    content = requirement.content
    position = requirement.storepos

    negated = requirement.negated

    store = dialogue.stores[storeID]

    result = True

    for c in content:
        if c[0] == '"':
            c = c.replace('"','') #strip quotes
            if not store.contains(c, negated):
                result = False
                break
        elif data is not None and "reply" in data:
            if c in data["reply"]:
                if not store.contains(data["reply"][c], negated):
                    result = False
                    break
        else:
            result = False
            break

    return result
