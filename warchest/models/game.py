# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from random import choice
import mongoengine
from mongoengine.fields import (
    DictField,
    StringField,
    EmbeddedDocumentField
)
from mongoengine.queryset.visitor import Q
from warchest.models.mixins import TimeTaggedDocument
from warchest.models.cards import Cards
from warchest.models.zones import Zone, PRIVATE, HIDDEN, PUBLIC
from warchest.errors import APIError
from warchest import get_client_id


COMPLETE = 'complete'
NEW = 'new'
IN_PROGRESS = 'in_progress'


class Game(TimeTaggedDocument, mongoengine.Document):

    # MONGOENGINE META OPTIONS
    meta = {
        'collection': 'games',
        'strict': False
    }

    status = StringField(required=True)
    wolves = StringField()
    ravens = StringField()
    initiative = StringField()
    zones = DictField()
    cards = EmbeddedDocumentField(Cards, null=True, required=False)

    @classmethod
    def make_new(cls):
        existing_game = cls.find_by_active_by_client()
        if existing_game:
            return existing_game

        return Game(
            wolves=get_client_id(),
            ravens=None,
            status=NEW
        ).save()

    @classmethod
    def find_by_active_by_client(cls):
        client_id = get_client_id()
        return cls.objects(Q(status__ne=COMPLETE) & (Q(wolves=client_id) | Q(ravens=client_id))).first()

    @classmethod
    def load(cls, id):
        try:
            game = cls.objects(id=id).first()
        except mongoengine.errors.ValidationError:
            pass

        if game:
            return game
        raise APIError("Game not found!", 404)

    @classmethod
    def find_by_status(cls, status):
        return cls.objects(status=status)

    def join(self):
        existing_game = self.find_by_active_by_client()
        if existing_game:
            raise APIError("Can't join game while you're already in one ({})".format(existing_game.id), 409)

        cards = Cards.new()

        def create_player_zones(client_id):
            return {
                'bag': Zone.new(client_id, HIDDEN),
                'hand': Zone.new(client_id, PRIVATE),
                'facedown': Zone.new(client_id, PRIVATE),
                'faceup': Zone.new(client_id, PUBLIC),
                'recruit': Zone.new(client_id, PUBLIC)
            }
        zones = {
            'wolves': create_player_zones(self.wolves),
            'ravens': create_player_zones(get_client_id()),
        }
        if self.modify(Q(status='new', ravens=None),
                       set__ravens=get_client_id(),
                       set__initiative=choice(['ravens', 'wolves']),
                       set__cards=cards,
                       set__zones=zones,
                       set__status=IN_PROGRESS):

            return True
        raise APIError("This game is already full. Sorry", 409)

    def your_turn(self):
        self.initiative = ('ravens' if self.initiative == 'wolves' else 'wolves')

    def is_it_my_turn(self):
        if ((self.initiative == 'wolves' and self.wolves != get_client_id()) or
           (self.initiative == 'ravens' and self.ravens != get_client_id())):
            raise APIError("It's not your turn", 420)

    def draw(self):
        if len(self.zones['wolves']['hand'].chips) > 0 or len(self.zones['ravens']['hand'].chips) > 0:
            return  # Its not time to draw yet

        # For each player, draw 3 chips
        for i in range(3):
            self.zones['wolves']['bag'].move(self.zones['wolves']['hand'])
            self.zones['ravens']['bag'].move(self.zones['ravens']['hand'])

    def to_dict(self):
        response = {
            "status": self.status,
            "id": str(self.id),
            "initiative": self.initiative,
            "wolves": self.wolves,  # TODO: UUID is secret
            "ravens": self.ravens   # TODO: UUID is secret
        }
        if self.cards:
            response['cards'] = self.cards.to_dict()

        if self.zones:
            response['zones'] = {
                "wolves": {
                    'bag': self.zones['wolves']['bag'].to_dict(),
                    'hand': self.zones['wolves']['hand'].to_dict(),
                    'facedown': self.zones['wolves']['facedown'].to_dict(),
                    'faceup': self.zones['wolves']['faceup'].to_dict(),
                    'recruit': self.zones['wolves']['recruit'].to_dict(),
                },
                "ravens": {
                    'bag': self.zones['ravens']['bag'].to_dict(),
                    'hand': self.zones['ravens']['hand'].to_dict(),
                    'facedown': self.zones['ravens']['facedown'].to_dict(),
                    'faceup': self.zones['ravens']['faceup'].to_dict(),
                    'recruit': self.zones['ravens']['recruit'].to_dict(),
                }
            }
        return response
