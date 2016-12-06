import os
import re
import html
import urllib.request

def request (link):
    req = urllib.request.Request (link)
    with urllib.request.urlopen(req) as response: 
       html = response.read().decode('utf-8')
    return html

def clean_article (text):
    regTag = re.compile('<.*?>', flags=re.DOTALL)
    regScript = re.compile('<script>.*?</script>', flags=re.DOTALL)
    regComment = re.compile('<!--.*?-->', flags=re.DOTALL)
    regSpace = re.compile('\s{2,}', flags = re.DOTALL)

    clean_text = regTag.sub("", text)
    clean_text = regSpace.sub("\n", clean_text)
    clean_text = regScript.sub("", clean_text)
    clean_text = regComment.sub("", clean_text)

    clean_text = html.unescape(clean_text)
    
    return clean_text

def create_array (string):
    string = re.sub ('\.', ' ', string)
    string = re.sub (':', ' ', string)
    string = re.sub ('!', ' ', string)
    array = string.split()
    
    for i in range (len(array)):
        array[i] = array[i].strip('!?":;-%,()[]«»')
        array[i] = array[i].lower()
        i+=1
    return array   

def create_little_array (array):
    little_array = []
    for i in range (len(array)):
        k = array.count(array[i])
        if k >1:
            little_array.append(array[i])
    return little_array     

def bunch_of_sets(news_dict):
    sets = []

    for key, value in news_dict.items():
        html = request (key)
        html = re.sub ('\n', '', html)
        m = re.search (value, html)
        news = m.group(1)

        if key == key[1]:
            news = re.sub ('<div class="relatedArticles">(.*?)</div>', '', news)

        news = clean_article (news)

        if key == key[0]:
            news = re.sub ('03.*?02', '', news)
            news = re.sub ('Д.*?ru', '', news)

        array = create_array(news)
        little_array = create_little_array (array)

        bset_key = set (array)
        lset_key = set (little_array)

        sets.append (bset_key)
        sets.append (lset_key)

    return sets

def save_file (array, name):
    with open (name, 'w', encoding = 'utf-8') as file:
        for word in array:
            file.write (word)
            file.write ('\n')

def main():
    with open ('links.txt', 'r', encoding = 'utf-8') as file:
        f = file.read()
        f = f.split('\n')

    news_dict = {f[i]: f[i+1] for i in range (0, len(f), 2)}
    little_set = []

    sets = bunch_of_sets (news_dict)

    intersection = sets[0] & sets[2] & sets[4] & sets[6]

    little_array = sets[1] | sets[3] | sets[5] | sets[7]

    a = sets[0] ^ sets[2]
    b = sets[4] ^ sets[6]
    difference = a ^ b
    
    intersection = list (intersection)
    difference = list (difference)

    for elem in difference:
        if elem in little_array:
            little_set.append(elem)

    intersection.sort()
    little_set.sort()

    save_file (intersection, 'intersection.txt')
    save_file (little_set, 'difference.txt')

if __name__ == '__main__':
    main()
