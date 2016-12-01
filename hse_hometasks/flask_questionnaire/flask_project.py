import re
import json

from flask import Flask
from flask import url_for, render_template, request, redirect

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/questions')
def questions():
    if request.args:
        data_collecting (request.args)
        return redirect (url_for ('index'))
    return render_template('questions.html')

@app.route('/stats')
def stats():
    info_stats = statistics_numbers()
    num_users = info_stats['number_of_users']
    num_lang = info_stats['number_of_languages']
    line1 = []
    line2 = []
    create_a_row (line1)
    create_a_row2 (line2)
    return render_template('stats.html', num_users=num_users, num_lang=num_lang, line1=line1, line2=line2)

@app.route('/json')
def data_json():
    create_json()
    return render_template('data.json')

@app.route('/search')
def search():
    delay = []
    languages = set_of_languages ()
    
    if request.args:
        for elem in request.args.keys():
            delay.append(elem)
            
        g = gest1_dict(delay)
        d = def1_dict (delay)
        e = exp1_dict (delay)

        g2 = gest2_dict(delay)
        d2 = def2_dict (delay)
        e2 = exp2_dict (delay)
        
        return render_template('results.html', delay=delay, g=g, d=d, e=e, g2=g2, d2=d2, e2=e2)
    return render_template('search.html', languages=languages)

def data_collecting (dicty):
    with open ('info_resp.csv', 'a', encoding = 'utf-8') as file:
        info = 'name\t%s\tcountry\t%s\tlanguage\t%s\tgesture1\t%s\tdefinition1\t%s\texplain1\t%s\tgesture2\t%s\tdefinition2\t%s\texplain2\t%s\n'
        file.write (info % (dicty['name'], dicty['country'], dicty['language'], dicty['gesture1'], dicty['definition1'], dicty['example1'], dicty['gesture2'], dicty['definition2'], dicty['example2']))

def statistics_numbers ():
    info_stats = {}
    with open ('info_resp.csv', 'r', encoding = 'utf-8') as file:
        f = file.read()
        users = re.findall ('name\t', f)
        languages = re.findall ('language\t(.*?)\t', f)
        info_stats['number_of_users'] = len (users)
        info_stats['number_of_languages'] = len (set (languages))
    return info_stats

def create_a_row (line1):
    gesture1 = ''
    def1 = ''
    exp1 = ''
    with open ('info_resp.csv', 'r', encoding = 'utf-8') as file:   
        for line in file.readlines():
            line = line.split('\t')
            gesture1 = gesture1 + line[5] + ' - ' + line[7] + ', '
            def1 = def1 + line[5] + ' - ' + line[9] + ', '
            exp1 = exp1 + line[5] + ' - ' + line[11] + ', '

    line1.append (gesture1)
    line1.append (def1)
    line1.append (exp1)

    return line1

def create_a_row2 (line2):
    gesture2 = ''
    def2 = ''
    exp2 = ''
    with open ('info_resp.csv', 'r', encoding = 'utf-8') as file:   
        for line in file.readlines():
            line = line.split('\t')
            gesture2 = gesture2 + line[5] + ' - ' + line[13] + '\n'
            def2 = def2 + line[5] + ' - ' + line[15] + '\n'
            exp2 = exp2 + line[5] + ' - ' + line[17] + '\n'

    line2.append (gesture2)
    line2.append (def2)
    line2.append (exp2)

    return line2

def create_json():
    data_json = open ('templates/data.json', 'w', encoding = 'utf-8')

    with open ('info_resp.csv', 'r', encoding = 'utf-8') as file:
        for line in file.readlines():
            data = {}
            line = line.split('\t')
            for i in range (0, len(line), 2):
                data[line[i]] = line[i+1]
            data_line = json.dumps(data)
            data_json.writelines (data_line)

    data_json.close()

def set_of_languages():
    with open ('info_resp.csv', 'r', encoding = 'utf-8') as file:
        f = file.read()
        languages = re.findall ('language\t(.*?)\t', f)
        languages = set (languages)
        languages = list (languages)
    return languages

def gest1_dict(delay):

    g = ''
    gest1_dict = {}

    with open ('info_resp.csv', 'r', encoding = 'utf-8') as file:
        for line in file.readlines():
            line = line.split('\t')
            gest1_dict [line[5] + ' - ' + line[7]] = line[5]

        for key, value in gest1_dict.items():
            if value in delay:
                g = g + key + ', '
    return g

def def1_dict(delay):

    d = ''
    def1_dict = {}

    with open ('info_resp.csv', 'r', encoding = 'utf-8') as file:
        for line in file.readlines():
            line = line.split('\t')
            def1_dict [line[5] + ' - ' + line[9]] = line[5]

        for key, value in def1_dict.items():
            if value in delay:
                d = d + key + ', '
    return d

def exp1_dict(delay):

    e = ''
    exp1_dict = {}

    with open ('info_resp.csv', 'r', encoding = 'utf-8') as file:
        for line in file.readlines():
            line = line.split('\t')
            exp1_dict [line[5] + ' - ' + line[11]] = line[5]

        for key, value in exp1_dict.items():
            if value in delay:
                e = e + key + ', '
    return e

def gest2_dict(delay):

    g2 = ''
    gest2_dict = {}

    with open ('info_resp.csv', 'r', encoding = 'utf-8') as file:
        for line in file.readlines():
            line = line.split('\t')
            gest2_dict [line[5] + ' - ' + line[13]] = line[5]

        for key, value in gest2_dict.items():
            if value in delay:
                g2 = g2 + key + ', '
    return g2

def def2_dict(delay):

    d2 = ''
    def2_dict = {}

    with open ('info_resp.csv', 'r', encoding = 'utf-8') as file:
        for line in file.readlines():
            line = line.split('\t')
            def2_dict [line[5] + ' - ' + line[15]] = line[5]

        for key, value in def2_dict.items():
            if value in delay:
                d2 = d2 + key + ', '
    return d2

def exp2_dict(delay):

    e2 = ''
    exp2_dict = {}

    with open ('info_resp.csv', 'r', encoding = 'utf-8') as file:
        for line in file.readlines():
            line = line.split('\t')
            exp2_dict [line[5] + ' - ' + line[17]] = line[5]

        for key, value in exp2_dict.items():
            if value in delay:
                e2 = e2 + key + ', '
    return e2

        
if __name__ == '__main__':
    app.run(debug=True)
