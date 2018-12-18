from warchest.errors import APIError
from warchest.models import units
from warchest.hexes import Hex, HEX_DIRECTIONS
from warchest.models.board import CONTROL_POINTS

PASS = 'pass'
INITIATIVE = 'initiative'
RECRUIT = 'recruit'
DEPLOY = 'deploy'
BOLSTER = 'bolster'
MOVE = 'move'
CONTROL = 'control'
ATTACK = 'attack'
TACTIC = 'tactic'
SAVE = 'save'  # This is the action taken to save the royal guard by using recruits when attacked

FACEUP_ACTIONS = [MOVE, CONTROL, ATTACK, TACTIC]
BOARD_ACTIONS = [DEPLOY, BOLSTER]
FACEDOWN_ACTIONS = [PASS, INITIATIVE, RECRUIT]

NO_OP = 'no-op'


def get_possible(game, coin):
    game.is_it_my_turn()
    waiting = are_we_waiting(game, coin)
    if waiting:
        return waiting

    zones = game.zones[game.active_player]

    if coin == NO_OP:
        if len(zones['hand'].coins) != 0:
            raise APIError("You have to do something")

        return {
            'coin': NO_OP,
            'options': {
                PASS: True
            }
        }

    # FOOTMAN B is a footman for this check
    if coin not in zones['hand']['coins']:
        if not game.should_wait:
            if coin == units.FOOTMAN_B and units.FOOTMAN not in zones['hand']['coins']:
                raise APIError("Can't do hypothecticals with {} ({})".format(coin, zones['hand']['coins']), 410)
            print("Counting footman b as footman")

        if game.should_wait and game.should_wait['unit'] != coin:
            raise APIError("We're waiting on {}, can't do {}".format(game.should_wait['unit'], coin), 409)

    actions = _get_facedown_actions(game, zones)
    actions.update(_get_deployment_actions(game, coin))
    actions.update(_get_activation_actions(game, coin))
    return {'coin': coin, 'options': actions}


def _get_activation_actions(game, coin):

    coins = game.board.get_coins_spaces(coin)
    if len(coins) == 0:
        tactics = {}
        if coin == units.ROYAL_TOKEN:
            tactics = {TACTIC: _get_tactic(game, {units.ROYAL_TOKEN: {}})}
        return tactics

    return {
        CONTROL: _get_control(game, coins),
        MOVE: _get_moves(game, coins),
        ATTACK: _get_attacks(game, coins),
        TACTIC: _get_tactic(game, coins),
    }


def _get_control(game, coins):
    controls = []
    for name, pos in coins.items():
        if pos in CONTROL_POINTS and pos not in game.board[game.active_player]:
            controls.append(name)
    return controls or False


def _get_moves(game, coins):
    movement = {}

    for name, pos in coins.items():
        options = [hex for hex in game.board.get_adjacent(pos) if not game.board.what_is_on(hex)]
        if len(options) > 0:
            movement[name] = options

    return movement or False


def _get_attacks(game, coins):
    attacks = {}

    for name, pos in coins.items():

        if name in [units.ARCHER, units.LANCER]:
            return False

        enemies = []
        # for each adjacent space, check to see if it has an enemy
        for hex in game.board.get_adjacent(pos):
            coin = game.board.what_is_on(hex)
            if not coin:
                continue

            if coin[1]['owner'] != game.active_player:

                if coin[0] == units.KNIGHT and game.board.coins_on[name]['coins'] == 1:
                    continue

                enemies.append(hex)

        if len(enemies) > 0:
            attacks[name] = enemies

    return attacks or False


