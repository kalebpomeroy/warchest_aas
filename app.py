import os
from warchest import app
from flask_cors import CORS

# Load all of our routes

from warchest.routes import games, clients, draft, actions  # NOQA


if __name__ == '__main__':

    CORS(app)
    app.run(host='0.0.0.0', debug=True, port=int(os.environ.get("PORT", 3030)))
