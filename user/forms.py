# project/user/forms.py
import datetime

from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, SelectField, SubmitField, StringField
from wtforms.fields.html5 import EmailField, DateField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError

from datatypes.course import Course
from datatypes.university import University
from datatypes.user import User


class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])


def validate_email(self, email):
    st = User.query.filter_by(email=email.data).first()
    if st:
        raise ValidationError('This email is already in use')


def validate_dateofbirth(self, dateofbirth):
    dat = dateofbirth.data
    if dat > datetime.date.today():  # TODO: improve validation
        raise ValidationError('Error in the date of birth')


class RegisterForm(FlaskForm):
    name = StringField('name:', validators=[DataRequired(), Length(min=2, max=20)])
    surname = StringField('surname:', validators=[DataRequired(), Length(min=2, max=20)])
    email = EmailField('email', validators=[DataRequired(), Email(), validate_email])
    password = PasswordField('password', validators=[DataRequired(), Length(min=4, max=80)])
    password_con = PasswordField('repeat password', validators=[DataRequired(), EqualTo('password', message='Passwords must match.')])
    university = SelectField('select university', choices=[(un.id, un.name) for un in University.query])
    course = SelectField('Select course', choices=[(c.id, c.name) for c in Course.query])
    dateofbirth = DateField('date of birth', validators=[DataRequired(), validate_dateofbirth])
    # submit = SubmitField('register')


class ForgotForm(FlaskForm):
    email = StringField(
        'email',
        validators=[DataRequired(), Email(message=None), Length(min=6, max=255)])

    def validate(self):
        initial_validation = super(ForgotForm, self).validate()
        if not initial_validation:
            return False
        user = User.query.filter_by(email=self.email.data).first()
        if not user:
            self.email.errors.append("This email is not registered")
            return False
        return True


class ChangePasswordForm(FlaskForm):
    password = PasswordField(
        'password',
        validators=[DataRequired(), Length(min=3, max=80)]
    )
    confirm = PasswordField(
        'Repeat password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match.')
        ]
    )
