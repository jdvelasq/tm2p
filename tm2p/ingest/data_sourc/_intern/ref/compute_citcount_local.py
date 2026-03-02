from tm2p import Field
from tm2p._intern.data_access import load_main_csv_zip, save_main_csv_zip


def compute_citcount_local(root_directory: str) -> int:

    dataframe = load_main_csv_zip(root_directory=root_directory, usecols=None)

    rec_id = dataframe[Field.RID.value].tolist()

    dataframe[Field.LCS.value] = dataframe[Field.REF_NORM.value]
    dataframe[Field.LCS.value] = dataframe[Field.LCS.value].fillna("")
    dataframe[Field.LCS.value] = dataframe[Field.LCS.value].str.split("; ")
    dataframe[Field.LCS.value] = dataframe[Field.LCS.value].apply(
        lambda refs: [ref.strip() for ref in refs],
    )
    dataframe[Field.LCS.value] = dataframe[Field.LCS.value].apply(
        lambda refs: [ref for ref in refs if ref in rec_id],
    )
    dataframe[Field.LCS.value] = dataframe[Field.LCS.value].apply(
        len,
    )
    save_main_csv_zip(df=dataframe, root_directory=root_directory)

    return len(dataframe)
