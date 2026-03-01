"""
Thesaurus manipulation internals.

This module provides mixins for thesaurus operations including
loading, processing, and saving thesaurus data.
"""

import sys
from pathlib import Path
from typing import TYPE_CHECKING, Dict, TextIO

import pandas as pd
from colorama import Fore
from tqdm import tqdm  # type: ignore

from tm2p._intern.data_access import load_filtered_main_csv_zip
from tm2p.refine.thesaurus_old._intern import (
    internal__create_fingerprint,
    internal__get_system_thesaurus_file_path,
    internal__get_user_thesaurus_file_path,
    internal__load_reversed_thesaurus_as_mapping,
    internal__load_thesaurus_as_mapping,
)

if TYPE_CHECKING:
    from tm2p._intern import Params

tqdm.pandas()


# Add after imports (line ~32):
class ThesaurusError(Exception):
    """Base exception for thesaurus operations."""


class ThesaurusIOError(ThesaurusError):
    """I/O operation failed."""


class ThesaurusValidationError(ThesaurusError):
    """Validation failed."""


class ThesaurusMixin:

    # Expected from host class:
    params: "Params"

    # Set by this mixin (ADD THESE):
    thesaurus_path: Path
    data_frame: pd.DataFrame
    mapping: Dict[str, str]
    filtered_records: pd.DataFrame
    n_initial_keys: int
    n_final_keys: int

    # -------------------------------------------------------------------------
    def _build_user_thesaurus_path(self) -> None:

        self.thesaurus_path = internal__get_user_thesaurus_file_path(params=self.params)

    # -------------------------------------------------------------------------
    def internal__build_system_thesaurus_path(self) -> None:

        self.thesaurus_path = Path(
            internal__get_system_thesaurus_file_path(
                thesaurus_file=self.params.thesaurus_file
            )
        )

    # -------------------------------------------------------------------------
    def internal__create_thesaurus_data_frame_from_field(self) -> None:

        keys = self.filtered_records[self.params.source_field].dropna()
        keys = keys.str.split("; ")
        keys = keys.explode()
        keys = keys.str.strip()
        keys = keys.drop_duplicates()

        data_frame = pd.DataFrame(
            {
                "key": keys.to_list(),
                "value": keys.to_list(),
            }
        )

        self.data_frame = data_frame

    # -------------------------------------------------------------------------
    def internal__explode_and_group_values_by_key(self) -> None:

        self.data_frame["value"] = self.data_frame["value"].str.split("; ")
        self.data_frame = self.data_frame.explode("value")
        self.data_frame["value"] = self.data_frame["value"].str.strip()

        if "__row_selected__" in self.data_frame.columns.tolist():
            self.data_frame = self.data_frame.groupby("key", as_index=False).agg(
                {"value": list, "__row_selected__": list}
            )
        else:
            self.data_frame = self.data_frame.groupby("key", as_index=False).agg(
                {"value": list}
            )

        self.data_frame["value"] = self.data_frame["value"].map(
            lambda x: sorted(set(x))
        )
        self.data_frame["value"] = self.data_frame["value"].str.join("; ")

        if "__row_selected__" in self.data_frame.columns.tolist():
            self.data_frame["__row_selected__"] = self.data_frame[
                "__row_selected__"
            ].map(any)

        self.data_frame = self.data_frame.reset_index(drop=True)

    # -------------------------------------------------------------------------
    def internal__load_filtered_records(self) -> None:

        self.filtered_records = load_filtered_main_csv_zip(params=self.params)

    # -------------------------------------------------------------------------
    def internal__load_reversed_thesaurus_as_mapping(self) -> None:
        self.mapping = internal__load_reversed_thesaurus_as_mapping(
            str(self.thesaurus_path)
        )

    # -------------------------------------------------------------------------
    def _load_thesaurus_as_mapping(self) -> None:
        mapping = internal__load_thesaurus_as_mapping(str(self.thesaurus_path))
        self.mapping = {key: "; ".join(value) for key, value in mapping.items()}

    # -------------------------------------------------------------------------
    def internal__reduce_keys(self) -> None:

        # initial number of keys:
        self.n_initial_keys = len(self.data_frame)

        # Based on the basic TheVantagePoint algorithm to group terms
        data_frame = self.data_frame.copy()
        data_frame["fingerprint"] = data_frame["key"].apply(
            internal__create_fingerprint
        )

        # preserve the key with the largest number of values
        data_frame["count"] = data_frame["value"].map(lambda x: len(x.split("; ")))
        data_frame = data_frame.sort_values(
            by=["fingerprint", "count", "key"], ascending=False
        )

        # mapping
        mapping_df = data_frame[["key", "fingerprint"]].copy()
        mapping_df = mapping_df.drop_duplicates()
        mapping_df = mapping_df.set_index("fingerprint")
        mapping = mapping_df["key"].to_dict()

        data_frame["key"] = data_frame["fingerprint"].apply(lambda x: mapping[x])
        data_frame = data_frame[["key", "value"]].copy()

        if "__row_selected__" in self.data_frame.columns.tolist():
            groupby = (
                self.data_frame[["key", "__row_selected__"]]
                .groupby("key")
                .agg({"__row_selected__": list})
            )
            groupby["__row_selected__"] = groupby["__row_selected__"].map(any)
            groupby_dict = groupby["__row_selected__"].to_dict()
            data_frame["__row_selected__"] = data_frame["key"].map(
                lambda x: groupby_dict[x]
            )

        self.data_frame = data_frame

    # -------------------------------------------------------------------------
    def internal__set_initial_keys(self) -> None:
        self.initial_keys = set(self.data_frame.key.to_list())

    # -------------------------------------------------------------------------
    def internal__set_final_keys(self) -> None:
        self.final_keys = set(self.data_frame.key.to_list())

    # -------------------------------------------------------------------------
    def internal__compute_changed_keys(self) -> None:

        set_a = self.initial_keys
        set_b = self.final_keys

        added = set_b - set_a
        removed = set_a - set_b

        len_added = len(added)
        len_removed = len(removed)

        self.total_key_changes = len_added + len_removed

    # -------------------------------------------------------------------------
    def internal__print_thesaurus_header_to_stream(
        self, n: int, stream: TextIO
    ) -> None:

        max_key_display = 80
        max_value_display = 76
        key_truncate_at = 77
        value_truncate_at = 73

        if self.params.quiet:
            return

        thesaurus_path = self.thesaurus_path
        colored_stderr = self.params.colored_stderr
        colored_output = self.params.colored_output
        data_frame = self.data_frame.head(n).copy()

        data_frame["key"] = data_frame["key"].map(
            lambda x: x[:key_truncate_at] + "..." if len(x) > max_key_display else x
        )
        data_frame["value"] = data_frame["value"].map(
            lambda x: x[:value_truncate_at] + "..." if len(x) > max_value_display else x
        )

        msg = f"INFO: Printing thesaurus header\n  Reading {thesaurus_path}\n\n"
        if colored_stderr:
            filename = str(thesaurus_path).rsplit("/", maxsplit=1)[1]
            msg = msg.replace("File :", f"{Fore.LIGHTBLACK_EX}File :")
            msg = msg.replace(filename, f"{Fore.RESET}{filename}")
        sys.stderr.write(msg)
        sys.stderr.flush()

        for _, row in data_frame.iterrows():
            stream.write(f"{row.key}\n")
            if (stream == sys.stdout and colored_output) or (
                stream == sys.stderr and colored_stderr
            ):
                stream.write(f"  {Fore.LIGHTBLACK_EX}{row.value}{Fore.RESET}\n")
            else:
                stream.write(f"  {row.value}\n")
        stream.write("\n")
        stream.flush()

    # -------------------------------------------------------------------------
    def _sort_data_frame_by_rows_and_key(self) -> None:

        self.data_frame["lower_key"] = (
            self.data_frame["key"].str.lower().str.replace("_", " ")
        )

        if "__row_selected__" in self.data_frame.columns:
            self.data_frame = self.data_frame.sort_values(
                ["__row_selected__", "lower_key"], ascending=[False, True]
            )
        else:
            self.data_frame = self.data_frame.sort_values("lower_key")

        self.data_frame = self.data_frame.drop(columns=["lower_key"])
        self.data_frame = self.data_frame[
            self.data_frame.key.fillna("").str.strip() != ""
        ]

    # -------------------------------------------------------------------------
    def _transform_mapping_to_data_frame(self) -> None:

        keys = list(self.mapping.keys())
        values = list(self.mapping.values())
        self.data_frame = pd.DataFrame({"key": keys, "value": values})

    # -------------------------------------------------------------------------
    def _write_thesaurus_data_frame_to_disk(self) -> None:

        if not hasattr(self, "data_frame"):
            raise ThesaurusValidationError("data_frame not initialized")

        if self.data_frame.empty:
            raise ThesaurusValidationError("Cannot write empty thesaurus")

        try:
            self.thesaurus_path.parent.mkdir(parents=True, exist_ok=True)
        except PermissionError as e:
            raise ThesaurusIOError(
                f"The parent directory {self.thesaurus_path.parent} not exists: {e}"
            ) from e

        try:
            with open(self.thesaurus_path, "w", encoding="utf-8") as file:
                for _, row in self.data_frame.iterrows():
                    file.write(row.key + "\n")
                    for value in row.value.split("; "):
                        file.write(f"    {value}\n")
        except PermissionError as e:
            raise ThesaurusIOError(
                f"The thesaurus file {self.thesaurus_path} cannot be opened: {e}"
            ) from e

        except OSError as e:
            raise ThesaurusIOError(f"Failed to write thesaurus: {e}") from e


# =============================================================================
