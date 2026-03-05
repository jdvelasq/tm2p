# CODE_REVIEW: 2026-01-26

from tm2p import Field
from tm2p._intern import Params

from ..step import Step


def build_reference_steps(params: Params) -> list[Step]:

    from ..auth.calculate_numauth import calculate_numauth
    from .assign_recid import assign_recid
    from .assign_recno import assign_recno
    from .calculate_numref_global import calculate_numref_global
    from .compute_lcs import compute_lcs
    from .normalize_global_references import normalize_global_references
    from .normalize_local_references import normalize_local_references

    common_kwargs = {"root_directory": params.root_directory}

    return [
        Step(
            name=f"Assigning '{Field.RNO.value}'",
            function=assign_recno,
            kwargs=common_kwargs,
            count_message="{count} record numbers assigned",
        ),
        Step(
            name=f"Assigning '{Field.RID.value}'",
            function=assign_recid,
            kwargs=common_kwargs,
            count_message="{count} record IDs assigned",
        ),
        Step(
            name=f"Calculating '{Field.N_AUTH.value}'",
            function=calculate_numauth,
            kwargs=common_kwargs,
            count_message="{count} records calculated",
        ),
        Step(
            name=f"Calculating '{Field.N_GCR.value}'",
            function=calculate_numref_global,
            kwargs=common_kwargs,
            count_message="{count} reference counts calculated",
        ),
        Step(
            name=f"Normalizing '{Field.GCR_RAW.value}'",
            function=normalize_global_references,
            kwargs=common_kwargs,
            count_message="{count} references normalized",
        ),
        Step(
            name=f"Normalizing '{Field.LCR_NORM.value}'",
            function=normalize_local_references,
            kwargs=common_kwargs,
            count_message="{count} references normalized",
        ),
        Step(
            name=f"Compute '{Field.LCS.value}'",
            function=compute_lcs,
            kwargs=common_kwargs,
            count_message="{count} records processed",
        ),
    ]


# TODO: _preprocess_references(root_directory)
# TODO: _preprocess_record_id(root_directory)

# TODO: _preprocess_global_references(root_directory)  # ok
# TODO: _preprocess_local_references(root_directory)  # ok
# TODO: _preprocess_local_citations(root_directory)  # ok
# TODO: _preprocess_references(root_directory)
