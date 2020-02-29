# coding=utf-8
import logging
from datetime import datetime, timedelta

__author__ = 'ThucNC'
_logger = logging.getLogger(__name__)


def now_plus_30_days():
    now = datetime.now()
    next_30_days = now + timedelta(days=30)
    return next_30_days
