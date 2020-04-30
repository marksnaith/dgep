import dgep

class DialogueManager:

    def __init__(self):
        pass

    @dgep.endpoint("new", parameters=["foo"])
    def new_dialogue(self, data):

        if data["foo"] is None:
            return "Foo not set"
        else:
            return "Foo set: "  + data["foo"]

    @dgep.endpoint("protocol")
    def protocol(self, data):
        return data

    @dgep.endpoint("interaction")
    def interaction(self, data):
        return data
