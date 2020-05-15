from argtech import ws

@ws.endpoint
class Protocol:

    """Create and manage protocols"""

    @ws.method("/<protocol>")
    def get(self, protocol):
        """
        get:
            summary: Get the DGDL specification of the given protocol
            responses:
                '200':
                    description: OK
            parameters:
                - name: protocol
                  in: path
                  required: true
                  description: The name of the protocol
        """
        return protocol


    @ws.method("/new",methods=["PUT"])
    def new(self):
        """
        put:
            summary: Upload a new DGDL protocol
            responses:
                '201':
                    description: Created
            consumes:
                - multipart/form-data
            parameters:
                - in: formData
                  name: dgdl_file
                  type: file
                  description: The DGDL file to save
        """

        file = ws.request.files['dgdl_file']

        return "Uploaded", 201


    @ws.method("/test",methods=["POST"])
    def test_file(self):
        """
        post:
            summary: Test the provided DGDL file
            responses:
                '200':
                    description: OK
            consumes:
                - multipart/form-data
            parameters:
                - in: formData
                  name: dgdl_file
                  type: file
                  description: The DGDL file to test
        """
        file = ws.request.files['dgdl_file']

        if file:
            return file.read()
        else:
            return "No file read"



    @ws.method("/test/<protocol>")
    def test(self, protocol):
        """
        get:
            summary: Test the given protocol
            responses:
                '200':
                    description: OK
                parameters:
                    - name: protocol
                      in: path
                      required: true
                      description: The name of the protocol to test
        """

        return protocol
