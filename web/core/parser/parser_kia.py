import requests
import re
from bs4 import BeautifulSoup
from mysql.connector import MySQLConnection, Error
from python_mysql_dbconfig import read_db_config
import pprint
import time
start_time = time.time()

url = 'https://www.kia.ru/models/'
url_model = 'https://www.kia.ru'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
cars = {}
all = {

}

cars_model = []  # ++ 1
cars_photo = []  # 1
cars_link = []  # +
cars_options = []  # +
cars_config = []  # + много
cars_config_name = []  # +
cars_config_price = []  # +
cars_config_options = []  # +
cars_config_engine = []
cars_config_power_engine = []
cars_config_type_engine = []
cars_config_transmission = []
cars_config_drive_unit = []
cars_config_consumption = []
cars_config_color = []
cars_config_lib = []
configur = []
cost = []

cars_name = soup.find_all('div', class_='car-card__name-block')  # Получаем список всех моделей
for i in range(len(cars_name)):
    href_soup = cars_name[i].find_all('a')  # Получаем ссылку на каждую модель
    cars_link.append(href_soup[0].get('href'))  # Присваевываем в лист ссылку на модель

for i in range(len(cars_link)):
    response_link = requests.get(url_model + cars_link[i])

    soup_link = BeautifulSoup(response_link.text, 'html.parser')
    cars_options_soup = soup_link.find_all('nav', class_='model-header-panel__nav__menu')

    href_options_soup = cars_options_soup[0].find_all('a')  # Получаем ссылку на каждую модель
    cars_options.append(href_options_soup[2].get('href'))

for i in range(len(cars_options)):

    configur = []
    cost = []
    engine_type = []
    engine = []
    drive_unit = []
    engine_pwr = []
    gear = []
    response_option = requests.get(url_model + cars_options[i])
    soup_option = BeautifulSoup(response_option.text, 'html.parser')
    cars_config_soup = soup_option.find('div', class_='flex items-center desktop:hidden js-submenu-toggle')  # Получаем список моделей
    no_tag_option = cars_config_soup.get_text()
    no_tag_space_option = re.sub(r"^\s+|\s+$", " ", no_tag_option)
    no_tag_space_option =no_tag_space_option.lstrip(" ")
    no_tag_space_option = no_tag_space_option.rstrip(" ")
    cars_config_name.append(no_tag_space_option)
    cars[no_tag_space_option] = {}
    cars_photo_all = soup.find_all('img', class_='car-card__img')  # Получаем фото всех моделей
    cars_model.append(no_tag_space_option)
    photo = cars_photo_all[i].get('src')

    cars[no_tag_space_option]['Photo'] = photo
    cars[no_tag_space_option]['Name'] = no_tag_space_option

    cars_config_table_soup = soup_option.find('div', class_='swiper-wrapper')  # Получаем таблицу компелектаций
    cars_config_soup = cars_config_table_soup.find_all('strong')  # Получаем ссылку компелектации
    href_config_options_soup = cars_config_table_soup.find_all('a', class_='config__variants__slide__title')  # Получаем ссылку на каждую комплектацию
    for k in href_config_options_soup:
        cars_config_options.append(k.get('href'))  # ссылка на комплектацию
    cars_engine_soup = cars_config_table_soup.find_all('div', class_='config__variants__slide__params mt-1 text-s3 color-dark-gray')  # Получаем характеристике]

    for j in range(len(cars_config_soup)):  # Получаем названия модификаций

        no_tag_config = cars_config_soup[j].get_text()

        no_tag_space_config = re.sub(r"^\s+|\s+$", " ", no_tag_config)
        no_tag_space_config = no_tag_space_config.lstrip(" ")

        cars_engine2_soup = cars_engine_soup[j].find('span')

        cars_engine3_soup = cars_engine2_soup.find('span')
        engine2 = cars_engine3_soup.get('aria-label')
        charahter = engine2.split(" / ")
        engine_type_gear = charahter[2].split(", ")
        engine_type.append(engine_type_gear[0])
        engine.append(charahter[0])

        engine_pwr.append(charahter[1])

        if charahter[3] == "Передний":
            drive = "2"
        elif charahter[3] == "Полный":
            drive = "1"
        else:
            drive = "3"
        drive_unit.append(drive)
        if engine_type_gear[1] == "Автомат":
            gears = "1"
        elif engine_type_gear[1] == "Механика":
            gears = "2"
        else:
            gears = "3"
        gear.append(gears)
        for name in cars.keys():

            if name == cars_config_name[i]:
                configur.append(cars_config_name[i] + " " + no_tag_space_config)
                cars[name]['Configuration'] = configur
                cars[name]['Type_Engine'] = engine_type
                cars[name]['Engine_pwr'] = engine_pwr
                cars[name]['Gear'] = gear
                cars[name]['Drive_unit'] = drive_unit
                cars[name]['Engine'] = engine


    cars_price_all_soup = cars_config_table_soup.find_all('div', class_='config__variants__slide__descr')
    for price in cars_price_all_soup:  # Получаем стоимость модификаций
        cars_price_soup = price.find('li')
        no_tag_price = cars_price_soup.get_text()
        no_tag_space_price = re.sub(r"^\s+|\s+$", "", no_tag_price)
        no_tag_space_price = no_tag_space_price.lstrip(" ")
        cars_config_price.append(no_tag_space_price)
        for name in cars.keys():
            if name == cars_config_name[i]:
                cost.append(no_tag_space_price)
                cars[name]['Price'] = cost

