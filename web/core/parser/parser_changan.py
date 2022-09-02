from bs4 import BeautifulSoup
#
#(10427, 1.6, 128, 'бензин');
#
#(14, 'Changan', 1),
#
#   models
#
#(497, 14, 'Changan CS55', 'от 2 029 900 руб', 'Внедорожник', 1),
#(498, 14, 'Changan CS75FL', 'от 2 279 900 руб', 'Внедорожник', 1),
#(499, 14, 'Changan CS35 Plus', 'от 1 869 900 руб', 'Внедорожник', 1);

#   set_id
#
#(1735, 497, 'Changan CS55 Luxury', '', ''),
#(1736, 497, 'Changan CS55 Comfort', '', ''),
#(1737, 498, 'Changan CS75FL Luxe', '', ''),
#(1738, 498, 'Changan CS75FL Comfort', '', ''),
#(1739, 499, 'Changan CS35 Plus Comfort'),
#(1740, 499, 'Changan CS35 Plus Luxe', '', '');
#
#
#
#

image_link = "https://cena-auto.ru/modules/available/src/images/cars/"
car_id = 25859
engine_id = 10427

wd_id = 0
city_id = 78
mark_id = 14

def changan_main():
    with open("chagan5.html", "r") as f:
        all_page = f.read()

    all_page = BeautifulSoup(all_page, "lxml")

    all_page = all_page.find_all(class_="Model-item Model-item--with_actions u-size4of12 u-lg-size3of12 js-available_car_card")

    for page in all_page :

        name = page.find(class_="Model-title")

        if ("CS55" in name.text):
            if ("Luxury" in name.text):
                set_id = 1735
            elif ("Comfort" in name.text):
                set_id = 1736
            else :
                print("err set_id in CS55")
        elif ("CS75FL" in name.text):
            if ("Luxe" in name.text):
                set_id = 1737
            elif ("Comfort" in name.text):
                set_id = 1738
            else :
                print("err set_id in CS75FL")
        elif ("CS35" in name.text):
            if ("Comfort" in name.text):
                set_id = 1739
            elif ("Luxe" in name.text):
                set_id = 1740
            else :
                print("err set_id in CS35")
        else :
            print("err in set_id")
            break

        image_url = page.find(class_="Model-photo Model-photo--available").find("img").get("src")
        image_ur = image_url.split("/")

        price = page.find(class_="Model-price")

        transmission_id = page.find(class_="Model-description")

        if ("AT" in transmission_id.text):
            transmission_id = 1
        elif ("MT" in transmission_id.text):
            transmission_id = 2
        else :
            print("err in transmission_id")
            break

        wd_id = page.find(class_="Model-description")
        if ("передний привод" in wd_id.text):
            wd_id = 2
        elif ("полный привод"):
            wd_id = 1
        else :
            print("erer in wd_id")
            break

        print(f"""({car_id}, '{name.text}', {set_id}, '{image_link+image_ur[1]}', {price.text.replace(' ', '').replace('P', '')}, {engine_id}, {transmission_id}, {wd_id}, 'нет данных', {city_id}, {mark_id}),""")

        car_id += 1

    #<img src="/modules/available/src/images/cars/1866859.jpg" alt="Новый Changan CS35 Plus, кроссовер, 1.6 MT (128 л.с.), бензин, передний привод, Comfort 1.6 5MT, 2021 в Ростове-на-Дону">

    #<p class="Model-title">Changan CS35 Plus, кроссовер, Comfort 1.6 5MT</p>

    #<div class="Model-text"><p class="Model-title">Changan CS35 Plus, кроссовер, Comfort 1.6 5MT</p><p class="Model-description">2021, 1.6 MT (128 л.с.), бензин, передний привод, Ростов-на-Дону</p><p class="Model-price">1 959 900 <span class="ruble">P</span></p><p class="Model-price-credit js-available_car_credit_link" data-href="/credit/?credit_amount=1959900">от 39 646 <span class="ALSRubl">i</span>/мес</p><div class="Model-actions js-available_car_actions" style="display: none;"><button class="Button Button--card-order_available_car Button--card-has_order_available_car Button--gray Button--with_arrow Button--arrow_gray Button--always_hidden js-has_order_available_car_button">Забронирован</button><button class="Button Button--card-order_available_car Button--filled-green js-order_available_car_button" data-modal_id="modal-auth" data-block_type="2" data-car_id="1866859" data-car_id_ilsa="4252154" data-preview_image_src="/modules/available/src/images/cars/1866859.jpg" data-car_title="Changan CS35 Plus" data-car_price="1 959 900" data-car_description="Changan CS35 Plus, кроссовер, 1.6 MT (128 л.с.), передний привод, бензин, Comfort 1.6 5MT, цвет серый" data-dealer_title="Чанган Центр Сокол Малиновского, Ростов-на-Дону, ул. Малиновского, 17В" data-price_value_slice_date="вчера, 19:20">Забронировать</button><button class="Button Button--large-green Button--icon_phone Button--callback_request Button--card-callback_request" data-modal_id="modal-dealer_callback_request" data-dealer_id="7641" data-dealer_title="Чанган Центр Сокол Малиновского" data-available_car_id="1866859">Заказать звонок</button></div></div>

    #<p class="Model-price">1 959 900 <span class="ruble">P</span></p>
