import argparse
from datetime import datetime, timezone, timedelta

from db.constant import KEY_APP_PKG_NAME, COLLECTION_PKG_NAMES, KEY_NAME, KEY_ACCESS_TIME, KEY_APP_VERSION
from db.db_helper import DbHelper
from utils import log
from pprint import pprint

dh = DbHelper()


def query_count():
    c_names = dh.get_collection_names()
    p_names = [n.get(KEY_NAME) for n in dh.find(COLLECTION_PKG_NAMES)]
    log.d('pkg_names: %s' % p_names)
    log.d('pkg_names len: %s' % len(p_names))
    for c in c_names:
        for p in p_names:
            count = dh.get_collection(c).count({KEY_APP_PKG_NAME: p})
            if count != 0:
                show(c, p, count)


def query_pkg_versions():
    c_names = dh.get_collection_names()
    p_names = [n.get(KEY_NAME) for n in dh.find(COLLECTION_PKG_NAMES)]
    pvs = dict().fromkeys(p_names, [])
    for p in p_names:
        rs = []
        for c in c_names:
            if 'crack' not in c:
                continue
            rs.extend(list(dh.get_collection(c).find({KEY_APP_PKG_NAME: p})))
        versions = list(set(r[KEY_APP_VERSION] for r in rs))
        pvs[p] = versions
    # pprint(pvs)
    return pvs


def query_count_by_time(start, end):
    pvs = query_pkg_versions()
    s_tsp = bjtime_to_timestamp(start)
    e_tsp = bjtime_to_timestamp(end)
    c_names = dh.get_collection_names()
    p_names = [n.get(KEY_NAME) for n in dh.find(COLLECTION_PKG_NAMES)]
    for c in c_names:
        if 'crack' not in c:
            continue
        for p in p_names:
            for pv in pvs[p]:
                count = dh.get_collection(c).count({KEY_ACCESS_TIME: {"$gte": s_tsp, "$lte": e_tsp}, KEY_APP_PKG_NAME: p, KEY_APP_VERSION: pv})
                if count != 0:
                    show(c, p, pv, count)
    print('done')


def bjtime_to_timestamp(time_str):
    time_format = "%Y%m%d_%H%M%S"
    time_str = '2017' + time_str
    dt = datetime.strptime(time_str, time_format)
    bj_tz = timezone(timedelta(hours=8))
    dt = dt.replace(tzinfo=bj_tz)
    print(dt)
    tsp = dt.timestamp()
    print(tsp)
    return tsp


def show(collection_name, pkg_name, pv, count):
    log.d('%s %s %s %s' % (collection_name.ljust(40), pkg_name.ljust(40), str(pv).ljust(40), count))


def parse_params():
    parser = argparse.ArgumentParser(description='query the crack db')
    parser.add_argument('-t', dest='time', nargs=2, help='query the count of records between start and end')
    args = parser.parse_args()

    if args.time:
        print(args.time)
        query_count_by_time(args.time[0], args.time[1])


if __name__ == '__main__':
    # query_pkg_versions()
    parse_params()
