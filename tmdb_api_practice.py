# option to check out a movie from your local library
# option to filter based on streaming services that you own (and are available in your country)

from tmdbv3api import TMDb
from tmdbv3api import Movie
from tmdbv3api import Discover
import os
from dotenv import load_dotenv

tmdb = TMDb()

load_dotenv()

tmdb.api_key = os.getenv("API_KEY")

tmdb.language = 'en'
tmdb.debug = True

discover = Discover()

filtered = discover.discover_movies({
    'primary_release_date.gte': '2023-12-23',
    'primary_release_date.lte': '2023-12-23'
})

for movie in filtered:
    id = movie.id
    title = movie.title
    movie = Movie(movie)
    results = movie.watch_providers(id)
    if results["results"]:
        for result in results["results"]:
            result = dict(result)
            if result["results"] == "US":
                print(title)
                where_to_watch = [dict(item) for item in result["US"] if type(item) != str]
                for option in where_to_watch:
                    if option["US"] == "rent":
                        for rented in option["rent"]:
                            print("Rent: ", rented["provider_name"])
                    if option["US"] == "buy":
                        for bought in option["buy"]:
                            print("Buy: ", bought["provider_name"])
                    if option["US"] == "flatrate":
                        for flatrate in option["flatrate"]:
                            print("Flatrate: ", flatrate["provider_name"])
                print()