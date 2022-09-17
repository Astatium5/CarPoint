#models
#   (320, 3, 'GEELY COOLRAY', 'От 1 879 990 руб', 'Внедорожник', 1),
#   (321, 3, 'GEELY ATLAS', 'от 1 838 990 руб', 'Внедорожник', 1),
#   (322, 3, 'ATLAS PRO', 'от 2 308 990 руб', 'Внедорожник', 1),
#   (323, 3, 'TUGELLA', 'От 3 549 990 ₽', 'Внедорожник', 1),
#
#marks
#   (3, 'Geely', 1),
#
#sets
#   (1715, 320, 'Coolray Flagship Sport', 'https://195004.selcdn.ru/ref/catalog/15641/7/3432083070.png', 'Однозонный климат-контроль|Подогрев руля|Задний центральный подлокотник с подстаканниками|Система бесключевого доступа'),
#   (1716, 320, 'Coolray Comfort', 'https://195004.selcdn.ru/ref/catalog/14531/7/2119cf2157.png', 'Регулировка руля по высоте и по вылету|Подогрев передних сидений|Кондиционер|Запуск двигателя кнопкой'),
#   (1717, 320, 'Coolray Luxury', 'https://195004.selcdn.ru/ref/catalog/15635/7/e37541e557.png', 'Регулировка руля по высоте и по вылету|Однозонный климат-контроль|Панорамная крыша с люком|Подогрев руля'),
#   (1718, 320, 'Coolray Flagship', 'https://195004.selcdn.ru/ref/catalog/14528/7/50a9c1bd6e.png', 'Однозонный климат-контроль|Панорамная крыша с люком|Подогрев руля|Система бесключевого доступа|Запуск двигателя кнопкой'),
#
#   (1719, 322, 'Atlas Pro Flagship', 'https://195004.selcdn.ru/ref/catalog/20154/7/ffb4f7ce6b.png', 'Двухзонный климат-контроль|Подогрев передних и задних боковых сидений|Подогрев рулевого колеса|Аудиосистема с 8 динамиками'),
#   (1720, 322, 'Atlas Pro Comfort', 'https://195004.selcdn.ru/ref/catalog/20142/7/f558c25866.png', 'Кнопка запуска двигателя|Функция блокировки замков при начале движения|Розетка 12В в передней части салона'),
#   (1721, 322, 'Atlas Pro Luxury', 'https://195004.selcdn.ru/ref/catalog/20148/7/715a09a6ac.png', 'Кнопка запуска двигателя|Функция блокировки замков при начале движения|Розетка 12В в передней части салона'),
#   (1722, 322, 'Atlas Pro Flagship+', 'https://195004.selcdn.ru/ref/catalog/20157/7/6f1f94105d.png', 'Кнопка запуска двигателя|Функция блокировки замков при начале движения|Розетка 12В в передней части салона'),
#
#   (1723, 323, 'Tugella Luxury', 'https://195004.selcdn.ru/ref/catalog/18740/7/15dbc2501a.png', 'Беспроводное подключение мобильного телефона по Bluetooth|Панорамная крыша с люком|Подогрев рулевого колеса'),
#   (1724, 323, 'Tugella Flagship', 'https://195004.selcdn.ru/ref/catalog/18740/7/15dbc2501a.png', 'Беспроводное подключение мобильного телефона по Bluetooth|Панорамная крыша с люком|Подогрев рулевого колеса'),
#
#
# (10425, 1.5, 177, 'бензин'),
# (10426, 2, 238, 'бензин');

from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import requests
from loguru import logger

from core.models import Car


URL = r"https://showroom.geely-motors.com/catalog/vehicle-list-by-models?brandName=geely&TotalVehicleSearch%5Bstatus%5D=1&TotalVehicleSearch%5Bcity_id%5D%5B0%5D=1459&TotalVehicleSearch%5Bdealership_id%5D=&TotalVehicleSearch%5Bmodel_id%5D%5B0%5D=19095&TotalVehicleSearch%5BmodificationList%5D=&TotalVehicleSearch%5BdriveTypeList%5D=&TotalVehicleSearch%5BequipmentList%5D=&page="
USER_AGENT = UserAgent()

ENGINE_ID = 10426
TRANSMISSION_ID = 2
CITY_ID = 78
MARK_ID = 3
WD_ID = 1
EXPENDITURE = '8.1 л.. смешанный'


def geely_main(page_n=1, all_n=0, all_n2=0, engine_n=2):
    try:
        for i in range(8):
            r = requests.get(URL+str(page_n)+'&per-page=18', headers={'user-agent': f'{USER_AGENT.random}'})
            page_n = incPage(page_n)

            all_site = BeautifulSoup(r.text, "lxml")
            all_name = all_site.find_all(class_="vehicle-preview--title--model")
            all_status = all_site.find_all(class_="vehicle-preview--title--equipment")
            all_price = all_site.find_all(class_="vehicle-preview--maininfo")
            all_engine = all_site.find_all(class_="vehicle-preview--information--item--text")
            all_image = all_site.find_all("picture")

            for i in range(len(all_price)):

                name = all_name[i].text
                status = all_status[i].text
                engine = all_engine[engine_n].text
                full_name = name+status

                price = all_price[i]
                try :
                    price = price.find(class_="vehicle-preview--price vehicle-preview--price--action").text
                except AttributeError:
                    price = price.find(class_="vehicle-preview--price").text

                price = price.replace(' ', '').replace('\t', '').replace('\n', '')

                image = all_image[i].find("img")
                link = image['data-srcset'].rsplit(',')

                if (status == ' Luxury'):
                    set_id = 1723
                elif (status == ' Flagship'):
                    set_id = 1724
                else :
                    set_id = 0

                car = Car.objects.filter(title=full_name, set_id=set_id, image=link[0], price=int(price), engine_id=ENGINE_ID, transmission_id=TRANSMISSION_ID, wd_id=WD_ID,
                    expenditure=EXPENDITURE, city_id=CITY_ID, mark_id=MARK_ID)

                if not car.exists():
                    Car.objects.create(title=full_name, set_id=set_id, image=link[0], price=int(price), engine_id=ENGINE_ID, transmission_id=TRANSMISSION_ID,
                        wd_id=WD_ID, expenditure=EXPENDITURE, city_id=CITY_ID, mark_id=MARK_ID)

                all_n += 1
                engine_n += 3
    except Exception as e:
        logger.error(e)

def incPage(n: int) -> int:
    n+=1
    return n
