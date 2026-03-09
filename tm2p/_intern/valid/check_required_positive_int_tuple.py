from typing import Tuple


def check_required_positive_int_tuple(
    tuple_values: Tuple[int, ...],
    param_name: str,
) -> Tuple[int, ...]:

    for i, val in enumerate(tuple_values):
        if not isinstance(val, int):
            raise TypeError(f"{param_name} value at index {i} ({val}) must be an int.")
        if val <= 0:
            raise ValueError(
                f"{param_name} value at index {i} ({val}) must be a positive int."
            )

    return tuple_values
