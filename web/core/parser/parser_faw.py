from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from bs4 import BeautifulSoup
import time

links = ["https://cena-auto.ru/faw/besturn_x80/1347/universal/29311/", "https://cena-auto.ru/faw/besturn_x80/1347/universal/29312/", "https://cena-auto.ru/faw/besturn_x80/1347/universal/29313/", "https://cena-auto.ru/faw/besturn_x40/1467/universal/31488/", "https://cena-auto.ru/faw/besturn_x40/1467/universal/31489/", "https://cena-auto.ru/faw/besturn_x40/1467/universal/31490/", "https://cena-auto.ru/faw/bestune_t77/1732/hatchback/35724/", "https://cena-auto.ru/faw/bestune_t77/1732/hatchback/35723/", "https://cena-auto.ru/faw/bestune_t77/1732/hatchback/35722/"]

binary = FirefoxBinary(r'bin/firefox.exe')
driver = webdriver.Firefox(executable_path=r'gecko/geckodriver', firefox_binary=binary)

for link in links:
    driver.get(link)
    time.sleep(1)

    element = driver.find_element(By.XPATH, """/html/body/div[1]/div[3]/main/div[2]/div/div[1]/div[1]/div/div[2]/div/div/button""")
    element.click()

    site = driver.page_source
    site = BeautifulSoup(site, "lxml")

    info = site.find(class_="Characteristic-top-wrapper")
    info = site.find("h1")

    info = info.text.split(',')

    name = info[0] + ' ' + info[3]
    engine = info[2].replace('(', '').replace(')', '')

    image = site.find(class_="Characteristic-top-photo")
    image = image.find("img").get("src")
    image = "https://cena-auto.ru" + image

    price = site.find(class_="New-price")
    price = price.text.replace(' ', '').replace('P', '')

    print(f"{name}, {image}, {price}")

driver.close()
