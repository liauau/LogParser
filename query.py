import log
from db.db_helper import DbHelper

dh = DbHelper()


def query_count_by_pkg_name(pkg_name):
    cs = dh.get_all_collections()
    for c in cs:
        count = dh.get_collection(c).count({'app_pkg_name': pkg_name})
        if count != 0:
            log.p(c.ljust(40), pkg_name.ljust(40), count, sep="\t")


def get_pkg_names():
    cs = dh.get_all_collections()
    pkg_names = []
    for c in cs:
        for r in dh.find(c):
            pkg_names.append(r['app_pkg_name'])
    pkg_names = list(set(pkg_names))
    return pkg_names


def go():
    for pn in PKG_NAME_LIST:
        query_count_by_pkg_name(pn)


PKG_NAME_LIST = get_pkg_names()

if __name__ == '__main__':
    go()
