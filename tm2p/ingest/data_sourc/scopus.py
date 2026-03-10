# CODE_REVIEW: 2026-01-26
"""
Scopus
===============================================================================

Smoke test - fintech - successful import:
    >>> from tm2p.ingest.data_sourc.scopus import Scopus
    >>> result = (
    ...     Scopus()
    ...     .where_root_directory("tests/scopus/")
    ...     .run()
    ... )  # doctest: +SKIP
    >>> result.success  # doctest: +SKIP
    True

Smoke test - fintech - result attributes:
    >>> result.file_path  # doctest: +SKIP
    'tests/fintech/'
    >>> result.status.startswith('Execution time :')  # doctest: +SKIP
    True

Smoke test - fintech - fluent interface:
    >>> scopus = Scopus()
    >>> scopus_configured = scopus.where_root_directory("tests/scopus/")
    >>> scopus_configured is scopus
    True

Smoke test - regtech - successful import:
    >>> from tm2p.ingest.data_sourc.scopus import Scopus
    >>> result = (
    ...     Scopus()
    ...     .where_root_directory("tests/regtech/")
    ...     .run()  # doctest: +SKIP
    ... )
    >>> result.success  # doctest: +SKIP
    True




"""

import sys
import time
from datetime import timedelta
from typing import Any

from tm2p._intern import ParamsMixin

from ._intern import Step
from ._intern.affil.build_steps import build_affiliation_steps
from ._intern.auth.build_steps import build_author_steps
from ._intern.concept.build_steps import build_concept_steps
from ._intern.doc.build_steps import build_document_steps
from ._intern.kw.build_steps import build_keyword_steps
from ._intern.ref.build_steps import build_reference_steps
from ._intern.review.build_steps import build_review_steps
from ._intern.scaffold.build_steps import build_scaffolding_steps
from ._intern.scopus_result import ScopusResult
from ._intern.src.build_steps import build_source_title_steps

__reviewed__ = "2026-01-28"


class Scopus(ParamsMixin):
    """:meta private:"""

    _HEADER_WIDTH = 70
    _STEP_PREFIX = "  → "
    _DETAIL_PREFIX = "    "

    _AFFILIATIONS = "Processing affiliations"
    _AUTHORS = "Processing authors"
    _DOCUMENT = "Processing document information"
    _KEYWORDS = "Processing keywords"
    _REFERENCES = "Processing references"
    _SCAFFOLDING = "Building project scaffold"
    _SOURCE_TITLE = "Processing source titles"
    _CONCEPTS = "Processing concepts"
    _REVIEW = "Extracting data for review"

    # -------------------------------------------------------------------------
    # I/O
    # -------------------------------------------------------------------------

    def _write(self, text: str) -> None:
        sys.stderr.write(text)
        sys.stderr.flush()

    def _print_header(self) -> None:
        separator = "=" * self._HEADER_WIDTH
        self._write(f"\n{separator}\nImporting Scopus Data\n{separator}\n")

    def _print_phase(self, index: int, description: str) -> None:
        self._write(f"\n[{index}] {description}\n")

    def _print_step(self, message: str) -> None:
        self._write(f"{self._STEP_PREFIX}{message}...\n")

    def _print_detail(self, message: str) -> None:
        self._write(f"{self._DETAIL_PREFIX}{message}\n")

    def _print_step_result(self, result: Any, count_message: str) -> None:
        if isinstance(result, dict):
            for key, value in result.items():
                self._print_detail(f"{key}: {value}")
        elif isinstance(result, list):
            count = len(result)
            if count > 0:
                self._print_detail(count_message.format(count=count))
        elif isinstance(result, int):
            if result > 0:
                self._print_detail(count_message.format(count=result))

    def _format_elapsed_time(self, elapsed: timedelta) -> str:
        total_seconds = int(elapsed.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}"

    # ------------------------------------------------------------------------
    # Execution
    # ------------------------------------------------------------------------

    def _pipeline(self) -> tuple[tuple[str, list[Step]], ...]:
        return (
            (self._SCAFFOLDING, build_scaffolding_steps(self.params)),
            (self._AFFILIATIONS, build_affiliation_steps(self.params)),
            (self._AUTHORS, build_author_steps(self.params)),
            (self._DOCUMENT, build_document_steps(self.params)),
            (self._KEYWORDS, build_keyword_steps(self.params)),
            (self._SOURCE_TITLE, build_source_title_steps(self.params)),
            (self._REFERENCES, build_reference_steps(self.params)),
            (self._CONCEPTS, build_concept_steps(self.params)),
            (self._REVIEW, build_review_steps(self.params)),
        )

    def _execute_step(self, step: Step) -> None:
        self._print_step(step.name)
        result = step()

        if step.count_message:
            self._print_step_result(result, step.count_message)

    def run(self) -> ScopusResult:

        start_time = time.monotonic()
        self._print_header()

        for phase_index, (phase_name, steps) in enumerate(self._pipeline(), start=1):
            self._print_phase(phase_index, phase_name)
            for step in steps:
                self._execute_step(step)

        end_time = time.monotonic()
        elapsed = timedelta(seconds=end_time - start_time)
        status = f"Execution time : {self._format_elapsed_time(elapsed)}"

        return ScopusResult(
            colored_output=self.params.colored_output,
            file_path=str(self.params.root_directory),
            msg="Data imported successfully.",
            success=True,
            status=status,
        )
