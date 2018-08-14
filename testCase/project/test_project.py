import time
import unittest
import math
import random
import readConfig
from testCase.project import project
from testCase.user import user


class ProjectCase(unittest.TestCase):

    # project用例执行前初始化参数
    @classmethod
    def setUpClass(cls):
        print("项目管理：start")
        # 获取登录人Id
        fp = readConfig.ReadConfig()
        cls.user_id = fp.getUserValue("userid")
        cls.pro = project.Project()
        cls.param = {
            "pageIndex": 1,
            "pageSize": 20,
            "keyword": "",
            "status": 1,        # 0 全部状态 1 进行中 2已完成
            "type": 2           # 0 全部类型 1 我参与的 2 我创建的 3 我负责的
        }
        # 获取我创建的最新一个项目id
        try:
            cls.project_id = cls.pro.my_list(cls.param).json()["data"]["records"][0]["id"]
        except Exception as e:
            print("获取项目id出错！", e)
        cls.us = user.User()

    # 每条用例执行前初始化param
    def setUp(self):
        self.param["pageIndex"] = 1
        self.param["pageSize"] = 20
        self.param["keyword"] = ""
        self.param["status"] = 0
        self.param["type"] = 0

    # 我的项目列表
    def test_my_list_001(self):
        """我的项目列表：默认数据"""
        result = self.pro.my_list(self.param)
        # 判断请求状态
        self.assertEqual(result.status_code, 200, msg=result.status_code)  # 判断请求状态是否为200
        req_json = result.json()
        self.assertEqual(req_json["errcode"], 0, msg=req_json["errcode"])  # 判断错误码是否为0
        self.assertEqual(req_json["errmsg"], "success", msg=req_json["errmsg"])  # 判断错误信息是否为success
        data = req_json["data"]
        total_records = data["totalRecords"]
        records = data["records"]
        actual_total = len(records)
        if total_records > self.param["pageSize"]:
            page = math.ceil(total_records/self.param["pageSize"])
            for p in range(2, page+1):
                self.param["pageIndex"] = p
                page_result = self.pro.my_list(self.param)
                self.assertEqual(page_result.status_code, 200, msg=page_result.status_code)  # 判断翻页获取数据是否正确
                page_json = page_result.json()
                self.assertEqual(page_json["errcode"], 0, msg=page_json["errcode"])  # 判断翻页错误码是否为0
                self.assertEqual(page_json["errmsg"], "success", msg=page_json["errmsg"])
                page_records = page_json["data"]["records"]
                actual_total += len(page_records)
        self.assertEqual(total_records, actual_total, msg=actual_total)  # 判断实际数据数量是否与返回的数据总数相同
        print("test my project list actual number:", actual_total)

    # 我的项目列表-搜索
    def test_my_list_002(self):
        """我的项目列表：搜索项目名称及内容"""
        self.param["keyword"] = "测试"
        result = self.pro.my_list(self.param)
        # 判断请求状态
        self.assertEqual(result.status_code, 200, msg=result.status_code)  # 判断请求状态是否为200
        req_json = result.json()
        self.assertEqual(req_json["errcode"], 0, msg=req_json["errcode"])  # 判断错误码是否为0
        self.assertEqual(req_json["errmsg"], "success", msg=req_json["errmsg"])  # 判断错误信息是否为success
        data = req_json["data"]
        total_records = data["totalRecords"]
        records = data["records"]
        # 判断搜索结果项目名称或项目简介是否包含关键字
        for re in records:
            # 搜索结果项目标题或简介包含keyword
            exp = (self.param["keyword"] in re["title"]) or (self.param["keyword"] in re["content"])
            self.assertTrue(exp, msg=re["title"])
        actual_total = len(records)
        # 查看翻页数据是否正确
        if total_records > self.param["pageSize"]:
            page = math.ceil(total_records / self.param["pageSize"])
            for p in range(2, page + 1):
                self.param["pageIndex"] = p
                page_result = self.pro.my_list(self.param)
                self.assertEqual(page_result.status_code, 200, msg=page_result.status_code)  # 判断翻页获取数据是否正确
                page_json = page_result.json()
                self.assertEqual(page_json["errcode"], 0, msg=page_json["errcode"])  # 判断翻页错误码是否为0
                self.assertEqual(page_json["errmsg"], "success", msg=page_json["errmsg"])
                page_records = page_json["data"]["records"]
                # 判断搜索结果翻页项目名称或项目简介是否包含关键字
                for re in page_records:
                    # 搜索结果项目标题或简介包含keyword
                    exp = (self.param["keyword"] in re["title"]) or (self.param["keyword"] in re["content"])
                    self.assertTrue(exp, msg=re["title"])
                actual_total += len(page_records)
        self.assertEqual(total_records, actual_total, msg=actual_total)  # 判断实际数据数量是否与返回的数据总数相同
        print("test my project list search result actual number:", actual_total)

    # 测试项目详情
    def test_project_detail(self):
        result = self.pro.project_detail(self.project_id)
        # 判断请求返回状态
        self.assertEqual(result.status_code, 200, msg=result.status_code)
        resp_json = result.json()
        # 判断返回body内容
        self.assertTrue(self.project_id == resp_json["id"])                 # 判断返回内容项目ID与请求ID是否一致

    # 获取项目模板
    def test_get_temp(self):
        """获取项目模板接口"""
        result = self.pro.get_temp()
        self.assertEqual(result.status_code, 200, msg=result.status_code)
        response_json = result.json()
        errcode = response_json["errcode"]
        errmsg = response_json["errmsg"]
        self.assertEqual(errcode, 0, msg=errcode)
        self.assertEqual(errmsg, errmsg, msg=errmsg)
        data = response_json["data"]
        nodes_exp = ["会议纪要与执行", "项目服务", "项目跟进", "销售人员招聘", "员工培训", "招标"]
        for node in data:
            self.assertTrue(node["nodeName"] in nodes_exp, msg=node["nodeName"])    # 判断返回的节点均属于5个节点之一

    # 新建项目
    def test_create_project(self):
        """新建项目用例：填写所有字段 """
        self.param["isAll"] = True
        self.param["isSelf"] = False
        customerId, customerName = self.pro.get_customer_similar(self.param)
        managers = self.us.get_User('刘洋C')
        members = [self.us.get_User('claire'), self.us.get_User('冉云A')]
        # 获取第一个项目模板的id
        try:
            project_temp_id = self.pro.get_temp().json()['data'][0]["id"]
        except Exception as e:
            print("get temp_list fail!", e)
        requestdata = {
            "title": "项目"+time.strftime("%Y-%m-%d %H:%M", time.localtime(int(time.time()))),
            "content": "项目简介测试",
            "managers": [{
                "canReadAll": True,
                "user": managers
                         }],  # 负责人
            "members": [
                {
                    "canReadAll": False,
                    "user": members[0]
                 },
                {
                    "canReadAll": False,
                    "user": members[1]
                }
                    ],  # 参与人
            "customerId": customerId,  # 关联客户ID
            "customerName": customerName,  # 关联客户名称
            "projectTempId": project_temp_id,  # 关联模板ID
            "projectTempName": "销售人员招聘"
        }
        result = self.pro.create_project(requestdata)
        self.assertEqual(result.status_code, 200, msg=result.status_code)
        self.assertTrue("id" in result.json())
        response_data = result.json()
        self.assertEqual(requestdata["title"], response_data["title"], msg=response_data["title"])
        self.assertEqual(requestdata["content"], response_data["content"], msg=response_data["content"])

    # 添加一级目录
    def test_add_node(self):
        """新建一级目录"""
        request_data = {
            "isUpImage": False,                                 # 是否上传附件
            "userIds": [self.user_id],                           # 可见用户Id
            "nodeType": 1,                                       # 节点类型 1 为目录  2 其他
            "hasChild": False,                                  # 是否具有子节点
            "memo": "阿尔意图",                                  # 目录说明
            "nodeName": "一级目录" + str(random.randint(1, 100)),
            "order": 0,                                          # 排序（目前前端传的都是0，后端没读取前端传的值）
            "level": 0,                                          # 节点层级，1为根节点（目前前端传的都是0，后端没读取前端传的值）
            "attachment": [],                                    # 附件对象
            "projectId": self.project_id,
            "bizType": 0,                                        # 业务Id
            "createdAt": 0
        }
        result = self.pro.create_node(self.project_id, request_data)
        # 判断返回状态信息
        self.assertEqual(result.status_code, 200, msg=result.status_code)   # 判断新建客户状态码
        resp_json = result.json()
        self.assertEqual(resp_json["errcode"], 0, msg=resp_json["errcode"])
        self.assertEqual(resp_json["errmsg"], "success", msg=resp_json["errmsg"])
        data = resp_json["data"]
        # 判断body内容
        self.assertEqual(data["nodeType"], request_data["nodeType"], msg=data["nodeType"])      # 判断节点类型是否正确，1为目录
        self.assertEqual(data["level"], 1, msg=data["level"])                                   # 判断节点是否为一级目录
        self.assertEqual(data["nodeName"], request_data["nodeName"], msg=data["nodeName"])      # 判断目录名称是否与提交数据一致
        self.assertEqual(data["memo"], request_data["memo"], msg=data["memo"])                  # 判断目录说明是否与提交数据一致
        self.assertEqual(data["projectId"], request_data["projectId"], msg=data["projectId"])   # 判断项目Id是否与提交数据一致
        self.assertEqual(data["userIds"], request_data["userIds"], msg=data["userIds"])         # 判断可见人是否与提交数据一致
        self.assertEqual(data["creatorId"], self.user_id, msg=data["creatorId"])                # 判断目录创建人是否是登录人

    # 添加子目录
    def test_add_child_node(self):
        """新建2级子目录"""
        try:
            resp_json = self.pro.project_detail(self.project_id).json()
            node_id = resp_json["projectNodes"][0]["id"]
        except Exception as e:
            print("获取一级目录节点id失败",e)
        request_data = {
            "isUpImage": False,                                 # 是否上传附件
            "nodeType": 1,                                       # 节点类型 1 为目录  2 其他
            "hasChild": False,                                  # 是否具有子节点
            "memo": "二级子目录描述啦啦啦",                      # 目录说明
            "nodeName": "二级子目录" + str(random.randint(101, 200)),
            "order": 0,                                          # 排序（目前前端传的都是0，后端没读取前端传的值）
            "level": 0,                                          # 节点层级，1为根节点（目前前端传的都是0，后端没读取前端传的值）
            "attachment": [],                                    # 附件对象
            "projectId": self.project_id,
            "bizType": 0,                                        # 业务Id
            "createdAt": 0,
            "parentId": node_id
        }
        result = self.pro.create_node(self.project_id, request_data)
        # 判断返回状态信息
        self.assertEqual(result.status_code, 200, msg=result.status_code)   # 判断新建客户状态码
        resp_json = result.json()
        self.assertEqual(resp_json["errcode"], 0, msg=resp_json["errcode"])
        self.assertEqual(resp_json["errmsg"], "success", msg=resp_json["errmsg"])
        data = resp_json["data"]
        # 判断body内容
        self.assertEqual(data["nodeType"], request_data["nodeType"], msg=data["nodeType"])      # 判断节点类型是否正确，1为目录
        self.assertEqual(data["level"], 2, msg=data["level"])                                   # 判断节点是否为2级目录
        self.assertEqual(data["nodeName"], request_data["nodeName"], msg=data["nodeName"])      # 判断目录名称是否与提交数据一致
        self.assertEqual(data["memo"], request_data["memo"], msg=data["memo"])                  # 判断目录说明是否与提交数据一致
        self.assertEqual(data["projectId"], request_data["projectId"], msg=data["projectId"])   # 判断项目Id是否与提交数据一致
        self.assertEqual(data["creatorId"], self.user_id, msg=data["creatorId"])                # 判断目录创建人是否是登录人
        self.assertEqual(data["parentId"], request_data["parentId"], msg=data["parentId"])      # 判断父目录节点Id与提交节点一致

    # 团队项目列表
    def test_team_list(self):
        """团队项目列表：默认数据"""
        result = self.pro.team_list(self.param)
        # 判断请求状态
        self.assertEqual(result.status_code, 200, msg=result.status_code)
        resp_json = result.json()
        self.assertEqual(resp_json["errcode"], 0, msg=resp_json["errcode"])
        self.assertEqual(resp_json["errmsg"], "success", msg=resp_json["errmsg"])
        # 判断body内容
        data = resp_json["data"]
        total_records = data["totalRecords"]
        records = data["records"]
        actual_total = len(records)
        if total_records > self.param["pageSize"]:
            page = math.ceil(total_records / self.param["pageSize"])
            # 判断翻页数据请求状态
            for p in range(2, page+1):
                self.param["pageIndex"] = p
                page_result = self.pro.team_list(self.param)
                self.assertEqual(page_result.status_code, 200, msg=page_result.status_code)  # 判断翻页获取数据是否正确
                page_json = page_result.json()
                self.assertEqual(page_json["errcode"], 0, msg=page_json["errcode"])  # 判断翻页错误码是否为0
                self.assertEqual(page_json["errmsg"], "success", msg=page_json["errmsg"])
                page_records = page_json["data"]["records"]
                actual_total += len(page_records)
            # 判断records总量是否与totalRecords相同
        self.assertEqual(total_records, actual_total, msg=actual_total)  # 判断实际数据数量是否与返回的数据总数相同
        print("test team project list actual number:", actual_total)

    # 新建任务、报告、审批归属项目接口
    def test_project_query(self):
        """新建任务、报告、审批添加归档项目接口"""
        self.param["status"] = 1
        result = self.pro.get_query(self.param)
        self.assertEqual(result.status_code, 200, msg=result.text)
        resp_json = result.json()
        total_records = resp_json["totalRecords"]
        records = resp_json["records"]
        if total_records == 0:
            self.assertTrue(records is None)
        else:
            actual_total = len(records)
            if total_records > self.param["pageSize"]:
                page = math.ceil(total_records / self.param["pageSize"])
                # 判断翻页数据请求状态
                for p in range(2, page + 1):
                    self.param["pageIndex"] = p
                    page_result = self.pro.get_query(self.param)
                    self.assertEqual(page_result.status_code, 200, msg=page_result.status_code)  # 判断翻页获取数据是否正确
                    page_json = page_result.json()
                    page_records = page_json["records"]
                    actual_total += len(page_records)
                    # 判断返回的项目状态是否为进行中状态--归属项目只能选择进行中的项目
                    for pr in page_records:
                        self.assertEqual(pr["status"], self.param["status"], msg=pr["title"])
                print(actual_total)
            # 判断records总量是否与totalRecords相同
            self.assertEqual(total_records, actual_total, msg=actual_total)  # 判断实际数据数量是否与返回的数据总数相同
            print("test query project list actual number:", actual_total)

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        print("项目管理：end")

if __name__ == "__main__":
    unittest.main()
