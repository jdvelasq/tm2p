from .s04_extr_scopus_ctry import _create_ctry_col, _create_ctry_thesaurus


def s04_extr_wos_ctry(root_directory: str) -> int:

    _create_ctry_col(root_directory=root_directory)
    _create_ctry_thesaurus(root_directory=root_directory)

    return 1
