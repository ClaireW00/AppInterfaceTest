import requests
import readConfig


class Project(object):

    def __init__(self):
        self.f = readConfig.ReadConfig()
        host = self.f.getHttpValue('host')
        self.baseurl = self.f.getHttpValue('baseurl')
        self.header = self.f.get_header()
        self.header['host'] = host
        self.header["Authorization"] = self.f.getUserValue('authorization')

    # 获取我的项目列表
    def my_list(self, param):
        url = self.baseurl + "/api/v2/oa/project/query/mobile"
        result = requests.get(url, headers=self.header, params=param)
        return result

    # 获取新建任务、审批、报告归档项目列表
    def get_query(self, param):
        url = self.baseurl + self.f.get_url("project", "query")
        result = requests.get(url, params=param, headers=self.header)
        return result

    # 获取全公司最新的一个客户，返回id和客户名称
    def get_customer_similar(self, param):

        url = self.baseurl + '/api/v2/customer/similar'
        try:
            result = requests.get(url, headers=self.header, params=param)
            cus_response = result.json()['data']['records']
            cust = cus_response[0]
            return cust['id'], cust['name']
        except Exception as E:
            print('result.text')

    # 新建项目
    def create_project(self, data):
        url = self.baseurl+'/api/v2/oa/project'
        result = requests.post(url, json=data, headers=self.header)
        return result

    # 获取项目关联模板
    def get_temp(self):
        url = self.baseurl+"/api/v2/oa/project/temp/list"
        result = requests.get(url, headers=self.header)
        return result

    # 新建目录
    def create_node(self, project_id, data):
        url = self.baseurl + "/api/v2/oa/project/node/" + project_id
        result = requests.post(url, headers=self.header, json=data)
        return result

    # 获取项目详情
    def project_detail(self, project_id):
        url = self.baseurl + "/api/v2/oa/project/" + project_id
        result = requests.get(url, headers=self.header)
        return result

    # 获取团队项目列表
    def team_list(self, param):
        url = self.baseurl + "/api/v2/oa/project/query/team/mobile"
        result = requests.get(url, headers=self.header, params=param)
        return result

if __name__ == '__main__':
    data1 = {
        "title": "项目0224-1133",
        "content": "项目简介009",
        "managers": [{
            "canReadAll": True,
            "user": {
                "name": "claire",
                "id": "5822f0eee44c3625ef0000bb",
                "avatar": "https:\/\/uimg.ukuaiqi.com\/8CC7BE04-EF5D-40D8-89DB-8B0B415B9294\/2CD97777-A86E-4469-83AD-A81A0000B821.jpg"
            }
        }],  # 负责人
        "members": [
            {
            "canReadAll": False,
            "user": {
                "name": "丁越（商务电话）",
                "id": "5a29ecd519b820025aea4171",
                "avatar": "https:\/\/dist.ukuaiqi.com\/male.png"
            }
            },
            {
            "canReadAll": False,
            "user": {
                "name": "侯超同学",
                "id": "59642a954eba364073d9d1d1",
                "avatar": "https:\/\/dist.ukuaiqi.com\/male.png"
            }
            }
        ],     # 参与人
        "customerId": "591f20a7e44c36080269f8b2",  # 关联客户ID
        "customerName": "公司名称0520-0040",  # 关联客户名称
        "projectTempId": "5977256419b82054bcb5e42c",  # 关联模板ID
        "projectTempName": "销售人员招聘"              # 关联模板名称
    }
    p = Project()
    r = p.create_project(data1)
    print(r.json())
