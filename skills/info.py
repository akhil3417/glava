import threading

import imdb
import wikipedia
import wolframalpha
from config import WOLFRAMALPHA_API, VOICE
from utils.input_output import speak_or_print, take_command


def search_on_wikipedia(query):
    """
    Perform a search on Wikipedia using the given query and return a summary of the search results.
    :param query: The search query for the Wikipedia search.
    :return: A summary of the search results.
    """
    try:
        results = wikipedia.summary(query, sentences=3)
        return results
    except wikipedia.exceptions.PageError:
        return "No page matches the query."
    except wikipedia.exceptions.DisambiguationError:
        return "There are multiple pages matching the query. Please be more specific."


async def wikipedia_command_async():
    """
    Asynchronous function to perform a Wikipedia search based on user input.
    """
    query = await take_command()  # Await take_command() here
    print(f"Searching on Wikipedia for", query)
    results = search_on_wikipedia(query).replace('"', "")
    speak_or_print("Heres a quick summary from Wikipedia.\n")
    print(results)
    speak_or_print(results)


def movie_command():
    """
    A function to search for a movie in the IMDb database, retrieve its information, and present information using text ,tts to the user in a well formatted way.
    """
    movies_db = imdb.IMDb()
    speak_or_print("Please tell me the movie name:")
    text = input().lower()
    movies = movies_db.search_movie(text)
    speak_or_print("searching for " + text)
    for movie in movies:
        title = movie["title"].replace('"', "").replace("'", "")
        year = movie["year"]
        info = movie.movieID
        movie_info = movies_db.get_movie(info)
        rating = movie_info["rating"]
        cast = movie_info["cast"]
        actor = [str(actor) for actor in cast[:5]]
        plot = movie_info.get("plot outline", "Plot summary not available")
        plot = plot.replace('"', "").replace("'", "")
        details = f"{title} was released in {year} and has an IMDB rating of {rating}. It stars {', '.join(actor)}. The plot summary of the movie is {plot}"
        if VOICE:
            print(details)
            speak_or_print(details)
            break
        else:
            print(details)
            break


def calculate_wolframe(user_input):
    """
    Calculate the result of the user input using the Wolfram Alpha API.

    Parameters:
    user_input (str): The input provided by the user.

    Returns:
    None
    """
    app_id = WOLFRAMALPHA_API
    client = wolframalpha.Client(app_id)
    result = client.query(user_input)
    try:
        ans = next(result.results).text
        print("The answer is " + ans)
        speak_or_print("The answer is " + ans)
    except StopIteration:
        speak_or_print("I couldnt find that. Please try again")


def what_is_wolframe(user_input):
    """
    Function to query the WolframAlpha API with a user input and retrieve the answer.
    Parameters:
        user_input (str): The input provided by the user.
    Return:
        None
    """
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
            print(ans)
        else:
            speak_or_print("I couldnt find that. Please try again.")
    except StopIteration:
        speak_or_print("I couldnt find that. Please try again.")


def run_wolframe(user_input):
    """
    Run the Wolframe with the given user input in a separate thread.

    :param user_input: the input for the Wolframe
    """
    t = threading.Thread(target=what_is_wolframe, args=(user_input,))
    t.start()
