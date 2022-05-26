import math
import uuid
import datetime

import bcrypt
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, Float, Enum
from sqlalchemy import create_engine
from sqlalchemy.orm import relation
from sqlalchemy.pool import StaticPool
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("mysql://root:root@localhost:3306/tutoring?charset=utf8mb4", poolclass=StaticPool)
Base = declarative_base()


def generate_uuid():
    return str(uuid.uuid4())


class User(Base):
    __tablename__ = 'user'
    uuid = Column(String(36), name="uuid", primary_key=True)
    username = Column(String(150), unique=True, nullable=False)
    full_name = Column(String(150), nullable=False)
    _password = Column(String(256), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    phone = Column(String(50))
    is_active = Column(Boolean)
    is_authenticated = Column(Boolean)
    photo_url = Column(String(150), nullable=True)
    is_admin = Column(Boolean)
    verified = Column(Boolean)

    def __init__(self, username, password, email, phone, full_name, is_active=True, is_authenticated=False, is_admin=False, verified=False):
        self.uuid = generate_uuid()
        self.username = username
        self._password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        self.email = email
        self.full_name = full_name
        self.phone = phone
        self.is_active = is_active
        self.is_authenticated = is_authenticated
        self.photo_url = ''
        self.is_admin = is_admin
        self.verified = verified

    def get_id(self):
        return self.uuid

    def __repr__(self):
        return self.full_name

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, _password):
        self._password = bcrypt.hashpw(_password.encode('utf-8'), bcrypt.gensalt())


class Ad(Base):
    __tablename__ = 'ad'
    uuid = Column(String(36), name="uuid", primary_key=True)
    title = Column(String(150), nullable=False)
    price = Column(Integer, nullable=False)
    user_id = Column(String(36), ForeignKey("user.uuid"))
    creation_date = Column(DateTime)
    body = Column(String(10000))
    author = relation('User')
    city_id = Column(Integer, ForeignKey("city.id"))
    city = relation('City')
    category = Column(String(50))
    online = Column(Boolean)
    stationary = Column(Boolean)
    evaluation = Column(Float)
    review_number = Column(Integer)

    def __init__(self, title, user_id, price, body, city_id, category, online=False, stationary=False):
        self.uuid = generate_uuid()
        self.title = title
        self.user_id = user_id
        self.price = price
        self.creation_date = datetime.datetime.now()
        self.body = body
        self.city_id = city_id
        self.category = category
        if not online and not stationary :
            self.online = True
            self.stationary = True
        else:
            self.online = online
            self.stationary = stationary
        self.evaluation = 0
        self.review_number = 0

    def __repr__(self):
        return '[' + self.title + ', ' + str(self.price) + ']\n'


class Review(Base):
    __tablename__ = 'review'
    uuid = Column(String(36), name="uuid", primary_key=True)
    user_id = Column(String(36), ForeignKey("user.uuid"))
    ad_id = Column(String(36), ForeignKey('ad.uuid'))
    body = Column(String(10000), nullable=True)
    rate = Column(Integer, nullable=False)
    creation_date = Column(DateTime)
    author = relation("User")
    ad = relation("Ad")
    responses = relation("Response", lazy='dynamic')
    responses_count = Column(Integer)

    def __init__(self, ad_id, user_id, body, rate):
        self.uuid = generate_uuid()
        self.ad_id = ad_id
        self.user_id = user_id
        self.body = body
        self.rate = rate
        self.creation_date = datetime.datetime.now()
        self.responses_count = 0


class Response(Base):
    __tablename__ = 'response'
    uuid = Column(String(36), name="uuid", primary_key=True)
    user_id = Column(String(36), ForeignKey("user.uuid"))
    review_id = Column(String(36), ForeignKey('review.uuid'))
    body = Column(String(10000), nullable=True)
    creation_date = Column(DateTime)
    author = relation("User")
    review = relation("Review")

    def __init__(self, review_id, user_id, body):
        self.uuid = generate_uuid()
        self.review_id = review_id
        self.user_id = user_id
        self.body = body
        self.creation_date = datetime.datetime.now()

    def as_dict(self):
        ret = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        ret.update({'author': self.author.full_name})
        return ret


class City(Base):
    __tablename__ = 'city'
    id = Column(Integer, primary_key=True)
    name = Column(String(36), name="name")
    lat = Column(Float, name="lat")
    lon = Column(Float, name="lon")

    def __init__(self, name, lat, lon):
        self.name = name
        self.lat = lat
        self.lon = lon

    def is_in_radius_of(self, city, radius: int) -> bool:
        """This function check if city given as a parameter is in radius
        of self
        :param: city City - other city
        :param: radius - radius of city search
        :returns: boolean
        """
        lat_distnce = abs(self.lat - city.lat) * 180/math.pi * 110.5
        lon_distnce = abs(self.lon - city.lon) * 180/math.pi * 111
        return lat_distnce**2 + lon_distnce**2 < radius**2


Base.metadata.create_all(engine)
