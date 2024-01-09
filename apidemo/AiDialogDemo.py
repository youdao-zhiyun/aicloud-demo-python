import base64
import json
import requests

from utils.AuthV3Util import returnAuthMap

# 您的应用ID
APP_KEY = ''
# 您的应用密钥
APP_SECRET = ''

def createRequest():
    # 1、 获取默认场景列表接口
    print("request get default topic: ")
    topic = getDefaultTopicHelper()
    print()

    # 2、生成场景接口
    print("request generate topic: ")
    genereate_topic_result_data = generateTopicHelper(topic=topic)
    print()

    '''
    note: 将下列变量替换为需要请求的参数
    取值参考文档：https://ai.youdao.com/DOCSIRMA/html/aigc/api/AIkyls/index.html
    '''
    requestDTO = {
        "taskId": genereate_topic_result_data["taskId"],
        "scene": genereate_topic_result_data["scene"],
        "userLevel": "0",
        "history": []
    }

    # 3、生成对话接口
    print("request generate dialog: ")
    sysWords = None
    userWords = None
    dialogIndex = 0
    while dialogIndex < 3:
        sysWords = generateDialogHelper(requestDTO, sysWords, userWords)
        if sysWords is None:
            print("generate dialog error")
            exit(0)
        print("系统：", sysWords)
        print("用户：")
        userWords = input()
        dialogIndex += 1
        print()

    # 4、生成推荐接口
    print("request generate recommendation: ")
    generateRecommendationHelper(requestDTO)
    print()

    # 5、生成报告接口
    print("request generate report: ")
    generateReportHelper(requestDTO)
    print()

def generateReportHelper(requestDTO):
    params = returnAuthMap(APP_KEY, APP_SECRET, requestDTO["taskId"])
    params["taskId"] = requestDTO["taskId"]
    params["userLevel"] = requestDTO["userLevel"]
    params["scene"] = requestDTO["scene"]
    # 添加音频示例
    requestDTO["history"][1]["voice"] = readFileAsBase64("音频路径")
    params["history"] = requestDTO["history"]
    data = json.dumps(params)
    print(data)
    print()
    header = {'Content-Type': 'application/json;charset=utf-8'}
    generate_report_result = doCall('http://openapi.youdao.com/ai_dialog/generate_report', header, data, 'post')
    print(str(generate_report_result.content, 'utf-8'))
    return str(generate_report_result.content, 'utf-8')

def generateRecommendationHelper(requestDTO):
    params = returnAuthMap(APP_KEY, APP_SECRET, requestDTO["taskId"])
    '''
    note: 将下列变量替换为需要请求的参数
    取值参考文档：https://ai.youdao.com/DOCSIRMA/html/aigc/api/AIkyls/index.html
    '''
    indexArr = ["1"]
    count = "1"
    params["taskId"] = requestDTO["taskId"]
    params["userLevel"] = requestDTO["userLevel"]
    params["scene"] = requestDTO["scene"]
    params["history"] = requestDTO["history"]
    params["indexArr"] = indexArr
    params["count"] = count
    data = json.dumps(params)
    print(data)
    print()
    header = {'Content-Type': 'application/json;charset=utf-8'}
    genereate_recommendation_result = doCall('http://openapi.youdao.com/ai_dialog/generate_recommendation', header, data, 'post')
    print(str(genereate_recommendation_result.content, 'utf-8'))
    return str(genereate_recommendation_result.content, 'utf-8')

def generateDialogHelper(requestDTO, sysWords, userWords):
    params = returnAuthMap(APP_KEY, APP_SECRET, requestDTO["taskId"])
    params["taskId"] = requestDTO["taskId"]
    params["userLevel"] = requestDTO["userLevel"]
    params["scene"] = requestDTO["scene"]
    
    if sysWords is not None or userWords is not None:
        sys = {
            "speaker":"System",
            "content":sysWords
        }
        user = {
            "speaker":"User",
            "content":userWords
        }
        requestDTO["history"].append(sys)
        requestDTO["history"].append(user)
    
    params["history"] = requestDTO["history"]
    data = json.dumps(params)
    print(data)
    print()
    header = {'Content-Type': 'application/json;charset=utf-8'}
    genereate_dialog_result = doCall('http://openapi.youdao.com/ai_dialog/generate_dialog', header, data, 'post')
    print(str(genereate_dialog_result.content, 'utf-8'))
    generate_dialog_result_json = json.loads(str(genereate_dialog_result.content, 'utf-8'))
    if(generate_dialog_result_json["code"] != "0"):
        exit(0)
    return generate_dialog_result_json["data"]["resultArr"][0]["result"][0]

def generateTopicHelper(topic):
    params = returnAuthMap(APP_KEY, APP_SECRET, topic)
    params["topic"] = topic
    data = json.dumps(params)
    print(data)
    print()
    header = {'Content-Type': 'application/json;charset=utf-8'}
    genereate_topic_result = doCall('http://openapi.youdao.com/ai_dialog/generate_topic', header, data, 'post')
    print(str(genereate_topic_result.content, 'utf-8'))
    genereate_topic_result_json = json.loads(str(genereate_topic_result.content, 'utf-8'), object_hook=decode_emoji)
    if(genereate_topic_result_json["code"] != "0"):
        exit(0)
    return genereate_topic_result_json["data"]
    
def getDefaultTopicHelper():
    q = 'topics'
    params = returnAuthMap(APP_KEY, APP_SECRET, q)
    params["q"] = q
    data = json.dumps(params)
    header = {'Content-Type': 'application/json;charset=utf-8'}
    get_default_topic_result = doCall('http://openapi.youdao.com/ai_dialog/get_default_topic', header, data, 'post')
    print(str(get_default_topic_result.content, 'utf-8'))
    get_default_topic_result_json = json.loads(str(get_default_topic_result.content, 'utf-8'))
    if(get_default_topic_result_json["code"] != "0"):
        exit(0)
    return get_default_topic_result_json["data"]["topicList"][0]["topics"][0]["enName"]

def doCall(url, header, params, method):
    if 'get' == method:
        return requests.get(url, params)
    elif 'post' == method:
        return requests.post(url, data = params, headers = header)
    
def readFileAsBase64(path):
    f = open(path, 'rb')
    data = f.read()
    return str(base64.b64encode(data), 'utf-8')
    
def decode_emoji(obj):
    if isinstance(obj, str):
        return obj.encode().decode('unicode_escape')
    return obj

# 网易有道智云AI口语老师服务api调用demo
# api接口: https://openapi.youdao.com
if __name__ == '__main__':
    createRequest()
