import requests,unittest,time
import random
import readConfig

class Salesleades(object):

    def __init__(self):
        self.f = readConfig.ReadConfig()
        self.host = self.f.getHttpValue("host")
        self.baseurl = self.f.getHttpValue("baseurl")
        Authorization = self.f.getUserValue("authorization")
        # 配置请求头
        self.header = self.f.get_header()
        self.header["Host"] = self.host
        self.header["Authorization"] = Authorization

    # 新建线索
    def create_sale(self, salelead):
        url = self.baseurl+'/api/v2/salesleads'
        result = requests.post(url, json=salelead, headers=self.header)
        return result

    # 获取线索列表第一条数据的id
    def get_Id(self):
        param = {
            "field": "lastActAt",
            "order": "desc",
            "pageSize": 20,
            "pageIndex": 1,
            "statusList": None,
            "tagsParams": []
        }
        result = self.own_saleslead(param)
        if result.status_code == 200:
            json_result = result.json()
            if json_result["errmsg"] == "success":
                if json_result["data"]["totalRecords"] > 0:
                    sales = json_result["data"]["records"]
                    return sales[0]["id"]

    # 获取详情
    def salesleads_detail(self, sale_id):
        url = self.baseurl + self.f.get_url("salesleads", "detail") + sale_id
        result = requests.get(url, headers=self.header)
        return result

    # 编辑线索
    def edit_saleslead(self, id, salelead):
        url=self.baseurl+'/api/v2/salesleads/'+id
        r = requests.put(url, json=salelead, headers=self.header)
        return r

    # 获取我的线索列表
    def own_saleslead(self, param):
        url = self.baseurl + self.f.get_url("salesleads", "ownsalesleads")
        result = requests.get(url, headers=self.header, params=param)
        return result

    # 获取团队线索列表
    def teamSaleslead(self, param):
        url=self.baseurl+"/api/v2/salesleads/mobile/team"
        result=requests.get(url,headers=self.header,params=param)
        return result


if __name__ == '__main__':
    s = Salesleades()
    # print(s.get_sale("5a5dcf9219b8203fa4776a18").json())
    param={
        "field":"lastActAt",
        "order":"desc",
        "pageSize": 20,
        "pageIndex": 1,
        "statusList":None,
        "tagsParams":[]
    }
    # print(s.ownSaleslead(param).json())
    # print(s.get_Id())
    print(s.teamSaleslead(param).json())
