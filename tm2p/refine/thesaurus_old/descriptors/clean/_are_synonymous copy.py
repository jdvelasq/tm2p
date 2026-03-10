"""
Are Synonymous?
===============================================================================


Smoke tests:
    >>> # TEST PREPARATION
    >>> import sys
    >>> from io import StringIO
    >>> from tm2p.refine.thesaurus_old.descriptors import InitializeThesaurus, AreSynonymous

    >>> # Redirecting stderr to avoid messages
    >>> original_stderr = sys.stderr
    >>> sys.stderr = StringIO()

    >>> # Create the thesaurus
    >>> InitializeThesaurus(root_directory="examples/fintech/", quiet=True).run()

    >>> # Populate stopwords
    >>> (
    ...     AreSynonymous()
    ...     .with_core_area("fintech (financial technologies)")
    ...     .having_n_contexts(10)
    ...     .having_items_in_top(40)
    ...     .having_items_ordered_by("OCC")
    ...     .having_item_occurrences_between(None, None)
    ...     .having_item_citations_between(None, None)
    ...     .having_items_in(None)
    ...     .where_root_directory("tests/scopus/")
    ... ).run()


    >>> # Capture and print stderr output
    >>> output = sys.stderr.getvalue()
    >>> sys.stderr = original_stderr
    >>> print(output)
                   lead_term                                  candidate_terms
    6   FINANCIAL_INDUSTRIES  FINANCIAL_SECTOR; FINANCIAL_SERVICES_INDUSTRIES
    15     FINTECH_COMPANIES                                 FINTECH_STARTUPS
    22  FINANCIAL_INNOVATION                               FINTECH_INNOVATION


"""

import json
import os
import sys

import openai
import pandas as pd
from openai import OpenAI
from textblob import Word
from tqdm import tqdm  # type: ignore

from tm2p._intern import ParamsMixin
from tm2p._intern.packag_data.templates.load_builtin_template import (
    load_builtin_template,
)
from tm2p.anal.metrics.metrics import Metrics as DominantDataFrame

# -----------------------------------------------------------------------------


