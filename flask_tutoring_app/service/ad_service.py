from typing import Optional

from flask import flash

from service.city_service import CityService
from service.review_service import ReviewService
from dao.ad_dao import *
from dao.city_dao import CityDao
from dao.review_dao import *
from dao.user_dao import *


class AdService:

    @classmethod
    def get_all_ad_detail(cls, ad_id: str, page: int = 1, size: int = 10) -> Tuple[Ad, List[Review]]:
        """ This function is used to get ad by id and page of its reviews
        :param ad_id: id of ad
        :param page: page of reviews set
        :param size: number of items in page
        :return: ad and one page of its reviews
        """
        ad = AdDao.get_ad_by_id(ad_id)
        reviews = ReviewDao.get_reviews_by_ad(ad_id, page, size)
        return ad, reviews

    @classmethod
    def get_ad_list(cls, page: int = 1, size: int = 10) -> List[Ad]:
        """ This function is used to get page of list af all ads sorted by evaluation
        :param page: page of ad ser
        :param size: size of page
        :return: one page of ads
        """
        ads = AdDao.get_all_ads(page, size)
        return ads

    @classmethod
    def get_ad_count(cls) -> int:
        """ This function is used to get number of all ads
        :return: Number of all ads
        """
        return AdDao.get_ad_count()

    @classmethod
    def filter_ads(cls, search_data: dict, page: int, size: int) -> Tuple[List[Ad], int]:
        """This function is used to transform data from search form in order to fit them to models
        :param: search_data - dict containing search form fields
        :param: page - page of data which hast to be returned
        :param: size - number of elements in page
        :returns: list of ads by page on size of all ads
        """
        search_data['user_id'] = UserDao.get_users_with_fullname_like(search_data.get('author')) \
            if search_data.get('author') else None
        if not search_data['user_id'] and search_data.get('author'):
            flash('Nie znaleziona użytkownika o podobnej nazwie')
            return [], 0
        search_data['form'] = {}
        if not search_data.get("online") and not search_data.get("stationary"):
            search_data["form"]["online"] = True
            search_data["form"]["stationary"] = True
        else:
            search_data["form"]["online"] = bool(search_data.get("online"))
            search_data["form"]["stationary"] = bool(search_data.get("stationary"))
        search_data["cities"] = cls.get_cities_of_search(search_data.get('city'), search_data.get('radius'))
        filter_data = cls.__clean_data(search_data)
        return AdDao.filter_ads(filter_data, page=page, size=size)

    @classmethod
    def get_cities_of_search(cls, city_name: str, radius: int) -> Optional[List[str]]:
        """This function returns ids of cities in radius of main_city
        :param: city_name - name of city in center of search
        :param: radius - radius of search
        :returns: List of city ids"""
        if not city_name:
            return None
        try:
            city = CityDao.get_city_by_name(city_name)
            if radius:
                radius = int(radius)
            else:
                radius = 0
        except ValueError:
            return [city.id]
        cities = CityService.get_cities_in_radius(radius=radius, main_city=city)
        return [city.id for city in cities]

    @classmethod
    def add_ad(cls, ad_form_data: dict, author_id: str) -> str:
        """This function is used to add ad
        :param ad_form_data: dict containing form data
        :param author_id: id of ad author
        :param city_name: name of ad city
        :return: id of new ad
        """
        city = CityDao.get_city_by_name(ad_form_data.get('city'))
        ad = Ad(title=ad_form_data.get('title'),
                price=ad_form_data.get('price'),
                body=ad_form_data.get('body'),
                category=ad_form_data.get('category'),
                user_id=author_id,
                city_id=city.id if city else None,
                online=ad_form_data.get('online'),
                stationary=ad_form_data.get('stationary'))
        AdDao.add_ad(ad)
        return ad.uuid

    @classmethod
    def get_ads_by_user(cls, user_id: str) -> List[Ad]:
        """
        :param user_id: id of an author
        :return: List of ads that belong to user with given id
        """
        return AdDao.get_ads_by_user(user_id)

    @classmethod
    def __clean_data(cls, kwargs: dict) -> dict:
        """ This function os used to remove None values from dict
        :param kwargs:
        :return:
        """
        ret = {}
        for kwarg in kwargs:
            if kwargs[kwarg]:
                ret[kwarg] = kwargs[kwarg]
        return ret

    @classmethod
    def delete_ad(cls, ad_id: str, user_id: str) -> bool:
        """
        This function is used to delete ad with given id
        :param ad_id: id of the ad
        :param user_id: id of the author
        :return: boolean value describing if ad was deleted
        """
        ad_to_delete = AdDao.get_ad_by_id(ad_id)
        if ad_to_delete and user_id == ad_to_delete.user_id:
            ReviewService.delete_reviews_by_ad(ad_id)
            AdDao.delete_ad(ad_to_delete)
            return True
        return False

    @classmethod
    def get_ad_by_id(cls, ad_id) -> Ad:
        """
        :param ad_id: id of the ad
        :return: Ad with given id
        """
        return AdDao.get_ad_by_id(ad_id)

    @classmethod
    def edit_ad(cls, ad: Ad, ad_form_data: dict, author_id: str):
        """
        :param ad: ad to be rdited
        :param ad_form_data: dict containing edit form data
        :param author_id: id of the author of ad
        """
        city = CityDao.get_city_by_name(ad_form_data.get('city'))
        del ad_form_data['city']
        ad_form_data['city_id'] = city.id if city else None
        if ad.user_id != author_id:
            raise werkzeug.exceptions.BadRequest
        AdDao.edit_ad(ad, ad_form_data)
