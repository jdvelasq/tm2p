"""
Count References
===============================================================================

Smoke tests:

    >>> from tm2p.manuscript import CountReferences
    >>> (
    ...     CountReferences()
    ...     .where_root_directory("tests/scopus/")
    ...     .run()
    ... )



"""

import glob
import os
import re

from tm2p._intern import ParamsMixin


class CountReferences(
    ParamsMixin,
):
    """:meta private:"""

    # -------------------------------------------------------------------------
    def internal__load_first_paragraph(self):

        filepath = os.path.join(
            self.params.root_directory,
            "outputs",
            "section_1_introduction",
            "first_paragraph.txt",
        )

        with open(filepath, "r", encoding="utf-8") as f:
            self.first_paragraph = f.read()

    # -------------------------------------------------------------------------
    def internal__load_second_paragraph(self):

        filepath = os.path.join(
            self.params.root_directory,
            "outputs",
            "section_1_introduction",
            "second_paragraph.txt",
        )

        with open(filepath, "r", encoding="utf-8") as f:
            self.second_paragraph = f.read()

    # -------------------------------------------------------------------------
    def internal__load_cluster_full_summaries(self):

        files = glob.glob(
            os.path.join(
                self.params.root_directory,
                "outputs",
                "section_5_discussion",
                "*full_summary.txt",
            )
        )

        cluster_descriptions = []
        for file in sorted(files):
            with open(file, encoding="utf-8") as f:
                text = f.read().strip()
                text += "\n\n"
                cluster_descriptions.append(text)

        self.cluster_full_summaries = "\n\n".join(cluster_descriptions)

    # -------------------------------------------------------------------------
    def internal__aggregate_texts(self):

        texts = [
            self.first_paragraph,
            self.second_paragraph,
            self.cluster_full_summaries,
        ]

        self.text = "\n\n".join(texts)

    # -------------------------------------------------------------------------
    def internal__extract_ut_from_text(self):

        pattern = r"\[([^\]]+)\]"

        matches = re.findall(pattern, self.text)
        uts = []
        for match in matches:
            parts = re.split(r"[;,]\s*", match)
            uts.extend(parts)

        self.uts = sorted(ut.strip() for ut in uts if ut.strip().startswith("UT "))

    # -------------------------------------------------------------------------
    def internal__count_appearances(self):

        self.ut_counts = {}
        for ut in self.uts:
            if ut in self.ut_counts:
                self.ut_counts[ut] += 1
            else:
                self.ut_counts[ut] = 1

    # -------------------------------------------------------------------------
    def internal__save_counts(self):

        # sort the UTs by their counts in descending order
        sorted_ut_counts = dict(
            sorted(self.ut_counts.items(), key=lambda item: item[1], reverse=True)
        )

        dirpath = os.path.join(
            self.params.root_directory, "outputs", "section_8_references"
        )

        if not os.path.exists(dirpath):
            os.makedirs(dirpath)

        output_filepath = os.path.join(
            dirpath,
            "reference_counts.txt",
        )

        with open(output_filepath, "w", encoding="utf-8") as f:
            for ut, count in sorted_ut_counts.items():
                f.write(f"{ut}\t{count}\n")

    # -------------------------------------------------------------------------
    def run(self):

        self.internal__load_first_paragraph()
        self.internal__load_second_paragraph()
        self.internal__load_cluster_full_summaries()
        self.internal__aggregate_texts()
        self.internal__extract_ut_from_text()
        self.internal__count_appearances()
        self.internal__save_counts()
