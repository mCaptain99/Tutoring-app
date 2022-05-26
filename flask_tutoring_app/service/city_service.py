from typing import List

from dao.city_dao import CityDao
from models import City


class CityService:
    @classmethod
    def get_cities_in_radius(cls, radius: int, main_city: City) -> List[City]:
        """This function returns all cities that are in radius given as parameter
        of main_city gicen as a parameter
        :param: radius - radius of a search
        :param: main_city - city in center of search
        :returns: List of cities in radius of main)city
        """
        cities = CityDao.get_all_cities()
        cities = [city for city in cities if city.is_in_radius_of(main_city, radius)]
        cities.append(main_city)
        return cities

    @classmethod
    def get_cities_by_name(cls, name: str) -> City:
        """
        :param name: name of city
        :return: City with given name
        """
        return CityDao.get_city_by_name(name)
