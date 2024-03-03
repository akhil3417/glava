import urllib.request

import requests
from bs4 import BeautifulSoup as bs
from config import COUNTRY, NEWS_API_KEY
from config import NEWS_HEADLINES_NUMBER as headlines
from utils.input_output import send_notification, speak_or_print


def google_news_command(VOICE, headlines=10):
    try:
        news_url = "https://news.google.com/news/rss"
        client = urllib.request.urlopen(news_url)
        xml_page = client.read()
        client.close()
        soup = bs(xml_page, "xml")
        news_list = soup.findAll("item")[:headlines]
        response = ""
        speak_or_print(f"Here are the top {headlines} headlines:", VOICE)
        headlines = []
        for idx, news in enumerate(news_list, start=1):
            data = f"\n{idx}. {news.title.text}"
            data = data.replace('"', "")
            response += data
            headlines.append(data)
        if VOICE:
            for headline in headlines:
                print(headline)
                speak_or_print(headline, VOICE=VOICE)
        else:
            print(response)
    except Exception as e:
        print("Error with the execution of skill with message {0}".format(e))
        speak_or_print("I can't find about daily news..", VOICE)


def get_news(user_input):
    news = []
    url = "https://newsapi.org/v2/top-headlines"
    categories = [
        "business",
        "entertainment",
        "general",
        "health",
        "sciences",
        "sports",
        "technology",
    ]
    sources = ["bbc-news", "the-times-of-india"]
    querystring = {"country": COUNTRY, "categories": "sciences"}
    #     result = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&sources=bbc-news&category=general&apiKey" f"={NEWS_API_KEY}").json()

    if any(category in user_input for category in categories):
        querystring = {
            "country": COUNTRY,
            "categories": next(
                category for category in categories if category in user_input
            ),
        }  # , "pageSize": "50"
    elif any(source in user_input for source in sources):
        querystring = {
            "sources": next(source for source in sources if source in user_input)
        }

    headers = {
        "x-api-key": NEWS_API_KEY,
        # 'x-rapidapi-host': "newsapi-org-headlines-live.p.rapidapi.com"
    }
    # response = requests.request("GET", url, headers=headers, params=querystring)

    print(querystring)
    session = requests.Session()
    response = session.get(url, headers=headers, params=querystring)
    response.raise_for_status()
    result = response.json()
    # Check if 'articles' key is present in the response
    if "articles" in result:
        articles = result["articles"]
        for article in articles:
            news.append(
                {"text": article["title"], "description": article["description"]}
            )
    else:
        print("Response does not contain 'articles' key")
    return news[:6]


def read_news(user_input):
    cmd = lambda text: print(text)  # Default command
    if "google" in user_input:
        if "speak" in user_input:
            google_news_command(VOICE=True)
        else:
            google_news_command(VOICE=None)
        return

    articles = get_news(user_input)
    if "speak" in user_input:
        cmd = speak_or_print
        for article in articles:
            print(article["text"])
            send_notification("News", article["text"])
            cmd((article["text"]), VOICE=True)
            if "desc" in user_input:
                print(article["description"])
                send_notification("News", article["description"])
                cmd(article["description"], VOICE=True)
        return
    else:
        for article in articles:
            print(article["text"])
            if "desc" in user_input:
                print(article["description"])
            if cmd != speak_or_print:
                print(
                    "---------------------------------------------------------------------------------------"
                )
