import datetime
import os

from flask import render_template, url_for, redirect
from flask import Blueprint
from flask_login import current_user
from flask_login import login_required
from flask_wtf import form
from werkzeug.utils import secure_filename

from app import db, app
from datatypes.course import Course
from datatypes.meeting import Meeting
from datatypes.subject import Subject
from datatypes.utils import get_subjects_for_course, get_notes_for_subject, add_note, get_notes_with_author_for_subject
from decorators import check_confirmed
from notes.forms import UploadForm
from security.templates import get_templates_path

notes_blueprint = Blueprint('notes', __name__, )


@notes_blueprint.route('/subjects')
@login_required
@check_confirmed
def subjects_list():
    course = Course.query.filter(Course.id.like(current_user.course)).first()
    return render_template(get_templates_path('notes/subjects_list.html'), course=course, current_user=current_user,
                           subjectslist=get_subjects_for_course(
                               current_user.course))


@notes_blueprint.route('/notes/<subject_id>')
@login_required
@check_confirmed
def notes_list(subject_id):
    subject = Subject.query.filter(Subject.id.like(subject_id)).first()
    return render_template(get_templates_path('notes/notes_list.html'), datetime=datetime, subject=subject,
                           current_user=current_user,
                           noteslist=get_notes_with_author_for_subject(subject_id))


@notes_blueprint.route("/upload", methods=["POST", "GET"])
@login_required
@check_confirmed
def upload():
    form = UploadForm()
    subjlist = get_subjects_for_course(current_user.course).all()
    form.subject.choices = map(lambda s: (s.id, s.name), subjlist)
    if form.validate_on_submit():
        filename = secure_filename(form.file.data.filename)
        form.file.data.save(os.path.join(app.config['UPLOAD_FOLDER'], current_user.id, 'notes', form.subject, filename))
        add_note(current_user.id, form.subject, form.description.data, filename)
        return redirect(url_for('upload'))

    return render_template(get_templates_path('notes/upload.html'), form=form)


@notes_blueprint.route("/download/<file>", methods=["POST", "GET"])
@login_required
@check_confirmed
def download(file):
    return redirect(url_for('notes.subjects_list'))
