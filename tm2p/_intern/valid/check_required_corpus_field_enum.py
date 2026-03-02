from tm2p import Field


def check_required_corpus_field_enum(value: Field, param_name: str) -> Field:

    if not isinstance(value, Field):
        raise TypeError(f"{param_name} must be a Field, got {type(value).__name__}")

    return value
