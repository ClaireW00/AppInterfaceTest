import math, random, time, unittest
from testCase.order import order
from testCase.user import user
from testCase.product import product
from testCase.customer import customerManger
from commom import commonassert
from commom import attachments
from datetime import datetime


class OrderCase(commonassert.CommonTest):

    @classmethod
    def setUpClass(cls):
        print('订单管理：start')
        cls.ord = order.Order()
        cls.cust = customerManger.CustomerManger()
        cls.u = user.User()
        cls.login_name = cls.u.getName()

    # 列表处理方式提炼
    def listProcess(self, result, param, first_at, port="old",  **kw):  # port接口为老接口还是新接口，老接口没返回errcode
        if port == "old":
            self.assertStatus(result, "old")
            data = result.json()
        else:
            self.assertStatus(result)
            data = result.json()["data"]
        total_records = data["totalRecords"]
        records = data["records"]  # list
        actual_total = len(records)
        if total_records == 0:
            self.assertEqual(actual_total, total_records, msg=result.text)
            return
        if param["pageIndex"] == 1:
            first_at = records[0][param["filed"]]  # 第一条数据要排序字段的值
        for sa in records:
            if param["orderBy"] == "desc":
                self.assertTrue(first_at >= sa[param["filed"]], msg=sa)
            elif param["orderBy"] == "asc":
                self.assertTrue(first_at <= sa[param["filed"]], msg=sa)
            for key in kw:
                self.assertEqual(sa[key], kw[key], msg=sa)  # 判断列表数据负责人是不是登录人，若不是打印出错误的数据
            first_at = sa[param["filed"]]
        return first_at, actual_total

    # 我负责的创建时间倒叙排序
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
        print('我的订单列表响应时间：', result.elapsed.microseconds / 1000, 'ms')
        first_at, actual_total = self.listProcess(result, param, 0, directorName=self.login_name)
        total_records = result.json()["totalRecords"]
        if total_records > param["pageSize"]:
            page = math.ceil(total_records / param["pageSize"])
            for p in range(2, page + 1):
                param["pageIndex"] = p
                page_result = self.ord.my_order(param)
                first_at, total_infor = self.listProcess(page_result, param, first_at, directorName=self.login_name)
                actual_total += total_infor
        print("我负责的订单实际数据数量", actual_total)
        self.assertEqual(total_records, actual_total, msg='返回总数与实际数量总数不同')  # 判断返回的数据总数与实际数据数量是否相同

    # 成交金额倒叙排序
    def test_MyOrder_O002(self):
        """测试获取我的订单列表：按成交金额倒叙"""
        param = {
            "filed": "dealMoney",
            "orderBy": "desc",
            "pageSize": 20,
            "pageIndex": 1,
            "startType": 0,  # 开始时间，0代表全部
            "status": 0      # 0全部状态  1待审核   7审批中  2未通过  3进行中  4已完成  5意外终止
        }
        result = self.ord.my_order(param)
        print('我的订单列表响应时间：', result.elapsed.microseconds / 1000, 'ms')
        first_at, actual_total = self.listProcess(result, param, 0, directorName=self.login_name)
        total_records = result.json()["totalRecords"]
        if total_records > param["pageSize"]:
            page = math.ceil(total_records / param["pageSize"])
            for p in range(2, page + 1):
                param["pageIndex"] = p
                page_result = self.ord.my_order(param)
                first_at, total_infor = self.listProcess(page_result, param, first_at, directorName=self.login_name)
                actual_total += total_infor
        self.assertEqual(total_records, actual_total, msg='返回总数与实际数量总数不同')  # 判断返回的数据总数与实际数据数量是否相同

    # 搜索
    def test_MyOrder_O003(self):
        """测试获取我的订单列表：搜索（测试订单标题、客户名称、产品是否包含关键字）"""
        param = {
            "pageSize": 20,
            "pageIndex": 1,
            "keyWords": "快启"
        }
        result = self.ord.my_order(param)
        self.assertEqual(result.status_code, 200)
        result_json = result.json()
        print('我的订单列表响应时间：', result.elapsed.microseconds / 1000, 'ms')
        total_records = result_json["totalRecords"]
        records = result_json["records"]  # list
        if total_records > param["pageSize"]:
            page = math.ceil(total_records / param["pageSize"])
            for p in range(2, page + 1):
                param["pageIndex"] = p
                page_result = self.ord.my_order(param)
                self.assertEqual(page_result.status_code, 200, msg='翻页错误')
                json = page_result.json()
                pagedata = json["records"]
                records.extend(pagedata)
        print("我负责的订单搜索结果数量", len(records))
        self.assertEqual(total_records, len(records), msg='返回总数与实际数量总数不同')  # 判断返回的数据总数与实际数据数量是否相同
        for sa in records:
            exp = (param["keyWords"]in sa["title"])or(param["keyWords"]in sa["customerName"])or(param["keyWords"]in sa["proName"])
            self.assertTrue(exp, msg=sa["title"])
            self.assertEqual(sa["directorName"], self.login_name, msg=sa)  # 判断列表数据负责人是不是登录人，若不是打印出错误的数据

    # 查看订单详情
    def test_detail(self):
        """订单详情"""
        param = {
            "filed": "createdAt",
            "orderBy": "desc",
            "pageSize": 20,
            "pageIndex": 1,
            "status": 0  # 0全部状态  1待审核   7审批中  2未通过  3进行中  4已完成  5意外终止
        }
        order_id = self.ord.get_order(param)["id"]
        result = self.ord.order_detail(order_id)
        self.assertStatus(result)
        self.assertEqual(order_id, result.json()["data"]["id"])  # 详情订单id与传入得id相同

    # 设置参与人
    def test_edit_partner(self):
        """设置参与人"""
        param = {
            "filed": "createdAt",
            "orderBy": "desc",
            "pageSize": 20,
            "pageIndex": 1,
            "status": 3  # 0全部状态  1待审核   7审批中  2未通过  3进行中  4已完成  5意外终止
        }
        order_id = self.ord.get_order(param)["id"]
        data = {
            "members": [self.u.get_User("陈老师"),
                        self.u.get_User("刘洋C")]
        }
        result = self.ord.edit_partner(order_id, data)
        self.assertStatus(result)
        ord_detail = self.ord.order_detail(order_id).json()["data"]
        print("设置参与人的订单：", ord_detail["title"])
        self.assertEqual(data["members"], ord_detail["members"], msg=ord_detail["title"])  # 断言设置联系人后，订单详情联系人与设置一致

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
            "title": "订单"+time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time())),
            "dealMoney":  pro['totalMoney'],
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
            "startAt": int(datetime.now().timestamp()),
            "status": 0
        }
        result = self.ord.create_order(request_data)
        self.assertStatus(result)
        response_data = result.json()['data']
        self.assertEqual(request_data["title"], response_data["title"], msg=response_data['title'])  # 判断订单标题是否一致
        # 判断成交金额吃否一致
        self.assertEqual(request_data['dealMoney'], response_data['dealMoney'], msg=response_data['dealMoney'])
        # 判断客户ID是否一致
        self.assertEqual(request_data["customerId"], response_data["customerId"], msg=response_data['customerId'])

    # 测试获取我参与的订单，按创建时间倒叙排序
    def test_LinkOrder(self):
        """我参与的订单列表"""
        param = {
            "filed": "createdAt",
            "orderBy": "desc",
            "pageIndex": 1,
            "pageSize": 20,
            "status": 0
        }
        result = self.ord.link_order(param)
        first_at, actual_total = self.listProcess(result, param, 0, port="new")
        total_records = result.json()["data"]["totalRecords"]
        if total_records > param["pageSize"]:
            page = math.ceil(total_records / param["pageSize"])
            for p in range(2, page + 1):
                param['pageIndex'] = p
                page_result = self.ord.link_order(param)
                first_at, total_infor = self.listProcess(page_result, param, first_at, port="new")
                actual_total += total_infor
        print("我参与的订单实际数据数量", actual_total)
        self.assertEqual(total_records, actual_total, msg='返回总数与实际数量总数不同')  # 判断返回的数据总数与实际数据数量是否相同

    # 测试获取团队订单列表，按创建时间倒叙（目前没测试数据权限）
    def test_TeamOrder_O01(self):
        """获取团队订单"""
        param = {
            "filed": "createdAt",
            "orderBy": "desc",
            "pageSize": 20,
            "pageIndex": 1,
            "status": 0  # 0全部状态  1待审核   7审批中  2未通过  3进行中  4已完成  5意外终止
            }
        result = self.ord.team_order(param)
        self.assertEqual(result.status_code, 200)
        print('团队订单列表响应时间：', result.elapsed.microseconds / 1000, 'ms')
        first_at, actual_total = self.listProcess(result, param, 0)
        total_records = result.json()["totalRecords"]
        if total_records > param["pageSize"]:
            page = math.ceil(total_records / param["pageSize"])
            for p in range(2, page + 1):
                param['pageIndex'] = p
                page_result = self.ord.team_order(param)
                first_at, total_infor = self.listProcess(page_result, param, first_at)
                actual_total += total_infor
        print("团队订单实际数据数量", actual_total)
        self.assertEqual(total_records, actual_total, msg='返回总数与实际数量总数不同')  # 判断返回的数据总数与实际数据数量是否相同

    # 按状态查询
    def test_TeamOder_002(self):
        """团队订单：按状态查询"""
        param = {
            "filed": "createdAt",
            "orderBy": "desc",
            "pageSize": 20,
            "pageIndex": 1,
            "status": 3  # 0全部状态  1待审核   7审批中  2未通过  3进行中  4已完成  5意外终止
        }
        result = self.ord.team_order(param)
        self.assertEqual(result.status_code, 200)
        print('团队订单列表响应时间：', result.elapsed.microseconds / 1000, 'ms')
        first_at, actual_total = self.listProcess(result, param, 0, status=param["status"])
        total_records = result.json()["totalRecords"]
        if total_records > param["pageSize"]:
            page = math.ceil(total_records / param["pageSize"])
            for p in range(2, page + 1):
                param['pageIndex'] = p
                page_result = self.ord.team_order(param)
                first_at, total_infor = self.listProcess(page_result, param, first_at, status=param["status"])
                actual_total += total_infor
        print("团队订单按状态筛选结果：", actual_total)
        self.assertEqual(total_records, actual_total, msg='返回总数与实际数量总数不同')  # 判断返回的数据总数与实际数据数量是否相同

    # 获取回款方式
    def test_payee(self):
        """获取回款方式"""
        result = self.ord.payee()
        self.assertStatus(result)

    # 新增回款记录
    def test_pay(self):
        """新增回款记录"""
        param = {
            "filed": "createdAt",
            "orderBy": "desc",
            "pageSize": 20,
            "pageIndex": 1,
            "status": 3  # 0全部状态  1待审核   7审批中  2未通过  3进行中  4已完成  5意外终止
        }
        pay_method = self.ord.payee().json()["data"][0]
        data = {
            "remark": "备注" + str(random.randint(0, 1000)),
            "payeeUser": self.u.get_User(self.u.getName()),
            "receivedMoney": random.randint(200, 1000),
            "orderId": self.ord.get_order(param)["id"],
            "attachmentCount": 1,
            "payeeMethodName": pay_method["name"],
            "uuid": attachments.attachments("26")["UUId"],    # 回款记录bizType为26
            "payeeMethod": pay_method["order"],
            "receivedAt": int(datetime(datetime.now().year, datetime.now().month, datetime.now().day).timestamp()),
            "billingMoney": random.randint(200, 1000)
        }
        result = self.ord.pay(data)
        self.assertStatus(result, "old")
        data_response = result.json()
        print(data_response["orderTitle"])
        # 断言请求值与返回值相同
        for key in data:
            self.assertEqual(data[key], data_response[key], msg=data["orderId"])

    # 新增回款计划
    def test_plan(self):
        param = {
            "filed": "createdAt",
            "orderBy": "desc",
            "pageSize": 20,
            "pageIndex": 1,
            "status": 3  # 0全部状态  1待审核   7审批中  2未通过  3进行中  4已完成  5意外终止
        }
        pay_method = self.ord.payee().json()["data"][0]
        data = {
            "planAt": int(datetime.now().timestamp()) + (86400 * 5),    # 计划回款时间，5天后
            "orderId": self.ord.get_order(param)["id"],
            "remark": "回款计划备注测试" + str(datetime.now()),
            "payeeMethodName": pay_method["name"],
            "payeeMethod":  pay_method["order"],
            "planMoney": random.randint(1000, 2000),
            "remindType": 3     # 提醒方式，1计划前1天， 2前2天，3前3天，4前一周，5不提醒
        }
        result = self.ord.plan(data)
        self.assertStatus(result, "old")
        data_response = result.json()
        print("添加回款计划的订单：", data_response["orderId"])
        for key in data:
            self.assertEqual(data[key], data_response[key], msg=data["orderId"])

    # 更改负责人
    def test_owner(self):
        param = {
            "filed": "createdAt",
            "orderBy": "desc",
            "pageSize": 20,
            "pageIndex": 1,
            "status": 3  # 0全部状态  1待审核   7审批中  2未通过  3进行中  4已完成  5意外终止
        }
        order_id = self.ord.get_order(param)["id"]
        data = {
            "ids": order_id,
            "owner": {
                         "id": self.u.get_User("陈老师")["id"]
            }
        }
        result = self.ord.owner(data)
        self.assertStatus(result)
        print("更改负责人的订单：", order_id)

    @classmethod
    def tearDownClass(cls):
        print('订单管理：end')


if __name__ == '__main__':
    unittest.main()
