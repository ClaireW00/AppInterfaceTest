# codingLutf-8
import unittest
import HTMLTestRunner
import readConfig
from testCase.login import test_login


def set_token():
    f = readConfig.ReadConfig()
    login = test_login.Login()
    username = f.getUserValue('username')
    pwd = f.getUserValue("password")
    result = login.App_login(username, pwd)
    if result.status_code == 200:
        access_data = result.json()['access_token']
        userid = result.json()['userId']
        authorization = 'Bearer ' + access_data
        f.set_UserId(userid)
        f.set_token(authorization)
        return authorization
    else:
        print('登陆失败！，后续用例不再执行')


def all_case():  # 待执行用例的目录

    case_dir = 'E:\\Python\\AppInterfaceTest\\testCase'
    testcase = unittest.TestSuite()
    discover = unittest.defaultTestLoader.discover(case_dir, pattern='test*.py', top_level_dir=None)    # 返回值是个二级数组

    for test_suite in discover:   # 将discover加载出来的数据循环加入到测试套件中
        for test_case in test_suite:
            testcase.addTests(test_case)

    return testcase


if __name__ == "__main__":
    token = set_token()
    '''
    if token is not None:     # 登录成功后执行测试用例
        report_path = 'C:\\Users\\Administrator\\AppInterfaceTest\\result.html'
        fp = open(report_path, 'wb')
        runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title='KuaiQi Test Report', description='测试用例执行明细')
        runner.run(all_case())
        fp.close()
    '''

