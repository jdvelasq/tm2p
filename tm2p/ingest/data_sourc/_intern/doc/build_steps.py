# CODE_REVIEW: 2026-01-26

from tm2p import Field
from tm2p._intern import Params

from ..step import Step


def build_document_steps(params: Params) -> list[Step]:

    from .normalize_doctype_raw import normalize_doctype_raw
    from .repair_citcount_global import repair_citcount_global
    from .repair_doi import repair_doi

    common_kwargs = {"root_directory": params.root_directory}

    return [
        Step(
            name=f"Repairing '{Field.GCS.value}'",
            function=repair_citcount_global,
            kwargs=common_kwargs,
            count_message="{count} records repaired",
        ),
        Step(
            name=f"Normalizing '{Field.PUBTYPE_RAW.value}'",
            function=normalize_doctype_raw,
            kwargs=common_kwargs,
            count_message="{count} records normalized",
        ),
        Step(
            name=f"Repairing '{Field.DOI.value}'",
            function=repair_doi,
            kwargs=common_kwargs,
            count_message="{count} records repaired",
        ),
    ]
