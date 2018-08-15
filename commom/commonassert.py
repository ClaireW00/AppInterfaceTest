import unittest


class CommonTest(unittest.TestCase):

    def assertStatus(self, result):
        self.assertEqual(result.status_code, 200, msg=result.text)

    def assertErrcode(self, result):
        self.assertStatus(result)
        result_json = result.json()
        self.assertEqual(result_json["errcode"], 0, msg=result.text)
        self.assertEqual(result_json["errmsg"], "success", msg=result.text)
