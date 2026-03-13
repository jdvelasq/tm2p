"""
ExtractAcronyms
===============================================================================


Smoke test:
    >>> from tm2p.ingest.rev import ExtractAcronyms
    >>> acronyms = (
    ...     ExtractAcronyms()
    ...     .where_root_directory("tests/scopus/")
    ...     .run()
    ... )
    >>> len(acronyms)
    96
    >>> "crm" in acronyms
    True
    >>> acronyms["crm"]
    {'customer relationship management'}


"""

from pathlib import Path

import pandas as pd  # type: ignore
from textblob import TextBlob  # type: ignore

from tm2p import Field
from tm2p._intern import ParamsMixin
from tm2p._intern.data_access import load_main_csv_zip
from tm2p._intern.packag_data import load_builtin_mapping

_EXCLUDED_COMMON_WORDS = [
    "classification",
    "computer",
    "consumers",
    "economics",
    "electronic",
    "electronics",
    "irrational",
    "online",
    "personnel",
]

_EXCLUDED_ENUMERATIONS = ["i", "ii", "iii", "iv", "v", "vi", "vii", "viii", "ix", "x"]

TRUNCATION_MARKER = "... "
MAX_VALUE_DISPLAY_LENGTH = 100
MIN_ACRONYM_LENGTH = 2
TRUNCATION_SUFFIX_LENGTH = 96


