#rules of tanka: line1 - 5 syllables, line2 - 7, line3 - 5, line4 and line5 - 7

import random

def cleaning (text):
    words = []
    for line in text.readlines():
        line = line.split()
        for word in line:
            words.append(word)
            
    for i in range (len(words)):
        words[i] = words[i].strip('.,%!"()?:;')
        words[i] = words[i].lower()
    return words


def number_of_syllables (line):
    k = 0
    for i in range (len(line)):
        if line[i] in 'ёуеыаоэяию':
            k+=1
    return k

def random_word (link):
    with open (link, 'r', encoding = 'utf-8') as text:
        words = cleaning (text)
    word = random.choice(words)
    return word
    

def first_line (): #"noun Nom + verb Praes"
    number = 0
    while number != 5:
        noun = random_word ('lexicon/nouns_Nom.txt')
        verb = random_word ('lexicon/verbs_Praes.txt')
        line = noun + ' ' + verb + '.'
        number = number_of_syllables (line)
    return line

def second_line (): #"noun Nom + noun Gen + noun Nom"
    number = 0
    while number != 7:
        noun_nom = random_word ('lexicon/nouns_Nom.txt')
        noun_nom2 = random_word ('lexicon/nouns_Nom.txt')
        noun_Gen = random_word('lexicon/nouns_Gen.txt')
        line = noun_nom + ' ' + noun_Gen + ', ' + noun_nom2 + ','
        number = number_of_syllables (line)
    return line

def third_line (): #"noun Acc + verb Perf"
    number = 0
    while number != 5:
        noun = random_word('lexicon/nouns_Acc.txt')
        verb = random_word('lexicon/verbs_Perf.txt')
        line = noun + ' ' + verb + '.'
        number = number_of_syllables (line)
    return line


def fourth_line (): #"если + не + verb Praes 2Sg + noun/pronoun Acc"
    number = 0
    while number != 7:
        verb = random_word ('lexicon/verbs_2Sg.txt')
        noun = random_word ('lexicon/nouns_Acc.txt')
        line = 'если' + ' ' + 'не' + ' ' + verb + ' ' + noun + ','
        number = number_of_syllables (line)
    return line

def fifth_line (): #"не + verb 2Sg Imper + adverb + inf."
    number = 0
    while number != 7:
        verb = random_word('lexicon/verbs_Imperativ.txt')
        adverb = random_word('lexicon/adverbs.txt')
        inf = random_word ('lexicon/verbs_Inf.txt')
        line = 'не' + ' ' + verb + ' ' + adverb + ' ' + inf + '.'
        number = number_of_syllables (line)
    return line

def main():
    tanka = first_line() + '\n' + second_line() + '\n' + third_line() + '\n' + fourth_line() + '\n' + fifth_line()
    print (tanka)
 
if __name__ == '__main__':
    main()
