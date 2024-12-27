import tkinter as tk
from tkinter import messagebox
import pandas as pd
from datetime import datetime
from pytz import timezone
import textwrap

df = pd.read_csv("hf://datasets/bloc4488/TMDB-all-movies/TMDB_10k_movies.csv")

df.drop(['id', 'revenue', 'budget', 'imdb_id', 'tagline', 'production_companies', 'director_of_photography', 'music_composer'], axis=1, inplace=True)

df.rename(columns={'Unnamed: 0': 'id'}, inplace=True)

window = tk.Tk()
window.title("[Re]Release")
window.geometry("500x440")
window.configure()

def find_movies():

    tz = timezone('EST')
    today = datetime.now(tz)

    matching = str(today)[4:10]

    if genre.get() == "Any" and era.get() == "Any" and rating.get() == "Any" and runtime.get() == "Any" and lang.get() == "Any":
        matching = str(today)[4:10]

        filtered_df = df[df['release_date'].str[4:] == matching]

        suggestion = filtered_df.sample()

        print("* " * 40)
        print("* Title: " + suggestion['title'].iloc[0] + " " * (80 - len(suggestion['title'].iloc[0]) - len("* Title: ") - 2) + "*")
        print("* Genre(s): " + suggestion['genres'].iloc[0] + " " * (80 - len(suggestion['genres'].iloc[0]) - len("* Genre(s): ") - 2) + "*")
        print("* Language: " + suggestion['spoken_languages'].iloc[0] + " " * (80 - len(suggestion['spoken_languages'].iloc[0]) - len("* Language: ") - 2) + "*")
        print("* Summary: ", end="")

        wrapper = textwrap.TextWrapper(width=60)
        text = wrapper.wrap(text=suggestion['overview'].iloc[0])
        for line in text:
            if text[0] != line:
                print("* " + line + (" " * (80 - len(line) - 4)) + "*")
            else:
                print(line + (" " * (80 - len(line) - len("* Summary: ") - 2) + "*"))
        print("* " * 40)


window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=1)

title = tk.Label(window, text="[Re]Release", font=("Arial", 25))
title.grid(row=0, column=0, columnspan=2, sticky="nsew")


genre_label = tk.Label(window, text="Genre")
genre_label.grid(row=1, column=0, sticky="nsew")

era_label = tk.Label(window, text="Era")
era_label.grid(row=2, column=0, sticky="nsew")

rating_label = tk.Label(window, text="Rating")
rating_label.grid(row=3, column=0, sticky="nsew")

runtime_label = tk.Label(window, text="Runtime")
runtime_label.grid(row=4, column=0, sticky="nsew")

lang_label = tk.Label(window, text="Language")
lang_label.grid(row=5, column=0, sticky="nsew")


genre_choices = ["Any", "Action", "Adventure", "Animation", "Comedy", "Crime", "Documentary", 
     "Drama", "Family", "Fantasy", "History", "Horror", "Music", "Mystery",
     "Science Fiction", "Thriller", "TV Movie", "War", "Western"]

genre = tk.StringVar()
genre.set(genre_choices[0])


genres = tk.OptionMenu(window, genre, *genre_choices)
genres.config(width=20)
genres.grid(row=1, column=1, sticky="nsew")
# window.grid_columnconfigure(1, weight=1)

era_choices = ["Any", "Silent Age (1911-1927)", "Pre-Code Era (1927-1933)", "Golden Age (1933-1965)", 
        "New Hollywood (1965-1983)", "Blockbuster Age (1983-present)"]

era = tk.StringVar()
era.set(era_choices[0])

eras = tk.OptionMenu(window, era, *era_choices)
eras.config(width=20)
eras.grid(row=2, column=1, sticky="nsew")




rating_choices = ["Any", "Acclaim (8.0 - 10.0)", "Positive (6.0-7.9)", "Mixed (4.0-5.9)", "Negative (2.0-3.9)", "Terrible (0.0-1.9)"]

rating = tk.StringVar()
rating.set(rating_choices[0])

ratings = tk.OptionMenu(window, rating, *rating_choices)
ratings.config(width=20)
ratings.grid(row=3, column=1, sticky="nsew")



runtime_choices = ["Any", "An Hour and a Half (or less)", "Two Hours (ish)", "Three Hours and Beyond"]

runtime = tk.StringVar()
runtime.set(runtime_choices[0])

runtimes = tk.OptionMenu(window, runtime, *runtime_choices)
runtimes.config(width=20)
runtimes.grid(row=4, column=1, sticky="nsew")



lang_choices = ["Any", "Czech", "Danish", "Dutch",  "English", "Finnish", "French", "German", 
                     "Hebrew", "Hindi", "Italian", "Japanese", "Korean",
                    "Mandarin Chinese", "Norwegian", "Polish", "Portuguese", "Russian", 
                     "Spanish", "Swedish", "Thai", "Turkish", ]

lang = tk.StringVar()
lang.set(lang_choices[0])

langs = tk.OptionMenu(window, lang, *lang_choices)
langs.config(width=20)
langs.grid(row=5, column=1, sticky="nsew")

find = tk.Button(text="Find Movies!", command=find_movies)
find.grid(row=6, column=0, columnspan=2, sticky="nsew", pady=20)

# frame.pack()
window.mainloop()