# CODE_REVIEW: 2026-01-26
"""
OpenAlex
===============================================================================

Smoke test - fintech - successful import:
    >>> from tm2p.ingest.datab import OpenAlex
    >>> result = (
    ...     OpenAlex()
    ...     .where_root_directory("tests/openalex/")
    ...     .run()
    ... )
    >>> result.success
    True






"""


from ._intern import Step
from ._intern.base_ingest import BaseIngest

__reviewed__ = "2026-01-28"


class OpenAlex(BaseIngest):
    """:meta private:"""

    _02_COMPRESS = "Compressing raw data"
    _03_PARS = "Parsing data"
    _04_FILTER = "Filtering data"
    _05_STRUCT_STAND = "Standarizing fields"
    _06_FIELD_NORMAL = "Normalizing fields"
    _07_ENRICH = "Enrichment"
    _08_SEMANT_KW_PREPAR = "Perparing KW"
    _09_SEMANT_NLP_PREPAR = "Preparing semanitc NLP"
    _10_CONCEPT = "Extracting concepts"
    _11_REVIEW = "Reviewing"

    # ------------------------------------------------------------------------
    # Execution
    # ------------------------------------------------------------------------

    def ingestion_pipeline(self) -> tuple[tuple[str, list[Step]], ...]:

        from ._intern.phases.p02_compress import build_openalex_compress_steps
        from ._intern.phases.p03_pars import build_openalex_pars_steps
        from ._intern.phases.p04_filter import build_openalex_filter_steps
        from ._intern.phases.p05_struct_stand import build_openalex_struct_stand_steps
        from ._intern.phases.p06_field_normal import build_openalex_field_normal_steps
        from ._intern.phases.p07_enrich import build_openalex_enrich_steps
        from ._intern.phases.p08_semant_kw_prepar import build_semant_kw_prepar_steps
        from ._intern.phases.p09_semant_nlp_prepar import build_semant_nlp_prepar_steps
        from ._intern.phases.p10_concept import build_concept_steps
        from ._intern.phases.p12_review import build_review_steps

        return (
            (self._02_COMPRESS, build_openalex_compress_steps(self.params)),
            (self._03_PARS, build_openalex_pars_steps(self.params)),
            (self._04_FILTER, build_openalex_filter_steps(self.params)),
            (self._05_STRUCT_STAND, build_openalex_struct_stand_steps(self.params)),
            (self._06_FIELD_NORMAL, build_openalex_field_normal_steps(self.params)),
            (self._07_ENRICH, build_openalex_enrich_steps(self.params)),
            (self._08_SEMANT_KW_PREPAR, build_semant_kw_prepar_steps(self.params)),
            (self._09_SEMANT_NLP_PREPAR, build_semant_nlp_prepar_steps(self.params)),
            (self._10_CONCEPT, build_concept_steps(self.params)),
            (self._11_REVIEW, build_review_steps(self.params)),
        )