class AreSynonymous(
    ParamsMixin,
):
    """:meta private:"""

    def internal__get_descriptors(self):

        if self.params.quiet is False:
            sys.stderr.write("  Getting descriptors\n")
            sys.stderr.flush()

        descriptors = (
            DominantDataFrame()
            .update(**self.params.__dict__)
            .with_source_field("descriptors")
            .run()
        )

        self.data_frame = pd.DataFrame({"lead_term": descriptors.index})
        self.data_frame = self.data_frame[self.data_frame.lead_term.str.count("_") >= 1]
        self.data_frame["merged"] = False
        self.data_frame["keys"] = [[] for _ in range(len(self.data_frame))]
        self.data_frame["contexts"] = [None for _ in range(len(self.data_frame))]
        self.data_frame["candidate_terms"] = [[] for _ in range(len(self.data_frame))]

    # -------------------------------------------------------------------------
    def internal__build_merging_keys(self):

        if self.params.quiet is False:
            sys.stderr.write("  Building merging keys\n")
            sys.stderr.flush()

        for idx, row in self.data_frame.iterrows():

            pattern = row.lead_term
            pattern = pattern.replace("_", " ")
            pattern = pattern.split()

            self.data_frame.at[idx, "keys"].append((pattern[0]))
            self.data_frame.at[idx, "keys"].append((pattern[-1]))

            # # first word + key length
            # self.data_frame.at[idx, "keys"].append(
            #     (pattern[0] + "-" + str(len(pattern)))
            # )

            # # last word + key length
            # self.data_frame.at[idx, "keys"].append(
            #     (pattern[-1] + "-" + str(len(pattern)))
            # )

            # # all bigrams separated by hyphen
            # if len(pattern) >= 2:
            #     for i in range(len(pattern) - 1):
            #         bigram = pattern[i] + "-" + pattern[i + 1]
            #         self.data_frame.at[idx, "keys"].append(bigram)

        self.data_frame["keys"] = self.data_frame["keys"].apply(lambda x: list(set(x)))

    # -------------------------------------------------------------------------
    def internal__compare_terms(
        self,
        lead_term,
        lead_contexts,
        candidate_term,
        candidate_contexts,
    ):

        user_prompt = self.user_template.format(
            core_area=self.params.core_area,
            lead_term=lead_term,
            lead_contexts=lead_contexts,
            candidate_term=candidate_term,
            candidate_contexts=candidate_contexts,
        )

        try:

            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": self.system_prompt,
                        "cache_control": {"type": "ephemeral"},
                    },
                    {
                        "role": "user",
                        "content": user_prompt,
                    },
                ],
                temperature=0,
                response_format={"type": "json_object"},
            )

        except openai.OpenAIError as e:
            print(f"Error processing the query: {e}")
            response = None
            raise ValueError("API error")

        if response is not None:

            answer = response.choices[0].message.content
            answer = answer.strip()
            answer = json.loads(answer)
            answer = answer["answer"]
            answer = answer.lower().strip()

            if answer == "yes":
                answer = True
            else:
                answer = False

        return answer

    # -------------------------------------------------------------------------
    def internal__evaluate_merging(self):

        if self.params.quiet is False:
            sys.stderr.write("  Comparing pairs of keywords\n")
            sys.stderr.flush()

        from tm2p.refine.thesaurus_old.descriptors import GetContexts

        self.get_contexts = (
            GetContexts().update(**self.params.__dict__).update(quiet=True)
        )

        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        self.system_prompt = load_builtin_template(
            "shell.thesaurus.descriptors.clean.synonyms.system.txt"
        )
        self.user_template = load_builtin_template(
            "shell.thesaurus.descriptors.clean.synonyms.user.txt"
        )

        def internal__get_row_contexts(pattern):

            contexts = self.get_contexts.having_text_matching([pattern]).run()
            contexts = [c for c in contexts if len(c) > 80]
            contexts = [c.lower().replace("_", " ") for c in contexts]
            contexts = [c for c in contexts if pattern.lower().replace("_", " ") in c]

            return "\n".join(contexts)

        for idx0, row0 in tqdm(
            self.data_frame.iterrows(),
            total=len(self.data_frame),
            bar_format="  {percentage:3.2f}% {bar} | {n_fmt}/{total_fmt} [{rate_fmt}] |",
            ascii=(" ", ":"),
            ncols=73,
        ):

            if idx0 == self.data_frame.index[-1]:
                break

            if self.data_frame.at[idx0, "merged"] is True:
                continue

            lead_keys = row0["keys"]
            lead_term = row0.lead_term
            lead_contexts = row0["contexts"]

            for idx1, row1 in tqdm(
                self.data_frame.iterrows(),
                total=len(self.data_frame),
                leave=False,
                bar_format="  {percentage:3.2f}% {bar} | {n_fmt}/{total_fmt} [{rate_fmt}] |",
                ascii=(" ", ":"),
                ncols=73,
            ):

                if idx0 >= idx1:
                    continue

                if self.data_frame.at[idx1, "merged"] is True:
                    continue

                candidate_keys = row1["keys"]
                candidate_term = row1.lead_term
                candidate_contexts = row1["contexts"]

                if len(set(lead_keys).intersection(set(candidate_keys))) == 0:
                    continue

                if lead_contexts == None:
                    lead_contexts = internal__get_row_contexts(lead_term)
                    self.data_frame.at[idx0, "contexts"] = lead_contexts

                if candidate_contexts == None:
                    candidate_contexts = internal__get_row_contexts(candidate_term)
                    self.data_frame.at[idx1, "contexts"] = candidate_contexts

                answer = self.internal__compare_terms(
                    lead_term,
                    lead_contexts,
                    candidate_term,
                    candidate_contexts,
                )

                if answer is True:
                    self.data_frame.at[idx1, "merged"] = True
                    self.data_frame.at[idx0, "candidate_terms"].append(candidate_term)

    # -------------------------------------------------------------------------
    def internal__format_output(self):

        self.data_frame = self.data_frame[
            self.data_frame.candidate_terms.apply(lambda x: x != [])
        ]

        self.data_frame["candidate_terms"] = self.data_frame[
            "candidate_terms"
        ].str.join("; ")

    # -------------------------------------------------------------------------
    def run(self):

        self.internal__get_descriptors()
        self.internal__build_merging_keys()
        self.internal__evaluate_merging()
        self.internal__format_output()

        return self.data_frame[["lead_term", "candidate_terms"]]


# =============================================================================
