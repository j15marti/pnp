from pnp_lab.trace import (
    TraceStep,
    lipschitz_violations,
    potential_drop,
    total_cost,
    validate_continuity,
)


def test_primitive_trace_accounting():
    steps = [
        TraceStep("a", cost=1, potential_before=5, potential_after=4),
        TraceStep("b", cost=2, potential_before=4, potential_after=2),
    ]
    assert validate_continuity(steps)
    assert total_cost(steps) == 3
    assert potential_drop(steps) == 3
    assert lipschitz_violations(steps, factor=1) == []


def test_detects_free_macro_discharge():
    step = TraceStep("free-shortcut", cost=1, potential_before=100, potential_after=0)
    assert lipschitz_violations([step], factor=1) == [step]
