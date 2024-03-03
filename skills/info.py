import threading

import imdb
import requests
import wikipedia
import wolframalpha
from bs4 import BeautifulSoup as bs
from config import WOLFRAMALPHA_API
from utils.input_output import speak_or_print, take_command


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
    print(f"Searching on Wikipedia for", query)
    results = search_on_wikipedia(query)
    speak_or_print("Here's a quick summary from Wikipedia.\n")
    speak_or_print(results)


def movie_command():
    movies_db = imdb.IMDb()
    speak_or_print("Please tell me the movie name:")
    text = input().lower()
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
        plot = movie_info.get("plot outline", "plot summary not available")
        speak_or_print(
            f"{title} was released in {year} has imdb ratings of {rating}.It has a cast of {actor}. "
            f"The plot summary of movie is {plot}"
        )

        print(
            f"{title} was released in {year} has imdb ratings of {rating}.\n It has a cast of {actor}. \n"
            f"The plot summary of movie is {plot}"
        )


def calculate_command():
    app_id = WOLFRAMALPHA_API
    client = wolframalpha.Client(app_id)
    user_input = input("enter")
    ind = user_input.lower().split().index("calculate")
    text = user_input.split()[ind + 1 :]
    result = client.query(" ".join(text))
    try:
        ans = next(result.results).text
        speak_or_print("The answer is " + ans)
        print("The answer is " + ans)
    except StopIteration:
        speak_or_print("I couldn't find that . Please try again")


def what_is_wolframe(user_input):
    app_id = WOLFRAMALPHA_API
    client = wolframalpha.Client(app_id)
    # user_input=input("Enter:")
    # user_input= await take_command()
    try:
        ind = (
            user_input.lower().index("what is")
            if "what is" in user_input.lower()
            else user_input.lower().index("who is")
            if "who is" in user_input.lower()
            else user_input.lower().index("which is")
            if "which is" in user_input.lower()
            else None
        )

        if ind is not None:
            text = user_input.split()[ind + 2 :]
            res = client.query(" ".join(text))
            ans = next(res.results).text
            speak_or_print(ans)
            # print("The answer is " + ans)
        else:
            speak_or_print("I couldn't find that. Please try again.")
    except StopIteration:
        speak_or_print("I couldn't find that. Please try again.")


def run_wolframe(user_input):
    t = threading.Thread(target=what_is_wolframe, args=(user_input,))
    t.start()
