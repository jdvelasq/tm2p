from tm2p._intern import Params
from tm2p.ingest.extr._helpers.values import extract_values


def extract_endswith(params: Params) -> list[str]:

    df = extract_values(params)
    return (
        df[df.term.str.endswith(params.pattern)]  # type: ignore
        .dropna()
        .sort_values(by="term", ascending=True)
        .term.tolist()
    )
