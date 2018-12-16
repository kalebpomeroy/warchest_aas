# 1 2 3 4 5 6 7
#       A
#     B   B
#   C   C   C
# D   D   D   D
#   E   E   E
# F   F   F   F
#   G   G   G
# H   H   H   H
#   I   I   I
# J   J   J   J
#   K   K   K
#     L   L
#       M
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import mongoengine
from warchest.models import units
from mongoengine.fields import (
    DictField,
    ListField
)
LETTER_LIST = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M']
POSITIONS_LIST = [
    [4],
    [3, 5],
    [2, 4, 6],
    [1, 3, 5, 7],
    [2, 4, 6],
    [1, 3, 5, 7],
    [2, 4, 6],
    [1, 3, 5, 7],
    [2, 4, 6],
    [1, 3, 5, 7],
    [2, 4, 6],
    [3, 5],
    [4]
]
CONTROL_POINTS = [
    'H1', 'H3', 'E2',  # Left Control Points
    'F7', 'F5', 'I9',  # Right Control Points
    'B3', 'C6',        # Ravens starting
    'K2', 'L5'         # Wolves starting
]

class Board(mongoengine.EmbeddedDocument):

    wolves = ListField()
    ravens = ListField()
    coins_on = DictField()

    @classmethod
    def new(cls):
        return cls(wolves=['K2', 'L5'], ravens=['B3', 'C6'])

    def to_dict(self):
        return {
            'coins_on': self.coins_on,
            'ravens': self.ravens,
            'wolves': self.wolves
        }

    # TODO: Get surrounding spaces

    def move(self, coin, to):
        unit = self.coins_on[coin]
        self.coins_on[to] = unit
        self.coins_on.pop(coin, None)

    def deploy(self, coin, space):
        if coin == units.FOOTMAN and coin in self.coins_on:
            coin = units.FOOTMAN_B

        self.coins_on[coin] = {
            'space': space,
            'coins': 1
        }

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
