from datetime import datetime

from sqlalchemy import func, case, text, exists, literal_column, literal, select

from app import bcrypt
from app import db
from course import Course
from meeting import Meeting
from note import Note
from subject import Subject
from user import User
from university import University
from meeting_users import MeetingUsers
from event import Event
from apartment import Apartment


def __safe_commit(transaction):
    try:
        result = transaction()
        db.session.commit()
        return result
    except Exception, e:
        print (str(e))
        db.session.rollback()
        return -1


def insert_user(name, surname, email, password, dateofbirth, university, course):
    return __safe_commit(lambda: __insert_user(name, surname, email, password, dateofbirth, university, course))


def __insert_user(name, surname, email, password, dateofbirth, university, course):
    pwhash = bcrypt.generate_password_hash(password).encode('utf-8')
    usr = User(
        name=name,
        surname=surname,
        email=email,
        password=pwhash,
        dateofbirth=dateofbirth,
        university=university,
        course=course,
        registered_on=datetime.today()
    )
    db.session.add(usr)
    return usr


def delete_user(usr):
    return __safe_commit(lambda: __delete_user(usr))


def __delete_user(usr):
    return db.session.delete(usr)


def delete_user_by_id(user_id):
    return __safe_commit(lambda: __delete_user_by_id(user_id))


