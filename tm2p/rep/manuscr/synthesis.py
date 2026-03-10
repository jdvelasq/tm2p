"""
Synthesis
===============================================================================

Smoke tests:

    >>> from tm2p.manuscript import Synthesis
    >>> (
    ...     Synthesis()
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


class Synthesis(
    ParamsMixin,
):
    """:meta private:"""

    # -------------------------------------------------------------------------
    def internal__load_cluster_descriptions(self):

        files = glob.glob(
            os.path.join(
                self.params.root_directory,
                "outputs",
                "section_5_discussion",
                "*full_summary.txt",
            )
        )

        cluster_descriptions = []
        for i_file, file in enumerate(sorted(files)):
            with open(file, encoding="utf-8") as f:
                text = f.read().strip()
                header = "-" * 40 + f" CLUSTER {i_file} " + "-" * 40 + "\n\n"
                text = header + text
                cluster_descriptions.append(text)

        self.cluster_descriptions = "\n\n".join(cluster_descriptions)

    # -------------------------------------------------------------------------
    def internal__load_template(self):
        self.template = load_builtin_template("internals.genai.synthesis.txt")

    # -------------------------------------------------------------------------
    def internal__generate_synthesis(self):

        path = os.path.join(
            self.params.root_directory, "outputs", "section_6_synthesis"
        )
        # delete the content of the directory if it exists
        if os.path.exists(path):
            for file in os.listdir(path):
                file_path = os.path.join(path, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
        else:
            os.makedirs(path, exist_ok=True)

        prompt = self.template.format(
            core_area=self.params.core_area,
            word_length=self.params.word_length,
            clusters_description=self.cluster_descriptions,
        )

        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        try:
            response = client.responses.create(model="gpt-4.1", input=prompt)
            answer = response.output_text

            self.synthesis = answer

        except Exception as e:
            print(f"Error processing: {e}")

    # -------------------------------------------------------------------------
    def internal__save_synthesis_to_disk(self):
        path = os.path.join(
            self.params.root_directory,
            "outputs",
            "section_6_synthesis",
            "synthesis.txt",
        )
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.synthesis)

    # -------------------------------------------------------------------------
    def run(self):

        self.internal__load_cluster_descriptions()
        self.internal__load_template()
        self.internal__generate_synthesis()
        self.internal__save_synthesis_to_disk()
