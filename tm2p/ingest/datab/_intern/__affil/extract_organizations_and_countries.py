from pathlib import Path

import pandas as pd  # type: ignore

from tm2p import Field
from tm2p._intern.data_access import load_main_csv_zip, save_main_csv_zip
from tm2p._intern.packag_data import load_builtin_mapping
from tm2p.ingest.datab._intern.oper.ltwa_col import ltwa_column

from ._internals import extract_country_name_from_string, extract_org_name_from_string

AFFIL_RAW = Field.AFFIL_RAW.value
CTRY_AFFIL = Field.CTRY_AFFIL.value
CTRY = Field.CTRY.value
CTRY_FIRST = Field.CTRY_FIRST.value
CTRY_ISO3 = Field.CTRY_ISO3.value
CTRY_ISO3_FIRST = Field.CTRY_ISO3_FIRST.value
ORG_FIRST = Field.ORG_FIRST.value

ORG = Field.ORG_RAW.value


def extract_organizations_and_countries(root_directory: str) -> int:

    dataframe = load_main_csv_zip(root_directory=root_directory)
    countries, organizations = _build_mappings(dataframe)
    dataframe = _create_country_columns(dataframe, countries)
    dataframe = _create_organization_column(dataframe, organizations)
    save_main_csv_zip(df=dataframe, root_directory=root_directory)

    _create_thesaurus_files(root_directory, countries, organizations)

    ltwa_column(
        source=Field.ORG_RAW,
        target=Field.ORG_NORM,
        root_directory=root_directory,
    )

    ltwa_column(
        source=Field.ORG_FIRST,
        target=Field.ORG_FIRST,
        root_directory=root_directory,
    )

    return int(dataframe[Field.AFFIL_RAW.value].notna().sum())


def _build_mappings(dataframe: pd.DataFrame) -> tuple[dict[str, str], dict[str, str]]:

    affiliations = _get_raw_affiliations(dataframe)
    affiliations[CTRY] = affiliations[AFFIL_RAW].apply(extract_country_name_from_string)
    affiliations[ORG] = affiliations[AFFIL_RAW].apply(extract_org_name_from_string)
    affiliations[ORG] = _assign_country_code_to_orgs(affiliations)

    countries = _get_country_mapping(affiliations)
    organizations = _get_organization_mapping(affiliations)

    return countries, organizations


def _get_raw_affiliations(dataframe: pd.DataFrame) -> pd.DataFrame:

    affiliations = dataframe[[AFFIL_RAW]].copy()
    affiliations = affiliations.dropna()
    affiliations[AFFIL_RAW] = affiliations[AFFIL_RAW].str.split("; ")
    raw_affiliation = affiliations.explode(AFFIL_RAW)  # type: ignore

    raw_affiliation[AFFIL_RAW] = raw_affiliation[AFFIL_RAW].str.strip()
    raw_affiliation = raw_affiliation.drop_duplicates()

    return raw_affiliation  # type: ignore


def _get_country_mapping(affiliations: pd.DataFrame) -> dict[str, str]:

    affiliations = affiliations[[AFFIL_RAW, CTRY]].dropna()  # type: ignore
    affiliations = affiliations.drop_duplicates()
    mapping: dict[str, str] = pd.Series(  # type: ignore
        affiliations[CTRY].values, index=affiliations[AFFIL_RAW]
    ).to_dict()

    return mapping


def _get_organization_mapping(affiliations: pd.DataFrame) -> dict[str, str]:

    affiliations = affiliations[[AFFIL_RAW, ORG]].dropna()  # type: ignore
    affiliations = affiliations.drop_duplicates()
    mapping: dict[str, str] = pd.Series(  # type: ignore
        affiliations[ORG].values, index=affiliations[AFFIL_RAW]
    ).to_dict()
    return mapping


def _assign_country_code_to_orgs(affiliations: pd.DataFrame) -> pd.Series:

    affiliations = affiliations.copy()
    country_to_alpha3 = load_builtin_mapping("country_to_alpha3.json")
    affiliations[ORG] += affiliations[CTRY].map(
        lambda country: f" [{country_to_alpha3.get(country, 'N/A')}]"
    )
    return affiliations[ORG]


def _create_country_columns(
    df: pd.DataFrame, country_mapping: dict[str, str]
) -> pd.DataFrame:

    df = df.copy()

    country_to_iso3 = load_builtin_mapping("country_to_alpha3.json")

    df[CTRY] = df[AFFIL_RAW].copy()
    df[CTRY] = df[CTRY].fillna("[n/a]")
    df[CTRY] = df[CTRY].str.split("; ")
    df[CTRY] = df[CTRY].apply(
        lambda affils: [country_mapping.get(affil, "[n/a]") for affil in affils],
    )
    df[CTRY_ISO3] = df[CTRY].apply(
        lambda countries: [
            country_to_iso3.get(country, "[n/a]") for country in countries
        ]
    )

    df[CTRY_FIRST] = df[CTRY].str[0]
    df[CTRY_ISO3_FIRST] = df[CTRY_ISO3].str[0]

    df[CTRY] = df[CTRY].apply(set)
    df[CTRY] = df[CTRY].apply(sorted)
    df[CTRY] = df[CTRY].str.join("; ")

    df[CTRY_ISO3] = df[CTRY_ISO3].apply(set)
    df[CTRY_ISO3] = df[CTRY_ISO3].apply(sorted)
    df[CTRY_ISO3] = df[CTRY_ISO3].str.join("; ")

    return df


def _create_organization_column(
    df: pd.DataFrame, organization_mapping: dict[str, str]
) -> pd.DataFrame:
    df = df.copy()

    df[ORG] = df[AFFIL_RAW].copy()
    df[ORG] = df[ORG].fillna("[n/a]")
    df[ORG] = df[ORG].str.split("; ")
    df[ORG] = df[ORG].apply(
        lambda affils: [organization_mapping.get(affil, "[n/a]") for affil in affils]
    )
    df[ORG_FIRST] = df[ORG].map(lambda orgs: orgs[0] if orgs else "[n/a]")
    df[ORG] = df[ORG].str.join("; ")

    return df


def _create_thesaurus_files(
    root_directory: str,
    countries: dict[str, str],
    organizations: dict[str, str],
) -> None:

    def _create_file(mapping: dict[str, str], filename: str) -> None:

        df = pd.DataFrame(
            {
                "key": list(mapping.values()),
                "value": list(mapping.keys()),
            }
        )

        grouped_df = df.groupby("key", as_index=False)["value"].apply(list)  # type: ignore

        filepath1 = Path(root_directory) / "ingest" / "processed/" / ("_" + filename)
        filepath2 = Path(root_directory) / "refine" / "thesaurus" / filename

        for filepath in [filepath1, filepath2]:

            with open(filepath, "w", encoding="utf-8") as file:

                for _, row in grouped_df.iterrows():
                    key = row["key"]
                    file.write(f"{key}\n")
                    for value in sorted(row["value"]):
                        file.write(f"    {value}\n")

    _create_file(countries, "ctry.the.txt")
    _create_file(organizations, "org.the.txt")
