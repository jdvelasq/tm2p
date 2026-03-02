"""
LTWAColumn
===============================================================================

Smoke test:
    >>> from tm2p import Field
    >>> from tm2p.ingest.oper import LTWAColumn
    >>> (
    ...     LTWAColumn()
    ...     .with_source_field(Field.SRC_RAW)
    ...     .with_target_field(Field.USR0)
    ...     .where_root_directory("tests/fintech/")
    ...     .run()
    ... )
    180

    >>> from tm2p.ingest.oper import Query
    >>> (
    ...     Query()
    ...     .with_query_expression("SELECT USR0 FROM database LIMIT 10;")
    ...     .where_root_directory("tests/fintech/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .run()
    ... )
                                                    USR0
    0                            J FINANC REPORT ACCOUNT
    1  HARNESSING BLOCKCHAIN-DIGITAL TWIN FUSION SUST...
    2                            J FINANC REPORT ACCOUNT
    3                                ELECTRON COMMER RES
    4                                INT REV ECON FINANC
    5                                    INT J BANK MARK
    6                                       RESOUR POLIC
    7                                    BUS STRATEG ENV
    8                                ELECTRON COMMER RES
    9                                       RESOUR POLIC




"""

from tm2p._intern import ParamsMixin
from tm2p.ingest.data_sourc._intern.oper.ltwa_col import ltwa_column
from tm2p.ingest.extr._helpers._protected_fields import PROTECTED_FIELDS


class LTWAColumn(
    ParamsMixin,
):
    """:meta private:"""

    def run(self) -> int:

        if self.params.source_field == self.params.target_field:
            raise ValueError(
                f"Source and target fields must differ (got `{self.params.source_field}`)"
            )

        if self.params.target_field in PROTECTED_FIELDS:
            raise ValueError(f"Field `{self.params.target_field}` is protected")

        return ltwa_column(
            source=self.params.source_field,
            target=self.params.target_field,
            root_directory=self.params.root_directory,
        )


#
