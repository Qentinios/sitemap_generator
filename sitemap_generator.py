from flask import Flask, render_template

import os
from forms import GeneratorForm

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


@app.route('/')
def home():
    form = GeneratorForm()

    return render_template('index.html', form=form)


@app.route('/generator', methods=['POST'])
def generator():
    form = GeneratorForm()

    if form.validate_on_submit():
        return 'valid'
    else:
        return render_template('index.html', form=form)
