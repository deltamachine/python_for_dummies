import urllib.request
import re

def news_titles():
    req = urllib.request.Request ('http://www.evening-kazan.ru/')
    with urllib.request.urlopen(req) as response: #NB: response ведет себя как файл
       html = response.read().decode('utf-8')
    
    regTag = re.compile('<.*?>', flags = re.DOTALL) #находит теги
    regSpace = re.compile('\s{2,}', flags = re.DOTALL) #находит два и больше пробела подряд

    titles = re.findall ('<span class="field-content"><a href="/articles/.*?[а-я].*?</a></span>', html)
    mini_titles = re.findall ('<a href="/news/.*?</a>', html)

    clean_titles = []

    results = titles + mini_titles
    
    for t in results:
        clean_t = regSpace.sub("", t)
        clean_t = regTag.sub("", clean_t) + '\n'
        if clean_t != '\n': #убирает случайные раздражающие пустые строки
            clean_titles.append(clean_t)

    with open ('titles_evening_kazan.txt', 'w', encoding = 'utf-8') as file:
        file.writelines (clean_titles)

def main():
    val = news_titles()

if __name__ == '__main__':
    main()
