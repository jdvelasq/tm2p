"""
Is Stopword?
===============================================================================


Smoke tests:
    >>> # TEST PREPARATION
    >>> from tm2p.refine.thesaurus_old.descriptors import InitializeThesaurus, IsStopword

    >>> # Create the thesaurus
    >>> InitializeThesaurus(root_directory="examples/fintech/", quiet=True).run()

    >>> # Is stopword?
    >>> from tm2p.refine.thesaurus_old.descriptors import IsStopword
    >>> df = (
    ...     IsStopword(quiet=False)
    ...     .with_core_area("FINTECH - FINANCIAL TECHNOLOGIES")
    ...     .having_n_contexts(10)
    ...     .having_items_in_top(40)
    ...     .having_items_ordered_by("OCC")
    ...     .having_item_occurrences_between(None, None)
    ...     .having_item_citations_between(None, None)
    ...     .having_items_in(None)
    ...     .where_root_directory("tests/scopus/")
    ... ).run()  # doctest: +SKIP
    >>> df # doctest: +SKIP
                           descriptor  is_domain_specific?  is_stopword?
    0                    CASE_STUDIES                False          True
    1                           CHINA                False          True
    2                     COMPETITION                False          True
    3                        RESEARCH                False          True
    4                        SERVICES                False          True
    5                         SURVEYS                False          True
    6                      TECHNOLOGY                False          True
    7         ARTIFICIAL_INTELLIGENCE                 True          True
    8                            BANK                 True          True
    9                         BANKING                 True          True
    10                       BIG_DATA                 True          True
    11                 BUSINESS_MODEL                 True          True
    12                        FINANCE                 True          True
    13           FINANCIAL_INDUSTRIES                 True          True
    14           FINANCIAL_INNOVATION                 True          True
    15          FINANCIAL_INSTITUTION                 True          True
    16               FINANCIAL_MARKET                 True          True
    17               FINANCIAL_SECTOR                 True          True
    18              FINANCIAL_SERVICE                 True          True
    19               FINANCIAL_SYSTEM                 True          True
    20            INFORMATION_SYSTEMS                 True          True
    21         INFORMATION_TECHNOLOGY                 True          True
    22                     INNOVATION                 True          True
    23                     INVESTMENT                 True          True
    24                     REGULATION                 True          True
    25                          RISKS                 True          True
    26                 SUSTAINABILITY                 True          True
    27        SUSTAINABLE_DEVELOPMENT                 True          True
    28                       ADOPTION                 True         False
    29                     BLOCKCHAIN                 True         False
    30  FINANCIAL_SERVICES_INDUSTRIES                 True         False
    31         FINANCIAL_TECHNOLOGIES                 True         False
    32                        FINTECH                 True         False
    33              FINTECH_COMPANIES                 True         False
    34             FINTECH_INNOVATION                 True         False
    35                 FINTECH_MARKET                 True         False
    36               FINTECH_SERVICES                 True         False
    37               FINTECH_STARTUPS                 True         False
    38               FINTECH_START_UP                 True         False
    39                        LENDING                 True         False



"""

import json
import os
import re
import sys

import openai
import pandas as pd
from colorama import Fore, init
from openai import OpenAI
from pandarallel import pandarallel

from tm2p._intern import ParamsMixin, load_builtin_template, stdout_to_stderr
from tm2p._intern.packag_data.word_lists import load_builtin_word_list
from tm2p.anal.metrics import Metrics as DominantDataFrame

with stdout_to_stderr():
    pandarallel.initialize(progress_bar=True)

# -----------------------------------------------------------------------------
system_prompt_without_contexts = None
system_prompt_with_contexts = None
user_template_without_contexts = None
user_template_with_contexts = None
geographic_names = None
core_area = None
client = None


# -----------------------------------------------------------------------------
def internal__is_domain_specific_term(row):

    pattern = row.descriptor
    contexts = row["contexts"]

    if pattern in geographic_names:
        return False

    if contexts is None:
        system_prompt = system_prompt_without_contexts
        user_prompt = user_template_without_contexts.format(
            pattern=pattern,
            core_area=core_area,
        )
    else:
        system_prompt = system_prompt_with_contexts
        user_prompt = user_template_with_contexts.format(
            pattern=pattern,
            core_area=core_area,
            contexts=contexts,
        )

    try:

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
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
        raise ValueError("API error")

    if response is not None:

        answer = response.choices[0].message.content
        answer = answer.strip()
        answer = json.loads(answer)
        answer = answer["answer"]
        answer = answer.lower().strip()

        if answer == "yes":
            return True

        return False

    return False


