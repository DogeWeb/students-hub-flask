from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import SubmitField, StringField, SelectField
from wtforms.validators import DataRequired, Length


class UploadForm(FlaskForm):
    file = FileField('file', validators=[DataRequired()])
    description = StringField('description', validators=[DataRequired(), Length(min=1, max=240)])
    subject = SelectField('Select subject', validators=[DataRequired()])
    upload = SubmitField('upload')
