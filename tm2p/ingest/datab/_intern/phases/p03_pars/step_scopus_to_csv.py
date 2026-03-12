def step_scopus_to_csv(root_directory: str) -> int:
    """:meta private:"""

    from .step_openalex_to_csv import step_openalex_to_csv

    return step_openalex_to_csv(root_directory)
