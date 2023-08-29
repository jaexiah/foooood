from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)

from linebot.models import *

app = Flask(__name__)

line_bot_api = LineBotApi('7fcG7R7hL+P8ITrwd1xcK0etcWwYgY0K1S9vQtW3jJhooCTOIaP8Xqgqt6yDjVR+W1MGyUSE2mpT7RUrLkQbV5qPCKhNyUBw0z+iIk8PmPtVJr+AE6q3ojCMVOcJ/vYdCujgXNx7DzDmnikkVWeVCQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('91e290021d70358510995f262aaa0121')


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
# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    #event有什麼資料？詳見補充

    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text='Hi! Welcome to LSTORE.'))
    
if __name__ == "__main__":
    app.run()