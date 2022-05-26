from typing import List, Tuple, Optional

import werkzeug

from dao.ad_dao import AdDao
from dao.review_dao import ReviewDao
from models import Review, Response


class ReviewService:

    @classmethod
    def add_review(cls, review_form_data: dict, author_id: str, ad_id: str) -> bool:
        """ This function ad review to an existing ad
        :param review_form_data: dict containing ad form data
        :param author_id: id of the author of ad
        :param ad_id: id of the ad
        :return: ad with given id
        """
        if cls.user_has_opinion(author_id, ad_id):
            return False
        else:
            review = Review(
                body=review_form_data.get('body'),
                rate=review_form_data.get('rate'),
                user_id=author_id,
                ad_id=ad_id
            )
            ReviewDao.add_review(review)
            AdDao.update_evaluation(ad_id)
            return True

    @classmethod
    def user_has_opinion(cls, author_id: str, ad_id: str) -> bool:
        """ This function checks if the user with given od has opinion about the ad with given od
        :param author_id: id of the author of review
        :param ad_id: id of an ad
        :return: bool
        """
        opinion = ReviewDao.get_review_by_user_and_ad(user_id=author_id, ad_id=ad_id)
        return bool(opinion)

    @classmethod
    def get_reviews_by_user(cls, user_id: str) -> List[Review]:
        """ This function gets reviews of ser with given id
        :param user_id: id of the review author
        :return: list of reviews belonging to user with given id
        """
        return ReviewDao.get_reviews_by_user(user_id)

    @classmethod
    def delete_reviews_by_ad(cls, ad_id: str):
        """ This function deletes reviews by ad
        :param ad_id: id of the ad
        """
        reviews = ReviewDao.get_reviews_by_ad(ad_id)
        for review in reviews:
            ReviewDao.delete_responses_by_review(review)
            ReviewDao.delete_review(review)
            AdDao.update_evaluation(ad_id)

    @classmethod
    def delete_review(cls, review_id: str, user_id: str) -> Tuple[bool, str]:
        """ This function deletes review with given user if it belongs to user with given od
        :param review_id: id of the review
        :param user_id: id of the author
        :return: Tuple containing bool value describing if review was deleted and id of ad, which review is about
        """
        review_to_delete = ReviewDao.get_review_by_id(review_id)
        if review_to_delete and user_id == review_to_delete.user_id:
            ReviewDao.delete_responses_by_review(review_to_delete)
            ReviewDao.delete_review(review_to_delete)
            AdDao.update_evaluation(review_to_delete.ad_id)
            return True, review_to_delete.ad_id
        return False, review_to_delete.ad_id

    @classmethod
    def add_response(cls, response_form_data: dict, user_id: str):
        """ This function ad response to the review with id given in form data
        :param response_form_data: dict containing form data
        :param user_id: id of the user
        """
        body, review_id = response_form_data.get('body'), response_form_data.get('review_id')
        if not ReviewDao.get_review_by_id(review_id):
            raise werkzeug.exceptions.NotFound('Nie ma opinii o takim id')
        ReviewDao.add_response(Response(body=body, review_id=review_id, user_id=user_id))
        ReviewDao.update_responses_count(review_id)

    @classmethod
    def delete_response(cls, response_id: str, user_id: str) -> Optional[Response]:
        """ This function delete response with given id
        :param response_id: id of the response to delete
        :param user_id: id of an author of response
        :return: boolean value describing if deleting was successful
        """
        response_to_delete = ReviewDao.get_response_by_id(response_id)
        if response_to_delete and user_id == response_to_delete.user_id:
            ReviewDao.delete_response(response_to_delete)
            return response_to_delete
        return None

    @classmethod
    def get_responses_by_review(cls, review_id: str, page: int) -> List[Response]:
        """ This function get page of responses belonging to review with given id
        :param review_id: id of the review
        :param page: page of result set
        :return: page from list of responses belonging to review
        """
        return ReviewDao.get_responses_by_review(review_id, page)

    @classmethod
    def get_review_count(cls, ad_id: str) -> int:
        """ This function get number of reviews belonging to ad with given id
        :param ad_id: id of the ad
        :return: number of reviews
        """
        return ReviewDao.get_reviews_count(ad_id)

    @classmethod
    def get_responses_by_user(cls, user_id: str) -> List[Response]:
        """ This function gets responses of the user with given id
        :param user_id: id of author of responses
        :return: List of responses belonging to the user
        """
        return ReviewDao.get_responses_by_user(user_id)
