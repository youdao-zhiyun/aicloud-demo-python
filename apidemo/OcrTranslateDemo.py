import base64

import requests

from utils.AuthV3Util import addAuthParams

# 您的应用ID
APP_KEY = ''
# 您的应用密钥
APP_SECRET = ''

# 待翻译图片路径, 例windows路径：PATH = "C:\\youdao\\media.jpg"
PATH = ''


def createRequest():
    '''
    note: 将下列变量替换为需要请求的参数
    取值参考文档: https://ai.youdao.com/DOCSIRMA/html/%E8%87%AA%E7%84%B6%E8%AF%AD%E8%A8%80%E7%BF%BB%E8%AF%91/API%E6%96%87%E6%A1%A3/%E5%9B%BE%E7%89%87%E7%BF%BB%E8%AF%91%E6%9C%8D%E5%8A%A1/%E5%9B%BE%E7%89%87%E7%BF%BB%E8%AF%91%E6%9C%8D%E5%8A%A1-API%E6%96%87%E6%A1%A3.html
    '''
    lang_from = '源语言语种'
    lang_to = '目标语言语种'
    render = '是否需要服务端返回渲染的图片'
    type = '1'

    # 数据的base64编码
    q = readFileAsBase64(PATH)
    data = {'q': q, 'from': lang_from, 'to': lang_to, 'render': render, 'type': type}

    addAuthParams(APP_KEY, APP_SECRET, data)

    header = {'Content-Type': 'application/x-www-form-urlencoded'}
    res = doCall('https://openapi.youdao.com/ocrtransapi', header, data, 'post')
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


# 网易有道智云图片翻译服务api调用demo
# api接口: https://openapi.youdao.com/ocrtransapi
if __name__ == '__main__':
    createRequest()
