from commom import commonassert
from testCase.task import task


class TaskCase(commonassert.CommonTest):
    @classmethod
    def setUpClass(cls):
        cls.task_ins = task.Task()
        cls.param = {
            "startAt": None,
            "endAt": None,
            "filed": "createdAt",
            "pageIndex": 1,
            "pageSize": 20,
            "sort": "desc",
            "joinType": 0,  # 1我分派的、2我负责的、3我参与的
            "status": 0
        }

    # 我的任务列表
    def test_myTask_001(self):
        """我的任务列表"""
        result = self.task_ins.my_task(self.param)
        self.assertStatus(result, "old")

    # 我负责的任务
    def test_myTask_002(self):
        """筛选我负责的任务"""
        self.param["joinType"] = 2
        self.param["pageIndex"] = 1
        result = self.task_ins.my_task(self.param)
        self.assertStatus(result, "old")
