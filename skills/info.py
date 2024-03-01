import threading
import urllib.request

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

