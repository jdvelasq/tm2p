"""
Statistics
===============================================================================

Smoke tests:
    >>> from tm2p import CorpusField
    >>> from tm2p.ingest.records import Statistics
    >>> df = (
    ...     Statistics()
    ...     .with_source_field(CorpusField.AUTH_KEY_RAW)
    ...     .where_root_directory("tests/fintech/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .run()
    ... )
    >>> df.head() # doctest: +SKIP
                         ART_NO                            ... REC_NO
                          count       mean std        min  ...    25%   50%   75%   max
    AUTH_KEY_RAW                                           ...
    Actor network theory    0.0        NaN NaN        NaN  ...   23.0  23.0  23.0  23.0
    Alipay                  1.0  2971643.0 NaN  2971643.0  ...    3.0   3.0   3.0   3.0
    Alternative finance     0.0        NaN NaN        NaN  ...   19.0  19.0  19.0  19.0
    Alternative lending     0.0        NaN NaN        NaN  ...   19.0  19.0  19.0  19.0
    Bank                    1.0  7796617.0 NaN  7796617.0  ...   20.0  20.0  20.0  20.0
    <BLANKLINE>
    [5 rows x 80 columns]



"""

from tm2p._intern import ParamsMixin
from tm2p._intern.data_access import load_filtered_main_csv_zip


class Statistics(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):

        field = self.params.source_field.value

        records = load_filtered_main_csv_zip(params=self.params)
        records = records.dropna(subset=[field])
        records[field] = records[field].str.split("; ")
        records = records.explode(field)
        records[field] = records[field].str.strip()
        summary = records.groupby(field).describe()

        return summary


#
