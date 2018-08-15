import math,random,time
from testCase.order import order
from testCase.user import user
from testCase.product import product
from testCase.customer import customerManger
from commom import commonassert


class OrderCase(commonassert.CommonTest):

    @classmethod
    def setUpClass(cls):
        print('订单管理：start')
        cls.ord = order.Order()
        cls.cust = customerManger.CustomerManger()

    # 创建时间倒叙排序
    def test_MyOrder_O001(self):
        """测试获取我的订单列表：按创建时间倒叙"""
        param = {
            "filed": "createdAt",
            "orderBy": "desc",
            "pageSize": 20,
            "pageIndex": 1,
            "status": 0  # 0全部状态  1待审核   7审批中  2未通过  3进行中  4已完成  5意外终止
        }
        result = self.ord.my_order(param)
        u = user.User()
        login_name = u.getName()
        self.assertStatus(result)
        result_json = result.json()
        print('我的订单列表响应时间：', result.elapsed.microseconds / 1000, 'ms')
        total_records = result_json["totalRecords"]
        records = result_json["records"]  # list
        if total_records > param["pageSize"]:
            page = math.ceil(total_records / param["pageSize"])
            for p in range(2, page + 1):
                param["pageIndex"] = p
                page_result = self.ord.my_order(param)
                self.assertStatus(page_result)
                pagedata = page_result.json()["records"]
                records.extend(pagedata)
        print("我的订单实际数据数量", len(records))
        self.assertEqual(total_records, len(records), msg='返回总数与实际数量总数不同')  # 判断返回的数据总数与实际数据数量是否相同
        if total_records > 0:
            firstAt = records[0]["createdAt"]
            for sa in records:
                self.assertTrue(firstAt >= sa["createdAt"], msg='创建时间倒叙排序正确')  # 判断列表按创建时间倒叙排序
                self.assertEqual(sa["directorName"], login_name, msg=sa["title"])  # 判断列表数据负责人是不是登录人，若不是打印出错误的数据
                firstAt = sa["createdAt"]

    # 成交金额倒叙排序
    def test_MyOrder_O002(self):
        """测试获取我的订单列表：按成交金额倒叙"""
        param = {
            "filed":"dealMoney",
            "endType": 0,  # 结束时间
            "pageSize": 20,
            "pageIndex": 1,
            "startType": 0,  # 开始时间，0代表全部
            "status": 0     # 0全部状态  1待审核   7审批中  2未通过  3进行中  4已完成  5意外终止
        }
        result = self.ord.myOrder(param)
        u = user.User()
        login_name = u.getName()
        self.assertEqual(result.status_code, 200)
        json_response = result.json()
        print('我的订单列表响应时间：', result.elapsed.microseconds / 1000, 'ms')
        totalRecords = json_response["totalRecords"]
        records = json_response["records"]  # list
        if totalRecords > param["pageSize"]:
            page = math.ceil(totalRecords / param["pageSize"])
            for p in range(2, page + 1):
                param["pageIndex"] = p
                pageResult = self.ord.myOrder(param)
                self.assertEqual(pageResult.status_code, 200, msg='翻页错误')
                json = pageResult.json()
                pagedata = json["records"]
                records.extend(pagedata)
        print("我的订单实际数据数量", len(records))
        self.assertEqual(totalRecords, len(records), msg='返回总数与实际数量总数不同')  # 判断返回的数据总数与实际数据数量是否相同
        if totalRecords > 0:
            firstMoney = records[0]["dealMoney"]
            for sa in records:
                self.assertTrue(firstMoney >= sa["dealMoney"], msg=sa["title"])  # 判断列表最高金额排序
                self.assertEqual(sa["directorName"], login_name, msg=sa["title"])  # 判断列表数据负责人是不是登录人，若不是打印出错误的数据
                firstMoney = sa["dealMoney"]

    # 搜索
    def test_MyOrder_O003(self):
        """测试获取我的订单列表：搜索（测试订单标题、客户名称、产品是否包含关键字）"""
        param = {
            "pageSize": 20,
            "pageIndex": 1,
            "keyWords":"快启"
        }
        result = self.ord.myOrder(param)
        u = user.User()
        login_name = u.getName()
        self.assertEqual(result.status_code, 200)
        json_response = result.json()
        print('我的订单列表响应时间：', result.elapsed.microseconds / 1000, 'ms')
        totalRecords = json_response["totalRecords"]
        records = json_response["records"]  # list
        if totalRecords > param["pageSize"]:
            page = math.ceil(totalRecords / param["pageSize"])
            for p in range(2, page + 1):
                param["pageIndex"] = p
                pageResult = self.ord.myOrder(param)
                self.assertEqual(pageResult.status_code, 200, msg='翻页错误')
                json = pageResult.json()
                pagedata = json["records"]
                records.extend(pagedata)
        print("我的订单搜索结果数量", len(records))
        self.assertEqual(totalRecords, len(records), msg='返回总数与实际数量总数不同')  # 判断返回的数据总数与实际数据数量是否相同
        for sa in records:
            exp=(param["keyWords"]in sa["title"])or(param["keyWords"]in sa["customerName"])or(param["keyWords"]in sa["proName"])
            self.assertTrue(exp,msg=sa["title"])
            self.assertEqual(sa["directorName"], login_name, msg=sa["title"])  # 判断列表数据负责人是不是登录人，若不是打印出错误的数据

    # 新建订单
    def test_CreateOder_O001(self):
        """新建订单：正常填写所有字段"""
        # 获取第一条有库存的产品
        pro = product.Product().get_product()
        pro["quantity"] = 1
        pro["costPrice"] = pro['unitPrice']
        pro["salePrice"] = pro['unitPrice']
        pro['discount'] = pro["salePrice"] / pro["costPrice"]
        pro['totalMoney'] = pro["quantity"] * pro["salePrice"]
        pro['stockEnabled'] = True
        customer_id = self.cust.getCustomerID()
        detail = self.cust.customer_detail(customer_id).json()["data"]
        customer_name = detail["name"]
        request_data = {
            # "uuid": "381DB79E-A351-4950-8806-44623AF2938E",
            "customerName": customer_name,
            "attachmentCount": 0,
            "planPayments": [{
                "planAt": int(time.time())+86400,    # 明天此时
                "payeeMethod": 5,
                "payeeMethodName": "基金",
                "planMoney": 500,
                "remindType": 5,
                "remark": "回款计划"
            }],  # 回款计划
            "customerId": customer_id,
            "title": "订单"+time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time())),
            "dealMoney": random.randint(1000, 5000),
            "endAt": -2209017601,
            "proInfo": [pro],   # 产品信息
            "proName": "小米5",
            "extDatas": [],
            # "wfTplId": "58be8f01d33c655a18000209",  # 审批流程ID
            "paymentRecords": [{
                "remark": "回款纪录",
                "receivedMoney": 580,
                "attachmentCount": 1,
                "payeeUser": {
                    "id": "590aebdbe44c366eaf00009e",
                    "depts": [{
                            "title": ""
                            }],
                    "name": "布莱尔",
                    "avatar": "https:\/\/uimg.ukuaiqi.com\/b4eb8611-4945-458d-a24e-a8c2050ce8c0\/20171208_20560032317214.jpg"
                },
                "payeeMethodName": "支票",
                "uuid": "0E3B149E-578E-4161-9E2F-EC5B630FA923",
                "payeeMethod": 8,
                "receivedAt": int(time.time()),
                "billingMoney": 3568
            }],
            "startAt": 1516678260,
            "status": 0
        }
        result = self.ord.createOrder(request_data)
        self.assertEqual(result.status_code, 200, msg=result.text)
        json_response = result.json()
        self.assertEqual(json_response["errcode"], 0, msg=result.text)
        self.assertEqual(json_response["errmsg"], "success", msg=result.text)
        response_data = json_response['data']
        self.assertEqual(request_data["title"], response_data["title"], msg=response_data['title'])  # 判断订单标题是否一致
        # 判断成交金额吃否一致
        self.assertEqual(request_data['dealMoney'], response_data['dealMoney'], msg=response_data['dealMoney'])
        # 判断客户ID是否一致
        self.assertEqual(request_data["customerId"], response_data["customerId"], msg=response_data['customerId'])

    # 测试获取团队订单列表，按创建时间倒叙（目前没测试数据权限）
    def test_TeamOrder_O001(self):
        """获取团队订单"""
        param = {
            "filed": "createdAt",
            "endType": 0,  # 结束时间
            "pageSize": 20,
            "pageIndex": 1,
            "startType": 0,  # 开始时间，0代表全部
            "status": 0  # 0全部状态  1待审核   7审批中  2未通过  3进行中  4已完成  5意外终止
            }
        result = self.ord.teamOrder(param)
        self.assertEqual(result.status_code,200)
        print('团队订单列表响应时间：', result.elapsed.microseconds / 1000, 'ms')
        json_response=result.json()
        self.assertTrue("totalRecords" in json_response,msg=json_response)    # 判断返回内容字端是否正确
        totalRecords=json_response['totalRecords']
        records=json_response['records']
        if totalRecords>0:
            firstAt=records[0]['createdAt']
        for sa in records:    # 判断第一页数据是否按创建时间倒叙排序
            self.assertTrue(firstAt>=sa['createdAt'])
            firstAt=sa['createdAt']
        realRecords = len(records)
        if totalRecords>param['pageSize']:     # 翻页获取第一页以后的数据数据
            page = math.ceil(totalRecords / param['pageSize'])    # 正向取整
            for p in range(2,page+1):
                param['pageIndex']=p
                self.ord.teamOrder(param)
                pageResult = self.ord.teamOrder(param)
                self.assertEqual(pageResult.status_code, 200, msg='翻页错误')
                json = pageResult.json()
                pagedata = json["records"]
                realRecords = realRecords+len(pagedata)
                for sa in pagedata:    # 判断每页数据排序是否争取
                    self.assertTrue(firstAt >= sa['createdAt'])
                    firstAt = sa['createdAt']

        print("团队订单实际数据数量", realRecords)
        self.assertEqual(totalRecords, realRecords, msg='返回总数与实际数量总数不同')  # 判断返回的数据总数与实际数据数量是否相同

    @classmethod
    def tearDownClass(cls):
        print('订单管理：end')


if __name__ == '__main__':
    unittest.main()
