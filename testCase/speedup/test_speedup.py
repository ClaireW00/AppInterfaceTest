import unittest
from testCase.speedup import speedup
from commom import commonassert
from commom import get_Time_Type


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

    @classmethod
    def tearDownClass(cls):
        print("快点：end")

if __name__ == "__main__":
    unittest.main()



