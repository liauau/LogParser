import gzip
import os
import parser
import shutil

import log
from db.db_helper import DbHelper

DEBUG = True

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_DIR = ROOT + '/input'

db_helper = DbHelper()


def insert(records):
    api_names = list(set(rx.api_name for rx in records))
    for name in api_names:
        db_helper.insert_many(name, [rx.__dict__ for rx in records if rx.api_name == name])


def show(records):
    api_names = list(set(rx.api_name for rx in records))
    gen = (db_helper.find(name) for name in api_names)
    for rds in gen:
        for rd in rds:
            log.p(rd['api_name'], str(rd['user_id']), sep='\t')


def clear(records):
    api_names = list(set(rx.api_name for rx in records))
    for name in api_names:
        db_helper.remove(name)


def process(records):
    insert(records)
    # show(records)
    # clear(records)


def decompress_to_str_log(file_in_path):
    file_out_path = './tmp.txt'
    g = gzip.GzipFile(mode='rb', fileobj=open(file_in_path, 'rb'))
    open(file_out_path, 'wb').write(g.read())
    return file_out_path


def handle_file(file_in_path):
    file_out_path = decompress_to_str_log(file_in_path)
    with open(file_out_path, 'r') as f:
        records = list(parser.parse(line) for line in f.readlines())
        process(records)
        f.close()
        os.remove(file_out_path)


def init_env():
    if os.path.exists(INPUT_DIR):
        log.p(INPUT_DIR + ' existed. Do not create.')
    else:
        log.p('created ' + INPUT_DIR)
        os.mkdir(INPUT_DIR)

    for (dir_path, dir_names, file_names) in os.walk(ROOT):
        log_names = [n for n in file_names if n.startswith('access.log') and n.endswith('gz')]
        for name in log_names:
            shutil.copy(dir_path + '/' + name, INPUT_DIR)
        break


def main_loop():
    for f in os.listdir(INPUT_DIR):
        log.p(f)
        handle_file(f)


if __name__ == '__main__':
    init_env()
    main_loop()
