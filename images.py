from flask import Flask
from flask import request
import json
import random

app = Flask(__name__)

Images  = [("965417/9f742cfaf8da737c9c92","Мартовский заяц"),("1540737/fe5ad9521bd078b5c625","Чеширский кот")]

@app.route('/post', methods=['POST'])
def main():
    ## Создаём ответ
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    ## Заполняем необходимую информацию
    handle_dialog(response, request.json)
    return json.dumps(response)


def handle_dialog(res,req):
    if req['request']['original_utterance']:
        ## Проверяем, есть ли содержимое
        res['response']['text'] = "Это случайная картинка"
        img, title = random.choice(Images)
        res['response']['card'] = {
            "type": "BigImage",
            "image_id": img,
            "title": title
        }
    else:
        ## Если это первое сообщение - представляемся
        res['response']['text'] = "Привет! Ты мне фразу - я тебе картинку"

if __name__ == '__main__':
    app.run()
