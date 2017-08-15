import argparse
from datetime import datetime, timezone, timedelta

from db.constant import KEY_APP_PKG_NAME, COLLECTION_PKG_NAMES, KEY_NAME, KEY_ACCESS_TIME, KEY_APP_VERSION, \
    COLLECTION_APP_VERSIONS, KEY_VALUE
from db.db_helper import DbHelper
from utils import log


class Query:
    def __init__(self):
        self.dh = DbHelper()

    def query_count_by_time(self, start, end):
        db_versions = list(self.dh.find(COLLECTION_APP_VERSIONS))
        s_tsp = self.__bjtime_to_timestamp(start)
        e_tsp = self.__bjtime_to_timestamp(end)
        c_names = self.dh.get_collection_names()
        p_names = [n.get(KEY_NAME) for n in self.dh.find(COLLECTION_PKG_NAMES)]
        lines = []
        for c in c_names:
            if 'crack' not in c:
                continue
            coll = self.dh.get_collection(c)
            for p in p_names:
                for pv in self.__get_versions_by_pkg(db_versions, p):
                    count = coll.count({KEY_APP_PKG_NAME: p,
                                        KEY_APP_VERSION: pv,
                                        KEY_ACCESS_TIME: {"$gte": s_tsp, "$lte": e_tsp}})
                    if count != 0:
                        self.__show(c, p, pv, count, lines)
        for l in lines:
            print(l, end='')
        print('done')

    def query_count(self):
        c_names = self.dh.get_collection_names()
        p_names = [n.get(KEY_NAME) for n in self.dh.find(COLLECTION_PKG_NAMES)]
        log.d('pkg_names: %s' % p_names)
        log.d('pkg_names len: %s' % len(p_names))
        for c in c_names:
            for p in p_names:
                count = self.dh.get_collection(c).count({KEY_APP_PKG_NAME: p})
                if count != 0:
                    self.__show(c, p, count)

    @staticmethod
    def __get_versions_by_pkg(db_versions, pkg):
        return list(v[KEY_VALUE] for v in db_versions if v[KEY_NAME] == pkg)

    @staticmethod
    def __bjtime_to_timestamp(time_str):
        time_format = "%Y%m%d_%H%M%S"
        time_str = '2017' + time_str
        dt = datetime.strptime(time_str, time_format)
        bj_tz = timezone(timedelta(hours=8))
        dt = dt.replace(tzinfo=bj_tz)
        print(dt)
        tsp = dt.timestamp()
        print(tsp)
        return tsp

    def __show(self, collection_name, pkg_name, pv, count, lines):
        line = ('%s %s %s %s \n' % (collection_name.ljust(40), pkg_name.ljust(40), str(pv).ljust(40), count))
        lines.append(line)
        # line.d('%s %s %s %s' % (collection_name.ljust(40), pkg_name.ljust(40), str(pv).ljust(40), count))


def parse_params():
    parser = argparse.ArgumentParser(description='query the crack db')
    parser.add_argument('-t', dest='time', nargs=2, help='query the count of records between start and end')
    args = parser.parse_args()

    if args.time:
        print(args.time)
        Query().query_count_by_time(args.time[0], args.time[1])


if __name__ == '__main__':
    parse_params()
