"""
CopyColumn
===============================================================================

Smoke Test:
    >>> from tm2p import Field
    >>> from tm2p.ingest.oper import CopyColumn
    >>> (
    ...     CopyColumn()
    ...     .with_source_field(Field.AUTHKW_RAW)
    ...     .with_target_field(Field.USR0)
    ...     .where_root_directory("tests/scopus/")
    ...     .run()
    ... )
    154

    >>> from tm2p.ingest.oper import Query
    >>> (
    ...     Query()
    ...     .with_query_expression("SELECT USR0 FROM database LIMIT 5;")
    ...     .where_root_directory("tests/scopus/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     #
    ...     .run()
    ... )
                                                    USR0
    0  Digital transformation; Financial sector; FinT...
    1                                               None
    2  Artificial intelligence; Banking industry sect...
    3  China; Fintech; G38; Intention to use; L16; M1...
    4  Fintech; Green environmental index; Green fina...


"""

from tm2p._intern import ParamsMixin
from tm2p.ingest.data_sourc._intern.oper.copy_col import copy_column
from tm2p.ingest.extr._helpers._protected_fields import PROTECTED_FIELDS


class CopyColumn(
    ParamsMixin,
):
    """:meta private:"""

    def run(self) -> int:

        if self.params.source_field == self.params.target_field:
            raise ValueError(
                f"Source and target fields must differ (got `{self.params.source_field}`)"
            )

        if self.params.target_field in PROTECTED_FIELDS:
            raise ValueError(
                f"Cannot overwrite protected field `{self.params.target_field}`"
            )

        return copy_column(
            source=self.params.source_field,
            target=self.params.target_field,
            root_directory=self.params.root_directory,
        )


#
