import datetime

from app import bcrypt
from flask import Blueprint, url_for, render_template, flash, redirect, request
from flask_login import login_required, current_user, logout_user, login_user

from app import db
from datatypes.user import User
from datatypes.utils import insert_user, update_user
from decorators import check_confirmed

from security.email import send_email
from security.token import generate_confirmation_token, confirm_token
from user.forms import LoginForm, RegisterForm, ForgotForm, ChangePasswordForm, EditProfileForm

user_blueprint = Blueprint('user', __name__, )


@user_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        usr = insert_user(
            name=form.name.data,
            surname=form.surname.data,
            email=form.email.data,
            password=form.password.data,
            dateofbirth=form.dateofbirth.data,
            university=form.university.data,
            course=form.course.data
        )
        if isinstance(usr, (int, long)):
            return redirect(url_for("user.register"))
        token = generate_confirmation_token(usr.email)
        confirm_url = url_for('user.confirm_email', token=token, _external=True)
        html = render_template('user/activate.html', confirm_url=confirm_url)
        subject = "Please confirm your email"
        send_email(usr.email, subject, html)

        login_user(usr)

        flash('A confirmation email has been sent via email.', 'success')
        return redirect(url_for("main.home"))

    return render_template('user/register.html', form=form)


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(
                user.password, request.form['password']):
            login_user(user)
            flash('Welcome ' + user.email, 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Invalid email and/or password.', 'danger')
            return render_template('user/login.html', form=form)
    return render_template('user/login.html', form=form)


@user_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You were logged out.', 'success')
    return redirect(url_for('user.login'))


@user_blueprint.route('/profile/', defaults={'edit': None}, methods=['GET', 'POST'])
@user_blueprint.route('/profile/<int:edit>', methods=['GET', 'POST'])
@login_required
@check_confirmed
def profile(edit):
    edit_flag = True if edit is not None and int(edit) == 1 else False

    form = EditProfileForm(request.form)

    if form.validate_on_submit():
        print update_user(current_user.id, name=form.name.data, surname=form.surname.data
                          , dateofbirth=form.dateofbirth.data, university=form.university.data, course=form.course.data)
        user = User.query.filter_by(email=current_user.email).first()
        flash('Personal Info successfully updated.', 'danger')
        if len(form.password.data) > 4:
            if user:
                user.password = bcrypt.generate_password_hash(form.password.data)
                db.session.commit()
                flash('Password successfully changed.', 'success')
                return redirect(url_for('user.profile'))
            else:
                flash('Password change was unsuccessful.', 'danger')
                return redirect(url_for('user.profile', edit=1))

    form.university.default = int(current_user.university)
    form.course.default = int(current_user.course)
    form.process()
    form.dateofbirth.data = current_user.dateofbirth
    form.name.data = str(current_user.name)
    form.surname.data = str(current_user.surname)

    if edit is None:
        form.university.render_kw = {'disabled': True}
        form.course.render_kw = {'disabled': True}
        form.dateofbirth.render_kw = {'disabled': True}
        form.name.render_kw = {'disabled': True}
        form.surname.render_kw = {'disabled': True}
        # form.password.render_kw = {'style': 'display:none'}
        # form.password_con.render_kw = {'style': 'display:none'}

    return render_template('user/profile.html', form=form, edit=edit_flag)


@user_blueprint.route('/confirm/<token>')
@login_required
def confirm_email(token):
    if current_user.confirmed:
        flash('Account already confirmed. Please login.', 'success')
        return redirect(url_for('main.home'))
    email = confirm_token(token)
    user = User.query.filter_by(email=current_user.email).first_or_404()
    if user.email == email:
        user.confirmed = True
        user.confirmed_on = datetime.datetime.now()
        db.session.add(user)
        db.session.commit()
        flash('You have confirmed your account. Thanks!', 'success')
    else:
        flash('The confirmation link is invalid or has expired.', 'danger')
    return redirect(url_for('main.home'))


@user_blueprint.route('/unconfirmed')
@login_required
def unconfirmed():
    if current_user.confirmed:
        return redirect(url_for('main.home'))
    flash('Please confirm your account!', 'warning')
    return render_template('user/unconfirmed.html')


@user_blueprint.route('/resend')
@login_required
def resend_confirmation():
    token = generate_confirmation_token(current_user.email)
    confirm_url = url_for('user.confirm_email', token=token, _external=True)
    html = render_template('user/activate.html', confirm_url=confirm_url)
    subject = "Please confirm your email"
    send_email(current_user.email, subject, html)
    flash('A new confirmation email has been sent.', 'success')
    return redirect(url_for('user.unconfirmed'))


@user_blueprint.route('/forgot', methods=['GET', 'POST'])
def forgot():
    form = ForgotForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()  # TODO: use utils methods
        token = generate_confirmation_token(user.email)

        user.password_reset_token = token
        db.session.commit()

        reset_url = url_for('user.forgot_new', token=token, _external=True)
        html = render_template('user/reset.html',
                               username=user.email,
                               reset_url=reset_url)
        subject = "Reset your password"
        send_email(user.email, subject, html)

        flash('A password reset email has been sent via email.', 'success')
        return redirect(url_for("main.home"))

    return render_template('user/forgot.html', form=form)


@user_blueprint.route('/forgot/new/<token>', methods=['GET', 'POST'])
def forgot_new(token):
    email = confirm_token(token)
    user = User.query.filter_by(email=email).first_or_404()

    if user.password_reset_token is not None:
        form = ChangePasswordForm(request.form)
        if form.validate_on_submit():
            user = User.query.filter_by(email=email).first()
            if user:
                # TODO: use utils methods
                user.password = bcrypt.generate_password_hash(form.password.data)
                user.password_reset_token = None
                db.session.commit()

                login_user(user)

                flash('Password successfully changed.', 'success')
                return redirect(url_for('user.profile'))

            else:
                flash('Password change was unsuccessful.', 'danger')
                return redirect(url_for('user.profile'))
        else:
            flash('You can now change your password.', 'success')
            return render_template('user/forgot_new.html', form=form)
    else:
        flash('Can not reset the password, try again.', 'danger')

    return redirect(url_for('main.home'))
