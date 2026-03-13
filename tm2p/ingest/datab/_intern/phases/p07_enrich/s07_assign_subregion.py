from tm2p import Field
from tm2p._intern.packag_data import load_builtin_mapping
from tm2p.ingest.oper.transform_column import transform_column


def s07_assign_subregion(root_directory: str) -> int:

    country_to_iso3 = load_builtin_mapping("country_to_subregion.json")

    def _transform(series):

        series = series.copy()
        series = series.str.split("; ")
        series = series.apply(
            lambda countries: [
                country_to_iso3.get(country, "[n/a]") for country in countries
            ]
        )
        series = series.apply(set)
        series = series.apply(sorted)
        series = series.str.join("; ")

        return series

    return transform_column(
        source=Field.CTRY,
        target=Field.SUBREGION,
        function=_transform,
        root_directory=root_directory,
    )
