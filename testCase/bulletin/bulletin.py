import requests
import readConfig
from testCase.user import user

class Bulletin(object):

    def __init__(self):
        f=readConfig.ReadConfig()
        self.host=f.getHttpValue("host")
        self.baseurl=f.getHttpValue("baseurl")
        Authorization=f.getUserValue("authorization")
        #配置请求头
        self.header=f.get_header()
        self.header["Host"]=self.host
        self.header["Authorization"]= Authorization

    def createBulletin(self,data):
        url=self.baseurl+"/api/v2/oa/bulletin"
        result=requests.post(url,json=data,headers=self.header)
        return result

if __name__=="__main__":
    b=Bulletin()
    print(b.header)
    data={
	"attachmentUUId": "5D46D196-0DE6-467C-8E39-8AD31C498A1B",
	"title": "标题0002",
	"content": "内容3245",
	"members": {
		"depts": [{
			"id": "57d6333cd33c65554d80513a",
			"name": "研发测试用公司",
			"xpath": "57d6333cd33c65554d80513a"
		}],
		"users": []
	},
	"attachments": [{
		"mime": "image\/jpeg",
		"originalName": "IMG_3372.jpg",
		"name": "C7CE1BAA-B711-4608-9162-DDAB907D1BCC\/IMG_3372.jpg"
	}]
}
    print(b.createBulletin(data))

