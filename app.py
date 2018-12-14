from warchest import app

# Load all of our routes

from warchest.routes import games, clients, draft  # NOQA


if __name__ == '__main__':
    app.run(debug=True, port=3000)
