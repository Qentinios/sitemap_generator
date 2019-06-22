from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import URL

DEPTH = [(str(i), str(i) + ' level') for i in range(1, 5)]
FORMAT = [('screen', 'Tree'), ('txt', 'Text'), ('xml', 'Xml')]


class GeneratorForm(FlaskForm):
    url = StringField('Target url', validators=[URL()])
    depth = SelectField('Recursion depth', choices=DEPTH)
    format = SelectField('Output format', choices=FORMAT)

