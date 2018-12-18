
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import mongoengine
from warchest.models import units
from warchest.hexes import Hex
from mongoengine.fields import (
    DictField,
    ListField
)

CONTROL_POINTS = [
    (-2, 0, 2), (-1, 1, 0), (-3, 2, 1),   # Left Control Points
    (2, 0, -2), (1, -1, 0), (3, -2, -1),  # Right Control Points
    (-1, -2, 3), (2, -3, 1),                 # Ravens starting
    (-2, 3, -1), (1, 2, -3)                  # Wolves starting
]


class Board(mongoengine.EmbeddedDocument):

    wolves = ListField()
    ravens = ListField()
    coins_on = DictField()

    @classmethod
    def new(cls):
        return cls(wolves=[(-2, 3, -1), (1, 2, -3)], ravens=[(-1, -2, 3), (2, -3, 1)])

    def to_dict(self):
        return {
            'coins_on': self.coins_on,
            'ravens': self.ravens,
            'wolves': self.wolves
        }

    def move(self, coin, to):
        self.coins_on[coin]['space'] = to

    def attack(self, attacker, target, ranged=False):
        coin, unit = self.what_is_on(target)
        if coin == units.PIKEMAN and not ranged:
            self.attack(None, self.coins_on[attacker]['space'])
        if coin == units.ROYAL_GUARD:
            if self._instance.zones[unit['owner']]['recruit'].coins.count(units.ROYAL_GUARD) > 0:
                return self._instance.should_wait == units.ROYAL_GUARD

        if unit['coins'] == 1:
            return self.coins_on.pop(coin)

        unit['coins'] = unit['coins'] - 1
        self.coins_on[coin] = unit

    def deploy(self, coin, space):
        if coin == units.FOOTMAN and coin in self.coins_on:
            coin = units.FOOTMAN_B

        self.coins_on[coin] = {
            'owner': self._instance.active_player,
            'space': space,
            'coins': 1
        }

    def get_adjacent(self, coordinates):
        return Hex(coordinates).hexes_within_n(1)

    def what_is_on(self, space):
        for coin, unit in self.coins_on.items():
            if unit['space'] == space:
                return (coin, unit)

        return False

    def control(self, coin):
        if self._instance.active_player == 'wolves':
            friendly = self.wolves
            enemy = self.ravens

        if self._instance.active_player == 'ravens':
            friendly = self.ravens
            enemy = self.wolves

        friendly.append(self.coins_on[coin]['space'])
        if self.coins_on[coin] in enemy:
            enemy.remove(self.coins_on[coin]['space'])

        if len(friendly) >= 6:
            self._instance.win()

    def bolster(self, coin, space):
        if coin == units.FOOTMAN:
            coin = self.which_footman(space)

        self.coins_on[coin]['coins'] = self.coins_on[coin]['coins'] + 1

    def get_coins_spaces(self, name):
        spaces = {}
        if name in self.coins_on:
            spaces[name] = self.coins_on[name]['space']

        if name == units.FOOTMAN and units.FOOTMAN_B in self.coins_on:
            spaces[units.FOOTMAN_B] = self.coins_on[units.FOOTMAN_B]['space']

        return spaces

    def which_footman(self, space):
        if self.coins_on[units.FOOTMAN]['space'] == space:
            return units.FOOTMAN
        return units.FOOTMAN_B
