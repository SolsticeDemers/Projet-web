from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, DecimalField
from wtforms import RadioField, SubmitField
from wtforms.validators import DataRequired, InputRequired, Optional, NumberRange, Length


class ArchiverProduitForm(FlaskForm):
    submit = SubmitField("Supprimer")
