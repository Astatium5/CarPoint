from email import header
import json
from collections import Counter

from loguru import logger
from django.shortcuts import render
from django.db.models.query import QuerySet
from requests import head
from rest_framework.generics import ListAPIView
from django.http import HttpRequest, HttpResponse

from .models import *


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

        def get(self, request: HttpRequest, mark: str, body: str, user_id: int, min_price: int, max_price: int):
            user = BotUser.objects.get(user_id=user_id)
            mark: QuerySet = Mark.objects.filter(title=mark).get()
            if max_price == 0:
                cars: QuerySet = Car.objects.filter(mark=mark, price__gte=min_price).all()
            else:
                cars: QuerySet = Car.objects.filter(mark=mark, price__range=[min_price, max_price]).all()
            engines = [car.engine.type_fuel for car in cars if car.set.model.body == body and car.city == user.city]
            counter = Counter(engines)
            fuel_types = list(counter.keys())
            return HttpResponse(json.dumps({"all_fuel_types": fuel_types}), content_type='application/json')


    class FindCarView(ListAPIView):
        serializer_class: Car = Car

        def get(self, request: HttpRequest,
            body: str, fuel_type: str, transmission: str, user_id: int
        ):
            headers = request.headers
            try:
                user = BotUser.objects.get(user_id=user_id)
                mark = Mark.objects.filter(title=headers.get("Mark")).get()
                transmission = Transmission.objects.filter(title=transmission).get()
                min_p = headers.get("Min-Price")
                max_p = headers.get("Max-Price")
                if bool(headers.get("Is-Volume")):
                    min_volume = float(headers.get("Min-Volume"))
                    max_volume = float(headers.get("Max-Volume"))
                    if int(max_p) == 0:
                        cars = Car.objects.filter(mark=mark, price__gte=min_p, engine__volume__range=[min_volume, max_volume],
                            city=user.city, transmission=transmission).all()
                    else:
                        cars = Car.objects.filter(mark=mark, price__range=[min_p, max_p], engine__volume__range=[min_volume, max_volume],
                            city=user.city, transmission=transmission).all()
                    if cars:
                        cars = [car.to_dict() for car in cars
                            if car.set.model.body == body and car.engine.type_fuel == fuel_type]
                        return HttpResponse(json.dumps({"response": True, "cars": cars}), content_type='application/json')
                if bool(headers.get("Is-Power")):
                    min_power = int(headers.get("Min-Power"))
                    max_power = int(headers.get("Max-Power"))
                    if int(max_p) == 0:
                        cars = Car.objects.filter(mark=mark, price__gte=min_p, engine__power__range=[min_power, max_power],
                            city=user.city, transmission=transmission).all()
                    else:
                        cars = Car.objects.filter(mark=mark, price__range=[min_p, max_p], engine__power__range=[min_power, max_power],
                            city=user.city, transmission=transmission).all()
                    if cars:
                        cars = [car.to_dict() for car in cars if car.set.model.body == body and car.engine.type_fuel == fuel_type]
                        return HttpResponse(json.dumps({"response": True, "cars": cars}), content_type='application/json')
            except Exception as e:
                logger.error(e)
                return HttpResponse(json.dumps({"response": True, "car": []}), content_type='application/json')
            return HttpResponse(json.dumps({"response": True, "car": []}), content_type='application/json')


class Web:
    def index(request) -> HttpResponse:
        return render(request, "index.html")
