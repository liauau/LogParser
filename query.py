from datetime import datetime, timezone, timedelta

from db.constant import KEY_APP_PKG_NAME, COLLECTION_PKG_NAMES, KEY_NAME, KEY_ACCESS_TIME
from db.db_helper import DbHelper
from utils import log

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


def query_count_by_time(start, end):
    s_tsp = bjtime_to_timestamp(start)
    e_tsp = bjtime_to_timestamp(end)
    c_names = dh.get_collection_names()
    p_names = [n.get(KEY_NAME) for n in dh.find(COLLECTION_PKG_NAMES)]
    for c in c_names:
        if 'crack' not in c:
            continue
        for p in p_names:
            count = dh.get_collection(c).count({KEY_ACCESS_TIME: {"$gte": s_tsp, "$lte": e_tsp}, KEY_APP_PKG_NAME: p})
            if count != 0:
                show(c, p, count)
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


def show(collection_name, pkg_name, count):
    log.d('%s %s %s' % (collection_name.ljust(40), pkg_name.ljust(40), count))


if __name__ == '__main__':
    # query_count()
    query_count_by_time('0807_140000', '0807_150000')
