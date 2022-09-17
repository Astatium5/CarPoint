#
# Haval, Geely, Chery, Changan
#
# В Haval нужно только -
#                    HAVAL DARGO
#                    GWM POER

from fake_useragent import UserAgent
import requests
import json

from core.models import Car

URL = "https://haval.ru/api/cars/list/?is_new=y&brands=5ce7dad4d999da000129d913%2C5ce7dad4d999da000129d905&cities=%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0"
USER_AGENT = UserAgent()

EXPENDITURE = "9.5 л.. смешанный"
CITY_ID = 78
MARK_ID = 1
ENGINE_ID = 10424


def haval_main(dargo_n=0, poer_n=0, name_arg="name", horse_p_arg="horse_power", liter_arg="liter"):
    r = requests.get(URL, headers={'user-agent': f'{USER_AGENT.random}'})
    x = json.loads(r.text)
    c = x.get('data')

    for i in c :
        v1 = i.get("attributes")
        v2 = v1.get("model")
        name = v2.get("name")
        if (name == 'Poer'):
            dargo_n += 1

            v2 = v1.get("marketing_complectation")
            text = v1.get("marketing_complectation")
            title = text[name_arg]

            v2 = v1.get("complectation")
            text = v1.get("complectation")
            set_id = get_set_id(text, name_arg)

            v2 = v1.get("stock_images_id")
            text = v1.get("stock_images_id")
            image = "https://cdn.kodixauto.ru/media/image/"+text[0]

            text = v1.get("price")
            price = text

            v2 = v1.get("transmission")
            text = v1.get("transmission")
            transmission_id = get_transmission_id(text, name_arg)

            v2 = v1.get("wheel_drive")
            text = v1.get("wheel_drive")
            wd_id = get_wd_id(text, name_arg)

            #v2 = v1.get("placeholders")
            #text = v1.get("${car.specifications.fuel_composite.value}")

            car = Car.objects.filter(title=title, set_id=set_id, image=image, price=int(price), engine_id=ENGINE_ID, transmission_id=transmission_id, wd_id=wd_id,
                expenditure=EXPENDITURE, city_id=CITY_ID, mark_id=MARK_ID)

            if not car.exists():
                Car.objects.create(title=title, set_id=set_id, image=image, price=int(price), engine_id=ENGINE_ID, transmission_id=transmission_id, wd_id=wd_id,
                expenditure=EXPENDITURE, city_id=CITY_ID, mark_id=MARK_ID)

def get_set_id(text, arg):
    if text[arg] == "Premium":
        return 1713
    elif text[arg] == "Comfort":
        return 1714

def get_transmission_id(text, arg):
    if text[arg] == "АКПП" :
        return 1
    else :
        return 2

def get_wd_id(text, arg):
    if text[arg] == "Полный":
        return 1
    elif text[arg] == "Передний":
        return 2
    else :
        return 3
