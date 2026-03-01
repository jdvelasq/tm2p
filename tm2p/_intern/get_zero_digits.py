import math


def get_zero_digits(root_directory: str) -> tuple[int, int]:

    from .data_access.load_main_csv_zip import load_main_csv_zip

    df = load_main_csv_zip(root_directory)
    n = len(df)
    occ_digits = len(str(n))
    gcs_digits = math.ceil(math.log10(n + 1)) + 2

    return occ_digits, gcs_digits
