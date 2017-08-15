class Record(object):
    def __init__(self, **rd):
        if rd is not None:
            self.__dict__.update(rd)
            return

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
               "access_time: %s \n" \
               "method: %s \n" \
               "status_code: %s\n" \
               "api_name: %s\n" \
               "app_pkg_name: %s\n" \
               "locale: %s\n" \
               "install_time: %s\n" \
               "user_id: %s\n" \
               "android_version: %s\n" \
               "app_version: %s\n" \
               "device_model: %s\n" \
               "update_time: %s\n" \
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
