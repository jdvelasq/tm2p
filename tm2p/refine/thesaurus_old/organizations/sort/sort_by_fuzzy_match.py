"""
Sort by Fuzzy Match
===============================================================================


Smoke tests:
    >>> import sys
    >>> from io import StringIO
    >>> from tm2p.refine.thesaurus_old.organizations import InitializeThesaurus, SortByFuzzyMatch

    >>> # Redirecting stderr to avoid messages
    >>> original_stderr = sys.stderr
    >>> sys.stderr = StringIO()

    >>> # Create thesaurus
    >>> InitializeThesaurus(root_directory="examples/fintech/", quiet=True).run()

    >>> # Create and run the sorter
    >>> sorter = (
    ...     SortByFuzzyMatch()
    ...     #
    ...     # THESAURUS:
    ...     .having_text_matching("Texas")
    ...     .using_match_threshold(70)
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/scopus/")
    ... )
    >>> sorter.run()

    >>> # Capture and print stderr output
    >>> output = sys.stderr.getvalue()
    >>> sys.stderr = original_stderr
    >>> print(output)
    Sorting thesaurus by fuzzy match...
                File : examples/fintech/data/thesaurus/organizations.the.txt
           Keys like : Texas
      Match thresold : 70
      3 matching keys found
      Sorting process completed successfully
    <BLANKLINE>
    Printing thesaurus header
      File : examples/fintech/data/thesaurus/organizations.the.txt
    <BLANKLINE>
        Texas AandM Univ Sch of Law (USA)
          Texas AandM University School of Law, United States
        Univ of North Texas (USA)
          Department of Information Technology & Decision Sciences, University of N...
        Univ of Texas at Austin (USA)
          McCombs School of Business, University of Texas at Austin, United States
        [UKN] Brussels, Belgium (BEL)
          Brussels, Belgium
        [UKN] CESifo, Poschingerstr. 5, Munich, 81679, Germany (DEU)
          CESifo, Poschingerstr. 5, Munich, 81679, Germany
        [UKN] FinTech HK, Hong Kong (HKG)
          FinTech HK, Hong Kong
        [UKN] Hochschule für Wirtschaft Fribourg, Switzerland (CHE)
          Hochschule für Wirtschaft Fribourg, Switzerland
        [UKN] Information Technol, Univeril, Germany (DEU)
          Information Technology, Univeril, Germany
    <BLANKLINE>
    <BLANKLINE>


"""

from tm2p._intern import ParamsMixin
from tm2p.refine.thesaurus_old.user import SortByFuzzyMatch as UserSortByFuzzyMatch


class SortByFuzzyMatch(
    ParamsMixin,
):
    """:meta private:"""

    # -------------------------------------------------------------------------
    def run(self):
        return (
            UserSortByFuzzyMatch()
            .update(**self.params.__dict__)
            .with_thesaurus_file("organizations.the.txt")
            .run()
        )


# =============================================================================
