import requests
import readConfig



class Order(object):
    def __init__(self):
        f = readConfig.ReadConfig()
        self.host = f.getHttpValue("host")
        self.baseurl = f.getHttpValue("baseurl")
        Authorization = f.getUserValue("authorization")
        # 配置请求头
        self.header = f.get_header()
        self.header["Host"] = self.host
        self.header["Authorization"] = Authorization

    #获取我的订单列表
    def myOrder(self,param):
        url=self.baseurl+"/api/v2/order/self"
        result=requests.get(url,params=param,headers=self.header)
        return result

    #获取团队订单列表
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
    param = {
        "field": "lastActAt",
        "order": "desc",
        "pageSize": 20,
        "pageIndex": 1,
        "statusList": None,
        "tagsParams": []
    }
    o=Order()
    print(o.MyOrder(param).json())



