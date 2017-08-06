"""
Class to simplify the handling of responses and errors from the API.
"""

class Result(dict):
    def __init__(self, result):
        """

        :param result: JSON-deserialised Python object
        """
        super(Result, self).__init__(result)

    def extract_result(self):
        """

        :return: result if not an error
        """
        if not self['error']:
            return self['result']
        else:
            raise Exception(self['error'])
