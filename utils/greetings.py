from datetime import datetime
from rich import print as rich_print


def get_time_of_day():
    hour = datetime.now().hour
    if (hour >= 6) and (hour < 12):
        return "Good morning"
    elif (hour >= 12) and (hour <= 16):
        return "Good afternoon"
    elif (hour >= 16) and (hour < 19):
        return "Good evening"
    else:
        return "Hello"


def greet_user(USER, HOSTNAME):
    time_of_day = get_time_of_day()
    rich_print(
        f"{time_of_day} [bold magenta]{USER}[/bold magenta]. I am [bold magenta]{HOSTNAME}[/bold magenta]. How may I assist you?"
    )
