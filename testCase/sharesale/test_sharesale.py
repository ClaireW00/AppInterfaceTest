import requests,unittest
from testCase.login import test_login
from commom import Excel_rd
import readConfig

class ShareSale(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        f=readConfig.ReadConfig()
        Authorization = f.getUserValue("authorization")
        cls.header = {
            "Authorization": Authorization
        }

    #开通共享销售
    def share_sale(self,data):
        url='https://ukuaiqi.com/p/oa/api/v2/shared/sale/itaojin'
        result = requests.post(url, json=data, headers=self.header).json()
        return result

    #测试开通Excel表中的公司的共享销售功能
    def test_OpenUp_sahresale(self):
        '''测试开通共享销售：开通excel表中给出的公司共享销售功能'''
        file='E:\\Python\\testData\\testcase_sharesales.xlsx'
        datas=Excel_rd.read_excel_table_byindex(file)

        for data in datas:
            result=self.share_sale(data)
            self.assertEqual(result['errcode'],0)
            self.assertEqual(result['errmsg'],'success')

    @classmethod
    def tearDownClass(cls):
        print('开通共享销售：end')

if __name__=='__main__':
    unittest.main()
