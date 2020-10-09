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

    print("Available moves: {}".format(str(d.get_available_moves())))

    moves = d.perform_interaction("TestMove", speaker="Bob", target="Alice", reply=reply)

    print("Available moves: {}".format(str(moves)))
