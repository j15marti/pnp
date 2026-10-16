# GUARDCOVER1 | 2026-10-16 23:21 KST

STATUS: PROVED/EXACT, restricted guarded SAT architecture. COMPUTATIONAL finite testing. Arbitrary-decider contraction OPEN. No P versus NP separation claimed.

Source-only structural guard C(F) recognizes ordered variable-disjoint CNF bins, at most N^0.401 children each encoded at most N^0.6 bits. Two-pass verification and serial materialization preserve SAT by AND of child answers. The bounds on marked inputs are t' <= max(1,0.401+0.6t) and s' <= max(0.6,0.6s), with child buffers charged.

Define G(A) as guarded decomposition on C(F), but a completed full-size A(F) fallback elsewhere. For every unmarked F and finite j, G^j(A)(F) executes A(F). Under a hypothetical polynomial SAT algorithm A0, prepend N^d dummy transitions to obtain another correct polynomial SAT algorithm A_d. On unmarked inputs, every iterate retains Omega(N^d) time. This violates an intended universal improving recurrence t' <= max(1.051,0.401+0.6d) once d is sufficiently large. It refutes this guarded fallback, not P=NP.

The conditional materialized target (1.051,0.6) still lies inside the FLMV sufficient time-space forbidden region. An all-input source-only replacement would already be forbidden by recursive query erasure.

15,370 checks passed, including repeated wrappers and unmarked crossings. Local artifacts: GUARDCOVER1 report.tex, test_guardcover1.py, raw.json and refs_guardcover1.bib. Next: genuinely decider-dependent, fully charged all-input coverage with no parent-sized fallback.

END_GUARDCOVER1_2321