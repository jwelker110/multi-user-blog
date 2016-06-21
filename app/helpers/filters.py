from datetime import datetime


def datetimefilter(value, f='%a %b %d, %Y'):
    return datetime.strftime(value, f)


def shortenfilter(value, size=47):
    return value if len(value) < 48 else value[:size] + '...'
