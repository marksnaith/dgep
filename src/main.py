"""
Copyright (C) 2020  Centre for Argument Technology (http://arg.tech)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

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
