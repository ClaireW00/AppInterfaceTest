import requests,time         #导入系统或第三方提供的库
import readConfig      #导入已封装的方法
from testCase.customer import customerManger
from testCase.product import product


class Chance(object):

    def __init__(self):
        f = readConfig.ReadConfig()
        host = f.getHttpValue('host')
        self.baseurl = f.getHttpValue('baseurl')
        self.header = f.get_header()
        self.header['host'] = host
        self.header["Authorization"] = f.getUserValue('authorization')
    # 新建机会

    def createChance(self, data):
        url=self.baseurl+"/api/v2/chance"
        result=requests.post(url,json=data,headers=self.header)
        return result

    # 获取销售阶段接口
    def get_saleStages(self):
        url=self.baseurl+'/api/v2/salestage'
        result=requests.get(url,headers=self.header)
        return result

    # 获取第一条销售阶段
    def get_saleStage(self):
        result=self.get_saleStages()
        if result.status_code != 200:
            return 'error'
        result_json = result.json()
        if result_json['errcode'] != 0:
            return 'error'
        data=result_json['data']
        return data[0]

    # 获取我的机会列表
    def myChance(self, param):
        url=self.baseurl+"/api/v2/chance/self"
        result=requests.get(url,params=param,headers=self.header)
        return result

    # 获取团队机会列表
    def teamChance(self, param):
        url = self.baseurl+'/api/v2/chance/team'
        result = requests.get(url, params=param, headers=self.header)
        return result

if __name__ == "__main__":
    chace = Chance()
    c=customerManger.CustomerManger()
    # 产品信息
    pro=product.Product().get_product()
    pro["quantity"]=1
    pro["costPrice"]=pro['unitPrice']
    pro["salePrice"] = pro['unitPrice']
    pro['discount']=pro["salePrice"]/pro["costPrice"]
    pro['totalMoney']=pro["quantity"]*pro["salePrice"]
    pro['stockEnabled']=True
    salestage=chace.get_saleStage()
    data={
        "cusName": c.get_SimilarCustorm()['name'],
        "name": "机会"+time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time())),
        "content": "接口创建销售机会"+time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time())),
        "prob": 60,
        "chanceType": "新客户",
        "product": [pro],
        "memo": "测试",
        "customerId": c.get_SimilarCustorm()['id'],
        "estimatedTime": int(time.time())+172800,#2天后
        "extDatas": [],
        "estimatedAmount": pro['totalMoney'],
        "wfState": 0, #审批状态
        "stageName": salestage['name'],
        "chanceSource": "搜索引擎",
        "stageId":salestage['id']
    }
    
    chace.createChance(data)