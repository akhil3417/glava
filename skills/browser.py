import re
import shlex
from config import BROWSER, PROFILE, SITES
from utils.input_output import (
    speak_or_print,
    start_process,
    take_command,
)


# This will also be a list of arguments
DEFAULT_BROWSER = shlex.split(BROWSER) + shlex.split(PROFILE)


def open_browser_command():
    """
    Function to open the browser and start a new process.
    """
    speak_or_print(f"Opening browser", {BROWSER})
    start_process(DEFAULT_BROWSER)  # Unpack the list of arguments


def get_site_url(site_key, user_input):
    """
    Retrieve the site URL based on the site key and user input.

    Args:
        site_key (str): The key of the site in the SITES dictionary.
        user_input (str): The user input to be formatted into the site URL.

    Returns:
        str: The formatted site URL.
    """
    return SITES.get(site_key).format(user_input=user_input)


def open_in_browser(DEFAULT_BROWSER, url):
    """
    Function to open the specified URL in the default web browser.

    Args:
        DEFAULT_BROWSER (str): The default web browser to use.
        url (str): The URL to open.

    Returns:
        None
    """
    command = DEFAULT_BROWSER + [url]
    start_process(command)


def web_search(user_input):
    """
    Perform a web search based on the user input by checking the SITES dictionary for matching site keys. If a match is found, open the corresponding site URL in the default browser. If no match is found, open the search in the default browser using the default search engine URL.

    Parameters:
    - user_input: a string representing the user's input for the search

    Return:
    - None
    """
    for site_key in SITES.keys():
        if site_key in user_input:
            query_match = re.search(
                r"for\s(.*?)\s*on", user_input
            )  #  NOTE : matches the text between for and on
            if query_match:
                user_input = query_match.group(1)
            url = get_site_url(site_key, user_input)
            open_in_browser(DEFAULT_BROWSER, url)
            return
    # If no match is found, open the search in the default browser
    url = get_site_url("def_search_engine", user_input)
    open_in_browser(DEFAULT_BROWSER, url)


def open_websites(user_input):
    """
    A function to open a website URL provided by the user in the default web browser.
    Parameters:
        user_input (str): The input string containing the URL.
    Return:
        None
    """
    print(user_input)
    # Extract URL from user_input
    url = re.findall(r"(?<=)\S+", user_input)
    if url:
        url = url[0]
        # If the URL doesn't start with 'http' or 'https', add 'https://' to the beginning
        if not re.match("(?:http|https)://", url):
            url = "https://" + url
        # Open URL in default web browser
        print(f"Opening {url}")
        print(DEFAULT_BROWSER)
        open_in_browser(DEFAULT_BROWSER, url)


async def query_web_command_async():
    """
    Asynchronous function to perform a web query command.
    This function prompts the user for a search query, retrieves the query input, and performs a web search.
    """
    speak_or_print("What do you want to search for?")
    query = await take_command()
    web_search(query)
