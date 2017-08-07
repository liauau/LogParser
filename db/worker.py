import gzip
import os
import shutil
from os.path import join

import db.logparser as logparser
import log
from db.constant import KEY_NAME, COLLECTION_PKG_NAMES
from db.db_helper import DbHelper

DEBUG = True

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_DIR = join(ROOT, 'input')


class Worker:
    def __init__(self, logs_path):
        self.dh = DbHelper()
        self.logs_path = logs_path

    def handle_files(self):
        for f in os.listdir(self.logs_path):
            self.handle_file(join(self.logs_path, f))

    def handle_file(self, clog_path):
        text_log = self.decompress(clog_path)
        records = list(logparser.parse(line) for line in open(text_log, 'r').readlines())
        self.insert(records)
        # self.clear(records)
        os.remove(text_log)

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
        pkg_names = list(set(r.app_pkg_name for r in records))
        self.dh.insert_many(COLLECTION_PKG_NAMES, [{KEY_NAME: n} for n in pkg_names])

    def clear(self, records):
        api_names = list(set(r.api_name for r in records))
        for name in api_names:
            self.dh.remove(c_name=name)
        self.dh.drop(c_name=COLLECTION_PKG_NAMES)

    def copy_logs(self):
        if os.path.exists(INPUT_DIR):
            log.d(INPUT_DIR + ' existed. Do not create.')
        else:
            log.d('will create ' + INPUT_DIR)
            os.mkdir(INPUT_DIR)
            for (dir_path, dir_names, file_names) in os.walk(ROOT):
                access_logs = [n for n in file_names if n.startswith('access.log') and n.endswith('gz')]
                for l in access_logs:
                    shutil.copy(dir_path + '/' + l, INPUT_DIR)
                break


if __name__ == '__main__':
    worker = Worker(INPUT_DIR)
    worker.handle_files()
