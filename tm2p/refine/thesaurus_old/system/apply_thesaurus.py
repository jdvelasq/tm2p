"""
Apply Thesaurus
===============================================================================

Smoke tests:
    >>> import sys
    >>> from io import StringIO
    >>> from tm2p.refine.thesaurus_old.system import ApplyThesaurus

    >>> # Redirecting stderr to avoid messages
    >>> original_stderr = sys.stderr
    >>> sys.stderr = StringIO()

    >>> #  Creating, configuring, and running the system thesaurus
    >>> applier = (
    ...     ApplyThesaurus()
    ...     .with_thesaurus_file("geography/country_to_region.the.txt")
    ...     .with_field("countries")
    ...     .with_other_field("regions")
    ...     .where_root_directory("tests/fintech/")
    ... )
    >>> applier.run()

    >>> # Capture and print stderr output
    >>> output = sys.stderr.getvalue()
    >>> sys.stderr = original_stderr
    >>> print(output)
    INFO: Applying system thesaurus to database...
      Thesaurus    : ...2/package_data/thesaurus/geography/country_to_region.the.txt
      Source field : countries
      Target field : regions
      Application process completed successfully
    <BLANKLINE>

"""

import sys

from colorama import Fore

from tm2p._intern import ParamsMixin
from tm2p._intern.data_access import load_all_records_from_database, save_main_csv_zip
from tm2p.refine.thesaurus_old._intern import (
    ThesaurusMixin,
    internal__load_thesaurus_as_mapping,
)


class ApplyThesaurus(
    ParamsMixin,
    ThesaurusMixin,
):
    """:meta private:"""

    #
    # NOTIFICATIONS:
    # -------------------------------------------------------------------------
    def internal__notify_process_start(self):

        if not self.params.quiet:

            file_path = str(self.thesaurus_path)
            field = self.params.source_field
            other_field = self.params.index_field

            if len(file_path) > 64:
                file_path = "..." + file_path[-60:]

            if self.params.colored_stderr:
                filename = str(file_path).rsplit("/", maxsplit=1)[1]
                file_path = file_path.replace(filename, f"{Fore.RESET}{filename}")
                file_path = Fore.LIGHTBLACK_EX + file_path

            sys.stderr.write("INFO: Applying system thesaurus to database...\n")
            sys.stderr.write(f"  Thesaurus    : {file_path}\n")
            sys.stderr.write(f"  Source field : {field}\n")
            sys.stderr.write(f"  Target field : {other_field}\n")
            sys.stderr.flush()

    # -------------------------------------------------------------------------
    def internal__notify_process_end(self):

        if not self.params.quiet:

            sys.stderr.write("  Application process completed successfully\n")
            sys.stderr.flush()

    #
    # ALGORITHM:
    # -------------------------------------------------------------------------
    def _load_thesaurus_as_mapping(self):
        self.mapping = internal__load_thesaurus_as_mapping(self.thesaurus_path)
        self.mapping = {k: v[0].strip() for k, v in self.mapping.items()}

    # -------------------------------------------------------------------------
    def internal__load_records(self):
        self.records = load_all_records_from_database(params=self.params)

    # -------------------------------------------------------------------------
    def internal__copy_field(self):
        if self.params.source_field != self.params.index_field:
            self.records[self.params.index_field] = self.records[
                self.params.source_field
            ].copy()

    # -------------------------------------------------------------------------
    def internal__split_other_field(self):
        self.records[self.params.index_field] = self.records[
            self.params.index_field
        ].str.split("; ")

    # -------------------------------------------------------------------------
    def internal__apply_thesaurus_to_other_field(self):

        self.records[self.params.index_field] = self.records[
            self.params.index_field
        ].map(
            lambda x: [self.mapping.get(item, item) for item in x],
            na_action="ignore",
        )

    # -------------------------------------------------------------------------
    def internal__remove_duplicates_from_other_field(self):
        #
        def f(x):
            # remove duplicated terms preserving the order
            terms = []
            for term in x:
                if term not in terms:
                    terms.append(term)
            return terms

        self.records[self.params.index_field] = self.records[
            self.params.index_field
        ].map(f, na_action="ignore")

    # -------------------------------------------------------------------------
    def internal__join_record_values(self):
        self.records[self.params.index_field] = self.records[
            self.params.index_field
        ].str.join("; ")

    # -------------------------------------------------------------------------
    def internal__write_records(self):
        save_main_csv_zip(params=self.params, records=self.records)

    # -------------------------------------------------------------------------
    def run(self):
        """:meta private:"""

        self.internal__build_system_thesaurus_path()
        self.internal__notify_process_start()
        self._load_thesaurus_as_mapping()
        self.internal__load_records()
        self.internal__copy_field()
        self.internal__split_other_field()
        self.internal__apply_thesaurus_to_other_field()
        self.internal__remove_duplicates_from_other_field()
        self.internal__join_record_values()
        self.internal__write_records()
        self.internal__notify_process_end()


# =============================================================================
