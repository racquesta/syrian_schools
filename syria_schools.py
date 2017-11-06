from bs4 import BeautifulSoup
import requests
import pymongo

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

#url = "http://sn4hr.org/page/" + num + "/?s=school"

db = client.syria
collection = db.school_attacks

link_list = []
for x in range(1, 50):
    try:
        url = "http://sn4hr.org/page/" + str(x) + "/?s=school"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        results = soup.find_all('h3', class_="entry-title td-module-title")
        
        for result in results:
            link_to_article = result.a['href']
            link_list.append(link_to_article)
    

for link in link_list:
    url = link
    response2 = requests.get(url)
    soup2 = BeautifulSoup(response2.text, 'html.parser')
 
    title = soup2.find('h1', class_="entry-title").text
    body = soup2.find('h5').text
    date_published = soup2.find('time', class_="entry-date updated td-module-date").text
    art_link = link
    unique_key = title + date_published

    print(date_published)

    count = collection.find({"unique_key": unique_key}).count()
    
    if count == 0:
        
        post = {
            "article_title": title,
            "article_text": body,
            "date_published": date_published,
            "article_link": art_link,
            "unique_key": unique_key 
        }

        collection.insert_one(post)
    else:
        print('Already in Database')
    
# post = {
#     "title":
#     "link": link 
# }

# link 
# date
# date_of_attack

# post = {
#     "link_to_article": link_to_article,
#     "date_of_attack": 
#     "headline":
#     "who_fired"
# }
