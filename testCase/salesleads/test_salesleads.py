import requests,unittest,time,math
import random
from testCase.salesleads import salesleads
from testCase.user import user


from testCase.login import test_login
class Salesleades(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("销售线索：start")

    # 测试新建线索
    def test_NewSaleslead(self):
        """测试新建线索用例：正常新建线索"""
        name = "线索" + time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))
        companyname='四川'+'有限公司'+str(random.randint(200, 10000))
        salelead_request = {
            "status": 1,
            "address": "人民南路地铁站",
            "cellphone": "135123" + str(random.randint(10000, 99999)),
            "scopeBusiness": "测试125464",
            "extDatas": [],
            "remark": "1测试\n2哈哈哈",
            "region": {
                "province": "山西省",
                "city": "太原市",
                "county": "市辖区"
            },
            "companyName": companyname,
            "tel": "02856832",
            "tags": [{
                "tId": "5a2a767e75d2a9290fb1ca74",
                "itemId": "5a2a767e75d2a9290fb1ca6d"
            }, {
                "tId": "5a2a767e75d2a9290fb1ca74",
                "itemId": "5a2a767e75d2a9290fb1ca70"
            }],
            "name": name
        }
        sale = salesleads.Salesleades()
        result = sale.create_sale(salelead_request)
        print(result.text)
        self.assertEqual(result.status_code, 200)

        self.assertEqual(result.json()["errcode"], 0, msg=result.text)
        self.assertEqual(result.json()["errmsg"], "success", msg=result.text)
        salelead_response = result.json()['data']
        print("新建线索数据：", salelead_response)
        self.assertEqual(salelead_request['name'], salelead_response['name'])
        self.assertEqual(salelead_request["companyName"], salelead_response["companyName"])

    # 测试查看线索详情
    def test_getSalelead(self):
        """测试查看线索详情用例：根据ID查看线索详情"""
        sale = salesleads.Salesleades()
        id_request = sale.get_Id()
        r = sale.salesleads_detail(id_request)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["errcode"], 0, msg='返回信息错误')
        self.assertEqual(r.json()["errmsg"], "success", msg='返回信息错误')
        salelead_response = r.json()['data']
        print("线索详情：", salelead_response)
        self.assertEqual(id_request, salelead_response["sales"]['id'])

    # 测试编辑线索
    def test_editSalelead(self):
        """测试编辑线索用例：正常编辑线索"""
        salelead_request = {
            "companyName":"深圳红旗连锁" + time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time())),
            "name" : "谭川江"+str(random.randint(200, 400)),
            "status": 1,
            "address": "人民南路地铁站",
            "cellphone": "135123" + str(random.randint(10000,99999)),
            "scopeBusiness": "测试125464",
            "extDatas": [],
            "remark": "1测试\n2哈哈哈",
            "region": {
                "province": "山西省",
                "city": "太原市",
                "county": "市辖区"
            },
            "tel": "02856832",
            "tags": [{
                "tId": "5a2a767e75d2a9290fb1ca74",
                "itemId": "5a2a767e75d2a9290fb1ca6d"
            }, {
                "tId": "5a2a767e75d2a9290fb1ca74",
                "itemId": "5a2a767e75d2a9290fb1ca70"
            }]
        }
        sale = salesleads.Salesleades()
        id_request = sale.get_Id()
        result = sale.edit_saleslead(id_request, salelead_request)
        self.assertEqual(result.status_code, 200)

        self.assertEqual(result.json()["errcode"], 0, msg='返回信息错误')
        self.assertEqual(result.json()["errmsg"], "success", msg='返回信息错误')

        salelead_response = result.json()['data']
        print("编辑线索返回结果：", salelead_response)
        self.assertEqual(id_request, salelead_response['id'])
        self.assertEqual(salelead_request['name'], salelead_response['name'])
        self.assertEqual(salelead_request['companyName'], salelead_response['companyName'])

    # 我的线索列表
    def test_ownSalesleads(self):
        """测试我的线索列表用例：默认跟进时间顺序排序"""
        param = {
            "field": "lastActAt",
            "order": "desc",
            "pageSize": 20,
            "pageIndex": 1,
            "statusList": None,
            "tagsParams": []
        }
        sale = salesleads.Salesleades()
        result = sale.own_saleslead(param)
        u=user.User()
        login_name=u.getName()
        self.assertEqual(result.status_code, 200)

        json_response = result.json()
        self.assertEqual(json_response["errcode"], 0, msg='返回信息错误')
        self.assertEqual(json_response["errmsg"], "success", msg='返回信息错误')

        print('我的线索->我的线索列表响应时间：', result.elapsed.microseconds / 1000, 'ms')
        data = json_response["data"]
        totalRecords = data["totalRecords"]
        records = data["records"]  # list
        if totalRecords > param["pageSize"]:
            page = math.ceil(totalRecords / param["pageSize"])
            for p in range(2, page + 1):
                param["pageIndex"] = p
                pageResult = sale.own_saleslead(param)
                self.assertEqual(pageResult.status_code, 200, msg='翻页错误')
                json = pageResult.json()
                self.assertEqual(json["errmsg"], "success", msg='翻页错误')
                pagedata = json["data"]["records"]
                records.extend(pagedata)
        print("我的线索实际数据数量", len(records))
        self.assertEqual(totalRecords, len(records), msg='返回总数与实际数量总数不同')  # 判断返回的数据总数与实际数据数量是否相同
        if totalRecords > 0:
            firstAt = records[0]["lastActAt"]
            for sa in records:
                self.assertTrue(firstAt >= sa["lastActAt"], msg='跟进时间倒叙排序正确')  # 判断列表按跟进时间倒叙排序
                self.assertEqual(sa["responsorName"], login_name, msg=sa["name"])  # 判断列表数据负责人是不是登录人，若不是打印出错误的数据
                firstAt = sa["lastActAt"]

    # 我的线索搜索
    def test_OwnSaleslead_Search(self):
        """测试我的线索列表搜索线索姓名或公司名称，关键字：张瑞"""
        key = '线索'
        param = {
            "keyword":key,
            "pageSize": 20,
            "pageIndex": 1,
        }
        sale = salesleads.Salesleades()
        result = sale.own_saleslead(param)
        u = user.User()
        login_name = u.getName()
        self.assertEqual(result.status_code, 200)
        result_json=result.json()
        self.assertEqual(result_json["errcode"],0)
        self.assertEqual(result_json["errmsg"],"success")
        records = result_json["data"]["records"]
        totalRecords = result_json["data"]["totalRecords"]
        if totalRecords > param["pageSize"]:
            page = math.ceil(totalRecords/param["pageSize"])
            for p in range(2, page+1):
                param["pageIndex"] = p
                pageResult = sale.own_saleslead(param)
                self.assertEqual(pageResult.status_code, 200, msg='翻页错误')
                json = pageResult.json()
                self.assertEqual(json["errmsg"], "success", msg='翻页错误')
                pagedata=json["data"]["records"]
                records.extend(pagedata)
        if totalRecords == 0:
            self.assertEqual(records, None)
        else:
            print("搜索结果实际数据数量", len(records))
            self.assertEqual(totalRecords, len(records), msg='返回总数与实际数量总数不同')  # 判断返回的数据总数与实际数据数量是否相同
        for sa in records:
            self.assertEqual(sa["responsorName"], login_name, msg=sa["name"])  # 判断列表数据负责人是不是登录人，若不是打印出错误的数据
            isTrue = (key in sa["name"])or(key in sa["companyName"])
            self.assertTrue(isTrue, msg='搜索结果错误！')

    def test_TeamSaleslead(self):
        '''测试获取团队线索'''
        param = {
            "field": "lastActAt",
            "order": "desc",
            "pageSize": 20,
            "pageIndex": 1,
            "statusList": None,
            "tagsParams": []
        }
        sale = salesleads.Salesleades()
        result=sale.teamSaleslead(param)
        self.assertEqual(result.status_code,200)
        result_json=result.json()
        self.assertEqual(result_json["errcode"], 0)
        self.assertEqual(result_json["errmsg"], "success")
        totalRecords=result_json["data"]["totalRecords"]
        records=result_json["data"]["records"]
        # 循环获取第一页之后的数据，将所有数据添加到records里
        if totalRecords>param["pageSize"]:
            page=math.ceil(totalRecords/param["pageSize"])
            for p in range(2,page+1):
                param["pageIndex"]=p
                pageResult=sale.teamSaleslead(param)
                self.assertEqual(pageResult.status_code,200,msg='翻页错误')
                json=pageResult.json()
                self.assertEqual(json["errmsg"], "success",msg='翻页错误')
                pagedata=json["data"]["records"]
                records.extend(pagedata)
        print("团队线索的数据总数",len(records))
        self.assertEqual(totalRecords,len(records),msg='返回总数与实际数量总数不同')  #判断返回的数据总数与实际数据数量是否相同
        if totalRecords > 0:
            firstAt = records[0]["lastActAt"]
            for sa in records:
                self.assertTrue(firstAt >= sa["lastActAt"],msg='跟进时间倒叙排序正确')  # 判断列表按跟进时间倒叙排序
                firstAt = sa["lastActAt"]

    @classmethod
    def tearDownClass(cls):
        print('销售线索：end')

if __name__ == '__main__':
    unittest.main()
