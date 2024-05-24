import requests
import sseclient

from utils.AuthV3Util import addAuthParams

# 您的应用ID
APP_KEY = ''
# 您的应用密钥
APP_SECRET = ''


def createRequest():
    '''
    note: 将下列变量替换为需要请求的参数
    '''
    i = '待翻译文本'
    lang_from = '源语种'
    lang_to = '目标语种'

    data = {'q': i, 'from': lang_from, 'to': lang_to, 'i': i}

    addAuthParams(APP_KEY, APP_SECRET, data)

    header = {'Content-Type': 'application/x-www-form-urlencoded', 'Accept': 'text/event-stream'}
    doCall('https://openapi.youdao.com/llm_trans', header, data, 'post')


def doCall(url, header, params, method):
    if 'get' == method:
        client = requests.get(url, params, headers=header)
    elif 'post' == method:
        client = requests.post(url, data=params, stream=True, headers=header)
    client = sseclient.SSEClient(client)
    for event in client.events():
        print(event.event)
        print(event.data)

# 网易有道智云大模型翻译服务api调用demo
# api接口: https://openapi.youdao.com/llm_trans
if __name__ == '__main__':
    createRequest()
