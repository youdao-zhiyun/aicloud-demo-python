import requests

from utils.AuthV3Util import addAuthParams

# 您的应用ID
APP_KEY = ''
# 您的应用密钥
APP_SECRET = ''


def createRequest():
    '''
    note: 将下列变量替换为需要请求的参数
    取值参考文档: https://ai.youdao.com/DOCSIRMA/html/dictionary/api/ydcd/index.html
    '''
    q = '待查询的词'
    lang_type = '输入的语言'
    dicts = '词典名'

    data = {'q': q, 'langType': lang_type, 'dicts': dicts}

    addAuthParams(APP_KEY, APP_SECRET, data)

    header = {'Content-Type': 'application/x-www-form-urlencoded'}
    res = doCall('https://openapi.youdao.com/v2/dict', header, data, 'post')
    print(str(res.content, 'utf-8'))


def doCall(url, header, params, method):
    if 'get' == method:
        return requests.get(url, params)
    elif 'post' == method:
        return requests.post(url, params, header)

# 网易有道智云有道词典服务api调用demo
# api接口: https://openapi.youdao.com/v2/dict
if __name__ == '__main__':
    createRequest()
