
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
nltk.download('punkt',quiet=True)
nltk.download('stopwords',quiet=True)
nltk.download('wordnet',quiet=True)
import json
from sqlalchemy import create_engine, Column, Integer, String, ARRAY, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import random



def preprocess_text(text):
    tokens=word_tokenize(text)
    tokens=[word for word in tokens if word.isalpha()]
    stop_words=set(stopwords.words('english'))
    tokens=[word for word in tokens if word.lower() not in stop_words]
    lemmatizer = WordNetLemmatizer()
    tokens=[lemmatizer.lemmatize(word) for word in tokens]
    return ' '.join(tokens)
    

with open('movies.json', 'r') as f:
    movies = json.load(f)
    

# Initialize the VADER sentiment analyzer
analyzer = SentimentIntensityAnalyzer()


def get_recommendations(user_input):
   
    processed_input = preprocess_text(user_input)
    input_sentiment = analyzer.polarity_scores(processed_input)
    input_sentiment_score = input_sentiment['compound']

    # Calculate similarities
    recommendations = []
    for movie in movies:
        movie_sentiments = [score['compound'] for score in movie['sentiment_scores']]
        if movie_sentiments:  # Avoid division by zero
            similarity = sum([abs(input_sentiment_score - score) for score in movie_sentiments]) / len(movie_sentiments)
            recommendations.append({
                'title': movie['title'],
                'poster_url': movie['poster_url'],
                'similarity': similarity
            })

    recommendations = sorted(recommendations, key=lambda x: x['similarity'])
    random_recommendations = random.sample(recommendations[:10], 2)  # Select 2 random recommendations from the top 10
    return random_recommendations
    

    

