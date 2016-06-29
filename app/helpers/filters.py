from datetime import datetime


def datetimefilter(value, f='%b %d, %Y'):
    return datetime.strftime(value, f)


def shortenfilter(value, size=97):
    return value if len(value) < 48 else value[:size] + '...'
