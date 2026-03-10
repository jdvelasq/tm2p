"""
CreateThesaurus
===============================================================================

Smoke tests:
    >>> from tm2p import Field
    >>> from tm2p.refine.user import CreateThesaurus
    >>> (
    ...     CreateThesaurus()
    ...     .using_colored_output(False)
    ...     .with_source_field(Field.DESCRIPTOR_TOK)
    ...     .with_thesaurus_file("demo.the.txt")
    ...     .where_root_directory("tests/scopus/")
    ...     .run()
    ... )
    INFO: Thesaurus initialized successfully.
      Success      : True
      File         : examples/fintech-with-references/refine/thesaurus/demo.the.txt
      Source field : DESCRIPTOR_TOK
      Status       : 2467 items added to the thesaurus.
    <BLANKLINE>



"""

from pathlib import Path

from tqdm import tqdm  # type: ignore

from tm2p._intern import ParamsMixin
from tm2p._intern.data_access import load_main_csv_zip
from tm2p.refine._intern.objs import ThesaurusCreationResult

tqdm.pandas()


class CreateThesaurus(
    ParamsMixin,
):
    """:meta private:"""

    #
    # ALGORITHM:
    # -------------------------------------------------------------------------
    def run(self) -> ThesaurusCreationResult:
        """:meta private:"""

        dataframe = load_main_csv_zip(
            root_directory=self.params.root_directory,
            usecols=[self.params.source_field.value],
        )
        dataframe = dataframe.dropna()
        series = dataframe[self.params.source_field.value]
        series = series.str.split("; ")
        series = series.explode()
        series = series.str.strip()
        series = series.drop_duplicates()
        terms = series.to_list()
        terms = sorted(terms)

        filepath = (
            Path(self.params.root_directory)
            / "refine"
            / "thesaurus"
            / self.params.thesaurus_file
        )

        with open(filepath, "w", encoding="utf-8") as file:
            for term in terms:
                file.write(f"{term}\n")
                file.write(f"    {term}\n")

        return ThesaurusCreationResult(
            colored_output=self.params.colored_output,
            file_path=str(filepath),
            source_field=self.params.source_field.value,
            msg="Thesaurus initialized successfully.",
            success=True,
            status=f"{len(terms)} items added to the thesaurus.",
        )
