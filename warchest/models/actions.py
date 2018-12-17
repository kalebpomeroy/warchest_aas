from warchest.errors import APIError
from warchest.models import units
from warchest.hexes import Hex
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

FACEUP_ACTIONS = [MOVE, CONTROL, ATTACK, TACTIC]
BOARD_ACTIONS = [DEPLOY, BOLSTER]
FACEDOWN_ACTIONS = [PASS, INITIATIVE, RECRUIT]

NO_OP = 'no-op'


def get_possible(game, coin):
    game.is_it_my_turn()
    zones = game.zones[game.active_player]

    if coin == NO_OP:
        if len(zones['hand'].coins) != 0:
            raise APIError("You have to do something")

        return {
            PASS: True
        }

    if coin not in zones['hand']['coins']:

        raise APIError("Can't do hypothecticals with {} ({})".format(coin, zones['hand']['coins']), 410)

    actions = _get_facedown_actions(game, zones)
    actions.update(_get_deployment_actions(game, coin))
    actions.update(_get_activation_actions(game, coin))
    return actions


def _get_activation_actions(game, coin):

    coins = game.board.get_coins_spaces(coin)
    if len(coins) == 0:
        return {}

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

        return list(set(moves))

    if name == units.ARCHER:
        targets = []
        for target_space in Hex(pos).hexes_within_n(2, at_least=2):

            target_unit = game.board.what_is_on(target_space)
            if target_unit and target_unit[1]['owner'] != game.active_player:
                targets.append(target_space)

        return list(set(targets)) or False

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

    possibles = get_possible(game, coin)

    if action not in possibles:
        raise APIError("Not a valid action", 400)

    if not possibles[action]:
        raise APIError("Action not possible", 400)

    if isinstance(possibles[action], list) and data not in possibles[action]:
        raise APIError("Option not in list of choices", 400)

    if isinstance(possibles[action], dict) and coin not in possibles[action] and data not in possibles[action][coin]:
        raise APIError("Option not in dict of choices", 400)


def execute(game, coin, action, data=None):
    # Is the action allowed right now?
    game.is_it_my_turn()
    check_action(game, coin, action, data)

    # Discard/Deploy the chip appropriately
    zones = game.zones[game.active_player]
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

    # If result puts the game into a weird state, handle that here
    game.your_turn()

    game.save()


def do_action(game, coin, action, data):
    if action == PASS:
        return

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
        return game.board.attack(coin, data)

    if action == CONTROL:
        return game.board.control(data)

    if action == TACTIC:
        if coin == units.LIGHT_CAVALRY:
            return game.board.move(coin, data)

        if coin == units.ARCHER:
            return game.board.attack(coin, data, ranged=True)
