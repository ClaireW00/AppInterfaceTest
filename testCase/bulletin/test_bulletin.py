import time,random, unittest
from testCase.bulletin import bulletin
from commom import attachments
from testCase.user import user


class BulletinCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):   # 类方法
        print('测试发布公告：start')

    def test_CreateBulletin(self):  # 实例方法
        """测试发布公告用例：填写所有字段 """
        U = user.User()
        attachment = attachments.attachments('19')
        data_request = {
            "attachmentUUId":attachment['UUId'],
            "title": "公告标题"+time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time())),
            "content": "公告内容"+str(random.randint(1,300)),
            "members": {
                "depts": [U.get_Dept('销售部')],
                "users": [U.get_User('陈老师')]
            },
            "attachments": [attachment]
        }
        B=bulletin.Bulletin()
        result=B.createBulletin(data_request)
        self.assertEqual(result.status_code,200)
        data_response=result.json()
        self.assertEqual(data_request['title'],data_response['title'])
        self.assertEqual(data_request['content'],data_response['content'])


if __name__=="__main__":
    unittest.main()