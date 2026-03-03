"""
Cutoff Fuzzy Merging
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


    >>> from tm2p.refine.thesaurus_old.user import ReduceKeys
    >>> (
    ...     ReduceKeys()
    ...     .with_thesaurus_file("demo.the.txt")
    ...     .using_colored_output(False)
    ...     .where_root_directory("tests/fintech/")
    ...     .run()
    ... )
    INFO: Thesaurus keys reduced successfully.
      Success : True
      File    : examples/fintech/data/thesaurus/demo.the.txt
      Status  : 0 changed keys
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


    >>> from tm2p.refine.thesaurus_old.user import CutoffFuzzyMerging
    >>> r = (
    ...     CutoffFuzzyMerging(tqdm_disable=True)
    ...     .with_thesaurus_file("demo.the.txt")
    ...     .with_field("raw_descriptors")
    ...     .where_root_directory("tests/fintech/")
    ...     .using_cutoff_threshold(85)
    ...     .using_match_threshold(95)
    ...     .run()
    ... ).to_string()
    >>> print(r)
                                                      lead                                                 candidate  fuzzy  cutoff
    0                            SYSTEMIC_INNOVATION_MODEL                               A_SYSTEMIC_INNOVATION_MODEL  100.0    96.0
    1               COMPETITIVE_AND_COOPERATIVE_MECHANISMS                THE_COMPETITIVE_AND_COOPERATIVE_MECHANISMS  100.0    95.0
    2              ECONOMIC_AND_TECHNOLOGICAL_DETERMINANTS               THE_ECONOMIC_AND_TECHNOLOGICAL_DETERMINANTS  100.0    95.0
    3                                  GROWING_COMPETITION                                     A_GROWING_COMPETITION  100.0    95.0
    4                                 MULTI_LEVEL_ANALYSIS                                    A_MULTI_LEVEL_ANALYSIS  100.0    95.0
    5                                THEORETICAL_FRAMEWORK                                   A_THEORETICAL_FRAMEWORK  100.0    95.0
    6                                     CLUSTER_ANALYSIS                                        A_CLUSTER_ANALYSIS  100.0    94.0
    7                                    HYBRID_MCDM_MODEL                                       A_HYBRID_MCDM_MODEL  100.0    94.0
    8   UNIFIED_THEORY_OF_ACCEPTANCE_AND_USE_OF_TECHNOLOGY  UNIFIED_THEORY_OF_ACCEPTANCE_AND_USE_OF_TECHNOLOGY_MODEL  100.0    94.0
    9                          A_SYSTEMIC_INNOVATION_MODEL                           A_NEW_SYSTEMIC_INNOVATION_MODEL  100.0    93.0
    10                        ELABORATION_LIKELIHOOD_MODEL                          THE_ELABORATION_LIKELIHOOD_MODEL  100.0    93.0
    11                         TECHNOLOGY_ACCEPTANCE_MODEL                           THE_TECHNOLOGY_ACCEPTANCE_MODEL  100.0    93.0
    12                             A_THEORETICAL_FRAMEWORK                               A_NEW_THEORETICAL_FRAMEWORK  100.0    92.0
    13                                         COMPETITION                                             A_COMPETITION  100.0    92.0
    14                              HISTORICAL_DEVELOPMENT                                THE_HISTORICAL_DEVELOPMENT  100.0    92.0
    15                              INFORMATION_TECHNOLOGY                                THE_INFORMATION_TECHNOLOGY  100.0    92.0
    16                             SUSTAINABLE_DEVELOPMENT                               THE_SUSTAINABLE_DEVELOPMENT  100.0    92.0
    17                            SYSTEMIC_CHARACTERISTICS                              THE_SYSTEMIC_CHARACTERISTICS  100.0    92.0
    18                                          DEFINITION                                              A_DEFINITION  100.0    91.0
    19                                DEVELOPING_COUNTRIES                                  THE_DEVELOPING_COUNTRIES  100.0    91.0
    20                               INNOVATION_MECHANISMS                                 THE_INNOVATION_MECHANISMS  100.0    91.0
    21                                STRATEGIC_CAPABILITY                                  THE_STRATEGIC_CAPABILITY  100.0    91.0
    22                               THEORETICAL_FRAMEWORK                                 THE_THEORETICAL_FRAMEWORK  100.0    91.0
    23                                            TAXONOMY                                                A_TAXONOMY  100.0    89.0
    24                                       ORGANIZATIONS                                           AN_ORGANIZATION   96.0    86.0
    25                                 RESEARCH_FRAMEWORKS                                      A_RESEARCH_FRAMEWORK   95.0    92.0
    26                               CONCEPTUAL_FRAMEWORKS                                  THE_CONCEPTUAL_FRAMEWORK   95.0    89.0
    27                                          CHALLENGES                                               A_CHALLENGE   95.0    86.0


"""

