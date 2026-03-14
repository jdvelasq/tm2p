# CODE_REVIEW: 2026-01-26

from tm2p import Field
from tm2p._intern import Params

from ...step import Step


def build_cref_steps(params: Params) -> list[Step]:

    from .s01_assign_recno import s01_assign_recno
    from .s02_assign_recid import s02_assign_recid
    from .s03_normalize_global_references import s03_normalize_global_references
    from .s04_normalize_local_references import s04_normalize_local_references
    from .s05_compute_lcs import s05_compute_lcs

    common_kwargs = {"root_directory": params.root_directory}

    return [
        Step(
            name=f"Assigning '{Field.RNO.value}'",
            function=s01_assign_recno,
            kwargs=common_kwargs,
            count_message="{count} record numbers assigned",
        ),
        Step(
            name=f"Assigning '{Field.RID.value}'",
            function=s02_assign_recid,
            kwargs=common_kwargs,
            count_message="{count} record IDs assigned",
        ),
        Step(
            name=f"Normalizing '{Field.GCR_FREE_TEXT.value}'",
            function=s03_normalize_global_references,
            kwargs=common_kwargs,
            count_message="{count} references normalized",
        ),
        Step(
            name=f"Normalizing '{Field.LCR_NORM.value}'",
            function=s04_normalize_local_references,
            kwargs=common_kwargs,
            count_message="{count} references normalized",
        ),
        Step(
            name=f"Compute '{Field.LCS.value}'",
            function=s05_compute_lcs,
            kwargs=common_kwargs,
            count_message="{count} records processed",
        ),
    ]
