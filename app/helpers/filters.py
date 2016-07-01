from datetime import datetime


def datetimefilter(value, f='%b %d, %Y'):
    return datetime.strftime(value, f)


def shortenfilter(value, size=247):
    return value[:size] + '...'
