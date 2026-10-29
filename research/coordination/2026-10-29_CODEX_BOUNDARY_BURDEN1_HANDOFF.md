# BOUNDARY_BURDEN1 handoff

29 October 2026, Los Angeles. No schedules, task identities, role states or ownership changed. P versus NP remains OPEN.

The requested real-instance test is in `research/explorations/boundary-burden/`. Read the full report and raw results before promoting the result. Restricted mathematical derivation has a complete proof; independent referee review is pending. Finite controls are COMPUTATIONAL.

New elementary strengthening: if h is the number of source clauses entirely in a boundary Y, contracting every private module plus its incident clauses gives a connected multigraph with b+k+h vertices and 4b edges. Therefore k+h <=3b+1. This works for every valid original static partition, including grouped components; b=0 gives k=1. Combining n<=3(b+sum|H_i|) with max |H_i|=q gives n<=3(b+q)+9bq and s=b+q >= (2/3)(sqrt(n+1)-1). The user's original sqrt(n/3)-1/4 bound remains valid. For integers use n<=3s+9 floor(s^2/4); with n divisible by three this equals the ceiling of the new continuous bound.

Exact small audit: all 70,208 boundaries on periodic n=6,9,12,15 and authenticated UNSAT W1 n=15. For fixed boundary the finest private components minimize the largest local hitting minimum, so these are global static-architecture optima. W1 and same-scope SAT V both have exact minimum b+q=5; the original rounded floor is 2. W1 has zero models, V 54, checked exhaustively. Sign-insensitive hitting burden cannot distinguish their labels.

Larger matched cycles n=60,120,240 achieve burdens 9,13,18 using tested port cuts. Matched torus/connector pairs n=81,189,621 achieve 28,64,176. These are verified feasible decompositions, not global optima over boundaries; local HiGHS optimal statuses are numerical finite evidence without extracted dual certificates. Ordinary independent capped DPLL decided all measured SAT and UNSAT sources. Torus UNSAT used 752 recursive nodes at all three sizes, reflecting a fixed easy core and confirming the prior report's promise-tractability warning.

Periodic n=600 requires static s>=16 by the new theorem, but moving frontier DP uses width four, peak 13 states and 15,512 transitions on the actual source. Thus no actual all-algorithm runtime lower bound follows from 2^(b+q). This is not a counterexample to the static theorem.

Original Connected_Interface_Audit.zip was freshly downloaded and audit.py reproduced archived results exactly, 4680/7191/139. New inputs and hashes are retained; the new code is self-contained with its three input modules. All stage invocations in this run were under three seconds. New report, code, raw data, CSV and explicit DIMACS fixtures are included.

Preflight reads current root as substantive but without the older specialist marker pattern. It reports marker failures. No unowned root edit is made; LSPV-5 owns any synthesis repair and adoption after independent review.

Next target: exact source-dependent lower and matching upper bounds for the attainable static burden on an increasing connected exact22 family; any transfer to arbitrary decision runtime needs a separate necessity theorem.