# -----------------------------------------------------------------------------
def internal__is_domain_specific_stopword(row):

    if row["is_domain_specific?"] is False:
        return row["is_stopword?"]

    contexts = row["contexts"]
    pattern = row.descriptor

    if pattern in geographic_names:
        return True

    if contexts is None:
        system_prompt = system_prompt_without_contexts
        user_prompt = user_template_without_contexts.format(
            pattern=pattern,
            core_area=core_area,
        )
    else:
        system_prompt = system_prompt_with_contexts
        user_prompt = user_template_with_contexts.format(
            pattern=pattern,
            core_area=core_area,
            contexts=contexts,
        )

    try:

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
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
        raise ValueError("API error")

    if response is not None:

        answer = response.choices[0].message.content
        answer = answer.strip()
        answer = json.loads(answer)
        answer = answer["answer"]
        answer = answer.lower().strip()

        if answer == "yes":
            return True

        return False

    return False


# -----------------------------------------------------------------------------
def internal__is_non_domain_specific_stopword(row):

    if row["is_domain_specific?"] is True:
        return row["is_stopword?"]

    contexts = row["contexts"]
    pattern = row.descriptor

    if pattern in geographic_names:
        return True

    if contexts is None:
        system_prompt = system_prompt_without_contexts
        user_prompt = user_template_without_contexts.format(
            pattern=pattern,
            core_area=core_area,
        )
    else:
        system_prompt = system_prompt_with_contexts
        user_prompt = user_template_with_contexts.format(
            pattern=pattern,
            core_area=core_area,
            contexts=contexts,
        )

    try:

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
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
        raise ValueError("API error")

    if response is not None:

        answer = response.choices[0].message.content
        answer = answer.strip()
        answer = json.loads(answer)
        answer = answer["answer"]
        answer = answer.lower().strip()

        if answer == "yes":
            return True

        return False


