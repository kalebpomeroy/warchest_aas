# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import mongoengine
from random import choice
from mongoengine.fields import (
    ListField,
    StringField
)
from warchest import get_client_id
from warchest.models import units


PRIVATE = "private"  # Only the owner can the contents
PUBLIC = "public"    # Everyone can see the contents
HIDDEN = "hidden"    # No one can see the contents


class Zone(mongoengine.EmbeddedDocument):

    owner = StringField()
    coins = ListField()
    visibility = StringField()

    @classmethod
    def new(cls, owner, visibility):
        return cls(owner=owner, visibility=visibility, coins=[])

    def move_all(self, new_zone):
        for coin in self.coins:
            self.move(new_zone, coin)

    def move(self, new_zone, coin=None):
        if len(self.coins) == 0:
            return

        if not coin:
            coin = choice(self.coins)

        new_zone.add(coin)
        self.remove(coin)
        return coin

    def add(self, coin):
        self.coins.append(get_coin_name(coin))

    def remove(self, coin):
        self.coins.remove(get_coin_name(coin))

    def to_dict(self):
        zone = {
            'count': len(self.coins)
        }

        if self.visibility == PUBLIC or (self.visibility == PRIVATE and get_client_id() == self.owner):
            zone['coins'] = self.coins

        return zone


def get_coin_name(coin):
    if coin == units.FOOTMAN_B:
        return units.FOOTMAN
    return coin
