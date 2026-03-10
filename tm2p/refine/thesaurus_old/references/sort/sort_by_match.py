"""
Sort by Key Match
===============================================================================

Finds a string in the terms of a thesaurus.

Smoke tests:
    >>> import sys
    >>> from io import StringIO
    >>> from tm2p.refine.thesaurus_old.references import InitializeThesaurus, SortByMatch

    >>> # Redirecting stderr to avoid messages
    >>> original_stderr = sys.stderr
    >>> sys.stderr = StringIO()

    >>> # Create, configure, and run the sorter
    >>> sorter = (
    ...     SortByMatch()
    ...     .having_text_matching("ECON")
    ...     .where_root_directory("tests/scopus/")
    ... )
    >>> sorter.run()

    >>> # Capture and print stderr output
    >>> output = sys.stderr.getvalue()
    >>> sys.stderr = original_stderr
    >>> print(output)
    Sorting thesaurus by match...
                File : examples/fintech/data/thesaurus/references.the.txt
             Pattern : ECON
      Case sensitive : False
         Regex Flags : 0
        Regex Search : False
      7 matching keys found
      Sorting process completed successfully
    <BLANKLINE>
    Printing thesaurus header
      File : examples/fintech/data/thesaurus/references.the.txt
    <BLANKLINE>
        Anagnostopoulos I., 2018, J ECON BUS, V100, P7
          Anagnostopoulos, Ioannis, FinTech and RegTech: Impact on regulators and b...
        Buchak G., 2018, J FINANC ECON, V130, P453
          Buchak G., Matvos G., Piskorski T., Seru A., Fintech, regulatory arbitrag...
        Chen L., 2016, CHINA ECON J, V9, P225
          Chen L., From Fintech to Finlife: The case of Fintech development in Chin...
        Gabor D., 2017, NEW POLIT ECON, V22, P423
          Gabor D., Brooks S., The Digital Revolution in Financial Inclusion: Inter...
        Gomber P., 2017, J BUS ECON, V87, P537
          Gomber P., Koch J., Siering M., Digital finance and fintech: current rese...
        Haddad C., 2019, SMALL BUS ECON, V53, P81
          Haddad C., Hornuf L., The emergence of the global fintech market: Economi...
        Jagtiani J., 2018, J ECON BUS, V100, P43
          Jagtiani J., Catharine L., Do fintech lenders penetrate areas that are un...
        Alt R., 2018, ELECTRON MARK, V28, P235
          Alt R., Beck R., Smits M.T., Fintech and the Transformation of the Financ...
    <BLANKLINE>
    <BLANKLINE>





"""

from tm2p._intern import ParamsMixin
from tm2p.refine.thesaurus_old.user import SortByMatch as UserSortByMatch


class SortByMatch(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):
        return (
            UserSortByMatch()
            .update(**self.params.__dict__)
            .with_thesaurus_file("references.the.txt")
            .run()
        )
