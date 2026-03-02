from typing import Union


def check_required_str_or_str_tuple(
    value: Union[str, tuple[str, ...]], param_name: str
) -> Union[str, tuple[str, ...]]:

    if not isinstance(value, tuple):
        value = (value,)
    for i, item in enumerate(value):
        if not isinstance(item, str):
            raise TypeError(
                f"All items in {param_name} must be strings. "
                f"Item at index {i} is of type {type(item).__name__}"
            )

    return value
