import dgep
from dialogue import Dialogue

class DialogueManager:

    def __init__(self):
        pass

    @dgep.endpoint("new")
    def new_dialogue(self, data):

        return Dialogue().load(1)
        #return Dialogue().new_dialogue("testgame", data)


    @dgep.endpoint("protocol")
    def protocol(self, data):
        return data

    @dgep.endpoint("interaction",parameters=["moveID"])
    def interaction(self, data):
        d = Dialogue('/lib/dgdl-parser/grammar/testgame.dgdl')

        return d.perform_interaction(data)
