from tm2p import ItemOrderBy


def check_required_items_order_by_enum(
    value: ItemOrderBy, param_name: str
) -> ItemOrderBy:

    if not isinstance(value, ItemOrderBy):
        raise TypeError(
            f"{param_name} must be an ItemsOrderBy, got {type(value).__name__}"
        )

    return value
