import random

# change location of these two functions?
from tmdbv3api import Genre
from tmdbv3api import TMDb
import os
from requests import get
import json
from zoneinfo import ZoneInfo
from datetime import datetime


class UserFilters():
    
    def __init__(self,
                 tmdb,
                 time_zone, 
                 min_runtime=None, 
                 max_runtime=None, 
                 incl_adult=False, 
                 min_vote_avg=None):
        self.tmdb = tmdb
        self.chosen_genre = None
        self.genres = self.get_genres(self.tmdb)
        self.langs = self.get_original_languages()
        self.curr_date = self.get_current_date(time_zone)
        self.min_runtime = min_runtime
        self.max_runtime = max_runtime
        self.incl_adult = incl_adult
        self.min_vote_avg = min_vote_avg
    
    def get_current_date(self, timezone):
        tz = ZoneInfo(timezone)
        now = datetime.now(tz=tz)
        curr_date = now.date()
        return curr_date


    def get_genres(self, tmdb : TMDb):
        genres = Genre(tmdb)
        genre_dict = genres.movie_list()
        genre_list = []
        for genre in genre_dict["genres"]:
            genre_list.append((genre["id"], genre["name"]))
        return genre_list
    
    def get_original_languages(self):
        access_token = os.getenv("READ_ACCESS_TOKEN")
        language_list = []
        headers = {
            "Authorization": "Bearer " + access_token,
            "accept": "application/json"
        }

        result = get(url="https://api.themoviedb.org/3/configuration/languages",
            headers=headers
            )
        json_result = json.loads(result.content)
        for lang in json_result:
            language_list.append(lang)
        return language_list


    def set_genres(self):
        chosen = random.randint(0, len(self.genres))
        self.chosen_genre = 18

    def set_languages(self):
        num_langs = random.randint(1,2)
        chosen = random.sample(self.langs, num_langs)
        self.langs = {'english_name': 'English', 'iso_639_1': 'en', 'name': 'English'}
    
    def get_incl_adult(self):
        return self.incl_adult

    def get_genre_list(self):
        return self.genres
    
    def get_selected_genre(self):
        return self.chosen_genre
    
    def get_lang_list(self):
        return self.langs
    
    def get_min_run(self):
        return self.min_runtime
    
    def get_max_run(self):
        return self.max_runtime
    
    def get_min_vote_avg(self):
        return self.min_vote_avg
    
    def get_region(self):
        return "US"
    
    def get_curr_date(self):
        return self.curr_date
    


    