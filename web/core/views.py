import re
import json
import csv
import codecs
import traceback
from collections import Counter
from typing import Any
from time import sleep

from loguru import logger
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models.query import QuerySet
from rest_framework.generics import ListAPIView
from django.contrib.sessions.models import Session
from django.http import HttpRequest, HttpResponse, HttpResponsePermanentRedirect

from core.models import *
from core.converts import str_to_bool, str_to_null
from core.tg.request import sendQuestion, leaveRequest
from core.utils.ip import get_client_ip
from core.utils.price import set_min_price, increase_price
from core.utils.car import sort_cars


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


class APIObj:
    class CreateBotUserView(ListAPIView):
        serializer_class: BotUser = BotUser  # Set serializer object.

        def get(self, request: HttpRequest, user_id: int, first_name: str, username: str) -> HttpResponse:
            user: QuerySet = BotUser.objects.filter(user_id=user_id)

            if not user.exists():
                BotUser.objects.create(
                    user_id=user_id, first_name=first_name, username=username)
                return HttpResponse(json.dumps({"response": True}), content_type='application/json')
            user = user.get()
            return HttpResponse(json.dumps({"response": False, "name": user.name, "city": user.city_id}), content_type='application/json')

    class SetNameView(ListAPIView):
        serializer_class: BotUser = BotUser

        def get(self, request: HttpRequest, user_id: int, name: str) -> HttpResponse:
            user: QuerySet = BotUser.objects.filter(user_id=user_id)
            user.update(name=name)
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
                min_price, max_price = increase_price(min_price)
                marks = Car.objects.filter(price__range=[min_price, max_price]).values(
                    "mark__title").distinct()
            else:
                marks = Car.objects.filter(price__range=[min_price, max_price]).values(
                    "mark__title").distinct()
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
                min_price, max_price = increase_price(min_price)
                if not mark:
                    car_filter = Car.objects.filter(
                        price__range=[min_price, max_price])
                else:
                    car_filter = Car.objects.filter(
                        mark=mark, price__lte=min_price)
            else:
                if not mark:
                    car_filter = Car.objects.filter(
                        price__range=[min_price, max_price])
                else:
                    car_filter = Car.objects.filter(
                        mark=mark, price__range=[min_price, max_price])

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
                    cars: QuerySet = Car.objects.filter(
                        price__lte=min_price).all()
                else:
                    mark: QuerySet = Mark.objects.filter(title=mark).get()
                    cars: QuerySet = Car.objects.filter(
                        mark=mark, price__lte=min_price).all()
            else:
                if mark == "any":
                    cars: QuerySet = Car.objects.filter(
                        price__range=[min_price, max_price]).all()
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
                is_any: bool = False
                mark = str_to_null(headers.get("Mark"))
                min_p = headers.get("Min-Price")
                max_p = headers.get("Max-Price")
                if str_to_bool(headers.get("Is-Volume")):
                    min_volume = float(headers.get("Min-Volume"))
                    max_volume = float(headers.get("Max-Volume"))
                    if int(max_p) == 0:
                        min_price, max_price = increase_price(min_price)
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
                                cars = [car.to_dict()
                                        for car in cars if car.mark_id == mark.pk]
                            else:
                                cars = [car.to_dict() for car in cars]
                                is_any = True
                        else:
                            if mark:
                                mark = Mark.objects.filter(title=mark).get()
                                cars = [car.to_dict(
                                ) for car in cars if car.engine.type_fuel == fuel_type and car.mark_id == mark.pk]
                            else:
                                cars = [
                                    car.to_dict() for car in cars if car.engine.type_fuel == fuel_type]
                                is_any = True
                        return HttpResponse(json.dumps({"response": True, "is_any": is_any, "cars": cars}), content_type='application/json')
                elif str_to_bool(headers.get("Is-Power")):
                    min_power: int = int(headers.get("Min-Power"))
                    max_power: int = int(headers.get("Max-Power"))
                    if int(max_p) == 0:
                        min_price, max_price = increase_price(min_price)
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
                                cars = [car.to_dict()
                                        for car in cars if car.mark_id == mark.pk]
                            else:
                                cars = [car.to_dict() for car in cars]
                                is_any = True
                        else:
                            if mark:
                                mark = Mark.objects.filter(title=mark).get()
                                cars = [car.to_dict(
                                ) for car in cars if car.engine.type_fuel == fuel_type and car.mark_id == mark.pk]
                            else:
                                cars = [
                                    car.to_dict() for car in cars if car.engine.type_fuel == fuel_type]
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
                entry = Entry.objects.create(user=user, username=username, car=car, email=email,
                                             name=name, address=address, phone=phone)
                setTypeCar = SetTypeCar.objects.filter(car=car)
                if setTypeCar.exists():
                    setTypeCar = setTypeCar.get()
                    distributor = Distributor.objects.get(distributor=setTypeCar.user)
                    set_entry = SetEntry.objects.create(
                        distributor=distributor, entry=entry)
                    distributor_file = DistributorEntryFiles.objects.create(entry=entry)
                    admin_file = AdminEntryFiles.objects.create(entry=entry)
                    set_entry.distributor_file = distributor_file
                    set_entry.admin_file = admin_file
                    set_entry.save()
                return HttpResponse(json.dumps({"response": True}), content_type='application/json')


