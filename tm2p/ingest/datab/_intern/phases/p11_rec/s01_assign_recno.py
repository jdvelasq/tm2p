from tm2p import Field
from tm2p._intern.data_access import load_main_csv_zip, save_main_csv_zip


def s01_assign_recno(root_directory):

    df = load_main_csv_zip(root_directory)

    num_zeros = len(str(len(df)))
    df[Field.REC_NO.value] = [f"{i:0{num_zeros}d}" for i in range(1, len(df) + 1)]

    save_main_csv_zip(df, root_directory)
