import os
import re
from os.path import join
from pprint import pprint

from db.worker import Worker
from env import ROOT

handled_file_path = join(ROOT, 'config', 'handled_files.txt')
LOG_DIR = join(ROOT, 'input', 'nginx')


def get_file_number(line):
    num = 0
    regex = r'access.*-(?P<number>[0-9]+).gz'
    pattern = re.compile(regex)
    m = pattern.match(line)
    if m:
        num = int(m.group('number'))
    return num


def get_max_handled_file():
    lines = open(handled_file_path, 'r').readlines()
    n = 0
    for l in lines:
        if n < get_file_number(l):
            n = get_file_number(l)
    print('max_handled_file_number: %s' % n)
    return n


def get_unhandle_files(path):
    maxhf = get_max_handled_file()
    fns = [f for f in os.listdir(path) if os.path.isfile(join(path, f))]
    fns = [n for n in fns if get_file_number(n) > maxhf]
    print('unhandle files:')
    pprint(fns)
    return fns


def done(filename):
    with open(handled_file_path, 'a') as f:
        f.write(filename + '\n')
        f.close()


def go(log_dir):
    wk = Worker()
    ufns = get_unhandle_files(log_dir)
    for fn in ufns:
        if wk.handle_file(join(log_dir, fn)):
            done(fn)


def build_app_version_collection():
    wk = Worker()
    wk.build_app_version_collection()


if __name__ == '__main__':
    go(LOG_DIR)
