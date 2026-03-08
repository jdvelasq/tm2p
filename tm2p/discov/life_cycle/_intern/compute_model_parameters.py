from scipy.optimize import curve_fit  # type: ignore

from tm2p.anal.annual_metrics import Metrics as AnnualMetrics
from tm2p.anal.annual_metrics.column import Column as AnnualColumn

from .logistic import logistic


def compute_model_parameters(params):

    metrics = AnnualMetrics().update(**params.__dict__).run()
    years = metrics.index.values
    annual_counts = metrics[AnnualColumn.OCC.value].values
    cumulative = metrics[AnnualColumn.CUMUL_OCC.value].values

    fit_result = curve_fit(
        logistic,
        years,
        cumulative,
        p0=[cumulative.max() * 2, 0.3, years.mean()],
        maxfev=10000,
    )
    popt = fit_result[0]
    K, r, t0 = popt

    return K, r, t0, years, annual_counts, cumulative
