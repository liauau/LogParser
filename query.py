import log
from db.constant import KEY_APP_PKG_NAME, COLLECTION_PKG_NAMES, KEY_NAME
from db.db_helper import DbHelper

dh = DbHelper()


def query_count():
    c_names = dh.get_collection_names()
    p_names = [n.get(KEY_NAME) for n in dh.find(COLLECTION_PKG_NAMES)]
    for c in c_names:
        for p in p_names:
            count = dh.get_collection(c).count({KEY_APP_PKG_NAME: p})
            if count != 0:
                show(c, p, count)


def show(collection_name, pkg_name, count):
    log.i('%s %s %s' % (collection_name.ljust(40), pkg_name.ljust(40), count))
    # log.d(collection_name.ljust(40), pkg_name.ljust(40), str(count))


if __name__ == '__main__':
    query_count()
