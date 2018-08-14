import requests,unittest
import readConfig


class User(object):
    def __init__(self):
        f = readConfig.ReadConfig()
        userName = f.getUserValue('username')
        pwd = f.getUserValue('password')
        self.host = f.getHttpValue('app_userhost')
        self.baseurl = f.getHttpValue("app_userbaseurl")
        authorization = f.getUserValue("authorization")
        # 配置请求头
        self.head = f.get_header()
        self.head["Host"] = self.host
        self.head["Authorization"] = authorization
        self.id = f.getUserValue("userid")

    # 获取组织架构接口
    def get_Organization(self):
        url = self.baseurl+"/api/v2/user/organization"
        result = requests.get(url, headers=self.head)
        return result

    # 获取非本人的一个用户信息
    def get_colleague(self):
        try:
            org = self.get_Organization().json()
            for dept in org:
                if dept["userNum"] == 0:
                    continue
                users = dept["users"]
                for user in users:
                    if user["id"] != self.id:
                        return user
        except Exception as e:
            print("获取公司非自己的用户失败", e)

    # 根据部门名称获取部门信息
    def get_Dept(self, deptName):
        r = self.get_Organization()
        if r.status_code == 200:
            oranization = r.json()    # 返回类型为list，每个值为一个部门信息
            n = 0
            while n < len(oranization):
                dept_response = oranization[n]            # user类型为字典
                if dept_response['name'] == deptName:
                    dept = dept_response
                    break
                n += 1
        return dept

    # 根据部门xpath获取部门人员
    def get_DeptUsersId(self,deptxpath):
        r=self.get_Organization()
        if r.status_code==200:
            oranization=r.json()    # 返回类型为list，每个值为一个部门信息
            n=0
            deptusersId=[]
            while n<len(oranization):
                dept_response=oranization[n]            # user类型为字典
                if dept_response['xpath'] == deptxpath:
                    users=dept_response['users']
                    print(users)
                    for u in range(0,len(users)):
                        deptusersId.append(users[u]['id'])
                    break
                n=n+1
        return deptusersId

    # 根据用户名获取某个人员的信息
    def get_User(self, userName):
        r = self.get_Organization()
        if r.status_code != 200:
            return None
        oranization = r.json()  # 返回类型为list，每个值为一个部门信息
        user = {}
        user['name'] = userName
        for dept in oranization:
            if "users" not in dept.keys():
                continue
            users = dept['users']
            n = 0
            while n < len(users):
                user_response = users[n]  # user类型为字典
                if user_response['name'] == userName:
                    user["id"] = user_response["id"]
                    user["avatar"] = user_response["avatar"]
                    break
                n += 1
        return user

    # 根据用户名获取用户id
    def get_UserId(self, userName):
        r = self.get_Organization()
        if r.status_code != 200:
            return None
        oranization = r.json()  # 返回类型为list，每个值为一个部门信息
        userId = None
        for dept in oranization:
            if "users" not in dept.keys():
                continue
            users = dept["users"]
            n = 0
            while n < len(users):
                user_response = users[n]  # user类型为字典
                if user_response['name'] == userName:
                    userId = user_response["id"]
                    break
                n += 1
        if userId == None:
             print('输入的用户名不存在')
        return userId

    # 获取个人信息
    def get_UserProfile(self):
        url = self.baseurl + "/api/v2/user/newprofile"
        result = requests.get(url, headers=self.head)
        return result

    # 获取登录人name
    def getName(self):
        result = self.get_UserProfile()
        if result.status_code == 200:
            json_response = result.json()
            if json_response['errmsg'] == 'success':
                return json_response['data']['name']
            else:
                print('登录失败')
        else:
            print('登录失败')


if __name__ == '__main__':
    u = User()
    # print(u.get_Dept("web前端"))
    # print(u.get_User('布莱尔'))
    # print(u.get_UserId("陈老师"))
    # print(u.get_DeptUsersId("57d6333cd33c65554d80513a/57d64d51d33c653e3a000028"))
    # print(u.getName())
    # print(u.get_UserProfile().json())
    print(u.get_colleague())

