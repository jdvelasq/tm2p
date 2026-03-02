from tm2p._intern import Params
from tm2p.ingest.extr._helpers.values import extract_values


def extract_contains(params: Params) -> list[str]:

    df = extract_values(params)

    if isinstance(params.pattern, str):
        params.pattern = (params.pattern,)

    items = set()
    for pattern in params.pattern:
        items.update(
            df[
                df.term.str.contains(
                    pat=pattern,
                    case=params.case_sensitive,
                    flags=params.regex_flags,
                )
            ]
            .dropna()
            .term.tolist()
        )

    return sorted(items)
