"""

Smoke test:
    >>> import pandas as pd
    >>> from tm2p.enum import Field
    >>> df = pd.DataFrame({
    ...     Field.AUTH_NORM.value: ["Doe, J.; Doe, J.", "Smith, A."],
    ...     Field.AUTHID_NORM.value: ["id1; id2", "id3"]
    ... })
    >>> mapping = _build_author_mapping(df)
    >>> mapping["id1"]
    'Doe, J.'
    >>> mapping["id2"]
    'Doe, J./1'

"""

import pandas as pd  # type: ignore

from tm2p import Field
from tm2p._intern.data_access import load_main_csv_zip
from tm2p.ingest.datab._intern.oper import transform_column


def s03_disambig_auth_norm(root_directory: str) -> int:

    id_to_name = _build_author_mapping(root_directory)

    def _disambiguate(series: pd.Series) -> pd.Series:
        return series.str.split(";").apply(
            lambda ids: (
                "; ".join([id_to_name[x.strip()] for x in ids])
                if isinstance(ids, list)
                else None
            )
        )

    count = transform_column(
        source=Field.AUTHID_RAW,
        target=Field.AUTH_NORM,
        function=_disambiguate,
        root_directory=root_directory,
    )

    return count


def _build_author_mapping(root_directory: str) -> dict[str, str]:

    df = load_main_csv_zip(
        root_directory,
        usecols=[Field.AUTH_NORM.value, Field.AUTHID_RAW.value],
    )
    df = df.dropna()

    df[Field.AUTH_NORM.value] = df[Field.AUTH_NORM.value].str.split("; ")
    df[Field.AUTHID_RAW.value] = df[Field.AUTHID_RAW.value].str.split("; ")

    for _, row in df.iterrows():
        if len(row[Field.AUTH_NORM.value]) != len(row[Field.AUTHID_RAW.value]):
            raise ValueError(
                f"Mismatch in number of authors and author IDs for row {_}"
            )

    df = df.explode(
        [
            Field.AUTH_NORM.value,
            Field.AUTHID_RAW.value,
        ]
    )

    df[Field.AUTH_NORM.value] = df[Field.AUTH_NORM.value].str.strip()
    df[Field.AUTHID_RAW.value] = df[Field.AUTHID_RAW.value].str.strip()

    df = df.drop_duplicates(subset=[Field.AUTHID_RAW.value])

    df = df.sort_values(Field.AUTH_NORM.value)
    df["counter"] = df.groupby(Field.AUTH_NORM.value).cumcount()

    mask_collision = df["counter"] > 0
    df.loc[mask_collision, Field.AUTH_NORM.value] += "/" + df.loc[
        mask_collision, "counter"
    ].astype(str)

    return dict(
        zip(
            df[Field.AUTHID_RAW.value],
            df[Field.AUTH_NORM.value],
        )
    )
