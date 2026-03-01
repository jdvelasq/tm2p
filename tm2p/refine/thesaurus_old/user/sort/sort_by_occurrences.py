"""
Sort by Occurrences
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

    >>> from tm2p.refine.thesaurus_old.user import SortByOccurrences
    >>> (
    ...     SortByOccurrences()
    ...     .with_thesaurus_file("demo.the.txt")
    ...     .with_field("raw_descriptors")
    ...     .where_root_directory("tests/fintech/")
    ...     .using_colored_output(False)
    ...     .run()
    ... )
    INFO: Thesaurus sorted successfully.
      Success : True
      File    : examples/fintech/data/thesaurus/demo.the.txt
      Header  :
        FINTECH
          FINTECH; FINTECHS
        FINANCE
          FINANCE
        INNOVATION
          INNOVATION; INNOVATIONS
        TECHNOLOGIES
          TECHNOLOGIES; TECHNOLOGY
        FINANCIAL_SERVICE
          FINANCIAL_SERVICE; FINANCIAL_SERVICES
        FINANCIAL_TECHNOLOGIES
          FINANCIAL_TECHNOLOGIES; FINANCIAL_TECHNOLOGY
        BANKS
          BANKS
        THE_DEVELOPMENT
          THE_DEVELOPMENT; THE_DEVELOPMENTS
    <BLANKLINE>



"""

from tm2p._intern import ParamsMixin
from tm2p._intern.data_access import load_filtered_main_csv_zip
from tm2p.refine.thesaurus_old._intern import ThesaurusMixin, ThesaurusResult


class SortByOccurrences(
    ParamsMixin,
    ThesaurusMixin,
):
    """:meta private:"""

    # -------------------------------------------------------------------------
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.raw_key2occ: dict = {}
        self.key_occurrences = None

    # -------------------------------------------------------------------------
    def _prepare_data(self):
        self._build_user_thesaurus_path()
        self._load_thesaurus_as_mapping()
        self._transform_mapping_to_data_frame()

    # -------------------------------------------------------------------------
    def _sort_data(self):
        self._get_raw_occurrences()
        self._compute_key_occurrences()

    # -------------------------------------------------------------------------
    def _get_raw_occurrences(self):

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
    def _compute_key_occurrences(self):

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

        self.data_frame = self.data_frame.sort_values(
            ["OCC", "key"], ascending=[False, True]
        )

    # -------------------------------------------------------------------------
    def _save_results(self):
        self._write_thesaurus_data_frame_to_disk()

    # -------------------------------------------------------------------------
    def _create_result(self) -> ThesaurusResult:

        return ThesaurusResult(
            colored_output=self.params.colored_output,
            file_path=str(self.thesaurus_path),
            msg="Thesaurus sorted successfully.",
            success=True,
            status=None,
            data_frame=self.data_frame,
        )

    # -------------------------------------------------------------------------
    def run(self) -> ThesaurusResult:

        self._prepare_data()
        self._sort_data()
        self._save_results()

        return self._create_result()


# =============================================================================
