from warchest import api
from warchest.models import Game


@api.get('/games')
def list_games():
    return {'games': [g.to_dict() for g in Game.find_by_status('new')]}


@api.post('/games')
def create_games():
    game = Game.make_new()
    return game.to_dict()


@api.post('/games/<id>')
def join_game(id):
    game = Game.load(id)
    game.join()
    return game.to_dict()


@api.get('/games/<id>')
def show_game(id):
    return Game.load(id).to_dict()
