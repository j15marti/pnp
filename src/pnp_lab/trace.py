"""Primitive-trace accounting helpers for battery/ratchet experiments."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class TraceStep:
    label: str
    cost: float
    potential_before: float
    potential_after: float
    metadata: dict[str, Any] | None = None

    @property
    def discharge(self) -> float:
        return self.potential_before - self.potential_after


def total_cost(steps: list[TraceStep]) -> float:
    return sum(step.cost for step in steps)


def potential_drop(steps: list[TraceStep]) -> float:
    if not steps:
        return 0.0
    return steps[0].potential_before - steps[-1].potential_after


def lipschitz_violations(steps: list[TraceStep], factor: float = 1.0) -> list[TraceStep]:
    """Return steps violating discharge <= factor * cost."""
    if factor < 0:
        raise ValueError("factor must be nonnegative")
    return [step for step in steps if step.discharge > factor * step.cost + 1e-12]


def validate_continuity(steps: list[TraceStep], tolerance: float = 1e-12) -> bool:
    return all(
        abs(a.potential_after - b.potential_before) <= tolerance
        for a, b in zip(steps, steps[1:])
    )
