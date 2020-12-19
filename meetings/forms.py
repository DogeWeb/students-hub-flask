import datetime

from flask_wtf import FlaskForm
from wtforms import ValidationError, StringField, SelectField, DateField
from wtforms.validators import DataRequired, Length


class Subject(object):
    pass

def validate_date(self, date):
    dat = date.data
    if dat < datetime.date.today():  # TODO: improve validation
        raise ValidationError('Error in the date of meeting')

class AddMeetingForm(FlaskForm):
    subject = SelectField('Select subject', validators=[DataRequired()])
    date_meeting = DateField('date:', validators=[DataRequired(), validate_date])

    description = StringField('description', validators=[DataRequired(), Length(min=1, max=240)])
    link = StringField('link', validators=[DataRequired(), Length(min=2, max=100)])



