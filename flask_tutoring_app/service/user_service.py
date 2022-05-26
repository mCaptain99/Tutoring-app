import os
import datetime

import werkzeug
from flask import flash
from flask_jwt_extended import create_access_token, decode_token
from typing import List, Optional

from dao.user_dao import UserDao
from models import User

PHOTOS_FOLDER = 'static/photos'


class UserService:

    @classmethod
    def register_user(cls, user_form_data: dict) -> Optional[User]:
        """ This function creates user object based on form data
        :param user_form_data: dict containing form data
        :return: boolean value describing if user was created
        """
        email_exists = bool(UserDao.get_user_by_email(user_form_data.get('email')))
        username_exists = bool(UserDao.get_by_username(user_form_data.get('username')))
        if email_exists:
            flash('Email jest już zajęty')
            return None
        if username_exists:
            flash('Nazwa użytkownika jest już zajęta')
            return None

        return UserDao.add(User(username=user_form_data.get('username'),
                           email=user_form_data.get('email'),
                           password=user_form_data.get('password'),
                           phone=user_form_data.get('phone'),
                           full_name=user_form_data.get('fullname')))

    @classmethod
    def get_by_username_and_password(cls, username: str, password: str) -> User:
        """ This function gets user by username and password
        :param username: username of the user
        :param password: password of the user
        :return: User object
        """
        return UserDao.get_by_username_and_password(username, password)

    @classmethod
    def get_by_id(cls, user_id: str) -> User:
        """ This function gets user by id
        :param user_id id of the user
        :return: User object
        """
        return UserDao.get_by_id(user_id)

    @classmethod
    def update_photo_url(cls, user: User, extension: str):
        """ This function remove old photo of user (if exists) and updates url extension
        :param user: user object
        :param extension: extension of an image of existing user
        """
        if os.path.exists(PHOTOS_FOLDER + '/' + user.username + '.' + user.photo_url):
            os.remove(PHOTOS_FOLDER + '/' + user.username + '.' + user.photo_url)
        UserDao.update_photo_url(user, extension)

    @classmethod
    def edit_user(cls, user_id: str, profile_form_data: dict):
        """ This function edit user with given id
        :param user_id: id of the user
        :param profile_form_data: dict containing form data
        """
        UserDao.edit_user(user_id, profile_form_data)

    @classmethod
    def get_admin_ids(cls) -> List[str]:
        """ This function get ids of users that are admins
        :return: List of ids
        """
        return [user.uuid for user in UserDao.get_admin_ids()]

    @classmethod
    def create_reset_token(cls, email: str) -> Optional[str]:
        """ This function search user with given email and creates token based on user id
        :param email: email of user
        :return: token
        """
        user = cls.get_user_by_email(email)
        if not user:
            flash('Nie ma w systemie konta o takim emailu')
            return None
        reset_token = create_access_token(user.uuid, expires_delta=datetime.timedelta(hours=24))
        return reset_token

    @classmethod
    def get_user_by_email(cls, email: str) -> User:
        """ This function gets user by email
        :param email: email of the user
        :return: User with given email
        """
        return UserDao.get_user_by_email(email)

    @classmethod
    def reset_password(cls, data: dict) -> Optional[User]:
        """ This function changes password of user with id encrypted in token
        :param data: dict containing form data
        :return: If operation was successful - user object, else False
        """
        reset_token = data.get('reset_token')
        password = data.get('password')
        user_id = decode_token(reset_token)['identity']
        if not user_id:
            return None
        user = UserDao.edit_user(user_id, new_data={'password': password})
        return user

    @classmethod
    def verify_user_email(cls, reset_token: str) -> Optional[User]:
        """ This function decode token sent to given email, and make user verified
        :param reset_token: token with user id encrypted
        :return: if operation was successful - user object, else False
        """
        user_id = decode_token(reset_token)['identity']
        if not user_id:
            return None
        user = UserDao.edit_user(user_id, new_data={'verified': True})
        return user
