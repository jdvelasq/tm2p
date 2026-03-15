# CODE_REVIEW: 2026-01-26

from tm2p import Field
from tm2p._intern import Params

from ...step import Step


def build_rec_steps(params: Params) -> list[Step]:

    from .s01_assign_recno import s01_assign_recno
    from .s02_assign_recid import s02_assign_recid

    common_kwargs = {"root_directory": params.root_directory}

    return [
        Step(
            name=f"Assigning '{Field.REC_NO.value}'",
            function=s01_assign_recno,
            kwargs=common_kwargs,
            count_message="{count} record numbers assigned",
        ),
        Step(
            name=f"Assigning '{Field.REC_ID.value}'",
            function=s02_assign_recid,
            kwargs=common_kwargs,
            count_message="{count} record IDs assigned",
        ),
    ]
