from lxml import etree
import requests, unittest
import re
import readConfig
from commom import excel_rd
import ddt
from commom import commonassert
import HTMLTestRunner

testData = excel_rd.read_excel_table_byindex("C:\\Users\\Administrator\\AppInterfaceTest\\testData\\loginData.xlsx")


@ddt.ddt
class Login(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
       print('登录测试：start')

    def App_login(self, username, pwd):
        f = readConfig.ReadConfig()
        baseurl = f.getHttpValue('app_userbaseurl')
        host = f.getHttpValue('app_userhost')
        url = baseurl+'/oapi/auth'
        # 配置请求头
        head = f.get_header()
        head["Host"] = host
        data = {
                "username": username,
                "password": pwd
        }
        result = requests.post(url, json=data, headers=head)
        return result

    @ddt.data(*testData)
    def test_login(self, data):

        result = self.App_login(data["userName"], data["password"])
        self.assertEqual(result.status_code, int(data["status"]))        # 断言请求状态
        response_data = result.json()
        self.assertEqual(response_data[data["field"]], data["assert"])  # 断言响应内容

    # 测试正确的密码，正确的账号
    def etest_AppLogin(self):
        """测试APP登录:正确的用户名，正确的密码"""
        f = readConfig.ReadConfig()
        username = f.getUserValue('username')
        password = f.getUserValue('password')
        result = self.App_login(username, password)
        self.assertEqual(result.status_code, 200)  # 测试状态码正确
        if result.status_code == 200:
            self.assertIn("access_token", result.text)  # 测试返回值有token
            json_response = result.json()
            self.assertTrue(json_response["access_token"] is not None, msg='正确的密码没有登录成功')  # 测试token不能为空

            # 测试正确的账号，错误的密码

    def etest_login_errorpwd(self):
        """测试APP登录接口：正确的用户名，错误的密码"""
        result = self.App_login('16512345671', '856985')
        self.assertNotEqual(result.status_code, 200, msg='密码错误时，仍然登录成功了')
        if result.status_code != 200:
            json_response = result.json()
            if "error" in json_response:
                self.assertEqual('手机号码或密码错误', json_response["error"], msg='返回错误信息错误')  # 断言返回的错误信息正确
            else:
                self.assertTrue(False)
                # self.assertIsNone(Authorization)

                # 测试不存在的账号

    def etest_login_errorUsername(self):
        """测试APP登录接口：不存在的用户名"""
        result = self.App_login('1651234567', '123456')
        self.assertNotEqual(result.status_code, 200, msg='密码错误时，仍然登录成功了')
        if result.status_code != 200:
            json_response = result.json()
            if "error" in json_response:
                self.assertEqual('该用户不存在!', json_response["error"], msg='返回错误信息错误')  # 断言返回的错误信息正确
                # self.assertIsNone(Authorization)
    @classmethod
    def tearDownClass(cls):
        print('登录测试：end')

if __name__ == '__main__':

    file = "C:\\Users\\Administrator\\AppInterfaceTest\\testCase\\login"
    testcase = unittest.TestSuite()
    discover = unittest.defaultTestLoader.discover(file, "test*.py", top_level_dir=None)
    for suite in discover:
        for case in suite:
            testcase.addTest(case)
    report = "C:\\Users\\Administrator\\AppInterfaceTest\\testData\\login.html"
    fp = open(report, "wb")
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title="登录测试", description="登录接口测试")
    run = runner.run(testcase)
    fp.close()
