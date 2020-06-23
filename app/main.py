from flask import Flask
from flask import request
from flask import Response
from flask import render_template
from flask import jsonify

from wiktionaryparser import WiktionaryParser

import random

app = Flask(__name__)
parser = WiktionaryParser()

fname = "words.txt"

@app.route('/')
def index():
    return render_template("index.html")
	
@app.route('/rand-word')
def rand_word():
    lines = open(fname).read().splitlines()
    return random.choice(lines)

@app.route('/origin/<word>')
def origin(word):
    word = parser.fetch(word)
    ety_orig = word[0]['etymology']
    print(ety_orig)
    ety = ety_orig.lower()
    german = ety.find('german')
    latin = ety.find('latin')
    if german == -1 and latin == -1:
        res = 'other', ety_orig
    elif german == -1 and latin > -1:
        res = 'latin', ety_orig
    elif german > -1 and latin == -1:
        res = 'germanic', ety_orig
    else:
        res = ('germanic' if german < latin else 'latin'), ety_orig
    return jsonify(res)

if __name__ == '__main__':
    app.run()

