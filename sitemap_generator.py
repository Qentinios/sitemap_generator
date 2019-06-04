from flask import Flask, render_template, jsonify, make_response

import os
from forms import GeneratorForm
from generator import Generator

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


@app.route('/', methods=['GET', 'POST'])
def home():
    form = GeneratorForm()

    if form.validate_on_submit():
        generator = Generator(url=form.url.data, depth=int(form.depth.data))
        sitemap = generator.generate()

        if form.format.data == 'screen':
            return make_response(jsonify(sitemap), 200)
        else:
            return 'file'
    else:
        return render_template('index.html', form=form)

