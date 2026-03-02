"""
TokenizeColumn
===============================================================================

Smoke test:
    >>> from tm2p import Field
    >>> from tm2p.ingest.oper import TokenizeColumn
    >>> (
    ...     TokenizeColumn()
    ...     #
    ...     # FIELDS:
    ...     .with_source_field(Field.ABSTR_RAW)
    ...     .with_target_field(Field.USR0)
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/fintech/")
    ...     #
    ...     .run()
    ... )
    180

    >>> from tm2p.ingest.oper import Query
    >>> df = (
    ...     Query()
    ...     .with_query_expression("SELECT USR0 FROM database LIMIT 10;")
    ...     .where_root_directory("tests/fintech/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .run()
    ... )
    >>> import textwrap
    >>> print(textwrap.fill(df.values[1][0], width=90))
    fintech applications are examined as catalysts for revolutionizing green finance ,
    showcasing their capacity to streamline processes , facilitate transparent transactions ,
    and provide personalized investment options . the functionalities of these applications
    are dissected , emphasizing their role in mitigating barriers such as information
    asymmetry and inefficiencies in fund distribution . blockchain ' s decentralized ledger
    system is analyzed for its ability to enhance trust and transparency in sustainable
    investment . it highlights successful implementations of blockchain in sustainable finance
    , illuminating its practical benefits in overcoming limitations like fraud risk and
    reducing administrative costs . this research delves into the transformative potential of
    integrating financial technology ( fintech ) and blockchain in green finance . by
    transcending traditional barriers , these technologies not only enrich the functionalities
    of applications but also open new horizons for sustainable investment , paving the way for
    a more resilient and environmentally conscious financial future . 2024 , igi global .


"""

from tm2p._intern import ParamsMixin
from tm2p.ingest.data_sourc._intern.oper.token_col import tokenize_column
from tm2p.ingest.extr._helpers._protected_fields import PROTECTED_FIELDS


class TokenizeColumn(
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

        return tokenize_column(
            source=self.params.source_field,
            target=self.params.target_field,
            root_directory=self.params.root_directory,
        )


#
