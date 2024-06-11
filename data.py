from selenium import webdriver
from selenium.webdriver.common.by  import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.common.exceptions import NoSuchElementException
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
nltk.download('punkt',quiet=True)
nltk.download('stopwords',quiet=True)
nltk.download('wordnet',quiet=True)
from sqlalchemy import create_engine, Column, Integer, String, ARRAY, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import urljoin
driver=webdriver.Safari()


def login_to_letterboxd(username, password):
    driver.get("https://letterboxd.com/sign-in/")
    time.sleep(2)
    username_field=driver.find_element(By.NAME,"username")
    password_field=driver.find_element(By.NAME,"password")
    username_field.send_keys(username)
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)
    time.sleep(5)

USERNAME="jpd13"
PWD= "vivov913"
login_to_letterboxd(USERNAME,PWD)


def get_movie_urls_from_list(page_url):

    driver.get(page_url)
    time.sleep(4)

    last_height= driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        time.sleep(2)
        new_height=driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height= new_height


    movie_elements= driver.find_elements(By.CSS_SELECTOR,"[data-component-class='globals.comps.FilmPosterComponent'] a")
    movie_urls= [elem.get_attribute('href') for elem in movie_elements]

    return movie_urls

Urls=[]
list_movies= ["https://letterboxd.com/fcbarcelona/list/movies-everyone-should-watch-at-least-once/page/2/",
               "https://letterboxd.com/fcbarcelona/list/movies-everyone-should-watch-at-least-once/page/3/",
              "https://letterboxd.com/fcbarcelona/list/movies-everyone-should-watch-at-least-once/page/4/",
              "https://letterboxd.com/fcbarcelona/list/movies-everyone-should-watch-at-least-once/page/5/",
              "https://letterboxd.com/darkestparadise/list/definition-of-girly-classics/",
              "https://letterboxd.com/darkestparadise/list/definition-of-girly-classics/page/2/",
              "https://letterboxd.com/darkestparadise/list/definition-of-girly-classics/page/3/",
              "https://letterboxd.com/dayaonfilm/list/obsession-in-movies/",
              "https://letterboxd.com/ellefnning/list/for-when-you-want-to-feel-something/",
              "https://letterboxd.com/ellefnning/list/for-when-you-want-to-feel-something/page/2/",
              "https://letterboxd.com/adaydreaming/list/feeling-lost-in-your-20s/",
              "https://letterboxd.com/adaydreaming/list/feeling-lost-in-your-20s/page/2/",
              "https://letterboxd.com/andredenervaux/list/youre-not-the-same-person-once-the-film-has/",
              "https://letterboxd.com/andredenervaux/list/youre-not-the-same-person-once-the-film-has/page/2/",

              "https://letterboxd.com/andredenervaux/list/youre-not-the-same-person-once-the-film-has/page/3/",
              "https://letterboxd.com/tediously_brief/list/what-is-reality/",
              "https://letterboxd.com/tediously_brief/list/what-is-reality/page/2/",
              "https://letterboxd.com/tediously_brief/list/what-is-reality/page/3/",
              "https://letterboxd.com/tediously_brief/list/what-is-reality/page/4/"]

for links in list_movies:
   Urls.extend(get_movie_urls_from_list(links))
   

def scrape_movie_details(movie_url):
  try:
     
     driver.get(movie_url)
     time.sleep(3)

     page_source = driver.page_source

     soup= BeautifulSoup(page_source,'html.parser')

     title_element = soup.select_one("h1.headline-1.filmtitle span.name")
     if not title_element:
        print(f"Title element not found for {movie_url}")
        return None
     movie_title = title_element.text.strip().replace('\xa0', ' ')

     poster_element=soup.select_one("img.image")
     poster_url = poster_element['src'] if poster_element else None
     
     reviews_link_element = soup.select_one("section.film-reviews a")
     reviews_link = urljoin('https://letterboxd.com',reviews_link_element['href'])
     driver.get(reviews_link)
     time.sleep(2)
     page_source = driver.page_source
     soup = BeautifulSoup(page_source, 'html.parser')

     review_elements= soup.select("div.collapsed-text p")
     review_texts = [review.text.strip() for review in review_elements[:12]]

    

     return[
        movie_title,
        poster_url,
        review_texts

     ]

       
             
  except NoSuchElementException as e:
      print(f"Unable to scrape {movie_url}: {e}")
       
     

all_movie_details={}
i=1
for url in Urls[:] :
        details = scrape_movie_details(url)
        if details:
           all_movie_details[i]= details
           i+=1
        time.sleep(2)
   

directory =os.path.expanduser('~/Downloads/Selenium-tutorial')
print(directory)
if not os.path.exists(directory):
     os.makedirs(directory)

file_path=os.path.join(directory,'movie_details.json')

with open('movie_details.json','w') as outfile:
    json.dump(all_movie_details,outfile,indent=4)



driver .quit()


def preprocess_text(text):
    tokens=word_tokenize(text)
    tokens=[word for word in tokens if word.isalpha()]
    stop_words=set(stopwords.words('english'))
    tokens=[word for word in tokens if word.lower() not in stop_words]
    lemmatizer = WordNetLemmatizer()
    tokens=[lemmatizer.lemmatize(word) for word in tokens]
    return ' '.join(tokens)

analyzer = SentimentIntensityAnalyzer()

def load_movie_data(path_of_file):
    processed_movies = []
    with open(path_of_file, 'r') as file:
        reviews_data = json.load(file)
        for key, value in reviews_data.items():
            processed_reviews = [preprocess_text(review) for review in value[2]]
            sentiment_scores = [analyzer.polarity_scores(review) for review in value[2]]
            movie = {
                'title': value[0],
                'poster_url': value[1],
                'reviews': value[2],
                'processed_reviews': processed_reviews,
                'sentiment_scores': sentiment_scores
            }
            processed_movies.append(movie)
    return processed_movies


database_url='postgresql://postgres:vivov913@localhost:5432/Movies'
engine = create_engine(database_url)
base=declarative_base()

class Movie(base):
    __tablename__='movies'
    id=Column(Integer,primary_key=True)
    title=Column(String)
    poster_url=Column(String)
    reviews = Column(ARRAY(String))
    processed_reviews = Column(ARRAY(String))
    sentiment_scores = Column(ARRAY(JSON))

base.metadata.create_all(engine)
Session=sessionmaker(bind=engine)
session=Session()



def save_movies_to_db(movies):
    i=0
    for movie in movies:
        i+=1
        new_movie=Movie(
            id=i,
            title=movie['title'],
            poster_url=movie['poster_url'],
            reviews=movie['reviews'],
            processed_reviews=movie['processed_reviews'],
            sentiment_scores=movie['sentiment_scores']
        )
        session.add(new_movie)
    session.commit()


movie_file_path = os.path.expanduser('~/Downloads/Selenium-tutorial/movie_details.json')
reviews_data = load_movie_data(movie_file_path)
save_movies_to_db(reviews_data)

