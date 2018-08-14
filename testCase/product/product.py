import requests
import readConfig

class Product(object):

    def __init__(self):
        f = readConfig.ReadConfig()
        host = f.getHttpValue('host')
        self.baseurl = f.getHttpValue('baseurl')
        self.header = f.get_header()
        self.header['host'] = host
        self.header["Authorization"] = f.getUserValue('authorization')

    #获取所有产品接口
    def get_AllProduct(self,param):
        url=self.baseurl+"/api/v2/product"
        result=requests.get(url,params=param,headers=self.header)
        return result

    #获取第一个库存不为空的产品
    def get_product(self):   #返回字段（'categoryId', 'id', 'unit', 'stockEnabled, 'name', 'unitPrice', 'stock'）
        param = {
            'pageSize': 20,
            'pageIndex': 1
        }
        result=self.get_AllProduct(param)
        if result.status_code!=200:
            return 'error'
        result_json=result.json()
        if result_json['errcode']!=0:
            return 'error'

        totalRecords=result_json['data']['totalRecords']
        if totalRecords==0:
            return 'no product!'
        products=result_json['data']['records']['products']
        for prod in products:   #第一页数据
            if 'stock' in prod:#因为后端库存为0时没反回库存字段
                if prod['stock']>0:
                    return prod


if __name__=='__main__':
    p=Product()
    print(p.get_product())