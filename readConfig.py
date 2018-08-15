import configparser


class ReadConfig(object):
    def __init__(self):
        try:
            self.cf = configparser.ConfigParser()
            self.cf.read('C:\\Users\\Administrator\\AppInterfaceTest\\config')
        except Exception as e:
            print(e)

    # 获取用户分组下指定名称的值
    def getUserValue(self, name):
        value = self.cf.get("user", name)
        return value

    # 获取HTTP分组下指定名称的值
    def getHttpValue(self, name):
        value = self.cf.get("HTTP", name)
        return value

    # 获取URL分组下的URL
    def get_url(self, sect, name):
        value = self.cf.get(sect, name)
        return value

    # 更新指定user下的token
    def set_token(self, token):
        self.cf.set("user", "Authorization", token)
        self.cf.write(open('E:\\Python\\AppInterfaceTest\\config', 'w'))  # 将对象接入文件

    # 更新登录人的userId
    def set_UserId(self, userId):
        self.cf.set("user", "userId", userId)
        self.cf.write(open('E:\\Python\\AppInterfaceTest\\config', 'w'))
        return self.getUserValue('userId')

    # 获取请求头
    def get_header(self):
        header = {
            "Accept": "",
            "LoyoOSVersion": "",
            "LoyoVersionCode": "2018010401",
            "Accept-Language": 'zh-Hans-CN;q=1',
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "application/json",
            "User-Agent": "",
            "LoyoPlatform": "iOS",
            "LoyoVersionName": "2.7.0",
            "Connection": "keep-alive",
            "LoyoAgent": "iPhone9,1"

        }
        for h in header:
            header[h]=self.cf.get('header', h)
        return header


if __name__ == "__main__":
    r = ReadConfig()
    # print(r.getHttpValue('host'))
    # print(r.getUserValue('username'),r.getUserValue('password'))
    print(r.get_header())
    print(r.set_UserId("1256"))

