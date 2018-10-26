"工作报告test"
__author__ = 'Claire Wang'

import requests
import readConfig
from commom import get_Time_Type
from testCase.user import user


class WorkReport(object):
    def __init__(self):
        f = readConfig.ReadConfig()
        self.host = f.getHttpValue("host")
        self.baseurl = f.getHttpValue("baseurl")
        self.Authorization = f.getUserValue("authorization")
        # 配置请求头
        self.header = f.get_header()
        self.header["Host"] = self.host
        self.header["Authorization"] = self.Authorization

    """
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
    """

    # 获取crmData
    def get_CrmData(self, begainAt, endAt):
        f = readConfig.ReadConfig()
        header = f.get_header()
        header["Host"] = f.getHttpValue("app_stathost")
        header["Authorization"] = self.Authorization
        url = f.getHttpValue("app_statbaseurl")+"/api/v2/statistics/process/number"
        param = {
            "startTime": begainAt,
            "endTime": endAt
        }
        result = requests.get(url, params=param, headers=header)
        return result

    # 新建报告
    def creat_WorkReport(self, data):
        url = self.baseurl+'/api/v2/oa/wreport'
        result = requests.post(url, json=data, headers=self.header)
        return result



    # 编辑报告
    def edit_wreport(self,wreportId,data):
        url = self.baseurl+'/api/v2/oa/wreport/'+wreportId
        result = requests.put(url, json=data, headers=self.header)
        return result

    '''
        #报告列表查询,默认返回第一页，20条数据，按创建时间查询
        参数:pageIndex int  "当前页码"
        pageSize int"每页记录数"
        sendType int "0:全部, 1:提交给我的 2:我提交的,3: 抄送给我的"
        reportType int "报告类型 全部:0 日报:1 周报:2 月报:3"
        isReviewed int "是否点评 0:全部 1:未点评 2:已点评"
        keyword string "关键词"
        startAt int64 "时间戳 开始时间"
        endAt int64 "时间戳 结束时间"
        '''

    # 获取我的报告列表
    def get_MyWrportlist(self, param):
        url = self.baseurl+'/api/v2/oa/wreport/mobile/simplify'
        result = requests.get(url, params=param, headers=self.header)
        return result

        # 返回我提交的,待点评的第一个报告的ID
    def getID(self):
        startAt, endAt = get_Time_Type.getTimeRegionByType('TheMonth')
        param={
                'pageIndex': 1,
                'pageSize': 20,
                'reportType': 0,
                'isReviewed': 1,
                'sendType':0,
                'startAt': startAt,
                'endAt': endAt
            }
        result = self.get_MyWrportlist(param)
        if result.status_code == 200:
            if len(result.json()['records']) > 0:
                return result.json()['records'][0]['id']
            else:
                print('用户无可编辑的报告')

'''
    #获取团队列表
    def get_Teamlist(self,param):
        url='https://ukuaiqi.com/p/oa/api/v2/oa/wreport/query/web/team'
        params={
            'pageIndex':pageIndex,
            'pageSize':pageSize ,
            'sortBy':sortBy,
            'order':order,
            'isReviewed':isReviewed,
            'keyword' :keyword,
            'xpath' :xpath,
            'userId':userId,
            'startAt':startAt,
            'endAt':endAt,
            'sort':sort
        }
        result=requests.get(url,params=params,headers=self.header)
        return result
'''


if __name__ == '__main__':
    w = WorkReport()
    startAt, endAt = get_Time_Type.getTimeRegionByType('TheMonth')
    # result=w.get_MyWrportlist(startAt, endAt,reportType=0,isReviewed=0,sendType=0)
    print(w.get_CrmData(startAt, endAt).text)
