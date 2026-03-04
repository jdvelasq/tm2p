from enum import Enum


class AssociationIndex(Enum):

    JACCARD = "jaccard"
    DICE = "dice"
    SALTON = "salton"
    EQUIVALENCE = "equivalence"
    INCLUSION = "inclusion"
    MUTUALINFO = "mutualinfo"
    ASSOCIATION = "association"
    NONE = "none"
