"""
CoalesceColumn
===============================================================================

Smoke test:
    >>> from tm2p import Field
    >>> from tm2p.ingest.oper import CopyColumn
    >>> (
    ...     CopyColumn()
    ...     .with_source_field(Field.SRC_ISO4_RAW)
    ...     .with_target_field(Field.USR0)
    ...     .where_root_directory("tests/fintech/")
    ...     .run()
    ... )
    180

    >>> from tm2p.ingest.oper import TransformColumn
    >>> (
    ...     TransformColumn()
    ...     .with_source_field(Field.USR0)
    ...     .with_target_field(Field.USR1)
    ...     .with_transformation_function(lambda x: None)
    ...     .where_root_directory("tests/fintech/")
    ...     .run()
    ... )
    0

    >>> from tm2p.ingest.oper import CoalesceColumn
    >>> (
    ...     CoalesceColumn()
    ...     .with_source_field(Field.SRC_ISO4_NORM)
    ...     .with_target_field(Field.USR1)
    ...     .where_root_directory("tests/fintech/")
    ...     .with_transformation_function(lambda x: pd.NA)
    ...     .run()
    ... )

    >>> from tm2p.ingest.oper import Query
    >>> (
    ...     Query()
    ...     .with_query_expression("SELECT USR1 FROM database LIMIT 5;")
    ...     .where_root_directory("tests/fintech/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...    .run()
    ... )
                                                    USR1
    0                            J FINANC REPORT ACCOUNT
    1  HARNESSING BLOCKCHAIN-DIGITAL TWIN FUSION SUST...
    2                            J FINANC REPORT ACCOUNT
    3                                ELECTRON COMMER RES
    4                                INT REV ECON FINANC


"""

from tm2p._intern import ParamsMixin
from tm2p.ingest.data_sourc._intern.oper.coalesc_col import coalesce_column
from tm2p.ingest.extr._helpers._protected_fields import PROTECTED_FIELDS


class CoalesceColumn(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):

        if self.params.source_field == self.params.target_field:
            raise ValueError(
                f"Source and target fields must differ (got `{self.params.source_field}`)"
            )

        if self.params.target_field in PROTECTED_FIELDS:
            raise ValueError(
                f"Cannot fill a protected field `{self.params.target_field}`"
            )

        coalesce_column(
            source=self.params.source_field,
            target=self.params.target_field,
            root_directory=self.params.root_directory,
        )
