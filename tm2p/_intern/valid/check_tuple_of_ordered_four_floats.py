from typing import Tuple, Union, cast


def check_tuple_of_ordered_four_floats(
    value: Tuple[
        Union[float, int],
        Union[float, int],
        Union[float, int],
        Union[float, int],
    ],
    param_name: str,
) -> Tuple[float, float, float, float]:

    cast_value = tuple(float(v) for v in value)
    cast_value = cast(Tuple[float, float, float, float], cast_value)
    if not isinstance(cast_value, tuple) or len(cast_value) != 4:
        raise TypeError(
            f"{param_name} must be a tuple of four floats, got {type(cast_value).__name__} with length {len(cast_value) if isinstance(cast_value, tuple) else 'N/A'}"
        )
    for i, v in enumerate(cast_value):
        if not isinstance(v, float):
            raise TypeError(
                f"{param_name}[{i}] must be a float, got {type(v).__name__}"
            )
    if not cast_value[0] <= cast_value[1] <= cast_value[2] <= cast_value[3]:
        raise ValueError(
            f"{param_name} values must be ordered: {cast_value[0]} ≤ {cast_value[1]} ≤ {cast_value[2]} ≤ {cast_value[3]}"
        )
    return value
