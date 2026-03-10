"""
Sort by Fuzzy Match
===============================================================================

Smoke tests:
    >>> import sys
    >>> from io import StringIO
    >>> from tm2p.refine.thesaurus_old.references import InitializeThesaurus, SortByFuzzyMatch

    >>> # Redirecting stderr to avoid messages
    >>> original_stderr = sys.stderr
    >>> sys.stderr = StringIO()

    >>> # Create the thesaurus
    >>> InitializeThesaurus(root_directory = "examples/fintech/", quiet=True, tqdm_disable=True).run()

    >>> # Create, configure, and run the sorter
    >>> sorter = (
    ...     SortByFuzzyMatch()
    ...     .having_text_matching("ACCOU")
    ...     .using_match_threshold(50)
    ...     .where_root_directory("tests/scopus/")
    ... )
    >>> sorter.run()

    >>> # Capture and print stderr output
    >>> output = sys.stderr.getvalue()
    >>> sys.stderr = original_stderr
    >>> print(output)
    Sorting thesaurus by fuzzy match...
                File : examples/fintech/data/thesaurus/references.the.txt
           Keys like : ACCOU
      Match thresold : 50
      2 matching keys found
      Sorting process completed successfully
    <BLANKLINE>
    Printing thesaurus header
      File : examples/fintech/data/thesaurus/references.the.txt
    <BLANKLINE>
        Cai C.W., 2018, ACCOUNT FINANC, V58, P965
          Cai C.W., Disruption of financial intermediation by FinTech: A review on ...
        Chen L., 2016, CHINA ECON J, V9, P225
          Chen L., From Fintech to Finlife: The case of Fintech development in Chin...
        Alt R., 2018, ELECTRON MARK, V28, P235
          Alt R., Beck R., Smits M.T., Fintech and the Transformation of the Financ...
        Anagnostopoulos I., 2018, J ECON BUS, V100, P7
          Anagnostopoulos, Ioannis, FinTech and RegTech: Impact on regulators and b...
        Arner D.W., 2017, NORTHWEST J INTL LAW BUS, V37, P373
          Arner D.W., Barberis J., Buckley R.P., Fintech, regtech, and the reconcep...
        Buchak G., 2018, J FINANC ECON, V130, P453
          Buchak G., Matvos G., Piskorski T., Seru A., Fintech, regulatory arbitrag...
        Dorfleitner G., 2017, FINTECH IN GER, P1
          Dorfleitner G., Hornuf L., Schmitt M., Weber M., FinTech in Germany, (2017)
        Gabor D., 2017, NEW POLIT ECON, V22, P423
          Gabor D., Brooks S., The Digital Revolution in Financial Inclusion: Inter...
    <BLANKLINE>
    <BLANKLINE>


"""

from tm2p._intern import ParamsMixin
from tm2p.refine.thesaurus_old.user import SortByFuzzyMatch as UserSortByFuzzyMatch


class SortByFuzzyMatch(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):
        return (
            UserSortByFuzzyMatch()
            .update(**self.params.__dict__)
            .with_thesaurus_file("references.the.txt")
            .run()
        )
