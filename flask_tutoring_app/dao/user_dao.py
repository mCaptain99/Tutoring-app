import hashlib

import bcrypt
import werkzeug
from sqlalchemy import exc
from sqlalchemy.orm import sessionmaker

from models import User, engine


class UserDao:
    Session = sessionmaker(bind=engine)
    session = Session()

    @classmethod
    def add(cls, user):
        try:
            cls.session.add(user)
            cls.session.commit()
            return user
        except exc.InvalidRequestError:
            return
        except exc.IntegrityError:
            return

    @classmethod
    def get_by_username_and_password(cls, username, password):
        user = cls.session.query(User).filter_by(username=username).first()
        if not user or not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            return None
        else:
            return user

    @classmethod
    def get_by_username(cls, username):
        user = cls.session.query(User).filter_by(username=username).first()
        if not user:
            return None
        else:
            return user

    @classmethod
    def get_by_id(cls, user_id):
        return cls.session.query(User).filter_by(uuid=user_id).first()

    @classmethod
    def get_users_with_fullname_like(cls, full_name):
        return [user.uuid for user in cls.session.query(User).filter(User.full_name.contains(full_name)).all()]

    @classmethod
    def update_photo_url(cls, user, extension):
        user.photo_url = extension
        cls.session.commit()

    @classmethod
    def edit_user(cls, user_id: str, new_data: dict) -> User:
        user = cls.get_by_id(user_id)
        if not user:
            raise werkzeug.exceptions.NotFound
        for field in new_data:
            user.__setattr__(field, new_data[field])
        cls.session.commit()
        return user

    @classmethod
    def get_admin_ids(cls):
        return cls.session.query(User).filter_by(is_admin=True).all()

    @classmethod
    def get_user_by_email(cls, email):
        return cls.session.query(User).filter_by(email=email).first()
