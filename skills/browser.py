import re
import shlex
from config import BROWSER, PROFILE, SITES
from utils.input_output import speak_or_print, start_process,take_command


DEFAULT_BROWSER = shlex.split(BROWSER) + shlex.split(PROFILE)  # This will also be a list of arguments

def open_browser_command():
    speak_or_print(f"Opening browser",{BROWSER})
    start_process(DEFAULT_BROWSER)  # Unpack the list of arguments

def get_site_url(site_key, user_input):
    return SITES.get(site_key).format(user_input=user_input)

def open_in_browser(DEFAULT_BROWSER, url):
    command = DEFAULT_BROWSER + [url]
    start_process(command)

def web_search(user_input):
    for site_key, site_url in SITES.items():
        if site_key in user_input:
            # user_input = re.sub(rf'{site_key}|new tab|search for', '', user_input).strip()
            query_match = re.search(r'for\s(.*?)\s*on', user_input) #  NOTE : matches the text between for and on
            if query_match:
                            user_input = query_match.group(1)
            url = get_site_url(site_key, user_input)
            open_in_browser(DEFAULT_BROWSER, url)
            return
    # If no match is found, open the search in the default browser
    url = get_site_url('def_search_engine', user_input)
    open_in_browser(DEFAULT_BROWSER, url)

def open_websites(user_input):
    print(user_input)
    # Extract URL from user_input
    url = re.findall(r'(?<=)\S+', user_input)
    if url:
        url = url[0]
        # If the URL doesn't start with 'http' or 'https', add 'https://' to the beginning
        if not re.match('(?:http|https)://', url):
            url = 'https://' + url
        # Open URL in default web browser
        print(f"Opening {url}")
        print(DEFAULT_BROWSER)
        open_in_browser(DEFAULT_BROWSER, url)

async def query_web_command_async():
    speak_or_print("What do you want to search for?")
    query= await take_command()
    web_search(query)

