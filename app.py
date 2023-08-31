from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)

from linebot.models import *
from models.database import db_session, init_db
from models.user import Users
from models.product import Products

app = Flask(__name__)

def get_or_create_user(user_id):
    user=db_session.query(Users).filter_by(id=user_id).first()
    if not user:
        profile=line_bot_api.get_profile(user_id)
        user=Users(id=user_id,nick_name=profile.display_name,image_url=profile.picture_url)
        db_session.add(user)
        db_session.commit()

    return user

line_bot_api = LineBotApi('7fcG7R7hL+P8ITrwd1xcK0etcWwYgY0K1S9vQtW3jJhooCTOIaP8Xqgqt6yDjVR+W1MGyUSE2mpT7RUrLkQbV5qPCKhNyUBw0z+iIk8PmPtVJr+AE6q3ojCMVOcJ/vYdCujgXNx7DzDmnikkVWeVCQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('91e290021d70358510995f262aaa0121')


# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'
# 處理訊息

def about_us_event(event):
    emoji = [
            {
                "index": 0,
                "productId": "5ac21184040ab15980c9b43a",
                "emojiId": "225"
            },
            {
                "index": 17,
                "productId": "5ac21184040ab15980c9b43a",
                "emojiId": "225"
            }
        ]
    text_message = TextSendMessage(text='''$ Master RenderP $
Hello! 您好，歡迎您成為 Master RenderP 的好友！

我是Master 支付小幫手 

-這裡有商城，還可以購物喔~
-直接點選下方【圖中】選單功能

-期待您的光臨！''', emojis=emoji)

    sticker_message = StickerSendMessage(
        package_id='8522',
        sticker_id='16581271'
    )
    line_bot_api.reply_message(
        event.reply_token,
        [text_message, sticker_message])

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    get_or_create_user(event.source.user_id)
    profile = line_bot_api.get_profile(event.source.user_id)
    uid = profile.user_id
    message_text = str(event.message.text).lower()

    if message_text == "使用說明":
        about_us_event(event)

    elif message_text == "我想訂購商品":
        message=Products.list_all()
    if message:
        line_bot_api.reply_message(
            event.reply_token,message
        )

    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text='Hi! Welcome to LSTORE.'))

#初始化產品資訊
@app.before_first_request
def init_products():
    # init db
    result = init_db()#先判斷資料庫有沒有建立，如果還沒建立就會進行下面的動作初始化產品
    if result:
        init_data = [Products(name='Coffee',
                              product_image_url='https://i.imgur.com/DKzbk3l.jpg',
                              price=150,
                              description='nascetur ridiculus mus. Donec quam felis, ultricies'),
                     Products(name='Tea',
                              product_image_url='https://i.imgur.com/PRTxyhq.jpg',
                              price=120,
                              description='adipiscing elit. Aenean commodo ligula eget dolor'),
                     Products(name='Cake',
                              price=180,
                              product_image_url='https://i.imgur.com/PRm22i8.jpg',
                              description='Aenean massa. Cum sociis natoque penatibus')]
        db_session.bulk_save_objects(init_data)#透過這個方法一次儲存list中的產品
        db_session.commit()#最後commit()才會存進資料庫
        #記得要from models.product import Products在app.py

if __name__ == "__main__":
    init_products()
    app.run()

