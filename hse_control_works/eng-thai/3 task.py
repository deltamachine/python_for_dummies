import json

from flask import Flask
from flask import url_for, render_template, request, redirect

app = Flask(__name__)

@app.route('/')
def index():
    if request.args:
        word = request.args['word']
        values = find_translation (word)
        return render_template('results.html', values=values)
    return render_template('index.html')

def find_translation(key):
    with open ('eng_thai.json', 'r', encoding = 'utf-8') as file:
        f = file.read()
        data = json.loads (f)
        values = data[key]
    return values
        

if __name__ == '__main__':
    app.run(debug=True)
