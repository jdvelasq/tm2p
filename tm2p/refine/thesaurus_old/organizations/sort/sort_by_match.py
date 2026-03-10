"""
Sort By Match
===============================================================================


Smoke tests:
    >>> # TEST PREPARATION
    >>> import sys
    >>> from io import StringIO
    >>> from tm2p.refine.thesaurus_old.organizations import InitializeThesaurus, SortByMatch

    >>> # Redirecting stderr to avoid messages
    >>> original_stderr = sys.stderr
    >>> sys.stderr = StringIO()

    >>> # Create thesaurus
    >>> InitializeThesaurus(root_directory="examples/fintech/", quiet=True).run()

    >>> # Create and run the sorter
    >>> sorter = (
    ...     SortByMatch()
    ...     #
    ...     # THESAURUS:
    ...     .having_text_matching("Sch")
    ...     .having_case_sensitive(False)
    ...     .having_regex_flags(0)
    ...     .having_regex_search(False)
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/scopus/")
    ... )
    >>> sorter.run()

    >>> # Capture and print stderr output
    >>> output = sys.stderr.getvalue()
    >>> sys.stderr = original_stderr
    >>> print(output)
    Sorting thesaurus by match...
                File : examples/fintech/data/thesaurus/organizations.the.txt
             Pattern : Sch
      Case sensitive : False
         Regex Flags : 0
        Regex Search : False
      12 matching keys found
      Sorting process completed successfully
    <BLANKLINE>
    Printing thesaurus header
      File : examples/fintech/data/thesaurus/organizations.the.txt
    <BLANKLINE>
        [UKN] CESifo, Poschingerstr. 5, Munich, 81679, Germany (DEU)
          CESifo, Poschingerstr. 5, Munich, 81679, Germany
        [UKN] Hochschule für Wirtschaft Fribourg, Switzerland (CHE)
          Hochschule für Wirtschaft Fribourg, Switzerland
        Columbia Grad Sch of Bus (USA)
          Columbia Graduate School of Business, United States
        Copenhagen Bus Sch (DNK)
          Copenhagen Business School, Department of IT Management, Howitzvej 60, Fr...
        Harvard Law Sch (USA)
          Harvard Law School, United States
        Henley Bus Sch (GBR)
          Henley Business School, United Kingdom
        Kingston Bus Sch (GBR)
          Kingston Business School, Department of Accounting, Finance and Informati...
        London Sch of Econ (GBR)
          London School of Economics, United Kingdom
    <BLANKLINE>
    <BLANKLINE>



"""

from tm2p._intern import ParamsMixin
from tm2p.refine.thesaurus_old.user import SortByMatch as UserSortByMatch


class SortByMatch(
    ParamsMixin,
):
    """:meta private:"""

    # -------------------------------------------------------------------------
    def run(self):
        return (
            UserSortByMatch()
            .update(**self.params.__dict__)
            .with_thesaurus_file("organizations.the.txt")
            .run()
        )


# ===============================================================================
