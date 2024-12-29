# Necessary imports
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import pandas as pd
from datetime import datetime
import textwrap

FILE = "hf://datasets/bloc4488/TMDB-all-movies/TMDB_10k_movies.csv"

# Defining dropdown menus
LANG_CHOICES = ["Any", "Bahasa melayu", "বাংলা", "广州话 / 廣州話", "Český", "Dansk", "Nederlands",  "English", 
                "Finnish", "Français", "Deutsch", "עִבְרִית", "हिन्दी", "Italiano", 
                "日本語", "한국어/조선말", "普通话", "Norsk", "Polski", "Português", "Pусский", 
                     "Español", "svenska", "ภาษาไทย", "Türkçe", ]

GENRE_CHOICES = ["Any", "Action", "Adventure", "Animation", "Comedy", "Crime", "Documentary", 
     "Drama", "Family", "Fantasy", "History", "Horror", "Music", "Mystery",
     "Romance", "Science Fiction", "Thriller", "TV Movie", "War", "Western"]

ERA_CHOICES = ["Any", "Silent Age (1911-1926)", "Pre-Code Era (1927-1933)", "Golden Age (1934-1965)", 
        "New Hollywood (1966-1983)", "Blockbuster Age (1984-present)"]

RATING_CHOICES = ["Any", "Acclaim (8.0 - 10.0)", "Positive (6.0-8.0)", "Mixed (4.0-6.0)", "Negative (2.0-4.0)", "Terrible (0.0-2.0)"]

RUNTIME_CHOICES = ["Any", "Short Film", "An Hour and a Half", "Two Hours (ish)", "Three Hours (ish) and Beyond"]

# Creates a tk instance and configures it
window = tk.Tk()
window.title("[Re]Release")
window.geometry("500x440")
window.configure()

frame = ttk.Frame(window)
frame.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=20, pady=20)

title = tk.Label(frame, text="[Re]Release", font=("Arial", 25))
title.grid(row=0, column=0, columnspan=2, sticky="nsew", pady=20)

# Saves the date of the query
matching = str(datetime.now())[4:10]

def read_into_df(file, matching):

    # Reads the data from Hugging Face -- 10k Movie Dataset from TMDb
    df = pd.read_csv(file)

    # Removes irrelevant columns from df
    df.drop(['id', 'revenue', 'vote_count', 'status', 'budget', 
                'imdb_id', 'tagline', 'production_companies', 'director_of_photography', 
                'budget', 'original_language', 'music_composer', 'popularity',
                'tagline', 'production_countries', 'cast', 'director', 'writers',
                'producers', 'original_title'], axis=1, inplace=True)

    # Removes movies with null overviews
    df = df.dropna(subset=['overview'])

    # Renames 'Unamed: 0' column to clearly be the ID
    df.rename(columns={'Unnamed: 0': 'id'}, inplace=True)

    # Creates the column 'years', which saves the year of release as an int
    df['years'] = df['release_date'].str[0:4]
    df['years'] = pd.to_numeric(df['years'], errors='coerce')

    # Creates columsn based on movie year of release
    df['Silent Age (1911-1926)'] = df['years'].apply(lambda x: x <= 1926 if pd.notnull(x) else False)
    df['Pre-Code Era (1927-1933)'] = df['years'].apply(lambda x: 1927 <= x <= 1933 if pd.notnull(x) else False)
    df['Golden Age (1934-1965)'] = df['years'].apply(lambda x: 1934 <= x <= 1965 if pd.notnull(x) else False)
    df['New Hollywood (1966-1983)'] = df['years'].apply(lambda x: 1966 <= x <= 1983 if pd.notnull(x) else False)
    df['Blockbuster Age (1984-present)'] = df['years'].apply(lambda x: 1984 <= x <= 2024 if pd.notnull(x) else False)

    # Creates columns based on movie level of acclaim
    df['Acclaim (8.0 - 10.0)'] = df['vote_average'].apply(lambda x: 8.0 <= x <= 10.0 if pd.notnull(x) else False)
    df['Positive (6.0-8.0)'] = df['vote_average'].apply(lambda x: 6.0 <= x < 8.0 if pd.notnull(x) else False)
    df['Mixed (4.0-6.0)'] = df['vote_average'].apply(lambda x: 4.0 <= x < 6.0 if pd.notnull(x) else False)
    df['Negative (2.0-4.0)'] = df['vote_average'].apply(lambda x: 2.0 <= x < 4.0 if pd.notnull(x) else False)
    df['Terrible (0.0-2.0)'] = df['vote_average'].apply(lambda x: 0.0 <= x < 2.0 if pd.notnull(x) else False)

    # Creates columns based on movie runtime
    df['Short Film'] = df['runtime'].apply(lambda x: 0.00 < x/60 <= 0.5 if pd.notnull(x) else False)
    df['An Hour and a Half'] = df['runtime'].apply(lambda x: 1.0 < x/60 <= 1.45 if pd.notnull(x) else False)
    df['Two Hours (ish)'] = df['runtime'].apply(lambda x: 1.45 < x/60 <= 2.45 if pd.notnull(x) else False)
    df['Three Hours (ish) and Beyond'] = df['runtime'].apply(lambda x: 2.45 < x/60 if pd.notnull(x) else False)

    # Filters the movies based on the release date (matching)
    df = df[df['release_date'].str[4:] == matching]

    return df

