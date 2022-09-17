import requests
import re
from bs4 import BeautifulSoup


class DB:
    def __init__(self):
        pass

    def create_model_obj(title, price, body, is_visible, mark_id):
        """
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
        """

    def create_engine_obj(power, type_fuel, volume):
        """
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
        """

    def create_set_obj(title, image, special, model):
        """
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
        """

    def create_setengine_obj(engine, set):
        """
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
        """

    def create_settransmission_obj(set, transmission_id):
        """
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
        """

    def create_car_obj(title, set, image, price, expenditure, city_id, engine, mark_id, transmission_id, wd_id):
        """
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
        """

    def create_color_obj(title):
        """
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
        """

    def create_setcolor_obj(car, color):
        """
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
        """


class KIA(DB):
    def __init__(self):
        super().__init__()

        self.url: str = r"https://www.kia.ru/models/"
        self.url_model: str = r"https://www.kia.ru"

        self.cars: dict = {}

        self.models: list = []
        self.photos: list = []
        self.links: list = []
        self.options: list = []

        self.names: list = []
        self.prices: list = []

        self.mark_id: int = 5
        self.city_id: int = 10

    def get_soup(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup

    def get_links(self, cars_name):
        links: list = []
        for i in range(len(cars_name)):
            href_soup = cars_name[i].find_all('a')  # Получаем ссылку на каждую модель
            links.append(href_soup[0].get('href'))  # Присваевываем в лист ссылку на модель
        return links

    def get_options(self, links):
        options: list = []
        for i in range(len(links)):
            response_link = requests.get(self.url_model + links[i])

            soup_link = BeautifulSoup(response_link.text, 'html.parser')
            cars_options_soup = soup_link.find_all('nav', class_='model-header-panel__nav__menu')

            href_options_soup = cars_options_soup[0].find_all('a')  # Получаем ссылку на каждую модель
            options.append(href_options_soup[2].get('href'))
        return options

    def filter(self, soup, options):
        for i in range(len(options)):
            configs: list = []
            cost: list = []
            engine_type: list = []
            engine: list = []
            drive_unit: list = []
            engine_pwr: list = []
            gears: list = []
            response_option = requests.get(self.url_model + options[i])
            soup_option = BeautifulSoup(response_option.text, 'html.parser')
            cars_config_soup = soup_option.find('div', class_='flex items-center desktop:hidden js-submenu-toggle')  # Получаем список моделей
            no_tag_option = cars_config_soup.get_text()
            no_tag_space_option = re.sub(r"^\s+|\s+$", " ", no_tag_option)
            no_tag_space_option = no_tag_space_option.lstrip(" ")
            no_tag_space_option = no_tag_space_option.rstrip(" ")
            self.names.append(no_tag_space_option)
            self.cars[no_tag_space_option] = {}
            cars_photo_all = soup.find_all('img', class_='car-card__img')  # Получаем фото всех моделей
            self.models.append(no_tag_space_option)
            photo = cars_photo_all[i].get('src')

            self.cars[no_tag_space_option]['Photo'] = photo
            self.cars[no_tag_space_option]['Name'] = no_tag_space_option

            cars_config_table_soup = soup_option.find('div', class_='swiper-wrapper')  # Получаем таблицу компелектаций
            cars_config_soup = cars_config_table_soup.find_all('strong')  # Получаем ссылку компелектации
            href_config_options_soup = cars_config_table_soup.find_all('a', class_='config__variants__slide__title')  # Получаем ссылку на каждую комплектацию
            for k in href_config_options_soup:
                options.append(k.get('href'))  # ссылка на комплектацию
            cars_engine_soup = cars_config_table_soup.find_all('div', class_='config__variants__slide__params mt-1 text-s3 color-dark-gray')  # Получаем характеристике]

            for j in range(len(cars_config_soup)):  # Получаем названия модификаций

                no_tag_config = cars_config_soup[j].get_text()
                no_tag_space_config = re.sub(r"^\s+|\s+$", " ", no_tag_config)
                no_tag_space_config = no_tag_space_config.lstrip(" ")

                cars_engine2_soup = cars_engine_soup[j].find('span')
                cars_engine3_soup = cars_engine2_soup.find('span')
                engine2 = cars_engine3_soup.get('aria-label')
                character = engine2.split(" / ")
                engine_type_gear = character[2].split(", ")
                engine_type.append(engine_type_gear[0])
                engine.append(character[0])
                engine_pwr.append(character[1])
                drive = self.f_drive_unit(character)
                drive_unit.append(drive)
                gear = self.f_engine_type_gear(engine_type_gear)
                gears.append(gear)
                for name in self.cars.keys():
                    if name == self.names[i]:
                        configs.append(self.names[i] + " " + no_tag_space_config)
                        self.cars[name]['Configuration'] = configs
                        self.cars[name]['Type_Engine'] = engine_type
                        self.cars[name]['Engine_pwr'] = engine_pwr
                        self.cars[name]['Gear'] = gear
                        self.cars[name]['Drive_unit'] = drive_unit
                        self.cars[name]['Engine'] = engine

            cars_price_all_soup = cars_config_table_soup.find_all('div', class_='config__variants__slide__descr')
            for price in cars_price_all_soup:  # Получаем стоимость модификаций
                cars_price_soup = price.find('li')
                no_tag_price = cars_price_soup.get_text()
                no_tag_space_price = re.sub(r"^\s+|\s+$", "", no_tag_price)
                no_tag_space_price = no_tag_space_price.lstrip(" ")
                self.prices.append(no_tag_space_price)
                for name in self.cars.keys():
                    if name == self.names[i]:
                        cost.append(no_tag_space_price)
                        self.cars[name]['Price'] = cost

        for i in range(len(options)):
            color: list = []
            engine: list = []
            body_name: list = []
            response_option_link = requests.get(self.url_model + options[i]) #звходим в необходимую комплектацию
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

            for name in self.cars.keys():
                for conf in self.cars[name]['Configuration']:
                    if conf == no_tag_option_title:
                        self.cars[name]['Color'] = color
                        self.cars[name]['Body'] = body_name

    def execute(self):
        soup = self.get_soup(self.url)
        cars_name = soup.find_all('div', class_='car-card__name-block')  # Получаем список всех моделей
        self.links = self.get_links(cars_name)
        self.options = self.get_options(self.links)
        self.filter(soup, self.options)

        for model in self.cars.keys():
            name = self.cars[model]['Name']
            price = re.sub(r" ", "", self.cars[model]['Price'][0])
            engine = self.cars[model]['Engine']
            photo = self.cars[model]['Photo']
            gear = self.cars[model]['Gear'][i]
            configuration = self.cars[model]['Configuration'][i]
            engine_power = self.cars[model]['Engine_pwr'][i]
            engine_type = self.cars[model]['Type_Engine'][i]
            drive_unit = self.cars[model]['Drive_unit'][i]

            for index in self.cars[model]['Body']:
                model_obj = self.create_model_obj(title=name, price=price, body=index, is_visible=1, mark_id=self.mark_id)

            for i in range(len(engine)):
                engine_obj = self.create_engine_obj(power=engine_power, type_fuel=engine_type, volume=engine[i])
                set_obj = self.create_set_obj(title=configuration, image=photo, special=None, model=model_obj)
                setengine_obj = self.create_setengine_obj(engine_obj, set_obj)
                settransmission_obj = self.create_settransmission_obj(set_obj, gear)
                title = f"Kia {configuration}"
                car_obj = self.create_car_obj(title=title, set=set_obj, image=photo, price=price, expenditure="", city_id=self.city_id,
                    engine=engine_obj, mark_id=self.mark_id, transmission_id=gear, wd_id=drive_unit)
                for color in self.cars[model]['Color']:
                    color_obj = self.create_color_obj(color)
                    setcolor_obj = self.create_setcolor_obj(car_obj, color_obj)

    def f_drive_unit(self, character):
        if character[3] == "Передний":
            return 2
        elif character[3] == "Полный":
            return 1
        else:
            return 3

    def f_engine_type_gear(self, engine_type_gear):
        if engine_type_gear[1] == "Автомат":
            return 1
        elif engine_type_gear[1] == "Механика":
            return 2
        else:
            return 3


if __name__ == "__main__":
    kia = KIA()
    kia.execute()