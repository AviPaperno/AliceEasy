from flask import Flask
from flask import request
import json
import random
import copy

app = Flask(__name__)

## Общий список слов
WORDS = {"а": ["анафема","аллегория","актёр","арка","аптека"],
         "б":["блюдо","борьба","брак"],
         "д":["дружба",'детство']
         }

## Словарь для хранения информации о пользователях
## Ключём будут их идентификаторы, а в качестве значений - будет список вида [[НЕИСПОЛЬЗОВАННЫЕ СЛОВА], [ИСПОЛЬЗОВАННЫЕ СЛОВА]]
USERS = {}

@app.route('/post', methods=['POST'])
def main():
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    handle_dialog(response, request.json)
    return json.dumps(response)

def random_word(user_id):
    '''
    Функция возвращает случайное слово из слов для заданного пользователя, и перемещает
    его из списка неиспользованных слов, в список использованных
    :param user_id:
    :return:
    '''
    global USERS
    all = []
    L_WORDS = USERS[user_id][0]
    for i in L_WORDS.values():
        all += i
    word = random.choice(all)
    L_WORDS[word[0]].remove(word)
    return word

def get_next_word(word,user_id):
    '''
    Функция возвращает следующее слово для заданного пользователя и текущего слова
    :param word:
    :param user_id:
    :return:
    '''
    global USERS
    L_WORDS = USERS[user_id][0]
    L_USED = USERS[user_id][1]
    try:
        while True:
            letter = word[-1]
            my_word = random.choice(L_WORDS[letter])
            L_WORDS[letter].remove(my_word)
            if my_word not in L_USED:
                break
        return my_word
    except:
        return False

def handle_dialog(res, req):
    global USERS
    user_id = req['session']['user_id']
    if req['session']['new']:
        # Если до этого пользователь не играл - нужно его "зарегистрировать в системе" и отправить первое слово
        USERS[user_id] = [copy.deepcopy(WORDS)]
        USERS[user_id].append([random_word(user_id)])
        res['response']['text'] = USERS[user_id][1][-1]
    else:
        L_USED = USERS[user_id][1]
        word = req['request']['nlu']['tokens'][0]
        if word[0] == L_USED[-1][-1]:
            # Если пользователь указал слово правильно(начинается на последнюю букву предыдущего), то генерируем следующее слово
            if word not in L_USED:
                # Если это слово не использовалось
                L_USED.append(word)
                next_w = get_next_word(word,user_id)
                if next_w:
                    res['response']['text'] = next_w
                    L_USED.append(next_w)
                else:
                    # Слова могут и закончится....
                    res['response']['text'] = "У меня закончились слова..."
            else:
                # Если слово уже было использовано человеком или Алисой
                res['response']['text'] = "Слово {} уже было".format(word)
        else:
            # Если пользователь попытался считерить и указать случайное слово
            res['response']['text'] = "Слово должно начинаться на последнюю букву моего. Попробуй опять"


if __name__ == '__main__':
    app.run()