def __delete_user_by_id(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user:
        MeetingUsers.query.filter_by(user=user_id).delete()
        return db.session.delete(user)
    return -1


def get_user_by_id(user_id):
    return User.query.filter_by(id=user_id).first()


def get_user_by_id_or_404(user_id):
    return User.query.filter_by(id=user_id).first_or_404()


def get_user_by_email(user_email):
    return User.query.filter_by(email=user_email).first()


def get_user_by_email_or_404(user_email):
    return User.query.filter_by(email=user_email).first_or_404()


def auth_user(user_email, user_pw):
    user = User.query.filter_by(email=user_email).first()
    if user and bcrypt.check_password_hash(user.password, user_pw):
        return user
    return -1


def update_user(user_id, name=None, surname=None, email=None, password=None, dateofbirth=None, university=None,
                course=None, confirmed=None, password_reset_token=None):
    return __safe_commit(
        lambda: __update_user(user_id, name, surname, email, password, dateofbirth, university, course, confirmed))


def __update_user(user_id, name=None, surname=None, email=None, password=None, dateofbirth=None, university=None,
                  course=None, confirmed=None, password_reset_token=None):
    usr = User.query.filter_by(id=user_id).first()
    if usr:
        if name is not None:
            usr.name = name
        if surname is not None:
            usr.surname = surname
        if email is not None:
            usr.email = email
        if password is not None:
            usr.password = bcrypt.generate_password_hash(password).encode('utf-8')
        if dateofbirth is not None:
            usr.dateofbirth = dateofbirth
        if university is not None:
            usr.university = university
        if course is not None:
            usr.course = course
        if confirmed is not None:
            usr.confirmed = confirmed
        if password_reset_token is not None:
            usr.password_reset_token = password_reset_token
    return True


def create_meeting(host_id, subject_id, datetime, creation_date, link, description):
    def part1():
        meeting = Meeting(
            host=host_id,
            subject=subject_id,
            datetime=datetime,
            creation_date=creation_date,
            link=link,
            description=description)
        db.session.add(meeting)
        return meeting

    meeting = __safe_commit(part1)

    def part2():
        db.session.commit()
        meeting_user = MeetingUsers(meeting=meeting.id, user=host_id)
        db.session.add(meeting_user)

    return __safe_commit(part2)


def add_user_to_meeting(user_id, meeting_id):
    already_in = MeetingUsers.query.filter(MeetingUsers.user.like(user_id)).filter(MeetingUsers.meeting.like(meeting_id)).first()
    if already_in:
        return
    return __safe_commit(lambda: __add_user_to_meeting(user_id, meeting_id))


def __add_user_to_meeting(user_id, meeting_id):
    meeting_user = MeetingUsers(meeting=meeting_id, user=user_id)
    db.session.add(meeting_user)
    return


def db_remove_user_from_meeting(user_id, meeting_id):
    return __safe_commit(lambda: __remove_user_from_meeting(user_id, meeting_id))


def __remove_user_from_meeting(user_id, meeting_id):
    meeting_user = MeetingUsers.query.filter_by(meeting=meeting_id, user=user_id).first()
    if meeting_user:
        db.session.delete(meeting_user)
        return 0
    return -1


def remove_meeting(meeting_id):
    return __safe_commit(lambda: __remove_meeting(meeting_id))


def __remove_meeting(meeting_id):
    MeetingUsers.query.filter_by(meeting=meeting_id).delete()
    Meeting.query.filter_by(id=meeting_id).delete()
    return


def add_note(user_id, subject_id, description, date, file_path):
    return __safe_commit(lambda: __add_note(user_id, subject_id, description, date, file_path))


def __add_note(user_id, subject_id, description, date, file_path):
    note = Note(
        author=user_id,
        subject=subject_id,
        description=description,
        upload_date=date,
        file=file_path)
    return db.session.add(note)


def get_meetings_for_course(course_id, current_user_id):
    # subqry = MeetingUsers.query\
    #              .join(Meeting)\
    #              .filter(MeetingUsers.user.like(current_user_id))\
    #              .filter(Meeting.id.like(MeetingUsers.meeting)).subquery()

    # subqry = db.session.execute(text("SELECT * FROM meeting_users WHERE meeting_users.user LIKE {} AND meeting.id LIKE meeting_users.meeting".format(current_user_id))).subquery()
    #
    # xpr = case([(exists(subqry), db.true())], else_=db.false())
    #
    # query = db.session.query(Meeting, Subject, Course, User, MeetingUsers, func.count(MeetingUsers.user), xpr) \
    #     .filter(Meeting.subject.like(Subject.id)) \
    #     .filter(Subject.course.like(Course.id)) \
    #     .filter(Course.id.like(course_id)) \
    #     .filter(User.id.like(Meeting.host)) \
    #     .filter(Meeting.id.like(MeetingUsers.meeting)) \
    #     .group_by(MeetingUsers.meeting)

    # Too complex to make a Sqlalchemy

    query = db.session.query(Meeting, Subject, Course, User, MeetingUsers, literal_column('count_1'), literal_column('in_the_meeting')).from_statement(_get_query(course_id, current_user_id))

    # print str(query)
    return query


def get_notes_for_subject(subject_id):
    return db.session.query(Note).join(Subject).filter(Note.subject.like(Subject.id)).filter(
        Subject.id.like(subject_id))


def get_notes_with_author_for_subject(subject_id):
    return db.session.query(Note, User).join(Subject).filter(Note.subject.like(Subject.id)).filter(
        Subject.id.like(subject_id)).filter(User.id.like(Note.author))


def get_subjects_for_course(course_id):
    return db.session.query(Subject).join(Course).filter(
        Subject.course.like(Course.id)).filter(Course.id.like(course_id))


def _get_query(course_id, current_user_id):
    # call me the master of queries :)
    return db.text("""
    SELECT meeting.id                AS meeting_id,
       meeting.host              AS meeting_host,
       meeting.subject           AS meeting_subject,
       meeting.datetime          AS meeting_datetime,
       meeting.creation_date     AS meeting_creation_date,
       meeting.link              AS meeting_link,
       meeting.description       AS meeting_description,
       subject.id                AS subject_id,
       subject.course            AS subject_course,
       subject.name              AS subject_name,
       course.id                 AS course_id,
       course.university         AS course_university,
       course.name               AS course_name,
       user.id                   AS user_id,
       user.name                 AS user_name,
       user.surname              AS user_surname,
       user.email                AS user_email,
       user.password             AS user_password,
       user.dateofbirth          AS user_dateofbirth,
       user.university           AS user_university,
       user.course               AS user_course,
       user.registered_on        AS user_registered_on,
       user.confirmed            AS user_confirmed,
       user.confirmed_on         AS user_confirmed_on,
       user.password_reset_token AS user_password_reset_token,
       meeting_users.meeting     AS meeting_users_meeting,
       meeting_users.user        AS meeting_users_user,
       count(meeting_users.user) AS count_1,
       CASE WHEN EXISTS(SELECT * FROM meeting_users WHERE meeting_users.user LIKE {} AND meeting.id LIKE meeting_users.meeting) THEN 1 ELSE 0 END [in_the_meeting]
FROM meeting,
     subject,
     course,
     user,
     meeting_users
WHERE meeting.subject LIKE subject.id
  AND subject.course LIKE course.id
  AND course.id LIKE {}
  AND user.id LIKE meeting.host
  AND meeting.id LIKE meeting_users.meeting
GROUP BY meeting_users.meeting
    """.format(current_user_id, course_id))