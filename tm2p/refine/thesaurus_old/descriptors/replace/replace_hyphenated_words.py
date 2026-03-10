"""
Replace hyphenated words
===============================================================================

Smoke tests:
    >>> import sys
    >>> from io import StringIO
    >>> from tm2p.refine.thesaurus_old.descriptors import InitializeThesaurus, ReplaceHyphenatedWords

    >>> # Redirecting stderr to avoid messages
    >>> original_stderr = sys.stderr
    >>> sys.stderr = StringIO()

    >>> # Create thesaurus
    >>> InitializeThesaurus(root_directory="examples/fintech/", quiet=True).run()

    >>> # Configure and run the replacer
    >>> replacer = (
    ...     ReplaceHyphenatedWords(tqdm_disable=True, )
    ...     .where_root_directory("tests/scopus/")
    ... )
    >>> replacer.run()

    >>> # Capture and print stderr output
    >>> output = sys.stderr.getvalue()
    >>> sys.stderr = original_stderr
    >>> print(output)  # doctest: +SKIP
    Replacing hyphenated words in thesaurus keys...
      File : examples/fintech/data/thesaurus/descriptors.the.txt
      33 hypenated words transformed successfully
      Replacement process completed successfully
    <BLANKLINE>
    Printing thesaurus header
      File : examples/fintech/data/thesaurus/descriptors.the.txt
    <BLANKLINE>
        A_FINTECH_ECO_SYSTEM
          A_FINTECH_ECOSYSTEM
        A_WIDE_RANGING_RE_CONCEPTUALIZATION
          A_WIDE_RANGING_RECONCEPTUALIZATION
        AGRI_BUSINESS
          AGRIBUSINESS
        BACK_OFFICE_FUNCTIONS
          BACKOFFICE_FUNCTIONS
        BLOCK_CHAIN
          BLOCKCHAIN
        BLOCK_CHAIN_IMPLEMENTATION
          BLOCKCHAIN_IMPLEMENTATION
        BROADER_AGRICULTURE_ECO_SYSTEM
          BROADER_AGRICULTURE_ECOSYSTEM
        COMPLEX_GENERATES_DIGITAL_ECO_SYSTEMS
          COMPLEX_GENERATES_DIGITAL_ECOSYSTEMS
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
from tm2p._intern.packag_data.word_lists import load_builtin_word_list
from tm2p.refine.thesaurus_old._intern import ThesaurusMixin

tqdm.pandas()


class ReplaceHyphenatedWords(
    ParamsMixin,
    ThesaurusMixin,
):
    """:meta private:"""

    #
    # NOTIFICATIONS:
    # -------------------------------------------------------------------------
    def internal__notify_process_start(self):

        file_path = str(self.thesaurus_path)

        if self.params.colored_stderr:
            filename = str(file_path).rsplit("/", maxsplit=1)[1]
            file_path = file_path.replace(filename, f"{Fore.RESET}{filename}")
            file_path = Fore.LIGHTBLACK_EX + file_path

        sys.stderr.write("Replacing hyphenated words in thesaurus keys...\n")
        sys.stderr.write(f"  File : {file_path}\n")
        sys.stderr.flush()

    # -------------------------------------------------------------------------
    def internal__notify_process_end(self):
        sys.stderr.write(f"  Replacement process completed successfully\n\n")
        sys.stderr.flush()

    #
    # ALGORITHM:
    # -------------------------------------------------------------------------
    def internal__fix_when_hyphenated_form_is_correct(self):

        self.data_frame["__row_selected__"] = False
        self.data_frame["org_key"] = self.data_frame["key"].copy()

        # replace the word by this hyphenated version
        words = load_builtin_word_list("hyphenated_is_correct.txt")

        patterns = []

        #
        # Words in lower case + spaces
        #
        patterns += [
            (
                re.compile(r"^" + word.lower().replace("_", "") + " "),
                word.lower() + " ",
            )
            for word in words
        ]

        patterns += [
            (
                re.compile(r" " + word.lower().replace("_", "") + r"$"),
                " " + word.lower(),
            )
            for word in words
        ]

        patterns += [
            (
                re.compile(r"^" + word.lower().replace("_", "") + r"$"),
                word.lower(),
            )
            for word in words
        ]

        #
        # Words in upper case + spaces
        #
        patterns += [
            (
                re.compile(r"^" + word.upper().replace("_", "") + " "),
                word.upper() + " ",
            )
            for word in words
        ]

        patterns += [
            (
                re.compile(r" " + word.upper().replace("_", "") + r"$"),
                " " + word.upper(),
            )
            for word in words
        ]

        patterns += [
            (
                re.compile(r"^" + word.upper().replace("_", "") + r"$"),
                word.upper(),
            )
            for word in words
        ]

        #
        # Words in upper case + "_"
        #
        patterns += [
            (
                re.compile(r"^" + word.upper().replace("_", "") + "_"),
                word.upper() + "_",
            )
            for word in words
        ]

        patterns += [
            (
                re.compile(r"_" + word.upper().replace("_", "") + r"$"),
                "_" + word.upper(),
            )
            for word in words
        ]

        # replace the words
        def f(x):
            for pattern, replacement in patterns:
                x = pattern.sub(replacement, x)
            return x

        tqdm.pandas(
            desc="    Processing correct words ",
            disable=self.params.tqdm_disable,
            ncols=80,
        )
        self.data_frame["key"] = self.data_frame["key"].progress_apply(f)
        tqdm.pandas(desc=None)

    # -------------------------------------------------------------------------
    def internal__fix_when_hyphenated_form_is_incorrect(self):

        # replace the word by this hyphenated version
        words = load_builtin_word_list("hyphenated_is_incorrect.txt")

        patterns = []

        #
        # Words in lower case + spaces
        #
        patterns += [
            (
                re.compile(r"^" + word.lower() + " "),
                word.lower().replace("_", "") + " ",
            )
            for word in words
        ]

        patterns += [
            (
                re.compile(r" " + word.lower() + r"$"),
                " " + word.lower().replace("_", ""),
            )
            for word in words
        ]

        patterns += [
            (
                re.compile(r"^" + word.lower() + r"$"),
                word.lower().replace("_", ""),
            )
            for word in words
        ]

        #
        # Words in upper case + spaces
        #
        patterns += [
            (
                re.compile(r"^" + word.upper() + " "),
                word.upper().replace("_", "") + " ",
            )
            for word in words
        ]

        patterns += [
            (
                re.compile(r" " + word.upper() + r"$"),
                " " + word.upper().replace("_", ""),
            )
            for word in words
        ]

        patterns += [
            (
                re.compile(r"^" + word.upper() + r"$"),
                word.upper().replace("_", ""),
            )
            for word in words
        ]

        #
        # Words in upper case + "_"
        #
        patterns += [
            (
                re.compile(r"^" + word.upper() + "_"),
                word.upper().replace("_", "") + "_",
            )
            for word in words
        ]

        patterns += [
            (
                re.compile(r"_" + word.upper() + r"$"),
                "_" + word.upper().replace("_", ""),
            )
            for word in words
        ]

        # replace the words
        def f(x):
            for pattern, replacement in patterns:
                x = pattern.sub(replacement, x)
            return x

        tqdm.pandas(
            desc="  Processing incorrect words ",
            disable=self.params.tqdm_disable,
            ncols=80,
        )
        self.data_frame["key"] = self.data_frame["key"].progress_apply(f)
        tqdm.pandas(desc=None)

        self.data_frame.loc[
            self.data_frame.key != self.data_frame.org_key,
            "__row_selected__",
        ] = True

        n_matches = self.data_frame.__row_selected__.sum()

        sys.stderr.write(f"  {n_matches} hypenated words transformed successfully\n")
        sys.stderr.flush()

    # -------------------------------------------------------------------------
    def run(self):
        """:meta private:"""

        self.with_thesaurus_file("concepts.the.txt")

        self._build_user_thesaurus_path()
        self.internal__notify_process_start()
        self._load_thesaurus_as_mapping()
        self._transform_mapping_to_data_frame()
        #
        self.internal__fix_when_hyphenated_form_is_correct()
        self.internal__fix_when_hyphenated_form_is_incorrect()
        #
        self.internal__reduce_keys()
        self.internal__explode_and_group_values_by_key()
        self._sort_data_frame_by_rows_and_key()
        self._write_thesaurus_data_frame_to_disk()
        self.internal__notify_process_end()
        self.internal__print_thesaurus_header_to_stream(n=8, stream=sys.stderr)
