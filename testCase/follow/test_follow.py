import unittest, random, time, math
import uuid
from datetime import datetime  # datetime是模块，模块中还有一个datetime类
from commom import attachments
from testCase.follow import follow
from commom import get_Time_Type
from testCase.user import user
from testCase.customer import customerManger
from testCase.salesleads import salesleads


class FollowCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.cust = customerManger.CustomerManger()
        cls.fo = follow.Follow()
        cls.org = user.User()
        print("快速记录测试：start")

    # 测试写跟进客户列表数据
    def test_similar_custlist(self):
        """测试写跟进客户列表，按跟进倒叙"""
        param = {
            "isAll": False,   # true，全公司数据，false排除公海客户
            "isSelf": True,   # true 我负责的和我参与的，false的情况没有
            "pageIndex": 1,
            "pageSize": 10      # 写跟进客户列表IOS每页获取10条 Android获取的是20
        }
        result = self.cust.customer_similar(param)
        self.assertEqual(result.status_code, 200, msg=result.text)
        result_json = result.json()
        self.assertEqual(result_json["errcode"], 0, msg=result.text)
        self.assertEqual(result_json["errmsg"], "success", msg=result.text)
        total_records = result_json["data"]["totalRecords"]
        records = result_json["data"]["records"]
        if total_records == 0:
            self.assertTrue(len(records) == 0, msg=result.text)
            return
        first_at = records[0]["lastActAt"]
        for cus in records:
            self.assertTrue(first_at >= cus["lastActAt"], msg=cus["name"])
            first_at = cus["lastActAt"]
        actual_total = len(records)
        if total_records >= param["pageSize"]:
            page = math.ceil(total_records/param["pageSize"])
            for p in range(2, page+1):
                param["pageIndex"] = p
                page_result = self.cust.customer_similar(param)
                self.assertEqual(page_result.status_code, 200, msg=page_result.text)
                page_result_json = page_result.json()
                self.assertEqual(page_result_json["errcode"], 0, msg=page_result.text)
                self.assertEqual(page_result_json["errmsg"], "success", msg=page_result.text)
                page_records = page_result_json["data"]["records"]
                for cus in page_records:
                    self.assertTrue(first_at >= cus["lastActAt"], msg=cus["name"] + "跟进时间：" + str(cus["lastActAt"]))
                    first_at = cus["lastActAt"]
                actual_total += len(page_records)
        print(actual_total)
        self.assertEqual(total_records, actual_total, msg="写跟进选择客户列表客户实际数量与总数不对应！")

    # 测试写跟进时获取到的客户信息正确
    def test_new_activity(self):
        """测试写跟进时获取到的客户信息正确"""
        customer_id = self.cust.get_similar_customer()["id"]
        cust_detail = self.cust.customer_detail(customer_id).json()["data"]
        result = self.fo.new_activity(customer_id)
        self.assertEqual(result.status_code, 200, msg=result.text)
        result_json = result.json()
        self.assertEqual(result_json["errcode"], 0, msg=result.text)
        self.assertEqual(result_json["errmsg"], "success", msg=result.text)
        activity_data = result_json["data"]
        # 断言+跟进时获取到的客户信息与客户详情信息是否一致
        self.assertEqual(activity_data["id"], customer_id, msg=customer_id)
        self.assertEqual(activity_data["name"], cust_detail["name"], msg=customer_id)
        self.assertEqual(activity_data["statusName"], cust_detail["statusName"], msg=customer_id)
        if "contacts" in activity_data:
            # 断言默认联系人相同
            self.assertEqual(activity_data["contacts"][0]["name"], cust_detail["contacts"][0]["name"], msg=customer_id)

    # 添加快速记录-客户
    def test_create_follow_001(self):
        """客户添加快速记录：填写所有系统字段"""
        u = user.User()
        customer_id = self.cust.get_similar_customer()["id"]
        fo = follow.Follow()
        type_id = fo.get_activity_type_id()  # 记录行为中任意一个行为的id
        cust_data = self.fo.new_activity(customer_id).json()["data"]
        data = {
            "uuid": attachments.attachments('0')['UUId'],
            "audioInfo": [{    # 录音文件
                "length": 4,
                "fileName": "CEC338E0-D700-41FC-9A8C-8435477C3414/153197011674852.wav"
            }],
            "remindAt": int(datetime.now().timestamp()+90000),   # 25小时以后
            "typeId": type_id,                                   # 记录行为ID
            "atUserIds": [u.get_UserId("陈老师")],               # @人员
            "contactPhone": "",                        # 联系人电话
            "contactName": "",                               # 联系人姓名
            "tags": [],  # 标签
            "customerId": customer_id,  # 客户ID
            "extUpdateAt": 1512959975,
            "location": {    # 定位
                "loc": [30.689161, 104.0737],
                "addr": "成都龙腾越人力资源管理有限公司(今年万达甲级写字楼B座3101)"
            },
            "isEnableCus": True,
            "contactRoleId": "",                # 联系人角色ID
            "extFields": {},  # 自定义字段
            "content": "接口写跟进，没填写自定义字段" + str(random.randint(100, 10000))    # 跟进内容
        }
        if "tags" in cust_data:
            data["tags"] = cust_data["tags"]
        if "contacts" in cust_data:
            data["contactId"] = cust_data["contacts"][0]["id"]
            data["contactName"] = cust_data["contacts"][0]["name"]
            if len(cust_data["contacts"][0]["tel"]) != 0:
                data["contactPhone"] = cust_data["contacts"][0]["tel"][0]
            elif len(cust_data["contacts"][0]["wiretel"]) != 0:
                data["contactPhone"] = cust_data["contacts"][0]["wiretel"][0]
            if "contactRoleId" in cust_data["contacts"][0]:
                data["contactRoleId"] = cust_data["contacts"][0]["contactRoleId"]

        """
        # 测试提醒时时间时写的循环
        for i in range(8, 25):
            data["remindAt"] = int(datetime.now().timestamp()) + i*3600
            data["content"] = "发布后写的跟进" + str(random.randint(100, 10000))
        """
        result = fo.create_follow(data)
        self.assertEqual(result.status_code, 200, msg=result.text)
        result_json = result.json()
        self.assertEqual(result_json['errcode'], 0, msg=result.text)
        self.assertEqual(result_json['errmsg'], 'success', msg=result.text)
        # 断言下跟进内容
        follow_response = result_json["data"]
        self.assertEqual(data["content"], follow_response["content"], msg='跟进内容与填写不一致')   # 检查客户名称、跟进内容、记录行为、下次跟进时间等是否一致
        self.assertEqual(data["customerId"], follow_response["customerId"], msg='客户ID与所填写不一致')
        self.assertEqual(data["typeId"], follow_response["typeId"], msg='记录行为ID与所填写不同')
        self.assertEqual(data["remindAt"], follow_response["remindAt"], msg="下次跟进时间错误")

    # 添加快速记录-线索
    def test_create_follow_002(self):
        """新建线索快速记录"""
        sale_id = self.fo.get_saleslead()["id"]
        sale = salesleads.Salesleades()
        sale_detail = sale.salesleads_detail(sale_id).json()["data"]["sales"]
        data = {
                "typeId": self.fo.get_activity_type_id(),
                "content": "线索写跟进" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())),
                "contactName": sale_detail["name"],
                "isEnableCus": True,
                "saleLeadStatus": sale_detail["status"],
                "uuid": str(uuid.uuid1()),
                "remindAt": int(datetime.now().timestamp() + 172800),   # 2天后提醒
                "audioInfo": [],
                "sealsleadId": sale_id,
                "tags": []
            }
        if "tags" in sale_detail:
            data["tags"] = sale_detail["tags"]
        result = self.fo.create_follow(data)
        self.assertEqual(result.status_code, 200, msg=result.text)
        result_json = result.json()
        self.assertEqual(result_json["errcode"], 0, msg=result.text)
        self.assertEqual(result_json["errmsg"], "success", msg=result.text)
        self.assertEqual(data["sealsleadId"], result_json["data"]["sealsleadId"], msg=result.text)              # 线索id
        self.assertEqual(data["content"], result_json["data"]["content"], msg=result.text)                      # 跟进内容
        self.assertEqual(data["remindAt"], result_json["data"]["remindAt"], msg=result.text)                    # 下次提醒时间
        self.assertEqual(data["typeId"], result_json["data"]["typeId"])                                         # 记录行为

    # 最近30天,跟进时间倒序组合查询
    def test_followList_001(self):
        """跟进时间最近30天,跟进时间倒序组合查询"""
        start_at, end_at = get_Time_Type.getTimeRegionByType("TheLast30Day")
        param = {
            "startAt": start_at,
            "endAt": end_at,
            "visitType": 2,             # 2代表跟进记录，3代表商务电话，5智能办公电话
            "field": "createdAt",       # 排序字段
            "filterTimeType": 1,        # "时间过滤字段 1:跟进时间 2:下次跟进时间"
            "orderBy": "desc",
            "method": 0,                # 跟进类型0:全部  1:开发客户跟进  2:线索跟进 3:签约客户跟进
            "pageIndex": 1,
            "pageSize": 10,
            "split": 1                  # 附件是否分割为图片和文件2个数组
            }
        result = self.fo.follow_list(param)
        self.assertEqual(result.status_code, 200, msg=result.text)
        result_json = result.json()
        self.assertEqual(result_json["errcode"], 0, msg=result.text)
        self.assertEqual(result_json["errmsg"], "success", msg=result.text)
        data = result_json["data"]
        total_records = data["totalRecords"]
        records = data["records"]
        if total_records == 0:
            self.assertTrue(records is None, msg=result.text)
            return None
        first_at = records[0]["createdAt"]
        actual_total = len(records)
        for fol in records:
            self.assertTrue(first_at >= fol["createdAt"])  # 断言列表按创建时间倒叙排序
            self.assertTrue(start_at <= fol["createdAt"] <= end_at)  # 判断第一页返回的数据属于最近30天新建的
            first_at = fol["createdAt"]
        if total_records > param["pageSize"]:
            page = math.ceil(total_records / param["pageSize"])
            for p in range(2, page + 1):
                param["pageIndex"] = p
                page_result = self.fo.follow_list(param)
                self.assertEqual(page_result.status_code, 200, msg=page_result.text)
                page_json = page_result.json()
                self.assertEqual(page_json["errcode"], 0, msg=page_result.text)
                self.assertEqual(page_json["errmsg"], "success", msg=page_result.text)
                page_records = page_json["data"]["records"]
                actual_total += len(page_records)
                for fol in page_records:
                    self.assertTrue(first_at >= fol["createdAt"])  # 判断列表按创建时间倒叙排序
                    self.assertTrue(start_at <= fol["createdAt"] <= end_at)  # 判断返回的数据属于最近30天新建的
                    first_at = fol["createdAt"]
        print("快速记录最近30天实际跟进数量", actual_total)
        self.assertEqual(total_records, actual_total)   # 判断返回的总数是否与实际数量相同

    # 最近7天+下次跟进时间倒叙组合查询
    def test_followList_002(self):
        """跟进时间最近7天，下次跟进时间倒叙组合查询"""
        start_at, end_at = get_Time_Type.getTimeRegionByType("LastSevenDay")
        param = {
            "field": "remindAt",         # 排序字段
            "orderBy": "desc",          # 排序方式 asc:升序  desc:降序
            "filterTimeType": 1,        # "时间过滤字段 1:跟进时间时间 2:下次跟进时间"
            "startAt": start_at,
            "endAt": end_at,
            "method": 0,                # 跟进类型0:全部  1:开发客户跟进  2:线索跟进 3:签约客户跟进
            "visitType": 2,             # 2代表跟进记录，3代表商务电话,5智能办公电话
            "pageIndex	": 1,
            "pageSize": 10,
            "split": 1                  # 图片和文件分开
        }
        result = self.fo.follow_list(param)
        self.assertEqual(result.status_code, 200, msg=result.text)
        result_json = result.json()
        self.assertEqual(result_json["errcode"], 0, msg=result.text)
        self.assertEqual(result_json["errmsg"], "success", msg=result.text)
        total_records = result_json["data"]["totalRecords"]

        records = result_json["data"]["records"]  # list
        if total_records == 0:
            self.assertEqual(records, None)
            return
        actual_total = len(records)
        first_at = records[0]["remindAt"]
        for fol in records:
            self.assertTrue(param["startAt"] <= fol["createAt"] <= param["endAt"], msg=fol["createAt"])   # 断言跟进时间属于最近7天
            if "remindAt" not in fol:
                continue
            self.assertTrue(first_at >= fol["remindAt"], msg=fol["remindAt"])                             # 断言下次提醒时间倒叙排序
            first_at = fol["remindAt"]
        if total_records > param["pageSize"]:
            page = math.ceil(total_records / param["pageSize"])
            for p in range(2, page + 1):
                param["pageIndex"] = p
                page_result = self.fo.follow_list(param)
                self.assertEqual(page_result.status_code, 200, msg=page_result.text)
                page_json = page_result.json()
                self.assertEqual(page_json["errmsg"], "success", msg=p)
                page_records = page_json["data"]["records"]
                actual_total += len(page_records)
                for fol in page_records:
                    # 断言跟进时间属于最近7天
                    self.assertTrue(param["startAt"] <= fol["createAt"] <= param["endAt"], msg=fol["createAt"])
                    if "remindAt" not in fol:
                        continue
                    self.assertTrue(first_at >= fol["remindAt"], msg=fol["remindAt"])        # 断言下次提醒时间倒叙排序
                    first_at = fol["remindAt"]
        self.assertEqual(total_records, actual_total, msg="返回的数据总数与实际数据数量不符")
        print("快速记录最近7天实际跟进数量", actual_total)

    # 部门+记录行为+跟进对象+跟进时间顺序组合查询
    def test_followList_003(self):
        """部门+记录行为+跟进对象+跟进时间顺序组合查询"""
        dept = self.org.get_Dept("总经办")
        param = {
            "field": "createAt",    # 排序字段
            "orderBy": "asc",       # 排序方式 asc:升序  desc:降序
            "filterTimeType": 1,    # "时间过滤字段 1:跟进时间时间 2:下次跟进时间"
            "startAt": "",
            "endAt": "",
            "method": 1,            # 跟进类型0:全部  1:开发客户跟进  2:线索跟进 3:签约客户跟进
            "visitType": 2,         # 2代表跟进记录，3代表商务电话,5智能办公电话
            "pageIndex	": 1,
            "pageSize": 10,
            "split": 1,              # 图片和文件分开
            "xpath": dept["xpath"],
            "typeId": self.fo.get_activity_type_id()    # 记录行为ID
        }
        dept_users = dept["users"]   # 获取部门人员
        result = self.fo.follow_list(param)
        self.assertEqual(result.status_code, 200, msg=result.text)
        result_json = result.json()
        self.assertEqual(result_json["errcode"], 0, msg=result.text)
        self.assertEqual(result_json["errmsg"], "success", msg=result.text)
        total_records = result_json["data"]["totalRecords"]
        records = result_json["data"]["records"]  # list
        if total_records == 0:
            self.assertTrue(records is None, msg="跟进总数错误")
            return
        actual_total = len(records)
        first_at = records[0]["createAt"]
        # 断言第一页的数据
        for fol in records:
            self.assertEqual(fol["customerType"], 1, msg=fol["createAt"])        # customerType客户类型 0.销售线索 1.开发客户 2.签约客户
            self.assertEqual(fol["typeId"], param["typeId"], msg=fol["createAt"])   # 断言记录行为是查询条件的记录行为
            self.assertTrue(first_at <= fol["createAt"], msg=fol["createAt"])       # 断言按照跟进时间顺序排序
            first_at = fol["createAt"]
            switch = False
            for us in dept_users:                                                # 断言跟进创建者id属于所选部门人员
                if fol["creatorId"] == us["id"]:
                    switch = True
                    break
            self.assertTrue(switch, msg="跟进创建人不属于该部门" + str(fol["createAt"]))

        if total_records > param["pageSize"]:
            page = math.ceil(total_records / param["pageSize"])
            for p in range(2, page + 1):
                param["pageIndex"] = p
                page_result = self.fo.follow_list(param)
                self.assertEqual(page_result.status_code, 200, msg='翻页错误')
                page_json = page_result.json()
                self.assertEqual(page_json["errmsg"], "success", msg='翻页错误')
                page_records = page_json["data"]["records"]
                actual_total += len(page_records)
                for fol in page_records:
                    self.assertEqual(fol["customerType"], 1,
                                     msg=fol["createAt"])  # customerType客户类型 0.销售线索 1.开发客户 2.签约客户
                    self.assertEqual(fol["typeId"], param["typeId"], msg=fol["createAt"])  # 断言记录行为是查询条件的记录行为
                    self.assertTrue(first_at <= fol["createAt"], msg=fol["createAt"])  # 断言按照跟进时间顺序排序
                    first_at = fol["createAt"]
                    switch = False
                    for us in dept_users:  # 断言跟进创建者id属于所选部门人员
                        if fol["creatorId"] == us["id"]:
                            switch = True
                            break
                    self.assertTrue(switch, msg="跟进创建人不属于该部门" + str(fol["createAt"]))
        self.assertEqual(total_records, actual_total, msg="返回数据总数与实际数据数量不等")
        print(actual_total, "记录id：", param["typeId"])

    # 下次跟进时间本月+跟进对象+下次跟进时间顺序组合筛选
    def test_followList_004(self):
        """下次跟进时间本月+跟进对象+下次跟进时间顺序组合筛选"""
        start_at, end_at = get_Time_Type.getTimeRegionByType("TheMonth")
        param = {
            "startAt": start_at,
            "endAt": end_at,
            "visitType": 2,         # 2代表跟进记录，3代表商务电话，5智能办公电话
            "field": "remindAt",    # 排序字段
            "filterTimeType": 2,    # "时间过滤字段 1:跟进时间 2:下次跟进时间"
            "orderBy": "asc",
            "method": 2,            # 跟进类型0:全部  1:开发客户跟进  2:线索跟进 3:签约客户跟进
            "pageIndex": 1,
            "pageSize": 10,
            "split": 1              # 附件是否分割为图片和文件2个数组
        }
        result = self.fo.follow_list(param)
        self.assertEqual(result.status_code, 200, msg=result.text)
        result_json = result.json()
        self.assertEqual(result_json["errcode"], 0, msg=result.text)
        self.assertEqual(result_json["errmsg"], "success", msg=result.text)
        data = result_json["data"]
        total_records = data["totalRecords"]
        records = data["records"]
        if total_records == 0:
            self.assertTrue(records is None, msg=result.text)
            return None
        first_at = records[0]["remindAt"]
        actual_total = len(records)
        for fol in records:
            self.assertEqual(fol["customerType"], 0, msg=fol["remindAt"])  # customerType客户类型 0.销售线索 1.开发客户 2.签约客户
            self.assertTrue(first_at <= fol["remindAt"], msg=fol["remindAt"])            # 断言列表按下次提醒时间顺序排序
            self.assertTrue(start_at <= fol["remindAt"] <= end_at, msg=fol["remindAt"])  # 判断第一页返回的数据属于下次提醒时间属于本月
            first_at = fol["remindAt"]
        if total_records > param["pageSize"]:
            page = math.ceil(total_records / param["pageSize"])
            for p in range(2, page + 1):
                param["pageIndex"] = p
                page_result = self.fo.follow_list(param)
                self.assertEqual(page_result.status_code, 200, msg=page_result.text)
                page_json = page_result.json()
                self.assertEqual(page_json["errcode"], 0, msg=page_result.text)
                self.assertEqual(page_json["errmsg"], "success", msg=page_result.text)
                page_records = page_json["data"]["records"]
                actual_total += len(page_records)
                for fol in page_records:
                    self.assertEqual(fol["customerType"], 0,
                                     msg=fol["remindAt"])  # customerType客户类型 0.销售线索 1.开发客户 2.签约客户
                    self.assertTrue(first_at <= fol["remindAt"], msg=fol["remindAt"])  # 断言列表按下次提醒时间顺序排序
                    self.assertTrue(start_at <= fol["remindAt"] <= end_at, msg=fol["remindAt"])  # 判断第一页返回的数据属于下次提醒时间属于本月
                    first_at = fol["remindAt"]
        print("快速记录下次提醒时间为本月的线索跟进数量：", actual_total)
        self.assertEqual(total_records, actual_total)  # 判断返回的总数是否与实际数量相同

    # 快速记录列表搜索
    def test_followList_005(self):
        """快速记录列表搜索跟进内容/跟进对象/联系人：关键字'测试'"""
        key_words = "李白"
        param = {
            "keyWords": key_words,
            "pageIndex": 1,
            "pageSize": 10,
            "split": 1,
            "visitType": 2      # 2代表跟进记录，3代表商务电话，5智能办公电话
        }
        result = self.fo.follow_list(param)
        self.assertEqual(result.status_code, 200, msg=result.text)
        result_json = result.json()
        self.assertEqual(result_json["errcode"], 0, msg=result.text)
        self.assertEqual(result_json["errmsg"], "success", msg=result.text)
        total_records = result_json["data"]["totalRecords"]
        records = result_json["data"]["records"]
        if total_records == 0:
            self.assertTrue(records is None, msg=records)
            return
        actual_total = len(records)
        first_at = records[0]["createAt"]
        for fol in records:
            if fol["customerType"] == 0:      # customerType客户类型 0.销售线索 1.开发客户 2.签约客户
                self.assertTrue(param["keyWords"] in fol["content"] or param["keyWords"] in fol["contactName"],
                                msg=fol)
            elif (fol["customerType"] == 1 or fol["customerType"] == 2) and "contactName" in fol:
                self.assertTrue(param["keyWords"] in fol["content"] or param["keyWords"] in fol["contactName"] or
                                param["keyWords"] in fol["customerName"], msg=fol)
            elif (fol["customerType"] == 1 or fol["customerType"] == 2) and "contactName" not in fol:
                self.assertTrue(param["keyWords"] in fol["content"] or param["keyWords"] in fol["customerName"],
                                msg=fol)
            self.assertTrue(first_at >= fol["createAt"], msg=["createAt"])  # 搜索结果按跟进时间倒叙排序
            first_at = fol["createAt"]
        if total_records > param["pageSize"]:
            page = math.ceil(total_records / param["pageSize"])
            for p in range(2, page + 1):
                param["pageIndex"] = p
                page_result = self.fo.follow_list(param)
                self.assertEqual(page_result.status_code, 200, msg=page_result.text)
                page_json = page_result.json()
                self.assertEqual(page_json["errcode"], 0, msg=page_result.text)
                self.assertEqual(page_json["errmsg"], "success", msg=page_result.text)
                page_records = page_json["data"]["records"]
                actual_total += len(page_records)
                for fol in page_records:
                    if fol["customerType"] == 0:  # customerType客户类型 0.销售线索 1.开发客户 2.签约客户
                        self.assertTrue(param["keyWords"] in fol["content"] or param["keyWords"] in fol["contactName"],
                                        msg=fol)
                    elif (fol["customerType"] == 1 or fol["customerType"] == 2) and "contactName" in fol:
                        self.assertTrue(param["keyWords"] in fol["content"] or param["keyWords"] in fol["contactName"]
                                        or param["keyWords"] in fol["customerName"], msg=fol)
                    elif (fol["customerType"] == 1 or fol["customerType"] == 2) and "contactName" not in fol:
                        self.assertTrue(param["keyWords"] in fol["content"] or param["keyWords"] in fol["customerName"],
                                        msg=fol)
                    self.assertTrue(first_at >= fol["createAt"], msg=["createAt"])
                    first_at = fol["createAt"]
        print("快速记录搜索结果数量：", actual_total)
        self.assertEqual(total_records, actual_total)  # 判断返回的总数是否与实际数量相同

    # 测试获取记录行为
    def test_get_saleactivitytype(self):
        """测试获取记录行为"""
        f = follow.Follow()
        result = f.get_activity_type()
        self.assertEqual(result.status_code, 200, msg=result.text)
        result_json = result.json()
        self.assertEqual(result_json["errcode"], 0, msg=result.text)
        self.assertEqual(result_json["errmsg"], "success", msg=result.text)
        self.assertTrue(len(result_json['data']) >= 1)   # 判断范围的记录行为有值，记录行为至少有默认值

    @classmethod
    def tearDownClass(cls):
        print('快速记录测试：end')

    if __name__ == "__main__":
        unittest.main()



