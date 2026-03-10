"""
ReprocessNounPhrases
===============================================================================

Smoke test:
    >>> from tm2p.ingest.rev import ReprocessNounPhrases
    >>> (
    ...     ReprocessNounPhrases()
    ...     .where_root_directory("tests/scopus/")
    ... ).run()


"""

import sys
from typing import Any

from tm2p._intern import ParamsMixin
from tm2p.ingest.data_sourc._intern.step import Step

from ..data_sourc._intern.concept.build_steps import build_concept_steps

__reviewed__ = "2026-01-28"


class ReprocessNounPhrases(
    ParamsMixin,
):
    """:meta private:"""

    _HEADER_WIDTH = 70
    _STEP_PREFIX = "  → "
    _DETAIL_PREFIX = "    "

    # -------------------------------------------------------------------------
    # I/O
    # -------------------------------------------------------------------------

    def _write(self, text: str) -> None:
        sys.stderr.write(text)
        sys.stderr.flush()

    def _print_header(self) -> None:
        separator = "=" * self._HEADER_WIDTH
        self._write(f"\n{separator}\nReprocessing noun phrases\n{separator}\n")

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

    # ------------------------------------------------------------------------
    # Execution
    # ------------------------------------------------------------------------

    def _execute_step(self, step: Step) -> None:
        self._print_step(step.name)
        result = step()

        if step.count_message:
            self._print_step_result(result, step.count_message)

    def run(self) -> None:

        self._print_header()
        for step in build_concept_steps(params=self.params):
            self._execute_step(step)
