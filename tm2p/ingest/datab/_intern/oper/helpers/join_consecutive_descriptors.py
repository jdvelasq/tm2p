import re

from tm2p._intern.packag_data.word_lists.load_builtin_word_list import (
    load_builtin_word_list,
)

PATTERN_1 = re.compile(r"[A-Z][A-Z_]+ [A-Z][A-Z_]+")
PATTERN_2 = re.compile(r"' ([A-Z][A-Z_]+) ' ([A-Z][A-Z_]+)\b")
PATTERN_3 = re.compile(r"\b([A-Z][A-Z_]+) \( ([A-Z][A-Z_]+) \) ([A-Z][A-Z_]+)\b")

STOPWORDS: set[str] = set(
    phrase.strip().lower()
    for phrase in load_builtin_word_list("stopwords.txt")
    if phrase.strip()
)


def join_consecutive_descriptors(text):

    matches = re.findall(PATTERN_1, text)
    if len(matches) > 0:
        for match in matches:
            word = match.split(" ")[1]
            word = word.split("_")[0]
            if word.lower() in STOPWORDS:
                continue
            regex = re.compile(r"\b" + re.escape(match) + r"\b")
            text = re.sub(regex, lambda z: z.group().upper().replace(" ", "_"), text)

    matches = re.findall(PATTERN_2, text)
    if len(matches) > 0:
        for match in matches:

            full_match = f"' {match[0]} ' {match[1]}"
            replacement = f"{match[0]}_{match[1]}"
            regex = re.compile(re.escape(full_match))
            text = re.sub(regex, replacement, text)

    matches = re.findall(PATTERN_3, text)
    if len(matches) > 0:
        for match in matches:

            full_match = f"{match[0]} ( {match[1]} ) {match[2]}"
            replacement = f"{match[0]}_{match[2]}"
            regex = re.compile(r"\b" + re.escape(full_match) + r"\b")
            text = re.sub(regex, replacement, text)

    return text
