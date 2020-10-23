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
