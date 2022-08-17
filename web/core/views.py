import json
from collections import Counter

from loguru import logger
from django.shortcuts import render
from django.db.models.query import QuerySet
from rest_framework.generics import ListAPIView
from django.http import HttpRequest, HttpResponse

from .models import *
from .converts import str_to_bool, str_to_null


PRICE_RANGE: dict = {
    "1": {
        "min": 500000,
        "max": 2000000
    },

    "2": {
        "min": 2000000,
        "max": 4000000
    },

    "3": {
        "min": 4000000,
        "max": 6000000
    },

    "4": {
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
                BotUser.objects.create(
                    user_id=user_id, first_name=first_name, username=username)
                return HttpResponse(json.dumps({"response": True}), content_type='application/json')
            user = queryset.get()
            return HttpResponse(json.dumps({"response": False, "name": user.name, "city": user.city_id}), content_type='application/json')

    class SetNameView(ListAPIView):
        serializer_class: BotUser = BotUser

        def get(self, request: HttpRequest, user_id: int, name: str) -> HttpResponse:
            queryset: QuerySet = BotUser.objects.filter(user_id=user_id)
            queryset.update(name=name)
            return HttpResponse(json.dumps({"response": True}), content_type='application/json')

    class SetCityView(ListAPIView):
        serializer_class: BotUser = BotUser

        def get(self, request: HttpRequest, user_id: int, city: str) -> HttpResponse:
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

        def get(self, request: HttpRequest, user_id: int) -> HttpResponse:
            queryset: QuerySet = BotUser.objects.get(user_id=user_id)

            if queryset.phone:
                return HttpResponse(json.dumps({"response": True}), content_type='application/json')
            else:
                return HttpResponse(json.dumps({"response": False}), content_type='application/json')

    class SetPhoneView(ListAPIView):
        serializer_class: BotUser = BotUser

        def get(self, request: HttpRequest, user_id: int, phone: int) -> HttpResponse:
            queryset: QuerySet = BotUser.objects.filter(user_id=user_id)
            queryset.update(phone=phone)
            return HttpResponse(json.dumps({"response": True}), content_type='application/json')

    class GetAllMarksView(ListAPIView):
        serializer_class: BotUser = BotUser

        def get(self, request: HttpRequest, min_price: int, max_price: int) -> HttpResponse:
            if max_price == 0:
                marks = Car.objects.filter(price__lte=min_price).values("mark__title").distinct()
            else:
                marks = Car.objects.filter(price__range=[min_price, max_price]).values("mark__title").distinct()
            all_marks = [mark.get("mark__title") for mark in marks]
            return HttpResponse(json.dumps({"all_marks": all_marks}), content_type='application/json')

    class GetAllBodiesView(ListAPIView):
        serializer_class: Model = Model

        def get(self, request: HttpRequest, mark: str, min_price: int, max_price: int) -> HttpResponse:
            if mark != "any":
                mark = Mark.objects.get(title=mark)
            else:
                mark = None
            if max_price == 0:
                if not mark:
                    car_filter = Car.objects.filter(price__lte=min_price)
                else:
                    car_filter = Car.objects.filter(mark=mark, price__lte=min_price)
            else:
                if not mark:
                    car_filter = Car.objects.filter(price__lte=min_price)
                else:
                    car_filter = Car.objects.filter(mark=mark, price__range=[min_price, max_price])

            if car_filter.exists():
                cars = car_filter.all()
                bodies = [car.set.model.body for car in cars]
                counter = Counter(bodies)
                bodies = list(counter.keys())
                return HttpResponse(json.dumps({"all_bodies": bodies}), content_type='application/json')
            else:
                return HttpResponse(json.dumps({"all_bodies": []}), content_type='application/json')

    class GetAllFuelTypesView(ListAPIView):
        serializer_class: Engine = Engine

        def get(self, request: HttpRequest, mark: str, body: str, min_price: int, max_price: int) -> HttpResponse:
            if max_price == 0:
                if mark == "any":
                    cars: QuerySet = Car.objects.filter(price__lte=min_price).all()
                else:
                    mark: QuerySet = Mark.objects.filter(title=mark).get()
                    cars: QuerySet = Car.objects.filter(
                        mark=mark, price__lte=min_price).all()
            else:
                if mark == "any":
                    cars: QuerySet = Car.objects.filter(price__range=[min_price, max_price]).all()
                else:
                    mark: QuerySet = Mark.objects.filter(title=mark).get()
                    cars: QuerySet = Car.objects.filter(
                        mark=mark, price__range=[min_price, max_price]).all()
            engines = [
                car.engine.type_fuel for car in cars if car.set.model.body == body]
            counter = Counter(engines)
            fuel_types = list(counter.keys())
            return HttpResponse(json.dumps({"all_fuel_types": fuel_types}), content_type='application/json')

    class FindCarView(ListAPIView):
        serializer_class: Car = Car

        def get(self, request: HttpRequest, body: str, fuel_type: str) -> HttpResponse:
            headers = request.headers
            try:
                mark = str_to_null(headers.get("Mark"))
                min_p = headers.get("Min-Price")
                max_p = headers.get("Max-Price")
                if str_to_bool(headers.get("Is-Volume")):
                    min_volume = float(headers.get("Min-Volume"))
                    max_volume = float(headers.get("Max-Volume"))
                    if int(max_p) == 0:
                        min_price = int(min_p) - 500000
                        max_price = int(min_p) + 300000
                        cars = Car.objects.filter(price__range=[min_price, max_price], engine__volume__range=[
                                                  min_volume, max_volume]).all()
                    else:
                        cars = Car.objects.filter(price__range=[
                                                  min_p, max_p], engine__volume__range=[min_volume, max_volume],
                                                  set__model__body=body).all()
                    if cars:
                        if str_to_bool(headers.get("Is-Any-Fuel-Type")):
                            if mark:
                                mark = Mark.objects.filter(title=mark).get()
                                cars = [car.to_dict() for car in cars if car.mark_id == mark.pk]
                                is_any = False
                            else:
                                cars = [car.to_dict() for car in cars]
                                is_any = True
                        else:
                            if mark:
                                mark = Mark.objects.filter(title=mark).get()
                                cars = [car.to_dict() for car in cars if car.engine.type_fuel == fuel_type and car.mark_id == mark.pk]
                                is_any = False
                            else:
                                cars = [car.to_dict() for car in cars if car.engine.type_fuel == fuel_type]
                                is_any = True
                        return HttpResponse(json.dumps({"response": True, "is_any": is_any, "cars": cars}), content_type='application/json')
                elif str_to_bool(headers.get("Is-Power")):
                    min_power = int(headers.get("Min-Power"))
                    max_power = int(headers.get("Max-Power"))
                    if int(max_p) == 0:
                        min_price = int(min_p) - 500000
                        max_price = int(min_p) + 300000
                        cars = Car.objects.filter(price__range=[min_price, max_price], engine__power__range=[
                                                  min_power, max_power],
                                                  set__model__body=body).all()
                    else:
                        cars = Car.objects.filter(price__range=[
                                                  min_p, max_p], engine__power__range=[min_power, max_power],
                                                  set__model__body=body).all()
                    if cars:
                        if str_to_bool(headers.get("Is-Any-Fuel-Type")):
                            if mark:
                                mark = Mark.objects.filter(title=mark).get()
                                cars = [car.to_dict() for car in cars if car.mark_id == mark.pk]
                                is_any = False
                            else:
                                cars = [car.to_dict() for car in cars]
                                is_any = True
                        else:
                            if mark:
                                mark = Mark.objects.filter(title=mark).get()
                                cars = [car.to_dict() for car in cars if car.engine.type_fuel == fuel_type and car.mark_id == mark.pk]
                                is_any = False
                            else:
                                cars = [car.to_dict() for car in cars if car.engine.type_fuel == fuel_type]
                                is_any = True
                        return HttpResponse(json.dumps({"response": True, "is_any": is_any, "cars": cars}), content_type='application/json')
            except Exception as e:
                logger.error(e)
                return HttpResponse(json.dumps({"response": True, "cars": []}), content_type='application/json')

    class GetCarInfoView(ListAPIView):
        serializer_class: Car = Car

        def get(self, request: HttpRequest, id: int) -> HttpResponse:
            car = Car.objects.get(id=id)
            return HttpResponse(json.dumps({"response": True, "car": car.to_dict()}), content_type='application/json')

    class CreateEntryView(ListAPIView):
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
        is_search = False
        image = None
        main_length = 0
        min_price = 0
        cars = None
        pricerange = request.GET.get("pricerange")
        mark = request.GET.get("mark")
        transmission = request.GET.get("transmission")
        body = request.GET.get("body")
        type_fuel = request.GET.get("type_fuel")
        volume = request.GET.get("volume")
        power = request.GET.get("power")
        cars = p_find_car(pricerange, mark, transmission, body, type_fuel, volume, power)

        if cars:
            main_length = sum([len(v) for v in cars.values()])
            cars_values = list(cars.values())
            is_search = True
            image = cars_values[0][0]["image"]
            min_price = min([car["price"] for car in cars_values[0]])

        return render(request, "index.html", dict(
                is_search=is_search, cars=cars, image=image, min_price=min_price,
                main_length=main_length, mark=mark))

    def oferta(request) -> HttpResponse:
        return render(request, "oferta.html")

    def get_cars(request, min_price: int, max_price: int, mark: str):
        mark = Mark.objects.get(title=mark)
        if max_price == 0:
            min_price = min_price - 500000
            max_price = min_price + 300000
            cars = Car.objects.filter(mark=mark, price__range=[min_price, max_price]).all()
        else:
            cars = Car.objects.filter(mark=mark, price__range=[min_price, max_price]).all()
        cars = [car.to_dict() for car in cars]
        return HttpResponse(json.dumps({"response": True, "cars": cars}), content_type='application/json')

    def get_cars_by_body(request, min_price: int, max_price: int, mark: str, body: str):
        mark = Mark.objects.get(title=mark)
        if max_price == 0:
            min_price = min_price - 500000
            max_price = min_price + 300000
            cars = Car.objects.filter(mark=mark, price__range=[min_price, max_price],
                set__model__body=body).all()
        else:
            cars = Car.objects.filter(mark=mark, price__range=[min_price, max_price],
                set__model__body=body).all()
        cars = [car.to_dict() for car in cars]
        return HttpResponse(json.dumps({"response": True, "cars": cars}), content_type='application/json')

    def get_cars_by_type_fuel(request, min_price: int, max_price: int, mark: str, body: str, type_fuel: str):
        mark = Mark.objects.get(title=mark)
        if max_price == 0:
            min_price = min_price - 500000
            max_price = min_price + 300000
            cars = Car.objects.filter(mark=mark, price__range=[min_price, max_price],
                set__model__body=body).all()
        else:
            cars = Car.objects.filter(mark=mark, price__range=[min_price, max_price],
                set__model__body=body).all()
        cars = [car.to_dict() for car in cars if car.engine.type_fuel == type_fuel]
        return HttpResponse(json.dumps({"response": True, "cars": cars}), content_type='application/json')


def p_find_car(
    pricerange: str, mark: str, transmission: str,
    body: str, type_fuel: str, volume: str, power: str
) -> list:
    if not pricerange or not mark or not transmission or not body or not type_fuel:
        return []
    else:
        price_range = PRICE_RANGE.get(pricerange)
        min_p = int(price_range.get("min"))
        max_p = int(price_range.get("max"))
        mark = Mark.objects.filter(title=mark).get()
        transmission = Transmission.objects.filter(title=transmission).get()
        if not volume and not power:
            return []
        elif volume:
            if max_p == 0:
                cars = Car.objects.filter(mark=mark, price__gte=min_p, engine__type_fuel=type_fuel,
                                        transmission=transmission, set__model__body=body, engine__volume__lte=volume).all()
            else:
                cars = Car.objects.filter(mark=mark, price__range=[min_p, max_p], engine__type_fuel=type_fuel,
                                        transmission=transmission, set__model__body=body, engine__volume__lte=volume).all()
            cars = [car for car in cars if car.set.model.body == body]
        elif power:
            if max_p == 0:
                cars = Car.objects.filter(mark=mark, price__gte=min_p, engine__type_fuel=type_fuel,
                                        transmission=transmission, set__model__body=body, engine__power__lte=power).all()
            else:
                cars = Car.objects.filter(mark=mark, price__range=[min_p, max_p], engine__type_fuel=type_fuel,
                                        transmission=transmission, set__model__body=body, engine__power__lte=power).all()
            cars = [car for car in cars if car.set.model.body == body]
        else:
            if max_p == 0:
                cars = Car.objects.filter(mark=mark, price__gte=min_p, engine__type_fuel=type_fuel,
                                        transmission=transmission, set__model__body=body, engine__power__lte=power,
                                        engine__volume__gte=volume).all()
            else:
                cars = Car.objects.filter(mark=mark, price__range=[min_p, max_p], engine__type_fuel=type_fuel,
                                        transmission=transmission, set__model__body=body, engine__power__lte=power,
                                        engine__volume__gte=volume).all()
            cars = [car for car in cars if car.set.model.body == body]
        cars = [car.to_dict() for car in cars]
        if cars:
            dct_cars = {}
            for car in cars:
                pattern = {"price": car["price"], "image": car["image"], "engine_volume": car["engine_volume"],
                    "engine_power": car["engine_power"], "engine_type_fuel": car["engine_type_fuel"],
                    "wd": car["wd"], "transmission": car["transmission"], "body": car["body"], "set_title": car["set_title"]}
                if not car["title"] in dct_cars:
                    dct_cars[car["title"]] = [pattern]
                else:
                    dct_cars[car["title"]].append(pattern)
        return dct_cars
