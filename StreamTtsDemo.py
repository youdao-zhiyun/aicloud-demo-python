import sys
import time

from utils.AuthV4Util import addAuthParams
from utils.WebSocketUtil import send_binary_message, init_connection_with_params, send_text_message

# 您的应用ID
APP_KEY = ''
# 您的应用密钥
APP_SECRET = ''

# 语音合成文本
TEXT = '语音合成文本'


def createRequest():
    '''
    note: 将下列变量替换为需要请求的参数
    '''
    lang_type = '语言类型'
    format = '音频格式'
    voice = '发言人'
    volume = '音量, 取值0.1-5'
    speed = '语速, 取值0.5-2'
    rate = '音频数据采样率'

    data = {'langType': lang_type, 'format': format, 'voice': voice, 'volume': volume, 'speed': speed, 'rate': rate}
    # 添加鉴权相关参数
    addAuthParams(APP_KEY, APP_SECRET, data)
    # 创建websocket连接
    ws_client = init_connection_with_params("wss://openapi.youdao.com/stream_tts", data)
    # 发送流式数据
    send_data(ws_client)


def send_data(ws_client):
    while not ws_client.return_is_connect():
        time.sleep(0.1)
    text_message = "{{\"text\":\"{text}\"}}".format(text=TEXT)
    # 发送合成文本
    send_text_message(ws_client.ws, text_message)
    end_message = "{\"end\": \"true\"}"
    # 发送{"end":"true"}标识
    send_binary_message(ws_client.ws, end_message)


# 网易有道智云流式语音合成服务api调用demo
# api接口: wss://openapi.youdao.com/stream_tts
if __name__ == '__main__':
    createRequest()
    sys.exit()
