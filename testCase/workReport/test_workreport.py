'工作报告test'
__author__='Claire Wang'

import time,requests,unittest,math
from commom import Excel_rd,attachments, get_Time_Type
from testCase.user import user
from testCase.workReport import workReport


class WorkReportCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.wreport = workReport.WorkReport()
        print("报告管理测试：start")
    # class workReport(object):
    '''
        def __init__(self,title,content,type,beginAt,endAt,projectId,attachmentUUId,reviewer,members,isDelayed,crmDatas):
            self.title=title               # 标题，string,提交后自动生成
            self.content=content           #内容，string
            self.type =type                #"报告类型，int,1：日报，2：周报，3：月报"
            self.beginAt=beginAt           #"时间戳 报告起始日期",int64
            self.endAt  =beginAt           #"时间戳 报告结束日期",int64
            self.projectId=projectId         #项目id，string
            self.attachmentUUId=attachmentUUId    #"附件guid",string
            self.reviewer=reviewer           #"点评人","Reviewer"
            self.members =members            #"抄送人""Member"
            self.isDelayed=isDelayed         # "是否补签",bool
            self.crmDatas=crmDatas           # "过程统计信息", Array("CRMData")
    '''

    # 测试获取跟进中的跟进统计-本月,暂时未判断数据是否正确
    def test_get_CrmData(self):
        """测试报告中跟进统计用例：获取本月跟进统计"""
        begainAT, endAt=get_Time_Type.getTimeRegionByType('TheMonth')
        r = self.wreport.get_CrmData(begainAT, endAt)
        print("111", r.text)
        self.assertEqual(r.status_code, 200)
        Tp = isinstance(r.json(), list)   # 看返回类型是不是一个list数组
        self.assertTrue(Tp)

    # 测试新建报告
    def test_CreateWorkReport(self):
        """测试新建报告用例：正常新建报告"""
        reportType = 3
        # "报告类型，int,1：日报，2：周报，3：月报"
        if reportType == 1:
            T = get_Time_Type.getTimeRegionByType('Today')
            beginAt=T[0]
            endAt=T[1]
        elif reportType==2:
            T = get_Time_Type.getTimeRegionByType('TheWeek')
            beginAt = T[0]
            endAt = T[1]
        elif reportType==3:
            T= get_Time_Type.getTimeRegionByType('TheMonth')
            beginAt = T[0]
            endAt = T[1]
        else:
            print('报告类型错误!')
            beginAt = 0
            endAt = 0

        wr =workReport.WorkReport()
        u = user.User()
        reviewer = u.get_User('刘洋C')   # 返回类型为字典
        members = [u.get_User('陈老师'), u.get_User('李明A')]
        workreport_request = {
            "activityStat": True,
            "content": "新建报告"+time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time())),
            "crmDatas": wr.get_CrmData(beginAt,endAt).json(),
            "members": {
                "users": members
            },
            "beginAt": beginAt,
            "endAt": endAt,
            "uuid": "",
            "type": reportType,
            "isDelayed": False,
            "reviewer": {
                "user": reviewer
            }
        }

        result = wr.creat_WorkReport(workreport_request)
        self.assertEqual(result.status_code, 200)
        workreport_response = result.json()
        print("报告详情：", workreport_response)
        # 返回类型为字典
        self.assertEqual(workreport_request['type'],workreport_response['type'],msg='报告类型错误')       # 验证报告类型是否与提交一致
        self.assertEqual(workreport_request["beginAt"],workreport_response["beginAt"],msg='报告日期错误')      # 验证报告日期是否与提交一致
        self.assertEqual(workreport_request["endAt"], workreport_response["endAt"])
        self.assertEqual(workreport_request['content'],workreport_response['content'])       # 验证报告内容是否与提交一致
        self.assertEqual(workreport_request['crmDatas'], workreport_response['crmDatas'])   # 验证跟进统计是否与提交一致

    # 测试编辑报告
    def test_Edit_Wreport(self):
        '''测试编辑报告用例：编辑报告内容'''
        reportType = 3
        # "报告类型，int,1：日报，2：周报，3：月报"
        if reportType == 1:
            T = get_Time_Type.getTimeRegionByType('Today')
            beginAt = T[0]
            endAt = T[1]
        elif reportType == 2:
            T = get_Time_Type.getTimeRegionByType('TheWeek')
            beginAt = T[0]
            endAt = T[1]
        elif reportType == 3:
            T = get_Time_Type.getTimeRegionByType('TheMonth')
            beginAt = T[0]
            endAt = T[1]
        us = user.User()
        reviewer = us.get_User('刘洋C')
        members = [us.get_User('布莱尔'), us.get_User('李明A')]
        wreport = workReport.WorkReport()
        wreportId = wreport.getID()
        wreport_request={
            "activityStat": True,
            "crmDatas": wreport.get_CrmData(beginAt, endAt).json(),
            "content": "1、这里是编辑过得报告内容，2、呵呵",
            "projectId": "5a0ae0fd19b8207d13c71252",
            "reviewer": {
                "user": reviewer
                            },
            "members": {
                "users": members
                        },
            }

        result=wreport.edit_wreport(wreportId,wreport_request)
        print(result.json())
        self.assertEqual(result.status_code,200)
        wreport_response=result.json()
        self.assertEqual(wreport_request['content'],wreport_response['content'])  #判断报告内容是否语体教相同

    # 测试我的报告列表-本月
    def test_Wreport_Mylist(self):
        """测试获取我的报告列表用例：默认获取本月数据"""
        startAt, endAt = get_Time_Type.getTimeRegionByType('TheMonth')
        param = {
            'pageIndex': 1,
            'pageSize': 20,
            'reportType': 0,
            'isReviewed': 0,
            'sendType':0,
            'startAt': startAt,
            'endAt': endAt
        }
        result = self.wreport.get_MyWrportlist(param)
        self.assertEqual(result.status_code,200)
        records=result.json()['records']
        totalRecords=result.json()['totalRecords']
        if totalRecords > param["pageSize"]:
            page = math.ceil(totalRecords / param["pageSize"])
            for p in range(2, page + 1):
                param["pageIndex"] = p
                pageResult = self.wreport.get_MyWrportlist(param)
                json = pageResult.json()
                pagedata = json["records"]
                records.extend(pagedata)
        print("本月报告数量", len(records))
        self.assertEqual(totalRecords, len(records), msg='返回总数与实际数量总数不同')  # 判断返回的数据总数与实际数据数量是否相同

        '''
            if len(records)>0:    #列表没反回抄送人所以无法判断数据准确性
                for wr in records:
                    reviewerName=wr['reviewerName']
                    creatorName=wr['creatorName']
          '''

    def T_Wreport_TeamList(self):
        """测试获取团队报告列表用例：获取本月团队报告"""
        startAt, endAt = get_Time_Type.getTimeRegionByType('TheMonth')
        result = self.wreport.get_Teamlist(startAt, endAt, reportType=0, isReviewed=0)
        self.assertEqual(result.status_code, 200)
        if result.status_code == 200:
            records = result.json()['records']
            totalRecords = result.json()['totalRecords']

            t=records[0]['createdAt']  # 获取第一条数据的创建时间
            for wr in records:  # 判断数据列表按创建时间倒叙
                self.assertTrue(t >= wr['createdAt'])
                t = wr['createdAt']

    def test_Wreport_Search(self):
        """测试报告列表搜索：关键字“测试周报"""
        startAt, endAt = get_Time_Type.getTimeRegionByType('TheMonth')
        param = {
            'pageIndex': 1,
            'pageSize': 20,
            'reportType': 0,
            'isReviewed': 0,
            'sendType': 0,
            'keyword': '测试周报'
        }
        result = self.wreport.get_MyWrportlist(param)
        self.assertEqual(result.status_code, 200)
        records = result.json()['records']
        totalRecords = result.json()['totalRecords']
        if totalRecords > param["pageSize"]:
            page = math.ceil(totalRecords / param["pageSize"])
            for p in range(2, page + 1):
                param["pageIndex"] = p
                pageResult = self.wreport.get_MyWrportlist(param)
                json = pageResult.json()
                pagedata = json["records"]
                records.extend(pagedata)
        print("搜索结果报告数量", len(records))
        self.assertEqual(totalRecords, len(records), msg='返回总数与实际数量总数不同')  # 判断返回的数据总数与实际数据数量是否相同
        # 判断报告内容或标题是否包含关键字

    @classmethod
    def tearDownClass(cls):
        print('报告管理测试：end')


if __name__ == '__main__':
    unittest.main()
