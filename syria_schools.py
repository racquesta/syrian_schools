from bs4 import BeautifulSoup
import requests
import pymongo
from mLabsignin import username, password

#establish connection to db
conn = 'mongodb://%s:%s@ds149905.mlab.com:49905/heroku_236cmwk4' % (username, password)
client = pymongo.MongoClient(conn)

#url = "http://sn4hr.org/page/" + num + "/?s=school"

#define db
db = client.heroku_236cmwk4

###if needed to start fresh
# db.drop_collection('school_attacks')
# print("collection dropped")

#define collection
collection = db.school_attacks

# get a list of links from search pages
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
    except:
        print('error')
print("links retreived")
# keep count of articles added to database
art_count = 1

# loop through links and add new aticles to database if they contain the word school
for link in link_list:
    try:
        url = link
        response2 = requests.get(url)
        soup2 = BeautifulSoup(response2.text, 'html.parser')
        title = soup2.find('h1', class_="entry-title").text
        body = soup2.find('h5').text
        title_lower = title.lower()
        body_lower = body.lower()
        if 'school' in title_lower or 'school' in body_lower:
            date_published = soup2.find('time', class_="entry-date updated td-module-date").text
            art_link = link
            unique_key = title + date_published

            print(date_published)

            count = collection.find({"unique_key": unique_key}).count()
            
            if count == 0:
                
                post = {
                    "article_title": title,
                    "title_lowercase": title_lower,
                    "article_text": body,
                    "article_text_lower": body_lower,
                    "date_published": date_published,
                    "article_link": art_link,
                    "unique_key": unique_key 
                }

                collection.insert_one(post)
            else:
                print('Already in Database')
            art_count += 1
    except:
        "Error"

#print report
print(str(art_count) + "articles_added")
