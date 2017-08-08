import argparse

from db.routine import go


def parse_params():
    parser = argparse.ArgumentParser(description='the routine to build stat db')
    parser.add_argument('-d', '--dir', metavar='log_dir', help='specified log dir to be handled')

    args = parser.parse_args()
    if args.dir is not None:
        go(args.dir)

if __name__ == '__main__':
    parse_params()
