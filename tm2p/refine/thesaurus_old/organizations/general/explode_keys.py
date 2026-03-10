"""
Explode Keys
===============================================================================

Smoke tests:
    >>> import sys
    >>> from io import StringIO
    >>> from tm2p.refine.thesaurus_old.organizations import InitializeThesaurus, ExplodeKeys

    >>> # Redirect stderr to capture output
    >>> original_stderr = sys.stderr
    >>> sys.stderr = StringIO()

    >>> # Create thesaurus
    >>> InitializeThesaurus(root_directory="examples/fintech/", quiet=True).run()

    >>> # Explode thesaurus keys
    >>> ExplodeKeys().where_root_directory("examples/fintech/").run()

    >>> from tm2p.refine.thesaurus_old.organizations import PrintHeader
    >>> (
    ...     PrintHeader()
    ...     .using_colored_output(False)
    ...     .where_root_directory("tests/scopus/")
    ... ).run()

"""

from tm2p._intern import ParamsMixin
from tm2p.refine.thesaurus_old.user import ExplodeKeys as UserExplodeKeys


class ExplodeKeys(
    ParamsMixin,
):
    """:meta private:"""

    # -------------------------------------------------------------------------
    def run(self):
        return (
            UserExplodeKeys()
            .update(**self.params.__dict__)
            .update(
                thesaurus_file="organizations.the.txt",
                root_directory=self.params.root_directory,
            )
            .run()
        )


# =============================================================================
