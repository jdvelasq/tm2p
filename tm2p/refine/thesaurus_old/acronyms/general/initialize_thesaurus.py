"""
Initialize Thesaurus
===============================================================================


Smoke tests:
    >>> # Create thesaurus
    >>> from tm2p.refine.thesaurus_old.acronyms import InitializeThesaurus
    >>> (
    ...     InitializeThesaurus()
    ...     .where_root_directory("tests/scopus/")
    ...     .run()
    ... )

    >>> from tm2p.refine.thesaurus_old.acronyms import PrintHeader
    >>> (
    ...     PrintHeader()
    ...     .where_root_directory("tests/scopus/")
    ...     .using_colored_output(False)
    ...     .run()
    ... )
    DEMATEL
      ... CRITERIA is constructed and both the DECISION_MAKING_TRIAL_AND_EVALUA...
    E_FINANCE
      ELECTRONIC_FINANCE
    E_PAYMENT
      ELECTRONIC_PAYMENT
    EPAM
      we propose A_RESEARCH_MODEL using AN_EXTENDED_POST_ACCEPTANCE_MODEL ( EPAM )
    FINTECH
      FINANCIAL_TECHNOLOGY
    IOT
      INTERNET_OF_THING; INTERNET_OF_THINGS
    ISED
      THE_DIGITAL_REVOLUTION adds NEW_LAYERS to THE_MATERIAL_CULTURES of financ...
    MCDM
      MULTI_CRITERIA_DECISION_MAKING; ... _INNOVATION_THEORY , we propose A_NOV...
    <BLANKLINE>


"""

import sys

import pandas as pd  # type: ignore
from nltk.corpus import words  # type: ignore
from textblob import TextBlob  # type: ignore

from tm2p._intern import ParamsMixin
from tm2p.refine.thesaurus_old._intern import (
    ThesaurusMixin,
    internal__get_system_thesaurus_file_path,
    internal__load_thesaurus_as_mapping,
)

EXCLUDED_COMMON_WORDS = [
    "CLASSIFICATION",
    "COMPUTER",
    "ECONOMICS",
    "ELECTRONICS",
    "ELECTRONIC",
    "IRRATIONAL",
    "ONLINE",
    "PERSONNEL",
]

EXCLUDED_ENUMERATIONS = ["I", "II", "III", "IV", "V", "1", "2", "3", "4", "5"]

TRUNCATION_MARKER = "... "
MAX_VALUE_DISPLAY_LENGTH = 100
MIN_ACRONYM_LENGTH = 1
TRUNCATION_SUFFIX_LENGTH = 96


