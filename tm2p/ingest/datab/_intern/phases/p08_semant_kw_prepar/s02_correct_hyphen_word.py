import json
import os
from pathlib import Path

import pandas as pd  # type: ignore
from openai import APIError, OpenAI
from tqdm import tqdm  # type: ignore

from tm2p import Field
from tm2p._intern.data_access import load_main_csv_zip, save_main_csv_zip
from tm2p._intern.packag_data import (
    add_new_words_to_builtin_word_list,
    load_builtin_word_list,
)

SYSTEM_PROMPT = """
INSTRUCTION:
You will be provided with two variations of the same word: one in hyphenated form and the other in non-hyphenated form.


TASK:
1. Analyze the two forms and determine which is correct in scientific or technical English usage.
2. Respond with "yes" if:
    - The hyphenated form is the only form correct.
    - The word is not standard English.
    - Both forms (hyphenated and non-hyphenated) are correct.
    - Neither form is correct.
3. Respond "no" if:
    - The non-hyphenated form is the only form correct.
    - The correct form is different from both provided forms.

    
OUTPUT FORMAT (STRICT — JSON ONLY):
The output MUST be a JSON object with the following structure:

{{
    "answer": "yes" or "no",
}}

Any output different of this must be considered invalid.

"""

USER_PROMPT = """

WORDS:
- Hyphenated: "{}"
- Non-hyphenated: "{}"

"""


def s02_correct_hyphen_word(root_directory: str) -> int:

    df = load_main_csv_zip(root_directory)
    if Field.IDXKW_RAW.value not in df.columns:
        return 0
    if Field.AUTHKW_RAW.value not in df.columns:
        return 0

    words = _extract_hyphenated_words(df)
    unknown_words = _extract_unknown_words(words, root_directory)
    new_valid_words, new_invalid_words = _classify_unknown_words(unknown_words)

    _report_new_words(
        new_valid_words=new_valid_words,
        new_invalid_words=new_invalid_words,
        root_directory=root_directory,
    )

    known_valid_words = _get_valid_words(root_directory)
    known_invalid_words = _get_invalid_words(root_directory)
    df = _replace(
        df,
        new_valid_words | known_valid_words,
        new_invalid_words | known_invalid_words,
    )

    save_main_csv_zip(df, root_directory)

    return max(
        int(df[Field.AUTHKW_TOK.value].notna().sum()),
        int(df[Field.IDXKW_TOK.value].notna().sum()),
    )


def _get_valid_words(root_directory: str) -> set:

    words: set[str] = set()

    my_keywords_path = Path(root_directory) / "refine" / "word_lists"

    report_file = my_keywords_path / "valid_hyphenated_words.txt"
    if report_file.exists():
        with open(report_file, "r", encoding="utf-8") as f:
            for line in f:
                words.add(line.strip())

    return words


def _get_invalid_words(root_directory: str) -> set:

    words: set[str] = set()

    my_keywords_path = Path(root_directory) / "refine" / "word_lists"

    report_file = my_keywords_path / "invalid_hyphenated_words.txt"
    if report_file.exists():
        with open(report_file, "r", encoding="utf-8") as f:
            for line in f:
                words.add(line.strip())

    return words


def _extract_hyphenated_words(dataframe: pd.DataFrame) -> set:

    hypenated_words: set[str] = set()
    for col in [
        Field.AUTHKW_TOK.value,
        Field.IDXKW_TOK.value,
    ]:

        series = dataframe[col].dropna()
        series = series.str.lower()
        keywords = series.str.split("; ").explode()
        keywords = keywords.str.strip()
        words = keywords.str.split(" ").explode()
        words = words.str.strip()
        words = words[~words.str.startswith("-")]
        words = words[~words.str.endswith("-")]
        words = words[words.str.contains("-")]
        words = words[~words.str.contains("--")]
        words = words[words.map(lambda x: x != "-")]
        words_set = set(words.tolist())
        hypenated_words.update(words_set)

    return hypenated_words


