"""
Print Header
===============================================================================


Smoke tests:
    >>> # Reset the thesaurus to initial state
    >>> from tm2p.refine.thesaurus_old.user import InitializeThesaurus
    >>> (
    ...     InitializeThesaurus(quit=True)
    ...     .with_thesaurus_file("demo.the.txt")
    ...     .with_field("raw_descriptors")
    ...     .where_root_directory("tests/scopus/")
    ... ).run()

    >>> from tm2p.refine.thesaurus_old.user import PrintHeader
    >>> (
    ...     PrintHeader()
    ...     .with_thesaurus_file("demo.the.txt")
    ...     .using_colored_output(False)
    ...     .where_root_directory("tests/scopus/")
    ... ).run()





"""

import sys

from tm2p._intern import ParamsMixin
from tm2p.refine.thesaurus_old._intern import ThesaurusMixin
from tm2p.refine.thesaurus_old._intern.load_thesaurus_as_data_frame import (
    internal__load_thesaurus_as_data_frame,
)


class PrintHeader(
    ParamsMixin,
    ThesaurusMixin,
):
    def internal__load_thesaurus_as_data_frame(self):
        self.data_frame = internal__load_thesaurus_as_data_frame(
            file_path=self.thesaurus_path,
        )

    def run(self):

        self._build_user_thesaurus_path()
        self.internal__load_thesaurus_as_data_frame()
        self.internal__print_thesaurus_header_to_stream(n=8, stream=sys.stdout)


# =============================================================================
