
class Component:

    def __repr__(self):
        ''' Returns a string representation of this class,
            excluding attributes that begin with "_" '''

        repr = {}

        for k in self.__dict__:
            if k[0] != "_":
                repr[k] = self.__dict__[k]

        return str(repr)

    def __str__(self):
        return str(self.__repr__())
