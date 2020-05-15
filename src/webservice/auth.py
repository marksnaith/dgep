from argtech import ws
import random
import hashlib
import pymongo

@ws.endpoint
class Auth:

    """Handles authentication for DGEP"""

    def __init__(self):
        self.mongo = pymongo.MongoClient("mongodb://dgep_mongo:27017/")

    @ws.method("/login",methods=["POST"])
    def login(self):
        """
        post:
            description: Log in
            responses:
                '200':
                    description: OK
                    schema:
                        type: object
                        properties:
                            username:
                                type: string
                            authToken:
                                type: string
                '401':
                    description: Not authorised
            parameters:
                - name: body
                  in: body
                  required: true
                  schema:
                    type: object
                    properties:
                        username:
                            type: string
                        password:
                            type: string
        """

        return ws.login(self.check_credentials)

    def check_credentials(self, username, password):
        db = self.mongo["dgep"]
        users = db["users"]

        result = users.find_one({"username":username})

        if not result:
            return None

        hashed, salt = self.hash(username, password, result["salt"])

        if hashed != result["password"]:
            return None

        return {"username": username}

    def hash(self, username, password, salt=None):
        if salt is None:
            ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
            chars = []

            for i in range(16):
                chars.append(random.choice(ALPHABET))

            salt = "".join(chars)

        return hashlib.sha224(str(username + password + salt).encode("utf-8")).hexdigest(), salt

    @ws.method("/register",methods=["POST"])
    def register(self):
        """
        post:
            description: Register a new user
            responses:
                '200':
                    description: OK
            parameters:
                - name: body
                  in: body
                  required: true
                  schema:
                    type: object
                    properties:
                        username:
                            type: string
                        password:
                            type: string
        """

        details = ws.request.get_json(force=True)

        if "username" not in details or "password" not in details:
            return "No username and/or password provided", 400

        username = details["username"]

        db = self.mongo["dgep"]
        users = db["users"]

        result = users.find_one({"username": username})

        if result is not None:
            return "User already exists", 403

        password, salt = self.hash(username, details["password"])

        obj = {"username": username, "password": password, "salt": salt}
        users.insert_one(obj)

        return "Success", 200
