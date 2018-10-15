import requests
import readConfig
import random


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

    # 获取一个我发起的售后流程
    def get_flow(self):
        param = {
            "field": "startAt",  # 排序字段
            "orderBy": "desc",
            "pageIndex": 1,
            "pageSize": 20,
            "status": 0,  # 事件状态，0全部，1执行中,2已完成；流程状态1:待分派 2:进行中 3:待确认完成 4:已完成 5:意外终止
            "qType": 0,  # 查询时间类型，0全部时间，1开始时间，2完成时间
            "source": 2,  # 0全部，1规则流程，2售后流程
        }
        flows = self.init_list(param).json()["data"]["records"]
        flow = flows[random.randint(0, len(flows)-1)]
        return flow

    # 获取售后流程信息
    def launch_concise(self):
        url = self.baseurl + self.f.get_url("speedup", "launch_concise")
        result = requests.get(url, headers=self.header)
        return result

    # 获取任意一个售后流程id
    def get_concise_id(self):
        data = self.launch_concise().json()["data"]
        return data[random.randint(0, len(data)-1)]["id"]

    # 手动发起售后流程
    def init_flow(self, data):
        url = self.baseurl + self.f.get_url("speedup", "init_flow")
        result = requests.post(url, headers=self.header, json=data)
        return result

    # 更改流程名称
    def title(self, flow_id, data):
        url = self.baseurl + self.f.get_url("speedup", "title") + flow_id + "/title"
        result = requests.put(url, headers=self.header, json=data)
        return result

    # 提交流程说明
    def remark(self, flow_id, data):
        url = self.baseurl + self.f.get_url("speedup", "remark") + flow_id
        result = requests.put(url, headers=self.header, json=data)
        return result

