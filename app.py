from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import os

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('0HaJGyHiDk9SSaHtvwnOcVl7hAYm7CGyzgiU6/oyW9d3AKhS5zSvmNlwD/GLwuHqjfyCRcqlkggmumi1cYQ4fQfTmx6/VmtvcTTy8gpMEQhFQCcgIiUrpSs12+xEg27Bm8EaY9nIqWQNSMefO3nl2QdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('f0c0a2590f8ff3a22ff59c04bc62c974')

line_bot_api.push_message('Ube79062ed247c073eb883921a930cd1f', TextSendMessage(text='你可以開始了'))

# KAMAKUKU !d4150894

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


# 訊息傳遞區塊
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token, message)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)