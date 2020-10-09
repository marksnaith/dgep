<<<<<<< Updated upstream
from dgep import *

if __name__ == '__main__':
    d = Dialogue()

    dgdl = open("assets/testgame.dgdl", "r")
    dgdl = dgdl.read()

    participants = [
        {
            "name":"Alice",
            "player":"Test"
        },
        {
            "name":"Bob",
            "player":"Test2"
        }
    ]

    dialogue = d.new_dialogue(dgdl, participants=participants)

    reply = {"p":"Hi!"}

    d.perform_interaction("TestMove", speaker="Bob", target="Alice", reply=reply)


    print(d.stores)
=======
import dgep
from dialogue_manager import DialogueManager
from interfaces.rest import app
from flask import Flask

class Test(Flask):

    def __init__(self, name, *args, **kwargs):
        super().__init__(name, *args, **kwargs)

    def route(self, *args, **kwargs):
        print("Hello, world", flush=True)
        return super().route(*args, **kwargs)


testapp = Test(__name__)

@testapp.route("/dgep/new")
def new():
    return "Hello world"

if __name__ == "__main__":
    print("Running DGEP")
    #dgep.run(DialogueManager)
    app.run()
>>>>>>> Stashed changes
