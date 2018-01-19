import argparse
from datetime import datetime, timezone, timedelta

from db.constant import KEY_APP_PKG_NAME, COLLECTION_PKG_NAMES, KEY_NAME, KEY_ACCESS_TIME, KEY_APP_VERSION, \
    COLLECTION_APP_VERSIONS, KEY_VALUE, KEY_ID, KEY_COUNT, KEY_USER_ID
from db.db_helper import DbHelper
from bson.son import SON


class Query:
    def __init__(self):
        self.QUERY_TYPE_APP = 0
        self.QUERY_TYPE_APP_USER = 1
        self.dh = DbHelper()

    def query_count(self, collection_name, start, end, query_type):
        s_tsp = self.__bjtime_to_timestamp(start)
        e_tsp = self.__bjtime_to_timestamp(end)
        coll = self.dh.get_collection(collection_name)
        result = list(coll.aggregate(self.get_pipeline(s_tsp, e_tsp, query_type)))
        self.show_result(collection_name, result)

    @staticmethod
    def show_result(collection_name, result):
        for r in result:
            pkg = r.get(KEY_ID).get(KEY_APP_PKG_NAME)
            version = r.get(KEY_ID).get(KEY_APP_VERSION)
            count = r.get(KEY_COUNT)
            if pkg:
                line = ('%s %s %s %s \n' % (collection_name.ljust(40), pkg.ljust(80), str(version).ljust(40), count))
                print(line, end='')
        print('done')

    def get_pipeline(self, s_tsp, e_tsp, query_type):
        pipeline = []
        if query_type == self.QUERY_TYPE_APP:
            pipeline = [
                {"$match": {KEY_ACCESS_TIME: {"$gt": s_tsp, "$lte": e_tsp}}},
                {"$group": {KEY_ID: {KEY_APP_PKG_NAME: "$app_pkg_name", KEY_APP_VERSION: "$app_version"}, KEY_COUNT: {"$sum": 1}}},
                {"$sort": SON([(KEY_COUNT, -1), (KEY_ID, 1)])}
            ]
        elif query_type == self.QUERY_TYPE_APP_USER:
            pipeline = [
                {"$match": {KEY_ACCESS_TIME: {"$gt": s_tsp, "$lte": e_tsp}}},
                {"$group": {KEY_ID: {KEY_APP_PKG_NAME: "$app_pkg_name", KEY_APP_VERSION: "$app_version", KEY_USER_ID: "$user_id"}}},
                {"$group": {KEY_ID: {KEY_APP_PKG_NAME: "$_id.app_pkg_name", KEY_APP_VERSION: "$_id.app_version"}, KEY_COUNT: {"$sum": 1}}},
                {"$sort": SON([(KEY_COUNT, -1), (KEY_ID, 1)])}
            ]
        return pipeline


    @staticmethod
    def __bjtime_to_timestamp(time_str):
        time_format = "%Y%m%d_%H%M%S"
        time_str = '20' + time_str
        dt = datetime.strptime(time_str, time_format)
        bj_tz = timezone(timedelta(hours=8))
        dt = dt.replace(tzinfo=bj_tz)
        print(dt)
        tsp = dt.timestamp()
        print(tsp)
        return tsp


def parse_params():
    parser = argparse.ArgumentParser(description='query the crack db')
    parser.add_argument('-q', dest='query', type=str, choices=['app', 'app_user'], help='specified the query type')
    parser.add_argument('-t', dest='time', nargs=2, required=True,
                        help='query the count of records between start and end. '
                             'time format is YMD_HMS like 180118_012020')
    args = parser.parse_args()

    q = Query()

    query_type = q.QUERY_TYPE_APP
    if args.query == 'app':
        query_type = q.QUERY_TYPE_APP
    elif args.query == 'app_user':
        query_type = q.QUERY_TYPE_APP_USER

    if args.time:
        print('query parameters:', args.query, query_type, args.time)
        q.query_count('v1_ad_crack_get', args.time[0], args.time[1], query_type)


if __name__ == '__main__':
    parse_params()
