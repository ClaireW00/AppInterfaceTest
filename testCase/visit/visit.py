import requests,random
import readConfig
from testCase.user import user

class Visit(object):

    def __init__(self):
        f=readConfig.ReadConfig()
        self.host=f.getHttpValue("host")
        self.baseurl=f.getHttpValue("baseurl")
        Authorization=f.getUserValue("authorization")
        #配置请求头
        self.header=f.get_header()
        self.header["Host"]=self.host
        self.header["Authorization"]= Authorization

    #获取拜访客户列表
    def get_CustormerNearme(self):
        url=self.baseurl+"/api/v2/customer/nearme"
        param={
            "pageIndex	":1,
            "pageSize":20,
            "x":"104.0737074110243",
            "y":"30.68949273003472"
        }
        result=requests.get(url,params=param,headers=self.header)
        return result




    def createVisit(self,data):
        url=self.baseurl+"/api/v2/visit"
        result=requests.post(url,json=data,headers=self.header)
        return result

    def visitList(self, param):
        url = self.baseurl+"/api/v2/visit/team"
        result = requests.get(url, params=param, headers=self.header)
        return result






'''
跟进列表时间类型：
    Today                    = 1  //今天
	YesToday                 = 2  //昨天
	TheWeek                  = 3  //本周
	LastWeek                 = 4  //上周
	TheMonth                 = 5  //本月
	LastMonth                = 6  //上月
	CurrentSeason            = 7  //本季度
	PrecedingQuarter         = 8  //上季度
	CurrentYear              = 9  //今年
	LastYear                 = 10 //去年
	NextWeek                 = 11 //下周
	NextMonth                = 12 //下月
	Tomorrow                 = 13 //明天
	AfterTomorrow            = 14 //后天
	NextSevenDay             = 15 //未来7天
	LastSevenDay             = 16 //最近7天
	LastThirtyDay            = 17 //最近30天
	NextSevenDayContainToday = 18 //未来7天(包含今天)
'''
if __name__=="__main__":
    v=Visit()
    param={
        "customerType":0,
        "filterType " :0,
        "pageIndex	":1,
        "pageSize":10,
        "timeType":17,
        "userId":'',
        "xpath":""
    }

    #print(v.visitList(param).json())

    data={
	"atUserIds": ["58a6c8c3e44c363e73000006"],
	"position": "四川省成都市金牛区北站西二巷36号成都金牛万达广场-甲级写字楼附近",
	"contactName": "姓名0520-0039",
	"isCusPosition": False,
	"gpsInfo": "104.0737581,30.6893964",
	"memo": "我拜访了公司名称0520-0040"+str(random.randint(1,300)),
	"attachmentUUId": "AED29C50-0CD8-4B3E-ABF2-58B1E13BCD20",
	"contactTpl": "13512345671",
	"customerId": "591f20a7e44c36080269f8b2",
	"audioInfo": [{
		"length": 3,
		"fileName": "114F2732-DC35-4591-A103-1829D6C9BC39\/15159865588246.wav"
	}],
	"contactRoleId": ""
}
    #print(v.createVisit(data).json())
    print(v.get_CustormerNearme().json())
