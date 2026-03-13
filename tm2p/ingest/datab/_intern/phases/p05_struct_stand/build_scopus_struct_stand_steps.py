# CODE_REVIEW: 2026-01-26

from tm2p._intern import Params

from ...step import Step


def build_scopus_struct_stand_steps(params: Params) -> list[Step]:

    from .s01_format_sep import s01_format_sep
    from .s02_renam_scopus_col import s02_renam_scopus_col
    from .s03_drop_empty_col import s03_drop_empty_col
    from .s04_repair_gcs_lcs_value import s04_repair_gcs_lcs_value
    from .s05_format_authkw_idxkw import s05_format_authkw_idxkw
    from .s06_format_src_raw import s06_format_src_raw
    from .s07_format_src_norm import s07_format_src_norm
    from .s08_format_src_iso4 import s08_format_src_iso4
    from .s09_format_orcid import s09_format_orcid
    from .s10_format_doi import s10_format_doi
    from .s11_format_doctype import s11_format_doctype
    from .s12_set_scopus_datab import s12_set_scopus_datab

    common_kwargs = {"root_directory": params.root_directory}

    return [
        Step(
            name="Formating separators",
            function=s01_format_sep,
            kwargs=common_kwargs,
        ),
        Step(
            name="Renaming Scopus columns",
            function=s02_renam_scopus_col,
            kwargs=common_kwargs,
        ),
        Step(
            name="Dropping empty columns",
            function=s03_drop_empty_col,
            kwargs=common_kwargs,
        ),
        Step(
            name="Setting GCS value",
            function=s04_repair_gcs_lcs_value,
            kwargs=common_kwargs,
        ),
        Step(
            name="Formating AUTHKW and IDXKW",
            function=s05_format_authkw_idxkw,
            kwargs=common_kwargs,
        ),
        Step(
            name="Formating SRC_RAW",
            function=s06_format_src_raw,
            kwargs=common_kwargs,
        ),
        Step(
            name="Formating SRC_NORM",
            function=s07_format_src_norm,
            kwargs=common_kwargs,
        ),
        Step(
            name="Formating SRC_ISO4",
            function=s08_format_src_iso4,
            kwargs=common_kwargs,
        ),
        Step(
            name="Formating ORCID",
            function=s09_format_orcid,
            kwargs=common_kwargs,
        ),
        Step(
            name="Formating DOI",
            function=s10_format_doi,
            kwargs=common_kwargs,
        ),
        Step(
            name="Formating DOCTYPE",
            function=s11_format_doctype,
            kwargs=common_kwargs,
        ),
        Step(
            name="Setting DATABASE value",
            function=s12_set_scopus_datab,
            kwargs=common_kwargs,
        ),
    ]
