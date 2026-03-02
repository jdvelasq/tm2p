"""
Smoke test:
    >>> from pprint import pprint
    >>> import pandas as pd
    >>> from tm2p.ingest.data_sourc._intern.auth.normalize_auth_raw import _normalize
    >>> data = pd.Series([
    ...     "Chang, V.; Chen, Y.; (Justin) Zhang, Z.; Xu, Q.A.; Baudier, P.; Liu. B.S.C.",
    ...     "Guo Y., (1); Klink A., (2); Bartolo P., (1); Guo W.G.",
    ...     "Huang (黃新棫) X.-Y.; Chen (陳怡妏) Y.-W.; Yang (楊鏡堂) J.-T.",
    ...     "ALSHAREEF M., Jr.; Chang, V.-T.",
    ...     None,
    ...     "[No author name available]",
    ...     "Anonymous",
    ...     "Anon",
    ... ])
    >>> pprint(_normalize(data).tolist())
    ['Chang V.; Chen Y.; (Justin) Zhang Z.; Xu Q.A.; Baudier P.; Liu. B.S.C.',
     'Guo Y.; Klink A.; Bartolo P.; Guo W.G.',
     'Huang (黃新棫) X.-Y.; Chen (陳怡妏) Y.-W.; Yang (楊鏡堂) J.-T.',
     'Alshareef M., Jr.; Chang V.-T.',
     <NA>,
     <NA>,
     <NA>,
     <NA>]



"""

import pandas as pd  # type: ignore

from tm2p import Field
from tm2p.ingest.oper.transform_column import transform_column

from ..oper import DataFile


def _normalize(series: pd.Series) -> pd.Series:
    #
    # Chang V.; Chen Y.; (Justin) Zhang Z.; Xu Q.A.; Baudier P.; Liu B.S.C.
    #                 Guo Y., (1); Klink A., (2); Bartolo P., (1); Guo W.G.
    #           Huang (黃新棫) X.-Y.; Chen (陳怡妏) Y.-W.; Yang (楊鏡堂) J.-T.
    #                                            ALSHAREEF M.; Chang, V.-T.
    #                                                                   NaN
    #                                            [No author name available]
    #                                                             Anonymous
    #                                                                  Anon
    #
    series = series.str.replace(r", \(\d\)", "", regex=True)

    #

    series = series.str.replace(",", "", regex=False)
    series = series.str.replace("; ", ";", regex=False)
    series = series.str.replace(";", "; ", regex=False)
    series = series.str.replace(" Jr.", ", Jr.", regex=False)
    #
    # some old database records uses ',' as separator
    # text = text.str.replace(", ", ",", regex=False).str.replace(",", "; ", regex=False)

    series = series.str.title()
    series = series.fillna(pd.NA)
    series = series.map(
        lambda x: (
            pd.NA if isinstance(x, str) and x.startswith("[") and x.endswith("]") else x
        )
    )
    series = series.map(
        lambda x: pd.NA if isinstance(x, str) and x.lower() == "anonymous" else x
    )
    series = series.map(
        lambda x: pd.NA if isinstance(x, str) and x.lower() == "anon" else x
    )

    return series


def _extract_first_author(series: pd.Series) -> pd.Series:
    return series.str.split(";").str[0].str.strip()


def normalize_auth_raw(root_directory, file: DataFile) -> int:
    """Run authors importer."""

    transform_column(
        source=Field.AUTH_RAW,
        target=Field.AUTH_NORM,
        function=_normalize,
        root_directory=root_directory,
        file=file,
    )

    return transform_column(
        source=Field.AUTH_NORM,
        target=Field.AUTH_FIRST,
        function=_extract_first_author,
        root_directory=root_directory,
        file=file,
    )
