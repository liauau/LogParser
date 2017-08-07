import logging

from db.worker import DEBUG


def d(msg, *args):
    if DEBUG:
        logging.debug(msg, *args)


def i(msg, *args):
    if DEBUG:
        logging.info(msg, *args)
