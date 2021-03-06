import unittest,time
from email.mime.text import MIMEText
import smtplib
from email.utils import parseaddr, formataddr
from email.header import Header
from email.mime.multipart import MIMEMultipart



class TimeTest(object):
    a = 1
    def __init__(self, hour, minute, second):
        self.hour = hour
        self.minute = minute
        self.second = second

    @staticmethod
    def showTime():
        print("000")
        return time.strftime("%H:%M:%S", time.localtime())
    @classmethod
    def add(cls, hour, minute, se):
        t1 = cls(hour=hour, minute=minute, second=se)
        return t1
    def jian(self):
        print("222")
'''
t = TimeTest(1, 2, 3)
L = TimeTest.add(1,3,3)
print(type(L))
print(datetime(datetime.now().year-20,datetime.now().month, datetime.now().day) - timedelta(days=8))
print(int(datetime.now().timestamp()))
'''

def a(x):
    return x*x

def b(y, fuc):
    return y+fuc(y)

n = 3
# print(b(n,a))


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, "utf-8").encode(), addr))

if __name__ == "__main__":
    from_addr = "320855089@qq.com"
    password = "cryfivtjpoukbjfc"
    to_addr = ["895457129@qq.com", "1271782085@qq.com"]
    smtp_server = "smtp.qq.com"

    msg = MIMEMultipart()
    msg["From"] = _format_addr("your baby<%s>" % from_addr)     # 设置发件人名
    msg["To"] = _format_addr("my pig<%s>" % to_addr)            # 设置收件人名
    msg["Subject"] = Header("我的接口测试报告", "utf-8").encode()   # 设置邮件标题
    msg.attach(MIMEText("my report:please look at attach", "plain", "utf-8"))   # 邮件内容
    # 邮件附件
    att = MIMEText(open("C:\\Users\\Administrator\\AppInterfaceTest\\result.html", "rb") .read(), "base64", "gb2312")
    att["Content-Type"] = "application/octet-stream"
    att["Content-Disposition"] = 'attachment; filename="result.html"'
    msg.attach(att)
    server = smtplib.SMTP(smtp_server, 25)
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, to_addr, msg.as_string())
    server.quit()

