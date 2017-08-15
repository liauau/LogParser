import gzip
import os
from os.path import join
from pprint import pprint

import db.logparser as logparser
from db.constant import KEY_NAME, COLLECTION_PKG_NAMES, COLLECTION_APP_VERSIONS, KEY_VALUE
from db.db_helper import DbHelper
from utils import log
from db.model import Record

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_DIR = join(ROOT, 'input')


class Worker:
    def __init__(self):
        self.dh = DbHelper()

    def handle_file(self, compressed_log_path):
        records = self.__gen_records(compressed_log_path)
        self.__insert_records(records)
        self.__insert_pkg_names(records)
        self.__insert_app_version(records)
        # self.__clear(records)
        return True

    def build_app_version_collection(self):
        c_names = self.dh.get_collection_names()
        for c in c_names:
            if 'v1' not in c or 'v1_ad_config' in c:
                continue
            print('handle collection: ' + c)
            records = list(Record(**d) for d in self.dh.find(c_name=c))
            self.__insert_app_version(records)

    def __gen_records(self, compressed_log_path):
        text_log = self.__decompress(compressed_log_path)
        records = list(logparser.parse(line) for line in open(text_log, 'r').readlines())
        records = [r for r in records if r.api_name.startswith('v1')]
        os.remove(text_log)
        return records

    @staticmethod
    def __decompress(clog):
        text_log = './tmp.txt'
        gzip_log = gzip.GzipFile(mode='rb', fileobj=open(clog, 'rb'))
        open(text_log, 'wb').write(gzip_log.read())
        return text_log

    def __insert_pkg_names(self, records):
        """
        insert pkg_names to COLLECTION_PKG_NAMES
        """
        existed_pkg_names = [n.get(KEY_NAME) for n in self.dh.find(COLLECTION_PKG_NAMES)]
        log.d('db_pns: %s' % existed_pkg_names)
        pkg_names = list(set(r.app_pkg_name for r in records))
        pkg_names = [n for n in pkg_names if n not in existed_pkg_names]
        log.d('in_pns: %s' % pkg_names)
        if len(pkg_names) > 0:
            self.dh.insert_many(COLLECTION_PKG_NAMES, [{KEY_NAME: n} for n in pkg_names])

    def __insert_records(self, records):
        """
        insert records to collections named with api_name
        """
        api_names = list(set(r.api_name for r in records))
        for name in api_names:
            self.dh.insert_many(name, [r.__dict__ for r in records if r.api_name == name])
            log.d(' done to insert %s' % name)

    def __insert_app_version(self, records):
        """
        insert app_version to COLLECTION_APP_VERSION
        the data format like {name: appA, value: 2}, {name: appA, value: 3}, {name: appB, value: 10}
        """
        existed_versions = list(v for v in self.dh.find(COLLECTION_APP_VERSIONS) if v.pop('_id'))

        unique_version_str_list = list(set(r.app_pkg_name + '@' + r.app_version for r in records
                                           if r.app_pkg_name != '' and r.app_version != ''))
        uvs = list({KEY_NAME: v.split('@')[0], KEY_VALUE: v.split('@')[1]}
                   for v in unique_version_str_list if len(v.split('@')) >= 2)
        filtered_vs = list(v for v in uvs if v not in existed_versions)
        pprint(filtered_vs)
        if len(filtered_vs) > 0:
            self.dh.insert_many(COLLECTION_APP_VERSIONS, filtered_vs)

    def __clear(self, records):
        api_names = list(set(r.api_name for r in records))
        for name in api_names:
            self.dh.drop(c_name=name)
        self.dh.drop(c_name=COLLECTION_PKG_NAMES)
        self.dh.drop(c_name=COLLECTION_APP_VERSIONS)


if __name__ == '__main__':
    pass