class WebObj:
    def index(request) -> HttpResponse:
        CAPTCHA_PUBLIC_KEY = settings.CAPTCHA_PUBLIC_KEY
        cities = City.objects.all()  # Get cities
        new_cars = NewCar.objects.all()  # Get new cars
        questions = Question.objects.all()  # Get questions
        # Init car config variables
        image: None = None
        main_length: int = 0
        min_price: int = 0
        cars: None = None
        # Get request values
        pricerange = request.GET.get("pricerange")
        mark = request.GET.get("mark")
        transmission = request.GET.get("transmission")
        body = request.GET.get("body")
        type_fuel = request.GET.get("type_fuel")
        volume = request.GET.get("volume")
        power = request.GET.get("power")
        cars = p_find_car(pricerange, mark, transmission,
                          body, type_fuel, volume, power)  # Call find car function

        if cars:
            cars_values = list(cars.values())
            main_length = sum([len(v["pattern"]) for v in cars_values])
            image = cars_values[0]["pattern"][0]["image"]
            min_price = min([car["pattern"][0]["price"]
                            for car in cars_values])

        return render(request, "main/index.html", dict(cities=cities, CAPTCHA_PUBLIC_KEY=CAPTCHA_PUBLIC_KEY,
                                                       new_cars=new_cars, questions=questions, cars=cars, image=image, min_price=min_price,
                                                       main_length=main_length, mark=mark))

    def oferta(request) -> HttpResponse:
        return render(request, "main/oferta.html")

    def get_cars(request, min_price: int, max_price: int, mark: str) -> HttpResponse:
        mark = Mark.objects.get(title=mark)  # Get mark obj
        if max_price == 0:
            min_price, max_price = increase_price(min_price)
            cars = Car.objects.filter(mark=mark, price__range=[
                min_price, max_price]).all()
        else:
            cars = Car.objects.filter(mark=mark, price__range=[
                min_price, max_price]).all()
        cars = sort_cars(cars, is_price=True)
        cars = [car.to_dict() for car in cars]
        return HttpResponse(json.dumps({"response": True, "cars": cars}), content_type='application/json')

    def get_cars_by_body(request, min_price: int, max_price: int, mark: str, body: str) -> HttpResponse:
        mark = Mark.objects.get(title=mark)  # Get mark obj
        if max_price == 0:
            min_price, max_price = increase_price(min_price)
            cars = Car.objects.filter(mark=mark, price__range=[min_price, max_price],
                                      set__model__body=body).all()
        else:
            cars = Car.objects.filter(mark=mark, price__range=[min_price, max_price],
                                      set__model__body=body).all()
        cars = sort_cars(cars, is_price=True)
        cars = [car.to_dict() for car in cars]
        return HttpResponse(json.dumps({"response": True, "cars": cars}), content_type='application/json')

    def get_cars_by_type_fuel(
        request, min_price: int, max_price: int, mark: str, body: str, type_fuel: str
    ) -> HttpResponse:
        mark = Mark.objects.get(title=mark)  # Get mark obj
        if max_price == 0:
            min_price, max_price = increase_price(min_price)
            cars = Car.objects.filter(mark=mark, price__range=[min_price, max_price],
                                      set__model__body=body).all()
        else:
            cars = Car.objects.filter(mark=mark, price__range=[min_price, max_price],
                                      set__model__body=body).all()
        cars = sort_cars(cars, is_price=True)
        cars = [car.to_dict()
                for car in cars if car.engine.type_fuel == type_fuel]
        return HttpResponse(json.dumps({"response": True, "cars": cars}), content_type='application/json')

    def get_cars_by_transmission(
        request, min_price: int, max_price: int, mark: str, body: str, type_fuel: str, transmission: str
    ) -> HttpResponse:
        mark = Mark.objects.get(title=mark)  # Get mark obj
        if max_price == 0:
            min_price, max_price = increase_price(min_price)
            cars = Car.objects.filter(mark=mark, price__range=[min_price, max_price],
                                      set__model__body=body).all()
        else:
            cars = Car.objects.filter(mark=mark, price__range=[min_price, max_price],
                                      set__model__body=body, transmission__title=transmission).all()
        cars = sort_cars(cars, is_price=True)
        cars = [car.to_dict()
                for car in cars if car.engine.type_fuel == type_fuel]
        return HttpResponse(json.dumps({"response": True, "cars": cars}), content_type='application/json')

    def get_cars_by_engine_volume(
        request, min_price: int, max_price: int, mark: str, body: str, type_fuel: str, transmission: str, engine_volume: str
    ) -> HttpResponse:
        mark = Mark.objects.get(title=mark)  # Get mark obj
        if max_price == 0:
            min_price, max_price = increase_price(min_price)
            cars = Car.objects.filter(mark=mark, price__range=[min_price, max_price],
                                      set__model__body=body, transmission__title=transmission, engine__volume__lte=engine_volume).all()
        else:
            cars = Car.objects.filter(mark=mark, price__range=[min_price, max_price],
                                      set__model__body=body, transmission__title=transmission, engine__volume__lte=engine_volume).all()
        cars = sort_cars(cars, is_price=True)
        cars = [car.to_dict()
                for car in cars if car.engine.type_fuel == type_fuel]
        return HttpResponse(json.dumps({"response": True, "cars": cars}), content_type='application/json')

    def send_question(request) -> HttpResponsePermanentRedirect:
        client_ip = get_client_ip(request)
        client = WebUser.objects.filter(ip_address=client_ip)
        if not client.exists():
            WebUser.objects.create(ip_address=client_ip)
        else:
            client = client.get()
            if not client.is_blocked:
                name: Any = request.POST.get("name")
                tel: str = re.sub("[^0-9]", "", request.POST.get("tel"))
                text = request.POST.get("text")
                UserQuestion.objects.create(
                    ip_address=client_ip, name=name, phone=tel, question=text)
                response = sendQuestion(name, tel, text)
        return redirect("/")

    def leave_request(request) -> HttpResponse:
        is_new = request.POST.get("is_new")
        car_id = request.POST.get("car_id")
        name = request.POST.get("name")
        city = request.POST.get("city")
        tel = re.sub("[^0-9]", "", request.POST.get("tel"))
        email = request.POST.get("email")
        address = request.POST.get("address")
        response = leaveRequest(car_id, name, city, tel,
                                email, address, is_new)
        if is_new:
            car = NewCar.objects.get(id=car_id)
        else:
            car = Car.objects.get(id=car_id)
            entry = Entry.objects.create(car=car, email=email,
                                 name=name, address=address, phone=tel)
            setTypeCar = SetTypeCar.objects.filter(car=car)
            if setTypeCar.exists():
                setTypeCar = setTypeCar.get()
                distributor = Distributor.objects.get(distributor=setTypeCar.user)
                set_entry = SetEntry.objects.create(
                    distributor=distributor, entry=entry)
                distributor_file = DistributorEntryFiles.objects.create(entry=entry)
                admin_file = AdminEntryFiles.objects.create(entry=entry)
                set_entry.distributor_file = distributor_file
                set_entry.admin_file = admin_file
                set_entry.save()
        return HttpResponse(json.dumps({"response": True}), content_type='application/json')


