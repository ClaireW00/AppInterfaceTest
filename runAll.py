# codingLutf-8
import HTMLTestRunner
import smtplib
import unittest
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
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

    case_dir = 'C:\\Users\\Administrator\\AppInterfaceTest\\testCase'
    testcase = unittest.TestSuite()
    discover = unittest.defaultTestLoader.discover(case_dir, pattern='test*.py', top_level_dir=None)    # 返回值是个二级数组

    for test_suite in discover:   # 将discover加载出来的数据循环加入到测试套件中
        for test_case in test_suite:
            testcase.addTests(test_case)
    return testcase


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, "utf-8").encode(), addr))


def send_report(report_path):      # 发送报告到指定email
    from_addr = "320855089@qq.com"
    password = "cryfivtjpoukbjfc"
    to_addr = ["wll@ukuaiqi.com", "1271782085@qq.com"]
    smtp_server = "smtp.qq.com"

    msg = MIMEMultipart()
    msg["From"] = _format_addr("your baby<%s>" % from_addr)  # 设置发件人名
    msg["To"] = _format_addr("my pig<%s>" % to_addr)  # 设置收件人名
    msg["Subject"] = Header("我的接口测试报告", "utf-8").encode()  # 设置邮件标题
    msg.attach(MIMEText("my report:please look at attach", "plain", "utf-8"))  # 邮件内容
    # 邮件附件
    att = MIMEText(open(report_path, "rb").read(), "base64", "gb2312")
    att["Content-Type"] = "application/octet-stream"
    att["Content-Disposition"] = 'attachment; filename="result.html"'
    msg.attach(att)
    server = smtplib.SMTP(smtp_server, 25)      # email模块复制构建邮件，SMTP负责发送邮件
    server.login(from_addr, password)
    server.sendmail(from_addr, to_addr, msg.as_string())
    server.quit()


if __name__ == "__main__":
    token = set_token()
    if token is not None:     # 登录成功后执行测试用例
        report_path = 'C:\\Users\\Administrator\\AppInterfaceTest\\result.html'
        fp = open(report_path, 'wb')
        runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title='KuaiQi Test Report', description='测试用例执行明细')
        runner.run(all_case())
        fp.close()
        send_report(report_path)

