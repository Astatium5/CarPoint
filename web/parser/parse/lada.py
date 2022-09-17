from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import time

driver = webdriver.Firefox()

info = [
" Granta седан Classic'22  ", " 1929 ",
" Granta седан Classic'22 Кондиционер  ", " 1930 ",
" Granta седан Classic ", " 1931 ",
" Granta седан Comfort ", " 1932 ",
" Granta седан спецсерия #CLUB22", " 1933 ",
" Granta седан спецсерия #CLUB  ", " 1934 ",
" Granta седан Luxe ", " 1935 ",
" Granta лифтбек Classic'22", " 1936 ",
" Granta лифтбек Classic'22 Кондиционер", " 1937 ",
" Granta лифтбек Classic  ", " 1938 ",
" Granta лифтбек Comfort  ", " 1939 ",
" Granta лифтбек спецсерия #CLUB22 ", " 1940 ",
" Granta лифтбек спецсерия #CLUB", " 1941 ",
" Granta лифтбек Luxe  ", " 1942 ",
" Granta хэтчбек Classic  ", " 1943 ",
" Granta хэтчбек Comfort  ", " 1944 ",
" Granta хэтчбек Luxe  ", " 1945 ",
" Granta универсал Classic'22 ", " 1946 ",
" Granta универсал Classic", " 1947 ",
" Granta универсал Comfort", " 1948 ",
" Granta универсал Luxe", " 1949 ",
" Granta Cross Classic'22  ", " 1950 ",
" Granta Cross Classic ", " 1951 ",
" Granta Cross Comfort'22 Light  ", " 1952 ",
" Granta Cross Comfort'22  ", " 1953 ",
" Granta Cross Comfort ", " 1954 ",
" Granta Cross спецсерия Quest22", " 1955 ",
" Granta Cross спецсерия Quest  ", " 1956 ",
" Granta Cross Luxe ", " 1957 ",
" Granta Drive Active Classic'22 ", " 1958 ",
" Granta Drive Active Comfort'22 ", " 1959 ",
" Granta Drive Active Comfort", " 1960 ",
" Granta Drive Active Comfort Light", " 1961 ",
" Vesta седан Classic  ", " 1962 ",
" Vesta седан Comfort  ", " 1963 ",
" Vesta седан Comfort Light  ", " 1964 ",
" Vesta седан Luxe EnjoY  ", " 1965 ",
" Vesta седан Luxe EnjoY Pro ", " 1966 ",
" Vesta седан Exclusive", " 1967 ",
" Vesta Cross Comfort  ", " 1968 ",
" Vesta Cross спецсерия [BLACK] ", " 1969 ",
" Vesta Cross Luxe EnjoY  ", " 1970 ",
" Vesta Cross Luxe EnjoY Pro ", " 1971 ",
" Vesta SW Classic  ", " 1972 ",
" Vesta SW Comfort  ", " 1973 ",
" Vesta SW Comfort Light  ", " 1974 ",
" Vesta SW Luxe EnjoY  ", " 1975 ",
" Vesta SW Luxe EnjoY Pro ", " 1976 ",
" Vesta SW Exclusive", " 1977 ",
" Vesta SW Cross Comfort  ", " 1978 ",
" Vesta SW Cross спецсерия [BLACK] ", " 1979 ",
" Vesta SW Cross Luxe EnjoY  ", " 1980 ",
" Vesta SW Cross Luxe EnjoY Pro ", " 1981 ",
" Vesta Sport Luxe  ", " 1982 ",
" Vesta Sport Luxe EnjoY Pro ", " 1983 ",
" XRAY  Standard ", " 1984 ",
" XRAY  Classic  ", " 1985 ",
" XRAY  Comfort  ", " 1986 ",
" XRAY  Comfort Light  ", " 1987 ",
" XRAY  спецсерия #CLUB", " 1988 ",
" XRAY  спецсерия #CLUB EnjoY", " 1989 ",
" XRAY  Luxe  ", " 1990 ",
" XRAY Cross Classic", " 1991 ",
" XRAY Cross Comfort", " 1992 ",
" XRAY Cross Comfort Light", " 1993 ",
" XRAY Cross спецсерия [BLACK]  ", " 1994 ",
" XRAY Cross Luxe", " 1995 ",
" XRAY Cross спецсерия Instinct ", " 1996 ",
" Largus универсал Classic", " 1997 ",
" Largus универсал Comfort", " 1998 ",
" Largus универсал Comfort Light", " 1999 ",
" Largus универсал Luxe Light", " 2000 ",
" Largus универсал Luxe", " 2001 ",
" Largus Cross Comfort ", " 2002 ",
" Largus Cross Comfort Light ", " 2003 ",
" Largus Cross Luxe Light ", " 2004 ",
" Largus Cross Luxe ", " 2005 ",
" Niva Travel  Classic ", " 2006 ",
" Niva Travel  Comfort ", " 2007 ",
" Niva Travel  спецсерия [BLACK]", " 2008 ",
" Niva Travel  Comfort Offroad ", " 2009 ",
" Niva Travel  Luxe ", " 2010 ",
" Niva Travel  Luxe Offroad ", " 2011 ",
" Niva Legend 3 дв. Classic'22", " 2012 ",
" Niva Legend 3 дв. Classic  ", " 2013 ",
" Niva Legend 3 дв. спецсерия [BLACK] ", " 2014 ",
" Niva Legend 3 дв. Luxe  ", " 2015 ",
" Niva Legend 3 дв. Urban ", " 2016 ",
" Niva Legend 5 дв. Classic  ", " 2017 ",
" Niva Legend 5 дв. спецсерия [BLACK] ", " 2018 ",
" Niva Legend 5 дв. Luxe  ", " 2019 ",
" Niva Legend 5 дв. Urban ", " 2020 ",
" Niva Bronto Luxe  ", " 2021 ",
" Niva Bronto Prestige ", " 2022 "]

