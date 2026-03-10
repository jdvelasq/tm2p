"""
Replace Starts With Word
===============================================================================


Smoke tests:
    >>> from tm2p.refine.thesaurus_old.user import InitializeThesaurus
    >>> (
    ...     InitializeThesaurus()
    ...     .with_thesaurus_file("demo.the.txt")
    ...     .with_field("raw_descriptors")
    ...     .where_root_directory("tests/scopus/")
    ...     .using_colored_output(False)
    ...     .run()
    ... )
    INFO: Thesaurus initialized successfully.
      Success : True
      File    : examples/fintech/data/thesaurus/demo.the.txt
      Status  : 1721 keys found
      Header  :
        A_A_THEORY
          A_A_THEORY
        A_BASIC_RANDOM_SAMPLING_STRATEGY
          A_BASIC_RANDOM_SAMPLING_STRATEGY
        A_BEHAVIOURAL_PERSPECTIVE
          A_BEHAVIOURAL_PERSPECTIVE
        A_BETTER_UNDERSTANDING
          A_BETTER_UNDERSTANDING
        A_BLOCKCHAIN_IMPLEMENTATION_STUDY
          A_BLOCKCHAIN_IMPLEMENTATION_STUDY
        A_CASE_STUDY
          A_CASE_STUDY
        A_CHALLENGE
          A_CHALLENGE
        A_CLUSTER_ANALYSIS
          A_CLUSTER_ANALYSIS
    <BLANKLINE>


    >>> from tm2p.refine.thesaurus_old.user import ReplaceWord
    >>> (
    ...     ReplaceWord()
    ...     .with_thesaurus_file("demo.the.txt")
    ...     .having_word("BUSINESS")
    ...     .having_replacement("business")
    ...     .where_root_directory("tests/scopus/")
    ...     .using_colored_output(False)
    ...     .run()
    ... )
    INFO: Word replacement successfully.
      Success : True
      File    : examples/fintech/data/thesaurus/demo.the.txt
      Status  : 1721 keys changed
      Header  :
        business
          BUSINESS; BUSINESSES
        business_DEVELOPMENT
          BUSINESS_DEVELOPMENT
        business_INFRASTRUCTURE
          BUSINESS_INFRASTRUCTURE; BUSINESS_INFRASTRUCTURES
        business_MODEL
          BUSINESS_MODEL; BUSINESS_MODELS
        business_OPPORTUNITIES
          BUSINESS_OPPORTUNITIES
        business_PROCESS
          BUSINESS_PROCESS
        business_TO_CONSUMERS_MODELS
          BUSINESS_TO_CONSUMERS_MODELS
        FUNDAMENTALLY_NEW_business_OPPORTUNITIES
          FUNDAMENTALLY_NEW_BUSINESS_OPPORTUNITIES
    <BLANKLINE>




"""

import re
import sys

import pandas as pd  # type: ignore
from colorama import Fore, init

from tm2p._intern import ParamsMixin
from tm2p.refine.thesaurus_old._intern import ThesaurusMixin, ThesaurusResult


class ReplaceWord(
    ParamsMixin,
    ThesaurusMixin,
):
    """:meta private:"""

    #
    # ALGORITHM:
    # -------------------------------------------------------------------------
    def internal__replace_word(self):
        #
        replacement = self.params.replacement
        self.data_frame["__row_selected__"] = False
        self.data_frame["org_key"] = self.data_frame["key"].copy()
        #
        if isinstance(self.params.word, str):
            words = [self.params.word]
        else:
            words = self.params.word

        for word in words:

            # complete word:
            self.data_frame["key"] = self.data_frame["key"].str.replace(
                re.compile("^" + word + "$"), replacement, regex=True
            )

            # starting word:
            self.data_frame["key"] = self.data_frame["key"].str.replace(
                re.compile("^" + word + "_"), replacement + "_", regex=True
            )
            self.data_frame["key"] = self.data_frame["key"].str.replace(
                re.compile("^" + word + " "), replacement + " ", regex=True
            )

            # ending word:
            self.data_frame["key"] = self.data_frame["key"].str.replace(
                re.compile("_" + word + "$"), "_" + replacement, regex=True
            )
            self.data_frame["key"] = self.data_frame["key"].str.replace(
                re.compile(" " + word + "$"), " " + replacement, regex=True
            )

            # middle word:
            self.data_frame["key"] = self.data_frame["key"].str.replace(
                re.compile("_" + word + "_"), "_" + replacement + "_", regex=True
            )
            self.data_frame["key"] = self.data_frame["key"].str.replace(
                re.compile(" " + word + "_"), " " + replacement + "_", regex=True
            )
            self.data_frame["key"] = self.data_frame["key"].str.replace(
                re.compile("_" + word + " "), "_" + replacement + " ", regex=True
            )
            self.data_frame["key"] = self.data_frame["key"].str.replace(
                re.compile(" " + word + " "), " " + replacement + " ", regex=True
            )

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
        self._load_thesaurus_as_mapping()
        self._transform_mapping_to_data_frame()
        self.internal__set_initial_keys()
        self.internal__replace_word()
        self.internal__reduce_keys()
        self.internal__explode_and_group_values_by_key()
        self._sort_data_frame_by_rows_and_key()
        self._write_thesaurus_data_frame_to_disk()
        self.internal__set_final_keys()
        self.internal__compute_changed_keys()

        return ThesaurusResult(
            colored_output=self.params.colored_output,
            file_path=str(self.thesaurus_path),
            msg="Word replacement successfully.",
            success=True,
            status=f"{len(self.mapping.keys())} keys changed",
            data_frame=self.data_frame,
        )


# =============================================================================
