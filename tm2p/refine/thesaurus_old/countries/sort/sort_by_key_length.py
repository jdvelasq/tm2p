"""
Sort by Key Length
===============================================================================


Smoke tests:
    >>> from tm2p.refine.thesaurus_old.countries import InitializeThesaurus
    >>> (
    ...     InitializeThesaurus()
    ...     .where_root_directory("tests/scopus/")
    ... ).run()


    >>> from tm2p.refine.thesaurus_old.countries import SortByKeyLength
    >>> (
    ...     SortByKeyLength()
    ...     .where_root_directory("tests/scopus/")
    ...     .run()
    ... )

    >>> from tm2p.refine.thesaurus_old.countries import PrintHeader
    >>> (
    ...     PrintHeader()
    ...     .using_colored_output(False)
    ...     .where_root_directory("tests/scopus/")
    ... ).run()
    Brunei Darussalam
      Universiti Brunei Darussalam, School of Business and Economics, Jln Tungk...
    United Kingdom
      Bristol Business School, University of the West of England, Bristol, Unit...
    United States
      Baylor University, United States; Columbia Graduate School of Business, U...
    Netherlands
      Erasmus University Rotterdam, Burgemeester Oudlaan, Rotterdam, 50, Nether...
    South Korea
      College of Business Administration, Soongsil University, South Korea; Dep...
    Switzerland
      Department of Informatics, University of Zurich, Binzmuehlestrasse 14, Zu...
    Kazakhstan
      Department of Accounting and Finance, Bang College of Business, KIMEP Uni...
    Australia
      Centre for Law, Markets & Regulation, UNSW Australia, Australia; Charles ...
    <BLANKLINE>



"""

from tm2p._intern import ParamsMixin
from tm2p.refine.thesaurus_old.user import SortByKeyLength as UserSortByKeyLength


class SortByKeyLength(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):
        return (
            UserSortByKeyLength()
            .update(**self.params.__dict__)
            .with_thesaurus_file("countries.the.txt")
            .run()
        )
