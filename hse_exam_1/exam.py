import os
import re

def reading (file_name):
    with open (file_name, 'r', encoding = 'utf-8') as file:
        f = file.read()
    return f

def task_1():
    f = reading('adyghe-unparsed-words.txt')
    page = reading('wp_category_politics.html')

    words = f.split('\n')
    news_words = []

    for word in words:
        if word in page:
            news_words.append (word)
            
    news_words = set(news_words)

    with open ('wordlist.txt', 'w', encoding = 'utf-8') as file:
        for word in news_words:
            if word != '':
                file.write(word)
                file.write('\n')

    return words

def task_2():
    f = reading('adyghe-unparsed-words.txt')

    with open ('adyghe-unparsed-words.txt', 'w', encoding = 'utf-8') as file:
        f = re.sub ('ӏ', 'л', f)
        file.write(f)

    os.system ('mystem.exe ' + 'adyghe-unparsed-words.txt' + ' ' + 'mystem-adyghe-unparsed-words.txt' + ' -cnid --format text')

    f = reading('mystem-adyghe-unparsed-words.txt')
    
    raw_nouns = re.findall ('{[а-я]+=S.*?}', f)
    rus_nouns = []
    dict_rus_nouns = {}

    for noun in raw_nouns:
        if 'им,ед' in noun and 'сокр' not in noun: #убираю всевозможные сокращения, потому что попадает много мусора
            m = re.search ('{([а-я]+)=', noun)
            rus_nouns.append(m.group(1))

    rus_nouns = set(rus_nouns)

    with open ('rus_nouns.txt', 'w', encoding = 'utf-8') as file:
        for noun in rus_nouns:
            file.write(noun)
            file.write('\n')
            
            re_string = '{' + noun + '=.*?}'
            dict_rus_nouns[noun] = set(re.findall(re_string, f))

    return dict_rus_nouns
            
def task_3 (dict_rus_nouns):
    with open ('sql.txt', 'w', encoding='utf-8') as file:
        for key in dict_rus_nouns.keys():
            for lemma in dict_rus_nouns[key]:
                command = 'INSERT INTO rus_words (wordform, lemma) VALUES (\'' + key + '\', \'' + lemma + '\');'
                file.write (command)
                file.write ('\n')

def main():
    task_1()
    dict_rus_nouns = task_2()
    task_3(dict_rus_nouns)

if __name__ == '__main__':
    main()
