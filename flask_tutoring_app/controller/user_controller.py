import datetime

from flask import render_template, url_for, request, flash
from flask_jwt_extended import create_access_token
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import redirect

from utils.mailing import send_message
from service.ad_service import AdService
from service.review_service import ReviewService
from service.user_service import UserService
from utils.forms import LoginForm, RegistrationForm, UserEditForm, PasswordForgotForm, PasswordResetForm, show_error_messages


@login_required
def logout():
    """This function implements POST /logout end point.
    It deletes user id from browser session.
    :returns: redirect to /login end point"""
    logout_user()
    return redirect(url_for('show_login'))


def show_login():
    """This function implements GET /login end point.
    :return: template with login page
    """
    previous = request.referrer if request.referrer else '/ads'
    form = LoginForm()
    return render_template('login.html', form=form, previous=previous)


def show_register():
    """This function implements GET /register end point.
    :return: template with register form
    """
    form = RegistrationForm()
    return render_template('register.html', form=form)


def register():
    """This function implements POST /register end point.
    It adds user and send an email with activation link
    :return: template with login
    """
    form = RegistrationForm(request.form)
    if form.validate():
        user = UserService.register_user(form.data)
        if user:
            flash('Wysłano link aktywacyjny na podany adres mail')
            expires = datetime.timedelta(hours=24)
            token = create_access_token(user.uuid, expires_delta=expires)
            url = request.host_url + 'verify/' + token
            send_message('[Korepetycje] Aktywacja konta',
                         sender='korepetycje33.pl@gmail.com',
                         recipients=[user.email],
                         text='Aktywuj swoje konto',
                         html=render_template('verify_account_message.html', url=url))
            return redirect('/login')
    show_error_messages(form)
    return render_template('register.html', form=form)


def login():
    """This function implements POST /login end point.
    It adds user to browser session.
    :return: redirect to previous page
    """
    form = LoginForm(request.form)
    if form.validate():
        username = form.username.data
        password = form.password.data
        user = UserService.get_by_username_and_password(username, password)
        if not user:
            flash('Niewłaściwe Hasło lub nazwa użytkownika')
            return render_template('login.html', form=form)
        if not user.verified:
            flash('Konto nie zostało zweryfikowane. Sprawdź swoją pocztę email')
            return render_template('login.html', form=form)
        user.is_authenticated = True
        login_user(user, remember=True)
        return redirect(form.previous.data)
    else:
        flash('niewłaściwe hało lub nazwa użytkownika')
        return render_template('login.html', form=form, message="niewłaściwe hasło lub nazwa użytkownika")


@login_required
def me():
    """This function implements GET /me end point
    :return: template with user details"""
    user_id = current_user.get_id()
    me = UserService.get_by_id(user_id)
    ads = AdService.get_ads_by_user(user_id)
    reviews = ReviewService.get_reviews_by_user(user_id)
    responses = ReviewService.get_responses_by_user(user_id)
    return render_template('me.html', user=me, ads=ads, reviews=reviews, responses=responses)


@login_required
def show_edit_profile():
    """This function implements GET /me/edit end point
    :returns: template with ser edit form"""
    user_id = current_user.get_id()
    me = UserService.get_by_id(user_id)
    return render_template('me_edit.html', me=me)


@login_required
def edit_profile():
    """This function implements POST /me/edit end point>
    It edits user data according to form data
    :returns: template with user details"""
    user_id = current_user.get_id()
    me = UserService.get_by_id(user_id)
    profile_form = UserEditForm(request.form)
    if profile_form.validate():
        UserService.edit_user(user_id, profile_form.data)
    else:
        show_error_messages(profile_form)
    return redirect('/me')


def forgot_password():
    """This function implements POST /forgot end point.
    It sends reset password token to email given in form
    :return: template with forgot password form"""
    form = PasswordForgotForm(request.form)
    email = form.email.data
    token = UserService.create_reset_token(email=email)
    if token:
        url = request.host_url + 'reset/' + token
        send_message('[Korepetycje] Zresetuj hasło',
                     sender='korepetycje33.pl@gmail.com',
                     recipients=[email],
                     text=render_template('reset_password_message.html', url=url),
                     html=render_template('reset_password_message.html',  url=url))
        flash('Wysłano email na podany adres')
    return render_template('forgot_password.html', form=form)


def reset_password():
    """This function implements POST /reset end point.
    It gets reset password token and decode it to get the user. Later it changes the password
    :return: template with forgot password form"""
    form = PasswordResetForm(request.form)
    if form.validate():
        user = UserService.reset_password(form.data)
        if user:
            send_message('[Korepetycje] Hasło zmienione',
                         sender='korepetycje33.pl@gmail.com',
                         recipients=[user.email],
                         text='Hasło zostało pomyślnie zmienione',
                         html='<p>Hasło zostało pomyślnie zmienione</p>')
            flash('Hasło zostało pomyślnie zmienione')
            return redirect('/login')
        else:
            flash('Niepoprawny token')
    show_error_messages(form)
    return render_template('reset_password.html', reset_token=form.reset_token.data, form=PasswordResetForm())


def show_forgot_password():
    """This function implements GET /forgot end point
    :return: template with forgot form"""
    form = PasswordForgotForm()
    return render_template('forgot_password.html', form=form)


def show_reset_password(reset_token):
    """This function implements GET /reset/<reset_token> end point.
    :param: reset token - token with encoded user id
    :returns: template with reset password form"""
    form = PasswordResetForm()
    return render_template('reset_password.html', reset_token=reset_token, form=form)


def verify_email(token):
    """This function implements GET /verify/<token> end point.
    :param: token - token with encoded ser id
    :returns: template with login page"""
    form = LoginForm()
    if UserService.verify_user_email(token):
        flash('Email zweryfikowano poprawnie! Możesz się teraz zalogować')
    else:
        flash('Coś poszło nie tak...')
    return render_template('login.html', form=form)
