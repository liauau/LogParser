class Record(object):
    def __init__(self):
        self.ip = ''
        self.access_time = ''
        self.access_time_zone = ''
        self.method = ''
        self.status_code = 0
        self.api_name = ''

        self.app_pkg_name = ''
        self.locale = ''
        self.install_time = 0
        self.user_id = ''
        self.android_version = 0
        self.app_version = 0
        self.device_model = ''
        self.update_time = 0

    def __str__(self, *args, **kwargs):
        return "ip: %s \n" \
               "access_time: %d \n" \
               "method: %s \n" \
               "status_code: %d\n" \
               "api_name: %s\n" \
               "app_pkg_name: %s\n" \
               "locale: %s\n" \
               "install_time: %d\n" \
               "user_id: %s\n" \
               "android_version: %d\n" \
               "app_version: %d\n" \
               "device_model: %s\n" \
               "update_time: %d\n" \
               % (self.ip,
                  self.access_time,
                  self.method,
                  self.status_code,
                  self.api_name,
                  self.app_pkg_name,
                  self.locale,
                  self.install_time,
                  self.user_id,
                  self.android_version,
                  self.app_version,
                  self.device_model,
                  self.update_time
                  )

