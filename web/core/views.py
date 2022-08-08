from distutils.command import check
import json
from collections import Counter
from tkinter import E

from loguru import logger
from django.shortcuts import render
from django.db.models.query import QuerySet
from rest_framework.generics import ListAPIView
from django.http import HttpRequest, HttpResponse

from .models import *
from .converts import str_to_bool


PRICE_RANGE: dict = {
    "500 000₽ - 2 000 000₽": {
        "min": 500000,
        "max": 2000000
    },

    "2 000 000₽ - 4 000 000₽": {
        "min": 2000000,
        "max": 4000000
    },

    "4 000 000₽ - 6 000 000₽": {
        "min": 4000000,
        "max": 6000000
    },

    "более 6 000 000₽": {
        "min": 6000000,
        "max": 0
    },
}  # Keys is ids price range.


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
            mark = Mark.objects.get(title=mark)
            if Car.objects.filter(mark_id=mark.pk).exists():
                queryset: QuerySet = Model.objects.filter(mark=mark.pk).all()
                counter = Counter([model.body for model in queryset if Set.objects.filter(model=model).exists()])
                bodies = list(counter.keys())
                return HttpResponse(json.dumps({"all_bodies": bodies}), content_type='application/json')
            else:
                return HttpResponse(json.dumps({"all_bodies": []}), content_type='application/json')


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
            body: str, fuel_type: str, user_id: int
        ):
            headers = request.headers
            try:
                user = BotUser.objects.get(user_id=user_id)
                mark = Mark.objects.filter(title=headers.get("Mark")).get()
                min_p = headers.get("Min-Price")
                max_p = headers.get("Max-Price")
                if str_to_bool(headers.get("Is-Volume")):
                    min_volume = float(headers.get("Min-Volume"))
                    max_volume = float(headers.get("Max-Volume"))
                    if int(max_p) == 0:
                        cars = Car.objects.filter(mark=mark, price__gte=min_p, engine__volume__range=[min_volume, max_volume],
                            city=user.city).all()
                    else:
                        cars = Car.objects.filter(mark=mark, price__range=[min_p, max_p], engine__volume__range=[min_volume, max_volume],
                            city=user.city).all()
                    if cars:
                        if str_to_bool(headers.get("Is-Any-Fuel-Type")):
                            cars = [car.to_dict() for car in cars if car.set.model.body == body]
                        else:
                            cars = [car.to_dict() for car in cars
                                if car.set.model.body == body and car.engine.type_fuel == fuel_type]
                        return HttpResponse(json.dumps({"response": True, "cars": cars}), content_type='application/json')
                elif str_to_bool(headers.get("Is-Power")):
                    min_power = int(headers.get("Min-Power"))
                    max_power = int(headers.get("Max-Power"))
                    if int(max_p) == 0:
                        cars = Car.objects.filter(mark=mark, price__gte=min_p, engine__power__range=[min_power, max_power],
                            city=user.city).all()
                    else:
                        cars = Car.objects.filter(mark=mark, price__range=[min_p, max_p], engine__power__range=[min_power, max_power],
                            city=user.city).all()
                    if cars:
                        if str_to_bool(headers.get("Is-Any-Fuel-Type")):
                            cars = [car.to_dict() for car in cars if car.set.model.body == body]
                        else:
                            cars = [car.to_dict() for car in cars
                                if car.set.model.body == body and car.engine.type_fuel == fuel_type]
                        return HttpResponse(json.dumps({"response": True, "cars": cars}), content_type='application/json')
            except Exception as e:
                logger.error(e)
                return HttpResponse(json.dumps({"response": True, "cars": []}), content_type='application/json')
            return HttpResponse(json.dumps({"response": True, "cars": []}), content_type='application/json')


    class GetCarInfoView(ListAPIView):
        serializer_class: Car = Car

        def get(self, request: HttpRequest, id: int):
            car = Car.objects.get(id=id)
            return HttpResponse(json.dumps({"response": True, "car": car.to_dict()}), content_type='application/json')


    class CreateEntry(ListAPIView):
        serializer_class: Entry = Entry

        def get(self,
            request: HttpRequest, user_id: int, username: str, car_id: int,
            email: str, name: str, address: str, phone: int
        ) -> HttpResponse:
            user = BotUser.objects.get(user_id=user_id)
            car = Car.objects.get(id=car_id)
            entry = Entry.objects.filter(user=user, username=username, car=car, email=email,
                name=name, address=address, phone=phone)
            if entry.exists():
                return HttpResponse(json.dumps({"response": False}), content_type='application/json')
            else:
                Entry.objects.create(user=user, username=username, car=car, email=email,
                name=name, address=address, phone=phone)
                return HttpResponse(json.dumps({"response": True}), content_type='application/json')


class Web:
    def index(request) -> HttpResponse:
        data = selected_data()
        return render(request, "index.html", data)

    def oferta(request):
        return render(request, "oferta.html")

    def find_car(request):
        city = request.POST.get("city")
        pricerange = request.POST.get("pricerange")
        mark = request.POST.get("mark")
        transmission = request.POST.get("transmission")
        body = request.POST.get("body")
        type_fuel = request.POST.get("type_fuel")
        engine = request.POST.get("engine")

        data = selected_data()
        data.update({"is_search": True, "car": p_find_car(
            city, pricerange, mark, transmission, body,  type_fuel, engine),
            "car": None})
        return render(request, "index.html", data)

    
def selected_data() -> dict:
    cities = City.objects.all()
    marks = Mark.objects.all()
    str_engine_obj = [engine.__str__() for engine in Engine.objects.all()]
    str_model_obj = [model.__str__() for model in Model.objects.all()]
    type_fuels = [engine.type_fuel for engine in Engine.objects.all()]
    engine_counter = Counter(str_engine_obj)
    model_counter = Counter(str_model_obj)
    type_fuel_counter = Counter(type_fuels)
    return {"cities": cities, "marks": marks, "engines": engine_counter, "models": model_counter,
             "type_fuels": type_fuel_counter}

def p_find_car(
    city: str, pricerange: str, mark: str, transmission: str,
    body: str, type_fuel: str, engine: str
) -> bool:
    price_range = PRICE_RANGE.get(pricerange)
    if not pricerange:
        return []
    else:
        min_p = int(price_range.get("min"))
        max_p = int(price_range.get("max"))
        mark = Mark.objects.filter(title=mark).get()
        city = City.objects.filter(title=city).get()
        transmission = Transmission.objects.filter(title=transmission)
        if max_p == 0:
            cars = Car.objects.filter(mark=mark, price__gte=min_p, 
                            city=city).all()
        else:
            cars = Car.objects.filter(mark=mark, price__range=[min_p, max_p],
                            city=city).all()
        print(cars)
        return cars
