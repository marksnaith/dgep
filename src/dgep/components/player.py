from .component import Component

class Player(Component):

    def __init__(self, name, player, roles=None, participantID=None):
        self.name = name
        self.player = player

        if roles is None:
            self.roles = []
        else:
            self.roles = roles

        self.participantID = participantID

    def in_role(self, role):
        return role in self.roles

    def remove_from_role(self, role):
        if self.in_role(role):
            self.roles.remove(role)
