"""
General Metrics Text
===============================================================================

Smoke tests:
    >>> from tm2p.refine.thesaurus_old.countries import (
    ...     InitializeThesaurus as CreateCountryThesaurus,
    ...     ApplyThesaurus as ApplyCountryThesaurus,
    ... )  # doctest: +ELLIPSIS
    Note...
    >>> from tm2p.refine.thesaurus_old.organizations import (
    ...     InitializeThesaurus as CreateOrganizationsThesaurus,
    ...     ApplyThesaurus as ApplyOrganizationsThesaurus,
    ... )
    >>> from tm2p.refine.thesaurus_old.descriptors import (
    ...     InitializeThesaurus as CreateDescriptorsThesaurus,
    ...     ApplyThesaurus as ApplyDescriptorsThesaurus,
    ... )


    >>> # Create and apply thesauri
    >>> CreateCountryThesaurus(root_directory="examples/fintech/", quiet=True).run()
    >>> ApplyCountryThesaurus(root_directory="examples/fintech/", quiet=True).run()
    >>> CreateOrganizationsThesaurus(root_directory="examples/fintech/", quiet=True).run()
    >>> ApplyOrganizationsThesaurus(root_directory="examples/fintech/", quiet=True).run()
    >>> CreateDescriptorsThesaurus(root_directory="examples/fintech/", quiet=True).run()
    >>> ApplyDescriptorsThesaurus(root_directory="examples/fintech/", quiet=True).run()

    >>> # Create, configure, and run the Text generator
    >>> from tm2p.report.manuscript.results.general_metrics.text import Text
    >>> (
    ...     Text()
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/scopus/")
    ...     .where_database("main")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run() # doctest: +SKIP
    ... )






"""

import os

from openai import OpenAI

from tm2p._intern import ParamsMixin
from tm2p._intern.packag_data.templates.load_builtin_template import (
    load_builtin_template,
)
from tm2p.discov.main_inf import Metrics as MainInformation


class GeneralMetrics(
    ParamsMixin,
):
    """:meta private:"""

    def __init__(self):
        super().__init__()
        self.df = None

    def compute_metrics(self):
        self.df = MainInformation().update(**self.params.__dict__).run()

    def timespan(self):
        return self.df.loc[
            (
                "GENERAL",
                "Timespan",
            ),
            "Value",
        ]

    def annual_growth_rate(self):
        return self.df.loc[
            (
                "GENERAL",
                "Annual growth rate %",
            ),
            "Value",
        ]

    def document_average_age(self):
        return self.df.loc[
            (
                "GENERAL",
                "Document average age",
            ),
            "Value",
        ]

    def average_citations_per_document(self):
        return self.df.loc[
            (
                "GENERAL",
                "Average citations per document",
            ),
            "Value",
        ]

    def average_citations_per_document_per_year(self):
        return self.df.loc[
            (
                "GENERAL",
                "Average citations per document per year",
            ),
            "Value",
        ]

    def sources(self):
        return self.df.loc[
            (
                "GENERAL",
                "Sources",
            ),
            "Value",
        ]

    def average_documents_per_source(self):
        return self.df.loc[
            (
                "GENERAL",
                "Average documents per source",
            ),
            "Value",
        ]

    def document_types(self):
        return ", ".join(
            f"{item}: {self.df.loc[('DOCUMENT TYPES', item), 'Value']}"
            for item in self.df.loc["DOCUMENT TYPES"].index
        )

    def authors(self):
        return self.df.loc[
            (
                "AUTHORS",
                "Authors",
            ),
            "Value",
        ]

    def authors_of_single_authored_documents(self):
        return self.df.loc[
            (
                "AUTHORS",
                "Authors of single-authored documents",
            ),
            "Value",
        ]

    def single_authored_documents(self):
        return self.df.loc[
            (
                "AUTHORS",
                "Single-authored documents",
            ),
            "Value",
        ]

    def multi_authored_documents(self):
        return self.df.loc[
            (
                "AUTHORS",
                "Multi-authored documents",
            ),
            "Value",
        ]

    def authors_per_document(self):
        return self.df.loc[
            (
                "AUTHORS",
                "Authors per document",
            ),
            "Value",
        ]

    def international_coauthorship(self):
        return self.df.loc[
            (
                "AUTHORS",
                "International co-authorship %",
            ),
            "Value",
        ]

    def organizations(self):
        return self.df.loc[
            (
                "AUTHORS",
                "organizations",
            ),
            "Value",
        ]

    def countries(self):
        return self.df.loc[
            (
                "AUTHORS",
                "Countries",
            ),
            "Value",
        ]

    def documents(self):
        return self.df.loc[
            (
                "GENERAL",
                "Documents",
            ),
            "Value",
        ]

    def build_template(self):
        template = load_builtin_template("internals.genai.general_metrics.txt")
        self.prompt = template.format(
            timespan=self.timespan(),
            documents=self.documents(),
            annual_growth_rate=self.annual_growth_rate(),
            document_average_age=self.document_average_age(),
            average_citations_per_document=self.average_citations_per_document(),
            average_citations_per_document_per_year=self.average_citations_per_document_per_year(),
            sources=self.sources(),
            average_documents_per_source=self.average_documents_per_source(),
            document_types=self.document_types(),
            authors=self.authors(),
            authors_of_single_authored_documents=self.authors_of_single_authored_documents(),
            single_authored_documents=self.single_authored_documents(),
            multi_authored_documents=self.multi_authored_documents(),
            authors_per_document=self.authors_per_document(),
            international_coauthorship=self.international_coauthorship(),
            organizations=self.organizations(),
            countries=self.countries(),
        )

    def execute_prompt(self):

        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        try:
            response = client.responses.create(
                model="gpt-4-turbo",
                input=self.prompt,
            )
            self.answer = response.output_text

        except Exception as e:
            print(f"Error processing: {e}")

    def save_text(self):

        dir_path = os.path.join(
            self.params.root_directory,
            "outputs",
            "section_4_results",
        )
        os.makedirs(dir_path, exist_ok=True)

        filename = os.path.join(dir_path, "general_metrics.txt")

        with open(filename, "w") as file:
            file.write(self.answer)

    def run(self):

        self.compute_metrics()
        self.build_template()
        self.execute_prompt()
        self.save_text()
