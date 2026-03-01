from tm2p import CorpusField
from tm2p._intern.data_access import load_main_csv_zip, save_main_csv_zip


def compute_citcount_local(root_directory: str) -> int:

    dataframe = load_main_csv_zip(root_directory=root_directory, usecols=None)

    rec_id = dataframe[CorpusField.RID.value].tolist()

    dataframe[CorpusField.LCS.value] = dataframe[CorpusField.REF_NORM.value]
    dataframe[CorpusField.LCS.value] = dataframe[CorpusField.LCS.value].fillna("")
    dataframe[CorpusField.LCS.value] = dataframe[CorpusField.LCS.value].str.split("; ")
    dataframe[CorpusField.LCS.value] = dataframe[CorpusField.LCS.value].apply(
        lambda refs: [ref.strip() for ref in refs],
    )
    dataframe[CorpusField.LCS.value] = dataframe[CorpusField.LCS.value].apply(
        lambda refs: [ref for ref in refs if ref in rec_id],
    )
    dataframe[CorpusField.LCS.value] = dataframe[CorpusField.LCS.value].apply(
        len,
    )
    save_main_csv_zip(df=dataframe, root_directory=root_directory)

    return len(dataframe)
