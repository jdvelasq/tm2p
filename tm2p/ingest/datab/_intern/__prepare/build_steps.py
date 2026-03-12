# CODE_REVIEW: 2026-01-26

from tm2p._intern import Params

from ..step import Step


def build_merging_steps(params: Params) -> list[Step]:

    # from ._compress_raw_files import compress_raw_files
    # from ._create_database_files import create_database_files
    # from ._drop_empty_columns import drop_empty_columns
    # from ._remove_non_english_abstracts import remove_non_english_abstracts
    # from ._rename_columns import rename_columns
    # from ._validate_required_columns import validate_required_columns
    from ..phases.pars.step_wos_to_csv import step_wos_to_csv

    common_kwargs = {"root_directory": params.root_directory}

    return [
        Step(
            name="Ingesting WoS files",
            function=step_wos_to_csv,
            kwargs=common_kwargs,
            count_message="{count} records ingested",
        ),
        # Step(
        #     name="Removing non-English abstracts",
        #     function=remove_non_english_abstracts,
        #     kwargs=common_kwargs,
        #     count_message="{count} records with non-English abstracts removed",
        # ),
        # Step(
        #     name="Compressing raw files",
        #     function=compress_raw_files,
        #     kwargs=common_kwargs,
        #     count_message="{count} raw files compressed",
        # ),
        # Step(
        #     name="Creating database files",
        #     function=create_database_files,
        #     kwargs=common_kwargs,
        #     count_message="{count} records created in database files",
        # ),
        # Step(
        #     name="Renaming columns",
        #     function=rename_columns,
        #     kwargs=common_kwargs,
        #     count_message="{count} files with renamed columns",
        # ),
        # Step(
        #     name="Dropping empty columns",
        #     function=drop_empty_columns,
        #     kwargs=common_kwargs,
        #     count_message="{count} empty columns dropped",
        # ),
        # Step(
        #     name="Validating required columns",
        #     function=validate_required_columns,
        #     kwargs=common_kwargs,
        #     count_message="{count} files with all required columns",
        # ),
    ]
