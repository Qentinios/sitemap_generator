from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import URL

DEPTH = [(str(i), str(i) + ' level') for i in range(1, 6)]
FORMAT = [('screen', 'Print on screen'), ('txt', 'Text file'), ('xml', 'Xml file')]


class GeneratorForm(FlaskForm):
    url = StringField('Target url', validators=[URL()])
    depth = SelectField('Recursion depth', choices=DEPTH)
    format = SelectField('Output format', choices=FORMAT)

