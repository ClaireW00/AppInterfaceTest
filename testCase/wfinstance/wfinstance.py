import requests
import readConfig


class Wfinstance(object):

    # 获取请求头信息header
    def __init__(self):
        self.fp = readConfig.ReadConfig()
        host = self.fp.getHttpValue("host")
        self.baseurl = self.fp.getHttpValue("baseurl")
        self.header = self.fp.get_header()
        self.header["host"] = host
        self.header["Authorization"] = self.fp.getUserValue("authorization")

    # 获取审批类别
    def get_wfbizform(self, param):
        url = self.baseurl+self.fp.get_url("wf_instance", "wfbizform")
        result = requests.get(url, headers=self.header, params=param)
        return result

    # 获取审批流程
    def get_wftemplate(self, wfbizform_id):
        url = self.baseurl+self.fp.get_url("wf_instance", "wftemplate") + wfbizform_id
        result = requests.get(url, headers=self.header)
        return result

    # 根据审批类别name获取审批类别信息,返回结果为dict结构包含id\name\isSysterm\enable
    def get_wfbizform_meg(self, param, name):
        wfbizforms = self.get_wfbizform(param)      # 请求审批类别接口
        try:
            records = wfbizforms.json()["records"]
            for wf in records:
                if wf["name"] == name:
                    return wf
            return "error"
        except Exception as e:
            print("获取请求名称的审批类别出错", e)

    # 新建审批
    def create_wfinstance(self, data):
        url = self.baseurl+self.fp.get_url("wf_instance", "wfinstance")
        result = requests.post(url, headers=self.header, json=data)
        return result

if __name__ == "__main__":
    param1 = {
        "pageSize": 1000
    }
    w = Wfinstance()
    result1 = w.get_wfbizform(param1)
    print(result1.json())







