import argparse

from db import routine


def parse_params():
    parser = argparse.ArgumentParser(description='the routine to build stat db')
    parser.add_argument('-d', '--dir', metavar='log_dir', help='specified log dir to be handled')
    parser.add_argument('-ba', '--build_app_version', action='store_true', help='build app version collection')

    args = parser.parse_args()
    if args.dir is not None:
        routine.go(args.dir)
    if args.build_app_version:
        routine.build_app_version_collection()


if __name__ == '__main__':
    parse_params()
