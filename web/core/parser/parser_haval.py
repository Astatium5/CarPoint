#
# Haval, Geely, Chery, Changan
#
# В Haval нужно только -
#                    HAVAL DARGO
#                    GWM POER

from fake_useragent import UserAgent
import requests
import json

url = "https://haval.ru/api/cars/list/?is_new=y&brands=5ce7dad4d999da000129d913%2C5ce7dad4d999da000129d905&cities=%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0"


user_agnt = UserAgent()

r = requests.get(url, headers={'user-agent': f'{user_agnt.random}'})

print(r.status_code)

x = json.loads(r.text)

c = x.get('data')

dargo_n = 0
poer_n = 0

arrg_1 = "name"
arrg_2 = "horse_power"
arrg_3 = "liter"
id = 24301

for i in c :
    v1 = i.get("attributes")
    v2 = v1.get("model")
    name = v2.get("name")
    if (name == 'Poer'):
        dargo_n += 1

        id += 1 #

        v2 = v1.get("marketing_complectation")
        text = v1.get("marketing_complectation")
        title = text[arrg_1] #


        v2 = v1.get("complectation")
        text = v1.get("complectation")
        if (text[arrg_1] == 'Premium'):
            set_id = 1713
        if (text[arrg_1] == 'Comfort'):
            set_id = 1714

        v2 = v1.get("stock_images_id")
        text = v1.get("stock_images_id")
        image = "https://cdn.kodixauto.ru/media/image/"+text[0] #

        text = v1.get("price")
        price = text #

        engine_id = 10424 #

        v2 = v1.get("transmission")
        text = v1.get("transmission")
        if (text[arrg_1]) == "АКПП" :
            transmission_id = 1 #
        else :
            transmission_id = 2 #

        v2 = v1.get("wheel_drive")
        text = v1.get("wheel_drive")
        if (text[arrg_1]) == "Полный" :
            wd_id = 1 #
        elif (text[arrg_1]) == "Передний" :
            wd_id = 2 #
        else :
            wd_id = 3 #

        #v2 = v1.get("placeholders")
        #text = v1.get("${car.specifications.fuel_composite.value}")
        expenditure = 9.5 #

        city_id = 78 #

        mark_id = 1

        print(f"""({id}, '{title}', {set_id}, '{image}', {price}, {engine_id}, {transmission_id}, {wd_id}, '{expenditure} л.. смешанный', {city_id}, {mark_id}),""")




#`cars` (`id`,`title`,`set_id`,`image`,`price`,`engine_id`,`transmission_id`,`wd_id`,`expenditure`,`city_id`,`mark_id`)
