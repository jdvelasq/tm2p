"""
CreateThesaurus
===============================================================================

Smoke tests:
    >>> from tm2p import Field
    >>> from tm2p.refine.organizations import CreateThesaurus
    >>> (
    ...     CreateThesaurus()
    ...     .using_colored_output(False)
    ...     .with_thesaurus_file("demo.the.txt")
    ...     .where_root_directory("tests/scopus/")
    ...     .run()
    ... )
    INFO: Thesaurus initialized successfully.
      Success      : True
      File         : examples/small/refine/thesaurus/organizations.the.txt
      Source field : ORGANIZATION_AND_AFFIL
      Status       : 45 organizations added to the thesaurus.
    <BLANKLINE>



"""

from pathlib import Path

from tqdm import tqdm  # type: ignore

from tm2p import Field
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
            usecols=[Field.ORG_AFFIL.value],
        )
        dataframe = dataframe.dropna()
        series = dataframe[Field.ORG_AFFIL.value]
        series = series.str.split("; ")
        series = series.explode()
        series = series.str.strip()
        series = series.drop_duplicates()
        series = series.str.split(" @ ")
        terms = series.to_list()

        mapping: dict[str, list[str]] = {}

        for term in terms:
            if term == ["[n/a]"]:
                continue
            organization, affil = term
            if organization not in mapping:
                mapping[organization] = []
            mapping[organization].append(affil)

        filepath = (
            Path(self.params.root_directory)
            / "refine"
            / "thesaurus"
            / "organizations.the.txt"
        )

        with open(filepath, "w", encoding="utf-8") as file:
            for organization in sorted(mapping.keys()):
                file.write(f"{organization}\n")
                for affil in sorted(mapping[organization]):
                    file.write(f"    {affil}\n")

        return ThesaurusCreationResult(
            colored_output=self.params.colored_output,
            file_path=str(filepath),
            source_field=Field.ORG_AFFIL.value,
            msg="Thesaurus initialized successfully.",
            success=True,
            status=f"{len(mapping.keys())} organizations added to the thesaurus.",
        )