def _extract_unknown_words(words: set, root_directory: str) -> set:

    invalid_hyphenated_words = load_builtin_word_list("invalid_hyphenated_words.txt")
    valid_hyphenated_words = load_builtin_word_list("valid_hyphenated_words.txt")

    known_words = set(valid_hyphenated_words) | set(invalid_hyphenated_words)

    known_valid_words = _get_valid_words(root_directory)
    known_invalid_words = _get_invalid_words(root_directory)
    known_words.update(known_valid_words)
    known_words.update(known_invalid_words)

    words = set(words)
    unknown_words = words - known_words

    return unknown_words


def _classify_unknown_words(unknown_words: set) -> tuple[set, set]:

    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY environment variable is not set.")

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    valid_words: set[str] = set()
    invalid_words: set[str] = set()

    if not unknown_words:
        return valid_words, invalid_words

    for word in tqdm(
        unknown_words,
        total=len(unknown_words),
        bar_format="  {percentage:3.2f}% {bar} | {n_fmt}/{total_fmt} [{rate_fmt}] |",
        ascii=" :",
        ncols=73,
    ):

        if "-" not in word:
            raise ValueError(f"Word '{word}' does not contain a hyphen.")

        parts = word.split("-")
        if parts[0] == parts[1]:
            invalid_words.add(word)
            continue

        query = USER_PROMPT.format(
            word.lower().replace("_", "-"), word.lower().replace("_", "")
        )

        try:

            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {
                        "role": "system",  # type: ignore
                        "content": SYSTEM_PROMPT,
                        "cache_control": {"type": "ephemeral"},
                    },
                    {
                        "role": "user",
                        "content": query,
                    },
                ],
                temperature=0,
                response_format={"type": "json_object"},
            )

            answer = response.choices[0].message.content
            if answer is None:
                print(f"Error: Empty response for word '{word}'")
                continue
            answer = json.loads(answer)
            answer = answer["answer"]
            answer = answer.lower()

            if answer == "no":
                invalid_words.add(word)
            else:
                valid_words.add(word)

        except (APIError, json.JSONDecodeError, KeyError) as e:
            print(f"Error processing {e}")

    return valid_words, invalid_words


def _report_new_words(
    new_valid_words: set,
    new_invalid_words: set,
    root_directory: str,
) -> None:

    my_keywords_path = Path(root_directory) / "refine" / "word_lists"

    if new_valid_words:

        report_file = my_keywords_path / "valid_hyphenated_words.txt"

        with open(report_file, "w", encoding="utf-8") as f:
            for word in sorted(new_valid_words):
                f.write(f"{word}\n")

        add_new_words_to_builtin_word_list(
            "valid_hyphenated_words.txt", list(new_valid_words)
        )

    if new_invalid_words:

        report_file = my_keywords_path / "invalid_hyphenated_words.txt"

        with open(report_file, "w", encoding="utf-8") as f:
            for word in sorted(new_invalid_words):
                f.write(f"{word}\n")

        add_new_words_to_builtin_word_list(
            "invalid_hyphenated_words.txt", list(new_invalid_words)
        )


def _replace(
    dataframe: pd.DataFrame,
    new_valid_words: set,
    new_invalid_words: set,
) -> pd.DataFrame:

    invalid_hyphenated_words = load_builtin_word_list("invalid_hyphenated_words.txt")
    valid_hyphenated_words = load_builtin_word_list("valid_hyphenated_words.txt")

    for col in [
        Field.AUTHKW_TOK.value,
        Field.IDXKW_TOK.value,
    ]:
        dataframe[col] = dataframe[col].str.lower()

        for word in invalid_hyphenated_words | new_invalid_words:
            dataframe[col] = dataframe[col].str.replace(
                word, word.replace("-", ""), regex=False
            )

        for word in valid_hyphenated_words | new_valid_words:
            dataframe[col] = dataframe[col].str.replace(
                word.replace("-", ""), word, regex=False
            )

    return dataframe
