from tm2p import Field
from tm2p.ingest.datab._intern.oper import count_column_items


def calculate_numauth(root_directory):

    return count_column_items(
        source=Field.AUTH_NORM,
        target=Field.N_AUTH,
        root_directory=root_directory,
    )
