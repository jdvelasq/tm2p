from enum import Enum


class Correlation(Enum):

    PEARSON = "pearson"
    SPEARMAN = "spearman"
    KENDALL = "kendall"
    COSINE = "cosine"
    MAXPROPORTIONAL = "maxproportional"
