from tm2p import Field
from tm2p._intern.data_access import load_main_csv_zip, save_main_csv_zip


def s03_calcul_openalex_n_gcr(root_directory: str) -> int:

    df = load_main_csv_zip(root_directory)
    df[Field.N_GCR.value] = 0
    save_main_csv_zip(df, root_directory)

    return 1
