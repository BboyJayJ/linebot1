from django.shortcuts import render
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse,HttpResponseBadRequest,HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

from linebot import LineBotApi, WebhookHandler,WebhookParser
from linebot.exceptions import InvalidSignatureError,LineBotApiError
from linebot.models import MessageEvent,TextSendMessage,TextMessage,ImageSendMessage
import random

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parse=WebhookParser(settings.LINE_CHANNEL_SECRET)

def index(request):
    return HttpResponse("<h1> LineBot APP </h1>")

@csrf_exempt    
def callback(request):
    if request.method=='POST':
        signature=request.META['HTTP_X_LINE_SIGNATURE']
        body=request.body.decode('utf-8')
        try:
            events=parse.parse(body,signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
        for event in events:
            if isinstance(event,MessageEvent):
                if isinstance(event.message,TextMessage):
                    message,img_url=None, None
                    text=event.message.text
                    print(text)

                    words=['早安~ 你好 今天好嗎?','天氣很不錯','今天如何呢','午餐要吃甚麼','再說一次']
                    if '台北捷運' in text:
                        message='https://www.metro.taipei/cp.aspx?n=91974F2B13D997F1'

                    elif '台中捷運' in text:
                        img_url='https://assets.piliapp.com/s3pxy/mrt_taiwan/taichung/20201112_zh.png?v=2'                       
                    elif '電影' in text:
                        message='https://movies.yahoo.com.tw/movie_intheaters.html'
                    elif '樂透' in text:
                        message=lotto()
                    elif '早安' in text:
                        message='早安你好'                       
                    else:
                         message=random.choice(words)
                
                                        
                else:  
                    message='無法解析'

                messageObject = TextSendMessage(text=message) if message is not None else \
                        ImageSendMessage(original_content_url=img_url,
                            preview_image_url=img_url)
                    
                line_bot_api.reply_message(event.reply_token, messageObject)



        return HttpResponse()
    else:
        return HttpResponseBadRequest()

def lotto():
    numbers = sorted(random.sample(range(1, 50), 6))
    result = ' '.join(map(str, numbers))
    n = random.randint(1, 50)

    return f'{result} 特別號:{n}'