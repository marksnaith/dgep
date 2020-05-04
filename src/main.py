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
