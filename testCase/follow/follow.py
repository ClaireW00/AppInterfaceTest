import requests
import readConfig
import random
from testCase.salesleads import salesleads


class Follow(object):

    def __init__(self):
        self.f = readConfig.ReadConfig()
        self.host = self.f.getHttpValue("host")
        self.baseurl=self.f.getHttpValue("baseurl")
        authorization = self.f.getUserValue("authorization")
        # 配置请求头
        self.header = self.f.get_header()
        self.header["Host"] = self.host
        self.header["Authorization"] = authorization

    # 选择客户后获取写跟进界面
    def new_activity(self, customer_id):
        url = self.baseurl + self.f.get_url("follow", "new_activity") + customer_id
        result = requests.get(url, headers=self.header)
        return result

    # 获取写跟进-线索列表中的一条线索
    def get_saleslead(self):
        sale = salesleads.Salesleades()
        param = {
            "field": "lastActAt",
            "order": "desc",
            "pageIndex": 1,
            "pageSize": 20
        }
        result = sale.own_saleslead(param)
        records = result.json()["data"]["records"]
        if result.json()["data"]["totalRecords"] > 0:
            return records[random.randint(0, len(records)-1)]       # 第一页中任意取一条线索

    # 获取记录行为
    def get_activity_type(self):
        url = self.baseurl + self.f.get_url("follow", "activity_type")
        result = requests.get(url, headers=self.header)
        return result

    # 获取任意一个记录行为id
    def get_activity_type_id(self):
        result = self.get_activity_type()
        data = result.json()["data"]
        num = len(data)
        type_id = data[random.randint(0, num-1)]["id"]      # randint闭包，包含2端的数据
        return type_id

    # 获取写跟进字段
    def get_Properties(self):
        url = self.baseurl+"/api/v2/properties/new"
        param = {
            "isConcision": True,   # 是否使用简介版本，true：是，false：否
            "isEnable": True,   # 是否只返回启用的字段，true:是，false：否
            "isCus": False,   # 是否只获取用户添加的字段，true:是，false：否
            "isSelf": True,  # true过滤创建人、创建时间
            "bizType": 106    # 业务类型，106代表写跟进
        }
        result = requests.get(url, params=param, headers=self.header)
        return result

    # 写跟进
    def create_follow(self, data):
        url = self.baseurl + self.f.get_url("follow", "activity")
        result = requests.post(url, json=data, headers=self.header)
        return result

    # 快速记录列表
    def follow_list(self, param):
        url = self.baseurl + self.f.get_url("follow", "saleactivity_list")
        result = requests.get(url, params=param, headers=self.header)
        return result


if __name__ == "__main__":
    fo = Follow()
    param1 = {
        "pageIndex": 1,
        "pageSize": 10,
        "split": 1,
        "timeType": 17,
        "visitType": 2
    }
    # print("跟进列表：",f.followList(param))

    # print("记录行为：",f.get_Saleactivitytype())
    # print("客户列表：",f.get_CustormerSimilar())
    # print("线索列表：", f.get_SalesLeadSimilar())
    da = {
            "uuid": "46D27661-9767-4FAE-BA50-92EB17C6555C",
            "audioInfo": [{
                "length": 2,
                "fileName": "23584F2B-99AF-41B0-BF60-A48E50755496\/151600699944644.wav"
            }],
            "remindAt": 1516352580,
            "typeId": "57d67241d33c653e3e005203",
            "atUserIds": ["58a6c8c3e44c363e73000006"],
            "contactPhone": "1351234567",
            "contactName": "订单",
            "tags": [{
                "tId": "59295aa462dfca0584f327ba",
                "itemName": "2-5种",
                "itemId": "59295aa462dfca0584f327bc"
            }, {
                "tId": "57d6333dd33c653e3e00469f",
                "itemName": "房地产",
                "itemId": "57d6333dd33c653e3e0046a2"
            }],
            "customerId": "59a7b7c919b820383c356d32",
            "extUpdateAt": 1512959975,
            "location": {
                "loc": [30.689161, 104.0737],
                "addr": "成都龙腾越人力资源管理有限公司(今年万达甲级写字楼B座3101)"
            },
            "isEnableCus": True,
            "contactId": "59a7b7c919b820383c356d33",
            "statusId": "591ef53b088cf34d1c59a6f2",
            "contactRoleId": "58a593d97c5f1d7ab3465e8e",
            "extFields": {
                "e1635e0c-6312-4a07-9257-2d72ed6a938b": {
                    "val": "May",
                    "properties": {
                        "fieldName": "e1635e0c-6312-4a07-9257-2d72ed6a938b",
                        "defVal": ["January", "February", "March", "April", "May", "June", "July"],
                        "sortable": False,
                        "label": "月份多选",
                        "val": "",
                        "isSpecial": False,
                        "isCustom": True,
                        "type": "multi-select",
                        "order": 7,
                        "isCommon": True,
                        "enabled": True,
                        "isSystem": False,
                        "required": True,
                        "name": "e1635e0c-6312-4a07-9257-2d72ed6a938b"
                    }
                },
                "bcfd12af-e60e-41c9-9133-5a387d4f4b7d": {
                    "val": "测试123456",
                    "properties": {
                        "fieldName": "bcfd12af-e60e-41c9-9133-5a387d4f4b7d",
                        "defVal": [],
                        "sortable": False,
                        "label": "犆st",
                        "val": "",
                        "isSpecial": False,
                        "isCustom": True,
                        "type": "string",
                        "order": 9,
                        "isCommon": True,
                        "enabled": True,
                        "isSystem": False,
                        "required": True,
                        "name": "bcfd12af-e60e-41c9-9133-5a387d4f4b7d"
                    }
                },
                "b426ef7e-5407-4a3b-9ead-75c5363edf0f": {
                    "val": "1579017600",
                    "properties": {
                        "fieldName": "b426ef7e-5407-4a3b-9ead-75c5363edf0f",
                        "defVal": [],
                        "sortable": False,
                        "label": "date日期",
                        "val": "",
                        "isSpecial": False,
                        "isCustom": True,
                        "type": "date",
                        "order": 6,
                        "isCommon": True,
                        "enabled": True,
                        "isSystem": False,
                        "required": False,
                        "name": "b426ef7e-5407-4a3b-9ead-75c5363edf0f"
                    }
                }
            },
            "content": "手动新建跟进数据"
        }
    # print(fo.createFollow(da).json())
    # fo.get_Properties()
    print(fo.get_activity_type_id())

