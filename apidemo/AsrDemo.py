import base64

import requests

from utils.AuthV3Util import addAuthParams

# 您的应用ID
APP_KEY = ''
# 您的应用密钥
APP_SECRET = ''

# 待识别图片路径, 例windows路径：PATH = "C:\\youdao\\media.wav"
PATH = ''


def createRequest():
    '''
    note: 将下列变量替换为需要请求的参数
    取值参考文档: https://ai.youdao.com/DOCSIRMA/html/tts/api/dyysb/index.html
    '''
    rate = '采样率，推荐16000'
    langType = '语种'
    format = 'wav'
    channel = '1'
    docType = 'json'
    type = '1'

    # 数据的base64编码
    q = readFileAsBase64(PATH)
    data = {'q': q, 'rate': rate, 'langType': langType, 'format': format,
            'channel': channel, 'docType': docType, 'type': type}

    addAuthParams(APP_KEY, APP_SECRET, data)

    header = {'Content-Type': 'application/x-www-form-urlencoded'}
    res = doCall('https://openapi.youdao.com/asrapi', header, data, 'post')
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


# 网易有道智云语音识别服务api调用demo
# api接口: https://openapi.youdao.com/asrapi
if __name__ == '__main__':
    createRequest()
