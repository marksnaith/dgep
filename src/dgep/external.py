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

import requests
import json
import traceback

def call_uri(uri, data=None):
    if data is None:
        data = {}

    if type(data) is dict:
        data = json.dumps(data)

    try:
        result = requests.post(uri, data=data)
        response = result.json()
    except:
        response = {"response": False}
        traceback.print_exc()

    return response
