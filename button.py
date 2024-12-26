import tkinter as tk
from tkinter import messagebox

# def button_click():
#     print("Button clicked!")

# window = tk.Tk()
# button = tk.Button(window, text="Click me!", command=button_click)
# button.pack()
# window.mainloop()

window = tk.Tk()
window.title("[Re]Release")
window.geometry("500x440")
# window.configure(bg='#333333')
# frame = tk.Frame(bg='#333333')


genre_label = tk.Label(window, text="Genre")
genre_label.grid(row=0, column=0)

era_label = tk.Label(window, text="Era")
era_label.grid(row=1, column=0)

rating_label = tk.Label(window, text="Rating")
rating_label.grid(row=2, column=0)

runtime_label = tk.Label(window, text="Runtime")
runtime_label.grid(row=3, column=0)

lang_label = tk.Label(window, text="Language")
lang_label.grid(row=4, column=0)


genre_choices = ["Any", "Action", "Adventure", "Animation", "Comedy", "Crime", "Documentary", 
     "Drama", "Family", "Fantasy", "History", "Horror", "Music", "Mystery",
     "Science Fiction", "Thriller", "TV Movie", "War", "Western"]

genre = tk.StringVar()
genre.set(genre_choices[0])


genres = tk.OptionMenu(window, genre, *genre_choices)
genres.grid(row=0, column=1)

era_choices = ["Any", "Silent Age (1911-1927)", "Pre-Code Era (1927-1933)", "Golden Age (1933-1948)", 
        "Fall of the Studio System (1948-1965)", "New Hollywood (1965-1983)", "Blockbuster Age (1983-present)"]

era = tk.StringVar()
era.set(era_choices[0])

eras = tk.OptionMenu(window, era, *era_choices)
eras.grid(row=1, column=1)



rating_choices = ["Any", "Acclaim (8.0 - 10.0)", "Positive (6.0-7.9)", "Mixed (4.0-5.9)", "Negative (2.0-3.9)", "Terrible (0.0-1.9)"]

rating = tk.StringVar()
rating.set(rating_choices[0])

ratings = tk.OptionMenu(window, rating, *rating_choices)
ratings.grid(row=2, column=1)



runtime_choices = ["Any", "An Hour and a Half (or less)", "Two Hours (ish)", "Three Hours and Beyond"]

runtime = tk.StringVar()
runtime.set(runtime_choices[0])

runtimes = tk.OptionMenu(window, runtime, *runtime_choices)
runtimes.grid(row=3, column=1)



lang_choices = ["Any", "Czech", "Danish", "Dutch",  "English", "Finnish", "French", "German", 
                     "Hebrew", "Hindi", "Italian", "Japanese", "Korean",
                    "Mandarin Chinese", "Norwegian", "Polish", "Portuguese", "Russian", 
                     "Spanish", "Swedish", "Thai", "Turkish", ]

lang = tk.StringVar()
lang.set(lang_choices[0])

langs = tk.OptionMenu(window, lang, *lang_choices)
langs.grid(row=4, column=1)

find = tk.Button(text="Find Movies!")
find.grid(row=5, column=0, columnspan=2)

# frame.pack()
window.mainloop()