import json
from collections import Counter

from loguru import logger
from django.shortcuts import render
from django.db.models.query import QuerySet
from requests import head
from rest_framework.generics import ListAPIView
from django.http import (HttpRequest, HttpResponse,
                         HttpResponseRedirect, HttpResponsePermanentRedirect)

from .models import *


PRICE_RANGE = {
    "87506fd2b91be8b7ab7b59d069c42d40": {
        "min": 500000,
        "max": 2000000
    },

    "1ee1876784dfba4421dfbc93272053a8": {
        "min": 2000000,
        "max": 4000000
    },

    "af499ea026c3e952d324d7af4cf7aaee": {
        "min": 4000000,
        "max": 6000000
    },

    "2a3225e2decd960cebe8c4de135f59a0": {
        "min": 6000000,
        "max": None
    },
} # Keys is ids price range.


class API:
    class CreateBotUserView(ListAPIView):
        serializer_class: BotUser = BotUser  # Set serializer object.

        def get(self, request: HttpRequest, user_id: int, first_name: str, username: str) -> HttpResponse:
            queryset: QuerySet = BotUser.objects.filter(user_id=user_id)

            if not queryset.exists():
                BotUser.objects.create(user_id=user_id, first_name=first_name, username=username)
                return HttpResponse(json.dumps({"response": True}), content_type='application/json')
            user = queryset.get()
            return HttpResponse(json.dumps({"response": False, "name": user.name, "city": user.city_id}), content_type='application/json')


    class SetNameView(ListAPIView):
        serializer_class: BotUser = BotUser

        def get(self, request: HttpRequest, user_id: int, name: str):
            queryset: QuerySet = BotUser.objects.filter(user_id=user_id)
            queryset.update(name=name)
            return HttpResponse(json.dumps({"response": True}), content_type='application/json')


    class SetCityView(ListAPIView):
        serializer_class: BotUser = BotUser

        def get(self, request: HttpRequest, user_id: int, city: str):
            queryset: QuerySet = BotUser.objects.filter(user_id=user_id)
            city: QuerySet = City.objects.filter(title=city)

            if not city:
                return HttpResponse(json.dumps({"response": False}), content_type='application/json')
            else:
                city = city.get()
                queryset.update(city_id=city.pk)
                return HttpResponse(json.dumps({"response": True, "message": city.message}), content_type='application/json')


    class CheckPhoneView(ListAPIView):
        serializer_class: BotUser = BotUser

        def get(self, request: HttpRequest, user_id: int):
            queryset: QuerySet = BotUser.objects.get(user_id=user_id)

            if queryset.phone:
                return HttpResponse(json.dumps({"response": True}), content_type='application/json')
            else:
                return HttpResponse(json.dumps({"response": False}), content_type='application/json')


    class SetPhoneView(ListAPIView):
        serializer_class: BotUser = BotUser

        def get(self, request: HttpRequest, user_id: int, phone: int):
            queryset: QuerySet = BotUser.objects.filter(user_id=user_id)
            queryset.update(phone=phone)
            return HttpResponse(json.dumps({"response": True}), content_type='application/json')


    class GetAllMarksView(ListAPIView):
        serializer_class: BotUser = BotUser

        def get(self, request: HttpRequest):
            queryset: QuerySet = Mark.objects.filter(is_visible=True).all()
            all_marks = [mark.title for mark in queryset]
            return HttpResponse(json.dumps({"all_marks": all_marks}), content_type='application/json')


    class GetAllBodiesView(ListAPIView):
        serializer_class: Model = Model

        def get(self, request: HttpRequest, mark: str):
            queryset: QuerySet = Model.objects.filter(mark=Mark.objects.get(title=mark).pk).all()
            counter = Counter([model.body for model in queryset])
            bodies = list(counter.keys())
            return HttpResponse(json.dumps({"all_bodies": bodies}), content_type='application/json')


    class GetAllFuelTypesView(ListAPIView):
        serializer_class: Engine = Engine

        def get(self, request: HttpRequest, mark: str):
            mark: QuerySet = Mark.objects.filter(title=mark).get()
            cars: QuerySet = Car.objects.filter(mark=mark).all()
            engines = [Engine.objects.filter(id=car.engine.pk).get() for car in cars]
            counter = Counter([engine.type_fuel for engine in engines])
            fuel_types = list(counter.keys())
            return HttpResponse(json.dumps({"all_fuel_types": fuel_types}), content_type='application/json')


    class FindCarView(ListAPIView):
        serializer_class: Car = Car

        def get(self, request: HttpRequest,
            body: str, fuel_type: str, transmission: str
        ):
            if body == "Unknow" or fuel_type == "Unknow":
                return HttpResponse(json.dumps({"response": False}), content_type='application/json')
            else:
                headers = request.headers
                user_id = int(headers.get("Userid"))
                try:
                    user = BotUser.objects.get(user_id=user_id)
                    mark = Mark.objects.filter(title=headers.get("Mark")).get()
                    transmission_obj = Transmission.objects.filter(title=transmission).get()
                    if bool(headers.get("Isrange")):
                        price_range = PRICE_RANGE.get(headers.get("Rangeid"))
                        min_p = price_range.get("min")
                        max_p = price_range.get("max")
                        if bool(headers.get("Isvolume")):
                            cars = Car.objects.filter(mark=mark, price__range=[min_p, max_p], city=user.city, transmission=transmission_obj).all()
                            if cars:
                                cars = [car.to_dict() for car in cars if car.set.model.body == body and car.engine.type_fuel == fuel_type]
                                return HttpResponse(json.dumps({"response": True, "cars": cars}), content_type='application/json')
                        elif bool(headers.get("Ispower")):
                            cars = Car.objects.filter(mark=mark, price__range=[min_p, max_p], city=user.city, transmission=transmission_obj).all()
                            if cars:
                                cars = [car.to_dict() for car in cars if car.set.model.body == body and car.engine.type_fuel == fuel_type]
                                return HttpResponse(json.dumps({"response": True, "cars": cars}), content_type='application/json')
                    elif bool(headers.get("Ismyselfrange")):
                        min_price = headers.get("Minprice")
                        max_price = headers.get("Maxprice")
                    elif bool(headers.get("Isspecificamount")):
                        pass
                except Exception as e:
                    logger.error(e)
                    return HttpResponse(json.dumps({"response": True, "car": []}), content_type='application/json')
                return HttpResponse(json.dumps({"response": True, "car": []}), content_type='application/json')


class Web:
    def index(request) -> HttpResponse:
        return render(request, "index.html")
