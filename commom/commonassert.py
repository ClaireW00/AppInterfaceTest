import unittest
import math
import readConfig


class CommonTest(unittest.TestCase):
    def assertStatus(self, result, port="new"):
        if port == "old":       # 老接口不需要判断errcode
            self.assertEqual(result.status_code, 200, msg=result.text)
            return
        result_json = result.json()
        self.assertEqual(result_json["errcode"], 0, msg=result.text)
        self.assertEqual(result_json["errmsg"], "success", msg=result.text)

    def is_contain(self, arr, field):  # 判断人员是否属于一个数组,arr数组，每个值为dict,field为判断字段的key
        self.user_id = readConfig.ReadConfig().getUserValue("userid")
        for member in arr:
            if member[field] == self.user_id:
                return True
        return False

    def get_data(self, result, port="new"):
        self.user_id = readConfig.ReadConfig().getUserValue("userid")
        if port == "old":  # 老接口没有errcode
            self.assertStatus(result, "old")
            data = result.json()
        else:
            self.assertStatus(result)
            data = result.json()["data"]
        return data

    # 接口列表统一处理，老接口没有errcode
    def listProcess(self, param, func, biz_type, port="new"):
        result = func(param)
        self.assertStatus(result)
        data = self.get_data(result)    # 根据新旧接口获取data
        total_records = data["totalRecords"]
        records = data["records"]
        actual_total = 0
        if total_records == 0:
            self.assertEqual(actual_total, 0, msg=result.text)
            return
        first_at = records[0][param["field"]]
        page = math.ceil(total_records / param["pageSize"])
        for p in range(1, page + 1):
            param["pageIndex"] = p
            result = func(param)
            self.assertStatus(result)   # 断言状态和errcode
            data = self.get_data(result)    # 根据新旧接口获取data
            records = data["records"]
            actual_total += len(records)
            for record in records:
                if param["orderBy"] == "desc":
                    self.assertTrue(first_at >= record[param["field"]], msg=record)  # 断言倒叙排序正确
                elif param["orderBy"] == "asc":
                    self.assertTrue(first_at <= record[param["field"]], msg=record)  # 断言顺序排序正确
                first_at = record[param["field"]]
                if biz_type == "event_list":     # 我执行的时间
                    executors = record["executors"]
                    # 断言事件执行者中包含登录人
                    self.assertTrue(self.is_contain(executors, "executorId"), msg=record["flowEventId"])
                if biz_type == "init_list":
                    self.assertEqual(record["initiatorId"], self.user_id)   # 发起人为登陆人
                if param["status"] != 0:
                    self.assertEqual(record["status"], param["status"], msg=record)
                # 按时间段查询
                if param["qType"] == 1:
                    key = "startdAt"
                if param["qType"] == 2:
                    key = "finishedAt"
                if "startAt" and "endAt" in param:  # 开始时间和结束时间均有
                    self.assertTrue(param["startAt"] <= record[key] <= param["endAt"], msg=record)
                elif "startAt" in param and "endAt" not in param:   # 只有开始时间，没有结束时间，大于startAt
                    self.assertTrue(param["startAt"] <= record[key], msg=record)
                elif "startAt" not in param and "endAt" in param:   # 没有开始时间，只有结束时间，小于结束时间
                    self.assertTrue(record[key] <= param["endAt"], msg=record)

        self.assertEqual(total_records, actual_total)       # 判断返回的数据数量与实际数据量相同
        # print(actual_total, first_at)
