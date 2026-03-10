"""
Explode Keys
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

    >>> from tm2p.refine.thesaurus_old.user import ExplodeKeys
    >>> (
    ...     ExplodeKeys()
    ...     .with_thesaurus_file("demo.the.txt")
    ...     .using_colored_output(False)
    ...     .where_root_directory("tests/scopus/")
    ...     .run()
    ... )
    INFO: Thesaurus exploded successfully.
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



"""

import sys

from colorama import Fore
from tqdm import tqdm  # type: ignore

from tm2p._intern import ParamsMixin
from tm2p.refine.thesaurus_old._intern import ThesaurusMixin, ThesaurusResult
from tm2p.refine.thesaurus_old.user.general.reduce_keys import ReduceKeys

tqdm.pandas()


class ExplodeKeys(
    ParamsMixin,
    ThesaurusMixin,
):
    """:meta private:"""

    #
    # ALGORITHM:
    # -------------------------------------------------------------------------
    def internal__explode_values(self):
        self.data_frame["value"] = self.data_frame["value"].str.split("; ")
        self.data_frame = self.data_frame.explode("value")
        self.data_frame["value"] = self.data_frame["value"].str.strip()
        self.data_frame = self.data_frame.reset_index(drop=True)

    # -------------------------------------------------------------------------
    def run(self):
        """:meta private:"""

        ReduceKeys().update(**self.params.__dict__).run()

        self._build_user_thesaurus_path()
        self._load_thesaurus_as_mapping()
        self._transform_mapping_to_data_frame()
        self.internal__set_initial_keys()
        self.internal__explode_values()
        self._sort_data_frame_by_rows_and_key()
        self._write_thesaurus_data_frame_to_disk()
        self.internal__set_final_keys()
        self.internal__compute_changed_keys()

        return ThesaurusResult(
            colored_output=self.params.colored_output,
            file_path=str(self.thesaurus_path),
            msg="Thesaurus exploded successfully.",
            success=True,
            status=f"{len(self.mapping.keys())} keys found",
            data_frame=self.data_frame,
        )
