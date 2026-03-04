import pandas as pd  # type: ignore

from tm2p.enum import Indicator


def create_node_degrees_data_frame(node_degrees):
    """Converts a list of degrees to a dataframe."""

    dataframe = pd.DataFrame(
        node_degrees,
        columns=[
            Indicator.NAME.value,
            Indicator.DEGREE.value,
        ],
    )
    dataframe[Indicator.COUNTERS.value] = dataframe[Indicator.NAME.value].map(
        lambda x: x.split(" ")[-1]
    )
    dataframe = dataframe.sort_values(
        by=[Indicator.DEGREE.value, Indicator.COUNTERS.value, Indicator.NAME.value],
        ascending=[False, False, True],
    )
    dataframe = dataframe.reset_index(drop=True)
    dataframe[Indicator.NODE.value] = dataframe.index
    dataframe = dataframe[
        [Indicator.NODE.value, Indicator.NAME.value, Indicator.DEGREE.value]
    ]

    return dataframe
