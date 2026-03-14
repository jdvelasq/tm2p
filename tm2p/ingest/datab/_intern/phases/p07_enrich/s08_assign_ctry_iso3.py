from tm2p import Field
from tm2p._intern.packag_data import load_builtin_mapping
from tm2p.ingest.oper.transform_column import transform_column


def s08_assign_ctry_iso3(root_directory: str) -> int:

    country_to_iso3 = load_builtin_mapping("country_to_alpha3.json")

    def _transform(series):

        series = series.copy()
        series = series.str.split("; ")
        series = series.map(
            lambda countries: [
                country_to_iso3.get(country, "[UNKNOWN]") for country in countries
            ],
            na_action="ignore",
        )
        series = series.map(set, na_action="ignore")
        series = series.map(sorted, na_action="ignore")
        series = series.str.join("; ")

        return series

    return transform_column(
        source=Field.CTRY,
        target=Field.CTRY_ISO3,
        function=_transform,
        root_directory=root_directory,
    )
