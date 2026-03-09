"""
Apply Thesaurus
===============================================================================


Smoke tests:
    >>> import sys
    >>> from io import StringIO
    >>> from tm2p.refine.thesaurus_old.references import ApplyThesaurus

    >>> # Redirecting stderr to avoid messages
    >>> original_stderr = sys.stderr
    >>> sys.stderr = StringIO()

    >>> # Applying thesaurus
    >>> ApplyThesaurus(root_directory="examples/fintech/").run()

    >>> # Capture and print stderr output
    >>> output = sys.stderr.getvalue()
    >>> sys.stderr = original_stderr
    >>> print(output)
    Applying user thesaurus to database
              File : examples/fintech/data/thesaurus/references.the.txt
      Source field : raw_global_references
      Target field : global_references
      Application process completed successfully
    <BLANKLINE>
    <BLANKLINE>



"""

import pathlib
import sys

import pandas as pd

from tm2p._intern import ParamsMixin
from tm2p._intern.data_access import save_main_csv_zip


#
#
class ApplyThesaurus(
    ParamsMixin,
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

            sys.stderr.write("INFO: Applying user thesaurus to database\n")
            sys.stderr.write(f"  File         : {file_path}\n")
            sys.stderr.write(f"  Source field : {field}\n")
            sys.stderr.write(f"  Target field : {other_field}\n")
            sys.stderr.flush()

    # -------------------------------------------------------------------------
    def internal__notify_process_end(self):

        if not self.params.quiet:

            sys.stderr.write(f"  Application process completed successfully\n")
            sys.stderr.flush()

    #
    # ALGORITHM:
    # -------------------------------------------------------------------------
    def internal__load_records(self):
        self.records = load_all_records_from_database(params=self.params)

    # -------------------------------------------------------------------------
    def internal__apply_thesaurus(self):

        field = self.params.source_field
        other_field = self.params.index_field

        # creates a list of references
        self.records[other_field] = self.records[field].str.split("; ")

        # replace the oriignal references by the record_id
        self.records[other_field] = self.records[other_field].map(
            lambda x: [self.mapping[t] for t in x if t in self.mapping.keys()],
            na_action="ignore",
        )
        self.records[other_field] = self.records[other_field].map(
            lambda x: pd.NA if x == [] else x, na_action="ignore"
        )
        self.records[other_field] = self.records[other_field].map(
            lambda x: "; ".join(sorted(x)) if isinstance(x, list) else x
        )

    # -------------------------------------------------------------------------
    def internal__write_records_to_file(self):
        save_main_csv_zip(params=self.params, records=self.records)

    # -------------------------------------------------------------------------
    def run(self):

        self.params.thesaurus_file = "references.the.txt"
        self.params.source_field = "raw_global_references"
        self.params.index_field = "global_references"

        self._build_user_thesaurus_path()
        self.internal__notify_process_start()
        self.internal__load_reversed_thesaurus_as_mapping()
        self.internal__load_records()
        self.internal__apply_thesaurus()
        self.internal__write_records_to_file()
        self.internal__notify_process_end()
