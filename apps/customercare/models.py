from datetime import datetime

from django.db import models

from sumo.models import ModelBase


class Tweet(ModelBase):
    """An entry on twitter."""
    tweet_id = models.BigIntegerField()
    raw_json = models.TextField()
    created = models.DateTimeField(default=datetime.now, db_index=True)

    class Meta:
        ordering = ('-created',)
