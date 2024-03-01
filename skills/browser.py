import re
import shlex
from config import BROWSER, PROFILE, SITES
from utils.input_output import speak_or_print, start_process,take_command
DEFAULT_BROWSER = shlex.split(BROWSER) + shlex.split(PROFILE)  # This will also be a list of arguments
