import re
import os

def read_text():
    with open ('try_it.txt', 'r', encoding = 'utf-8') as file:
        f = file.read()

    clean_words = []

    words = f.split()
    
    for i in range (len(words)):
        words[i] = words[i].strip('«»\.,?!:;"()%-')
        words[i] = words[i].lower()
        m = re.search('[0-9]', words[i])
        if words[i] != '—' and words[i] != '' and m == None:
            if '-' in words[i]:
                half = words[i].split('-')
                clean_words+=half
            else:
                clean_words.append(words[i])

    clean_words = set(clean_words)

    with open ('words.txt', 'w', encoding = 'utf-8') as file:
        for word in clean_words:
            file.write('\n')
            file.write(word)

    return clean_words

def create_lemma(clean_words):
    os.system ('mystem.exe ' + 'words.txt' + ' ' + 'mystem-words.txt' + ' -cnid --format text')

    with open ('mystem-words.txt', 'r', encoding = 'utf-8') as file:
        f = file.read()

    lemmas = {}

    for word in clean_words:
        re_string = '\n' + word + '({.*?})'
        m = re.search (re_string, f)
        lemmas[word] = m.group(1)

    return lemmas

def create_inserts(lemmas):
    k = 0
    with open ('sql.txt', 'w', encoding='utf-8') as file:
        for key, value in lemmas.items():
            k +=1
            command = 'INSERT INTO mystem_wordforms (id, wordform, lemma) VALUES (\'' + str(k) + '\', \'' + key + '\', \'' + value + '\');'
            file.write (command)
            file.write ('\n')
        
def main():
    clean_words = read_text()
    lemmas = create_lemma(clean_words)
    create_inserts(lemmas)
    
if __name__ == '__main__':
    main()
