# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from mongoengine.fields import DateTimeField


class TimeTaggedDocument(object):
    """ This class serves as a base for models which should have their creation
        timestamp, as well as an `updated_at` timestamp attached.
        This class should not be instantiated by itself!
    """

    # MONGOENGINE FIELDS
    created_at = DateTimeField(db_field="_tim", required=True, default=datetime.utcnow)
    updated_at = DateTimeField()

    @classmethod
    def pre_save(cls, sender, document, **kw):
        document.updated_at = datetime.utcnow()
