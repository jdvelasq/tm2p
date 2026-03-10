"""
Apply Thesaurus
===============================================================================

Smoke tests:
    >>> from tm2p.refine.thesaurus_old.countries import InitializeThesaurus
    >>> (
    ...     InitializeThesaurus()
    ...     .where_root_directory("tests/scopus/")
    ... ).run()

    >>> from tm2p.refine.thesaurus_old.countries import ApplyThesaurus
    >>> ApplyThesaurus().where_root_directory("examples/fintech/").run()

    >>> from tm2p.io import Query
    >>> result = Query(
    ...     query_expression="SELECT countries FROM database LIMIT 10;",
    ...     root_directory="examples/fintech/",
    ...     database="main",
    ...     record_years_range=(None, None),
    ...     record_citations_range=(None, None),
    ... ).run()
    >>> print(result)
                       countries
    0                South Korea
    1                South Korea
    2                      China
    3                     Latvia
    4             United Kingdom
    5       United States; China
    6                Switzerland
    7  Australia; Denmark; China
    8                Switzerland
    9                    Germany

    >>> result = Query(
    ...     query_expression="SELECT regions FROM database LIMIT 10;",
    ...     root_directory="examples/fintech/",
    ...     database="main",
    ...     record_years_range=(None, None),
    ...     record_citations_range=(None, None),
    ... ).run()
    >>> print(result)
                     regions
    0                   Asia
    1                   Asia
    2                   Asia
    3                 Europe
    4                 Europe
    5         Americas; Asia
    6                 Europe
    7  Oceania; Europe; Asia
    8                 Europe
    9                 Europe

    >>> result = Query(
    ...     query_expression="SELECT subregions FROM database LIMIT 10;",
    ...     root_directory="examples/fintech/",
    ...     database="main",
    ...     record_years_range=(None, None),
    ...     record_citations_range=(None, None),
    ... ).run()
    >>> print(result)
                                              subregions
    0                                       Eastern Asia
    1                                       Eastern Asia
    2                                       Eastern Asia
    3                                    Northern Europe
    4                                    Northern Europe
    5                     Northern America; Eastern Asia
    6                                     Western Europe
    7  Australia and New Zealand; Northern Europe; Ea...
    8                                     Western Europe
    9                                     Western Europe


"""

from tm2p._intern import ParamsMixin
from tm2p.refine.thesaurus_old._intern import internal__transform
from tm2p.refine.thesaurus_old.system import ApplyThesaurus as ApplySystemThesaurus
from tm2p.refine.thesaurus_old.user import ApplyThesaurus as ApplyUserThesaurus


class ApplyThesaurus(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):

        # Affiliations to countries mmapping
        ApplyUserThesaurus().update(**self.params.__dict__).update(
            thesaurus_file="countries.the.txt",
            field="affiliations",
            other_field="countries",
            root_directory=self.params.root_directory,
            quiet=self.params.quiet,
        ).run()

        # Country of first author
        internal__transform(
            #
            # FIELD:
            field="countries",
            other_field="country_1st_author",
            function=lambda x: x.str.split("; ").str[0],
            root_dir=self.params.root_directory,
        )

        # Country to region mapping
        ApplySystemThesaurus().update(**self.params.__dict__).update(
            thesaurus_file="geography/country_to_region.the.txt",
            field="countries",
            other_field="regions",
            root_directory=self.params.root_directory,
            quiet=self.params.quiet,
        ).run()

        # Country to subregion mapping
        ApplySystemThesaurus().update(**self.params.__dict__).update(
            thesaurus_file="geography/country_to_subregion.the.txt",
            field="countries",
            other_field="subregions",
            root_directory=self.params.root_directory,
            quiet=self.params.quiet,
        ).run()
