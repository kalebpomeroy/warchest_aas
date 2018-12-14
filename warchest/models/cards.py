# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from random import sample
import mongoengine
from mongoengine.fields import (
    ListField
)
from warchest.models import units
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

    def do_draft(self, picks):
        self._instance.is_it_my_turn()

        if len(self.draft) == 0:
            raise APIError("We're not drafting right now, that doesn't make sense", 409)
        elif len(self.draft) == 8:
            if len(picks) != 1:
                raise APIError("Your first pick has to be exactly one card", 400)
        else:
            if len(picks) != 2:
                raise APIError("You should be picking exactly two cards here", 400)

            if picks[0] == picks[1]:
                raise APIError("You can't pick the same card twice dummy", 400)

        for pick in picks:
            if pick not in self.draft:
                raise APIError("Can't draft a card not in the list.", 400)

        # All the pre-reqs check out, ready to play
        for pick in picks:
            self.draft.remove(pick)
            self[self._instance.active_player].append(pick)

        self._instance.your_turn(drafting=True)

        # If there's one left, give it to the next player
        if len(self.draft) == 1:
            self[self._instance.active_player].append(self.draft[0])
            self.draft = []
            self._instance.cards.setup_coins()
            self._instance.new_round()

        self._instance.save()
