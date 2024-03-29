import os
from flask import Flask, request, abort
from flask_sqlalchemy import SQLAlchemy
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

db = SQLAlchemy()
app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://user001:!v31542870@192.168.1.101:3306/sql_pintai"

Channel_access_token = '0HaJGyHiDk9SSaHtvwnOcVl7hAYm7CGyzgiU6/oyW9d3AKhS5zSvmNlwD/GLwuHqjfyCRcqlkggmumi1cYQ4fQfTmx6/VmtvcTTy8gpMEQhFQCcgIiUrpSs12+xEg27Bm8EaY9nIqWQNSMefO3nl2QdB04t89/1O/w1cDnyilFU='
Channel_secret = 'f0c0a2590f8ff3a22ff59c04bc62c974'
user_ID = 'Ube79062ed247c073eb883921a930cd1f'

line_bot_api = LineBotApi(Channel_access_token)
handler = WebhookHandler(Channel_secret)

db.init_app(app)
line_bot_api.push_message(user_ID, TextSendMessage(text='測試啟動'))
'''
for i in range(5, 0, -1):
    line_bot_api.push_message(user_ID, TextSendMessage(text='倒數' + str(i)))
    time.sleep(1)
'''

# KAMAKUKU !v31542870

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value: 驗證訊息來源
    signature = request.headers['X-Line-Signature']

    # get request body as text: 讀取訊息內容
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
    sql = 'select * from data1'
    message = event.message.text

    query_data = db.engine.execute(sql)
    for data_ in query_data:
        if message in data_[3]:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=data_[1]))
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=message))
    '''
    if '吃' in message:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='拉麵'))
    elif '貼圖' in message:
        sticker_message = StickerSendMessage(package_id='11537', sticker_id='52002734')
        line_bot_api.reply_message(event.reply_token, sticker_message)
    elif '玩' in message:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='DBD'))
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=message))
    '''

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

'''
Procfile：heroku 執行命令，web: {語言} {檔案}，語言為 python，要自動執行的檔案為 app.py，因此我們改成 web: python app.py。
requirements.txt：列出所有用到的套件，heroku 會依據這份文件來安裝需要套件
    reply_message(reply_token, 訊息物件)
    push_message(push_token, 訊息物件)

【Line Bot申請與串接】 (https://www.youtube.com/watch?v=7roDWI0_YMo)
如何 使用flask 連結 MySQL (https://www.maxlist.xyz/2019/11/10/flask-sqlalchemy-setting/)
'''
