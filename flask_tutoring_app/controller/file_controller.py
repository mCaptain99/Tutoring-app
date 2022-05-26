from flask import request, flash

from flask_login import login_required, current_user
from werkzeug.utils import redirect, secure_filename

from service.user_service import UserService

PHOTOS_EXTENSIONS = ('png', 'jpg', 'jpeg')
PHOTOS_FOLDER = 'static/photos'


@login_required
def upload_file():
    """This function implements POST /upload end point
    It save given file to folder in server
    :return: redirect to user detail page
    """
    file = request.files['file']
    if not file or not file.filename:
        flash('Nie wybrano pliku')
    else:
        *filename, extension = file.filename.split('.')
        if extension not in PHOTOS_EXTENSIONS or not filename:
            flash('Zły format pliku')
        else:
            user = UserService.get_by_id(current_user.get_id())
            extension, filename = secure_filename(extension), secure_filename(user.username)
            UserService.update_photo_url(user, extension)
            file.save('/'.join([PHOTOS_FOLDER, filename + '.' + extension]))
    return redirect('/me')
