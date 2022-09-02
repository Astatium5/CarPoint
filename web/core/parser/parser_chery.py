# Chery Tiggo 8 PRO MAX    от 3 440 900 ₽
#   - Dreamline
#   - Ultimate
#
# Chery Tiggo 8 Pro        от 2 779 900 ₽
#   - Prestige Dreamline
#   - Prestige Ultimate
#
#
# Chery Tiggo 8            от 2 479 900 ₽
#   - Prestige
#
# Chery Tiggo 7 Pro        от 2 309 900 ₽
#   - Elite
#   - Prestige
#
# Chery Tiggo 4            от 1 699 900 ₽
#   - Comfort
#   - Cosmo
#   - Travel
#
#
#(328, 4, 'Tiggo 4', 'от 1 699 900 ₽', 'Внедорожник', 1),
#(329, 4, 'Tiggo 7 Pro', 'от 2 309 900 ₽', 'Внедорожник', 1),
#(330, 4, 'Tiggo 8', 'от 2 479 900 ₽', 'Внедорожник', 1),
#(331, 4, 'Tiggo 8 Pro', 'от 2 779 900 ₽', 'Внедорожник', 1),
#(496, 4, 'Tiggo 8 PRO MAX', 'от 3 440 900 ₽', 'Внедорожник', 1);
#
#(1725, 328, 'Tiggo 4 Comfort', 'https://cdn.kodixauto.ru/media//media/image/62c6a6b2314d2d90fb1d5c20', ''),
#(1726, 328, 'Tiggo 4 Cosmo', 'https://cdn.kodixauto.ru/media//media/image/62c6a6af314d2d90fb1d5c05', ''),
#(1727, 328, 'Tiggo 4 Travel', 'https://cdn.kodixauto.ru/media//media/image/62c6a6b2314d2d90fb1d5c20', ''),
#(1728, 329, 'Tiggo 7 Pro Elite', 'https://cdn.kodixauto.ru/media//media/image/62c6a6b3314d2d90fb1d5c2b', ''),
#(1729, 329, 'Tiggo 7 Pro Prestige', 'https://cdn.kodixauto.ru/media//media/image/62c6a6b2314d2d90fb1d5c25', ''),
#(1730, 330, 'Tiggo 8 Prestige', 'https://cdn.kodixauto.ru/media//media/image/62c6a6b2314d2d90fb1d5c25', ''),
#(1731, 331, 'Tiggo 8 Pro Prestige Dreamline', 'https://cdn.kodixauto.ru/media//media/image/62c6a6b2314d2d90fb1d5c25', ''),
#(1732, 331, 'Tiggo 8 Pro Prestige Ultimate', 'https://cdn.kodixauto.ru/media//media/image/62c6a6b2314d2d90fb1d5c25', ''),
#(1733, 496, 'Tiggo 8 PRO MAX Dreamline', 'https://cdn.kodixauto.ru/media//media/image/62c6a6b2314d2d90fb1d5c25', ''),
#(1734, 496, 'Tiggo 8 PRO MAX Ultimate', 'https://cdn.kodixauto.ru/media//media/image/62c6a6b2314d2d90fb1d5c25', '');
#
#(8863, 2, 197, 'Бензин'),
#(553, 1.5, 147, 'Бензин'),
#(444, 1.5, 113, 'Бензин'),
#(551, 1.6, 186, 'Бензин'),

import json

with open('chery.dealon.online.json') as f:
    data = json.load(f)

data = data.get("data")
data = data.get("cars")

print(len(data))

image_url = "https://cdn.kodixauto.ru/media//media/image/"
n = 0
n_real = 0

city_id = 78
mark_id = 4

#715
#1250

for i in data :

    n_real += 1
    #if (n_real <= 535):
    #    continue

    price = i.get("attributes").get("price")
    name = i.get("attributes").get("marketing_complectation")
    complectation = i.get("attributes").get("complectation")
    body = i.get("attributes").get("body")
    model = i.get("attributes").get("model")
    power = i.get("attributes").get("engine").get("power")
    volume = i.get("attributes").get("engine").get("volume")
    image = i.get("attributes").get("dealer_images_id")
    wheel_drive = i.get("attributes").get("wheel_drive")
    fuel = i.get("attributes").get("fuel")
    transmission = i.get("attributes").get("transmission")
    exprnditure = i.get("attributes").get("placeholders")

    #set_id
    if (name["name"] == "Tiggo 4 Comfort"):
        set_id = 1725
    elif (name["name"] == "Tiggo 4 Cosmo"):
        set_id = 1726
    elif (name["name"] == "Tiggo 4 Travel"):
        set_id = 1727
    elif (name["name"] == "Tiggo 7 Pro Elite"):
        set_id = 1728
    elif (name["name"] == "Tiggo 7 Pro Prestige"):
        set_id = 1729
    elif (name["name"] == "Tiggo 8 Prestige"):
        set_id = 1730
    elif (name["name"] == "Tiggo 8 Pro Prestige Dreamline"):
        set_id = 1731
    elif (name["name"] == "Tiggo 8 Pro Prestige Ultimate"):
        set_id = 1732
    elif (name["name"] == "Tiggo 8 Pro Max Dreamline"):
        set_id = 1733
    elif (name["name"] == "Tiggo 8 Pro Max Ultimate"):
        set_id = 1734
    else :
        print("error set_id")
        break

    #engine_id
    if (f"""{volume["liter"]}, {power["horse_power"]}""" == "2.0, 197"):
        engine_id = 8863
    elif (f"""{volume["liter"]}, {power["horse_power"]}""" == "1.5, 147"):
        engine_id = 553
    elif (f"""{volume["liter"]}, {power["horse_power"]}""" == "1.5, 113"):
        engine_id = 444
    elif (f"""{volume["liter"]}, {power["horse_power"]}""" == "1.6, 186"):
        engine_id = 551
    else :
        print("error engine_id")
        break

    #transmission_id
    if (transmission["name"] == "Роботизированная" or transmission["name"] == "Вариатор"):
        transmission_id = 1
    elif (transmission["name"] == "МКПП"):
        transmission_id = 2
    elif (transmission["name"] == "АКПП"):
        transmission_id = 1
    else :
        print("transmission_id")
        break
    print(transmission_id)
    print(name["name"])

    #wd_id
    if (wheel_drive["name"] == "Полный"):
        wd_id = 1
    elif (wheel_drive["name"] == "Передний"):
        wd_id = 2
    elif (wheel_drive["name"] == "Задний"):
        wd_id = 3
    else :
        print("twd_id")
        break


    #print(f"""({n}, 'Chery {name["name"]}', {set_id}, '{image_url+image[0]}', {price}, {engine_id}, {transmission_id}, {wd_id}, '{exprnditure["${car.specifications.fuel_composite.value}"]} л. смешанный', {city_id}, {mark_id}),""")

    n += 1
