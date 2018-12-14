# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import mongoengine
from random import choice
from mongoengine.fields import (
    ListField,
    StringField
)
from warchest import get_client_id


PRIVATE = "private"  # Only the owner can the contents
PUBLIC = "public"    # Everyone can see the contents
HIDDEN = "hidden"    # No one can see the contents


class Zone(mongoengine.EmbeddedDocument):

    owner = StringField()
    chips = ListField()
    visibility = StringField()

    @classmethod
    def new(cls, owner, visibility):
        return cls(owner=owner, visibility=visibility, chips=[])

    def move(self, new_zone, chip=None):
        if len(self.chips) == 0:
            return

        if not chip:
            chip = choice(self.chips)

        new_zone.add(chip)
        self.remove(chip)

    def add(self, chip):
        self.chips.append(chip)

    def remove(self, chip):
        self.chips.remove(chip)

    def to_dict(self):
        zone = {
            'count': len(self.chips)
        }

        if self.visibility == PUBLIC or (self.visibility == PRIVATE and get_client_id() == self.owner):
            zone['chips'] = self.chips

        return zone
