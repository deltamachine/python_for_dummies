import flask
import telebot
import urllib.request
import urllib.parse
import re
import os


TOKEN = os.environ["TOKEN"]
bot = telebot.TeleBot(TOKEN, threaded=False)
bot.remove_webhook()
bot.set_webhook(url="https://yiddish-bot.herokuapp.com/bot")

app = flask.Flask(__name__)


def parse_results(link): #чистит страницу с результатами
    req = urllib.request.Request(link)

    with urllib.request.urlopen(req) as f:
        response = f.read().decode('utf-8')
    
    results = response.split('<br />\r\n<br />\r\n<br />\r\n<br />')

    for i in range (len(results)):
        results[i] = re.sub('<.*?>', '', results[i])

    return results


def ask_corpus(word, values): #задает корпусу запрос и получает выдачу
    url = 'http://www.web-corpora.net/YNC/search/results.php'

    data = urllib.parse.urlencode(values).encode("utf-8")
    req = urllib.request.Request(url)

    with urllib.request.urlopen(req, data=data) as f:
        response = f.read().decode('utf-8')

    m = re.search('<script>self.location.href.*?(results.*?interface_language=ru).*?</script>', response)

    if m != None:
        imp_part = m.group(1)
        link = 'http://web-corpora.net/YNC/search/' + imp_part

        with urllib.request.urlopen(link) as f:
            html = f.read().decode('utf-8')

        answer = re.search('Найдено:.*?документов', html).group()
        answer = re.sub ('<.*?>', '', answer)
        answer = re.sub (':', '', answer)
        answer = re.sub ('  ', ' ', answer)
        answer = 'Объем корпуса - около 4 миллионов словоупотреблений. ' + answer

        print_link = re.search ('<a onClick=.*?(contexts.*?interface_language=ru&print=1&page=1).*?;', html).group(1)
        print_link = 'http://web-corpora.net/YNC/search/' + print_link

        results = parse_results(print_link)

        print_link = 'Ссылка на версию для печати (первая страница выдачи): ' + print_link

    else:
        answer = 'Извините, кажется, по вашему запросу ничего не нашлось'
        print_link = 'Попробуйте что-нибудь еще?'
        results = ['Я пытался :(']

    return answer, print_link, results


def check_tags(tag_params): #проверяет, нет ли ошибок во введенных тегах
    tags = ['N', 'A', 'V', 'ADV', 'NUM', 'PRON', 'PREP', 'POST', 'CONJ', 'PART', 'INTJ', 'nom', 'gen', 'dat', 'acc', 'sg', 'pl', \
    'm', 'f', 'n', 'short', 'inf', 'ptcp', 'pres', 'res', 'imp', '1', '2', '3']

    tag_params = re.sub('\(', '', tag_params)
    tag_params = re.sub('\)', '', tag_params)
    tag_params = re.sub('\|', ' ', tag_params)
    tag_params = re.sub(',', ' ', tag_params)

    tag_params = tag_params.split()
    answer = []

    for elem in tag_params:
        if elem not in tags:
            answer.append(elem)

    return answer


@bot.message_handler(commands=['start']) #приветствует пользователя
def send_welcome(message):
    bot.send_message(message.chat.id, "Шолэм алэйхем! Я бот, который умеет работать с корпусом языка идиш.")
    bot.send_message(message.chat.id, "Я умею искать как точные вхождения слов, так и словоформы с заданными грамматическими параметрами. А еще вы можете получать как выдачу, использующую традиционный алфавит, так и выдачу, использующую латиницу. При вводе слова тоже можно использовать как латиницу, так и традиционный алфавит")
    bot.send_message(message.chat.id, "Для латиницы используйте параметр translit1, для традиционного алфавита - yiddish")
    bot.send_message(message.chat.id,'Если вы хотите найти документы с точным вхождением слова, наберите "token способ_выдачи слово" - например, "token yiddish הי"')
    bot.send_message(message.chat.id, 'Если же вы хотите найти документы с вхождением словоформы с заданными грамматическими параметрами, наберите "wordform способ_выдачи слово набор_тегов" - например, "wordform translit1 shvarts A,nom,sg"')
    bot.send_message(message.chat.id, "Если вы не знаете или не помните, как выглядят теги, наберите /helptable")
    bot.send_message(message.chat.id, "Если вам нужна инструкция по вводу тегов, наберите /helptags")

