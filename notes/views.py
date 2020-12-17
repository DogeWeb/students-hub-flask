import datetime
import os

from flask import render_template, url_for, redirect, flash, request, send_from_directory
from flask import Blueprint
from flask_login import current_user
from flask_login import login_required
from flask_wtf import form
from werkzeug.datastructures import CombinedMultiDict
from werkzeug.utils import secure_filename

from app import db, app
from datatypes.course import Course
from datatypes.meeting import Meeting
from datatypes.subject import Subject
from datatypes.utils import get_subjects_for_course, get_notes_for_subject, add_note, get_notes_with_author_for_subject, \
    get_note_by_id, add_or_update_note_rating, remove_note_rating
from decorators import check_confirmed
from notes.forms import UploadForm
from projconfig import basedir

notes_blueprint = Blueprint('notes', __name__, )


@notes_blueprint.route('/subjects')
@login_required
@check_confirmed
def subjects_list():
    course = Course.query.filter(Course.id.like(current_user.course)).first()
    return render_template('notes/subjects_list.html', course=course, current_user=current_user,
                           subjectslist=get_subjects_for_course(
                               current_user.course))


@notes_blueprint.route('/notes/<subject_id>')
@login_required
@check_confirmed
def notes_list(subject_id):
    subject = Subject.query.filter(Subject.id.like(subject_id)).first()
    return render_template('notes/notes_list.html', datetime=datetime, subject=subject,
                           current_user=current_user,
                           noteslist=get_notes_with_author_for_subject(subject_id))


@notes_blueprint.route("/upload", methods=["POST", "GET"])
@login_required
@check_confirmed
def upload():
    form = UploadForm(CombinedMultiDict((request.files, request.form)))
    subjlist = get_subjects_for_course(current_user.course).all()
    form.subject.choices = map(lambda s: (s.id, s.name), subjlist)
    form.subject.choices.insert(0, ('', ''))
    if form.validate_on_submit():
        filename = secure_filename(form.file.data.filename)
        save_path = os.path.join(basedir, app.config['UPLOAD_FOLDER'], str(current_user.id), 'notes', form.subject.data)

        if not os.path.exists(save_path):
            os.makedirs(
                os.path.join(basedir, app.config['UPLOAD_FOLDER'], str(current_user.id), 'notes', form.subject.data))

        form.file.data.save(os.path.join(save_path, filename))
        add_note(current_user.id, int(form.subject.data), form.description.data, filename)
        flash('Note correctly uploaded')
        return redirect(url_for('notes.notes_list', subject_id=int(form.subject.data)))

    return render_template('notes/upload.html', form=form)


@notes_blueprint.route("/download/<user_id>/<subject_id>/<file_name>", methods=["POST", "GET"])
@login_required
@check_confirmed
def download(user_id, subject_id, file_name):
    return send_from_directory(
        directory=os.path.join(basedir, app.config['UPLOAD_FOLDER'], user_id, 'notes', subject_id), filename=file_name,
        attachment_filename=file_name)


@notes_blueprint.route("/notes/rating/<note_id>")
@login_required
@check_confirmed
def rating(note_id):
    note = get_note_by_id(note_id)
    rating = request.args.get('rating')
    if not note or not rating:
        return redirect(url_for('notes.subjects_list'))
    add_or_update_note_rating(current_user.id, int(note_id), int(rating))
    return redirect(url_for('notes.notes_list', subject_id=note.subject))


@notes_blueprint.route("/notes/remove_rating/<note_id>")
@login_required
@check_confirmed
def remove_rating(note_id):
    note = get_note_by_id(note_id)
    if not note:
        return redirect(url_for('notes.subjects_list'))
    remove_note_rating(current_user.id, int(note_id))
    return redirect(url_for('notes.notes_list', subject_id=note.subject))
