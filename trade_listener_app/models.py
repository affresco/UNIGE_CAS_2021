import datetime as dt
from django.db import models
from django.utils.translation import ugettext_lazy as _

import hashlib

class TradeData(models.Model):
    """
    This model represents a single trade received by the listener.
    """

    class Meta:
        verbose_name = _('Trade Data')
        verbose_name_plural = _('Trades Data')

    # User id
    user_id = models.IntegerField(db_index=True)

    # Sequencing
    trade_id = models.CharField(max_length=64)
    trade_seq = models.CharField(max_length=64)

    # Timestamp
    timestamp = models.IntegerField(db_index=True)

    # Instrument
    currency = models.CharField(max_length=8, db_index=True)
    instrument_name = models.CharField(max_length=64, db_index=True)

    # Price
    price = models.FloatField()
    quantity = models.FloatField()
    direction = models.IntegerField()

    # Identification
    index_price = models.FloatField()

    # Hash
    hash = models.CharField(max_length=256, null=True)

    @classmethod
    def compute_hash(cls, **kwargs):
        condensed = ""
        for _, v in kwargs.items():
            condensed += str(v)
        return hashlib.sha224(str.encode(condensed)).hexdigest()