def _get_tactic(game, coins):

    name, pos = coins.popitem()

    if name == units.LIGHT_CAVALRY:

        first_moves = [hex for hex in game.board.get_adjacent(pos) if not game.board.what_is_on(hex)]
        moves = []
        for move in first_moves:
            moves = moves + [_hex for _hex in game.board.get_adjacent(move) if not game.board.what_is_on(_hex)]

        return list(set(moves)) or False

    if name == units.HEAVY_CAVALRY:

        first_moves = [hex for hex in game.board.get_adjacent(pos) if not game.board.what_is_on(hex)]
        targets = {}
        for move in first_moves:
            enemies = []
            for _hex in game.board.get_adjacent(move):
                target_unit = game.board.what_is_on(_hex)
                if target_unit and target_unit[1]['owner'] != game.active_player:
                    enemies.append(target_unit[1]['space'])
            if enemies:
                targets[str(move)] = enemies

        return targets or False

    if name == units.ARCHER:
        targets = []
        for target_space in Hex(pos).hexes_within_n(2, at_least=2):

            target_unit = game.board.what_is_on(target_space)
            if target_unit and target_unit[1]['owner'] != game.active_player:
                targets.append(target_space)

        return list(set(targets)) or False

    if name == units.ROYAL_TOKEN:
        guard = game.board.coins_on.get(units.ROYAL_GUARD)
        if not guard or guard['owner'] != game.active_player:
            return False
        return _get_moves(game, {units.ROYAL_GUARD: guard['space']})[units.ROYAL_GUARD]

    if name == units.CROSSBOWMAN:
        targets = []
        my_spot = Hex(pos)
        for d, h in HEX_DIRECTIONS.items():
            next_space = my_spot.add(h)
            if not next_space or game.board.what_is_on(next_space):
                continue

            next_space = my_spot.add(h)
            if not next_space:
                continue

            next_next_space = next_space.add(h)
            if not next_next_space:
                continue

            target_unit = game.board.what_is_on(game.board.what_is_on(next_next_space))
            if target_unit:
                if target_unit[1]['owner'] != game.active_player:
                    targets[next_space] = next_next_space

    if name == units.LANCER:
        targets = {}
        my_spot = Hex(pos)
        for d, h in HEX_DIRECTIONS.items():
            next_space = my_spot.add(h)
            if not next_space or game.board.what_is_on(next_space):
                continue

            next_space = my_spot.add(h)
            if not next_space:
                continue

            next_next_space = next_space.add(h)
            if not next_next_space:
                continue

            target_unit = game.board.what_is_on(game.board.what_is_on(next_next_space))
            if target_unit:
                if target_unit[1]['owner'] != game.active_player:
                    targets[str(next_space)] = next_next_space
            else:
                next_space = my_spot.add(h)
                if not next_space:
                    continue

                next_next_space = next_space.add(h)
                if not next_next_space:
                    continue
                target_unit = game.board.what_is_on(game.board.what_is_on(next_next_space))
                if target_unit and target_unit[1]['owner'] != game.active_player:
                        targets[str(next_space)] = next_next_space

        return targets or False

    if name == units.MARSHALL:
        targets = {}
        for target_space in Hex(pos).hexes_within_n(2):
            target_unit = game.board.what_is_on(target_space)
            if target_unit and target_unit[1]['owner'] == game.active_player:
                attacks = _get_attacks(game, {target_unit[0]: target_unit[1]['space']})
                if attacks:
                    targets[target_unit[0]] = attacks

        return targets or False

    if name == units.ENSIGN:
        targets = {}
        for target_space in Hex(pos).hexes_within_n(2):
            target_unit = game.board.what_is_on(target_space)
            if target_unit and target_unit[1]['owner'] == game.active_player:
                possible_moves = _get_moves(game, {target_unit[0]: target_unit[1]['space']})
                if not possible_moves:
                    continue
                moves = [m for m in possible_moves[target_unit[0]] if Hex(pos).distance(Hex(m)) <= 2]
                if moves:
                    targets[target_unit[0]] = moves

        return targets or False

    return False


def _get_deployment_actions(game, coin):
    bolster = False
    deploy = False

    if coin == units.ROYAL_TOKEN:
        return {
            DEPLOY: False,
            BOLSTER: False
        }
    # Is the unit on the board?
    spaces = game.board.get_coins_spaces(coin)
    if len(spaces) > 0:
        bolster = list(spaces.values())

    if len(spaces) == 0 or (len(spaces) == 1 and coin == units.FOOTMAN):
        deploy = []
        for cp in game.board[game.active_player]:
            if not game.board.what_is_on(cp):
                deploy.append(cp)

        if coin == units.SCOUT:
            for c, unit in game.board.coins_on.items():
                if unit['owner'] == game.active_player:
                    for adj in game.board.get_adjacent(unit['space']):
                        if adj not in deploy and not game.board.what_is_on(adj):
                            deploy.append(adj)

        if len(deploy) == 0:
            deploy = False

    return {
        DEPLOY: deploy,
        BOLSTER: bolster
    }


def _get_facedown_actions(game, zones):
    initiative = False
    recruit = False

    if len(zones['recruit'].coins) > 0:
        recruit = list(set(zones['recruit'].coins))

    if game.initiative != game.active_player and not game.initiative_taken_this_round:
        initiative = True

    return {
        PASS: True,  # You can always pass
        INITIATIVE: initiative,
        RECRUIT: recruit,
    }


def check_action(game, coin, action, data):

    possibles_options = get_possible(game, coin)
    possible_coin = possibles_options['coin']
    possibles = possibles_options['options']

    if possible_coin != coin or action not in possibles:
        print("Trying to {} with {} ({})".format(action, coin, data))
        print("POSSIBLES: ", possibles)
        raise APIError("Not a valid action", 400)

    if not possibles[action]:
        raise APIError("Action not possible", 400)

    if isinstance(possibles[action], list) and data not in possibles[action]:
        raise APIError("Option not in list of choices", 400)

    if isinstance(possibles[action], dict):
        if action != TACTIC and coin not in possibles[action] and data not in possibles[action][coin]:
            raise APIError("Option not in dict of choices", 400)
        elif action == TACTIC:
            key = list(data.keys())[0]
            if key not in possibles[action] or data[key] not in possibles[action][key]:
                raise APIError("Can't do a tactic like that")


