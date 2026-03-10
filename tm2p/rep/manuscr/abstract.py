"""
Abstract
===============================================================================

Smoke tests:

    >>> from tm2p.manuscript import Abstract
    >>> (
    ...     Abstract()
    ...     #
    ...     # TEXT:
    ...     .with_core_area("fintech")
    ...     .with_word_length(200)
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/scopus/")
    ...     #
    ...     .run()
    ... )



"""

import glob
import os

from openai import OpenAI

from tm2p._intern import ParamsMixin
from tm2p._intern.packag_data.templates.load_builtin_template import (
    load_builtin_template,
)
from tm2p.ingest.rec import RecordMapping


class Abstract(
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
    def internal__load_cluster_short_summaries(self):

        files = glob.glob(
            os.path.join(
                self.params.root_directory,
                "outputs",
                "section_5_discussion",
                "*short_summary.txt",
            )
        )

        cluster_descriptions = []
        for i_file, file in enumerate(sorted(files)):
            with open(file, encoding="utf-8") as f:
                text = f.read().strip()
                header = "-" * 40 + f" Cluster {i_file} " + "-" * 40 + "\n\n"
                text = header + text
                cluster_descriptions.append(text)

        self.cluster_short_summaries = "\n\n".join(cluster_descriptions)

    # -------------------------------------------------------------------------
    def internal__load_general_metrics(self):

        filepath = os.path.join(
            self.params.root_directory,
            "outputs",
            "section_4_results",
            "general_metrics.txt",
        )

        with open(filepath, "r", encoding="utf-8") as f:
            self.general_metrics = f.read()

    # -------------------------------------------------------------------------
    def internal__load_synthesis(self):

        filepath = os.path.join(
            self.params.root_directory,
            "outputs",
            "section_6_synthesis",
            "synthesis.txt",
        )

        with open(filepath, "r", encoding="utf-8") as f:
            self.synthesis = f.read()

    # -------------------------------------------------------------------------
    def internal__load_examples(self):

        mapping = (
            RecordMapping()
            #
            .where_root_directory("./")
            .where_database("main")
            .where_record_years_range(None, None)
            .where_record_citations_range(None, None)
            .where_records_ordered_by(None)
            .where_records_match({"document_type": ["Review"]})
            .run()
        )

        mapping = [x["AB"].lower().replace("_", " ") for x in mapping]
        mapping = "\n\n---\n\n".join(mapping)
        self.examples = mapping

    # -------------------------------------------------------------------------
    def internal__load_template(self):
        self.template = load_builtin_template("internals.genai.abstract.txt")

    # -------------------------------------------------------------------------
    def internal__generate_abstract(self):

        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        prompt = self.template.format(
            core_area=self.params.core_area,
            word_length=self.params.word_length,
            definition_of_core_area=self.first_paragraph,
            justification=self.second_paragraph,
            general_metrics=self.general_metrics,
            clusters_summaries=self.cluster_short_summaries,
            synthesis=self.synthesis,
            examples=self.examples,
            cluster_names="\n".join(self.params.cluster_names),
        )

        try:
            response = client.responses.create(model="gpt-4.1", input=prompt)
            answer = response.output_text

            self.abstract = answer

        except Exception as e:
            print(f"Error processing: {e}")

    # -------------------------------------------------------------------------
    def internal__save_abstract(self):

        dirpath = os.path.join(
            self.params.root_directory,
            "outputs",
            "section_0_abstract",
        )

        os.makedirs(dirpath, exist_ok=True)

        filepath = os.path.join(
            dirpath,
            "abstract.txt",
        )

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(self.abstract)

    # -------------------------------------------------------------------------
    def run(self):

        self.internal__load_first_paragraph()
        self.internal__load_second_paragraph()
        self.internal__load_cluster_short_summaries()
        self.internal__load_general_metrics()
        self.internal__load_synthesis()
        self.internal__load_examples()
        self.internal__load_template()
        self.internal__generate_abstract()
        self.internal__save_abstract()
        print("INFO: Done!")
