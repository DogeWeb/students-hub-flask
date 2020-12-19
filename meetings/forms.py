import datetime

from flask_wtf import FlaskForm
from wtforms import ValidationError, StringField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length


def validate_date(self, date):
    dat = date.data
    if dat < datetime.date.today():
        raise ValidationError('Error in the date of meeting, the date has to be in the future')


class AddMeetingForm(FlaskForm):
    subject = SelectField('Select subject', validators=[DataRequired()])
    date_meeting = DateField('date:', validators=[DataRequired(), validate_date])
    description = StringField('description', validators=[DataRequired(), Length(min=1, max=240)])
    link = StringField('link', validators=[DataRequired(), Length(min=2, max=100)])
