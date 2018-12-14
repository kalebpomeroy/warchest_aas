from random import sample
import json
from warchest import app
from warchest.routes import games, clients, draft  # NOQA

client = app.test_client()


def test_unauthorized():
    rv = client.get('/games')
    assert rv.status_code == 401


def test_happy_path():
    c = {}
    rv = client.post('/register')
    c['wolves'] = json.loads(rv.data)['client_id']

    rv = client.post('/register')
    c['ravens'] = json.loads(rv.data)['client_id']

    # create a game
    rv = client.post('/games', headers={'X-Client-ID': c['wolves']})
    game = json.loads(rv.data)
    assert game['status'] == 'new'

    # Play two joins the game
    rv = client.post('/games/{}'.format(game['id']), headers={'X-Client-ID': c['ravens']})
    game = json.loads(rv.data)
    assert game['status'] == 'in_progress'
    assert len(game['cards']['draft']) == 8

    for i in [1, 2, 2, 2]:
        rv = client.post('/games/{}/draft'.format(game['id']),
                         data=json.dumps({"picks": sample(game['cards']['draft'], i)}),
                         headers={
                            'X-Client-ID': c[game['initiative']],
                            'Content-Type': 'application/json'
                        })
        game = json.loads(rv.data)

    assert game['status'] == 'in_progress'
    assert game['zones']['wolves']['hand']['count'] == 3
    assert game['zones']['ravens']['hand']['count'] == 3
    assert game['zones']['wolves']['recruit']['count'] >= 7
    assert game['zones']['ravens']['recruit']['count'] >= 7
    assert game['zones']['ravens']['bag']['count'] == 6
    assert game['zones']['ravens']['bag']['count'] == 6

    # A player can only see one of their chips
    assert ("chips" not in game['zones']['wolves']['hand']) | ("chips" not in game['zones']['ravens']['hand'])
