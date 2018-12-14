from warchest import app
from flask import jsonify


class APIError(Exception):
    def __init__(self, message, status_code):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


@app.errorhandler(APIError)
def handle_invalid_usage(error):
    response = jsonify({"message": error.message})
    response.status_code = error.status_code
    return response