def find_movies(df : pd.DataFrame, matching, genre : tk.StringVar, era : tk.StringVar, rating : tk.StringVar, runtime : tk.StringVar, lang : tk.StringVar):
    # Filters based on genre selection
    if genre.get() != "Any":
        df['contains_genre'] = df['genres'].str.contains(genre.get(), case=False, na=False)
        df = df[df['contains_genre'] == True]
    
    # Filters based on era selection
    elif era.get() != "Any":
        df = df[df[era.get()] == True]
    
    # Filters based on rating selection
    elif rating.get() != "Any":
        df = df[df[rating.get()] == True]

    # Filters based on runtime selection
    elif runtime.get() != "Any":
        df = df[df[runtime.get()] == True]
    
    # Filters based on language selection
    elif lang.get() != "Any":
        df['contains_lang'] = df['spoken_languages'].str.contains(lang.get(), case=False, na=False)
        df = df[df['contains_lang'] == True]

    # If the filters result in at least one option to recommend
    if df.empty == False:
        suggestion = df.sample()

        print("* " * 50)
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
    
    # If there are no movies that fit the specifications
    else:
        print(f"There have been no movies released on {matching[1:3]}/{matching[4:]} that match your search.")


def make_option_menu(parent, dropdown, text, row, column, sticky):
    label = tk.Label(parent, text=text)
    label.grid(row=row, column=column, sticky=sticky)
    var = tk.StringVar()
    var.set(dropdown[0])
    choices = tk.OptionMenu(parent, var, *dropdown)
    choices.config(width=20)
    choices.grid(row=row, column=column + 1, stick=sticky)
    return var

df = read_into_df(FILE, matching)

genre = make_option_menu(frame, GENRE_CHOICES, "Genre", 1, 0, "nsew")
era = make_option_menu(frame, ERA_CHOICES, "Era", 2, 0, "nsew")
rating = make_option_menu(frame, RATING_CHOICES, "Rating", 3, 0, "nsew")
runtime = make_option_menu(frame, RUNTIME_CHOICES, "Runtime", 4, 0, "nsew")
lang = make_option_menu(frame, LANG_CHOICES, "Language", 5, 0, "nsew")

# Search Button
find = tk.Button(frame, text="Find Movies!", command=lambda : find_movies(df, matching, genre, era, rating, runtime, lang))
find.grid(row=6, column=0, columnspan=2, sticky="nsew", pady=10)

window.mainloop()