class InitializeThesaurus(
    ParamsMixin,
    ThesaurusMixin,
):
    """:meta private:"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Initialize attributes to avoid defining them outside __init__
        self.words = []

    #
    # NOTIFICATIONS:
    # -------------------------------------------------------------------------
    def internal__notify_process_start(self):

        if not self.params.quiet:

            sys.stderr.write("INFO: Initializing thesaurus...\n")
            sys.stderr.flush()

    # -------------------------------------------------------------------------
    def internal__notify_process_end(self):

        if not self.params.quiet:

            sys.stderr.write(f"  {len(self.data_frame)} acronyms found\n")
            sys.stderr.write("  Initialization process completed successfully\n")
            sys.stderr.flush()

    #
    # ALGORITHM:
    # -------------------------------------------------------------------------
    def internal__create_valid_words(self):

        data_frame = self.data_frame.copy()
        data_frame = data_frame[["value"]]

        data_frame["value"] = data_frame["value"].str.split("_")
        data_frame = data_frame.explode("value")
        data_frame["value"] = data_frame["value"].str.strip()

        data_frame["value"] = data_frame["value"].str.split(" ")
        data_frame = data_frame.explode("value")
        data_frame["value"] = data_frame["value"].str.strip()

        data_frame["value"] = data_frame["value"].map(
            lambda x: x[1:-1] if x.startswith("(") and x.endswith(")") else x
        )
        data_frame["value"] = data_frame["value"].str.strip()

        data_frame = data_frame[data_frame["value"].str.len() > 1]

        self.words = data_frame["value"].drop_duplicates().tolist()

    # -------------------------------------------------------------------------
    def internal__extract_acronyms_from_definitions(self):

        data_frame = self.data_frame.copy()

        data_frame = data_frame.loc[data_frame.value.str.contains("(", regex=False), :]
        data_frame = data_frame.loc[data_frame.value.str.endswith(")"), :]
        data_frame = data_frame[["value"]].drop_duplicates()
        data_frame["value"] = data_frame["value"].str[:-1]
        data_frame["value"] = data_frame["value"].str.split(" (", regex=False)

        data_frame = data_frame[data_frame.value.map(len) == 2]
        data_frame["key"] = data_frame.value.map(lambda x: x[1])
        data_frame["value"] = data_frame.value.map(lambda x: x[0])
        data_frame = data_frame[data_frame.key.str.len() < data_frame.value.str.len()]

        self.data_frame = data_frame

    # -------------------------------------------------------------------------
    def internal__extract_acronyms_from_abstracts(self):

        records = self.filtered_records[["abstract"]].dropna()

        # extract phrases
        records["abstract"] = records.abstract.map(
            lambda x: [str(s) for s in TextBlob(x).sentences]
        )
        # records["abstract"] = records.abstract.map(
        #     lambda x: [t for s in x for t in s.split(",")]
        # )
        records = records.explode("abstract")
        records["abstract"] = records.abstract.str.strip()

        # select abstracts with parentheses
        records = records[records.abstract.str.contains("(", regex=False)]
        records = records[records.abstract.str.contains(")", regex=False)]

        # extract acronyms
        records["key"] = records.abstract.str.extract(r"\(([^)]+)\)")
        records["key"] = records.key.str.upper().str.strip()
        records["value"] = records.abstract.str.replace(r"\([^)]+\)", "")
        records = records[["key", "value"]].drop_duplicates()
        records = records.dropna(subset=["key"])

        # remove text from the right of the abbreviation
        records = records.reset_index(drop=True)
        for index, row in records.iterrows():
            records.loc[index, "value"] = row.value.split("( " + row.key + " )")[0]
            records.loc[index, "value"] = row.value.split(
                "( " + row.key.lower() + " )"
            )[0]
            abbr = "( " + row.key.upper() + " )"
            records.loc[index, "value"] += abbr
            if len(records.loc[index, "value"]) > MAX_VALUE_DISPLAY_LENGTH:
                records.loc[index, "value"] = (
                    TRUNCATION_MARKER
                    + records.loc[index, "value"][-TRUNCATION_SUFFIX_LENGTH:]
                )

        # remove enumerations
        records = records[
            records.key.map(
                lambda x: x not in EXCLUDED_ENUMERATIONS, na_action="ignore"
            )
        ]

        records = records[records.key.map(lambda x: "," not in x, na_action="ignore")]
        records = records[records.key.map(lambda x: " " not in x, na_action="ignore")]
        records = records[records.key.map(lambda x: x != "_S_", na_action="ignore")]

        records = records[
            records.key.map(
                lambda x: not (
                    x.startswith("_") and x[1:5].isdigit() and x.endswith("_")
                ),
                na_action="ignore",
            )
        ]

        # remove acronyms of length 1
        records = records[records.key.str.len() > MIN_ACRONYM_LENGTH]

        # remove enumerations already listed in the keywords
        existent_acronyms = self.data_frame.key.drop_duplicates().tolist()
        records = records[records.key.map(lambda x: x not in existent_acronyms)]

        # remove acronyms that are only digits
        records = records[
            records.key.map(lambda x: not x.isdigit(), na_action="ignore")
        ]

        # validate acronyms
        records = records[
            records.key.map(lambda x: x in self.words, na_action="ignore")
        ]

        # concat data frames
        self.data_frame = pd.concat([self.data_frame, records], ignore_index=True)

    # -------------------------------------------------------------------------
    def internal__filter_common_word_acronyms(self):

        for abbr in EXCLUDED_COMMON_WORDS:
            self.data_frame = self.data_frame[self.data_frame.key != abbr]

    # -------------------------------------------------------------------------
    def internal__add_known_acronyms(self):

        # Load known acronyms
        file_path = internal__get_system_thesaurus_file_path("acronyms/common.the.txt")
        common_abbrvs = internal__load_thesaurus_as_mapping(file_path)

        # Load raw descriptors from records
        raw_descriptors = self.filtered_records[self.params.source_field].dropna()
        raw_descriptors = raw_descriptors.str.split("; ")
        raw_descriptors = raw_descriptors.explode()
        raw_descriptors = raw_descriptors.str.strip()
        raw_descriptors = raw_descriptors.drop_duplicates().tolist()

        # Adds definitions from raw descriptors
        for abbr, meaning in common_abbrvs.items():

            process = False

            if abbr in self.data_frame.key.tolist():
                process = True

            if abbr in raw_descriptors:
                process = True

            if any([x.startswith(abbr + "_") for x in raw_descriptors]):
                process = True

            if any([x.endswith("_" + abbr) for x in raw_descriptors]):
                process = True

            if any([("_" + abbr + "_") in x for x in raw_descriptors]):
                process = True

            if process:
                new_frame = pd.DataFrame({"value": [meaning[0]], "key": [abbr]})
                self.data_frame = pd.concat(
                    [self.data_frame, new_frame], ignore_index=True
                )

    # -------------------------------------------------------------------------
    def internal__prepare_fingerprints(self):
        self.data_frame["key"] = self.data_frame["key"].str.strip()
        self.data_frame = self.data_frame[self.data_frame.key != ""]
        self.data_frame["fingerprint"] = self.data_frame.key.copy()

    # -------------------------------------------------------------------------
    def internal__sort_mapping_values(self):
        self.data_frame["value"] = self.data_frame["value"].str.split("; ")
        self.data_frame["value"] = self.data_frame["value"].map(
            lambda x: sorted(x, key=len)
        )
        self.data_frame["value"] = self.data_frame["value"].str.join("; ")

    # -------------------------------------------------------------------------
    def internal__validate_keys(self):
        english_words = set(words.words())
        self.data_frame = self.data_frame[
            self.data_frame.key.map(
                lambda x: x.lower() not in english_words, na_action="ignore"
            )
        ]

    # -------------------------------------------------------------------------
    def run(self):

        self.params.source_field = "raw_descriptors"
        self.params.thesaurus_file = "acronyms.the.txt"

        self._build_user_thesaurus_path()
        self.internal__notify_process_start()
        self.internal__load_filtered_records()
        self.internal__create_thesaurus_data_frame_from_field()

        self.internal__create_valid_words()

        self.internal__extract_acronyms_from_definitions()
        self.internal__extract_acronyms_from_abstracts()
        self.internal__filter_common_word_acronyms()
        self.internal__add_known_acronyms()
        self.internal__prepare_fingerprints()
        self.internal__reduce_keys()
        self.internal__explode_and_group_values_by_key()
        self._sort_data_frame_by_rows_and_key()
        self.internal__sort_mapping_values()
        self.internal__validate_keys()
        self._write_thesaurus_data_frame_to_disk()
        self.internal__notify_process_end()
        self.internal__print_thesaurus_header_to_stream(n=8, stream=sys.stderr)