import pandas as pd
from fuzzywuzzy import fuzz  # type: ignore
from tqdm import tqdm  # type: ignore

from tm2p._intern import ParamsMixin
from tm2p._intern.data_access import load_filtered_main_csv_zip
from tm2p._intern.packag_data.word_lists import load_builtin_word_list
from tm2p.anal.metrics.metrics import Metrics
from tm2p.refine.thesaurus_old._intern import ThesaurusMixin

tqdm.pandas()


class CutoffFuzzyMerging(
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
    def internal__get_raw_occurrences(self):

        records = load_filtered_main_csv_zip(params=self.params)
        records = records[[self.params.source_field]]
        records = records.dropna()
        records[self.params.source_field] = records[self.params.source_field].str.split(
            "; "
        )
        records = records.explode(self.params.source_field)
        records[self.params.source_field] = records[
            self.params.source_field
        ].str.strip()
        records["OCC"] = 1
        counts = records.groupby(self.params.source_field, as_index=True).agg(
            {"OCC": "sum"}
        )

        self.raw_key2occ = dict(zip(counts.index, counts.OCC))

    # -------------------------------------------------------------------------
    def internal__compute_key_occurrences(self):

        self.key_occurrences = self.data_frame.copy()

        self.key_occurrences["value"] = self.key_occurrences["value"].str.split("; ")
        self.key_occurrences = self.key_occurrences.explode("value")
        self.key_occurrences["value"] = self.key_occurrences["value"].str.strip()

        self.key_occurrences["OCC"] = self.key_occurrences.value.map(
            # lambda x: raw_key2occ.get(x, 1)
            lambda x: self.raw_key2occ[x]
        )
        self.key_occurrences["OCC"] = self.key_occurrences["OCC"].astype(int)
        self.key_occurrences = self.key_occurrences[["key", "OCC"]]
        self.key_occurrences = self.key_occurrences.groupby("key", as_index=False).agg(
            {"OCC": "sum"}
        )

        keys2occ = dict(zip(self.key_occurrences.key, self.key_occurrences.OCC))

        self.data_frame["OCC"] = self.data_frame.key.map(keys2occ)

    # -------------------------------------------------------------------------
    def internal__sort_by_keylength(self):

        self.data_frame["key_length"] = self.data_frame["key"].str.len()

        self.data_frame = self.data_frame.sort_values(
            by=["key_length", "OCC"], ascending=[True, False]
        )

    # -------------------------------------------------------------------------
    def internal__compute_fuzzy_match(self, string1, string2):

        # obtain the shorten and lengthen strings
        string1 = string1.split(" ")
        string2 = string2.split(" ")

        if len(string1) > len(string2):
            shorten_string = string2
            lengthen_string = string1
        else:
            shorten_string = string1
            lengthen_string = string2

        scores_per_word = []
        for base_word in shorten_string:
            best_match = 0
            for candidate_word in lengthen_string:
                score = fuzz.ratio(base_word, candidate_word)
                if score > best_match:
                    best_match = score
            scores_per_word.append(best_match)

        score = min(scores_per_word)
        match = all(score >= self.params.fuzzy_threshold for score in scores_per_word)

        return score, match

    # -------------------------------------------------------------------------
    def internal__compute_mergings(self):

        self.data_frame["selected"] = False
        self.data_frame["cutoff"] = 0.0
        self.data_frame["fuzzy"] = 0.0
        self.data_frame = self.data_frame.reset_index(drop=True)
        self.data_frame["key"] = self.data_frame["key"].str.lower()
        self.data_frame["key"] = self.data_frame["key"].str.replace("_", " ")
        self.data_frame["key_length"] = self.data_frame["key"].str.len()

        ##
        self.data_frame["__row_selected__"] = False
        ##

        keys = self.data_frame["key"].tolist()
        mergings = {}

        for index, key in tqdm(
            enumerate(keys),
            total=len(keys),
            desc="  Progress",
            ncols=80,
            disable=self.params.tqdm_disable,
        ):

            if self.data_frame.loc[index, "selected"] is True:
                continue

            # Select the rows not evaluated
            df = self.data_frame[self.data_frame.index > index]

            # Only evaluate noun phrases
            key_length = len(key.split(" "))
            df = df[
                df.is_keyword.apply(lambda x: x is False)
                | (df.key_length == key_length)
            ]

            # Preselect
            diff_in_length = (
                int((1 - self.params.similarity_cutoff / 100.0) * len(key)) + 1
            )
            min_key_length = max(len(key) - diff_in_length, 1)
            max_key_length = len(key) + diff_in_length
            df = df[df.key_length <= max_key_length]
            df = df[df.key_length >= min_key_length]

            # Apply the cutoff rule
            df["cutoff"] = df["key"].apply(lambda x: fuzz.ratio(key, x))
            df = df[df["cutoff"] >= self.params.similarity_cutoff]

            if df.empty:
                continue

            results = df["key"].apply(
                lambda x: self.internal__compute_fuzzy_match(key, x)
            )

            df["fuzzy"] = results.map(lambda x: x[0])
            df["fuzzy_match"] = results.map(lambda x: x[1])

            df = df[df["fuzzy_match"].apply(lambda x: x is True)]

            if df.empty:
                continue

            key = key.replace(" ", "_").upper()
            df["key"] = df["key"].str.replace(" ", "_").str.upper()

            self.data_frame.loc[df.index, "fuzzy"] = df.fuzzy
            self.data_frame.loc[df.index, "cutoff"] = df.cutoff
            self.data_frame.loc[df.index, "selected"] = True
            self.data_frame.loc[df.index, "__row_selected__"] = True
            self.data_frame.loc[self.data_frame["key"] == key, "__row_selected__"] = (
                True
            )

            mergings[key] = df["key"].tolist()

        self.mergings = mergings

        self.data_frame["key"] = self.data_frame["key"].str.upper()
        self.data_frame["key"] = self.data_frame["key"].str.replace(" ", "_")

    # -------------------------------------------------------------------------
    def internal__generate_merging_data_frame(self):

        # reversed_mergings = {v: k for k, vs in self.mergings.items() for v in vs}
        # self.data_frame["key"] = self.data_frame["key"].map(
        #     lambda x: reversed_mergings.get(x, x)
        # )

        fuzzy_mapping = {row.key: row.fuzzy for _, row in self.data_frame.iterrows()}
        cutoff_mapping = {row.key: row.cutoff for _, row in self.data_frame.iterrows()}

        keys = [key for key, values in self.mergings.items() for _ in values]
        values = [value for _, values in self.mergings.items() for value in values]
        self.result = pd.DataFrame(
            {
                "lead": keys,
                "candidate": values,
            }
        )

        self.result["fuzzy"] = self.result["candidate"].map(fuzzy_mapping)
        self.result["cutoff"] = self.result["candidate"].map(cutoff_mapping)
        self.result = self.result.sort_values(
            by=["fuzzy", "cutoff", "lead"], ascending=[False, False, True]
        ).reset_index(drop=True)

    # -------------------------------------------------------------------------
    def run(self):
        """:meta private:"""

        self._build_user_thesaurus_path()
        self._load_thesaurus_as_mapping()
        self._transform_mapping_to_data_frame()
        self.internal__set_initial_keys()
        self.internal__get_keywords()
        self.internal__mark_keywords()
        self.internal__get_raw_occurrences()
        self.internal__compute_key_occurrences()
        self.internal__sort_by_keylength()
        self.internal__compute_mergings()
        self.internal__generate_merging_data_frame()

        return self.result
