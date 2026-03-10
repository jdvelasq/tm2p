"""
CountColumnItems
===============================================================================

Smoke test:
    >>> from tm2p import Field
    >>> from tm2p.ingest.oper import CountColumnItems
    >>> (
    ...     CountColumnItems()
    ...     .with_source_field(Field.AUTHKW_RAW)
    ...     .with_target_field(Field.USR0)
    ...     .where_root_directory("tests/scopus/")
    ...     .run()
    ... )
    180

    >>> from tm2p.ingest.oper import Query
    >>> (
    ...     Query()
    ...     .with_query_expression("SELECT AUTHKW_RAW, USR0 FROM database LIMIT 5;")
    ...     .where_root_directory("tests/scopus/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .run()
    ... )
                                              AUTHKW_RAW  USR0
    0  Digital transformation; Financial sector; FinT...     8
    1                                               None     0
    2  Artificial intelligence; Banking industry sect...     8
    3  China; Fintech; G38; Intention to use; L16; M1...    11
    4  Fintech; Green environmental index; Green fina...     5




"""

from tm2p._intern import ParamsMixin
from tm2p.ingest.data_sourc._intern.oper.count_col_item import count_column_items
from tm2p.ingest.extr._helpers._protected_fields import PROTECTED_FIELDS


class CountColumnItems(
    ParamsMixin,
):
    """:meta private:"""

    def run(self) -> int:

        if self.params.source_field.value == self.params.target_field.value:
            raise ValueError(
                f"Source and target fields must differ (got `{self.params.source_field.value}`)"
            )

        if self.params.target_field in PROTECTED_FIELDS:
            raise ValueError(
                f"Cannot overwrite protected field `{self.params.target_field}`"
            )
        return count_column_items(
            source=self.params.source_field,
            target=self.params.target_field,
            root_directory=self.params.root_directory,
        )


#
