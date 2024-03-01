import threading
import urllib.request

import imdb
import requests
import wikipedia
import wolframalpha
from bs4 import BeautifulSoup as bs
from config import COUNTRY, NEWS_API_KEY
from config import NEWS_HEADLINES_NUMBER as headlines
from utils.input_output import speak_or_print, take_command

def google_news_command(): #TODO 2024-02-24: today news 10 ,num =headlines
    try:
        news_url = "https://news.google.com/news/rss"
        client = urllib.request.urlopen(news_url)
        xml_page = client.read()
        client.close()
        soup = bs(xml_page, "xml")
        news_list = soup.findAll("item")
        response = ""
        speak_or_print(f"Here are the top {headlines} headlines:")
        for idx, news in enumerate(news_list[:headlines], start=1):
            data = f"\n{idx}. {news.title.text}"
            speak_or_print(data)
            response += data
    except Exception as e:
            speak_or_print("Error with the execution of skill with message {0}".format(e))
            speak_or_print("I can't find about daily news..")


def get_news(user_input):
    news = []
    url = "https://newsapi.org/v2/top-headlines"
    categories = ["business", "entertainment", "general", "health", "sciences", "sports", "technology"]
    sources = ["bbc-news", "the-times-of-india"]
    querystring = {"country": COUNTRY,"categories":"sciences"}
#     result = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&sources=bbc-news&category=general&apiKey" f"={NEWS_API_KEY}").json()

    if any(category in user_input for category in categories):
        querystring = {"country": COUNTRY, "categories": next(category for category in categories if category in user_input)}#, "pageSize": "50"
    elif any(source in user_input for source in sources):
        querystring = {"sources": next(source for source in sources if source in user_input)}

    headers = {
        'x-api-key': NEWS_API_KEY,
        # 'x-rapidapi-host': "newsapi-org-headlines-live.p.rapidapi.com"
    }
    # response = requests.request("GET", url, headers=headers, params=querystring)

    print(querystring)
    session = requests.Session()
    response = session.get(url, headers=headers, params=querystring)
    response.raise_for_status()
    result = response.json()
    # Check if 'articles' key is present in the response
    if 'articles' in result:
        articles = result["articles"]
        for article in articles:
            news.append({
                'text': article["title"],
                'description': article["description"]
            })
    else:
        print("Response does not contain 'articles' key")
    return news[:6]


def read_news(user_input):
    cmd = lambda text: print(text)  # Default command
    if "google" in user_input:
        google_news_command()
        if "speak" in user_input:
            google_news_command(VOICE=True)
        return
    articles = get_news(user_input)
    if "speak" in user_input:
        cmd=speak_or_print
        for article in articles:
            print(article["text"])
            cmd((article["text"]),VOICE=True)
            if "desc" in user_input:
                print(article["description"])
                cmd(article["description"],VOICE=True)
        return
    else:
      for article in articles:
          print(article["text"])
          if "desc" in user_input:
              print(article["description"])
          if cmd != speak_or_print :
              print("---------------------------------------------------------------------------------------")


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


def calculate_command():
    app_id = "KTKV36-2LRW2LELV8"
    client = wolframalpha.Client(app_id)
    user_input=input("enter")
    ind = user_input.lower().split().index("calculate")
    text = user_input.split()[ind + 1:]
    result = client.query(" ".join(text))
    try:
        ans = next(result.results).text
        speak_or_print("The answer is " + ans)
        print("The answer is " + ans)
    except StopIteration:
        speak_or_print("I couldn't find that . Please try again")


def what_is_wolframe(user_input):
    app_id = "KTKV36-2LRW2LELV8"
    client = wolframalpha.Client(app_id)
    # user_input=input("Enter:")
    # user_input= await take_command()
    try:
        ind = user_input.lower().index('what is') if 'what is' in user_input.lower() else \
            user_input.lower().index('who is') if 'who is' in user_input.lower() else \
                user_input.lower().index('which is') if 'which is' in user_input.lower() else None

        if ind is not None:
            text = user_input.split()[ind + 2:]
            res = client.query(" ".join(text))
            ans = next(res.results).text
            speak_or_print("The answer is " + ans)
            print("The answer is " + ans)
        else:
            speak_or_print("I couldn't find that. Please try again.")
    except StopIteration:
        speak_or_print("I couldn't find that. Please try again.")


def run_wolframe(user_input):
    t = threading.Thread(target=what_is_wolframe, args=(user_input,))
    t.start()
