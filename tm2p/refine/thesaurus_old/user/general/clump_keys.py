"""
Clump Keys
===============================================================================


Smoke tests:
    >>> from tm2p.refine.thesaurus_old.user import InitializeThesaurus
    >>> (
    ...     InitializeThesaurus()
    ...     .with_thesaurus_file("demo.the.txt")
    ...     .with_field("raw_descriptors")
    ...     .where_root_directory("tests/fintech/")
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


    >>> from tm2p.refine.thesaurus_old.user import ClumpKeys
    >>> (
    ...     ClumpKeys(tqdm_disable=True, )
    ...     .with_thesaurus_file("demo.the.txt")
    ...     .using_colored_output(False)
    ...     .where_root_directory("tests/fintech/")
    ...     .run()
    ... )
    INFO: Thesaurus clumped successfully.
      Success : True
      File    : examples/fintech/data/thesaurus/demo.the.txt
      Status  : 64 changed keys
      Header  :
        BUSINESS_MODELS
          BUSINESS_MODEL; BUSINESS_MODELS; NEW_BUSINESS_MODELS; REIMAGINE_BUSINESS_...
        CAPACITY_BUILDING
          CAPACITY_BUILDING; LARGE_SCALE_CAPACITY_BUILDING
        CASE_STUDY
          A_CASE_STUDY; CASE_STUDIES; CASE_STUDY; CASE_STUDY_SAMPLES; THE_CASE_STUD...
        CLUSTER_ANALYSIS
          A_CLUSTER_ANALYSIS; CLUSTER_ANALYSIS
        DATA_DRIVEN
          A_THEORETICAL_DATA_DRIVEN_FINTECH_FRAMEWORK; DATA_DRIVEN
        DATA_SECURITY
          DATA_SECURITY; DATA_SECURITY_AND_CONSUMER_TRUST; SECURITY_OF_DATA
        DECISION_MAKING
          A_NOVEL_HYBRID_MULTIPLE_CRITERIA_DECISION_MAKING_METHOD; DECISION_MAKING;...
        DEVELOPING_COUNTRIES
          DEVELOPING_COUNTRIES; THE_DEVELOPING_COUNTRIES
    <BLANKLINE>





"""

import re

from tqdm import tqdm  # type: ignore

from tm2p._intern import ParamsMixin
from tm2p._intern.packag_data.word_lists import load_builtin_word_list
from tm2p.anal.metrics.metrics import Metrics
from tm2p.refine.thesaurus_old._intern import ThesaurusMixin, ThesaurusResult


class ClumpKeys(
    ParamsMixin,
    ThesaurusMixin,
):
    """:meta private:"""

    #
    # ALGORITHM:
    # -------------------------------------------------------------------------
    def internal__get_keywords(self):

        self.keywords = (
            Metrics()
            .with_source_field("raw_keywords")
            .having_items_ordered_by("OCC")
            .where_root_directory(self.params.root_directory)
        ).run()

        known_keywords = load_builtin_word_list("noun_phrases.txt")

        self.keywords = self.keywords[self.keywords.index.isin(known_keywords)]

        self.keywords["length"] = self.keywords.index.str.split("_").str.len()
        self.keywords = self.keywords.sort_values(
            by=["length", "rank_occ"], ascending=[False, True]
        )

    # -------------------------------------------------------------------------
    def internal__mark_keywords(self):
        self.data_frame["is_keyword"] = False
        self.data_frame.loc[
            self.data_frame["key"].isin(self.keywords.index.to_list()), "is_keyword"
        ] = True

    # -------------------------------------------------------------------------
    def internal__combine_keywords(self):

        for keyword, _ in tqdm(
            self.keywords.iterrows(),
            total=self.keywords.shape[0],
            desc="  Clumping keywords ",
            disable=self.params.tqdm_disable,
            ncols=80,
        ):

            regex = keyword.replace("_", " ")
            regex = re.escape(regex)
            regex = r"\b" + regex + r"\b"

            candidates = self.data_frame.copy()
            candidates = candidates[
                candidates.is_keyword.apply(lambda x: x is False)
            ].copy()
            candidates = candidates[
                candidates["phrase"].str.contains(regex, regex=True)
            ]
            if len(candidates) == 0:
                continue
            self.data_frame.loc[candidates.index, "key"] = keyword
            self.data_frame.loc[candidates.index, "is_keyword"] = True
            #
            self.data_frame.loc[
                self.data_frame["key"] == keyword, "__row_selected__"
            ] = True

    # -------------------------------------------------------------------------
    def internal__combine_words(self):

        self.data_frame["phrase"] = self.data_frame["phrase"].str.split()
        self.data_frame["phrase"] = self.data_frame["phrase"].map(sorted)
        self.data_frame["phrase"] = self.data_frame["phrase"].str.join(" ")

        for keyword, _ in tqdm(
            self.keywords.iterrows(),
            total=self.keywords.shape[0],
            desc="     Clumping words ",
            ncols=80,
            disable=self.params.tqdm_disable,
        ):

            regex = keyword.replace("_", " ")
            regex = regex.split()
            regex = sorted(regex)
            regex = " ".join(regex)
            regex = re.escape(regex)
            regex = r"\b" + regex + r"\b"

            candidates = self.data_frame.copy()
            candidates = candidates[candidates.is_keyword == False].copy()
            candidates = candidates[
                candidates["phrase"].str.contains(regex, regex=True)
            ]
            if len(candidates) == 0:
                continue
            self.data_frame.loc[candidates.index, "key"] = keyword
            self.data_frame.loc[candidates.index, "is_keyword"] = True
            #
            self.data_frame.loc[
                self.data_frame["key"] == keyword, "__row_selected__"
            ] = True

    # -------------------------------------------------------------------------
    def internal__combine_keys(self):

        self.n_initial_keys = len(self.data_frame.key.drop_duplicates())
        self.data_frame["phrase"] = self.data_frame["key"].str.replace("_", " ")
        #
        self.data_frame["__row_selected__"] = False
        #
        self.internal__combine_keywords()
        self.internal__combine_words()
        self.data_frame.pop("phrase")
        self.data_frame.pop("is_keyword")

    # -------------------------------------------------------------------------
    def internal__group_values_by_key(self):
        self.data_frame = self.data_frame.groupby("key", as_index=False).agg(
            {"value": "; ".join}
        )
        self.data_frame = self.data_frame.sort_values("key")
        self.data_frame = self.data_frame.reset_index(drop=True)

    # -------------------------------------------------------------------------
    def run(self):
        """:meta private:"""

        self._build_user_thesaurus_path()
        self._load_thesaurus_as_mapping()
        self._transform_mapping_to_data_frame()
        self.internal__set_initial_keys()
        self.internal__get_keywords()
        self.internal__mark_keywords()
        self.internal__combine_keys()
        self.internal__reduce_keys()
        self.internal__explode_and_group_values_by_key()
        self._sort_data_frame_by_rows_and_key()
        self._write_thesaurus_data_frame_to_disk()
        self.internal__set_final_keys()
        self.internal__compute_changed_keys()

        return ThesaurusResult(
            colored_output=self.params.colored_output,
            file_path=str(self.thesaurus_path),
            msg="Thesaurus clumped successfully.",
            success=True,
            status=f"{self.total_key_changes} changed keys",
            data_frame=self.data_frame,
        )
