import tkinter as tk
from tkinter import messagebox
import pandas as pd
from datetime import datetime
from pytz import timezone
import textwrap



lang_choices = ["Any", "Bahasa melayu", "বাংলা", "广州话 / 廣州話", "Český", "Dansk", "Nederlands",  "English", 
                "Finnish", "Français", "Deutsch", "עִבְרִית", "हिन्दी", "Italiano", 
                "日本語", "한국어/조선말", "普通话", "Norsk", "Polski", "Português", "Pусский", 
                     "Español", "svenska", "ภาษาไทย", "Türkçe", ]


window = tk.Tk()
window.title("[Re]Release")
window.geometry("500x440")
window.configure()

def find_movies():

    

    df = pd.read_csv("hf://datasets/bloc4488/TMDB-all-movies/TMDB_10k_movies.csv")

    df.drop(['id', 'revenue', 'budget', 'imdb_id', 'tagline', 'production_companies', 'director_of_photography', 'music_composer'], axis=1, inplace=True)

    df.rename(columns={'Unnamed: 0': 'id'}, inplace=True)

    df = df.dropna(subset=['overview'])

    df['years'] = df['release_date'].str[0:4]
    df['years'] = pd.to_numeric(df['years'], errors='coerce')


    df['silent'] = df['years'].apply(lambda x: x <= 1926 if pd.notnull(x) else False)
    df['pre_code'] = df['years'].apply(lambda x: 1927 <= x <= 1933 if pd.notnull(x) else False)
    df['golden_age'] = df['years'].apply(lambda x: 1934 <= x <= 1965 if pd.notnull(x) else False)
    df['new_hollywood'] = df['years'].apply(lambda x: 1966 <= x <= 1983 if pd.notnull(x) else False)
    df['blockbuster'] = df['years'].apply(lambda x: 1984 <= x <= 2024 if pd.notnull(x) else False)


    df['Acclaim (8.0 - 10.0)'] = df['vote_average'].apply(lambda x: 8.0 <= x <= 10.0 if pd.notnull(x) else False)
    df['Positive (6.0-8.0)'] = df['vote_average'].apply(lambda x: 6.0 <= x < 8.0 if pd.notnull(x) else False)
    df['Mixed (4.0-6.0)'] = df['vote_average'].apply(lambda x: 4.0 <= x < 6.0 if pd.notnull(x) else False)
    df['Negative (2.0-4.0)'] = df['vote_average'].apply(lambda x: 2.0 <= x < 4.0 if pd.notnull(x) else False)
    df['Terrible (0.0-2.0)'] = df['vote_average'].apply(lambda x: 0.0 <= x < 2.0 if pd.notnull(x) else False)

    df['Short Film'] = df['runtime'].apply(lambda x: 0.00 < x/60 <= 0.5 if pd.notnull(x) else False)
    df['An Hour and a Half'] = df['runtime'].apply(lambda x: 1.0 < x/60 <= 1.45 if pd.notnull(x) else False)
    df['Two Hours (ish)'] = df['runtime'].apply(lambda x: 1.45 < x/60 <= 2.45 if pd.notnull(x) else False)
    df['Three Hours (ish) and Beyond'] = df['runtime'].apply(lambda x: 2.45 < x/60 if pd.notnull(x) else False)


    tz = timezone('EST')
    today = datetime.now(tz)

    matching = str(today)[4:10]

    era_assignment = {"Silent Age (1911-1926)" : "silent", "Pre-Code Era (1927-1933)" : "pre_code", "Golden Age (1934-1965)"  : "golden_age", 
        "New Hollywood (1966-1983)" : "new_hollywood", "Blockbuster Age (1984-present)" : "blockbuster"}


    df = df[df['release_date'].str[4:] == matching]

    if genre.get() != "Any":
        df['contains_genre'] = df['genres'].str.contains(genre.get(), case=False, na=False)
        df = df[df['contains_genre'] == True]
    
    elif era.get() != "Any":
        df = df[df[era_assignment[era.get()]] == True]
    
    elif rating.get() != "Any":
        df = df[df[rating.get()] == True]

    elif runtime.get() != "Any":
        df = df[df[runtime.get()] == True]
    
    elif lang.get() != "Any":
        df['contains_lang'] = df['spoken_languages'].str.contains(lang.get(), case=False, na=False)
        df = df[df['contains_lang'] == True]
        print(df['title'])

    if df.empty == False:
        suggestion = df.sample()

        print("* " * 50)
        # print(suggestion['release_date'])
        print("* Title: " + suggestion['title'].iloc[0] + " " * (100 - len(suggestion['title'].iloc[0]) - len("* Title: ") - 2) + "*")
        print("* Genre(s): " + suggestion['genres'].iloc[0] + " " * (100 - len(suggestion['genres'].iloc[0]) - len("* Genre(s): ") - 2) + "*")
        print("* Language: " + suggestion['spoken_languages'].iloc[0] + " " * (100 - len(suggestion['spoken_languages'].iloc[0]) - len("* Language: ") - 2) + "*")
        
        wrapper = textwrap.TextWrapper(width=60)
        print("* Summary: ", end="")
        text = wrapper.wrap(text=suggestion['overview'].iloc[0])
        for line in text:
            if text[0] != line:
                print("* " + line + (" " * (100 - len(line) - 4)) + "*")
            else:
                print(line + (" " * (100 - len(line) - len("* Summary: ") - 2) + "*"))
        print("* " * 50)
    
    else:
        print(f"There have been no movies released on {matching[1:3]}/{matching[4:]} that match your search.")


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
     "Romance", "Science Fiction", "Thriller", "TV Movie", "War", "Western"]

genre = tk.StringVar()
genre.set(genre_choices[0])


genres = tk.OptionMenu(window, genre, *genre_choices)
genres.config(width=20)
genres.grid(row=1, column=1, sticky="nsew")
# window.grid_columnconfigure(1, weight=1)

era_choices = ["Any", "Silent Age (1911-1926)", "Pre-Code Era (1927-1933)", "Golden Age (1934-1965)", 
        "New Hollywood (1966-1983)", "Blockbuster Age (1984-present)"]

era = tk.StringVar()
era.set(era_choices[0])

eras = tk.OptionMenu(window, era, *era_choices)
eras.config(width=20)
eras.grid(row=2, column=1, sticky="nsew")




rating_choices = ["Any", "Acclaim (8.0 - 10.0)", "Positive (6.0-8.0)", "Mixed (4.0-6.0)", "Negative (2.0-4.0)", "Terrible (0.0-2.0)"]

rating = tk.StringVar()
rating.set(rating_choices[0])

ratings = tk.OptionMenu(window, rating, *rating_choices)
ratings.config(width=20)
ratings.grid(row=3, column=1, sticky="nsew")



runtime_choices = ["Any", "Short Film", "An Hour and a Half", "Two Hours (ish)", "Three Hours (ish) and Beyond"]

runtime = tk.StringVar()
runtime.set(runtime_choices[0])

runtimes = tk.OptionMenu(window, runtime, *runtime_choices)
runtimes.config(width=20)
runtimes.grid(row=4, column=1, sticky="nsew")





lang = tk.StringVar()
lang.set(lang_choices[0])

langs = tk.OptionMenu(window, lang, *lang_choices)
langs.config(width=20)
langs.grid(row=5, column=1, sticky="nsew")

find = tk.Button(text="Find Movies!", command=find_movies)
find.grid(row=6, column=0, columnspan=2, sticky="nsew", pady=20)

# frame.pack()
window.mainloop()