@bot.message_handler(commands=['helptable']) #посылает таблицу с тегами
    tagtable= open('tagtable.png', 'rb')
    bot.send_message(message.chat.id, 'Я создал для вас справочную таблицу со всеми тегами, которые вы можете использовать в запросе. Вот она:')
    bot.send_photo(message.chat.id, tagtable)

@bot.message_handler(commands=['helptags']) #посылает информацию о вводе тегов
def help_user_with_tags(message):
    bot.send_message(message.chat.id, 'Немного о правилах ввода тегов:')
    bot.send_message(message.chat.id, '1. Теги из одной категории заключаются в скобки и разделяются знаком |, например (sg|pl)')
    bot.send_message(message.chat.id, 'Важное исключение №1: так как в категории "Форма прилагательного" только один тег, заключать в скобки его не надо')
    bot.send_message(message.chat.id, 'Важное исключение №2: рода выбираются следующим образом - m, f, n, (m|f), "m,n", "f,n", (m|f),n. Я не знаю, что это у разработчиков за странный баг со средним родом, правда.')
    bot.send_message(message.chat.id, '2. Группы тегов или одиночные теги из разных категорий разделяются запятыми. Примеры запросов:')
    bot.send_message(message.chat.id, 'N,nom,sg')
    bot.send_message(message.chat.id, 'N,(nom|dat),(sg|pl)')
    bot.send_message(message.chat.id, 'A,sg,(m|f),n,short')
    bot.send_message(message.chat.id, 'Надеюсь, после этой небольшой инструкции вам стало понятнее, как со мной работать :)')

@bot.message_handler(func=lambda m: True)
def find_params(message): #принимает от юзера параметры для поиска и выдаёт результаты
    word = message.text.split()

    if word[0].lower() == 'token':
        values = {'fullsearch': word[2], 'occurences_per_page': '10', 'interface_language': 'ru',
        'sentences_per_enlarged_occurrence': '1', 'contexts_layout': 'basic', 'show_gram_info': '1',
        'contexts_output_language': word[1].lower(), 'sort_by': '', 'search_language': 'yiddish', 'selected_words_percent': '1',
        'subcorpus': '', 'subcorpus_query': ''}
        
        checker = 0

    if word[0].lower() == 'wordform':
        check_answer = check_tags(word[3])
        
        if check_answer != []:
            check_answer = 'Кажется, вы опечатались при вводе тегов. Поищите ошибку здесь: ' + ', '.join(check_answer)
            checker = 1
            
            bot.send_message(message.chat.id, check_answer)
        else:
            values = {'lex1': word[2], 'gr1': word[3], 'occurences_per_page': '10', 'interface_language': 'ru',
            'sentences_per_enlarged_occurrence': '1', 'contexts_layout': 'basic', 'show_gram_info': '1',
            'contexts_output_language': word[1].lower(), 'sort_by': '', 'search_language': 'yiddish', 'selected_words_percent': '1',
            'subcorpus': '', 'subcorpus_query': ''}

            checker = 0

    if checker == 0:
        answer, print_link, results = ask_corpus(word, values)

        bot.send_message(message.chat.id, answer)
        
        if len(results) > 1:
            for i in range (0, 10):
                bot.send_message(message.chat.id, results[i])
        else:
            bot.send_message(message.chat.id, results[0])

        bot.send_message(message.chat.id, print_link)


@app.route("/", methods=['GET', 'HEAD'])
def index():
    return 'ok'


@app.route("/bot", methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)
    
if __name__ == '__main__':
    import os
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
