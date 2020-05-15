from argtech import ws
from dialogue import Dialogue as DGEPDialogue
import uuid

@ws.endpoint
class Dialogue:

    """Create and manage dialogues"""

    @ws.method("/new/<protocol>",methods=["POST"])
    def new(self, protocol):
        """
        post:
            summary: Create a new dialogue
            security:
                - APIAuthKey: []
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
        """

        data = ws.request.get_json(force=True)

        d = DGEPDialogue()
        response = d.new_dialogue(protocol, data, "mark")

        return response

    @ws.method("/<dialogueID>/moves",methods=["GET"])
    def moves(self, dialogueID):
        """
        get:
            summary: Get the currently available moves for the given dialogueID
            security:
                - APIAuthKey: []
            parameters:
                - name: dialogueID
                  in: path
                  required: true
                  description: The ID of the dialogue
            responses:
                '401':
                    description: Not authorised
                '404':
                    description: Not found
                '200':
                    description: OK
                    schema:
                        type: object
                        properties:
                            dialogueID:
                                type: string
                            moves:
                                type: object
                                properties:
                                    <player>:
                                        type: array
                                        items:
                                            type: object
                                            properties:
                                                reply:
                                                    type: object
                                                    properties:
                                                        p:
                                                            type: string
                                                        target:
                                                            type: string
                                                        moveID:
                                                            type: string
                                                        opener:
                                                            type: string
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
                return "Dialogue not found", 404
        else:
            return ws._401()

    @ws.method("/<dialogueID>/interaction/<interactionID>",methods=["POST"])
    def interaction(self, dialogueID, interactionID):
        """
        post:
            summary: Performs the given interaction
            security:
                - APIAuthKey: []
            responses:
                '200':
                    description: OK
            parameters:
                - name: dialogueID
                  in: path
                  required: true
                  description: The ID of the dialogue in which to perform the interaction

                - name: interactionID
                  in: path
                  required: true
                  description: The ID of the interaction to perform

                - name: body
                  in: body
                  required: true
                  description: The body of the interaction
                  schema:
                    type: object
                    properties:
                        speaker:
                            type: string
                        target:
                            type: string
                        reply:
                            type: object
                            properties:
                                p:
                                    type: string
        """

        return "DialogueID: {}; interactionID: {}".format(dialogueID,interactionID)
