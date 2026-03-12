# CODE_REVIEW: 2026-01-26
"""
WoS
===============================================================================

Smoke test - fintech - successful import:
    >>> from tm2p.ingest.datab.wos import WoS
    >>> result = (
    ...     WoS()
    ...     .where_root_directory("tests/wos/")
    ...     .run()
    ... )
    >>> result.success
    True

"""


from ._intern import Step

# from .._intern._affil.build_steps import build_affiliation_steps
# from .._intern._auth.build_steps import build_author_steps
# from .._intern._concept.build_steps import build_concept_steps
# from .._intern._doc.build_steps import build_document_steps
# from .._intern._kw.build_steps import build_keyword_steps
# from .._intern._ref.build_steps import build_reference_steps
# from .._intern._review.build_steps import build_review_steps
# from .._intern._src.build_steps import build_source_title_steps
from ._intern.base_ingest import BaseIngest

__reviewed__ = "2026-01-28"


class WoS(BaseIngest):
    """:meta private:"""

    # _AFFILIATIONS = "Processing affiliations"
    # _AUTHORS = "Processing authors"
    # _DOCUMENT = "Processing document information"
    # _INGEST = "Ingesting data"
    # _KEYWORDS = "Processing keywords"
    # _REFERENCES = "Processing references"
    # _SCAFFOLDING = "Building project scaffold"
    # _SOURCE_TITLE = "Processing source titles"
    # _CONCEPTS = "Processing concepts"
    # _REVIEW = "Extracting data for review"

    _COMPRESS = "Compressing raw data"
    _PARSING = "Parsing data"
    _STRUCT_STAND = "Structural standardization"
    _FIELD_NORMAL = "Field normalization"

    # ------------------------------------------------------------------------
    # Execution
    # ------------------------------------------------------------------------

    def ingestion_pipeline(self) -> tuple[tuple[str, list[Step]], ...]:

        from ._intern.phases.p02_compress import build_wos_compress_steps
        from ._intern.phases.p03_pars import build_wos_parsing_steps
        from ._intern.phases.p04_struct_stand import build_wos_struct_stand_steps
        from ._intern.phases.p05_field_normal import build_wos_field_normal_steps

        return (
            (self._COMPRESS, build_wos_compress_steps(self.params)),
            (self._PARSING, build_wos_parsing_steps(self.params)),
            (self._STRUCT_STAND, build_wos_struct_stand_steps(self.params)),
            (self._FIELD_NORMAL, build_wos_field_normal_steps(self.params)),
            #
            #
            # (self._INGEST, build_merging_steps(self.params)),
            # (self._AFFILIATIONS, build_affiliation_steps(self.params)),
            # (self._AUTHORS, build_author_steps(self.params)),
            # (self._DOCUMENT, build_document_steps(self.params)),
            # (self._KEYWORDS, build_keyword_steps(self.params)),
            # (self._SOURCE_TITLE, build_source_title_steps(self.params)),
            # (self._REFERENCES, build_reference_steps(self.params)),
            # (self._CONCEPTS, build_concept_steps(self.params)),
            # (self._REVIEW, build_review_steps(self.params)),
        )
