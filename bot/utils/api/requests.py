from typing import Any
from urllib import response
from .execute import make_request

class Requests:
    def create_user(self, user_id: int, first_name: str, username: str) -> dict:
        path: str = "api/create_user/"
        response: dict = make_request(path=path, user_id=user_id, first_name=first_name, username=username)
        return response

    def set_name(self, user_id: int, name: str) -> dict:
        path: str = "api/set_name/"
        response: dict = make_request(path=path, user_id=user_id, name=name)
        return response

    def set_city(self, user_id: int, city: str) -> dict:
        path: str = "api/set_city/"
        response: dict = make_request(path=path, user_id=user_id, city=city)
        return response

    def check_phone(self, user_id: int) -> dict:
        path: str = "api/check_phone/"
        response: dict = make_request(path=path, user_id=user_id)
        return response

    def set_phone(self, user_id: int, phone: int) -> dict:
        path: str = "api/set_phone/"
        response: dict = make_request(path=path, user_id=user_id, phone=phone)
        return response

    def get_all_marks(self) -> dict:
        path: str = "api/get_all_marks"
        response: dict = make_request(path=path)
        return response

    def get_all_bodies(self, mark: str) -> dict:
        path: str = "api/get_all_bodies/"
        response: dict = make_request(path=path, mark=mark)
        return response

    def get_all_fuel_types(self, mark: str) -> dict:
        path: str = "api/get_all_fuel_types/"
        response: dict = make_request(path=path, mark=mark)
        return response

    def find_car(self,
        **kwargs
    ) -> dict:
        path: str = "api/find_car/"
        _: dict[str, Any] = kwargs
        params: dict[str, Any] = dict(body=_.get("Body") if _.get("Body") else "Unknow",
            fuel_type=_.get("FuelType") if _.get("FuelType") else "Unknow",
            transmission=_.get("Transmission") if _.get("Transmission") else "Unknow")
        del kwargs["Body"], kwargs["FuelType"], kwargs["Transmission"]
        response: dict = make_request(path=path, headers=kwargs, **params)
        return response
