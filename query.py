import argparse
from datetime import datetime, timezone, timedelta

from db.constant import KEY_APP_PKG_NAME, COLLECTION_PKG_NAMES, KEY_NAME, KEY_ACCESS_TIME, KEY_APP_VERSION, \
    COLLECTION_APP_VERSIONS, KEY_VALUE, KEY_ID, KEY_COUNT
from db.db_helper import DbHelper
from bson.son import SON


class Query:
    def __init__(self):
        self.dh = DbHelper()

    def query_count(self, collection_name, start, end):
        s_tsp = self.__bjtime_to_timestamp(start)
        e_tsp = self.__bjtime_to_timestamp(end)
        coll = self.dh.get_collection(collection_name)
        pipeline = [
            {"$match": {KEY_ACCESS_TIME: {"$gt": s_tsp, "$lte": e_tsp}}},
            {"$group": {KEY_ID: {KEY_APP_PKG_NAME: "$app_pkg_name", KEY_APP_VERSION: "$app_version"}, KEY_COUNT: {"$sum": 1}}},
            {"$sort": SON([(KEY_COUNT, -1), (KEY_ID, 1)])}
        ]
        result = list(coll.aggregate(pipeline))
        for r in result:
            pkg = r.get(KEY_ID).get(KEY_APP_PKG_NAME)
            version = r.get(KEY_ID).get(KEY_APP_VERSION)
            count = r.get(KEY_COUNT)
            if pkg:
                line = ('%s %s %s %s \n' % (collection_name.ljust(40), pkg.ljust(80), str(version).ljust(40), count))
                print(line, end='')
        print('done')

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


def parse_params():
    parser = argparse.ArgumentParser(description='query the crack db')
    parser.add_argument('-t', dest='time', nargs=2, help='query the count of records between start and end')
    args = parser.parse_args()

    if args.time:
        print(args.time)
        Query().query_count('v1_ad_crack_get', args.time[0], args.time[1])


if __name__ == '__main__':
    parse_params()
