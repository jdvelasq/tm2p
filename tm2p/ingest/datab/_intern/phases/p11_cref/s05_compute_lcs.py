from tm2p import Field
from tm2p._intern.data_access import load_main_csv_zip, save_main_csv_zip


def s05_compute_lcs(root_directory: str) -> int:

    df = load_main_csv_zip(root_directory=root_directory, usecols=None)

    rec_id = df[Field.RID.value].tolist()

    df[Field.LCS.value] = df[Field.GCR_WOS_FORMAT.value]
    df[Field.LCS.value] = df[Field.LCS.value].fillna("")
    df[Field.LCS.value] = df[Field.LCS.value].str.split("; ")
    df[Field.LCS.value] = df[Field.LCS.value].apply(
        lambda refs: [ref.strip() for ref in refs],
    )
    df[Field.LCS.value] = df[Field.LCS.value].apply(
        lambda refs: [ref for ref in refs if ref in rec_id],
    )
    df[Field.LCS.value] = df[Field.LCS.value].apply(len)

    save_main_csv_zip(df=df, root_directory=root_directory)

    return len(df)
