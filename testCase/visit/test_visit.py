import unittest,random,math
from commom import get_Time_Type
from testCase.visit import visit

class VisitCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("拜访签到测试：start")

    def test_createVisit(self):
        """新建拜访：填写所有字段"""
        data = {
            "atUserIds": ["58a6c8c3e44c363e73000006"],
            "position": "四川省成都市金牛区北站西二巷36号成都金牛万达广场-甲级写字楼附近",
            "contactName": "姓名0520-0039",
            "isCusPosition": False,
            "gpsInfo": "104.0737581,30.6893964",
            "memo": "我拜访了公司名称0520-0040" + str(random.randint(1, 300)),
            "attachmentUUId": "AED29C50-0CD8-4B3E-ABF2-58B1E13BCD20",
            "contactTpl": "13512345671",
            "customerId": "591f20a7e44c36080269f8b2",
            "audioInfo": [{
                "length": 3,
                "fileName": "114F2732-DC35-4591-A103-1829D6C9BC39\/15159865588246.wav"
            }],
            "contactRoleId": "58a593d97c5f1d7ab3465e8c"
        }
        v=visit.Visit()
        result=v.createVisit(data)
        self.assertEqual(result.status_code,200,msg='返回状态码错误')
        if result.status_code==200:
            result_json=result.json()
            visit_response=result_json['data']
            self.assertEqual(data["contactName"],visit_response["contactName"],msg='客户名称与所填写不一致')   # 检查客户名称、拜访内容、定位信息是否与所填写信息一致
            self.assertEqual(data["memo"], visit_response["content"],msg='拜访内容与所填写不一致')
            self.assertEqual(data["position"], visit_response["position"],msg='定位与所填写不一致')
            self.assertEqual(data["contactRoleId"], visit_response["contactRoleId"], msg='联系人角色与所填写不一致')

    def test_VisitList(self):
        '''拜访签到列表默认展示数据:最近30天,创建时间倒叙'''
        param={
        "customerType":0,   #0全部，1开发客户，2签约客户
        "filterType " :0,
        "pageIndex	":1,
        "pageSize":10,
        "timeType":17,     #表示最近30天
        "userId":'',
        "xpath":""
    }
        v=visit.Visit()
        result=v.visitList(param)
        self.assertEqual(result.status_code,200)
        data=result.json()["data"]
        totalRecords=data["totalRecords"]
        records=data["records"]    #list
        if totalRecords > param["pageSize"]:
            page = math.ceil(totalRecords / param["pageSize"])
            for p in range(2, page + 1):
                param["pageIndex"] = p
                pageResult = v.visitList(param)
                self.assertEqual(pageResult.status_code, 200, msg='翻页错误')
                json = pageResult.json()
                self.assertEqual(json["errmsg"], "success", msg='翻页错误')
                pagedata = json["data"]["records"]
                records.extend(pagedata)
        print("最近30天拜访数量", len(records))
        self.assertEqual(totalRecords,len(records),msg='返回数据实际数量与总数不同') #判断返回的总数是否与实际数量相同
        startAt,endAt=get_Time_Type.getTimeRegionByType("TheLast30Day")  #获取最近30天的时间戳
        if totalRecords>0:
            firstAt=records[0]["createdAt"]
        for vi in records:
            self.assertTrue(startAt<=vi["createdAt"]and vi["createdAt"]<=endAt)   #判断第一页返回的数据属于最近30天新建的
            self.assertTrue(firstAt>=vi["createdAt"])    #判断列表按创建时间倒叙排序
            firstAt = vi["createdAt"]

    def test_VisitList_Today(self):
        '''拜访签到列表按时间筛选数据:今天，创建时间倒叙'''
        param={
        "customerType":0,
        "filterType " :0,
        "pageIndex	":1,
        "pageSize":10,
        "timeType":1,   #表示今天
        "userId":'',
        "xpath":""
    }
        v=visit.Visit()
        result=v.visitList(param)
        self.assertEqual(result.status_code,200)
        data=result.json()["data"]
        totalRecords=data["totalRecords"]
        records = data["records"]  # list
        if totalRecords > param["pageSize"]:
            page = math.ceil(totalRecords / param["pageSize"])
            for p in range(2, page + 1):
                param["pageIndex"] = p
                pageResult = v.visitList(param)
                self.assertEqual(pageResult.status_code, 200, msg='翻页错误')
                json = pageResult.json()
                self.assertEqual(json["errmsg"], "success", msg='翻页错误')
                pagedata = json["data"]["records"]
                records.extend(pagedata)
        print("今天拜访数量", len(records))
        self.assertEqual(totalRecords, len(records), msg='返回数据实际数量与总数不同')  # 判断返回的总数是否与实际数量相同
        startAt,endAt=get_Time_Type.getTimeRegionByType("Today")  #获取最近今天的时间戳
        if totalRecords>0:
            firstAt=records[0]["createdAt"]
        for vi in records:
            self.assertTrue(startAt<=vi["createdAt"]and vi["createdAt"]<=endAt)   #判断第一页返回的数据属于今天天新建的
            self.assertTrue(firstAt >= vi["createdAt"])  # 判断列表按创建时间倒叙排序
            firstAt = vi["createdAt"]

    def test_VisitList_user(self):
        '''拜访签到列表按人员筛选数据:时间不限，人员：陈老师'''
        param={
        "customerType":0,
        "filterType " :0,
        "pageIndex	":1,
        "pageSize":10,
        "timeType":None,#所有数据
        "userId":'58a6c8c3e44c363e73000006',
        "xpath":""
    }
        v=visit.Visit()
        result=v.visitList(param)
        self.assertEqual(result.status_code,200)
        data=result.json()["data"]
        totalRecords=data["totalRecords"]
        records = data["records"]  # list
        if totalRecords > param["pageSize"]:
            page = math.ceil(totalRecords / param["pageSize"])
            for p in range(2, page + 1):
                param["pageIndex"] = p
                pageResult = v.visitList(param)
                self.assertEqual(pageResult.status_code, 200, msg='翻页错误')
                json = pageResult.json()
                self.assertEqual(json["errmsg"], "success", msg='翻页错误')
                pagedata = json["data"]["records"]
                records.extend(pagedata)
        print("按人员查询实际拜访数量", len(records))
        self.assertEqual(totalRecords, len(records), msg='返回数据实际数量与总数不同')  # 判断返回的总数是否与实际数量相同
        if totalRecords>0:
            firstAt=records[0]["createdAt"]
        for vi in records:
            self.assertEqual(vi["creator"]["id"],param["userId"])
            self.assertTrue(firstAt >= vi["createdAt"])  # 判断列表按创建时间倒叙排序
            firstAt = vi["createdAt"]

    def test_VisitList_customerType(self):
        '''拜访签到列表按客户类型筛选数据:客户类型：开发客户'''
        param={
        "customerType":1,
        "filterType " :0,
        "pageIndex	":1,
        "pageSize":10,
        "timeType":17,#所有数据
        "userId":'',
        "xpath":""
    }
        v=visit.Visit()
        result=v.visitList(param)
        self.assertEqual(result.status_code,200)
        data=result.json()["data"]
        totalRecords=data["totalRecords"]
        records = data["records"]  # list
        if totalRecords > param["pageSize"]:
            page = math.ceil(totalRecords / param["pageSize"])
            for p in range(2, page + 1):
                param["pageIndex"] = p
                pageResult = v.visitList(param)
                self.assertEqual(pageResult.status_code, 200, msg='翻页错误')
                json = pageResult.json()
                self.assertEqual(json["errmsg"], "success", msg='翻页错误')
                pagedata = json["data"]["records"]
                records.extend(pagedata)
        print("开发客户最近30天拜访数量", len(records))
        self.assertEqual(totalRecords, len(records), msg='返回数据实际数量与总数不同')  # 判断返回的总数是否与实际数量相同
        print("开发客户拜访签到",records)
        if totalRecords>0:
            firstAt=records[0]["createdAt"]
        for vi in records:
            self.assertEqual(vi["customerType"],param["customerType"])
            self.assertTrue(firstAt >= vi["createdAt"])  # 判断列表按创建时间倒叙排序
            firstAt = vi["createdAt"]

    def test_CustormerNearme(self):
        '''测试获取拜访客户列表'''
        v = visit.Visit()
        result = v.get_CustormerNearme()
        self.assertEqual(result.status_code, 200)  #目前无法获取数据准确性，只能根据状态判断（后期需要再获取数据库数据对比）
        self.assertEqual(result.json()["errcode"], 0, msg='返回信息错误')
        self.assertEqual(result.json()["errmsg"], "success", msg='返回信息错误')
        data=result.json()["data"]
        print("拜访客户列表：",data)

    @classmethod
    def tearDownClass(cls):
        print('拜访签到测试：end')

    if __name__ == "__main__":
        unittest.main()



