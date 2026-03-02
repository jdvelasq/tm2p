import pandas as pd  # type: ignore

from tm2p._intern import Params
from tm2p._intern.data_access import load_filtered_main_csv_zip


def extract_values(params: Params) -> pd.DataFrame:
    field = params.source_field.value
    df = load_filtered_main_csv_zip(params)[[field]].dropna().copy()
    df[field] = df[field].str.split("; ")
    return (
        df.explode(field)  # type: ignore
        .assign(**{field: lambda d: d[field].str.strip()})
        .drop_duplicates()
        .reset_index(drop=True)
        .rename(columns={field: "term"})
    )
