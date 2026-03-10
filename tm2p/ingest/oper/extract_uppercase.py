"""
ExtractUppercase
===============================================================================

Smoke test:
    >>> from tm2p import Field
    >>> from tm2p.ingest.oper import ExtractUppercase
    >>> (
    ...     ExtractUppercase()
    ...     #
    ...     # FIELDS:
    ...     .with_source_field(Field.ABSTR_UPPER)
    ...     .with_target_field(Field.USR0)
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/scopus/")
    ...     #
    ...     .run()
    ... )


    >>> from tm2p.ingest.oper import Query
    >>> df = (
    ...     Query()
    ...     .with_query_expression("SELECT USR0 FROM database LIMIT 10;")
    ...     .where_root_directory("tests/scopus/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .run()
    ... )

    >>> import textwrap
    >>> print(textwrap.fill(df.values[1][0], width=90))
    fintech applications; catalysts; green finance; their capacity; streamline processes;
    facilitate transparent transactions; personalized investment options; the functionalities;
    these applications; their role; barriers; information asymmetry; inefficiencies; fund
    distribution; blockchain; ledger system; its ability; enhance trust; transparency;
    sustainable investment; highlights successful implementations; blockchain; sustainable
    finance; its practical benefits; limitations; fraud risk; administrative costs; the
    transformative potential; financial technology; fintech; blockchain; green finance;
    traditional barriers; these technologies; the functionalities; applications; open new
    horizons; sustainable investment; the way; a more resilient and environmentally conscious
    financial future

"""

from tm2p._intern import ParamsMixin
from tm2p.ingest.data_sourc._intern.oper import extract_uppercase
from tm2p.ingest.extr._helpers._protected_fields import PROTECTED_FIELDS


class ExtractUppercase(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):

        if self.params.target_field in PROTECTED_FIELDS:
            raise ValueError(f"Field `{self.params.target_field}` is protected")

        extract_uppercase(
            source=self.params.source_field,
            target=self.params.target_field,
            root_directory=self.params.root_directory,
        )
