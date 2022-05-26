from sqlalchemy import exc
from sqlalchemy.orm import sessionmaker

from models import engine, City


class CityDao:
    Session = sessionmaker(bind=engine)
    session = Session()

    @classmethod
    def get_all_cities(cls):
        return cls.session.query(City).all()

    @classmethod
    def get_city_by_name(cls, name):
        return cls.session.query(City).filter_by(name=name).first()

    @classmethod
    def add_city(cls, city):
        try:
            cls.session.add(city)
            cls.session.commit()
            return city
        except exc.InvalidRequestError:
            return
        except exc.IntegrityError:
            return
