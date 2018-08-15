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
    def my_order(self, param):
        url = self.baseurl + self.f.get_url("order", "my_order")
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
    param1= {
            "filed": "createdAt",
            "orderBy": "desc",
            "pageSize": 20,
            "pageIndex": 1,
            "status": 0  # 0全部状态  1待审核   7审批中  2未通过  3进行中  4已完成  5意外终止
        }
    o = Order()
    print(o.my_order(param1))



