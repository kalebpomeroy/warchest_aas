import mongoengine
from warchest.models.game import Game  # NOQA

mongoengine.connect('warchest')
