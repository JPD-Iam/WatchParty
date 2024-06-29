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

Python
Flask: For creating the web application.
SQLAlchemy: For database ORM.
VADER Sentiment Analyzer: For sentiment analysis.
Beautiful Soup: For web scraping.
PostgreSQL: Database to store movie details and reviews.
AWS: For cloud deployment.
Project Setup

1. Environment Setup
Install Dependencies
