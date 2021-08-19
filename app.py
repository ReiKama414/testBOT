import os
import pandas as pd
import pymysql
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

Channel_access_token = '0HaJGyHiDk9SSaHtvwnOcVl7hAYm7CGyzgiU6/oyW9d3AKhS5zSvmNlwD/GLwuHqjfyCRcqlkggmumi1cYQ4fQfTmx6/VmtvcTTy8gpMEQhFQCcgIiUrpSs12+xEg27Bm8EaY9nIqWQNSMefO3nl2QdB04t89/1O/w1cDnyilFU='
Channel_secret = 'f0c0a2590f8ff3a22ff59c04bc62c974'
user_ID = 'Ube79062ed247c073eb883921a930cd1f'

app = Flask(__name__)

line_bot_api = LineBotApi(Channel_access_token)
handler = WebhookHandler(Channel_secret)

line_bot_api.push_message(user_ID, TextSendMessage(text='測試啟動'))

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
    message = event.message.text

    conn = pymysql.connect(
        user='testuser',
        port=3306,
        host='192.168.43.194',
        passwd='!d4150894',
        charset='utf8',
        db='sql_pintai'
    )

    sql = 'SELECT * FROM data1;'
    df = pd.read_sql(sql, conn, index_col=['id'])
    mask = df[df['keyword'].str.contains(message, na=False)]

    if '玩' in message:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='DBD'))
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=message))

    if len(mask) == 0:
        if '吃' in message:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='拉麵'))
        if '貼圖' in message:
            sticker_message = StickerSendMessage(package_id='11537',
                                                 sticker_id='52002734')
            line_bot_api.reply_message(event.reply_token, sticker_message)
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=message))
    else:
        search_ans = ''
        n = 1
        search_ans += '總共有' + str(len(mask)) + '筆搜尋結果！\n'
        for i, j, k in zip(mask['title'].items(), mask['link'].items(), mask['keyword'].items()):
            search_ans += '【' + str(n) + '】 ' + i[1] + '\n' + j[1] + '\n關鍵詞：' + k[1] + '\n'
            n += 1
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=search_ans))

    conn.close()


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
