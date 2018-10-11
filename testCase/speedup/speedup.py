import requests
import readConfig


class SpeedUp(object):
    def __init__(self):
        self.f = readConfig.ReadConfig()
        self.baseurl = self.f.getHttpValue("baseurl")
        # 配置请求头
        self.header = self.f.get_header()
        self.header["Host"] = self.f.getHttpValue("host")
        self.header["Authorization"] = self.f.getUserValue("authorization")

    # 我执行的事件视图
    def event_list(self, param):
        url = self.baseurl + self.f.get_url("speedup", "event_list")
        result = requests.get(url, headers=self.header, params=param)
        return result

    # 我组织的
    def flow_list(self, param):
        url = self.baseurl + self.f.get_url("speedup", "flow_list")
        result = requests.get(url, headers=self.header, params=param)
        return result

    # 流程信息及流程事件节点列表(流程详情)
    def flow_event(self, flow_id):
        url = self.baseurl + self.f.get_url("speedup", "flow_event") + flow_id
        result = requests.get(url, headers=self.header)
        return result

    # 我发起的
    def init_list(self, param):
        url = self.baseurl + self.f.get_url("speedup", "init_list")
        result = requests.get(url, headers=self.header, params=param)
        return result

    # 手动发起售后流程
    def init_flow(self, data):
        url = self.baseurl + self.f.get_url("speedup", "init_flow")
        result = requests.post(url, headers=self.header, json=data)
        return result
