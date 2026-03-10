"""
Network Metrics
===============================================================================

Smoke tests:
    >>> from tm2p import CouplingUnit
    >>> from tm2p.synthes.netw.coupl import NetworkMetrics
    >>> df = (
    ...     NetworkMetrics()
    ...     #
    ...     # COUPLING UNIT:
    ...     .with_coupling_unit(CouplingUnit.DOC)
    ...     .having_items_in_top(30)
    ...     .having_items_in(None)
    ...     .having_citation_threshold(0)
    ...     .having_occurrence_threshold(2)
    ...     #
    ...     # COUNTERS:
    ...     .using_counters(True)
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/scopus/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    ... )
    >>> df.head(5)
                                                 DEGREE  ...  PAGERANK
    Bollaert, 2021, J CORP FINANC 1:00393             4  ...  0.089492
    Cai, 2018, ACCOUNT FINANC 1:00251                 4  ...  0.064559
    Gomber, 2017, J BUS ECON 1:01152                  3  ...  0.072873
    Haddad, 2019, BUS ECON 1:00530                    3  ...  0.046680
    Belanche, 2019, IND MANAG DATA SYST 1:00605       2  ...  0.076812
    <BLANKLINE>
    [5 rows x 4 columns]


    >>> df = (
    ...     NetworkMetrics()
    ...     #
    ...     # COUPLING UNIT:
    ...     .with_coupling_unit(CouplingUnit.DOC)
    ...     .having_items_in_top(30)
    ...     .having_items_in(None)
    ...     .having_citation_threshold(0)
    ...     .having_occurrence_threshold(2)
    ...     #
    ...     # COUNTERS:
    ...     .using_counters(False)
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/scopus/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    ... )
    >>> df.head(5)
                                         DEGREE  BETWEENNESS  CLOSENESS  PAGERANK
    Bollaert, 2021, J CORP FINANC             4     0.026144   0.231481  0.089492
    Cai, 2018, ACCOUNT FINANC                 4     0.026144   0.231481  0.064559
    Gomber, 2017, J BUS ECON                  3     0.000000   0.198413  0.072873
    Haddad, 2019, BUS ECON                    3     0.000000   0.198413  0.046680
    Belanche, 2019, IND MANAG DATA SYST       2     0.006536   0.111111  0.076812


    >>> df = (
    ...     NetworkMetrics()
    ...     #
    ...     # COUPLING UNIT:
    ...     .with_coupling_unit(CouplingUnit.AUTH)
    ...     .having_items_in_top(30)
    ...     .having_items_in(None)
    ...     .having_citation_threshold(0)
    ...     .having_occurrence_threshold(2)
    ...     #
    ...     # COUNTERS:
    ...     .using_counters(True)
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/scopus/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    ... )
    >>> df.head(5)
                           DEGREE  BETWEENNESS  CLOSENESS  PAGERANK
    Li X. 003:00894            12     0.155263   0.625000  0.082741
    Jagtiani J. 005:01156      11     0.110526   0.592105  0.058820
    Luo S. 002:00670            9     0.034211   0.535714  0.060131
    Zhou G. 002:00670           9     0.034211   0.535714  0.060131
    Lee C.-C. 002:00717         8     0.000000   0.511364  0.053898


    >>> df = (
    ...     NetworkMetrics()
    ...     #
    ...     # COUPLING UNIT:
    ...     .with_coupling_unit(CouplingUnit.AUTH)
    ...     .having_items_in_top(30)
    ...     .having_items_in(None)
    ...     .having_citation_threshold(0)
    ...     .having_occurrence_threshold(2)
    ...     #
    ...     # COUNTERS:
    ...     .using_counters(False)
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/scopus/")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    ... )
    >>> df.head(5)
                 DEGREE  BETWEENNESS  CLOSENESS  PAGERANK
    Li X.            12     0.155263   0.625000  0.082741
    Jagtiani J.      11     0.110526   0.592105  0.058820
    Luo S.            9     0.034211   0.535714  0.060131
    Zhou G.           9     0.034211   0.535714  0.060131
    Lee C.-C.         8     0.000000   0.511364  0.053898


"""

from tm2p import CouplingUnit, ItemOrderBy
from tm2p._intern import ParamsMixin, remove_counters
from tm2p.synthes.netw.coupl._intern.doc import NetworkMetrics as DocNetworkMetrics
from tm2p.synthes.netw.coupl._intern.other import NetworkMetrics as OtherNetworkMetrics


class NetworkMetrics(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):

        if self.params.coupling_unit == CouplingUnit.DOC:
            Metrics = DocNetworkMetrics
        else:
            Metrics = OtherNetworkMetrics

        use_counters = self.params.counters
        self.params.counters = True

        df = (
            Metrics()
            .update(**self.params.__dict__)
            .update(items_order_by=ItemOrderBy.OCC)
            .run()
        )

        if use_counters is False:
            self.params.counters = False
            names = df.index.tolist()
            names = [remove_counters(name) for name in names]
            df.index = names

        return df
