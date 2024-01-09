import json

import requests

from utils.AuthV3Util import addAuthParams

# 您的应用ID
APP_KEY = ''
# 您的应用密钥
APP_SECRET = ''

# 上传文档路径，例 windows 路径：PATH = "C:\\youdao\\doc.pdf"
PATH = ''


def createKB(kbName):
    data = {'q': kbName}
    addAuthParams(APP_KEY, APP_SECRET, data)
    header = {'Content-Type': 'application/json'}
    print('请求参数:' + json.dumps(data))
    res = doCall('https://openapi.youdao.com/q_anything/paas/create_kb', header, json.dumps(data), 'post')
    print(str(res.content, 'utf-8'))


def deleteKB(kbId):
    data = {'q': kbId}
    addAuthParams(APP_KEY, APP_SECRET, data)
    header = {'Content-Type': 'application/json'}
    print('请求参数:' + json.dumps(data))
    res = doCall('https://openapi.youdao.com/q_anything/paas/delete_kb', header, json.dumps(data), 'post')
    print(str(res.content, 'utf-8'))


def uploadDoc(kbId, file):
    data = {'q': kbId}
    addAuthParams(APP_KEY, APP_SECRET, data)
    res = requests.post('https://openapi.youdao.com/q_anything/paas/upload_file', data=data, files={'file': file})
    print(str(res.content, 'utf-8'))


def uploadUrl(kbId, url):
    data = {'q': kbId, 'url': url}
    addAuthParams(APP_KEY, APP_SECRET, data)
    header = {'Content-Type': 'application/json'}
    print('请求参数:' + json.dumps(data))
    res = doCall('https://openapi.youdao.com/q_anything/paas/upload_url', header, json.dumps(data), 'post')
    print(str(res.content, 'utf-8'))


def deleteFile(kbId, fileId):
    data = {'q': kbId, 'fileIds': [fileId]}
    addAuthParams(APP_KEY, APP_SECRET, data)
    header = {'Content-Type': 'application/json'}
    print('请求参数:' + json.dumps(data))
    res = doCall('https://openapi.youdao.com/q_anything/paas/delete_file', header, json.dumps(data), 'post')
    print(str(res.content, 'utf-8'))


def kbList():
    data = {'q': ''}
    addAuthParams(APP_KEY, APP_SECRET, data)
    header = {'Content-Type': 'application/json'}
    print('请求参数:' + json.dumps(data))
    res = doCall('https://openapi.youdao.com/q_anything/paas/kb_list', header, json.dumps(data), 'post')
    print(str(res.content, 'utf-8'))


def fileList(kbId):
    data = {'q': kbId}
    addAuthParams(APP_KEY, APP_SECRET, data)
    header = {'Content-Type': 'application/json'}
    print('请求参数:' + json.dumps(data))
    res = doCall('https://openapi.youdao.com/q_anything/paas/file_list', header, json.dumps(data), 'post')
    print(str(res.content, 'utf-8'))


def chat(kbId, q):
    data = {'q': q, 'kbIds': [kbId]}
    addAuthParams(APP_KEY, APP_SECRET, data)
    header = {'Content-Type': 'application/json'}
    print('请求参数:' + json.dumps(data))
    res = doCall('https://openapi.youdao.com/q_anything/paas/chat', header, json.dumps(data), 'post')
    print(str(res.content, 'utf-8'))


def chatStream(kbId, q):
    data = {'q': q, 'kbIds': [kbId]}
    addAuthParams(APP_KEY, APP_SECRET, data)
    header = {'Content-Type': 'application/json'}
    print('请求参数:' + json.dumps(data))
    res = doCall('https://openapi.youdao.com/q_anything/paas/chat_stream', header, json.dumps(data), 'post')
    print(str(res.content, 'utf-8'))


def doCall(url, header, params, method):
    if 'get' == method:
        return requests.get(url, params)
    elif 'post' == method:
        return requests.post(url, params, headers=header)


# 网易有道智云QAnything服务api调用demo
if __name__ == '__main__':
    # 将下列参数替换为需要的请求参数
    # 知识库名称
    kbName = ''
    # 知识库id
    kbId = ''
    # 上传的url地址
    url = ''
    # 文档id
    fileId = ''

    # NOTE: 1、知识库管理
    # 1.1、创建知识库
    createKB(kbName)
    # 1.2、删除知识库
    deleteKB(kbId)
    # 1.3、上传文档
    file = open(PATH, 'rb')
    uploadDoc(kbId, file)
    # 1.4、上传url资源
    uploadUrl(kbId, url)
    # 1.5、删除文档
    deleteFile(kbId, fileId)
    # 1.6、查询知识库列表
    kbList()
    # 1.7、查询文档列表
    fileList(kbId)

    # 提问问题
    q = ''

    # NOTE: 2、文档问答接口
    # 2.1、文档问答
    chat(kbId, q)
    # 2.2、文档问答(流式)
    chatStream(kbId, q)
