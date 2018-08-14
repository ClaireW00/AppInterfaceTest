import random
import requests
import readConfig


class CustomerManger(object):
    def __init__(self):
        self.f = readConfig.ReadConfig()
        self.host = self.f.getHttpValue("host")
        self.baseurl = self.f.getHttpValue("baseurl")
        authorization = self.f.getUserValue("authorization")
        # 配置请求头
        self.header = self.f.get_header()
        self.header["Host"] = self.host
        self.header["Authorization"] = authorization

    # 获取客户状态接口
    def get_tags(self, param):
        url = self.baseurl + self.f.get_url("customer", "tags")
        result = requests.get(url, headers=self.header, params=param)
        return result

    # 获取一个开发客户状态表中随机一个状态ID
    def get_status(self):
        param = {
            "filterType": 0,
            "tagsType": 0
        }
        result = self.get_tags(param)
        if result.status_code != 200:
            return None
        try:
            response_data = result.json()["data"]
            items = response_data[0]["items"]      # 开发客户状态
            number = len(items)
            num = random.randint(0, number-1)
            status = items[num]["id"]
            return status
        except Exception as e:
            print(e, "获取开发客户状态ID出错")

    # 新建客户
    def new_customer(self, customer_data):
        url = self.baseurl+self.f.get_url("customer", "customer")
        # 新建客户请求
        result = requests.post(url, json=customer_data, headers=self.header)
        return result

    # 获取客户详情
    def customer_detail(self, customer_id):
        url = self.baseurl + self.f.get_url("customer", "customer_detail") + customer_id
        result = requests.get(url=url, headers=self.header)
        return result

    # 客户详情快捷编辑状态
    def edit_status(self, customer_id, status):
        url = self.baseurl + self.f.get_url("customer", "status_edit") + customer_id
        result = requests.put(url, headers=self.header, json=status)
        return result

    # 编辑客户
    def edit_customer(self, data, customer_id):
        url = self.baseurl + self.f.get_url("customer", "customer")+customer_id
        result = requests.put(url, headers=self.header, json=data)
        return result

    # 删除客户
    def delete_customer(self, customer_id):
        url = self.baseurl + self.f.get_url("customer", "customer_delete") + customer_id
        result = requests.delete(url, headers=self.header)
        return result

    # 转移客户
    def owner_customer(self, data):
        url = self.baseurl + self.f.get_url("customer", "owner")
        result = requests.put(url, headers=self.header, json=data)
        return result

    # 丢公海开关是否开启
    def cus_reason_switcher(self):
        url = self.baseurl + self.f.get_url("customer", "config") + "?key=cus_reason_switcher"
        result = requests.get(url, headers=self.header)
        return result

    # 获取丢公海原因
    def cus_reason(self):
        url = self.baseurl + self.f.get_url("customer", "reason")
        result = requests.get(url, headers=self.header)
        return result

    # 手动丢公海
    def throw_sea(self, customer_id, *kw):     # 关键字参数
        url = self.baseurl + self.f.get_url("customer", "customer") + customer_id + "/sea"
        if len(kw) == 0:
            result = requests.put(url, headers=self.header)
        else:
            result = requests.put(url, headers=self.header, json=kw[0])
        return result

    # 客户详情跟进列表
    def cus_saleactivity(self, customer_id, param):
        url = self.baseurl + self.f.get_url("customer", "cus_saleactivity") + customer_id
        result = requests.get(url, headers=self.header, params=param)
        return result

    # 客户详情拜访列表
    def cus_visit(self, param):
        url = self.baseurl + self.f.get_url("customer", "cus_visit")
        result = requests.get(url, headers=self.header, params=param)
        return result

    # 客户详情订单列表
    def cus_order(self, customer_id, param):
        url = self.baseurl + self.f.get_url("customer", "cus_order") + customer_id
        result = requests.get(url, headers=self.header, params=param)
        return result

    # 客户详情任务列表
    def cus_task(self, param):
        url = self.baseurl + self.f.get_url("task", "task_own")
        result = requests.get(url, headers=self.header, params=param)
        return result

    # 客户详情机会列表
    def cus_chance(self, param):
        url = self.baseurl + self.f.get_url("customer", "cus_chance")
        result = requests.get(url, headers=self.header, params=param)
        return result

    # 客户详情审批列表
    def cus_wfinstance(self, customer_id, param):
        url = self.baseurl + self.f.get_url("customer", "cus_wfinstance") + customer_id
        result = requests.get(url, headers=self.header, params=param)
        return result

    # 客户详情项目列表
    def cus_project(self, customer_id, param):
        url = self.baseurl + self.f.get_url("customer", "cus_project") + customer_id
        result = requests.get(url, headers=self.header, params=param)
        return result

    # 客户详情快点
    def cus_speedup(self, customer_id, param):
        url = self.baseurl + self.f.get_url("customer", "cus_speedup") + customer_id
        result = requests.get(url, headers=self.header, params=param)
        return result

    # 新建客户联系人
    def create_contact(self, customer_id, data):
        url = self.baseurl + self.f.get_url("customer", "create_contact") + customer_id
        result = requests.post(url, headers=self.header, json=data)
        return result

    # 获取客户联系人列表
    def contact(self, customer_id):
        url = self.baseurl + self.f.get_url("customer", "contact") + customer_id
        result = requests.get(url, headers=self.header)
        return result

    # 获取列表第一条数据ID
    def getCustomerID(self):
        param = {
            "order": "asc",
            "pageIndex": 1,
            "pageSize": 20,
            "field": "lastActAt"
        }
        result = self.customer_OwnList(param)
        json_result = result.json()
        if json_result["errmsg"] == "success":
            custs = json_result["data"]["records"]
            return custs[0]["id"]

    # 我负责的客户列表
    def customer_OwnList(self, param):
        url = self.baseurl + self.f.get_url("customer", "customer_own")
        result = requests.post(url, headers=self.header, json=param, timeout=15)
        return result

    # 我参与的客户列表
    def customer_link(self, param):
        url = self.baseurl + self.f.get_url("customer", "customer_link")
        result = requests.post(url, headers=self.header, json=param)
        return result

    # 获取团队客户列表
    def customer_team(self, param):
        url = self.baseurl + self.f.get_url("customer", "customer_team")
        result = requests.post(url, headers=self.header, json=param)
        return result

    # 获取和我相关的客户列表
    def customer_similar(self, param):
        url = self.baseurl + self.f.get_url("customer", "customer_similar")
        result = requests.get(url, params=param, headers=self.header)
        return result

    # 获取和我相关的客户列表第一条数据信息dict
    def get_similar_customer(self):
        param = {
            "isAll": False,  # true，全公司数据，false排除公海客户
            "isSelf": True,  # true 我负责的和我参与的，false的情况没有
            "pageIndex": 20,
            "pageSize": 1
        }
        result = self.customer_similar(param)
        result_json = result.json()
        if result_json['data']['totalRecords'] > 0:
            records = result_json["data"]["records"]
            return records[0]
        else:
            print("该用户无客户，请先创建客户！")


if __name__ == '__main__':
    c = CustomerManger()
    param1 = {
        "order": "asc",
        "pageIndex": 1,
        "pageSize": 20,
        "field": "lastActAt"
    }
    # print(c.custorm_OwnList(param1).json())
    data1 = {
        "summary": "",
        "contacts.wiretel": [],
        "name": "客户0116-1425",
        "uuid": "5FBD1E09-D97B-41A4-81F8-F94AA36843A5",
        "webSite": "",
        "statusId": "57d6333dd33c653e3e004699",
        "regional": {},
        "tags": [{
            "tId": "57d6333dd33c653e3e00469f",
            "itemName": "金融保险",
            "itemId": "57d6333dd33c653e3e0046a1"
        }],
        "loc": {
            "loc": [0, 0],
            "addr": "成都市人民北路"
        }
    }
    # print(c.custorm_Link(param1).json())
    customerId = "5ae31c3b62dfca34f6d721ff"
    param2 = {
            "pageIndex": 1,
            "userId": ""
    }
    # print(c.custorm_team(param2).json())
    # print(c.getCustormID())
    print(c.cus_speedup(customerId, param2).json())