for i in range(len(cars_config_options)):
    color = []
    col = []
    engine = []
    body_name = []
    response_option_link = requests.get(url_model + cars_config_options[i]) #звходим в необходимую комплектацию
    soup_option_link = BeautifulSoup(response_option_link.text, 'html.parser')
    cars_options_name_soup = soup_option_link.find('h2', class_='constructor-summary-header__model text-x5 desktop:text-x4')


    no_tag_cars_options_name = cars_options_name_soup.get_text()
    no_tag_option_title = re.sub(r"^\s+|\s+$", " ", no_tag_cars_options_name)
    no_tag_option_title = no_tag_option_title.lstrip(" ")

    cars_color_soup = soup_option_link.find('div', class_='showroom-fullscreen-colors__selection-items pt-1 pb-4 tablet:pb-0')  # тэг на цвета
    cars_color_soup2 = cars_color_soup.find_all('div', class_='showroom-fullscreen-colors__selection-item', id=True)

    cars_body_name_soup = soup_option_link.find_all('div', class_='info-section__body pt-4 desktop:pt-6')
    cars_name_soup = cars_body_name_soup[2].find_all('dl')
    for index in range(len(cars_name_soup)):
        span = cars_name_soup[index].find('dt')
        name_sort = span.get_text()

        if name_sort == 'Тип кузова':
            span_dl = cars_name_soup[index].find('dd')
            name = span_dl.get_text()
            body_name = name

    for colorss in cars_color_soup2:
        cars_color = colorss.get('id')
        color_split = cars_color.split("/")
        color.append(color_split[1])


    for name in cars.keys():
        for conf in cars[name]['Configuration']:
            if conf == no_tag_option_title:

                cars[name]['Color'] = color
                cars[name]['Body'] = body_name




def core_model(title, price, body, is_visible, mark_id):
    global core_model_last_id
    query = "INSERT INTO core_model(title, price, body, is_visible, mark_id) VALUES(%s,%s,%s,%s,%s)"
    args = (title, price, body, is_visible, mark_id)

    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)

        cursor = conn.cursor()
        cursor.execute(query, args)
        core_model_last_id = cursor.lastrowid

        conn.commit()
    except Error as error:
        print(error)

    finally:
        cursor.close()
        conn.close()

def core_engine(power, type_fuel, volume):
    global core_engine_last_id
    query = "INSERT INTO core_engine(power, type_fuel, volume) VALUES(%s,%s,%s)"
    args = (power, type_fuel, volume)

    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)

        cursor = conn.cursor()
        cursor.execute(query, args)
        core_engine_last_id = cursor.lastrowid

        conn.commit()
    except Error as error:
        print(error)

    finally:
        cursor.close()
        conn.close()

