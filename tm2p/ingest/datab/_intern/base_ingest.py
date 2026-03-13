import sys
import time
from abc import ABC, abstractmethod
from datetime import timedelta
from typing import Any

from tm2p._intern import ParamsMixin

from .._intern import Step
from .ingest_result import IngestResult
from .phases.p01_scaffold.create_project_structure import create_project_structure


class BaseIngest(
    ABC,
    ParamsMixin,
):

    _HEADER_WIDTH = 80
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
        self._write(f"\n{separator}\nImporting Data\n{separator}\n")

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

    def _execute_step(self, step: Step) -> None:
        self._print_step(step.name)
        result = step()

        if step.count_message:
            self._print_step_result(result, step.count_message)

    def run(self) -> IngestResult:

        start_time = time.monotonic()
        self._print_header()

        create_project_structure(str(self.params.root_directory))

        for phase_index, (phase_name, steps) in enumerate(
            self.ingestion_pipeline(), start=1
        ):
            self._print_phase(phase_index, phase_name)
            for step in steps:
                self._execute_step(step)

        end_time = time.monotonic()
        elapsed = timedelta(seconds=end_time - start_time)
        status = f"Execution time : {self._format_elapsed_time(elapsed)}"

        return IngestResult(
            colored_output=self.params.colored_output,
            file_path=str(self.params.root_directory),
            msg="Data imported successfully.",
            success=True,
            status=status,
        )

    @abstractmethod
    def ingestion_pipeline(self) -> tuple[tuple[str, list[Step]], ...]:
        pass