class DistributorObj:
    def distributor(request, cars=None, files=None):
        if not request.user.is_authenticated:
            # Return auth page
            return redirect("distributor/auth")
        session_key = request.COOKIES.get("sessionid")
        session = Session.objects.filter(session_key=session_key)
        if not session.exists():
            return redirect("auth")
        session = session.get()
        uid = session.get_decoded().get('_auth_user_id')
        user = User.objects.get(pk=uid)
        files = File.objects.filter(user=user).all()
        cars = SetTypeCar.objects.filter(user=user, car__isnull=False).all()
        return render(request, "distributor/index.html", {
            "username": user.username, "full_name": user.get_full_name(),
            "session_key": session_key, "cars": cars, "files": files}
        )

    def auth(request):
        if request.user.is_authenticated:
            # Return main page
            return redirect("distributor")

        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            if not user.is_superuser:
                login(request, user)
                return redirect("distributor")
        return render(request, "distributor/auth.html")

    def logout_view(request):
        logout(request)
        return HttpResponse(json.dumps({"response": True}), content_type='application/json')

    def upload_csv_file(request, n=0):
        user = user_obj(request)
        distributor = Distributor.objects.filter(distributor=user)
        if not distributor.exists():
            return HttpResponse(json.dumps({"response": False, "type": "NotDistribAccount"}), content_type='application/json')
        try:
            file = request.FILES.get("file")
            reader = csv.reader(codecs.iterdecode(file, 'utf-8'))
            for r in reader:
                if n >= 1:
                    power, type_fuel, volume, transmission_id, wd_id, title, price, body, mark_id, image, color = r
                    try:
                        engine = Engine.objects.filter(
                            volume=volume, power=power, type_fuel=type_fuel)
                        if not engine.exists():
                            engine = Engine.objects.create(
                                volume=volume, power=power, type_fuel=type_fuel)
                        else:
                            engine = engine.first()
                        car = Car.objects.filter(title=title, image=image, price=price, engine=engine,
                                                 transmission_id=transmission_id, wd_id=wd_id, mark_id=mark_id)
                        if not car.exists():
                            model = Model.objects.create(
                                mark_id=mark_id, title=title, price=price, body=body, is_visible=True)
                            set = Set.objects.create(
                                model=model, title=title, image=image)
                            car = Car.objects.create(title=title, set=set, image=image, price=price, engine=engine,
                                                     transmission_id=transmission_id, wd_id=wd_id, mark_id=mark_id)
                            color_obj = Color.objects.filter(title=color)
                            if not color_obj.exists():
                                color_obj = Color.objects.create(title=color)
                            else:
                                color_obj = color_obj.get()
                            SetColor.objects.create(car=car, color=color_obj)
                            SetTypeCar.objects.create(
                                type="distributor", car=car, user=user)
                    except Exception as e:
                        traceback.print_exc()
                n += 1
            File.objects.create(file=file, user=user)
            sleep(1)
            return HttpResponse(json.dumps({"response": True}), content_type='application/json')
        except Exception as e:
            traceback.print_exc()
            return HttpResponse(json.dumps({"response": False, "error_message": e}), content_type='application/json')

    def profile(request):
        if not request.user.is_authenticated:
            # Return auth page
            return render(request, "distributor/auth.html")
        user = user_obj(request)
        distributor = Distributor.objects.filter(distributor=user)
        if distributor.exists():
            distributor = distributor.get()
        return render(request, "distributor/profile.html", {"username": user.username,
                                                            "date_joined": user.date_joined, "distributor": distributor})

    def cars(request):
        return render(request, "distributor/cars.html")

    def save_data(request):
        title = request.POST.get("title")
        image = request.FILES.get("image")
        user = user_obj(request)
        distributor = Distributor.objects.filter(distributor=user)
        if not distributor.exists():
            Distributor.objects.create(
                distributor=user, title=title, image=image)
        else:
            distributor = distributor.get()
            distributor.title = title
            distributor.image = image
            distributor.save()
        return HttpResponse(json.dumps({"response": True}), content_type='application/json')

    def orders(request):
        user = user_obj(request)
        distributor = Distributor.objects.filter(distributor=user).get()
        orders = SetEntry.objects.filter(distributor=distributor).all()
        return render(request, "distributor/orders.html", {"orders": orders})

    def upload_documents(request):
        files = request.FILES
        data = request.POST
        id = data.get("id")
        act = files.get("act")
        agreement = files.get("agreement")
        bill = files.get("bill")
        dFile = DistributorEntryFiles.objects.get(entry=SetEntry.objects.get(id=id).entry)
        dFile.act = act
        dFile.agreement = agreement
        dFile.bill = bill
        dFile.save()
        return HttpResponse(json.dumps({"response": True}), content_type='application/json')

    def distribEntryInfo(request):
        id = request.POST.get("id")
        entry = SetEntry.objects.filter(pk=id).get().to_dict(is_distributor=True)
        return HttpResponse(json.dumps({"response": True, "entry": entry}), content_type='application/json')

    def changeEntryStatus(request):
        id = request.POST.get("id")
        value = request.POST.get("value")
        if value == "1":
            status = "new"
        elif value == "2":
            status = "work"
        elif value == "3":
            status = "complete"
        setEntry = SetEntry.objects.get(id=id)
        setEntry.status = status
        setEntry.save()
        return HttpResponse(json.dumps({"response": True}), content_type='application/json')

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
        elif power:
            if max_p == 0:
                cars = Car.objects.filter(mark=mark, price__gte=min_p, engine__type_fuel=type_fuel,
                                          transmission=transmission, set__model__body=body, engine__power__lte=power).all()
            else:
                cars = Car.objects.filter(mark=mark, price__range=[min_p, max_p], engine__type_fuel=type_fuel,
                                          transmission=transmission, set__model__body=body, engine__power__lte=power).all()
        else:
            if max_p == 0:
                cars = Car.objects.filter(mark=mark, price__gte=min_p, engine__type_fuel=type_fuel,
                                          transmission=transmission, set__model__body=body, engine__power__lte=power,
                                          engine__volume__gte=volume).all()
            else:
                cars = Car.objects.filter(mark=mark, price__range=[min_p, max_p], engine__type_fuel=type_fuel,
                                          transmission=transmission, set__model__body=body, engine__power__lte=power,
                                          engine__volume__gte=volume).all()
        if cars:
            cars = [car.to_dict()
                    for car in cars if car.set.model.body == body]
            dct_cars: dict = {}
            price_arr: list = []
            for car in cars:
                pattern = {"id": car["id"], "title": car["title"], "price": car["price"], "image": car["image"], "engine_volume": car["engine"]["volume"],
                           "engine_power": car["engine"]["power"], "engine_type_fuel": car["engine"]["type_fuel"],
                           "wd": car["wd"], "transmission": car["transmission"], "body": car["body"], "set_title": car["set_title"],
                           "special": car["special"]}
                if not car["model_title"] in dct_cars:
                    dct_cars[car["model_title"]] = {"pattern": [pattern]}
                    price_arr.append(car["price"])
                else:
                    if not car["price"] in price_arr:
                        dct_cars[car["model_title"]]["pattern"].append(pattern)
                        price_arr.append(car["price"])
            dct_cars = set_min_price(dct_cars)
            return dct_cars
        else:
            return []


def user_obj(request):
    session_key = request.COOKIES.get("sessionid")
    session = Session.objects.filter(session_key=session_key)
    if not session.exists():
        return redirect("auth")
    session = session.get()
    uid = session.get_decoded().get('_auth_user_id')
    user = User.objects.get(pk=uid)
    return user
