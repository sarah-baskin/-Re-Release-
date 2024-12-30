# [Re]Release

Last updated: 12.30.2024

## Introduction
It's a problem that we've all experienced many times before... you want to watch a movie, maybe you have a vague sense that you want it to be a comedy, plus you've been feeling a bit nostalgic recently so you're feeling an early 2000s romp as well, and so you hop on Netflix, or Disney+, or some other preferred streaming platform, and do a quick search to find something that fits that bill and BAMM! A thousand movies come at you, some of which fit your preferred requirements, but many of which don't. And so now, before you can even really wittle the choices down to those that you're actually interested in, you need to make your way through a bunch of random movies. The choices pile up until you decide to inevitably just rewatch New Girl for the millionth time (not speaking from personal experience or anything).

Choice paralysis is something that we're faced with seemingly everywhere now, but I have noticed a certain pervacity in the world of streaming in particular. Platforms have paid a lot of money to be able to offer the widest breadth possible of classic films, superhero blockbusters, romcom classics, detective capers, and niche international offerings, and so streamers want you to engage with as much of that content:tm: before you actually hunker down and choose what to watch. That's great for streaming minutes, certainly, and shows just how much traffic a page is receiving, but for us as as the viewers, this can become mentally taxing.

There's a certain beauty to having limited options, to be able to have a handful of choices and selecting the ideal out of what you could realistically want, not what you could conceivably want. But there don't seem to be a lot of applications out there that directly address this problem, or at least, there don't seem to be a lot of applications out there that directly address this problem in a way that is most benficial to me as a consumer. And since anything that I work on I make first and foremost to address a problem that I myself face, I started to wonder if there was indeed a better way to go about answering the age old question of "What do you want to watch?". 

I wanted to design a sleek, simplistic yet stylish application that would allow users to search for films based on specific criteria, and then generate options one at a time that match the preferences stated. This completely eliminates choice paralysis, literally only giving you one movie to consider at a time.

## Development
Since I was envisioning an app with myself in mind as the ideal consumer, there were a few important things that I knew I had to take into account:

1. **Avoid repetition**

This is the big one for me when it comes to recommendation systems. I can't stand it when I find a good service that is consistently able to give me options that fit my preferences, but then after a while it starts regurgitating the same recommendations. If I already saw the movie recently, I don't necessarily want to rewatch it just yet, I want to find something new! My solution for this problem is to use the date of a particular query as a "seed value" of sorts. The application notes the day on which the user is accessing the application, and only returns films that were also released on that given day. This ensures that if someone looks for a recommendation one week, they won't accidentally get that same film recommended again in a few days. This touch also creates a connection to each of the films, giving the user a throughline to pull from that will make them more likely to actually choose the movie that is recommended to them.

2. **Ensure that recommendations contain just the right amount of information**

The question of what metadata to include in a recommendation is a heavy one. For me, I like mostly the barebones. Film title, spoken languages, genre, and a brief summary generally is good enough. The summary specifically is key, as without it, it can be hard to really get the feel of a film. I might make more additions to the recommendations later on, but for now I feel that this is enough for a user to get a sense of whether or not a movie is right for them.


3. **Encourage engagement with obscure or unheard of films**

The other issue that tends to come up when you rely on streaming services or Google searches to recommend you movies is that the recommendation is usually at least in part based on how popular certain films are. Although this leads to an increased chance of satisfaction with a recommendation, this can also in turn limit people from discovering hidden gems or more obscure outings. My application generates recommendations purely based on the metrics laid out above, meaning that the popularity of a film has no impact on the likelihood of it being recommended.

## Tools and Methods

The application itself was designed using `tkinter`, Python's in-house library used for making stripped-down apps.

For the backend movie database, I used TMDb, which houses movie meta data taken from IMDb. Due to limitations with API Key access, I am currently accessing TMDb through [Hugging Face]([url](https://huggingface.co/datasets/bloc4488/TMDB-all-movies/viewer/default/train?sort[column]=id&sort[direction]=desc)).

For the filters themselves (which are optional), these are currently the options available:

### Genre
Action, Adventure, Animation, Comedy, Crime, Documentary, Drama, Family, Fantasy, History, Horror, Music, Mystery, Romance, Science Fiction, Thriller, TV Movie, War, Western


### Era
Silent Age (1911-1926), Pre-Code Era (1927-1933), Golden Age (1934-1965), New Hollywood (1966-1983), Blockbuster Age (1984-present)


### Rating
Acclaim (8.0 - 10.0), Positive (6.0-8.0), Mixed (4.0-6.0), Negative (2.0-4.0), Terrible (0.0-2.0)


### Runtime
Short Film, An Hour and a Half, Two Hours (ish), Three Hours (ish) and Beyond


### Language -- listed in English alphabetical order
Bahasa melayu, বাংলা, 广州话 / 廣州話, Český, Dansk, Nederlands,  English, Finnish, Français, Deutsch, עִבְרִית, हिन्दी, Italiano, 日本語, 한국어/조선말, 普通话, Norsk, Polski, Português, Pусский, 
Español, svenska, ภาษาไทย, Türkçe

## Ongoing Work
At this point, the back-end is largely set in stone, and it now becomes a question of tuning the UI to best suit my purposes. `tkinter` is slightly limited in this respect, but I still hope to make the user experience as smooth as possible and expand the filter system to enable multi-select.
