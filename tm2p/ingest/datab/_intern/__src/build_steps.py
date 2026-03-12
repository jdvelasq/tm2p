# CODE_REVIEW: 2026-01-26

from tm2p import Field
from tm2p._intern import Params

from ..step import Step


def build_source_title_steps(params: Params) -> list[Step]:

    from .assign_subjarea import assign_subjarea
    from .normalize_src_abbr_raw import normalize_srctitle_abbr_raw
    from .normalize_src_raw import normalize_srctitle_raw

    common_kwargs = {"root_directory": params.root_directory}

    return [
        Step(
            name=f"Normalizing {Field.ASJC.value}",
            function=assign_subjarea,
            kwargs=common_kwargs,
            count_message="{count} records processed",
        ),
        Step(
            name=f"Normalizing {Field.SRC_RAW.value}",
            function=normalize_srctitle_raw,
            kwargs=common_kwargs,
            count_message="{count} records processed",
        ),
        Step(
            name=f"Normalizing {Field.SRC_ISO4_RAW.value}",
            function=normalize_srctitle_abbr_raw,
            kwargs=common_kwargs,
            count_message="{count} records processed",
        ),
    ]
