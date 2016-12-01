import re
import os
import json
import html

def create_thai_eng():
    os.chdir('C:/Users/Анна/Desktop/google_time/control_work/thai_pages')
    file_names = os.listdir('C:/Users/Анна/Desktop/google_time/control_work/thai_pages')
    thai_eng = {}
    
    for name in file_names:
        with open (name, 'r', encoding = 'utf-8') as file:
            f = file.read()
            words = re.findall ('<tr><td class=th><a href=.*?>(.*?)</a>.*?<td class=pos>(.*?)</td><td>(.*?)</td></tr>', f)
            for elem in words:
                if elem[1] != 'example sentence':
                    thai = elem[0]
                    eng1 = elem[2].split(';')
                    eng = eng1[0]
                    thai = clean_word(thai)
                    eng = clean_word(eng)
                    thai_eng[thai] = eng
                    
    return thai_eng

def clean_word(word):
    regTag = re.compile('<.*?>', flags=re.DOTALL)
    regScript = re.compile('<script>.*?</script>', flags=re.DOTALL)
    regComment = re.compile('<!--.*?-->', flags=re.DOTALL)

    clean_word = regTag.sub("", word)
    clean_word = regScript.sub("", clean_word)
    clean_word = regComment.sub("", clean_word)
    clean_word = re.sub('\[.*?\]', '', clean_word)
    clean_word = re.sub('\\"', '', clean_word)
    clean_word = clean_word.strip(' \';:?!"/,.')

    clean_word = html.unescape(clean_word)
    
    return clean_word

def create_json (dictionary, string):
    os.chdir('C:/Users/Анна/Desktop/google_time/control_work/')
    data_dict = json.dumps(dictionary)

    with open (string, 'w', encoding = 'utf-8') as file:
        file.writelines (data_dict)

def create_eng_thai (thai_eng):
    eng_thai = dict()

    for key in thai_eng:
        value = thai_eng[key]
        if value not in eng_thai:
            eng_thai[value] = [key]
        else:
            eng_thai[value].append(key)

    return eng_thai
    
def main():
    thai_eng = create_thai_eng()
    create_json (thai_eng, 'thai_eng.json')
    eng_thai = create_eng_thai (thai_eng)
    create_json (eng_thai, 'eng_thai.json')

if __name__ == '__main__':
    main()
