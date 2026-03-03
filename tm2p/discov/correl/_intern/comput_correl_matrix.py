import numpy as np  # type: ignore
import pandas as pd  # type: ignore
from sklearn.metrics.pairwise import cosine_similarity

from tm2p import Correlation
from tm2p._intern import Params


def _compute_similarity(x: pd.Series, y: pd.Series, method: Correlation) -> float:
    if method == Correlation.COSINE:
        return cosine_similarity(x.values.reshape(-1, 1), y.values.reshape(-1, 1))[0][0]  # type: ignore
    elif method in (Correlation.PEARSON, Correlation.SPEARMAN, Correlation.KENDALL):
        corr = x.corr(other=y, method=method.value)
        return max(0.0, corr)
    else:
        raise ValueError(f"Unknown correlation method: {method}")


def comput_correl_matrix(
    params: Params,
    tfidf: pd.DataFrame,
):
    """:meta private:"""

    tfidf = tfidf.copy()

    if params.correlation_method == Correlation.MAXPROPORTIONAL:

        co_occ = tfidf.T @ tfidf
        freq = np.array(tfidf.sum(axis=0)).ravel()
        den = np.maximum.outer(freq, freq)
        mpc = co_occ / den
        mpc[np.isnan(mpc)] = 0.0

        return pd.DataFrame(
            mpc,
            columns=tfidf.columns.to_list(),
            index=tfidf.columns.to_list(),
        )

    corr_matrix = pd.DataFrame(
        0.0,
        columns=tfidf.columns.to_list(),
        index=tfidf.columns.to_list(),
    )

    for col in tfidf.columns:
        for row in tfidf.columns:
            corr = _compute_similarity(
                x=tfidf[col],
                y=tfidf[row],
                method=params.correlation_method,
            )
            corr_matrix.loc[row, col] = corr
            corr_matrix.loc[col, row] = corr

    return corr_matrix
