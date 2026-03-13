from tm2p._intern.data_access import load_main_csv_zip, save_main_csv_zip


def s01_format_sep(root_directory: str) -> int:

    df = load_main_csv_zip(root_directory)
    df = df.replace(r"\|", "; ", regex=True)
    save_main_csv_zip(df, root_directory)

    return 1
