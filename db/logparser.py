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

223.176.120.107 - - [06/Dec/2017:23:57:21 +0000] "GET /v1/ad_crack/get?_appPkgName=apptrends.live_wallpaper.photo_animation.scorpio&_locale=US&_installTime=1512519304&_userId=6349336a-778b-45fc-82d1-087833afedff&_androidVersion=22&_appVersion=1&_deviceModel=GiONEE_WBL7352&_updateTime=1512519304 HTTP/1.1" 200 2101 "-" "Dalvik/2.1.0 (Linux; U; Android 5.1; P5L Build/LMY47D)" "-"
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

    d = dict([param.split(EQUAL) for param in query_params_list if len(param.split(EQUAL)) >= 2])

    r.app_pkg_name = get_param(d, '_appPkgName')
    r.locale = get_param(d, '_locale')
    r.install_time = (get_param(d, '_installTime'))
    r.user_id = get_param(d, '_userId')
    r.android_version = (get_param(d, '_androidVersion'))
    r.app_version = (get_param(d, '_appVersion'))
    r.device_model = get_param(d, '_deviceModel')
    r.update_time = (get_param(d, '_updateTime'))

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
