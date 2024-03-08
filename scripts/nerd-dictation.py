#!/usr/bin/env python

import re

# -----------------------------------------------------------------------------
# Constants

# Commands to use.
START_COMMAND = ("start", "writing")
FINISH_COMMAND = ("stop", "writing")

# Replacements
TEXT_REPLACE_REGEX = (
    ("\\b" "data type" "\\b", "data-type"),
    ("\\b" "copy on write" "\\b", "copy-on-write"),
    ("\\b" "key word" "\\b", "keyword"),
)
TEXT_REPLACE_REGEX = tuple(
    (re.compile(match), replacement) for (match, replacement) in TEXT_REPLACE_REGEX
)
WORD_REPLACE = {
    "i": "I",
    "api": "API",
    "linux": "Linux",
    # It's also possible to ignore words entirely.
    "hmm": "",
    "um": "",
}
WORD_REPLACE_REGEX = (("^i'(.*)", "I'\\1"),)
WORD_REPLACE_REGEX = tuple(
    (re.compile(match), replacement) for (match, replacement) in WORD_REPLACE_REGEX
)
CLOSING_PUNCTUATION = {
    "period": ".",
    "comma": ",",
    "question mark": "?",
    "close quote": '"',
    "slash": "/",
    "dash": "-",
}
OPENING_PUNCTUATION = {
    "open quote": '"',
}

# Global, track when dictation is active.
is_active = False

# -----------------------------------------------------------------------------
# Utility Functions


def match_words_at_index(haystack_words, haystack_index, needle_words):
    """
    Check needle_words is in haystack_words at haystack_index.
    """
    return (
        (needle_words[0] == haystack_words[haystack_index])
        and (haystack_index + len(needle_words) <= len(haystack_words))
        and (
            needle_words[1:]
            == haystack_words[haystack_index + 1 : haystack_index + len(needle_words)]
        )
    )


# -----------------------------------------------------------------------------
# Main Processing Function


def nerd_dictation_process(text):
    global is_active

    words_input = tuple(text.split(" "))
    words = []

    i = 0

    # First check if there is text prior to having begun/ended dictation.
    # The part should always be ignored.
    if is_active:
        while i < len(words_input):
            if match_words_at_index(words_input, i, START_COMMAND):
                i += len(START_COMMAND)
                break
            i += 1
        if i == len(words_input):
            i = 0
        # Else keep the advance of 'i', since it skips text before dictation started.

    while i < len(words_input):
        word = words_input[i]
        if is_active:
            if match_words_at_index(words_input, i, FINISH_COMMAND):
                is_active = False
                i += len(FINISH_COMMAND)
                continue
        else:
            if match_words_at_index(words_input, i, START_COMMAND):
                is_active = True
                i += len(START_COMMAND)
                continue

        if is_active:
            # Apply the text replacement rules
            for match, replacement in TEXT_REPLACE_REGEX:
                word = match.sub(replacement, word)

            # Apply the closing punctuation
            for match, replacement in CLOSING_PUNCTUATION.items():
                word = word.replace(" " + match, replacement)

            # Apply the opening punctuation
            for match, replacement in OPENING_PUNCTUATION.items():
                word = word.replace(match + " ", replacement)

            # Apply the word replacement rules
            word_init = word
            word_test = WORD_REPLACE.get(word)
            if word_test is not None:
                word = word_test
            if word_init == word:
                for match, replacement in WORD_REPLACE_REGEX:
                    word_test = match.sub(replacement, word)
                    if word_test != word:
                        word = word_test
                        break

            words.append(word)
        i += 1

    return " ".join(words)
