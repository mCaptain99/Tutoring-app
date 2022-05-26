import enum

from sqlalchemy import exc, or_
from sqlalchemy.orm import sessionmaker, Query
from typing import List, Tuple

from models import Ad, engine, Review


class AdSort(enum.Enum):
    EVALUATION = 1
    PRICE = 2
    TITLE = 3


class AdDao:
    Session = sessionmaker(bind=engine)
    session = Session()

    @classmethod
    def get_ad_by_id(cls, ad_id):
        return cls.session.query(Ad).filter_by(uuid=ad_id).first()

    @classmethod
    def get_all_ads(cls, page, size):
        page -= 1
        return cls.session.query(Ad).order_by(Ad.evaluation.desc()).limit(size).offset(page*size)

    @classmethod
    def get_ad_count(cls):
        return cls.session.query(Ad).count()

    @classmethod
    def add_ad(cls, ad):
        try:
            cls.session.add(ad)
            cls.session.commit()
            return ad
        except exc.InvalidRequestError:
            return
        except exc.IntegrityError:
            return

    @classmethod
    def filter_ads(cls, kwargs: dict, page: int, size: int) -> Tuple[List[Ad], int]:
        """This functions filter and sort ads by sending queries to database
        :param kwargs: dict containing search params
        :param page: page of data
        :param size: number of elements in page
        :return: list of ads by page on size of all ads
        """
        ads = cls.session.query(Ad)
        for kwarg in kwargs:
            if kwarg == "price":
                ads = ads.filter(Ad.price <= kwargs[kwarg])
            elif kwarg == "title":
                ads = ads.filter(Ad.title.contains(kwargs[kwarg]))
            elif kwarg == "user_id":
                ads = ads.filter(Ad.user_id.in_(kwargs[kwarg]))
            elif kwarg == 'cities':
                ads = ads.filter(Ad.city_id.in_(kwargs[kwarg]))
            elif kwarg == 'form':
                ads = ads.filter(or_(Ad.online == kwargs[kwarg]['online'], Ad.stationary == kwargs[kwarg]['stationary']))
            elif kwarg == 'category':
                ads = ads.filter(Ad.category == kwargs[kwarg])
        if kwargs["sort"] == '1':
            ads = ads.order_by(Ad.evaluation.desc())
        elif kwargs["sort"] == '2':
            ads = ads.order_by(Ad.price)
        elif kwargs["sort"] == '3':
            ads = ads.order_by(Ad.title)
        elif kwargs["sort"] == '4':
            ads = ads.order_by(Ad.creation_date.desc())
        page -= 1
        total = ads.count()
        return ads.limit(size).offset(page*size), total

    @classmethod
    def get_ads_by_user(cls, user_id):
        return cls.session.query(Ad).filter_by(user_id=user_id).all()

    @classmethod
    def delete_ad(cls, ad_to_delete):
        cls.session.delete(ad_to_delete)
        cls.session.commit()

    @classmethod
    def edit_ad(cls, ad, new_data):
        for field in new_data:
            ad.__setattr__(field, new_data[field])
        cls.session.commit()

    @classmethod
    def update_evaluation(cls, ad_id):
        ad = cls.session.query(Ad).filter_by(uuid=ad_id).first()
        reviews = cls.session.query(Review).filter_by(ad_id=ad_id).all()
        ad.review_number = len(reviews)
        ad.evaluation = sum([review.rate for review in reviews]) / ad.review_number if ad.review_number else 0
        cls.session.commit()
