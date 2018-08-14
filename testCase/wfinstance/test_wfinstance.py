import unittest
from testCase.wfinstance import wfinstance
from testCase.customer import customerManger
from testCase.user import user


class WfInstanceCase(unittest.TestCase):

    # wfI用例执行前初始化参数
    @classmethod
    def setUpClass(cls):
        print("审批流程：start")
        cls.wfin = wfinstance.Wfinstance()
        cls.param = {
            "pageSize": 20
        }
        cls.cus = customerManger.CustomerManger()  # 定义一个客户对象
        cls.us = user.User()

    # 每条用例执行前初始化参数param
    def setUp(self):
        self.param = {
            "pageSize": 20
        }

    # 获取审批类别
    def test_get_wfbizform(self):
        """获取审批类别接口"""
        self.param["pageSize"] = 1000
        result = self.wfin.get_wfbizform(self.param)
        self.assertEqual(result.status_code, 200, msg=result.status_code)
        resp_json = result.json()
        # 判断响应内容
        self.assertTrue("totalRecords" in resp_json)
        self.assertTrue("records" in resp_json)
        total_records = resp_json["totalRecords"]
        records = resp_json["records"]
        self.assertTrue(len(records) >= 6)           # 请假、出差、订单、回款、赢单、意外终止6个审批为系统审批
        self.assertTrue(total_records == len(records))

    # 测试获取审批流程，目前只能判断请求状态，无法判断内容是否正确
    def test_get_wftemplate(self):
        """获取审批流程接口"""
        self.param["pageSize"] = 1000
        bizform_id = self.wfin.get_wfbizform_meg(self.param, "请假")["id"]        # 获取请假审批的id
        result = self.wfin.get_wftemplate(bizform_id)                   # 根据审批类别ID获取流程
        self.assertEqual(result.status_code, 200, msg=result.status_code)

    # 新建审批
    def test_create_wfinstance(self):
        """新建请假审批"""
        self.param["pageSize"] = 1000
        try:
            bizform_id = self.wfin.get_wfbizform_meg(self.param, "请假")["id"]     # 获取请假审批的id
            # 获取相关联的客户信息
            custom = self.cus.get_similar_customer()
            # 获取登录人所属部门deptId
            dept_id = self.us.get_UserProfile().json()["data"]["depts"][0]["shortDept"]["id"]
            # 获取审批流程的Id
            wftpt_id = self.wfin.get_wftemplate(bizform_id).json()[0]["id"]
            # 获取项目id

        except Exception as e:
            print("请求审批相关信息失败", e)
        requestdata = {
            "title": "布莱尔提交三天以内请假流程审批",
            "customerId": custom["id"],
            "customerName": custom["name"],
            "bizformId": bizform_id,                        # 审批类别ID，如请假、出差。。。
            "bizExtData": {                               # 扩展数据，附件个数，讨论个数
                "attachmentCount": 1
            },
            "deptId": dept_id,
            "memo": "备注信息测试003",
            "wftemplateId": wftpt_id,     # 审批流程ID
            "workflowValues": [{                            # 审批内容
                "57d901c7d33c6511f4001573": "2018-03-28 11:49",
                "5a4e1b1462dfca12f56f84e3": "www.baidu.com",
                "57d6333dd33c653e3e0046bc": "2018-03-28 11:48",
                "57d6333dd33c653e3e0046bd": "2018-03-29 11:49",
                "57d6333dd33c653e3e0046be": 2,
                "59e5f7a716e93ca85907fa65": 0,
                "5937a63c19b8203d75c574e7": "12",
                "57d6333dd33c653e3e0046bf": "测试请假",
                "59e5f7a716e93ca85907fa66": 0,
                "5937a62b19b8203d75c574d1": "测试",
                "59e05d0a19b8204faaa62f6e": "32"
            }],
            "projectId": "5ab1b8dd62dfca240bb8209f",
            "attachmentUUId": "57F2B5CE-1EEC-41B4-B8F6-DD539CDDD089",
            "bizCode": 100
        }
        result = self.wfin.create_wfinstance(requestdata)
        self.assertEqual(result.status_code, 200, msg=result.status_code)

    @classmethod
    def tearDownClass(cls):
        print("审批流程：end")

if __name__ == "__main__":
    unittest.main()
