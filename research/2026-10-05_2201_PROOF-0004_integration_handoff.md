# PROOF-0004 integration handoff

GitHub accepted the detailed PROOF-0004 theorem report but blocked direct replacement writes to main2.tex during this run. No main2/main3 update is claimed.

## Text to integrate into main2/main3

PROOF-0004 proves LINEAR-SEPARATOR-EQUIV1: for every nonempty final Boolean range R in F_2^m, a nonconstant affine Boolean function D(x)=a dot x + b rejects every point of R if and only if aff(R) is a proper affine subspace of F_2^m. Such D is exactly half-dense. If 0 belongs to R, b=0 and the condition is equivalent to span(R) being proper.

Consequence for the Drive COMMON-LINEAR/SCD clue: succinct constraint detection can efficiently expose dual constraints that exist in an upstream linear code/view, but it does not prove that the exact final RMV Boolean range has a common parity separator. After nonlinear/adaptive extraction and Boolean postprocessing, one must separately prove final-range affine-rank deficiency. That remains OPEN.

Barrier status: LINEAR-SEPARATOR-EQUIV1 is finite linear algebra and relativizes/algebrizes. It is not a runtime lower bound or nonrelativizing hinge.

Suggested theorem-to-gap row:
LINEAR-SEPARATOR-EQUIV1 | exact existence criterion for affine/parity separator | exact final RMV affine-rank deficiency remains OPEN

Canonical detailed report:
research/2026-10-05_2201_PROOF-0004_linear_separator_boundary.md
