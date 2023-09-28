import requests

from utils.AuthV3Util import addAuthParams

# 您的应用ID
APP_KEY = ''
# 您的应用密钥
APP_SECRET = ''


def createRequest():
    '''
    note: 将下列变量替换为需要请求的参数
    '''
    q1 = '待输入文本1'
    q2 = '待输入文本2'
    q3 = '待输入文本3'
    # q4...

    header = {'Content-Type': 'application/x-www-form-urlencoded'}
    # 1、请求version服务
    # 注: q参数本身非必传, 但是计算签名时需要用作空字符串处理""
    data = {'q': ""}
    addAuthParams(APP_KEY, APP_SECRET, data)
    res = doCall('https://openapi.youdao.com/textEmbedding/queryTextEmbeddingVersion', header, data, 'get')
    print("version: " + str(res.content, 'utf-8'))

    # 2、请求embedding服务
    # 注: 包含16个q时效果最佳, 每个q不要超过500个token
    data = {'q': [q1, q2, q3]}
    addAuthParams(APP_KEY, APP_SECRET, data)
    res = doCall('https://openapi.youdao.com/textEmbedding/queryTextEmbeddings', header, data, 'post')
    print("embedding: " + str(res.content, 'utf-8'))


def doCall(url, header, params, method):
    if 'get' == method:
        return requests.get(url, params)
    elif 'post' == method:
        return requests.post(url, params, header)


# 网易有道智云文本embedding服务api调用demo
# api接口:
# 1、https://openapi.youdao.com/textEmbedding/queryTextEmbeddings
# 2、https://openapi.youdao.com/textEmbedding/queryTextEmbeddingVersion
if __name__ == '__main__':
    createRequest()
