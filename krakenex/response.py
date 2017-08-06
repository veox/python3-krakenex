"""
Class to simplify the handling of responses and errors from the API.
"""

class Response(dict):
    def __init__(self, result):
        """

        :param result: JSON-deserialised Python object
        """
        super(Response, self).__init__(result)

    def extract_result(self):
        """

        :return: result if not an error
        """
        if not self['error']:
            return self['result']
        else:
            return self['error']
