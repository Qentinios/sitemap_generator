from flask import Flask, render_template, jsonify, make_response

import os
from forms import GeneratorForm
from generator import Generator
from lxml import etree

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.route('/', methods=['GET', 'POST'])
def home():
    form = GeneratorForm()

    if form.validate_on_submit():
        generator = Generator(url=form.url.data, depth=int(form.depth.data), flat=(form.format.data != 'screen'))
        sitemap = generator.generate()

        if form.format.data == 'screen':
            return make_response(jsonify(sitemap), 200)
        elif form.format.data == 'xml':
            root = etree.Element('sitemap')
            home_url = etree.Element('url')
            home_url.text = form.url.data
            root.append(home_url)

            for hyperlink in sitemap:
                url = etree.Element('url')
                url.text = hyperlink
                root.append(url)

            xml = etree.tostring(root, pretty_print=True)

            response = make_response(xml, 200)
            response.headers['Content-Type'] = 'application/xml'

            return response
        else:
            text = form.url.data + '<br>'
            text += '<br>'.join(sitemap)

            return make_response(text, 200)
    else:
        return render_template('index.html', form=form)

