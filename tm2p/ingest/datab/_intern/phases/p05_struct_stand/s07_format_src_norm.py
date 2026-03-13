from tm2p.enum import Field
from tm2p.ingest.datab._intern.oper import transform_column


def s07_format_src_norm(root_directory: str) -> int:

    def _normalize(text):
        text = text.str.replace("<.*?>", "", regex=True)
        return text

    return transform_column(
        source=Field.SRC_RAW,
        target=Field.SRC_NORM,
        function=_normalize,
        root_directory=root_directory,
    )
