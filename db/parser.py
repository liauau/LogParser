import calendar
import time

from db.model import Record

API_AD_CONFIG = 'ad_config'
API_AD_CRACK = 'ad_crack'

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
    r.install_time = int(get_param(d, 'installTime'))
    r.user_id = get_param(d, 'userId')
    r.android_version = int(get_param(d, 'androidVersion'))
    r.app_version = int(get_param(d, 'appVersion'))
    r.device_model = get_param(d, 'deviceModel')
    r.update_time = int(get_param(d, 'updateTime'))

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
    return None
