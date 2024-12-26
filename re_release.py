import pandas as pd
from datetime import datetime
from pytz import timezone

df = pd.read_csv("hf://datasets/bloc4488/TMDB-all-movies/TMDB_10k_movies.csv")

df.drop(['id', 'revenue', 'budget', 'imdb_id', 'tagline', 'production_companies', 'director_of_photography', 'music_composer'], axis=1, inplace=True)

df.rename(columns={'Unnamed: 0': 'id'}, inplace=True)

# tz = timezone('EST')
# today = datetime.now(tz)


# matching = str(today)[4:10]

# for index, row in df.iterrows():
#     if str(row['release_date'])[4:] == matching:
#         print("--------------------------------------------------------------")
#         print("**", row['title'], "**")
#         print(row['genres'])
#         print(row['overview'])
#         print()