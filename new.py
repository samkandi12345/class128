from tkinter import BROWSE
from unicodedata import name
from wsgiref import headers
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
import requests
planet_data = []
starturl = "https://exoplanets.nasa.gov/discovery/exoplanet-catalog/"
browser = webdriver.Chrome("C:\Users\samra\Downloads\chromedriver_win32")
browser.get(starturl)
time.sleep(10) 

def scrap():
    headers = ["name","Light-yearsfromEarth","Planet_mass","Stellar_magnitude","Discovery_date"]
    planet_data = []
    for i in range(0,428):
        soup = BeautifulSoup(browser.page_source,"html.parser")
        for ul_tag in soup.find_all("ul",attrs={"class","exoplanets"}):
            li_tags = ul_tag.find_all("li")
            temp_list = []
            for index,li_tag in enumerate(li_tags):
                if index == 0:
                    temp_list.append(li_tag.find_all("a")[0].contents[0])
                else:
                    try:
                        temp_list.append(li_tag.contents[0])
                    except:
                        temp_list.append("")
            planet_data.append(temp_list)
        browser.find_element_by_xpath("/html/body/div[2]/div/div[3]/section[2]/div/section[2]/div/div/article/div/div[2]/section/div/div/div/ul[2]")
    with open("file.csv","w") as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(headers)
        csvwriter.writerows(planet_data)

new_planet_data = []

def scrap_more_data(hyperlink):
    page = requests.get(hyperlink)
    soup = BeautifulSoup(page.content,"html.parsar")
    for tr_tag in soup.find_all("tr",attrs={"class":"fact_row"}):
        td_tags = tr_tag.find_all("td")
        temp_list = []
        for td_tag in td_tags:
            try:
                temp_list.append(td_tag.find_all("div",attrs={"class":"value"})[0].contents[0])
            except:
                temp_list.append("")
            new_planet_data.append(temp_list)

    pass

scrap()

for data in planet_data:
    scrap_more_data(data[5])

for index,data in enumerate(planet_data):
    new_planet_data.append(data+new_planet_data[index])

with open("csv2.csv","w") as f:
    csvwriter = csv.writer(f)
    csvwriter.writerow(headers)
    csvwriter.writerows(new_planet_data)
    



