# CODE_REVIEW: 2025-01-26
"""
Step
===============================================================================

Smoke test - basic instantiation:
    >>> from tm2p.ingest.data_sourc._intern import Step
    >>> def sample_function(x, y):
    ...     return x + y
    >>> step = Step(
    ...     name="Add values",
    ...     function=sample_function,
    ...     kwargs={"x": 5, "y": 3}
    ... )
    >>> step.name
    'Add values'
    >>> step()
    8

Smoke test - with count message:
    >>> step_with_count = Step(
    ...     name="Process items",
    ...     function=lambda data: len(data),
    ...     kwargs={"data": [1, 2, 3]},
    ...     count_message="Processed {count} items"
    ... )
    >>> step_with_count.count_message
    'Processed {count} items'

Smoke test - default count message:
    >>> step_no_count = Step(
    ...     name="Transform",
    ...     function=lambda s: s.upper(),
    ...     kwargs={"s": "hello"}
    ... )
    >>> step_no_count.count_message is None
    True

"""
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any, Callable, Optional


@dataclass(frozen=True)
class Step:

    name: str
    function: Callable[..., Any]
    kwargs: Mapping[str, Any]
    count_message: Optional[str] = None

    def __post_init__(self):
        if not callable(self.function):
            raise TypeError(
                f"argument 'function' must be callable, got {type(self.function).__name__!r}"
            )

    def __call__(self) -> Any:
        return self.function(**self.kwargs)
