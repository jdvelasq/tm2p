import pandas as pd  # type: ignore

from tm2p.enum.column import COUNTERS, DEGREE, NAME, NODE


def create_node_degree_dataframe(node_degrees):
    """Converts a list of degrees to a dataframe."""

    dataframe = pd.DataFrame(
        node_degrees,
        columns=[
            NAME,
            DEGREE,
        ],
    )
    dataframe[COUNTERS] = dataframe[NAME].map(lambda x: x.split(" ")[-1])
    dataframe = dataframe.sort_values(
        by=[DEGREE, COUNTERS, NAME],
        ascending=[False, False, True],
    )
    dataframe = dataframe.reset_index(drop=True)
    dataframe[NODE] = dataframe.index
    dataframe = dataframe[[NODE, NAME, DEGREE]]

    return dataframe
