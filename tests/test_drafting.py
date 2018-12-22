from random import sample, choice, randint
import json
from warchest import app
from warchest.routes import games, clients, draft, actions  # NOQA

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
    assert game['status'] == 'drafting'
    assert len(game['cards']['draft']) == 8

    for i in [1, 2, 2, 2]:
        rv = client.post('/games/{}/draft'.format(game['id']),
                         data=json.dumps({"picks": sample(game['cards']['draft'], i)}),
                         headers={
                            'X-Client-ID': c[game['active_player']],
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

    # A player can only see one of their coins
    assert ("coins" not in game['zones']['wolves']['hand']) | ("coins" not in game['zones']['ravens']['hand'])

    for i in range(300):
        game = take_a_turn(game, c)

        if 'message' in game:
            print("v"*80)
            print (game['message'])
            print("^"*80)

        if game['status'] == 'complete':
            print("!"*80)
            print("! WINNER on turn {}".format(i))
            print("!"*80)
            break
    print("FINISHED")

    assert False


def take_a_turn(game, c):
    # This is where the game play actually starts
    rv = client.get('/games/{}'.format(game['id']), headers={'X-Client-ID': c[game['active_player']]})
    game = json.loads(rv.data)

    p = game['active_player']

    hand = game['zones'][game['active_player']]['hand']
    only_choice = game.get('should_wait', {}).get('unit', False)
    if len(hand['coins']) > 0 or only_choice:
        use_coin = only_choice or choice(hand['coins'])

        print("{} is getting options for {} (only_choice: {}, hand: {})".format(p, use_coin, only_choice, hand['coins']))
        url = '/games/{}/action/{}'.format(game['id'], use_coin)
        rv = client.get(url, headers={'X-Client-ID': c[game['active_player']]})
        options = json.loads(rv.data)
        print("These are the options: ", options)

        coin, action, d = get_action(options['coin'], options['options'])
        data = {'action': action, 'data': d}
        url = '/games/{}/action/{}'.format(game['id'], coin)
        print("{} decided on using {} to {} ({}).".format(p, use_coin, action, data['data']))
    else:
        data = {'action': 'pass', 'data': None}
        url = '/games/{}/action/no-op'.format(game['id'])
        print("{} is forced to pass. coins: {} should_wait: {}".format(p, ))
    rv = client.post(url,
                     data=json.dumps(data),
                     headers={'X-Client-ID': c[game['active_player']], 'Content-Type': 'application/json'})
    game = json.loads(rv.data)
    print("\n\n")
    return game


def get_action(coin, options):

    def is_a_good_action(action, options):
        if not options[action]:
            return False

        if action in ['tactic', 'control', 'attack']:
            return True

        if action in ['move', 'deploy', 'recruit'] and randint(0, 10) < 7:
            return True

        if action in ['pass', 'initiative'] and randint(0, 10) < 1:
            return True

        # Never bolster cause computers are dumb
        return False

    action = choice(list(options.keys()))
    if not is_a_good_action(action, options):
        return get_action(coin, options)

    if isinstance(options[action], list):
        return (coin, action, choice(options[action]))

    if isinstance(options[action], dict):
        if action == 'tactic' and coin in ['ensign', 'marshall', 'heavycavalry', 'lancer', 'royaltoken']:
            coin_to_use = choice(list(options[action].keys()))
            return (coin, action, {coin_to_use: choice(options[action][coin_to_use])})

        coin_to_use = choice(list(options[action].keys()))
        return (coin_to_use, action, choice(options[action][coin_to_use]))

    return (coin, action, None)
