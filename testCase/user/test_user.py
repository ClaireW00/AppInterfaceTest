import requests,unittest
import readConfig
from testCase.user import user


class UserCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("获取组织架构测试：start")

    # 测试获取组织架构接口
    def test_Get_Allusers(self):
        """测试获取组织架构接口：获取组织架构"""
        u = user.User()
        r = u.get_Organization()
        self.assertEqual(r.status_code, 200)
        if r.status_code == 200:
            organization = r.json()
            self.assertTrue(len(organization) > 0)    # 判断返回的组织架构中有数据

    # test获取个人信息接口
    def test_UserProfile(self):
        """测试个人信息界面"""
        f = readConfig.ReadConfig()
        username = f.getUserValue('username')
        u = user.User()
        result = u.get_UserProfile()
        self.assertEqual(result.status_code, 200)
        if result.status_code == 200:
            json_response = result.json()
            self.assertEqual(json_response["errcode"], 0, msg='返回信息错误')
            self.assertEqual(json_response["errmsg"], "success", msg='返回信息错误')
            if json_response["errmsg"] == "success":
                username_response = json_response['data']["username"]
                self.assertEqual(username, username_response, msg='登录人与返回信息不一致')
                print('登录人userName:', username_response)

    @classmethod
    def tearDownClass(cls):
        print('获取组织架构：end')

if __name__=='__main__':
    unittest.main()