driver.get("https://www.lada.ru/configurator")

time.sleep(1)

#kill cookies baner
element = driver.find_element(By.XPATH, """/html/body/div/div[2]/div[1]/div/div[7]/div[2]/div[1]/div/div/div/div[1]/div/div""")
element.click()

element = driver.find_element(By.XPATH, '//*[@id="1671ce26-5863-5732-906c-4ad7fc2b4b37"]')
element.click()

#`models` (`id`, `mark_id`, `title`, `price`, `body`, `visible`)
#(328, 4, 'Tiggo 4', '1 139 900 ₽', 'Внедорожник', 1)
#<h4 class="styles_title__3G8IX">Семейство Granta</h4>

n_models = 2

while (True):

    site = driver.page_source
    site = BeautifulSoup(site, "lxml")
    names = site.find_all(class_="styles_title__31j9w")
    prices = site.find_all(class_="styles_fullPrice__7ciD8 styles_family__2Hacm")
    models = site.find_all(class_="styles_title__3G8IX")

    i = 0

    #print(models[n_models-2].text)
    for name in names :
        #print("---", end = '')
        #print(name.text, end = ' ')
        #print(prices[i].text)

        time.sleep(1)
        element = driver.find_elements(By.XPATH, '//*[@id="9c9c7427-69a9-5b98-8a3c-c6869ffd1a2a"]')
        element[i].click()
        time.sleep(1)

        site1 = driver.page_source
        site1 = BeautifulSoup(site1, "lxml")

        names1 = site1.find_all(class_="styles_title__3vMCj")

        prices2 = site1.find_all(class_="styles_price__2y_rj")

        j = 0
        i += 1

        for name1 in names1:
            inf = 0
            set_id = 0
            status_car = name.text + ' ' + name1.text
            #print("---" + status_car, end = ' to ')
            #print("------", end = '')
            #print(name1.text, end = ' ')
            #print(prices2[j].text)

            while (inf < len(info)):
                if (status_car in info[inf]):
                    set_id = info[inf+1]

                    #print(info[inf] + " " +set_id)
                    inf += 2
                    break
                inf += 2
            if (set_id == 0):
                continue

            equipments = driver.find_elements(By.CLASS_NAME, "styles_item__32UVV")
            button_equipments = equipments[j].find_elements(By.TAG_NAME, "button")
            driver.execute_script("arguments[0].click();", button_equipments[1])
            time.sleep(1)

            site2 = driver.page_source
            site2 = BeautifulSoup(site2, "lxml")

            transmission_n = 0
            transmission_car = site2.find_all(class_="styles_transmission__2w53k")
            names_eng2 = site2.find_all(class_="styles_title__1Kdhd")

            n_equipments2 = 0
            n_equipments3 = 0
            for q in names_eng2:
                #print(" " * 10, end = ' ')
                #print(q.text)
                if ("Механическая" in transmission_car[transmission_n].text):
                    transmission_id = 2
                elif ("Автоматическая" in transmission_car[transmission_n].text) :
                    transmission_id = 1
                else :
                    print("eeeeeeee")
                    exit()
                if ("CNG" in q.text):
                    continue

