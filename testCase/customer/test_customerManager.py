import HTMLTestRunner
import math
import random
import time
import unittest
import re
from datetime import datetime, timedelta
from testCase.customer import customerManger
from testCase.user import user
from commom import commonassert


class CustomerManagerCase(commonassert.CommonTest):
    # 类属性
    custom = customerManger.CustomerManger()
    switcher = custom.cus_reason_switcher().json()["value"]  # 丢公海原因开关，1开启，0未开启

    @classmethod
    def setUpClass(cls):
        cls.cust = customerManger.CustomerManger()
        print("开发客户测试：start")

    # 获取客户状态
    def test_tags(self):
        """获取客户状态和标签"""
        param = {
            "filterType": 0,
            "tagsType": 0
        }
        result = self.cust.get_tags(param)
        # 断言状态及错误码
        self.assertStatus(result)
        result_json = result.json()
        # 断言返回数据不为空
        data = result_json["data"]
        self.assertTrue(len(data) >= 2)

    # 新建客户测试
    def test_createCustomer(self):
        """新建客户用例：正常新建客户"""
        status_id = self.cust.get_status()  # 随机获取一个已存在的状态
        customer_data = {
            "name": "客户" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(time.time()))),
            "position": {  # 定位
                "loc": [104.0138168334961, 30.70565223693848],
                "addr": "茶店子客运站(西三环路五段289号)"
            },
            "summary": "1、销售也行业\n2、主营运动产品" + str(random.randint(1, 300)),  # 简介
            "contacts.name": "简爱" + str(random.randint(1, 500)),  # 联系人
            "contacts.tel": ["15802856" + str(random.randint(1000, 9999))],  # 手机
            "contacts.wiretel": ["0285623585"],  # 座机
            "regional": {
                "province": "山西省",
                "city": "太原市",
                "county": "市辖区"
            },  # 地区
            "uuid": "5BDCEAA3-D00B-4820-BB41-112995108D14",
            "webSite": "www.baidu.com",
            "statusId": status_id,  # 客户状态
            "tags": [],  # 标签
            "extDatas": []  # 自定义字段
        }
        for i in range(300, 600):
            customer_data["name"] = "公海提醒测试" + "00" + str(i)
            customer_data["statusId"] = self.cust.get_status()
            result = self.cust.new_customer(customer_data)
        """
        # 断言请求状态和错误码是否正确
        self.assertStatus(result)
        # 断言客户信息是否正确
        cust_response = result.json()['data']
        self.assertEqual(cust_response['name'], customer_data['name'], msg=cust_response['name'])
        self.assertEqual(cust_response["summary"], customer_data['summary'])
        self.assertEqual(cust_response["statusId"], customer_data['statusId'])
        """

    # 客户名称为空
    def test_customer_namenull(self):
        """新建客户用例：客户名称为空"""
        status_id = self.cust.get_status()
        customer_data = {
            "name": "",
            "position": {  # 定位
                "loc": [104.0138168334961, 30.70565223693848],
                "addr": "茶店子客运站(西三环路五段289号)"
            },
            "summary": "1、销售也行业\n2、主营运动产品" + str(random.randint(1, 300)),  # 简介
            "contacts.name": "廖小姐" + str(random.randint(1, 500)),  # 联系人
            "contacts.tel": ["158028568325"],  # 手机
            "contacts.wiretel": ["0285623585"],  # 座机
            "regional": {
                "province": "山西省",
                "city": "太原市",
                "county": "市辖区"
            },  # 地区
            "uuid": "5BDCEAA3-D00B-4820-BB41-112995108D14",
            "webSite": "www.baidu.com",
            "statusId": status_id,  # 客户状态
            "tags": [],  # 标签
            "extDatas": []  # 自定义字段
        }
        result = self.cust.new_customer(customer_data)
        # 请求状态和错误码是否正确
        self.assertStatus(result, "old")
        result_json = result.json()
        self.assertEqual(result_json['errcode'], 60001, msg=result.text)  # 错误时打印返回内容
        self.assertEqual(result_json['errmsg'], '客户名称不能为空或者不能全为空格!', msg=result.text)

    # 状态为空，2.10版本状态、标签分离后续获取默认状态判断是否不传就是默认状态
    def test_customer_statusnull(self):
        """新建客户用例：状态传空"""
        customer_data = {
            "name": "客户" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(time.time()))),
            "position": {  # 定位
                "loc": [104.0138168334961, 30.70565223693848],
                "addr": "茶店子客运站(西三环路五段289号)"
            },
            "summary": "1、销售也行业\n2、主营运动产品" + str(random.randint(1, 300)),  # 简介
            "contacts.name": "简爱" + str(random.randint(1, 500)),  # 联系人
            "contacts.tel": ["15802856" + str(random.randint(1000, 9999))],  # 手机
            "contacts.wiretel": ["028562" + str(random.randint(1000, 9999))],  # 座机
            "regional": {
                "province": "山西省",
                "city": "太原市",
                "county": "市辖区"
            },  # 地区
            "uuid": "5BDCEAA3-D00B-4820-BB41-112995108D14",
            "webSite": "www.baidu.com",
            "statusId": "",  # 客户状态
            "tags": [],  # 标签
            "extDatas": []  # 自定义字段
        }
        result = self.cust.new_customer(customer_data)
        # 断言请求状态和错误码是否正确
        self.assertStatus(result)

    # 获取客户详情
    def test_customer_detail(self):
        """获取客户详情"""
        customer_id = self.cust.getCustomerID()
        result = self.cust.customer_detail(customer_id)
        # 断言返回状态码和错误码
        self.assertStatus(result)
        data = result.json()["data"]
        # 断言客户的id与传入的id一致
        self.assertEqual(data["id"], customer_id, msg=data["name"])

    # 转移客户
    def test_customer_owner(self):
        """转移客户"""
        customer_id = self.cust.getCustomerID()
        us = user.User().get_colleague()
        data = {
            "customerType": 1,
            "updateChance": True,       # 机会是否转移
            "ownerId": us["id"],
            "ownerName": us["name"],
            "updateFlowEvent": True,        # 快点是否转移
            "ids": customer_id
        }
        result = self.cust.owner_customer(data)
        self.assertStatus(result)
        # 调用客户详情接口，查看负责人是否修改成功
        result_detail = self.cust.customer_detail(customer_id)
        self.assertStatus(result_detail)
        # 客户详情查看负责人id和name是否与提交是数据一致
        owner = result_detail.json()["data"]["owner"]
        self.assertEqual(owner["name"], data["ownerName"], msg="转移后客户负责人显示错误")
        self.assertEqual(owner["id"], data["ownerId"], msg="转移后客户负责人显示错误")

    # 删除客户
    def test_delete_customer(self):
        """删除客户"""
        customer_id = self.cust.getCustomerID()
        result = self.cust.delete_customer(customer_id)
        # 断言请求状态
        self.assertStatus(result, "old")
        # 断言客户是否真的被删除，调用客户详情接口查看客户是否已被删除
        result_detail = self.cust.customer_detail(customer_id)
        self.assertEqual(result_detail.status_code, 200, msg=result_detail.text)
        detail_json = result_detail.json()
        self.assertEqual(detail_json["errcode"], 50012, msg=result_detail.text)
        self.assertEqual(detail_json["errmsg"], "客户不存在或已删除!", msg=result_detail.text)

    # 编辑客户
    def test_edit_customer(self):
        """编辑客户名称、状态、简介"""
        # 获取一个客户ID，编辑该客户
        customer_id = self.cust.getCustomerID()
        # 获取客户详情中负责人信息，负责人没更改
        cust_detail = self.cust.customer_detail(customer_id).json()["data"]
        owner = cust_detail["owner"]
        status_id = self.cust.get_status()
        edit_data = {
            "name": "编辑客户日期" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))),
            "statusId": status_id,  # 随机获取一个已存在的客户状态
            "summary": "编辑客户简介" + str(random.randint(200, 500)),
            "position": {  # 定位
                "loc": [104.0138168334961, 30.70565223693848],
                "addr": "茶店子客运站(西三环路五段289号)"
            },
            "webSite": "www.ukuaiqi.com",
            "owner": owner,
            "members": [],
            "tags": [],
            "contacts.wiretel": [],
            "contacts.name": "",
            "extDatas": [],
            "contacts.tel": [],
            "regional": {},
            "loc": {
                "loc": [0, 0],
                "addr": ""
            },
        }
        result = self.cust.edit_customer(edit_data, customer_id)
        # 断言返回状态及错误码
        self.assertStatus(result)
        data = result.json()["data"]
        # 断言编辑数据提交后数据是否与提交一致
        self.assertEqual(edit_data["name"], data["name"], msg=data)
        self.assertEqual(edit_data["statusId"], data["statusId"], msg=data)
        self.assertEqual(edit_data["summary"], data["summary"], msg=data)

    # 客户详情快捷编辑状态
    def test_edit_status(self):
        """客户详情快捷编辑状态"""
        customer_id = self.cust.getCustomerID()
        status_id = self.cust.get_status()
        status = {
            "statusId": status_id
        }
        result = self.cust.edit_status(customer_id, status)
        self.assertStatus(result)
        try:
            # 获取客户详情，断言状态是否修改成功
            result_detail = self.cust.customer_detail(customer_id)
            self.assertEqual(result_detail.status_code, 200, msg=result_detail.text)
            detail_json = result_detail.json()
            data = detail_json["data"]
            # 断言客户的id与传入的id一致
            self.assertEqual(data["statusId"], status_id, msg=data["name"])
        except Exception as e:
            print("请求客户详情出错", e)

    # 丢公海开关
    def test_cus_reason_switcher(self):
        """手动丢公海原因是否开启"""
        result = self.cust.cus_reason_switcher()
        self.assertEqual(result.status_code, 200, msg=result.text)
        result_json = result.json()
        self.assertEqual(result_json["key"], "cus_reason_switcher", msg=result.text)
        self.assertTrue((result_json["value"] == "0" or result_json["value"] == "1"))     # value="1"开启，value="0"未开启

    # 丢公海原因
    def test_cus_reason(self):
        """获取丢公海原因"""
        result = self.cust.cus_reason()
        self.assertStatus(result)
        # 列表有且仅有一条系统字段，“其他”
        data = result.json()["data"]
        self.assertTrue(len(data) >= 1)
        sys = 0
        for reason in data:
            if reason["isSys"]:
                self.assertEqual(reason["name"], "其他", msg="系统默认选项错误")
                sys += 1
        self.assertTrue(sys == 1)

    # 客户详情跟进列表
    def test_cus_saleactivity(self):
        """客户详情跟进列表"""
        param = {
            "pageIndex": 1,
            "pageSize": 10,
            "split": 1      # 将图片与其他格式附件分离
        }
        customer_id = self.cust.getCustomerID()
        detail = self.cust.customer_detail(customer_id).json()["data"]
        count = detail["counter"]["activity"]
        customer_name = detail["name"]
        result = self.cust.cus_saleactivity(customer_id, param)
        # 断言请求状态和请求状态码
        self.assertStatus(result)
        data = result.json()["data"]
        total_records = data["totalRecords"]
        records = data["records"]
        actual_total = len(records)
        # 断言跟进数据按创建时间倒叙排序,且跟进属于该客户
        if total_records > 0:
            first_at = records[0]["createdAt"]
            for saleact in records:
                self.assertTrue(first_at >= saleact["createdAt"], msg=customer_name+str(saleact["createdAt"]))
                self.assertEqual(saleact["customerId"], customer_id, msg=customer_name+str(saleact["createdAt"]))
                first_at = saleact["createdAt"]
        if total_records > param["pageSize"]:
            page = math.ceil(total_records/param["pageSize"])
            for p in range(2, page+1):
                param["pageIndex"] = p
                page_result = self.cust.cus_saleactivity(customer_id, param)
                self.assertStatus(page_result)
                page_records = page_result.json()["data"]["records"]
                actual_total += len(page_records)
                for saleact in page_records:
                    self.assertTrue(first_at >= saleact["createdAt"], msg=customer_name+str(saleact["createdAt"]))
                    self.assertEqual(saleact["customerId"], customer_id, msg=customer_name+str(saleact["createdAt"]))
                    first_at = saleact["createdAt"]
        # 断言跟进实际数量与tab数量相同
        self.assertTrue(actual_total == count, msg=customer_name)
        self.assertTrue(actual_total == total_records, msg=customer_name)

    # 客户详情跟进列表查看转码是否成功
    @unittest.skip("测试录音转码专用用例")
    def test_cus_saleactivity(self):
        param = {
            "pageIndex": 1,
            "pageSize": 10,
            "split": 1  # 将图片与其他格式附件分离
        }
        customer_id = "5b04d9a48c2ec4b7480e3c98"
        result = self.cust.cus_saleactivity(customer_id, param)
        # 断言请求状态和请求状态码
        self.assertStatus(result)
        data = result.json()["data"]
        total_records = data["totalRecords"]
        records = data["records"]
        success_code = 0
        audio = []
        # 断言跟进数据按创建时间倒叙排序,且跟进属于该客户
        for saleact in records:
            if re.match(r'.*?\.mp3', saleact["audioUrl"]) is None:
                audio.append(saleact["audioUrl"])
                success_code += 1

        if total_records > param["pageSize"]:
            page = math.ceil(total_records / param["pageSize"])
            for p in range(2, page + 1):
                param["pageIndex"] = p
                page_result = self.cust.cus_saleactivity(customer_id, param)
                self.assertStatus(page_result)
                page_records = page_result.json()["data"]["records"]
                for saleact in page_records:
                    if re.match(r'.*?\.mp3', saleact["audioUrl"]) is None:
                        audio.append(saleact["audioUrl"])
                        success_code += 1
        createAt = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(records[0]["createdAt"]))
        now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(time.time())))
        print("跟进提交时间：", createAt)
        print("查看转码时间：", now)
        print("总共数量：", total_records)
        print("转码失败的数量：", success_code)
        print(audio)

    # 客户详情拜访列表
    def test_cus_visit(self):
        """客户详情拜访列表"""
        customer_id = self.cust.getCustomerID()
        detail = self.cust.customer_detail(customer_id).json()["data"]
        count = detail["counter"]["visit"]
        customer_name = detail["name"]
        param = {
            "customerId": customer_id,
            "pageIndex": 1,
            "pageSize": 20
        }
        result = self.cust.cus_visit(param)
        self.assertStatus(result)
        data = result.json()["data"]
        total_records = data["totalRecords"]
        records = data["records"]
        actual_total = len(records)
        # 断言拜访数据按创建时间倒叙排序,且跟进属于该客户
        if total_records > 0:
            first_at = records[0]["createdAt"]
            for vis in records:
                self.assertTrue(first_at >= vis["createdAt"], msg=customer_name + str(vis["createdAt"]))
                self.assertEqual(vis["customerId"], customer_id, msg=customer_name + str(vis["createdAt"]))
                self.assertEqual(vis["visitType"], 1, msg=customer_name + str(vis["createdAt"]))         # 1拜访， 2跟进
                first_at = vis["createdAt"]
        if total_records > param["pageSize"]:
            page = math.ceil(total_records / param["pageSize"])
            for p in range(2, page + 1):
                param["pageIndex"] = p
                page_result = self.cust.cus_visit(param)
                self.assertStatus(page_result)
                page_records = page_result.json()["data"]["records"]
                actual_total += len(page_records)
                for vis in page_records:
                    self.assertTrue(first_at >= vis["createdAt"], msg=customer_name + str(vis["createdAt"]))
                    self.assertEqual(vis["customerId"], customer_id, msg=customer_name + str(vis["createdAt"]))
                    self.assertEqual(vis["visitType"], 1, msg=customer_name + str(vis["createdAt"]))  # 1拜访， 2跟进
                    first_at = vis["createdAt"]
        # 断言拜访实际数量与tab数量相同
        self.assertTrue(actual_total == count, msg=customer_name)
        self.assertTrue(actual_total == total_records, msg=customer_name)

    # 客户详情订单列表
    def test_cus_order(self):
        """客户详情订单列表"""
        param = {
            "pageIndex": 1,
            "pageSize": 20
        }
        customer_id = self.cust.getCustomerID()
        detail = self.cust.customer_detail(customer_id).json()["data"]
        count = detail["counter"]["order"]
        customer_name = detail["name"]
        result = self.cust.cus_order(customer_id, param)
        self.assertEqual(result.status_code, 200, msg=result.text)
        result_json = result.json()
        total_records = result_json["totalRecords"]
        records = result_json["records"]
        actual_total = len(records)
        # 断言订单按创建时间倒叙排序,且订单属于该客户
        if total_records > 0:
            first_at = records[0]["createdAt"]
            for orde in records:
                self.assertTrue(first_at >= orde["createdAt"], msg=customer_name + orde["title"])
                self.assertEqual(orde["customerName"], customer_name, msg=customer_name + orde["title"])
                first_at = orde["createdAt"]
        if total_records > param["pageSize"]:
            page = math.ceil(total_records / param["pageSize"])
            for p in range(2, page + 1):
                param["pageIndex"] = p
                page_result = self.cust.cus_order(customer_id, param)
                self.assertEqual(page_result.status_code, 200, msg=page_result.text)
                page_json = page_result.json()
                page_records = page_json["records"]
                actual_total += len(page_records)
                for orde in page_records:
                    self.assertTrue(first_at >= orde["createdAt"], msg=customer_name + orde["title"])
                    self.assertEqual(orde["customerId"], customer_id, msg=customer_name + orde["title"])
                    first_at = orde["createdAt"]
        self.assertTrue(total_records == count, msg=customer_name)
        self.assertTrue(actual_total == count, msg=customer_name)

    # 客户详情任务列表
    def test_cus_task(self):
        """客户详情任务列表"""
        customer_id = self.cust.getCustomerID()
        detail = self.cust.customer_detail(customer_id).json()["data"]
        count = detail["counter"]["task"]
        customer_name = detail["name"]
        param = {
            "customerId": customer_id,
            "pageIndex": 1,
            "pageSize": 20
        }
        result = self.cust.cus_task(param)
        self.assertEqual(result.status_code, 200, msg=result.text)
        result_json = result.json()
        total_records = result_json["totalRecords"]
        records = result_json["records"]
        actual_total = len(records)
        # 断言任务数量tab数量相同
        if total_records > param["pageSize"]:
            page = math.ceil(total_records / param["pageSize"])
            for p in range(2, page + 1):
                param["pageIndex"] = p
                page_result = self.cust.cus_task(param)
                self.assertEqual(page_result.status_code, 200, msg=page_result.text)
                page_json = page_result.json()
                page_records = page_json["records"]
                actual_total += len(page_records)
        self.assertTrue(total_records == count, msg=customer_name)
        self.assertTrue(actual_total == count, msg=customer_name)

    # 客户详情机会列表
    def test_cus_chance(self):
        """客户详情机会列表"""
        customer_id = self.cust.getCustomerID()
        detail = self.cust.customer_detail(customer_id).json()["data"]
        count = detail["counter"]["demand"]
        customer_name = detail["name"]
        param = {
            "customerId": customer_id,
            "pageIndex": 1,
            "pageSize": 20
        }
        result = self.cust.cus_chance(param)
        self.assertEqual(result.status_code, 200, msg=result.text)
        result_json = result.json()
        total_records = result_json["totalRecords"]
        records = result_json["records"]
        actual_total = len(records)
        if total_records > param["pageSize"]:
            page = math.ceil(total_records/param["pageSize"])
            for p in range(2, page+1):
                param["pageIndex"] = p
                page_result = self.cust.cus_chance(param)
                self.assertEqual(page_result.status_code, 200, page_result.text)
                page_json = page_result.json()
                page_records = page_json["records"]
                actual_total += len(page_records)
        self.assertEqual(actual_total, count, msg=customer_name)

    # 客户详情审批
    def test_cus_wfinstance(self):
        """客户详情审批列表"""
        customer_id = self.cust.getCustomerID()
        detail = self.cust.customer_detail(customer_id).json()["data"]
        count = detail["counter"]["workflow"]
        customer_name = detail["name"]
        param = {
            "pageIndex": 1,
            "pageSize": 20
        }
        result = self.cust.cus_wfinstance(customer_id, param)
        self.assertEqual(result.status_code, 200, msg=result.text)
        result_json = result.json()
        total_records = result_json["totalRecords"]
        records = result_json["records"]
        # 断言无数据时，records是None，且count=0
        if total_records == 0:
            self.assertIsNone(records, msg=result.text)
            self.assertEqual(count, total_records, msg=customer_name)
            return None
        # 断言records不为None时，count与实际数据数量相同
        actual_total = len(records)
        if total_records > param["pageSize"]:
            page = math.ceil(total_records / param["pageSize"])
            for p in range(2, page + 1):
                param["pageIndex"] = p
                page_result = self.cust.cus_wfinstance(customer_id, param)
                self.assertEqual(page_result.status_code, 200, page_result.text)
                page_json = page_result.json()
                page_records = page_json["records"]
                actual_total += len(page_records)
        self.assertEqual(actual_total, count, msg=customer_name)

        # 客户详情审批

    # 客户详情下项目
    def test_cus_project(self):
        """客户详情项目列表"""
        customer_id = self.cust.getCustomerID()
        detail = self.cust.customer_detail(customer_id).json()["data"]
        count = detail["counter"]["projectNum"]
        customer_name = detail["name"]
        param = {
            "pageIndex": 1,
            "pageSize": 20
        }
        result = self.cust.cus_project(customer_id, param)
        self.assertStatus(result)
        total_records = result.json()["data"]["totalRecords"]
        records = result.json()["data"]["records"]
        # 断言无数据时，records是None，且count=0
        if total_records == 0:
            self.assertIsNone(records, msg=result.text)
            self.assertEqual(count, total_records, msg=customer_name)
            return None
        # 断言records不为None时，count与实际数据数量相同
        actual_total = len(records)
        if total_records > param["pageSize"]:
            page = math.ceil(total_records / param["pageSize"])
            for p in range(2, page + 1):
                param["pageIndex"] = p
                page_result = self.cust.cus_project(customer_id, param)
                self.assertEqual(page_result.status_code, 200, page_result.text)
                page_json = page_result.json()
                page_records = page_json["data"]["records"]
                actual_total += len(page_records)
        self.assertEqual(actual_total, count, msg=customer_name)

    # 客户详情快点列表
    def test_cus_speedup(self):
        """客户详情快点列表测试"""
        customer_id = self.cust.getCustomerID()
        detail = self.cust.customer_detail(customer_id).json()["data"]
        count = detail["counter"]["flowEventNum"]
        customer_name = detail["name"]
        param = {
            "pageIndex": 1,
            "pageSize": 20,
            "qTime": 1
        }
        result = self.cust.cus_speedup(customer_id, param)
        self.assertStatus(result)
        total_records = result.json()["data"]["totalRecords"]
        records = result.json()["data"]["records"]
        actual_total = len(records)
        # 断言列表数据按开始时间倒序、且属于该客户
        if total_records > 0:
            first_at = records[0]["startAt"]
            for speed in records:
                self.assertTrue(first_at >= speed["startAt"], msg=customer_name + "的快点" + speed["flowTitle"])
                self.assertEqual(speed["customerId"], customer_id, msg=customer_name + "的快点" + speed["flowTitle"])
                first_at = speed["startAt"]
        if total_records > param["pageSize"]:
            page = math.ceil(total_records/param["pageSize"])
            for p in range(2, page+1):
                param["pageIndex"] = p
                page_result = self.cust.cus_speedup(customer_id, param)
                self.assertStatus(page_result)
                page_records = page_result.json()["data"]["records"]
                actual_total += len(page_records)
                for speed in page_records:
                    self.assertEqual(first_at >= speed["startAt"], msg=customer_name + "的快点" + speed["flowTitle"])
                    self.assertEqual(speed["customerId"], customer_id, msg=customer_name + "的快点" + speed["flowTitle"])
                    first_at = speed["startAt"]
        self.assertEqual(actual_total, count, msg=customer_name)

    # 获取客户详情联系人列表
    def test_contact(self):
        """客户详情联系人列表"""
        customer_id = self.cust.getCustomerID()
        # 获取客户详情联系人个数
        count = self.cust.customer_detail(customer_id).json()["data"]["counter"]["contact"]
        # 获取联系人列表
        result = self.cust.contact(customer_id)
        # 断言tab上联系人个数与实际联系人数量是否相同
        result_json = result.json()
        if "contacts" in result_json:
            actual_count = len(result_json["contacts"])
            self.assertEqual(actual_count, count, msg=customer_id)
        else:
            self.assertEqual(count, 0, msg=customer_id)

    # 新建客户联系人
    def test_createContact(self):
        """新建客户联系人"""
        customer_id = "5bce94d63ea34b0af47a18c7"  # self.cust.getCustomerID()
        # 获取kehu 添加联系人前联系人数量
        count_before = self.cust.customer_detail(customer_id).json()["data"]["counter"]["contact"]
        tel = "158028" + str(random.randint(10000, 99999))
        nowtime = datetime.now()
        birth = int((datetime(nowtime.year - 20, nowtime.month+1, nowtime.day) - timedelta(days=8)).timestamp())
        contact_data = {
            "wiretel": ["028568333"],
            "extDatas": [],
            "name": "秦立民" + str(random.randint(1, 300)),
            "birth": birth,
            "tel": [tel]
        }
        for i in range(1, 20, 2):
            contact_data["name"] = "林琳" + str(random.randint(300, 800))
            contact_data["birth"] = int((datetime(nowtime.year - 10-i, nowtime.month+1, nowtime.day) - timedelta(days=8)).timestamp()) + i*86400
            result = self.cust.create_contact(customer_id, contact_data)
        """
        self.assertEqual(result.status_code, 200, msg=result.text)
        data = result.json()
        self.assertEqual(data["name"], contact_data["name"], msg=customer_id)
        self.assertEqual(data["birth"], contact_data["birth"], msg=customer_id)
        self.assertEqual(data["tel"], contact_data["tel"], msg=customer_id)
        self.assertEqual(data["wiretel"], contact_data["wiretel"], msg=customer_id)
        # 断言客户联系人数量是否+1
        count_after = self.cust.customer_detail(customer_id).json()["data"]["counter"]["contact"]
        self.assertTrue((count_after == count_before+1), msg=customer_id)
        """

    # 未开启丢公海原因时手动丢公海,switcher="1"跳过
    @unittest.skipIf(switcher == "1", "开启手动丢公海原因，跳过用例test_throw_sea_001")
    def test_throw_sea_001(self):
        """未开启丢公海原因时手动丢公海"""
        us = user.User()
        customer_id = self.cust.getCustomerID()
        result = self.cust.throw_sea(customer_id)
        self.assertEqual(result.status_code, 200, msg=result.content)
        # 查看客户详情，判断客户是否是公海客户
        result_detail = self.cust.customer_detail(customer_id)
        self.assertStatus(result_detail)
        data = result_detail.json()["data"]
        # 断言客户为公海客户，丢公海类型、丢公海原因为空,丢公海人为登录人
        self.assertEqual(data["lock"], False, msg=data["name"])     # lock=false公海客户，lock=true非公海客户
        self.assertEqual(data["recycleType"], 1, msg=data["name"])  # 1手动丢公海，2自动丢公海
        self.assertEqual(data["recycleReason"], "", msg=data["name"])
        self.assertEqual(data["recycleName"], us.getName(), msg=data["name"])

    # 开启丢公海原因时手动丢公海,switcher= "0"跳过
    @unittest.skipIf(switcher == "0", "未开启手动丢公海原因，跳过用例test_throw_sea_002")
    def test_throw_sea_002(self):
        """开启丢公海原因时手动丢公海"""
        us = user.User()
        customer_id = self.cust.getCustomerID()
        reasons = self.cust.cus_reason().json()["data"]
        reason_id = reasons[0]["id"]
        reason_name = reasons[0]["name"]
        reason = {
            "id": reason_id,        # 丢公海原因
            "comment": "手动丢弃客户的原因" + str(random.randint(1, 1000))    # 原因说明
        }
        expect = reason_name + "(" + reason["comment"] + ")"
        result = self.cust.throw_sea(customer_id, reason)
        self.assertEqual(result.status_code, 200, msg=result.content)
        # 查看客户详情，判断客户是否是公海客户
        result_detail = self.cust.customer_detail(customer_id)
        self.assertStatus(result_detail)
        data = result_detail.json()["data"]
        # 断言客户为公海客户，丢公海类型、丢公海原因,丢公海人为登录人
        self.assertEqual(data["lock"], False, msg=data["name"])     # lock=false公海客户，lock=true非公海客户
        self.assertEqual(data["recycleType"], 1, msg=data["name"])  # 1手动丢公海，2自动丢公海
        self.assertEqual(data["recycleReason"], expect, msg=data["name"])
        self.assertEqual(data["recycleName"], us.getName(), msg=data["name"])

    # 我负责的客户列表默认展示
    def test_ownlist_Default(self):
        """我负责的客户列表：默认跟进时间顺序排序"""
        param = {
            "order": "asc",
            "tagsParams": [],
            "statusIds": [],
            "regional": {},
            "pageIndex": 1,
            "pageSize": 20,
            "field": "lastActAt"
        }
        result = self.cust.customer_OwnList(param)
        # 断言请求状态和错误码是否正确
        self.assertStatus(result)
        print('开发客户->我负责的列表响应时间：', result.elapsed.microseconds / 1000, 'ms')
        data = result.json()["data"]
        total_records = data["totalRecords"]
        records = data["records"]  # list
        actual_total = len(records)  # 实际数据数量
        if total_records > 0:
            first_last_actat = records[0]["lastActAt"]
        # 断言客户是否为开发客户，是否按跟进时间顺序排序
        for cus in records:
            self.assertEqual(cus["customerType"], 1, msg=cus["name"])  # 判断客户为开发客户
            self.assertTrue(first_last_actat <= cus["lastActAt"], msg=cus["name"])  # 判断列表按跟进时间顺序排序
            first_last_actat = cus["lastActAt"]
        # 断言返回的数据总数与实际数据数量是否相同
        if total_records > param["pageSize"]:
            page = math.ceil(total_records / param["pageSize"])
            for p in range(2, page + 1):
                param["pageIndex"] = p
                page_result = self.cust.customer_OwnList(param)
                self.assertStatus(page_result)
                page_records = page_result.json()["data"]["records"]
                actual_total += len(page_records)
                # 断言翻页客户是否为开发客户，是否按跟进时间顺序排序
                for cus in page_records:
                    self.assertEqual(cus["customerType"], 1, msg=cus["name"])  # 判断客户为开发客户
                    self.assertTrue(first_last_actat <= cus["lastActAt"], msg=cus["name"])  # 判断列表按跟进时间顺序排序
                    first_last_actat = cus["lastActAt"]
        print("我负责的客户实际数据数量", len(records))
        self.assertEqual(total_records, actual_total, msg='返回总数与实际数量总数不同')  # 判断返回的数据总数与实际数据数量是否相同

    # 我负责的客户列表跟进时间倒序排序
    def test_ownlist_lastActAt_desc(self):
        """我负责的客户列表：按跟进时间倒序排序"""
        param = {
            "order": "desc",
            "tagsParams": [],
            "statusIds": [],
            "regional": {},
            "pageIndex": 1,
            "pageSize": 20,
            "field": "lastActAt"
        }
        result = self.cust.customer_OwnList(param)
        # 断言请求状态和错误码是否正确
        self.assertStatus(result)
        data = result.json()["data"]
        total_records = data["totalRecords"]
        records = data["records"]  # list
        actual_total = len(records)  # 实际数据数量
        if total_records > 0:
            first_last_actat = records[0]["lastActAt"]
        # 断言客户是否为开发客户，是否按跟进时间顺序排序
        for cus in records:
            self.assertEqual(cus["customerType"], 1, msg=cus["name"])  # 判断客户为开发客户
            self.assertTrue(first_last_actat >= cus["lastActAt"], msg=cus["name"])  # 判断列表按跟进时间顺序排序
            first_last_actat = cus["lastActAt"]
        # 断言返回的数据总数与实际数据数量是否相同
        if total_records > param["pageSize"]:
            page = math.ceil(total_records / param["pageSize"])
            for p in range(2, page + 1):
                param["pageIndex"] = p
                page_result = self.cust.customer_OwnList(param)
                self.assertStatus(page_result)
                page_records = page_result.json()["data"]["records"]
                actual_total += len(page_records)
                # 断言翻页客户是否为开发客户，是否按跟进时间顺序排序
                for cus in page_records:
                    self.assertEqual(cus["customerType"], 1, msg=cus["name"])  # 判断客户为开发客户
                    self.assertTrue(first_last_actat >= cus["lastActAt"], msg=cus["name"])  # 判断列表按跟进时间顺序排序
                    first_last_actat = cus["lastActAt"]
        self.assertEqual(total_records, actual_total, msg='返回总数与实际数量总数不同')  # 判断返回的数据总数与实际数据数量是否相同

    # 我负责的客户列表搜索，判断搜索结果是否正确
    def test_ownlist_search(self):
        """我负责的客户列表搜索：关键字“成都”"""
        key = '成都'
        param = {
            "pageSize": 20,
            "keyWords": key,
            "pageIndex": 1
        }
        result = self.cust.customer_OwnList(param)
        # 断言请求状态和错误码是否正确
        self.assertStatus(result)
        data = result.json()["data"]
        total_records = data["totalRecords"]
        records = data["records"]  # list
        actual_total = len(records)  # 实际数据数量
        for cus in records:
            self.assertEqual(cus["customerType"], 1, msg=cus["name"])  # 判断客户为开发客户
            exp = (key in cus['name']) or (key in cus['loc']["addr"])  # 判断客户姓名或地址中包含搜索关键字，目前没判断联系人
            self.assertTrue(exp)
        if total_records > param["pageSize"]:
            page = math.ceil(total_records / param["pageSize"])
            for p in range(2, page + 1):
                param["pageIndex"] = p
                page_result = self.cust.customer_OwnList(param)
                self.assertStatus(page_result)
                page_records = page_result.json()["data"]["records"]
                actual_total += len(page_records)
                for cus in page_records:
                    self.assertEqual(cus["customerType"], 1, msg=cus["name"])  # 判断客户为开发客户
                    exp = (key in cus['name']) or (key in cus['loc']["addr"])  # 判断客户姓名或地址中包含搜索关键字，目前没判断联系人
                    self.assertTrue(exp)
        self.assertEqual(total_records, actual_total)  # 判断返回的数据总数与实际数据数量是否相同
        # 断言搜索结果是否在客户名称或地址中包含搜索关键字

    # 我参与的客户列表：默认跟进时间顺序排序
    def test_linkList(self):
        """我参与的客户：默认跟进时间顺序排序"""
        param = {
            "order": "asc",
            "tagsParams": [],
            "statusIds": [],
            "regional": {},
            "pageIndex": 1,
            "pageSize": 20,
            "field": "lastActAt"
        }
        result = self.cust.customer_link(param)
        # 断言请求状态和错误码是否正确
        self.assertStatus(result)
        print('开发客户->我参与的列表响应时间：', result.elapsed.microseconds / 1000, 'ms')
        data = result.json()["data"]
        total_records = data["totalRecords"]
        records = data["records"]  # list
        if records is None and total_records == 0:
            return None
        actual_total = len(records)  # 实际数据数量
        if total_records > 0:
            first_last_actat = records[0]["lastActAt"]
        # 断言客户是否为开发客户，是否按跟进时间顺序排序
        for cus in records:
            self.assertEqual(cus["customerType"], 1, msg=cus["name"])  # 判断客户为开发客户
            self.assertTrue(first_last_actat <= cus["lastActAt"], msg=cus["name"])  # 判断列表按跟进时间顺序排序
            first_last_actat = cus["lastActAt"]
        if total_records == 0:
            self.assertTrue(records is None)
        elif total_records > param["pageSize"]:
            page = math.ceil(total_records / param["pageSize"])
            for p in range(2, page + 1):
                param["pageIndex"] = p
                page_result = self.cust.customer_link(param)
                self.assertStatus(page_result)
                page_records = page_result.json()["data"]["records"]
                actual_total += len(page_records)
                # 断言数据为开发客户且排序正确
                for cus in page_records:
                    self.assertEqual(cus["customerType"], 1, msg=cus["name"])  # 判断客户为开发客户
                    self.assertTrue(first_last_actat <= cus["lastActAt"], msg=cus["name"])  # 判断列表按跟进时间顺序排序
                    first_last_actat = cus["lastActAt"]
        print("我参与的客户数量", total_records)
        self.assertEqual(total_records, actual_total)  # 判断返回的总数是否与实际数量相同

    # 团队的客户列表：默认跟进时间顺序排序
    def test_teamList(self):
        """团队的客户列表：默认跟进时间顺序排序"""
        param = {
            "field": "lastActAt",
            "order": "asc",
            "xpath": "",
            "pageSize": 20,
            "pageIndex": 1,
            "userId": "",
            "tagsParams": [],
            "statusIds": [],
            "regional": {}
        }
        result = self.cust.customer_team(param)
        # 断言请求状态和错误码是否正确
        self.assertStatus(result)
        print('开发客户->团队客户的列表响应时间：', result.elapsed.microseconds / 1000, 'ms')
        data = result.json()["data"]
        total_records = data["totalRecords"]
        records = data["records"]  # list
        actual_total = len(records)  # 实际数据数量
        if total_records > 0:
            first_last_actat = records[0]["lastActAt"]
        # 断言数据为开发客户且按跟进时间顺序排序
        for cus in records:
            self.assertEqual(cus["customerType"], 1, msg=cus["name"])  # 判断客户为开发客户
            self.assertTrue(first_last_actat <= cus["lastActAt"], msg=cus["name"])  # 判断列表按跟进时间顺序排序
            first_last_actat = cus["lastActAt"]
        if total_records > param["pageSize"]:
            page = math.ceil(total_records / param["pageSize"])
            for p in range(2, page + 1):
                param["pageIndex"] = p
                page_result = self.cust.customer_team(param)
                self.assertStatus(page_result)
                page_records = page_result.json()["data"]["records"]
                actual_total += len(page_records)
                # 断言数据为开发客户且按跟进时间顺序排序
                for cus in page_records:
                    self.assertEqual(cus["customerType"], 1, msg=cus["name"])  # 判断客户为开发客户
                    self.assertTrue(first_last_actat <= cus["lastActAt"], msg=cus["name"])
                    first_last_actat = cus["lastActAt"]
        print("团队客户实际返回数据数量", actual_total)
        self.assertEqual(total_records, actual_total)  # 判断返回的总数是否与实际数量相同

    # 测试团队的客户列表：按人员查询
    def test_teamList_dept(self):
        """测试团队的客户列表：按人员查询:刘洋C"""
        us = user.User()
        param = {
            "field": "lastActAt",
            "order": "asc",
            "xpath": "",
            "pageSize": 20,
            "pageIndex": 1,
            "userId": us.get_UserId("刘洋C"),
            "tagsParams": [],
            "statusIds": [],
            "regional": {}
        }
        result = self.cust.customer_team(param)
        # 断言请求状态和错误码是否正确
        self.assertStatus(result)
        print('开发客户->团队客户的列表响应时间：', result.elapsed.microseconds / 1000, 'ms')
        data = result.json()["data"]
        total_records = data["totalRecords"]
        records = data["records"]  # list
        actual_total = len(records)  # 实际数据数量
        if total_records > 0:
            first_last_actat = records[0]["lastActAt"]
        # 断言数据为开发客户且按跟进时间顺序排序
        for cus in records:
            self.assertEqual(cus["customerType"], 1, msg=cus["name"])  # 判断客户为开发客户
            self.assertEqual(cus["ownerName"], "刘洋C", msg=cus["name"])
            self.assertTrue(first_last_actat <= cus["lastActAt"], msg=cus["name"])  # 判断列表按跟进时间倒叙排序
            first_last_actat = cus["lastActAt"]
        if total_records > param["pageSize"]:
            page = math.ceil(total_records / param["pageSize"])
            for p in range(2, page + 1):
                param["pageIndex"] = p
                page_result = self.cust.customer_team(param)
                self.assertStatus(page_result)
                page_records = page_result.json()["data"]["records"]
                actual_total += len(page_records)
                for cus in page_records:
                    self.assertEqual(cus["customerType"], 1, msg=cus["name"])  # 判断客户为开发客户
                    self.assertEqual(cus["ownerName"], "刘洋C", msg=cus["name"])
                    self.assertTrue(first_last_actat <= cus["lastActAt"], msg=cus["name"])  # 判断列表按跟进时间倒叙排序
                    first_last_actat = cus["lastActAt"]
        print("团队客户按人员查询结果数量", actual_total)
        # 断言返回的总数是否与实际数量相同
        self.assertEqual(total_records, actual_total)

    @classmethod
    def tearDownClass(cls):
        print('客户管理：end')


if __name__ == "__main__":
    file = "C:\\Users\\Administrator\\AppInterfaceTest\\testCase\\customer"
    testcase = unittest.TestSuite()
    discover = unittest.defaultTestLoader.discover(file, "test*.py", top_level_dir=None)
    for suite in discover:
        for case in suite:
            testcase.addTest(case)
    report = "C:\\Users\\Administrator\\AppInterfaceTest\\customer.html"
    fp = open(report, "wb")
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title="开发客户测试", description="开发客户接口测试")
    run = runner.run(testcase)
    fp.close()

