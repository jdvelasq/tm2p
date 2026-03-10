"""
Explode Keys
===============================================================================

Smoke tests:
    >>> from tm2p.refine.thesaurus_old.countries import InitializeThesaurus
    >>> (
    ...     InitializeThesaurus()
    ...     .where_root_directory("tests/scopus/")
    ... ).run()


    >>> from tm2p.refine.thesaurus_old.countries import ExplodeKeys
    >>> ExplodeKeys().where_root_directory("examples/fintech/").run()

    >>> from tm2p.refine.thesaurus_old.countries import PrintHeader
    >>> (
    ...     PrintHeader()
    ...     .using_colored_output(False)
    ...     .where_root_directory("tests/scopus/")
    ... ).run()
    Australia
      Centre for Law, Markets & Regulation, UNSW Australia, Australia; Charles ...
    Belgium
      Brussels, Belgium
    Brunei Darussalam
      Universiti Brunei Darussalam, School of Business and Economics, Jln Tungk...
    China
      The Research center of information technology & economic and social devel...
    Denmark
      Copenhagen Business School, Department of IT Management, Howitzvej 60, Fr...
    France
      SKEMA Business School, Lille, France; University of Lille Nord de France,...
    Germany
      Leipzig University, Leipzig, Germany; University of Trier, Trier, Germany...
    Ghana
      University of the Free State and University of Ghana Business School, Uni...
    <BLANKLINE>



"""

from tm2p._intern import ParamsMixin
from tm2p.refine.thesaurus_old.user import ExplodeKeys as UserExplodeKeys


class ExplodeKeys(
    ParamsMixin,
):
    """:meta private:"""

    # -------------------------------------------------------------------------
    def run(self):
        (
            UserExplodeKeys()
            .update(**self.params.__dict__)
            .update(
                thesaurus_file="countries.the.txt",
                root_directory=self.params.root_directory,
            )
            .run()
        )


# =============================================================================
