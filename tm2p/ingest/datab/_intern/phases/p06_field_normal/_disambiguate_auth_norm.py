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

from pathlib import Path

import pandas as pd  # type: ignore

from tm2p import Field

from ...oper import DataFile, transform_column


def _load_authors_data(root_directory: Path) -> pd.DataFrame:

    main_file = root_directory / "ingest" / "process" / "main.csv.zip"
    ref_file = root_directory / "ingest" / "process" / "references.csv.zip"

    if not main_file.exists():
        raise FileNotFoundError(f"{main_file} not found")

    df = pd.read_csv(
        main_file,
        usecols=[
            Field.AUTH_NORM.value,
            Field.SCOPUS_AUTHID_NORM.value,
        ],
        compression="zip",
        encoding="utf-8",
        low_memory=False,
    )

    if ref_file.exists():

        ref_df = pd.read_csv(
            ref_file,
            usecols=[
                Field.AUTH_NORM.value,
                Field.SCOPUS_AUTHID_NORM.value,
            ],
            compression="zip",
            encoding="utf-8",
            low_memory=False,
        )
        df = pd.concat([df, ref_df], ignore_index=True)

    return df.dropna()


def _build_author_mapping(df: pd.DataFrame) -> dict[str, str]:

    df[Field.AUTH_NORM.value] = df[Field.AUTH_NORM.value].str.split("; ")
    df[Field.SCOPUS_AUTHID_NORM.value] = df[Field.SCOPUS_AUTHID_NORM.value].str.split(
        "; "
    )

    df = df.explode(
        [
            Field.AUTH_NORM.value,
            Field.SCOPUS_AUTHID_NORM.value,
        ]
    )

    df[Field.AUTH_NORM.value] = df[Field.AUTH_NORM.value].str.strip()
    df[Field.SCOPUS_AUTHID_NORM.value] = df[Field.SCOPUS_AUTHID_NORM.value].str.strip()

    df = df.drop_duplicates(subset=[Field.SCOPUS_AUTHID_NORM.value])

    df = df.sort_values(Field.AUTH_NORM.value)
    df["counter"] = df.groupby(Field.AUTH_NORM.value).cumcount()

    mask_collision = df["counter"] > 0
    df.loc[mask_collision, Field.AUTH_NORM.value] += "/" + df.loc[
        mask_collision, "counter"
    ].astype(str)

    return dict(
        zip(
            df[Field.SCOPUS_AUTHID_NORM.value],
            df[Field.AUTH_NORM.value],
        )
    )


def disambiguate_auth_norm(root_directory: str) -> int:

    root = Path(root_directory)

    raw_data = _load_authors_data(root)
    id_to_name = _build_author_mapping(raw_data)

    def _apply_normalization(series: pd.Series) -> pd.Series:
        return series.str.split(";").apply(
            lambda ids: (
                "; ".join([id_to_name[x.strip()] for x in ids])
                if isinstance(ids, list)
                else None
            )
        )

    count = transform_column(
        source=Field.SCOPUS_AUTHID_NORM,
        target=Field.AUTH_DISAMB,
        function=_apply_normalization,
        root_directory=root_directory,
        file=DataFile.MAIN,
    )

    count += transform_column(
        source=Field.SCOPUS_AUTHID_NORM,
        target=Field.AUTH_DISAMB,
        function=_apply_normalization,
        root_directory=root_directory,
        file=DataFile.REFERENCES,
    )

    return count
