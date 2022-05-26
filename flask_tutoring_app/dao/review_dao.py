from sqlalchemy import exc
from sqlalchemy.orm import sessionmaker

from models import Review, engine, Response


class ReviewDao:
    Session = sessionmaker(bind=engine)
    session = Session()

    @classmethod
    def get_reviews_by_ad(cls, ad_id, page=1, size=10):
        page -= 1
        return cls.session.query(Review).filter_by(ad_id=ad_id).limit(size).offset(page*size)

    @classmethod
    def get_review_by_user_and_ad(cls, user_id, ad_id):
        return cls.session.query(Review).filter_by(user_id=user_id).filter_by(ad_id=ad_id).first()

    @classmethod
    def add_review(cls, review):
        try:
            cls.session.add(review)
            cls.session.commit()
            return review
        except exc.InvalidRequestError:
            return
        except exc.IntegrityError:
            return

    @classmethod
    def get_review_by_ad(cls, ad_id):
        return cls.session.query(Review).filter_by(ad_id=ad_id).all()

    @classmethod
    def get_reviews_by_user(cls, user_id):
        return cls.session.query(Review).filter_by(user_id=user_id).all()

    @classmethod
    def delete_review(cls, review):
        cls.session.delete(review)
        cls.session.commit()

    @classmethod
    def get_review_by_id(cls, review_id):
        return cls.session.query(Review).filter_by(uuid=review_id).first()

    @classmethod
    def add_response(cls, response):
        try:
            cls.session.add(response)
            cls.session.commit()
            return response
        except exc.InvalidRequestError:
            return
        except exc.IntegrityError:
            return

    @classmethod
    def get_response_by_id(cls, response_id):
        return cls.session.query(Response).filter_by(uuid=response_id).first()

    @classmethod
    def delete_response(cls, response):
        review = cls.get_review_by_id(response.review_id)
        cls.session.delete(response)
        review.responses_count -= 1
        cls.session.commit()

    @classmethod
    def delete_responses_by_review(cls, review):
        for response in review.responses:
            cls.delete_response(response)

    @classmethod
    def get_reviews_count(cls, ad_id):
        return cls.session.query(Review).filter_by(ad_id=ad_id).count()

    @classmethod
    def get_responses_count_by_review(cls, review_id):
        return cls.session.query(Response).filter_by(review_id=review_id)

    @classmethod
    def get_responses_by_review(cls, review_id, page):
        size = 3
        page -= 1
        return cls.session.query(Response).filter_by(review_id=review_id).limit(size).offset(page*size).all()

    @classmethod
    def update_responses_count(cls, review_id):
        review = cls.get_review_by_id(review_id=review_id)
        review.responses_count += 1
        cls.session.commit()

    @classmethod
    def get_responses_by_user(cls, user_id):
        return cls.session.query(Response).filter_by(user_id=user_id)
