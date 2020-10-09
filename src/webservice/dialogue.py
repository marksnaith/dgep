from argtech import ws
from dialogue import Dialogue as DGEPDialogue
import uuid

@ws.group
class Dialogue:

    """Create and manage dialogues"""

    @ws.method("/new/<protocol>",methods=["POST"])
    def new(self, protocol):
        """
        @/app/docs/dialogue/new.yml
        """

        login = ws.authorise()

        if login is not None:
            data = ws.request.get_json(force=True)

            d = DGEPDialogue()
            response = d.new_dialogue(protocol, data, login["username"])

            return response
        else:
            return ws._401()

    @ws.method("/<dialogueID>/moves",methods=["GET"])
    def moves(self, dialogueID):
        """
        @/app/docs/dialogue/moves.yml
        """

        login = ws.authorise()

        if login is not None:
            d = DGEPDialogue().load(dialogueID)

            if d is not None:
                if d.owner == login["username"]:
                    return d.get_available_moves(), 200
                else:
                    return ws._401()
            else:
                return "Dialogue not found", 404
        else:
            return ws._401()

    @ws.method("/<dialogueID>/interaction/<interactionID>",methods=["POST"])
    def interaction(self, dialogueID, interactionID):
        """
        @/app/docs/dialogue/interaction.yml
        """

        login = ws.authorise()

        if login is not None:
            d = DGEPDialogue().load(dialogueID)

            if d is not None:
                if d.owner == login["username"]:
                    data = ws.request.get_json(force=True)
                    return d.perform_interaction(interactionID, data)
                    #return data
                else:
                    return ws._401()
        else:
            return ws._401()

        return "DialogueID: {}; interactionID: {}".format(dialogueID,interactionID)

    @ws.method("/<dialogueID>/status",methods=["GET"])
    def status(self, dialogueID):
        """
        @/app/docs/dialogue/status.yml
        """

        login = ws.authorise()

        if login is not None:
            d = DGEPDialogue().load(dialogueID)

            if d is not None:
                if d.owner == login["username"]:
                    return d.json(), 200
                else:
                    return ws._401()
        else:
            return ws._401()
