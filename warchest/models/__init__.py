import os
import mongoengine
from warchest.models.game import Game  # NOQA


mongoengine.connect('warchest', host=os.environ.get("MONGODB_URI", None))
