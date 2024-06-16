import requests
from sseclient import SSEClient

from utils.AuthV3Util import addXiaopAuthParams

# 您的应用ID
APP_KEY = ''
# 您的应用密钥
APP_SECRET = ''


def create_first_chat_params():
    """
        note: 将下列变量替换为需要请求的参数
    """
    user_id = "【公共参数】用户id，不为空串，100个字符以内"
    task_name = "【业务参数】任务名称，最多20个字符，首轮对话创建任务使用，为空时系统生成。"
    """
        【业务参数】输入内容，格式为chat_item的列表（目前只支持一个chat_item），chat_item包含两个字段：
         一、参数说明
         type：输入类型枚举【text、image、image_url】
         content：输入内容，text文本/image图片ocr识别的结果有 token 4096 长度限制
         
         二、type详细说明
         text：文本输入UTF-8
         当 type = text 时，chat_info = [{"type":"text","content":"文本输入内容"}]
         
         image：图片base64编码：智云OCR支持的图片格式：支持27种语言的自动识别！支持图片格式：.bmp、.jpg、.png，图片大小Base64后≤2M
         当 type = image 时，chat_info = [{"type":"image","content":"图片base64编码"}]
         
         image_url：整张图片的URL：智云OCR支持的图片格式：支持27种语言的自动识别！支持图片格式：.bmp、.jpg、.png，图片大小Base64后≤2M
         当 type = image_url 时，chat_info = [{"type":"image_url","content":"图片的URL链接（需要公网能访问下载）"}]
    """
    chat_info = "【业务参数】对话内容"
    template_id = "【业务参数】prompt模版id，可为空，取值与业务相关，请和开发人员联系"
    """
         sse流固定返回begin、message、end、error事件。对于其他想要的事件，需要调用方主动传递此参数订阅，多个订阅事件传值以英文逗号分隔，默认是空-无事件订阅。
         可以订阅的事件：
            query_suggestion :插件能力，订阅才执行——猜你想问
    """
    subscribe = "【业务参数】订阅事件"
    return {'user_id': user_id, 'task_name': task_name, 'chat_info': chat_info, 'template_id': template_id,
            'subscribe': subscribe}


def create_next_chat_params():
    """
        note: 将下列变量替换为需要请求的参数
    """
    user_id = "【公共参数】用户id，不为空串，100个字符以内"
    task_id = "【业务参数】任务id，用来标识用户一次会话session（关联一组对话历史），取接口返回的返回值"
    parent_chat_id = "【业务参数】父对话id，用来标识唯一输入或输出，非首轮对话以接口返回的上一次对话为准"
    """
        【业务参数】输入内容，格式为chat_item的列表（目前只支持一个chat_item），chat_item包含两个字段：
         一、参数说明
         type：输入类型枚举【text、image、image_url】
         content：输入内容，text文本/image图片ocr识别的结果有 token 4096 长度限制

         二、type详细说明
         text：文本输入UTF-8
         当 type = text 时，chat_info = [{"type":"text","content":"文本输入内容"}]

         image：图片base64编码：智云OCR支持的图片格式：支持27种语言的自动识别！支持图片格式：.bmp、.jpg、.png，图片大小Base64后≤2M
         当 type = image 时，chat_info = [{"type":"image","content":"图片base64编码"}]

         image_url：整张图片的URL：智云OCR支持的图片格式：支持27种语言的自动识别！支持图片格式：.bmp、.jpg、.png，图片大小Base64后≤2M
         当 type = image_url 时，chat_info = [{"type":"image_url","content":"图片的URL链接（需要公网能访问下载）"}]
    """
    chat_info = "【业务参数】对话内容"
    template_id = "【业务参数】prompt模版id，可为空，取值与业务相关，请和开发人员联系"
    """
         sse流固定返回begin、message、end、error事件。对于其他想要的事件，需要调用方主动传递此参数订阅，多个订阅事件传值以英文逗号分隔，默认是空-无事件订阅。
         可以订阅的事件：
            query_suggestion :插件能力，订阅才执行——猜你想问
    """
    subscribe = "【业务参数】订阅事件"
    return {'user_id': user_id, 'task_id': task_id, 'parent_chat_id': parent_chat_id, 'chat_info': chat_info,
            'template_id': template_id, 'subscribe': subscribe}


def create_request_param_example():
    user_id = 'user_test'
    task_name = '你好'
    chat_info = "[{\"type\":\"text\",\"content\":\"你好\"}]"
    return {'user_id': user_id, 'task_name': task_name, 'chat_info': chat_info}


def do_call():
    # 构造请求参数
    params = create_request_param_example()
    addXiaopAuthParams(APP_KEY, APP_SECRET, params)
    # 发送请求
    url = 'https://openapi.youdao.com/llmserver/ai/teacher/dialogue/chat'
    header = {'Content-Type': 'application/x-www-form-urlencoded', 'Accept': 'text/event-stream'}
    response = requests.post(url, data=params, stream=True, headers=header)

    # 处理 SSE 事件流
    client = SSEClient(response)
    for event in client.events():
        print(event.event)
        print(event.data)


# 网易有道智云大模型翻译服务api调用demo
# api接口: https://openapi.youdao.com/llmserver/ai/teacher/dialogue/chat
if __name__ == '__main__':
    do_call()
