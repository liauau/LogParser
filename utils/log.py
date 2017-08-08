import logging

from env import DEBUG

logging.root.setLevel(level=logging.INFO)
logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')


def d(msg, *args):
    if DEBUG:
        print(msg)
        # logging.debug(msg, *args)


def i(msg, *args):
    if DEBUG:
        logging.info(msg, *args)
