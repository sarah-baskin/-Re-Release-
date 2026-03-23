from datetime import datetime
from zoneinfo import ZoneInfo
from tmdbv3api import TMDb
from tmdbv3api import Movie
from tmdbv3api import Discover
from tmdbv3api import Genre
from tmdbv3api import Search
import os
from dotenv import load_dotenv
from requests import get
import json
from user_filters import UserFilters

# TODO: testing for watch_region parameter filtering
# TODO: testing for language parameter filtering

def set_tmdb_language(tmdb : TMDb, locale):
    tmdb.language = locale
    return tmdb

def filter_movies(tmdb : TMDb, 
                  filters : UserFilters, 
                  curr_date : datetime):
    discover = Discover(tmdb)

    year = curr_date.year
    month = curr_date.month
    day = curr_date.day

    filtered = []
    # 1894
    for curr in range(1894, year):
        inst = discover.discover_movies({
            'include_adult':filters.get_incl_adult(),
            'primary_release_date.gte': f'{curr}-{month}-{day}',
            'primary_release_date.lte': f'{curr}-{month}-{day}',
            'with_genres': filters.get_selected_genre(),
            'watch_region': filters.get_region()
        })
        filtered.append(inst)

    return filtered

def further_filtering(filtered_movies, filters : UserFilters):

    more_filtered = []
    movie = Movie()
    for entry in filtered_movies:
        results = entry["results"]
        for result in results:
            movie_id = result["id"]
            to_append = True
            details = movie.details(movie_id)
            if filters.get_min_run() and not(details.runtime >= filters.get_min_run()):
                to_append = False
            elif not filters.get_min_run() and details.runtime < 1:
                to_append = False
            elif filters.get_max_run() and not(details.runtime <= filters.get_max_run()):
                to_append = False
            elif filters.get_min_vote_avg() and not(details.vote_average >= filters.get_min_vote_avg()):
                to_append = False
            elif details.status != "Released":
                to_append = False
            if details.spoken_languages:
                for lang in details.spoken_languages:
                    if lang not in filters.get_lang_list():
                        to_append = False
            else:
                if filters.get_lang_list()["iso_639_1"] != details.original_language:
                    to_append = False    
            if to_append:
                result["watch_providers"] = movie.watch_providers(movie_id)
                result["runtime"] = details.runtime
                more_filtered.append(result)
    return more_filtered

def time_in_hours(runtime):
    num_hours = runtime // 60
    num_mins = runtime % 60
    if num_hours == 0:
        return f"{num_mins} minutes"
    else:
        return f"{num_hours}h {num_mins}"

def where_to_watch(options, region):

    print("Streaming: ", end="")
    for option in options["results"]:
        if option["results"] == region:
            result = option[region]
            if result[1][region] == "rent":
                for rented in result[1]["rent"]:
                    print("Rent: ", rented["provider_name"])
            if result[1][region] == "buy":
                for bought in result[1]["buy"]:
                    print("Buy: ", bought["provider_name"])
            if result[1][region] == "flatrate":
                for flatrate in result[1]["flatrate"]:
                    print("Flatrate: ", flatrate["provider_name"])

def genre_translation(filters : UserFilters, genre_ids):

    genres = []
    for id in genre_ids:
        for genre in filters.get_genre_list():
            if id in genre:
                genres.append(genre[1])
    return ", ".join(genres)

def print_movie_info(filters, filtered):
    if len(filtered) == 0:
        print("There are no movies matching your search. Please try modifying your parameters.")
    else:
        for item in filtered:
            print("Title: ", item['title'])
            print("Genre(s): ", genre_translation(filters, item["genre_ids"]))
            print("Release Year: ", item["release_date"][:item["release_date"].index("-")])
            print("Overview: ", item["overview"])
            if item["vote_count"] > 0:
                print("Rating: ", item["vote_average"], "out of", item["vote_count"], "votes.")
            print("Runtime: ", time_in_hours(item["runtime"]))
            if item["watch_providers"]["results"]:
                where_to_watch(item["watch_providers"], filters.get_region())
            print()


if __name__ == "__main__":
    
    load_dotenv()
    tmdb = TMDb()
    tmdb = set_tmdb_language(tmdb, "en")
    tmdb.api_key = os.getenv("API_KEY")
    tmdb.debug = True

    filters = UserFilters(tmdb, "America/New_York", min_runtime=60)
    filters.set_genres()
    filters.set_languages()

    filtered_movies = filter_movies(tmdb, filters, filters.get_curr_date())
    filtered_movies = further_filtering(filtered_movies, filters)
    print_movie_info(filters, filtered_movies)

    

    
    