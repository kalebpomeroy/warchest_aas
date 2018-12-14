from flask import request
from warchest import api
from warchest.models import Game


@api.post('/games/<id>/draft')
def draft(id):
    game = Game.load(id)
    data = request.json
    game.cards.do_draft(data['picks'])
    return game.to_dict()
