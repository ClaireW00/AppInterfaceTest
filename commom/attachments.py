import requests
import uuid
import readConfig


# 上传附件返回UUID,现在没有返回UUID
def attachments(BizType):       # BizType为字符类型
    UUid = str(uuid.uuid1())
    f = readConfig.ReadConfig()
    Authorization = f.getUserValue("authorization")
    url = 'https://ukuaiqi.com/p/attachment/api/v2/attachment?uuid=' + UUid
    # 配置请求头
    header = {"Authorization": Authorization}
    file = {'attachments': ('荷花.jpg', open('E:\\Python\\testData\\荷花.jpg', 'rb'), 'image/png'),
                'bizType': BizType,  # "业务类型 (BizType)"
                'uuid': UUid
            }
    r = requests.post(url, headers=header, files=file)
    if r.status_code == 200:
        attach_response = r.json()
        attachment = {'size': attach_response['size'],
                      'originalName': attach_response['originalName'],
                      'mime': attach_response['mime'],
                      'UUId': attach_response['UUId']
                      }
        return attachment
    else:
        print(r.status_code, '-附件上传失败！', r.text)
        return ''


if __name__ == '__main__':

    print(attachments('1'))