class ExtractAcronyms(
    ParamsMixin,
):
    """:meta private:"""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.acronyms: dict[str, set[str]] = {}

    # -------------------------------------------------------------------------
    def extract_acronyms_from_keywords_with_parentheses(self):

        df = load_main_csv_zip(
            root_directory=self.params.root_directory,
        )

        for col in [
            Field.AUTHKW_TOK.value,
            Field.IDXKW_TOK.value,
        ]:
            if col not in df.columns:
                continue

            keywords = df[col].dropna().str.split("; ")
            keywords = keywords.explode().str.strip()
            keywords = keywords[
                keywords.str.contains("(", regex=False)
                & keywords.str.contains(")", regex=False)
            ]
            keywords = keywords[~keywords.str.startswith("(")]  # type: ignore

            if not keywords.empty:  # type: ignore

                for _, text in keywords.items():  # type: ignore

                    text = text[:-1]
                    splited_text = text.split(" ( ")
                    if len(splited_text) != 2:
                        continue
                    def_text, acr_text = splited_text
                    if len(acr_text.split()) > 1:
                        continue
                    if len(def_text.split()) == 1:
                        continue
                    if acr_text.isdigit():
                        continue
                    if len(acr_text) < MIN_ACRONYM_LENGTH:
                        continue
                    if acr_text in _EXCLUDED_ENUMERATIONS:
                        continue
                    if acr_text in _EXCLUDED_COMMON_WORDS:
                        continue
                    if acr_text[0] != def_text[0]:
                        continue

                    acr_text = acr_text.lower().strip()
                    def_text = def_text.lower().strip()
                    if acr_text in self.acronyms:
                        self.acronyms[acr_text].add(def_text)
                    else:
                        self.acronyms[acr_text] = {def_text}

    # -------------------------------------------------------------------------
    def extract_acronyms_in_keywords(self):

        dataframe = load_main_csv_zip(root_directory=self.params.root_directory)

        for col in [
            Field.AUTHKW_TOK.value,
            Field.IDXKW_TOK.value,
        ]:
            if col not in dataframe.columns:
                continue

            keywords = dataframe[col].dropna().str.split("; ")
            keywords = keywords.explode().str.strip()
            keywords = keywords.str.replace(r"\([^)]*\)", "", regex=True).str.strip()

            single_words = keywords[keywords.str.split().map(len) == 1]
            single_words = single_words.str.strip().str.lower().drop_duplicates()  # type: ignore

            multi_words = keywords[keywords.str.split().map(len) > 1]
            multi_words = multi_words.str.strip().str.lower().drop_duplicates()  # type: ignore

            if not multi_words.empty and not single_words.empty:

                for _, def_text in multi_words.items():

                    acr_text = "".join([word[0] for word in def_text.split()])
                    if len(acr_text) < MIN_ACRONYM_LENGTH:
                        continue

                    if acr_text in single_words.values:
                        acr_text = acr_text.strip()
                        def_text = def_text.strip()
                        if acr_text in self.acronyms:
                            self.acronyms[acr_text].add(def_text)
                        else:
                            self.acronyms[acr_text] = {def_text}

    # -------------------------------------------------------------------------
    def extract_acronyms_from_abstracts(self):

        abs_col = Field.ABSTR_TOK.value

        dataframe = load_main_csv_zip(
            root_directory=self.params.root_directory,
            usecols=[abs_col],
        ).dropna()

        sentences = (
            dataframe[abs_col]
            .str.replace(r"\)(?!\.)", ") .", regex=True)
            .apply(lambda x: [str(s) for s in TextBlob(x).sentences])  # type: ignore
            .explode()
            .str.strip()
        )

        sentences = sentences[sentences.str.contains("(", regex=False)]
        sentences = sentences[sentences.str.contains(")", regex=False)]
        sentences = sentences.str.replace(r"\)[^)]*$", ")", regex=True)

        extracted_acronyms = sentences.str.extract(r"\(([^)]+)\)")[0]

        builtin_acronyms = load_builtin_mapping("acronyms.json")

        for def_text, acr_text in zip(sentences.values, extracted_acronyms.values):

            if pd.isna(acr_text):
                continue

            if pd.isna(def_text):
                continue

            acr_text = acr_text.lower().strip()
            def_text = def_text.lower().strip()
            def_text = def_text[-90:]

            if def_text == "":
                continue

            if acr_text in _EXCLUDED_ENUMERATIONS:
                continue
            if acr_text in _EXCLUDED_COMMON_WORDS:
                continue
            if acr_text.isdigit():
                continue
            if len(acr_text.split()) > 1:
                continue
            if len(acr_text) < MIN_ACRONYM_LENGTH:
                continue
            if acr_text.isdigit():
                continue

            text = def_text.split("(")[0].strip()
            full_words = text.split()
            words = [w for w in full_words if w != "and"]
            first_letters = "".join(word[0] for word in words)

            if first_letters.endswith(acr_text):

                if "and" in words[-len(acr_text) :]:
                    def_text = full_words[-len(acr_text) + 1 :]
                else:
                    def_text = full_words[-len(acr_text) :]
                def_text = " ".join(def_text)

            elif acr_text[-1] == "s" and first_letters.endswith(acr_text[:-1]):

                if "and" in full_words[-(len(acr_text) - 1) :]:
                    def_text = full_words[-len(acr_text) :]
                else:
                    def_text = full_words[-(len(acr_text) - 1) :]
                def_text = " ".join(def_text)
            elif acr_text in builtin_acronyms:
                for acronym_definition in builtin_acronyms[acr_text]:
                    if acronym_definition in def_text:
                        def_text = acronym_definition
            else:
                pass

            if acr_text in self.acronyms:
                self.acronyms[acr_text].add(def_text)
            else:
                self.acronyms[acr_text] = {def_text}

    # -------------------------------------------------------------------------
    def run(self):

        self.extract_acronyms_from_keywords_with_parentheses()
        self.extract_acronyms_in_keywords()
        self.extract_acronyms_from_abstracts()
        return self.acronyms


if __name__ == "__main__":

    acronyms = ExtractAcronyms().where_root_directory("./").run()

    filepath = Path("./") / "refine" / "word_lists" / "acronyms.txt"

    with open(filepath, "w", encoding="utf-8") as file:
        sorted_acronyms = sorted(acronyms.keys())
        for acronym in sorted_acronyms:
            print(acronym, file=file)
            for definition in sorted(acronyms[acronym]):
                print(f"    {definition}", file=file)
