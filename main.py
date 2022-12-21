from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup as soup
from selenium import webdriver
import requests
from selenium.webdriver.common.by import By
from urllib.request import urlopen as uReq
import openpyxl




myurl ='https://baucenter.ru/shtukaturki/'
uClient  = uReq(myurl)
page_html = uClient.read()
uClient.close()
page_soup = soup(page_html, features="html.parser")
containers = page_soup.find_all("div",{"class": "catalog_item with-tooltip"})
workbook = openpyxl.Workbook()
worksheet = workbook.active
worksheet['A1']='Product_name'
worksheet['B1']='Pricing'
worksheet['C1']='Ratings'
data = []
for container in containers:
    name_container = container.find_all("div",{"class": "catalog_item_heading h4"})
    name = name_container[0].text.strip()
    price_container = container.find_all("div", {"class": "price-block"})
    price = price_container[0].text.strip()
    rating_container = container.find_all("div", {"class": "catalog_item_rating"})
    ratings = rating_container[0].text
    edit_price = ''.join(price.split(','))
    sym_rupee = edit_price.split("?")
    add_rs_price = "RUB" + sym_rupee[0]
    split_price = add_rs_price.split(".")
    final_price = split_price[0]
    split_name = name.split('<div>')
    final_name = split_name[0]

    split_rating = str(ratings).split(" ")
    final_rating = split_rating[0]
    result = final_name +'@'+ final_price
    result = result.split('@')
    data.append(result)
row = 2

for i in data:

    for j in i:
        worksheet['A'+str(row)]=i[i.index(j)-1]
        worksheet['B'+str(row)]=i[i.index(j)]

    row+=1

workbook.save('products.xlsx')









