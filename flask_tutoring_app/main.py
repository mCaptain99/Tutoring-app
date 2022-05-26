# -*- coding: utf-8 -*-

from flask_admin import Admin
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager
from flask_recaptcha import ReCaptcha
from werkzeug.exceptions import InternalServerError

from controller.file_controller import upload_file
from dao.user_dao import UserDao
from models import User, City, Review, Ad, Response
from controller.user_controller import *
from controller.ads_controller import *
from controller.review_controller import *
from flask_wtf.csrf import CSRFProtect
from app_context import app

csrf = CSRFProtect(app)

#
#  Init login manager
#
login_manager = LoginManager()
login_manager.init_app(app)

#
#  Init ReCaptcha
#
recaptcha = ReCaptcha(app=app)
app.config['SECRET_KEY'] = 'localhost'
app.config['RECAPTCHA_USE_SSL'] = False
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LdOFjAdAAAAAMke6eBCsv2Eo97FLZ69ILq7YnPs'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LdOFjAdAAAAAIRvg4vukMDgX4g95_hTOCKWN7Of'
app.config['RECAPTCHA_OPTIONS'] = {'theme': 'black'}

import os
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

UPLOAD_FOLDER = 'static/photos'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#
#  Init flask admin
#
admin = Admin(app)
admin.add_view(FileAdmin(UPLOAD_FOLDER, '/static/', name='Static Files'))
admin.add_view(ModelView(User, UserDao.session))
admin.add_view(ModelView(Ad, UserDao.session))
admin.add_view(ModelView(Review, UserDao.session))
admin.add_view(ModelView(Response, UserDao.session))
admin.add_view(ModelView(City, UserDao.session))


@app.before_request
def before_request():
    if '/admin' in request.url:
        if not current_user.is_authenticated or not current_user.get_id() in UserService.get_admin_ids():
            raise werkzeug.exceptions.Forbidden


def verify_recaptcha(f):
    def wrapper(*args, **kwargs):
        if recaptcha.verify():
            return f(*args, **kwargs)
        else:
            return werkzeug.exceptions.BadRequest
    return wrapper


@login_manager.user_loader
def load_user(user_id):
    return UserService.get_by_id(user_id)


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for("show_login"))


app.add_url_rule('/logout', view_func=logout, methods=['GET'])
app.add_url_rule('/login', view_func=login, methods=['POST'])
app.add_url_rule('/login', view_func=show_login, methods=['GET'])
app.add_url_rule('/register', view_func=show_register, methods=['GET'])
app.add_url_rule('/register', view_func=register, methods=['POST'])
app.add_url_rule('/ads', view_func=show_ads, methods=['GET'])
app.add_url_rule('/ads/new', view_func=show_add_ad, methods=['GET'])
app.add_url_rule('/ads/search', view_func=csrf.exempt(filter_ads), methods=['POST', 'GET'])
app.add_url_rule('/ads/<ad_id>', view_func=ad_detail, methods=['GET'])
app.add_url_rule('/ads/<ad_id>', view_func=ad_review, methods=['POST'])
app.add_url_rule('/ads', view_func=add_ad, methods=['POST'])
app.add_url_rule('/me', view_func=me, methods=['GET'])
app.add_url_rule('/me/edit', view_func=show_edit_profile, methods=['GET'])
app.add_url_rule('/me/edit', view_func=edit_profile, methods=['POST'])
app.add_url_rule('/ads/<ad_id>/delete', view_func=delete_ad, methods=['POST'])
app.add_url_rule('/ads/<ad_id>/edit', view_func=edit_ad, methods=['POST'])
app.add_url_rule('/ads/<ad_id>/edit', view_func=show_edit_ad, methods=['GET'])
app.add_url_rule('/reviews/<review_id>/delete', view_func=delete_review, methods=['POST'])
app.add_url_rule('/ads/<ad_id>/add_response', view_func=add_response, methods=['POST'])
app.add_url_rule('/responses/<response_id>/delete', view_func=delete_response, methods=['POST'])
app.add_url_rule('/upload', view_func=upload_file, methods=['POST'])
app.add_url_rule('/reviews/<review_id>/responses', view_func=get_responses_by_review, methods=['GET'])
app.add_url_rule('/forgot', view_func=show_forgot_password, methods=['GET'])
app.add_url_rule('/forgot', view_func=forgot_password, methods=['POST'])
app.add_url_rule('/reset', view_func=reset_password, methods=['POST'])
app.add_url_rule('/reset/<reset_token>', view_func=show_reset_password, methods=['GET'])
app.add_url_rule('/verify/<token>', view_func=verify_email, methods=['GET'])


if __name__ == "__main__":
    app.run()
