import requests
import json

from utils.AuthV3Util import addXiaopAuthParams

# 您的应用ID
APP_KEY = ''
# 您的应用密钥
APP_SECRET = ''


def create_suggest_params_by_id():
    """
        note: 将下列变量替换为需要请求的参数
    """
    user_id = "【公共参数】用户id，不为空串，100个字符以内"
    task_id = "【业务参数】任务id，请求对话接口的begin事件中返回"
    chat_id = "【业务参数】对话id，请求对话接口的begin事件中返回"
    return {"user_id": user_id, "task_id":task_id, "chat_id":chat_id}


def create_suggest_params():
    """
        note: 将下列变量替换为需要请求的参数
    """
    user_id = "【公共参数】用户id，不为空串，100个字符以内"
    query = "【业务参数】需要推荐问题的原始问题"
    answer = "【业务参数】原始问题的回答"
    return {"user_id": user_id, "query": query, "answer": answer}


def create_request_param_example():
    return {
        "user_id": "user_test",
        "query": "背诵静夜思",
        "answer": "床前明月光，疑是地上霜。举头望明月，低头思故乡。"
    }


def do_call():
    # 构造请求参数
    param = create_request_param_example()
    addXiaopAuthParams(APP_KEY, APP_SECRET, param)
    # 发送请求
    url = 'https://openapi.youdao.com/llmserver/plugin/suggest'
    response = requests.post(url, data=param, headers={})
    data = response.content
    print(json.loads(data))


if __name__ == '__main__':
    do_call()