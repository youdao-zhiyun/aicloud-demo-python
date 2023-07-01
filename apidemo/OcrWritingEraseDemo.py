import base64

import requests

from utils.AuthV3Util import addAuthParams

# 您的应用ID
APP_KEY = ''
# 您的应用密钥
APP_SECRET = ''

# 待识别图片路径, 例windows路径：PATH = "C:\\youdao\\picture.jpg"
PATH = ''

def createRequest():
    '''
    note: 将下列变量替换为需要请求的参数
    取值参考文档: https://ai.youdao.com/DOCSIRMA/html/ocr/api/sxocr/index.html
    '''
    # 是否进行360角度识别 0：不识别，1：识别。
    angle = '0'

    # 数据的base64编码
    q = readFileAsBase64(PATH)
    data = {'q': q, 'angle': angle}

    addAuthParams(APP_KEY, APP_SECRET, data)

    header = {'Content-Type': 'application/x-www-form-urlencoded'}
    res = doCall('https://openapi.youdao.com/ocr_writing_erase', header, data, 'post')
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


# 网易有道智云手写体擦除服务api调用demo
# api接口: https://openapi.youdao.com/ocr_writing_erase
if __name__ == '__main__':
    createRequest()
