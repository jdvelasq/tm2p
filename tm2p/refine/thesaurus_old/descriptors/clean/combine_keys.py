"""
Combine Keys
===============================================================================

Smoke tests:
    >>> # Preparation
    >>> from tm2p.refine.thesaurus_old.descriptors import InitializeThesaurus
    >>> from tm2p.refine.thesaurus_old.descriptors import ApplyThesaurus
    >>> InitializeThesaurus(root_directory="examples/fintech/", quiet=True).run()
    >>> ApplyThesaurus(root_directory="examples/fintech/", quiet=True).run()

    >>> # Use
    >>> from tm2p.refine.thesaurus_old.descriptors import CombineKeys
    >>> df = (
    ...     CombineKeys()
    ...     #
    ...     # FIELD:
    ...     .with_field_pattern('FINTECH')
    ...     .having_items_in_top(30)
    ...     .having_items_ordered_by("OCC")
    ...     .having_item_occurrences_between(2, None)
    ...     .having_item_citations_between(None, None)
    ...     .having_items_in(None)
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/scopus/")
    ...     .where_database("main")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    ... )
    >>> df.head()  # doctest: +SKIP
           rows                 columns  probability combine?
    3   FINTECH            TECHNOLOGIES        0.316       no
    6   FINTECH  FINANCIAL_TECHNOLOGIES        0.289       no
    8   FINTECH  THE_FINANCIAL_INDUSTRY        0.237       no
    13  FINTECH              REGULATORS        0.211       no
    23  FINTECH                   BANKS        0.184       no



"""

from tm2p._intern import ParamsMixin
from tm2p.refine.thesaurus_old.user import CombineKeys as UserCombineKeys


class CombineKeys(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):

        return (
            UserCombineKeys()
            .update(**self.params.__dict__)
            .with_source_field("descriptors")
            .run()
        )
