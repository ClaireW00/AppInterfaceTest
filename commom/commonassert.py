import unittest


class CommonTest(unittest.TestCase):

    def assertStatus(self, result):
        self.assertEqual(result.status_code, 200, msg=result.text)

    def assertErrcode(self, result):
        self.assertStatus(result)
        result_json = result.json()
        self.assertEqual(result_json["errcode"], 0, msg=result.text)
        self.assertEqual(result_json["errmsg"], "success", msg=result.text)

    # 老接口列表处理，老接口没有errcode
    def old_listProcess(self, result, param):
        self.assertStatus(result)
        result_json = result.json()
        total_records = result_json["totalRecords"]
        records = result_json["records"]        # list
        actual_total = len(records)
        if total_records == 0:
            self.assertEqual(actual_total, total_records, msg=result.text)
            return
        firstAt = records[0][param["filed"]]        # 第一条数据要排序字段的值
        return firstAt


    # 新接口列表处理，新接口有errcode
    def new_listProcess(self, result):
        pass
