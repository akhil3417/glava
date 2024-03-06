from pathlib import Path
from typer import secho
from sgpt.config import cfg
from sgpt.handlers.chat_handler import ChatSession

# Assuming the storage path is where the chat history files are stored
CHAT_CACHE_PATH = Path(cfg.get("CHAT_CACHE_PATH"))
CHAT_CACHE_LENGTH = int(cfg.get("CHAT_CACHE_LENGTH"))
chat_session = ChatSession(CHAT_CACHE_LENGTH, CHAT_CACHE_PATH)


def show_chat_history(chat_id: str) -> None:
    """
    Prints the chat history for the given chat_id.

    :param chat_id: The ID of the chat session.
    """
    chat_history = chat_session.get_messages(chat_id)
    for index, message in enumerate(chat_history):
        color = "magenta" if index % 2 == 0 else "green"
        secho(message, fg=color)
