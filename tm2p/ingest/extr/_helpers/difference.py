from tm2p._intern import Params
from tm2p.ingest.extr._helpers.values import extract_values


def extract_difference(params: Params) -> list[str]:

    source_fields = params.source_fields

    if not source_fields or len(source_fields) != 2:
        raise ValueError("Exactly two source fields must be provided")

    params.source_field = source_fields[0]
    set_a = set(extract_values(params).term)

    params.source_field = source_fields[1]
    set_b = set(extract_values(params).term)

    return sorted(set_a.difference(set_b))
