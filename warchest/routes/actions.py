from flask import request
from warchest import api
from warchest.models import Game
from warchest.models import actions


@api.get('/games/<id>/action/<coin>')
def get_actions(id, coin):
    game = Game.load(id)

    return actions.get_possible(game, coin)


@api.post('/games/<id>/action/<coin>')
def do_actions(id, coin):
    game = Game.load(id)

    data = request.json

    actions.execute(game, coin, data['action'], data.get('data', None))
    return game.to_dict()
