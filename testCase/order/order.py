import requests
import readConfig


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
    def order_self(self, param):
        url = self.baseurl + self.f.get_url("order", "order_self")
        result = requests.get(url, params=param, headers=self.header)
        return result

    # 获取团队订单列表
    def teamOrder(self,param):
        url=self.baseurl+'/api/v2/order/team'
        result=requests.get(url,params=param,headers=self.header)
        return result

    #新建订单
    def createOrder(self,data):
        url=self.baseurl+"/api/v2/order"
        result=requests.post(url,json=data,headers=self.header)
        return result





if __name__=="__main__":
    param1 = {
        "field": "lastActAt",
        "order": "desc",
        "pageSize": 20,
        "pageIndex": 1,
        "statusList": None,
        "tagsParams": []
    }
    o = Order()
    print(o.MyOrder(param1).json())



