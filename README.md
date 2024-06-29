# WatchParty
Project Overview

This project aims to create a movie recommendation system that suggests movies to users based on the sentiment of their input text. The system uses Natural Language Processing (NLP) techniques and sentiment analysis to find movies with reviews that have similar sentiment scores to the user's input.

Features

Sentiment Analysis: Utilizes VADER Sentiment Intensity Analyzer to compute sentiment scores.
Text Preprocessing: Tokenizes, lemmatizes, and removes stopwords from the user input.
Recommendation Engine: Calculates similarity between user input sentiment and movie review sentiments.
Randomized Recommendations: Provides random movie recommendations from the most similar movies.
User Session Management: Remembers users and their activity across sessions.
Technology Stack

Python Flask: For creating the web application.

SQLAlchemy: For database ORM.

VADER Sentiment Analyzer: For sentiment analysis.

Beautiful Soup: For web scraping.

PostgreSQL: Database to store movie details and reviews.

AWS: For cloud deployment.


##Project Setup

1. Environment Setup
Install Dependencies

```bash
pip install -r requirements.txt
```
NLTK Data

Ensure necessary NLTK data files are downloaded:

```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
```


2. Database Setup
Create a PostgreSQL database and table to store movie data.

```sql
CREATE TABLE movies (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255),
    poster_url VARCHAR(255),
    reviews TEXT[],
    processed_reviews TEXT[],
    sentiment_scores JSON[]
);
```

3. Flask Application
Create a Flask application (app.py):

```python
from flask import Flask, jsonify, request, render_template
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import json
import random
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)

def preprocess_text(text):
    tokens = word_tokenize(text)
    tokens = [word for word in tokens if word.isalpha()]
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word.lower() not in stop_words]
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    return ' '.join(tokens)

# Load the movies data from JSON file
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
        movie_sentiments = [score['compound'] for score in movie['sentiment_scores'] if 'compound' in score]
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

application = Flask(__name__)

@application.route('/')
def index():
    return render_template('index.html')

@application.route('/recommend', methods=['POST'])
def recommend_route():
    user_input = request.json.get('description', '')
    if not user_input:
        return jsonify({"error": "Invalid input"}), 400
    recommendations = get_recommendations(user_input)
    return jsonify(recommendations)

if __name__ == "__main__":
    application.run(host="0.0.0.0", debug=False)
```

