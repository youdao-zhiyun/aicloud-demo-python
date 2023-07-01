import sys
import time

from utils.AuthV4Util import addAuthParams
from utils.WebSocketUtil import send_binary_message, init_connection_with_params

# 您的应用ID
APP_KEY = ''
# 您的应用密钥
APP_SECRET = ''

# 识别音频路径, 例windows路径：PATH = 'C:\\youdao\\media.wav'
PATH = ''


def createRequest():
    '''
    note: 将下列变量替换为需要请求的参数
    取值参考文档: https://ai.youdao.com/DOCSIRMA/html/tts/api/ssyysb/index.html
    '''
    langType = '语种'
    rate = '采样率 推荐16000'

    data = {'langType': langType, 'format': 'wav', 'channel': '1', 'version': 'v1', 'rate': rate}
    # 添加鉴权相关参数
    addAuthParams(APP_KEY, APP_SECRET, data)
    # 创建websocket连接
    ws_client = init_connection_with_params("wss://openapi.youdao.com/stream_asropenapi", data)
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

# 网易有道智云实时语音识别服务api调用demo
# api接口: wss://openapi.youdao.com/stream_asropenapi
if __name__ == '__main__':
    createRequest()
    sys.exit()
