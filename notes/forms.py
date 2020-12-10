from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import SubmitField, StringField, SelectField
from wtforms.validators import DataRequired, Length, ValidationError, InputRequired
from wtforms.widgets import TextArea

from datatypes.note import Note
from datatypes.utils import get_note


class UploadForm(FlaskForm):
    file = FileField('file', validators=[FileRequired()])
    description = StringField('Description', validators=[Length(min=0, max=240)], widget=TextArea())
    subject = SelectField('Select subject', validators=[DataRequired()])
    upload = SubmitField('upload')

    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            return False

        if not self.description.data:
            self.description.errors.append('You must provide a description')
            return False
        note = get_note(current_user.id, int(self.subject.data), self.file.data.filename)
        if note is not None:
            self.file.errors.append(
                'A file with this name uploaded by you already exists in this subject, please check the file name')
            return False

        return True
