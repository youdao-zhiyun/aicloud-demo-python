import base64

import requests

from utils.AuthV3Util import addAuthParams

# 您的应用ID
APP_KEY = ''
# 您的应用密钥
APP_SECRET = ''

# 作文图片路径, 例windows路径：PATH = "C:\\youdao\\media.jpg"
PATH = ''


def createRequest():
    '''
    note: 将下列变量替换为需要请求的参数
    取值参考文档: https://ai.youdao.com/DOCSIRMA/html/%E4%BD%9C%E6%96%87%E6%89%B9%E6%94%B9/API%E6%96%87%E6%A1%A3/%E4%B8%AD%E6%96%87%E4%BD%9C%E6%96%87%E6%89%B9%E6%94%B9%EF%BC%88%E5%9B%BE%E5%83%8F%E8%AF%86%E5%88%AB%EF%BC%89/%E4%B8%AD%E6%96%87%E4%BD%9C%E6%96%87%E6%89%B9%E6%94%B9%EF%BC%88%E5%9B%BE%E5%83%8F%E8%AF%86%E5%88%AB%EF%BC%89-API%E6%96%87%E6%A1%A3.html
    '''
    grade = '作文等级'
    title = '作文标题'
    requirement = '题目要求'

    # 数据的base64编码
    q = readFileAsBase64(PATH)
    data = {'q': q, 'grade': grade, 'to': title, 'requirement': requirement}

    addAuthParams(APP_KEY, APP_SECRET, data)

    header = {'Content-Type': 'application/x-www-form-urlencoded'}
    res = doCall('https://openapi.youdao.com/correct_writing_cn_image', header, data, 'post')
    print(str(res.content, 'utf-8'))


def doCall(url, header, params, method):
    if 'get' == method:
        return requests.get(url, params)
    elif 'post' == method:
        return requests.post(url, params, header)


def readFileAsBase64(path):
    f = open(path, 'rb')
    data = f.read()
    return str(base64.b64encode(data), 'utf-8')


# 网易有道智云中文图片作文批改服务api调用demo
# api接口: https://openapi.youdao.com/correct_writing_cn_image
if __name__ == '__main__':
    createRequest()
