import calendar
import time

from db.model import Record

EMPTY = ''
SPACE = ' '
LEFT = '['
RIGHT = ']'
QUOTE = '"'
MARK = '?'
AND = '&'
UNDERLINE = '_'
EQUAL = '='
SLASH = '/'

"""
log format:
$remote_addr - $remote_user [$time_local] $request $status $body_bytes_sent $http_referer $http_user_agent $http_x_forwarded_for

example:
137.97.9.45 - - [01/Aug/2017:04:52:17 +0000] "GET /pic/icon_fastcleaner.png HTTP/1.1" 200 15222 "-" "Dalvik/2.1.0 (Linux; U; Android 6.0.1; LS-5505 Build/LYF_LS-5505_01_09)" "-"

"""


def parse(line):
    record_str_list = line.split(sep=SPACE)

    r = Record()
    r.ip = record_str_list[0]
    r.access_time = get_utc_timestamp(record_str_list[3].replace(LEFT, EMPTY))
    r.access_time_zone = record_str_list[4].replace(RIGHT, EMPTY)
    r.method = record_str_list[5].replace(QUOTE, EMPTY)
    r.status_code = int(record_str_list[8])

    query = record_str_list[6]
    query_path = query.split(MARK)[0]
    r.api_name = query_path.replace(SLASH, UNDERLINE)[1:]

    if len(query.split(MARK)) < 2:
        return r

    query_params = query.split(MARK)[1]
    query_params_list = query_params.split(AND)

    d = dict([param.replace(UNDERLINE, EMPTY).split(EQUAL) for param in query_params_list])
    r.app_pkg_name = get_param(d, 'appPkgName')
    r.locale = get_param(d, 'locale')
    r.install_time = (get_param(d, 'installTime'))
    r.user_id = get_param(d, 'userId')
    r.android_version = (get_param(d, 'androidVersion'))
    r.app_version = (get_param(d, 'appVersion'))
    r.device_model = get_param(d, 'deviceModel')
    r.update_time = (get_param(d, 'updateTime'))

    return r


def get_utc_timestamp(time_str):
    time_tuple = time.strptime(time_str, "%d/%b/%Y:%H:%M:%S")
    utc_timestamp = calendar.timegm(time_tuple)
    # print(time_str)
    # print(utc_timestamp)
    return utc_timestamp


def get_param(d, keyword):
    if keyword in d.keys():
        return d[keyword]
    return ''
