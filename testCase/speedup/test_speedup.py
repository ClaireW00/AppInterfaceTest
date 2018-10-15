import unittest
from testCase.speedup import speedup
from commom import commonassert
from commom import get_Time_Type
from commom import attachments
from testCase.customer import customerManger
from testCase.order import order
import time


class SpeedupCase(commonassert.CommonTest):

    @classmethod
    def setUpClass(cls):
        print("快点：start")
        cls.speed = speedup.SpeedUp()

    def setUp(self):    # 每条用例执行完初始化param
        self.param = {
            "field": "startAt",  # 排序字段
            "orderBy": "desc",
            "pageIndex": 1,
            "pageSize": 20,
            "status": 0,  # 事件状态，0全部，1执行中,2已完成；流程状态1:待分派 2:进行中 3:待确认完成 4:已完成 5:意外终止
            "qType": 0,  # 查询时间类型，0全部时间，1开始时间，2完成时间
            "source": 0,  # 0全部，1规则流程，2售后流程
            "isAll": False,  # 是否全部，True全部事件|流程列表，False获取我执行的|我组织的列表
            "isOverTime": 0  # 是否逾期，0全部，1已逾期，2未逾期
        }

    # 我执行的列表全部数据，按开始时间倒叙排序
    def test_eventList_001(self):
        """我执行的：全部数据按开始时间倒叙排序"""
        self.listProcess(self.param, self.speed.event_list, "event_list")

    # 我执行的：执行中数据按开始时间顺序排序"
    def test_eventList_002(self):
        """我执行的：执行中数据按开始时间顺序排序"""
        self.param["status"] = 1
        self.param["orderBy"] = "asc"
        self.listProcess(self.param, self.speed.event_list, "event_list")

    # 我执行的：最近30天已完成数据按完成时间倒叙
    def test_eventList_003(self):
        """我执行的：最近30天已完成数据按完成时间倒叙"""
        self.param["status"] = 2
        self.param["field"] = "finishedAt"    # 按完成时间倒叙
        self.param["orderBy"] = "desc"
        self.param["qType"] = 2             # 按完成时间、最近30天查询
        self.param["startAt"], self.param["endAt"] = get_Time_Type.getTimeRegionByType("TheLast30Day")
        self.listProcess(self.param, self.speed.event_list, "event_list")

    # 我组织的（后端没有返回流程组织者）
    def test_flowList_001(self):
        """我组织的：进行中按开始时间倒序"""
        self.param["startType"] = 0      # 触发方式 0:all 1:智能触发 2:手动新建
        self.param["status"] = 2         # 进行中
        self.param["source"] = 2         # 售后流程
        self.listProcess(self.param, self.speed.flow_list, "flow_list")     # 后端没返回组织者，所以未判断组织者

    # 流程事件节点列表
    def test_flowEvent(self):
        """我组织的流程事件"""
        self.param["startType"] = 0  # 触发方式 0:all 1:智能触发 2:手动新建
        self.param["source"] = 2  # 售后流程
        flow = self.speed.flow_list(self.param).json()["data"]["records"][0]    # 获取一个我组织的流程
        result = self.speed.flow_event(flow["id"])
        self.assertStatus(result)
        data = result.json()["data"]
        self.assertEqual(data["id"], flow["id"], msg=data)     # 断言流程id与查询的id相同
        self.assertEqual(data["flowTitle"], flow["flowTitle"], msg=data)    # 判断列表与详情返回的标题和关联客户一致
        self.assertEqual(data["customerName"], flow["customerName"], msg=data)
        self.assertTrue(self.is_contain(data["organizers"], "organizerId"), msg=data)   # 断言登录人是组织者

    # 我发起的
    def test_initList_001(self):
        """我发起的：按完成时间倒叙"""
        self.param["source"] = 2  # 售后流程
        self.param["field"] = "finishedAt"
        self.param["orderBy"] = "desc"
        self.listProcess(self.param, self.speed.init_list, "init_list")     # 断言发起人是登录人和排序

    # 获取售后流程类型
    def test_launchConcise(self):
        """获取售后流程类型"""
        result = self.speed.launch_concise()
        self.assertStatus(result)

    # 手动发起关联客户流程
    def test_initFlow_001(self):
        """手动发起关联客户流程"""
        customer_id = customerManger.CustomerManger().get_similar_customer()["id"]
        data = {
            "flowTitle": "关联客户流程" + time.strftime("%Y-%m-%d %H:%M", time.localtime(time.time())),
            "cusServiceId": self.speed.get_concise_id(),
            "customerId": customer_id
        }
        result = self.speed.init_flow(data)
        self.assertStatus(result)
        flow = result.json()["data"]
        self.assertEqual(data["flowTitle"], flow["flowTitle"], msg=data)
        self.assertEqual(data["cusServiceId"], flow["flowId"], msg=data)
        self.assertEqual(data["customerId"], flow["customerId"], msg=data)

    # 手动发起关联订单售后流程
    def test_initFlow_002(self):
        """手动发起关联订单流程"""
        params = {
            "filed": "createdAt",
            "orderBy": "desc",
            "pageSize": 20,
            "pageIndex": 1,
            "status": 0  # 0全部状态  1待审核   7审批中  2未通过  3进行中  4已完成  5意外终止
        }
        order_id = order.Order().get_order(params)["id"]
        data = {
            "flowTitle": "关联订单流程" + time.strftime("%Y-%m-%d %H:%M", time.localtime(time.time())),
            "cusServiceId": self.speed.get_concise_id(),
            "orderId": order_id
        }
        result = self.speed.init_flow(data)
        self.assertStatus(result)
        flow = result.json()["data"]
        self.assertEqual(data["flowTitle"], flow["flowTitle"], msg=data)
        self.assertEqual(data["cusServiceId"], flow["flowId"], msg=data)
        self.assertEqual(data["orderId"], flow["orderId"], msg=data)

    # 更改流程名称
    def test_title(self):
        """更改流程名称"""
        flow_id = self.speed.get_flow()["id"]
        data = {
            "title": "更改过名称的流程" + time.strftime("%Y-%m-%d %H:%M", time.localtime(time.time()))
        }
        result = self.speed.title(flow_id, data)
        self.assertStatus(result)
        flow = self.speed.flow_event(flow_id).json()["data"]       # 修改后获取流程信息
        self.assertEqual(data["title"], flow["flowTitle"])         # 断言修改后流程名称是否正确

    # 提交流程说明
    def test_remark(self):
        """提交流程说明"""
        flow_id = self.speed.get_flow()["id"]
        data = {
            "remark": "添加流程说明" + time.strftime("%Y-%m-%d", time.localtime(time.time())),     # 流程说明
            "uuid": attachments.attachments("0")["UUId"]
        }
        result = self.speed.remark(flow_id, data)
        self.assertStatus(result)
        data_response = result.json()["data"]
        self.assertEqual(data["remark"], data_response["remark"], msg=data_response)
        self.assertEqual(1, len(data_response["attachments"]), msg=data_response)   # 断言附件数量与上传一致


    @classmethod
    def tearDownClass(cls):
        print("快点：end")

if __name__ == "__main__":
    unittest.main()



