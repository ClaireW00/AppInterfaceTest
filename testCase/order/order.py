import requests
import readConfig
import random


class Order(object):
    def __init__(self):
        self.f = readConfig.ReadConfig()
        self.host = self.f.getHttpValue("host")
        self.baseurl = self.f.getHttpValue("baseurl")
        authorization = self.f.getUserValue("authorization")
        # 配置请求头
        self.header = self.f.get_header()
        self.header["Host"] = self.host
        self.header["Authorization"] = authorization

    # 获取我的订单列表
    def my_order(self, param):
        url = self.baseurl + self.f.get_url("order", "my_order")
        result = requests.get(url, params=param, headers=self.header)
        return result

    # 获取我负责的订单列表符合条件的任意一个订单
    def get_order(self, param):
        result = self.my_order(param)
        records = result.json()["records"]
        if len(records) == 0:
            print("records is None")
            return
        ordmes = records[random.randint(0, len(records))]  # 符合条件的任意一个订单
        return ordmes

    # 获取我参与的订单
    def link_order(self, param):
        url = self.baseurl + self.f.get_url("order", "link_order")
        result = requests.get(url, headers=self.header, params=param)
        return result

    # 获取订单详情
    def order_detail(self, order_id):
        url = self.baseurl + self.f.get_url("order", "order") + "/" + order_id
        param = {"refreshPro": 0}
        result = requests.get(url, headers=self.header, params=param)
        return result

    # 设置订单参与人
    def edit_partner(self, order_id, member):
        url = self.baseurl + self.f.get_url("order", "partner") + order_id
        result = requests.put(url, headers=self.header, json=member)
        return result

    # 获取团队订单列表
    def team_order(self, param):
        url = self.baseurl + self.f.get_url("order", "team_order")
        result = requests.get(url, params=param, headers=self.header)
        return result

    # 新建订单
    def create_order(self, data):
        url = self.baseurl + self.f.get_url("order", "order")
        result = requests.post(url, json=data, headers=self.header)
        return result

    # 获取回款方式
    def payee(self):
        url = self.baseurl + self.f.get_url("order", "payee")
        result = requests.get(url, headers=self.header)
        return result


if __name__ == "__main__":
    param1 = {
        "filed": "createdAt",
        "orderBy": "desc",
        "pageSize": 20,
        "pageIndex": 1,
        "status": 0  # 0全部状态  1待审核   7审批中  2未通过  3进行中  4已完成  5意外终止
    }
    o = Order()
    print(o.my_order(param1))
