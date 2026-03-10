"""
Get Values
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

    >>> from tm2p.refine.thesaurus_old.user import GetValues
    >>> terms = (
    ...     GetValues()
    ...     .with_thesaurus_file("demo.the.txt")
    ...     .using_pattern(["FINTECH", "FINANCIAL_TECHNOLOGIES"])
    ...     .where_root_directory("tests/scopus/")
    ...     .run()
    ... )
    >>> terms[:5]
    ['FINANCIAL_TECHNOLOGIES', 'FINANCIAL_TECHNOLOGY', 'FINTECH', 'FINTECHS']



"""

import sys

from tm2p._intern import ParamsMixin
from tm2p.refine.thesaurus_old._intern import ThesaurusMixin


class GetValues(
    ParamsMixin,
    ThesaurusMixin,
):
    """:meta private:"""

    # -------------------------------------------------------------------------
    def internal__get_values(self):
        self.data_frame = self.data_frame[
            self.data_frame["key"].isin(self.params.pattern)
        ].copy()
        values = self.data_frame["value"].to_list()
        values = [t.strip() for v in values for t in v.split("; ")]
        self.values = values

    # -------------------------------------------------------------------------
    def run(self):
        """:meta private:"""

        if self.params.quiet is False:
            sys.stderr.write("Getting thesaurus values...\n")
            sys.stderr.flush()

        self._build_user_thesaurus_path()
        self._load_thesaurus_as_mapping()
        self._transform_mapping_to_data_frame()
        self.internal__get_values()

        if self.params.quiet is False:
            sys.stderr.write("Getting thesaurus values completed successfully\n")
            sys.stderr.flush()

        return self.values
