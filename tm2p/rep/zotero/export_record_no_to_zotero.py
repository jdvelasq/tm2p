"""
Export Record No to Zotero
=======================================================================================

Smoke tests:
    >>> from tm2p.zotero import ExportRecordNoToZotero
    >>> zot = (
    ...     ExportRecordNoToZotero()
    ...     .using_zotero_api_key("MifzqqRsPK5OHvmNoW4Y9Zre")  # https://www.zotero.org/settings/keys/new
    ...     .using_zotero_library_id(5242364)   # https://www.zotero.org/groups/5242364/fintech-scopus
    ...     .using_zotero_library_type("group")  # "user" or "group"
    ...     .where_root_directory("tests/fintech/")
    ... ).run() # doctest: +ELLIPSIS +SKIP

"""

import pathlib
import sys

import pandas as pd
from colorama import Fore, init
from pyzotero import zotero
from tqdm import tqdm  # type: ignore

from tm2p._intern import ParamsMixin


class ExportRecordNoToZotero(ParamsMixin):
    """:meta private:"""

    #
    # NOTIFICATIONS:
    # -------------------------------------------------------------------------
    def internal__notify_process_start(self):

        if not self.params.quiet:

            sys.stderr.write("Updating Zotero web library...\n")
            sys.stderr.flush()

    # -------------------------------------------------------------------------
    def internal__notify_process_end(self):

        if not self.params.quiet:

            sys.stderr.write("  Updating process completed successfully\n\n")
            sys.stderr.flush()

    #
    # ALGORITHM:
    # -------------------------------------------------------------------------
    def internal__connet_to_zotero(self):
        self.zot = zotero.Zotero(
            self.params.zotero_library_id,
            self.params.zotero_library_type,
            self.params.zotero_api_key,
        )

    # -------------------------------------------------------------------------
    def internal__load_records(self):
        self.records = load_all_records_from_database(params=self.params)

    # -------------------------------------------------------------------------
    def internal__update_zotero(self):

        logs = []

        for _, record in tqdm(
            self.records.iterrows(),
            total=len(self.records),
            desc="       Progress ",
            disable=self.params.tqdm_disable,
            ncols=80,
        ):
            title = record["raw_document_title"]
            record_no = record["record_no"]
            authors = record["raw_authors"]
            year = record["year"]

            ut_code = f"{self.params.zotero_library_id}@{record_no}"

            zotero_items = self.zot.items(q=title)

            if len(zotero_items) == 1:
                updated_item = zotero_items[0]
                updated_item["data"]["shortTitle"] = ut_code
                self.zot.update_item(updated_item)
            else:

                if pd.isna(year) or pd.isna(authors):
                    logs.append((record_no, title))
                    continue

                is_ok = False
                for item in zotero_items:
                    if (
                        str(year) in item["data"]["date"]
                        and item["data"]["creators"][0]["lastName"].lower()
                        in authors.lower()
                    ):
                        updated_item = zotero_items[0]
                        updated_item["data"]["shortTitle"] = ut_code
                        self.zot.update_item(updated_item)
                        is_ok = True
                        break

                if not is_ok:
                    logs.append((record_no, title))

        if len(logs) != 0:
            sys.stderr.write("  Some records were not updated in Zotero\n")
            sys.stderr.flush()

            filepath = pathlib.Path(self.params.root_directory) / "zotero.log"

            with open(filepath, "w") as f:
                for record_no, title in logs:
                    f.write(f"{record_no}\n")
                    f.write(f"    {title}\n")

    # -------------------------------------------------------------------------
    def run(self):

        self.internal__notify_process_start()
        self.internal__connet_to_zotero()
        self.internal__load_records()
        self.internal__update_zotero()
        self.internal__notify_process_end()
