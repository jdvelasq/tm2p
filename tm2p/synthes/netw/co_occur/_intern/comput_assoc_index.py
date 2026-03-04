import numpy as np
import pandas as pd  # type: ignore

from tm2p import AssociationIndex


def comput_assoc_index(
    assoc_index: AssociationIndex, cooc_matrix: pd.DataFrame
) -> pd.DataFrame:

    if assoc_index == AssociationIndex.NONE:
        out = cooc_matrix.copy()
        out = out.map(float)
        for i in range(len(out)):
            out.iloc[i, i] = 0.0
        return out

    m = cooc_matrix.copy().map(float)

    if list(m.index) != list(m.columns):
        raise ValueError("cooc_matrix must be square with identical index/columns.")

    a = m.to_numpy(dtype=float, copy=False)
    diag = np.diag(a).copy()

    with np.errstate(divide="ignore", invalid="ignore"):

        if assoc_index.value == "JACCARD":
            den = diag[:, None] + diag[None, :] - a
            out = np.divide(a, den, out=np.zeros_like(a), where=den != 0)

        elif assoc_index.value == "DICE":
            den = diag[:, None] + diag[None, :]
            num = 2.0 * a
            out = np.divide(num, den, out=np.zeros_like(a), where=den != 0)

        elif assoc_index.value == "SALTON":
            den = np.sqrt(diag[:, None] * diag[None, :])
            out = np.divide(a, den, out=np.zeros_like(a), where=den != 0)

        elif assoc_index.value == "EQUIVALENCE":
            den = diag[:, None] * diag[None, :]
            num = a * a
            out = np.divide(num, den, out=np.zeros_like(a), where=den != 0)

        elif assoc_index.value == "INCLUSION":
            den = np.minimum(diag[:, None], diag[None, :])
            out = np.divide(a, den, out=np.zeros_like(a), where=den != 0)

        elif assoc_index.value == "ASSOCIATION":
            den = diag[:, None] * diag[None, :]
            out = np.divide(a, den, out=np.zeros_like(a), where=den != 0)

        elif assoc_index.value == "MUTUALINFO":
            total = a.sum()
            if total <= 0:
                out = np.zeros_like(a)
            else:
                p_ij = a / total
                p_i = diag / total
                den = p_i[:, None] * p_i[None, :]
                out = np.log(
                    np.divide(
                        p_ij, den, out=np.zeros_like(a), where=(p_ij > 0) & (den > 0)
                    )
                )

        else:
            raise KeyError(f"Unknown association index: {assoc_index.value}")

    np.fill_diagonal(out, 0.0)

    return pd.DataFrame(out, index=m.index, columns=m.columns)
