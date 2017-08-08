import gzip
import os
from os.path import join

import db.logparser as logparser
from db.constant import KEY_NAME, COLLECTION_PKG_NAMES
from db.db_helper import DbHelper
from utils import log

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_DIR = join(ROOT, 'input')


class Worker:
    def __init__(self):
        self.dh = DbHelper()

    # def handle_files(self):
    #     for f in os.listdir(self.logs_path):
    #         self.handle_file(join(self.logs_path, f))

    def handle_file(self, clog_path):
        text_log = self.decompress(clog_path)
        records = list(logparser.parse(line) for line in open(text_log, 'r').readlines())
        records = [r for r in records if r.api_name.startswith('v1')]
        self.insert(records)
        # self.clear(records)
        os.remove(text_log)
        return True

    def decompress(self, clog):
        text_log = './tmp.txt'
        gzip_log = gzip.GzipFile(mode='rb', fileobj=open(clog, 'rb'))
        open(text_log, 'wb').write(gzip_log.read())
        return text_log

    def insert(self, records):
        # insert records to collections named with api_name
        api_names = list(set(r.api_name for r in records))
        for name in api_names:
            self.dh.insert_many(name, [r.__dict__ for r in records if r.api_name == name])
            log.d(' done to insert %s' % name)

        # insert pkg_names to COLLECTION_PKG_NAMES
        existed_pkg_names = [n.get(KEY_NAME) for n in self.dh.find(COLLECTION_PKG_NAMES)]
        log.d('db_pns: %s' % existed_pkg_names)
        pkg_names = list(set(r.app_pkg_name for r in records))
        pkg_names = [n for n in pkg_names if n not in existed_pkg_names]
        log.d('in_pns: %s' % pkg_names)
        if len(pkg_names) > 0:
            self.dh.insert_many(COLLECTION_PKG_NAMES, [{KEY_NAME: n} for n in pkg_names])

    def clear(self, records):
        api_names = list(set(r.api_name for r in records))
        for name in api_names:
            # self.dh.remove(c_name=name)
            self.dh.drop(c_name=name)
        self.dh.drop(c_name=COLLECTION_PKG_NAMES)

if __name__ == '__main__':
    pass
