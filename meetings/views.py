import datetime

from flask import render_template, redirect, url_for, request
from flask import Blueprint
from flask_login import current_user
from flask_login import login_required

from app import db
from datatypes.course import Course
from datatypes.meeting import Meeting
from datatypes.subject import Subject
from datatypes.utils import get_meetings_for_course, add_user_to_meeting, db_remove_user_from_meeting, create_meeting, \
    get_subjects_for_course
from decorators import check_confirmed
from meetings.forms import AddMeetingForm

meetings_blueprint = Blueprint('meetings', __name__, )


@meetings_blueprint.route('/meetings')
@login_required
@check_confirmed
def meetings_list():
    course = Course.query.filter(Course.id.like(current_user.course)).first()
    return render_template('meetings/meetings_list.html', datetime=datetime, course=course,
                           current_user=current_user, meetlist=get_meetings_for_course(
            current_user.course, current_user.id))


@meetings_blueprint.route('/meetings/join/<meeting_id>')
@login_required
@check_confirmed
def join_meeting(meeting_id):
    add_user_to_meeting(current_user.id, meeting_id)
    return redirect(url_for('meetings.meetings_list'))


@meetings_blueprint.route('/meetings/removeuser/<meeting_id>')
@login_required
@check_confirmed
def remove_user_from_meeting(meeting_id):
    db_remove_user_from_meeting(current_user.id, meeting_id)
    return redirect(url_for('meetings.meetings_list'))

@meetings_blueprint.route('/meetings/addMeeting')
@login_required
@check_confirmed
def addMeeting():
    form = AddMeetingForm(request.form)
    subjlist = get_subjects_for_course(current_user.course).all()
    form.subject.choices = map(lambda s: (s.id, s.name), subjlist)
    form.subject.choices.insert(0, ('', ''))
    if form.validate_on_submit():
        create_meeting(
            host=current_user.id,
            subject=form.subject.data,
            datetime=form.date_meeting.data,
            creation_date=datetime.now(),
            link=form.link.data,
            description=form.description.data
        )
        redirect(url_for('meetings.meetings_list'))
    return render_template('meetings/createMeeting.html', form=form)