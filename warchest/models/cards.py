# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from random import sample
import mongoengine
from mongoengine.fields import (
    ListField
)
from warchest.models import units
from warchest.models import game
from warchest.errors import APIError


class Cards(mongoengine.EmbeddedDocument):

    draft = ListField()
    wolves = ListField()
    ravens = ListField()

    @classmethod
    def new(cls):
        return Cards(
            draft=sample(units.UNITS.keys(), 8),
            wolves=[],
            ravens=[]
        )

    # At the start of the game, this gets the tokens setup
    def setup_coins(self):
        self._instance['zones']['wolves']['bag'].add(units.ROYAL_TOKEN)
        self._instance['zones']['ravens']['bag'].add(units.ROYAL_TOKEN)
        for unit in self.wolves:
            self._instance['zones']['wolves']['bag'].add(unit)
            self._instance['zones']['wolves']['bag'].add(unit)
            for i in range(units.UNITS[unit]['count']-2):
                self._instance['zones']['wolves']['recruit'].add(unit)
        for unit in self.ravens:
            self._instance['zones']['ravens']['bag'].add(unit)
            self._instance['zones']['ravens']['bag'].add(unit)
            for i in range(units.UNITS[unit]['count']-2):
                self._instance['zones']['ravens']['recruit'].add(unit)

    def to_dict(self):
        return {
            'draft': self.draft,
            'wolves': self.wolves,
            'ravens': self.ravens
        }

    def do_draft(self, pick):
        self._instance.is_it_my_turn()

        if pick not in self.draft:
            raise APIError("Can't draft a card not in the list {} ({}).".format(pick, self.draft), 400)

        self.draft.remove(pick)
        self[self._instance.active_player].append(pick)

        if len(self.draft) in [7, 5, 3, 1]:
            self._instance.your_turn(drafting=True)

        # If there's one left, give it to the next player
        if len(self.draft) == 1:
            self[self._instance.active_player].append(self.draft[0])
            self.draft = []
            self._instance.cards.setup_coins()
            self._instance.new_round()
            self._instance.status = game.IN_PROGRESS

        self._instance.save()
