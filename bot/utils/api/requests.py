from urllib import response
from .execute import make_request
from log.logger import logger

class Requests:
    def create_user(self, user_id: int, first_name: str, username: str):
        path = "api/create_user/"
        response = make_request(path=path, user_id=user_id, first_name=first_name, username=username)

        if response.get("response"):
            logger.info(F"Created new user! ID: {user_id}")
        return response

    def set_name(self, user_id: int, name: str):
        path = "api/set_name/"
        response = make_request(path=path, user_id=user_id, name=name)

        if response.get("response"):
            logger.info(F"Set name! ID: {user_id}")
        return response

    def set_city(self, user_id: int, city: str):
        path = "api/set_city/"
        response = make_request(path=path, user_id=user_id, city=city)

        if response.get("response"):
            logger.info(F"Set city! ID: {user_id}")
        return response

    def check_phone(self, user_id: int):
        path = "api/check_phone/"
        response = make_request(path=path, user_id=user_id)
        return response

    def set_phone(self, user_id: int, phone: int):
        path = "api/set_phone/"
        response = make_request(path=path, user_id=user_id, phone=phone)
        return response

    def get_all_marks(self):
        path = "api/get_all_marks"
        response = make_request(path=path)
        return response

    def get_all_bodies(self):
        path = "api/get_bodies"
        response = make_request(path=path)
        return response
