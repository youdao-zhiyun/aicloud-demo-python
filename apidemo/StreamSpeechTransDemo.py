import sys
import time

from utils.AuthV4Util import addAuthParams
from utils.WebSocketUtil import send_binary_message, init_connection_with_params

# 您的应用ID
APP_KEY = ''
# 您的应用密钥
APP_SECRET = ''

# 识别音频路径, 例windows路径：PATH = 'C:\\tts\\media.wav'
PATH = ''


def createRequest():
    '''
    note: 将下列变量替换为需要请求的参数
    取值参考文档: https://ai.youdao.com/DOCSIRMA/html/%E5%AE%9E%E6%97%B6%E8%AF%AD%E9%9F%B3%E7%BF%BB%E8%AF%91/API%E6%96%87%E6%A1%A3/%E5%AE%9E%E6%97%B6%E8%AF%AD%E9%9F%B3%E7%BF%BB%E8%AF%91%E6%9C%8D%E5%8A%A1/%E5%AE%9E%E6%97%B6%E8%AF%AD%E9%9F%B3%E7%BF%BB%E8%AF%91%E6%9C%8D%E5%8A%A1-API%E6%96%87%E6%A1%A3.html
    '''
    lang_from = '源语言语种'
    lang_to = '目标语言语种'
    rate = '音频数据采样率, 推荐16000'
    format = '音频格式, 推荐wav'

    data = {'from': lang_from, 'to': lang_to, 'format': format, 'channel': '1', 'version': 'v1', 'rate': rate}
    # 添加鉴权相关参数
    addAuthParams(APP_KEY, APP_SECRET, data)
    # 创建websocket连接
    ws_client = init_connection_with_params("wss://openapi.youdao.com/stream_speech_trans", data)
    # 发送流式数据
    send_data(PATH, 6400, ws_client)


def send_data(path, step, ws_client):
    while not ws_client.return_is_connect():
        time.sleep(0.1)
    file = open(path, 'rb')
    while True:
        try:
            data = file.read(step)
            if not data:
                break
            send_binary_message(ws_client.ws, data)
            time.sleep(0.2)
        except Exception as e:
            print(e)
            sys.exit()

    end_message = "{\"end\": \"true\"}"
    send_binary_message(ws_client.ws, end_message)

# 网易有道智云流式语音翻译服务api调用demo
# api接口: wss://openapi.youdao.com/stream_speech_trans
if __name__ == '__main__':
    createRequest()
    sys.exit()