def core_set(title, image, special, model_id):
    global core_set_last_id
    query = "INSERT INTO core_set(title, image, special, model_id) VALUES(%s,%s,%s,%s)"
    args = (title, image, special, model_id)

    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)

        cursor = conn.cursor()
        cursor.execute(query, args)
        core_set_last_id = cursor.lastrowid

        conn.commit()
    except Error as error:
        print(error)

    finally:
        cursor.close()
        conn.close()

def core_setengine(engine_id, set_id):
    global core_setengine_last_id
    query = "INSERT INTO core_setengine(engine_id, set_id) VALUES(%s,%s)"
    args = (engine_id, set_id)

    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)

        cursor = conn.cursor()
        cursor.execute(query, args)
        core_setengine_last_id = cursor.lastrowid

        conn.commit()
    except Error as error:
        print(error)

    finally:
        cursor.close()
        conn.close()

def core_settransmission(set_id, transmission_id):

    query = "INSERT INTO core_settransmission(set_id, transmission_id) VALUES(%s,%s)"
    args = (set_id, transmission_id)

    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)

        cursor = conn.cursor()
        cursor.execute(query, args)


        conn.commit()
    except Error as error:
        print(error)

    finally:
        cursor.close()
        conn.close()
def core_car(title, set_id, image, price, expenditure, city_id, engine_id, mark_id, transmission_id, wd_id):
    global core_car_last_id
    query = "INSERT INTO core_car(title, set_id, image, price, expenditure, city_id, engine_id, mark_id, transmission_id, wd_id) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    args = (title, set_id, image, price, expenditure, city_id, engine_id, mark_id, transmission_id, wd_id)

    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)

        cursor = conn.cursor()
        cursor.execute(query, args)
        core_car_last_id = cursor.lastrowid

        conn.commit()
    except Error as error:
        print(error)

    finally:
        cursor.close()
        conn.close()

def core_colors(title):
    global core_color_last_id
    query = "INSERT INTO core_color(title) VALUES(%s)"
    args = [(title)]

    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)

        cursor = conn.cursor()
        cursor.execute(query, args)
        core_color_last_id = cursor.lastrowid

        conn.commit()
    except Error as error:
        print(error)

    finally:
        cursor.close()
        conn.close()

def core_setcolor(car_id, color_id):

    query = "INSERT INTO core_setcolor(car_id, color_id) VALUES(%s,%s)"
    args = (car_id, color_id)

    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)

        cursor = conn.cursor()
        cursor.execute(query, args)


        conn.commit()
    except Error as error:
        print(error)

    finally:
        cursor.close()
        conn.close()

def main():
    for model in cars.keys():
        for index in cars[model]['Body']:
            core_model(cars[model]['Name'],re.sub(r" ", "", cars[model]['Price'][0]),index, '1','5') # возвращает core_model_last_id


        for i in range(len(cars[model]['Engine'])):
            core_engine(cars[model]['Engine_pwr'][i], cars[model]['Type_Engine'][i], cars[model]['Engine'][i]) # Возвращает core_engine_last_id
            core_set(cars[model]['Configuration'][i], cars[model]['Photo'], 'None', core_model_last_id)  # Возвращает core_set_last_id
            core_setengine(core_engine_last_id,core_set_last_id)
            core_settransmission(core_set_last_id, cars[model]['Gear'][i]) #core_settransmission_last_id
            core_car('Kia ' + cars[model]['Configuration'][i], core_set_last_id, cars[model]['Photo'], cars[model]['Price'][i],'' , '10', core_engine_last_id, '5',cars[model]['Gear'][i], cars[model]['Drive_unit'][i])
            for colors in cars[model]['Color']:
                core_colors(colors)  # возвращает core_color_last_id
                core_setcolor(core_car_last_id,core_color_last_id)

if __name__ == '__main__':
    main()



print ("time elapsed: {:.2f}s".format(time.time() - start_time))
