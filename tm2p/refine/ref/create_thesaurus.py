"""
CreateThesaurus
===============================================================================

Smoke tests:
    >>> from tm2p import Field
    >>> from tm2p.refine.references import CreateThesaurus
    >>> (
    ...     CreateThesaurus()
    ...     .using_colored_output(False)
    ...     .where_root_directory("tests/scopus/")
    ...     .run()
    ... )
    INFO: Thesaurus initialized successfully.
      Success      : True
      File         : examples/small/refine/thesaurus/references.the.txt
      Source field : REF_AND_REC_ID
      Status       : 57 references added to the thesaurus.
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
            usecols=[Field.GCR_RID.value],
        )
        dataframe = dataframe.dropna()
        series = dataframe[Field.GCR_RID.value]
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
            rec_id, ref = term
            if rec_id == "[n/a]":
                continue
            if rec_id not in mapping:
                mapping[rec_id] = []
            mapping[rec_id].append(ref)

        filepath = (
            Path(self.params.root_directory)
            / "refine"
            / "thesaurus"
            / "references.the.txt"
        )

        with open(filepath, "w", encoding="utf-8") as file:
            for rec_id in sorted(mapping.keys()):
                file.write(f"{rec_id}\n")
                for ref in sorted(mapping[rec_id]):
                    file.write(f"    {ref}\n")

        return ThesaurusCreationResult(
            colored_output=self.params.colored_output,
            file_path=str(filepath),
            source_field=Field.GCR_RID.value,
            msg="Thesaurus initialized successfully.",
            success=True,
            status=f"{len(mapping.keys())} references added to the thesaurus.",
        )
