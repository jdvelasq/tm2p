"""
Define Key
===============================================================================

Smoke tests:
    >>> # Preparation
    >>> from tm2p.refine.thesaurus_old.descriptors import InitializeThesaurus
    >>> from tm2p.refine.thesaurus_old.descriptors import ApplyThesaurus
    >>> InitializeThesaurus(root_directory="examples/fintech/", quiet=True).run()
    >>> ApplyThesaurus(root_directory="examples/fintech/", quiet=True).run()

    >>> # Use
    >>> from tm2p.refine.thesaurus_old.descriptors import DefineTerm
    >>> definitions = (
    ...     DefineTerm()
    ...     #
    ...     # FIELD:
    ...     .with_core_area("FINTECH (financial technologies)")
    ...     .with_patterns(['FINTECH', 'FINANCIAL_TECHNOLOGIES'])
    ...     .having_n_contexts(10)
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/scopus/")
    ...     .where_database("main")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    ... ) # doctest: +SKIP
    >>> from textwrap import fill
    >>> for definiition in definitions:
    ...     print(fill(definiition, width=70)) # doctest: +SKIP
    FINTECH, short for financial technology, refers to the innovative use
    of technology in the design and delivery of financial products and
    services. it has become a crucial component of modern banking,
    enabling banks to compete with nonfinancial institutions offering
    services like payments. FINTECH encompasses a wide range of
    applications, including robo-advising, artificial intelligence, and
    cryptocurrencies, fundamentally altering banking operations, capital
    raising, and even the concept of money. the rapid growth of FINTECH
    has prompted regulatory bodies to prioritize its supervision.
    understanding the perceived benefits and risks of FINTECH is essential
    for its adoption across diverse user types and sectors, such as
    agriculture sustainability.
    FINANCIAL TECHNOLOGIES, commonly referred to as fintech, encompass the
    design and delivery of financial products and services through
    advanced technology. they have become integral to modern banking,
    extending beyond traditional financial services to include innovations
    like payment services, robo-advising, and cryptocurrencies. fintech
    has transformed the financial landscape, prompting nonfinancial
    institutions to enter the market and challenging existing regulatory
    frameworks. the sector's growth is driven by technological and
    economic factors, influencing user adoption based on perceived
    benefits and risks. fintech also supports broader applications, such
    as enhancing agricultural sustainability and reshaping capital raising
    and monetary forms.


"""

import json
import os

import openai
from openai import OpenAI

from tm2p._intern import ParamsMixin
from tm2p._intern.packag_data.templates.load_builtin_template import (
    load_builtin_template,
)


class DefineTerm(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):

        from tm2p.refine.thesaurus_old.descriptors import GetContexts

        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        contexts = GetContexts().update(**self.params.__dict__).run()
        core_area = self.params.core_area

        terms = self.params.pattern

        system_prompt = load_builtin_template(
            "shell.thesaurus.descriptors.clean.define.system.txt"
        )

        user_template = load_builtin_template(
            "shell.thesaurus.descriptors.clean.define.user.txt"
        )

        definitions = []

        for term in terms:

            user_prompt = user_template.format(
                term=term,
                contexts=contexts,
                core_area=core_area,
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

            answer = response.choices[0].message.content
            answer = answer.strip()
            answer = json.loads(answer)
            answer = answer["text"]
            answer = answer.lower().strip()
            answer = answer.replace(
                term.lower().replace("_", " "),
                term.upper().replace("_", " "),
            )

            definitions.append(answer)

        return definitions
