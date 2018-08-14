import time
from datetime import datetime ,timedelta  #datetime是模块，模块中还有一个datetime类


# 返回开始时间和结束时间戳，默认返回今天
def getTimeRegionByType(timeType='Today'):
    nowTime = datetime.now()
    if timeType == 'Today':
        startAt = datetime(nowTime.year, nowTime.month, nowTime.day, 0, 0, 0).timestamp()   # 用指定日期创建时间,timestamp()将日期转为时间戳
        endAt = datetime(nowTime.year, nowTime.month, nowTime.day, 23, 59, 59).timestamp()
    elif timeType == 'Yestorday':
        timeInfor = timedelta(days=1)
        startAt = (datetime(nowTime.year, nowTime.month, nowTime.day, 0, 0, 0)-timeInfor).timestamp()
        endAt = (datetime(nowTime.year, nowTime.month, nowTime.day, 23, 59, 59)-timeInfor).timestamp()
    elif timeType == 'Tomorrow':
        timeInfor = timedelta(days=1)
        startAt = (datetime(nowTime.year, nowTime.month, nowTime.day, 0, 0, 0) + timeInfor).timestamp()
        endAt = (datetime(nowTime.year, nowTime.month, nowTime.day, 23, 59, 59) + timeInfor).timestamp()
    elif timeType == 'TheWeek':
        timeInfor1 = timedelta(days=nowTime.weekday())
        timeInfor2 = timedelta(days=6-nowTime.weekday())
        startAt = (datetime(nowTime.year, nowTime.month, nowTime.day, 0, 0, 0)-timeInfor1).timestamp()
        endAt = (datetime(nowTime.year, nowTime.month, nowTime.day, 23, 59, 59)+timeInfor2).timestamp()
    elif timeType == 'LastWeek':
        timeInfor1 = timedelta(days=nowTime.weekday()+7)
        timeInfor2 = timedelta(days=nowTime.weekday()+1)
        startAt = (datetime(nowTime.year, nowTime.month, nowTime.day, 0, 0, 0)-timeInfor1).timestamp()
        endAt = (datetime(nowTime.year, nowTime.month, nowTime.day, 23, 59, 59)-timeInfor2).timestamp()
    elif timeType == 'TheMonth':
        startAt = datetime(nowTime.year, nowTime.month, 1, 0, 0, 0).timestamp()
        if nowTime.month == 12:
            endAt = datetime(nowTime.year, 12, 31, 23, 59, 59).timestamp()
        else:
            endAt = (datetime(nowTime.year, nowTime.month+1, 1, 23, 59, 59)-timedelta(days=1)).timestamp()
    elif timeType == 'LastMonth':
        timeInfor = datetime(nowTime.year, nowTime.month, 1) - timedelta(days=1)
        endAt = (datetime(nowTime.year, nowTime.month, 1, 23, 59, 59) - timedelta(days=1)).timestamp()
        startAt = (datetime(timeInfor.year, timeInfor.month, 1, 0, 0, 0)).timestamp()
    elif timeType == 'TheLast30Day':
        timeInfor = timedelta(days=29)
        startAt = (datetime(nowTime.year, nowTime.month, nowTime.day, 0, 0, 0) - timeInfor).timestamp()
        endAt = datetime(nowTime.year, nowTime.month, nowTime.day, 23, 59, 59).timestamp()
    elif timeType == 'LastSevenDay':
        timeInfor = timedelta(days=6)
        startAt = (datetime(nowTime.year, nowTime.month, nowTime.day, 0, 0, 0) - timeInfor).timestamp()
        endAt = datetime(nowTime.year, nowTime.month, nowTime.day, 23, 59, 59).timestamp()

    return int(startAt), int(endAt)      # timestamp()时间戳是float，小数代表毫秒

if __name__ == '__main__':
    t0 = getTimeRegionByType('Today')
    t1 = getTimeRegionByType('Yestorday')
    t2 = getTimeRegionByType('Tomorrow')
    t3 = getTimeRegionByType('TheWeek')
    t4 = getTimeRegionByType('LastWeek')
    t5 = getTimeRegionByType('TheMonth')
    t6 = getTimeRegionByType('LastMonth')
    t7 = getTimeRegionByType('TheLast30Day')
    t8 = getTimeRegionByType('LastSevenDay')
    print(t0, t1, t2, t3, t4, t5, t6, t7, t8)

