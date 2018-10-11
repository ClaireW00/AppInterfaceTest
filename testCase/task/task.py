import requests
import readConfig


class Task(object):
    def __init__(self):
        self.f = readConfig.ReadConfig()
        self.baseurl = self.f.getHttpValue("baseurl")
        # 将host、token加入header
        self.header = self.f.get_header()
        self.header["Host"] = self.f.getHttpValue("host")
        self.header["Authorization"] = self.f.getUserValue("authorization")

    def my_task(self, param):
        url = self.baseurl + self.f.get_url("task", "task_own")
        result = requests.get(url, headers=self.header, params=param)
        return result

