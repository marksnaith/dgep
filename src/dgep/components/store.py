from .component import Component

class Store(Component):

    def __init__(self, id, owner, structure, visibility, content):
        self.id = id
        self.owner = owner
        self.structure = structure
        self.visibility = visibility
        self.content = content


    def contains(self, content, negated=False):

        result = content in self.content

        if negated:
            result = not result

        return result
