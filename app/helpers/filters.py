from datetime import datetime


def datetimefilter(value, f='%a %b %d, %Y'):
    return datetime.strftime(value, f)
