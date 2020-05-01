''' Module for handling conditionals

    Allows for easy development of new conditional *requirements if/when new
    requirements are added to the DGDL spec

    All new requirement handlers have the same basic signature:

    @requirement_handler(<requirement>)
    def handle_<requirement>_effect(dialogue, requirement)
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
        If all requirements = False, then either elseif if evaluated, or
            "else" effects (if any) are returned
    '''
    outcome = True

    for requirement in conditional.requirements:
        if requirement.type in requirement_handlers:
            outcome = requirement_handlers[requirement.type](dialogue, requirement)
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
def handle_event_requirement(dialogue, requirement):
    return True

@requirement_handler("inrole")
def handle_role_requirement(dialogue, requirement):
    playerID = requirement.playerID
    role = requirement.role

    outcome = False

    for name,player in dialogue.players.items():
        print("Testing if " + str(playerID) + " is in role " + str(role), flush=True)
        if player.player == playerID and player.in_role(role):
            outcome = True
            break

    if requirement.negative:
        return not outcome
    else:
        return outcome

@requirement_handler("inspect")
def handle_inspect_requirement(dialogue, requirement):
    return True
