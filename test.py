import unittest,time
from datetime import datetime,timedelta

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
    def add(cls,hour,minute, se):
        t1= cls(hour=hour,minute=minute,second=se)
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

n=3
print(b(n,a))


