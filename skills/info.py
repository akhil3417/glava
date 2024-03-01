import threading
import urllib.request

import imdb
import wikipedia
def search_on_wikipedia(query):
    try:
        results = wikipedia.summary(query, sentences=3)
        return results
    except wikipedia.exceptions.PageError:
        return "No page matches the query."
    except wikipedia.exceptions.DisambiguationError:
        return "There are multiple pages matching the query. Please be more specific."

async def wikipedia_command_async():
    query = await take_command()  # Await take_command() here
    print(f"Searching on Wikipedia for",query)
    results = search_on_wikipedia(query)
    speak_or_print("Here's a quick summary from Wikipedia.\n")
    speak_or_print(results)


def movie_command():
    movies_db = imdb.IMDb()
    speak_or_print("Please tell me the movie name:")
    text=input().lower()
    movies = movies_db.search_movie(text)
    speak_or_print("searching for" + text)
    speak_or_print("I found these")
    for movie in movies:
        title = movie["title"]
        year = movie["year"]
        speak_or_print(f"{title}-{year}")
        info = movie.getID()
        movie_info = movies_db.get_movie(info)
        rating = movie_info["rating"]
        cast = movie_info["cast"]
        actor = cast[0:5]
        plot = movie_info.get('plot outline', 'plot summary not available')
        speak_or_print(f"{title} was released in {year} has imdb ratings of {rating}.It has a cast of {actor}. "
              f"The plot summary of movie is {plot}")

        print(f"{title} was released in {year} has imdb ratings of {rating}.\n It has a cast of {actor}. \n"
              f"The plot summary of movie is {plot}")


