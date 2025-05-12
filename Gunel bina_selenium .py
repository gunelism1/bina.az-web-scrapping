from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from openpyxl import Workbook
import time

options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

url = "https://bina.az/baki/alqi-satqi/menziller/yeni-tikili/4-otaqli"
driver.get(url)
time.sleep(5)  

soup = BeautifulSoup(driver.page_source, "html.parser")
driver.quit()

wb = Workbook()
ws = wb.active
ws.title = "Bina Siyahi"
ws.append(["Address", "Price", "Datetime", "Attributes"])

listings = soup.find_all("div", class_="items-i")

for item in listings:
    price_tag = item.find("span", class_="price-val")
    price = price_tag.get_text(strip=True) if price_tag else ""

    location_tag = item.find("div", class_="location")
    location = location_tag.get_text(strip=True) if location_tag else ""

    datetime_tag = item.find("div", class_="city_when")
    datetime = datetime_tag.get_text(strip=True) if datetime_tag else ""

    name_list = item.find("ul", class_="name")
    if name_list:
        attributes = "; ".join([li.get_text(strip=True) for li in name_list.find_all("li")])
    else:
        attributes = ""

    if price and location:
        ws.append([location, price, datetime, attributes])

wb.save("bina_siyahi_selenium.xlsx")
print("Ugurla yadda saxlandi: bina_siyahi_selenium.xlsx")