# -----------------------------------------------------------------------------
class IsStopword(
    ParamsMixin,
):
    """:meta private:"""

    #
    # NOTIFICATIONS:
    # -------------------------------------------------------------------------
    def internal__notify_process_start(self):

        if not self.params.quiet:
            sys.stderr.write("\nINFO: Searching for stopwords...\n")
            sys.stderr.flush()

    # -------------------------------------------------------------------------
    def internal__notify_process_end(self):

        if not self.params.quiet:
            sys.stderr.write("  Searching for stopwords... Done\n")
            sys.stderr.flush()

    #
    # ALGORITHM:
    # -------------------------------------------------------------------------
    def internal__load_global_params(self):

        global client
        global core_area
        global geographic_names

        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        core_area = self.params.core_area
        geographic_names = load_builtin_word_list("geography.txt")

    # -------------------------------------------------------------------------
    def internal__get_descriptors(self):

        descriptors = (
            DominantDataFrame()
            .update(**self.params.__dict__)
            .with_source_field("descriptors")
            .run()
        )

        self.descriptors = pd.DataFrame({"descriptor": descriptors.index})
        self.descriptors["is_domain_specific?"] = False
        self.descriptors["is_stopword?"] = False

    # -------------------------------------------------------------------------
    def internal__get_contexts(self):

        from tm2p.refine.thesaurus_old.descriptors import GetContexts

        get_contexts = GetContexts().update(**self.params.__dict__).update(quiet=True)

        sys.stderr.write("  Retrieving contexts for descriptors\n")
        sys.stderr.flush()

        with stdout_to_stderr():
            self.descriptors["contexts"] = self.descriptors[
                "descriptor"
            ].parallel_apply(
                lambda x: "\n".join(
                    get_contexts.having_text_matchings_matching([re.escape(x)]).run()
                )
            )

        sys.stderr.write("\n")
        sys.stderr.flush()

    # -------------------------------------------------------------------------
    def internal__is_domain_specific_term(self):

        global system_prompt_without_contexts
        global user_template_without_contexts
        global system_prompt_with_contexts
        global user_template_with_contexts

        system_prompt_without_contexts = load_builtin_template(
            "shell.thesaurus.descriptors.clean.stopwords.phase_1_without_context_phrases.system.txt"
        )
        user_template_without_contexts = load_builtin_template(
            "shell.thesaurus.descriptors.clean.stopwords.phase_1_without_context_phrases.user.txt"
        )

        system_prompt_with_contexts = load_builtin_template(
            "shell.thesaurus.descriptors.clean.stopwords.phase_1_with_context_phrases.system.txt"
        )
        user_template_with_contexts = load_builtin_template(
            "shell.thesaurus.descriptors.clean.stopwords.phase_1_with_context_phrases.user.txt"
        )

        sys.stderr.write("  Determining if descriptors are non-domain specific\n")
        sys.stderr.flush()

        with stdout_to_stderr():
            self.descriptors["is_domain_specific?"] = self.descriptors.parallel_apply(
                internal__is_domain_specific_term, axis=1
            )

        sys.stderr.write("\n")
        sys.stderr.flush()

    def internal__is_domain_specific_stopword(self):

        global system_prompt_without_contexts
        global user_template_without_contexts
        global system_prompt_with_contexts
        global user_template_with_contexts

        system_prompt_without_contexts = load_builtin_template(
            "shell.thesaurus.descriptors.clean.stopwords.phase_2_without_context_phrases.system.txt"
        )
        user_template_without_contexts = load_builtin_template(
            "shell.thesaurus.descriptors.clean.stopwords.phase_2_without_context_phrases.user.txt"
        )

        system_prompt_with_contexts = load_builtin_template(
            "shell.thesaurus.descriptors.clean.stopwords.phase_2_with_context_phrases.system.txt"
        )
        user_template_with_contexts = load_builtin_template(
            "shell.thesaurus.descriptors.clean.stopwords.phase_2_with_context_phrases.user.txt"
        )

        sys.stderr.write("  Evaluating domain specific descriptors\n")
        sys.stderr.flush()

        with stdout_to_stderr():
            self.descriptors["is_stopword?"] = self.descriptors.parallel_apply(
                internal__is_domain_specific_stopword, axis=1
            )

        sys.stderr.write("\n")
        sys.stderr.flush()

    # -------------------------------------------------------------------------
    def internal__is_non_domain_specific_stopword(self):

        global system_prompt_without_contexts
        global user_template_without_contexts
        global system_prompt_with_contexts
        global user_template_with_contexts

        system_prompt_without_contexts = load_builtin_template(
            "shell.thesaurus.descriptors.clean.stopwords.phase_3_without_context_phrases.system.txt"
        )
        user_template_without_contexts = load_builtin_template(
            "shell.thesaurus.descriptors.clean.stopwords.phase_3_without_context_phrases.user.txt"
        )

        system_prompt_with_contexts = load_builtin_template(
            "shell.thesaurus.descriptors.clean.stopwords.phase_3_with_context_phrases.system.txt"
        )
        user_template_with_contexts = load_builtin_template(
            "shell.thesaurus.descriptors.clean.stopwords.phase_3_with_context_phrases.user.txt"
        )

        sys.stderr.write("  Evaluating non-domain specific descriptors\n")
        sys.stderr.flush()

        with stdout_to_stderr():
            self.descriptors["is_stopword?"] = self.descriptors.parallel_apply(
                internal__is_non_domain_specific_stopword, axis=1
            )

        sys.stderr.write("\n")
        sys.stderr.flush()

    # -------------------------------------------------------------------------
    def run(self):

        self.internal__notify_process_start()
        self.internal__load_global_params()
        self.internal__get_descriptors()
        self.internal__get_contexts()
        self.internal__is_domain_specific_term()
        self.internal__is_domain_specific_stopword()
        self.internal__is_non_domain_specific_stopword()
        self.internal__notify_process_end()

        self.descriptors = self.descriptors.sort_values(
            by=["is_stopword?", "is_domain_specific?", "descriptor"],
            ascending=[False, True, True],
        ).reset_index(drop=True)

        return self.descriptors[
            [
                "descriptor",
                "is_domain_specific?",
                "is_stopword?",
            ]
        ]


# =============================================================================
