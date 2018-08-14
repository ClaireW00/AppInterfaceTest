import unittest,time,math
from testCase.chance import chance
from testCase.customer import customerManger
from testCase.product import product


class ChanceCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("销售线索：start")

    def setUp(self):
        self.cha = chance.Chance()
        self.param = {
            "pageIndex": 1,
            "pageSize": 20,
            "sortType": 1   # 排序方式，1创建时间，2更新时间，3最高金额
        }

    # 用例：新建销售机会
    def test_createSalestage(self):
        """新建机会"""
        custo = customerManger.CustomerManger()
        # 产品信息
        pro = product.Product().get_product()
        pro["quantity"] = 1
        pro["costPrice"] = pro['unitPrice']
        pro["salePrice"] = pro['unitPrice']
        pro['discount'] = pro["salePrice"] / pro["costPrice"]
        pro['totalMoney'] = pro["quantity"] * pro["salePrice"]
        pro['stockEnabled'] = True
        salestage = self.cha.get_saleStage()  # 获取销售阶段信息
        data = {
            "cusName": custo.get_similar_customer()['name'],
            "name": "机会" + time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time())),
            "content": "接口创建销售机会" + time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time())),
            "prob": 60,
            "chanceType": "新客户",
            "product": [pro],
            "memo": "测试",
            "customerId": custo.get_similar_customer()['id'],
            "estimatedTime": int(time.time()) + 172800,  # 2天后
            "extDatas": [],
            "estimatedAmount": pro['totalMoney'],
            "wfState": 0,  # 审批状态
            "stageName": salestage['name'],
            "chanceSource": "搜索引擎",
            "stageId": salestage['id']
        }
        result=self.cha.createChance(data)
        self.assertEqual(result.status_code,200)
        response=result.json()
        self.assertEqual(data['name'],response['name'])     # 断言机会名称
        self.assertEqual(data['cusName'],response['cusName'])   # 断言关联客户名称
        self.assertEqual(data['stageName'], response['stageName'])   # 断言销售阶段
        self.assertEqual(data['estimatedAmount'], response['estimatedAmount'])  # 断言预计成交金额

    # 用例：获取我的机会列表
    def test_MyChance_001(self):
        """我的机会列表：默认排序方式‘创建时间倒叙"""
        result=self.cha.myChance(self.param)
        self.assertEqual(result.status_code,200)
        result_json=result.json()
        self.assertTrue('totalRecords'in result_json)
        totalRecords=result_json['totalRecords']
        records=result_json['records']
        actualTotal=len(records)   # 实际返回数据数量
        # 获取第一页以后的数据并计算长度
        if totalRecords>self.param['pageSize']:
            page=math.ceil(totalRecords/self.param['pageSize'])
            for p in range(2,page+1):
                self.param['pageIndex']=p
                pageresult=self.cha.myChance(self.param)
                self.assertEqual(pageresult.status_code,200,msg=p)   # 翻页获取数据出错时，打印出出错的页数
                pageRecords=pageresult.json()['records']
                actualTotal = actualTotal+len(pageRecords)
        self.assertEqual(totalRecords, actualTotal, msg=actualTotal)  # 判断返回的数据总数与数据数量是否一致,错误时返回实际数据数量

    # 用例：我的机会列表按照最高金额排序
    def test_MyChance_002(self):
        '''我的机会列表：按照最高金额排序'''

        self.param['sortType']=3  #3表示按照最高金额排序
        result=self.cha.myChance(self.param)
        self.assertEqual(result.status_code,200)
        result_json=result.json()
        self.assertTrue('totalRecords'in result_json)
        totalRecords=result_json['totalRecords']
        records=result_json['records']
        actualTotal=len(records)#实际返回数据数量
        if totalRecords>=0:
            firstAmount=records[0]['estimatedAmount']  #取第一条数据的金额
        #判断按最高金额倒叙
        for re in records:
            self.assertTrue(firstAmount>=re['estimatedAmount'],msg=re['name'])#排序错误时，打印出数据的名称
            firstAmount=re['estimatedAmount']

        #获取第一页以后的数据并计算长度
        if totalRecords>self.param['pageSize']:
            page=math.ceil(totalRecords/self.param['pageSize'])
            for p in range(2,page+1):
                self.param['pageIndex']=p
                pageresult=self.cha.myChance(self.param)
                self.assertEqual(pageresult.status_code,200,msg=p)   #翻页获取数据出错时，打印出出错的页数
                pageRecords=pageresult.json()['records']
                actualTotal=actualTotal+len(pageRecords)
                for pRe in pageRecords:#判断翻页数据按金额排序是否正确
                    self.assertTrue(firstAmount>=pRe['estimatedAmount'], msg=pRe)  # 排序错误时，打印出数据的名称
                    firstAmount = pRe['estimatedAmount']
        self.assertEqual(totalRecords, actualTotal, msg=actualTotal)  # 判断返回的数据总数与数据数量是否一致,错误时返回实际数据数量

    # 用例：我的机会列表按照销售阶段查询
    def test_MyChance_003(self):
        '''我的机会列表：按销售阶段查询’'''
        firstStage=self.cha.get_saleStage()  #获取第一个销售阶段的信息
        self.param['stageId']=firstStage['id']
        firstStageName=firstStage['name']

        result=self.cha.myChance(self.param)
        self.assertEqual(result.status_code,200)
        result_json=result.json()
        self.assertTrue('totalRecords' in result_json)
        totalRecords=result_json['totalRecords']
        records=result_json['records']
        actualTotal=len(records)  #实际返回数据数量
        #判断返回数据是否正确
        for re in records:
            self.assertEqual(re['stageNmae'],firstStageName,msg=re['name'])  #判断返回结果机会阶段名称是否与查询阶段一致
        #获取第一页以后的数据并计算长度
        if totalRecords>self.param['pageSize']:
            page=math.ceil(totalRecords/self.param['pageSize'])
            for p in range(2,page+1):
                self.param['pageIndex']=p
                pageResult=self.cha.myChance(self.param)
                self.assertEqual(pageResult.status_code,200,msg=p)   #请求出出错时打印出错的页码
                pageRecords=pageResult.json()['records']
                actualTotal=actualTotal+len(pageRecords)
                for re in pageRecords:
                    self.assertEqual(re['stageNmae'], firstStageName)  # 判断返回结果机会阶段名称是否与查询阶段一致
        self.assertEqual(totalRecords,actualTotal,msg=actualTotal)   #判断返回的数据总数与数据数量是否一致,错误时返回实际数据数量

    # 用例：团队机会列表，目前没根据数据权限判断默认数据展示
    def test_TeamChance_004(self):
        '''团队机会列表：默认显示'''
        result=self.cha.teamChance(self.param)
        self.assertEqual(result.status_code,200)
        result_json=result.json()
        self.assertTrue('totalRecords'in result_json)
        totalRecords=result_json['totalRecords']
        records=result_json['records']
        actualTotal = len(records)  # 实际返回数据数量
        # 获取第一页以后的数据并计算长度
        if totalRecords > self.param['pageSize']:
            page = math.ceil(totalRecords/self.param['pageSize'])
            for p in range(2, page+1):
                self.param['pageIndex'] = p
                pageResult = self.cha.teamChance(self.param)
                self.assertEqual(pageResult.status_code, 200, msg=p)  # 翻页获取数据出错时，打印出出错的页数
                pageRecords = pageResult.json()['records']
                actualTotal = actualTotal + len(pageRecords)
        self.assertEqual(totalRecords, actualTotal, msg=actualTotal)  # 判断返回的数据总数与数据数量是否一致,错误时返回实际数据数量

    def tearDown(self):
        self.param = {
            "pageIndex": 1,  # 置为1，否则其它用例获取列表时，第一页取得是最后一页数据
            "pageSize": 20,
            "sortType": 1    # 排序方式，1创建时间，2更新时间，3最高金额
                    }

    @classmethod
    def tearDownClass(cls):
        print("销售机会：end")

if __name__ == '__main__':
    unittest.main()