#                | 10464 |    90 | Бензин                     |    1.6 |
#                | 10465 |   106 | Бензин                     |    1.6 |
#                | 10466 |    98 | Бензин                     |    1.6 |
#                | 10467 |   106 | Бензин                     |    1.6 |
#                | 10468 |   113 | Бензин                     |    1.6 |
#                | 10469 |   122 | Бензин                     |    1.8 |
#                | 10470 |   145 | Бензин                     |    1.8 |
#                | 10471 |    80 | Бензин                     |    1.7 |
#                | 10472 |    83 | Бензин                     |    1.7 |
                engine_id = 0
                if ("90" in q.text and "1.6" in q.text):
                    engine_id = 10464
                if ("106" in q.text and "1.6" in q.text):
                    engine_id = 10465
                if ("98" in q.text and "1.6" in q.text):
                    engine_id = 10466
                if ("113" in q.text and "1.6" in q.text):
                    engine_id = 10468
                if ("122" in q.text and "1.8" in q.text):
                    engine_id = 10469
                if ("145" in q.text and "1.8" in q.text):
                    engine_id = 10470
                if ("80" in q.text and "1.7" in q.text):
                    engine_id = 10471
                if ("83" in q.text and "1.7" in q.text):
                    engine_id = 10472

                equipments2 = driver.find_elements(By.CLASS_NAME, "styles_container__3zMSQ")
                button_equipments2 = equipments2[n_equipments2].find_elements(By.TAG_NAME, "button")
                driver.execute_script("arguments[0].click();", button_equipments2[0])
                time.sleep(1)

                try:
                    continue1 = driver.find_element(By.XPATH, '//*[@id="d7aac8ee-53f7-5a24-b292-615fc9a035ec"]')
                    driver.execute_script("arguments[0].click();", continue1)
                    time.sleep(0.5)
                except Exception as e:
                    continue1 = driver.find_element(By.XPATH, '//*[@id="55bdcee8-7ecc-5e1c-87f1-b94163437dcc"]')
                    driver.execute_script("arguments[0].click();", continue1)
                    time.sleep(0.5)


                time.sleep(1)
                try:
                    equipments3 = driver.find_element(By.CLASS_NAME, "styles_colors__3-0PC")
                    button_equipments3 = equipments3.find_elements(By.TAG_NAME, "button")
                except Exception as e:
                    print("#"*20)
                    print(e)
                    print("#"*20)
                    back = driver.find_element(By.XPATH, '/html/body/div/div[2]/div[1]/div/div[7]/div[2]/div[2]/div[3]/div[2]/div[2]')
                    back.click()
                    continue
                button_equipments3_n = 0
                for butt_eq3 in button_equipments3:
                    try:
                        driver.execute_script("arguments[0].click();", button_equipments3[len(button_equipments3)-1])
                    except Exception as e:
                        print("#"*20)
                        print(e)
                        print("#"*20)
                        time.sleep(1)
                        back = driver.find_element(By.XPATH, '/html/body/div/div[2]/div[1]/div/div[7]/div[2]/div[2]/div[5]/div[2]')
                        time.sleep(1)
                        driver.execute_script("arguments[0].click();", back)
                        time.sleep(0.5)
                        equipments3 = driver.find_element(By.CLASS_NAME, "styles_colors__3-0PC")
                        button_equipments3 = equipments3.find_elements(By.TAG_NAME, "button")
                        break
                    time.sleep(1)
                    site3 = driver.page_source
                    site3 = BeautifulSoup(site3, "lxml")
                    name4 = site3.find(class_="styles_colorTitle__3Ycwe")
                    image = site3.find(class_="styles_image__LwpIR").find("img").get("src")
                    #print(" " * 20, end = '')
                    #print(name4.text)
                    button_equipments3_n += 1

                    try:
                        continue2 = driver.find_element(By.XPATH, '//*[@id="d5b56ade-2fb4-556c-a023-4fb328d81b24"]')
                        driver.execute_script("arguments[0].click();", continue2)
                    except Exception as e:
                        print("#"*20)
                        print(e)
                        print("#"*20)
                        time.sleep(1)
                        back = driver.find_element(By.XPATH, '/html/body/div/div[2]/div[1]/div/div[7]/div[2]/div[2]/div[5]/div[2]')
                        time.sleep(1)
                        driver.execute_script("arguments[0].click();", back)
                        time.sleep(0.5)
                        equipments3 = driver.find_element(By.CLASS_NAME, "styles_colors__3-0PC")
                        button_equipments3 = equipments3.find_elements(By.TAG_NAME, "button")
                        continue

                    time.sleep(5)
                    site3 = driver.page_source
                    site3 = BeautifulSoup(site3, "lxml")

                    car_info1 = site3.find(class_="styles_h2__3OnKJ styles_title__eS8FR")
                    car_info2 = site3.find(class_="styles_p__2Tvzc styles_desc__3NvRu")
                    car_info3 = site3.find(class_="styles_price__1oj9c")
                    car_info4 = image

                    try:
                        car_info3 = car_info3.text
                        car_info3 = car_info3.replace(' ', '')
                        car_info3 = car_info3.replace('₽', '')
                    except Exception as e:
                        print("#"*20)
                        print(e)
                        print("#"*20)
                        time.sleep(1)
                        back = driver.find_element(By.XPATH, '/html/body/div/div[2]/div[1]/div/div[7]/div[2]/div[2]/div[5]/div[2]')
                        time.sleep(1)
                        driver.execute_script("arguments[0].click();", back)
                        time.sleep(0.5)
                        equipments3 = driver.find_element(By.CLASS_NAME, "styles_colors__3-0PC")
                        button_equipments3 = equipments3.find_elements(By.TAG_NAME, "button")
                        continue



                    wd_id = 2
                    sity_id = 78
                    mark_id = 2

                    expenditure = site3.find_all(class_="styles_cell__v4g__")
                    for expen in expenditure:
                        if("Смешанный цикл" in expen.text):
                            expenditure = expen.find(class_="styles_value__34M3J styles_technical__value__2hGgj")
                            gg = 1
                            break
                        else :
                            gg = 0
                    if (gg == 0):
                        expenditure1 = "Нет данных"
                    else :
                        expenditure1 = expenditure.text



                    #{car_id}, '{name+status}', {set_id}, '{link[0]}', {int(price)}, {engine_id}, {transmission_id}, {wd_id}, '{expenditure}', {city_id}, {mark_id}
                    print(f"""'Lada {status_car}', '{set_id}', '{car_info4}', '{car_info3}', '{engine_id}', '{transmission_id}', '{wd_id}', '{expenditure1}л смешанный', '{sity_id}', '{mark_id}'""")
                    back = driver.find_element(By.XPATH, '/html/body/div/div[2]/div[1]/div/div[7]/div[2]/div[2]/div[5]/div[2]')
                    driver.execute_script("arguments[0].click();", back)

                    time.sleep(1)

                    #print(" " * 20, end = '')

                    equipments3 = driver.find_element(By.CLASS_NAME, "styles_colors__3-0PC")
                    button_equipments3 = equipments3.find_elements(By.TAG_NAME, "button")
                    break

                back = driver.find_element(By.XPATH, '/html/body/div/div[2]/div[1]/div/div[7]/div[2]/div[2]/div[3]/div[2]/div[2]')
                back.click()

                time.sleep(1)

                n_equipments2 += 1
                n_equipments3 += 1

            back = driver.find_element(By.XPATH, '/html/body/div/div[2]/div[1]/div/div[7]/div[1]/div/div[2]')
            back.click()

            j += 1

        back = driver.find_element(By.XPATH, '/html/body/div/div[2]/div[1]/div/div[7]/div[1]/div/div[1]/div[2]')
        back.click()

    if (n_models == 7):
        break
    element = driver.find_element(By.XPATH, f"""/html/body/div/div[2]/div[1]/div/div[7]/div[2]/div[1]/div/div/div/div[{n_models}]/div/div""")
    element.click()
    time.sleep(1)
    n_models += 1

driver.close()
