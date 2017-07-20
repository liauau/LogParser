from db.main import DEBUG


def p(*args, sep=' ', end='\n', file=None):
    if DEBUG:
        print(*args, sep=sep, end=end, file=file)
