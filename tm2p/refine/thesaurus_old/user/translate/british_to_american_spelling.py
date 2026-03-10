"""
British to American Spelling
===============================================================================


Smoke tests:
    >>> import sys
    >>> from io import StringIO
    >>> from tm2p.refine.thesaurus_old.user import BritishToAmericanSpelling, InitializeThesaurus

    >>> # Redirecting stderr to avoid messages during doctests
    >>> original_stderr = sys.stderr
    >>> sys.stderr = StringIO()

    >>> # Reset the thesaurus to initial state
    >>> InitializeThesaurus(thesaurus_file="demo.the.txt", field="raw_descriptors",
    ...     root_directory="examples/fintech/", quiet=True).run()

    >>> # Creates, configures, an run the translator
    >>> translator = (
    ...     BritishToAmericanSpelling(tqdm_disable=True, )
    ...     .with_thesaurus_file("demo.the.txt")
    ...     .where_root_directory("tests/scopus/")
    ... )
    >>> translator.run()

    >>> # Capture and print stderr output to test the code using doctest
    >>> output = sys.stderr.getvalue()
    >>> sys.stderr = original_stderr
    >>> print(output) # doctest: +SKIP
    Converting British to American English...
      File : examples/fintech/data/thesaurus/demo.the.txt
      10 replacements made successfully
      Translation process completed successfully
    <BLANKLINE>
    Printing thesaurus header
      File : examples/fintech/data/thesaurus/demo.the.txt
    <BLANKLINE>
        ANALOG_PROCESSES
          ANALOGUE_PROCESSES
        ANALYZE
          ANALYSE
        BEHAVIORAL_ECONOMICS
          BEHAVIOURAL_ECONOMICS
        ENTREPRENEURIAL_ENDEAVORS
          ENTREPRENEURIAL_ENDEAVOURS
        FAVOR
          FAVOUR
        HARMONIZE_TECHNOLOGICAL_ADVANCEMENTS
          HARMONISE_TECHNOLOGICAL_ADVANCEMENTS
        INSTILL_CULTURE_CHANGE
          INSTIL_CULTURE_CHANGE
        INTERNATIONAL_DEVELOPMENT_ORGANIZATIONS
          INTERNATIONAL_DEVELOPMENT_ORGANISATIONS
    <BLANKLINE>
    <BLANKLINE>



"""

import re
import sys

import pandas as pd  # type: ignore
from colorama import Fore, init
from textblob import Word  # type: ignore
from tqdm import tqdm  # type: ignore

from tm2p._intern import ParamsMixin
from tm2p.refine.thesaurus_old._intern import (
    ThesaurusMixin,
    internal__get_system_thesaurus_file_path,
    internal__load_thesaurus_as_mapping,
)

tqdm.pandas()


class BritishToAmericanSpelling(
    ParamsMixin,
    ThesaurusMixin,
):
    """:meta private:"""

    #
    # NOTIFICATIONS:
    # -------------------------------------------------------------------------
    def internal__notify_process_start(self):

        file_path = str(self.thesaurus_path)

        if len(file_path) > 72:
            file_path = "..." + file_path[-68:]

        if self.params.colored_stderr:
            filename = str(file_path).rsplit("/", maxsplit=1)[1]
            file_path = file_path.replace(filename, f"{Fore.RESET}{filename}")
            file_path = Fore.LIGHTBLACK_EX + file_path

        sys.stderr.write("Converting British to American English...\n")
        sys.stderr.write(f"  File : {file_path}\n")
        sys.stderr.flush()

    # -------------------------------------------------------------------------
    def internal__notify_process_end(self):

        sys.stderr.write("  Translation process completed successfully\n\n")
        sys.stderr.flush()

    #
    # ALGORITHM:
    # -------------------------------------------------------------------------
    def internal__translate_words_on_keys(self):

        self.data_frame["__row_selected__"] = False
        self.data_frame["org_key"] = self.data_frame["key"].copy()

        file_path = internal__get_system_thesaurus_file_path(
            "language/british2american.the.txt"
        )
        mapping = internal__load_thesaurus_as_mapping(file_path)
        mapping = {k: v[0] for k, v in mapping.items()}

        patterns = []

        for key, value in mapping.items():
            pat = [
                (re.compile(r"^" + key.lower() + " "), value.lower() + " "),
                (re.compile(r" " + key.lower() + r"$"), " " + value.lower()),
                (re.compile(r"^" + key.lower() + r"$"), value.lower()),
                (re.compile(r"^" + key.upper() + " "), value.upper() + " "),
                (re.compile(r" " + key.upper() + r"$"), " " + value.upper()),
                (re.compile(r"^" + key.upper() + r"$"), value.upper()),
                (re.compile(r"^" + key.upper() + "_"), value.upper() + "_"),
                (re.compile(r"_" + key.upper() + r"$"), "_" + value.upper()),
            ]
            patterns.extend(pat)

        # replace the words
        def f(x):
            for pattern, replacement in patterns:
                x = pattern.sub(replacement, x)
            return x

        sys.stderr.flush()
        tqdm.pandas(desc="  Progress ", disable=self.params.tqdm_disable, ncols=80)
        self.data_frame["key"] = self.data_frame["key"].progress_apply(f)
        tqdm.pandas(desc=None)
        sys.stderr.flush()

        self.data_frame.loc[
            self.data_frame.key != self.data_frame.org_key,
            "__row_selected__",
        ] = True

        n_matches = self.data_frame.__row_selected__.sum()

        sys.stderr.write(f"  {n_matches} replacements made successfully\n")
        sys.stderr.flush()

    # -------------------------------------------------------------------------
    def run(self):
        """:meta private:"""

        self._build_user_thesaurus_path()
        self.internal__notify_process_start()
        self._load_thesaurus_as_mapping()
        self._transform_mapping_to_data_frame()
        self.internal__translate_words_on_keys()
        self.internal__reduce_keys()
        self.internal__explode_and_group_values_by_key()
        self._sort_data_frame_by_rows_and_key()
        self._write_thesaurus_data_frame_to_disk()
        self.internal__notify_process_end()
        self.internal__print_thesaurus_header_to_stream(n=8, stream=sys.stderr)
