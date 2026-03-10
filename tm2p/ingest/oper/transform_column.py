"""
TransformColumn
===============================================================================

Smoke test:
    >>> from tm2p import Field
    >>> from tm2p.ingest.oper import TransformColumn
    >>> (
    ...     TransformColumn()
    ...     .with_source_field(Field.AUTHKW_RAW)
    ...     .with_target_field(Field.USR0)
    ...     .with_transformation_function(lambda x: x.str.upper())
    ...     .where_root_directory("tests/scopus/")
    ...     .run()
    ... )
    154

    >>> from tm2p.ingest.oper import Query
    >>> (
    ...     Query()
    ...     .with_query_expression("SELECT USR0 FROM database LIMIT 10;")
    ...     .where_root_directory("tests/scopus/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .run()
    ... )
                                                    USR0
    0  DIGITAL TRANSFORMATION; FINANCIAL SECTOR; FINT...
    1                                               None
    2  ARTIFICIAL INTELLIGENCE; BANKING INDUSTRY SECT...
    3  CHINA; FINTECH; G38; INTENTION TO USE; L16; M1...
    4  FINTECH; GREEN ENVIRONMENTAL INDEX; GREEN FINA...
    5  BANKING; DARK SIDE; FINANCIAL SERVICES; FINTEC...
    6  ENVIRONMENTAL SUSTAINABILITY; FINTECH; NATURAL...
    7  CORPORATE CARBON EMISSIONS; CORPORATE GREEN IN...
    8  A COMPARATIVE STUDY; FINTECH; G11; G14; G15; G...
    9  CARBON EMISSIONS: GREEN FINANCE; ENVIRONMENTAL...


"""

from tm2p._intern import ParamsMixin
from tm2p.ingest.data_sourc._intern.oper.transform_col import transform_column
from tm2p.ingest.extr._helpers._protected_fields import PROTECTED_FIELDS


class TransformColumn(
    ParamsMixin,
):
    """:meta private:"""

    def run(self) -> int:

        if self.params.source_field == self.params.target_field:
            raise ValueError(
                f"Source and target fields must differ (got `{self.params.source_field}`)"
            )

        if self.params.source_field in PROTECTED_FIELDS:
            raise ValueError(f"Field `{self.params.source_field}` is protected")

        if self.params.transformation_function is None:
            raise ValueError("Transformation function must be provided")

        return transform_column(
            #
            # FIELD:
            source=self.params.source_field,
            target=self.params.target_field,
            function=self.params.transformation_function,
            root_directory=self.params.root_directory,
        )


#
