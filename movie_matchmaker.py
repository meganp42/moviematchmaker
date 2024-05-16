#Megan Ponce 
#CS110
#Final Project 

import logging
from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# logging to track the program as I code
logging.basicConfig(level=logging.DEBUG)  # Set logging level to DEBUG

# Function to map personality words to TMDb genre IDs
def map_personality_to_genre(personality_word):
    genre_map = {
        'romantic': 10749,  # Romance genre ID
        'fun': 35,          # Comedy genre ID
        'happy': 10751,     # Family genre ID
        'sensation seekers': 27,  # Horror genre ID
        'problem-solver': 9648,   # Mystery genre ID
        'realistic': 18,    # Drama genre ID
        'adventurous': 28   # Action genre ID
    }
    return genre_map.get(personality_word, None)  # Return None if personality word not found

# Function to search for movies based on personality words using TMDb API
def search_movies_by_personality(personality_words):
    base_url = 'https://api.themoviedb.org/3/discover/movie'
    recommended_movies = []

    #looping through the words from the user
    for word in personality_words:
        genre_id = map_personality_to_genre(word)
        if genre_id:
            params = {
                'api_key': '4a2e0a6048e6398f392c9e3ded4640e8',
                'with_genres': genre_id,    # Filter by genre ID
                'sort_by': 'popularity.desc',  # Sort by popularity
                'page': 1                    # Page number
            }
            response = requests.get(base_url, params=params)
            if response.status_code == 200:
                data = response.json()
                if 'results' in data:
                    for movie in data['results']:
                        recommended_movies.append(movie['title'])

    return recommended_movies

#opening page of the website
@app.route('/')
def main():
    return render_template('index.html')

#switching to movie recommedation page of the website
@app.route('/recommend', methods=['POST', 'GET'])
def recommend_movies():
    if request.method == 'POST':
        personality_words = request.form.getlist('personality')
        logging.debug(f"Selected personality words: {personality_words}")  # Log selected personality words
        movies = search_movies_by_personality(personality_words) #searching for movies
        if movies:
            logging.debug(f"Recommended movies: {movies}")  # Log recommended movies
            return render_template('recommendations.html', movies=movies)
        else:
            logging.warning("No movies found for the given personality words.")  # Log a warning message
            return render_template('error.html')  # switch to error page on website (with start over button to try again)
    else:
        logging.error("Invalid request method")  # Log an error message
        return "Invalid request method"

if __name__ == "__main__":
    app.run(debug=True)
