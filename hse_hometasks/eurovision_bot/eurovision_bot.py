import flask
import telebot
import conf

with open ('links.txt', 'r', encoding = 'utf-8') as file:
    links = file.read().split('\n')

videos = {}

for elem in links:
    pair = elem.split('\t')
    videos[pair[0]] = pair[1]

WEBHOOK_URL_BASE = "https://{}:{}".format(conf.WEBHOOK_HOST, conf.WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/{}/".format(conf.TOKEN)

bot = telebot.TeleBot(conf.TOKEN, threaded=False)

bot.remove_webhook()

bot.set_webhook(url=WEBHOOK_URL_BASE+WEBHOOK_URL_PATH)

app = flask.Flask(__name__)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Привет. Я не умею считать длину твоего сообщения, потому что это довольно скучно. Но я умею кое-что получше.")
    bot.send_message(message.chat.id, "Я могу скидывать тебе ссылки на выступления разных стран на Евровидении-2017! Просто упомяни в своем сообщении страну, песню которой ты хочешь услышать.")
    bot.send_message(message.chat.id, "Если ты не помнишь, какие страны участвовали в этом году, набери /countries, я тебе подскажу.")
    bot.send_message(message.chat.id, "Если тебе интересно, кто победил, набери /winner")
    bot.send_message(message.chat.id, "Если хочешь посмотреть на результаты финала, набери /final")

@bot.message_handler(commands=['countries'])
def list_of_countries(message):
    bot.send_message(message.chat.id, "Вот полный список участников: Австралия, Австрия, Албания, Армения, Беларусь, Бельгия, Болгария, Великобритания, Венгрия, Германия, Греция, Грузия, Дания, Израиль, Ирландия, Исландия, Испания, Италия, Кипр, Латвия, Литва, Македония, Мальта, Молдова, Нидерланды, Норвегия, Польша, Португалия, Румыния, Сан-Марино, Сербия, Словения, Украина, Финляндия, Франция, Хорватия, Черногория, Чехия, Швейцария, Швеция, Эстония.")

@bot.message_handler(commands=['winner'])
def look_at_winner(message):
    bot.send_message(message.chat.id, "Победитель Евровидения-2017 - представитель Португалии Сальвадор Собрал!")
    bot.send_message(message.chat.id, "https://www.youtube.com/watch?v=Qotooj7ODCM")

@bot.message_handler(commands=['final'])
def send_final_results(message):
    results = open('results.jpg', 'rb')
    bot.send_photo(message.chat.id, results)

@bot.message_handler(func=lambda m: True)
def find_video(message):
    for key in videos.keys():
        if key.lower() in message.text.lower():
            bot.send_message(message.chat.id, videos[key])

@app.route('/', methods=['GET', 'HEAD'])
def index():
    return 'ok'

@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)