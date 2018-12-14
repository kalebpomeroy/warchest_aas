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


class Board(mongoengine.EmbeddedDocument):

    control_points = [
        'H1', 'H3', 'E2',  # Left Control Points
        'F7', 'F5', 'I9',  # Right Control Points
        'B3', 'C6',        # Ravens starting
        'K2', 'L5'         # Wolves starting
    ]
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

    def deploy(self, coin, space):
        self.coins_on[coin] = {
            'space': space,
            'coins': 1
        }

    def bolster(self, coin, space):
        if coin == units.FOOTMAN:
            coin = self.which_footman(space)

        self.coins_on[coin]['coins'] = self.coins_on[coin]['coins'] + 1

    def get_coins_spaces(self, name):
        spaces = []
        if name in self.coins_on:
            spaces.append(self.coins_on[name]['space'])

        if name == units.FOOTMAN and units.FOOTMAN_B in self.coins_on:
            spaces.append(self.coins_on[units.FOOTMAN_B]['space'])

        return spaces

    def which_footman(self, space):
        if self.coins_on[units.FOOTMAN]['space'] == space:
            return units.FOOTMAN
        return units.FOOTMAN_B