def execute(game, coin, action, data=None):
    # Is the action allowed right now?
    game.is_it_my_turn()
    check_action(game, coin, action, data)

    # Is this a freebie action?
    is_freebie = game.should_wait

    # Discard/Deploy the chip appropriately (assuming its not a freebie action)
    zones = game.zones[game.active_player]
    if not is_freebie or is_freebie['unit'] == units.WARRIOR_PRIEST:
        if action in FACEDOWN_ACTIONS and coin != NO_OP:
            zones['hand'].move(zones['facedown'], coin=coin)
        elif action in BOARD_ACTIONS:
            zones['hand'].remove(coin=coin)
        elif action in FACEUP_ACTIONS:
            zones['hand'].move(zones['faceup'], coin=coin)

    # Do whatever the action is
    do_action(game, coin, action, data)

    # Make sure the zones are set appropriately
    game.set_zones(zones)

    if not should_wait(game, coin, action, data):
        game.your_turn()

    game.save()


def do_action(game, coin, action, data):
    if action == PASS:
        return True

    if action == INITIATIVE:
        return game.take_initiative()

    if action == RECRUIT:
        zones = game.zones[game.active_player]
        return zones['recruit'].move(zones['faceup'], coin=data)

    if action == DEPLOY:
        return game.board.deploy(coin, data)

    if action == BOLSTER:
        return game.board.bolster(coin, data)

    if action == MOVE:
        return game.board.move(coin, data)

    if action == ATTACK:
        game.board.attack(coin, data)
        if coin == units.SWORDSMAN:
            game.waiton = units.SWORDSMAN
            return False

    if action == CONTROL:
        return game.board.control(data)

    if action == TACTIC:
        if coin == units.LIGHT_CAVALRY:
            return game.board.move(coin, data)

        if coin in [units.ARCHER, units.CROSSBOWMAN]:
            return game.board.attack(coin, data, ranged=True)

        if coin == units.ENSIGN:
            unit = list(data.keys())[0]
            return game.board.move(unit, data[unit])

        if coin == units.MARSHALL:
            unit = list(data.keys())[0]
            return game.board.attack(unit, data[unit])

        if coin == units.ROYAL_TOKEN:
            return game.board.move(units.ROYAL_GUARD, data)

        if coin in [units.LANCER, units.HEAVY_CAVALRY]:
            move_to = list(data.keys())[0]
            move_to_hex = Hex([int(i) for i in move_to.split(",")])
            game.board.move(coin, move_to_hex)
            return game.board.attack(coin, data[move_to])

    if action == SAVE:
        if data:
            return zones['recruit'].remove(units.ROYAL_GUARD)
        else:
            game.board.attack(None, game.board.coins_on[units.ROYAL_GUARD]['space'])


def should_wait(game, coin, action, data):
    if coin == units.SWORDSMAN and action == ATTACK:
        game.should_wait = {'unit': units.SWORDSMAN}
    elif action == RECRUIT and data == units.MERCENARY and game.board.coins_on.get(units.MERCENARY):
        game.should_wait = {'unit': units.MERCENARY}
    elif coin == units.WARRIOR_PRIEST and action in [CONTROL, ATTACK]:
        game.should_wait = {'unit': units.WARRIOR_PRIEST, 'data': game.draw(game.active_player)}
    # elif coin == units.BERSERKER and action in [CONTROL, ATTACK, MOVE]:
    #     game.should_wait = {'unit': units.BERSERKER}
    elif coin == units.FOOTMAN and action == TACTIC:
        game.should_wait = {'unit': units.FOOTMAN_B}
    else:
        game.should_wait = None
    return game.should_wait


def are_we_waiting(game, coin):
    if not game.should_wait:
        return False

    if game.should_wait['unit'] == units.ROYAL_GUARD:
        options = {
            'coin': coin,
            SAVE: [True, False]
        }

    if game.should_wait['unit'] == units.WARRIOR_PRIEST:
        if coin == game.should_wait['data']:
            return False

        coin = game.should_wait['data']
        return {'coin': coin, 'options': get_possible(game, coin)['options']}

    if game.should_wait['unit'] == units.FOOTMAN:
        coin = units.FOOTMAN_B

    coins = game.board.get_coins_spaces(coin)

    # Swordsman, Mercenary, Berserker, and Footman can all move/pass
    options = {
        PASS: True,
        MOVE: _get_moves(game, coins)
    }

    if game.should_wait['unit'] in [units.MERCENARY, units.BERSERKER, units.FOOTMAN]:
        options[CONTROL] = _get_control(game, coins)
        options[ATTACK] = _get_attacks(game, coins)

    return {'coin': game.should_wait['unit'], 'options': options}
