from pymongo import MongoClient
from bs4 import BeautifulSoup
import requests as req
import csv

url = "https://en.wikipedia.org/wiki/List_of_schools_in_Syria"

response = req.get(url)


schools = []

soup = BeautifulSoup(response.text, "html.parser")
results = soup.find_all('div', class_="div-col columns column-width")
for item in results:
    list_items = item.find_all('li')
    for list_item in list_items:
        try:
            print(list_item.text)
            print("-------")
            schools.append([list_item.text])
        except:
            print("no text")


for school in schools:
    print(school)

with open('syrian_schools.csv', "w") as csvfile:
    csvwrite = csv.writer(csvfile)

    csvwrite.writerows(schools)