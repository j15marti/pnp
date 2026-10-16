# CROSS-TRACK REFLECTIONRESTRICT2

2026-10-16 10:59 Asia/Seoul. P versus NP: OPEN.

Established: For odd-charge cubic-expander Tseitin 3-CNF F, construct selector-guarded soundness formula H = (AND over C in F: s_C) AND (AND over all proper 3-clauses C: (NOT s_C OR C)). Setting s_C=1 on F and zero outside F restricts H to F exactly. Hence ordinary Resolution complexity of H is at least that of F, exponentially large by the known expander Tseitin lower bound. The UNSAT recognizer that checks designated selector bits runs in polynomial time and is sound on every selected formula, but does not decide arbitrary SAT. This is a fixed-proof-system reflection firewall, not a SAT runtime lower bound.

Finite computational audit: K4, triangular prism, cube Q3; exact restriction verified for all three, with 62 selector-superset tests. See attached reflection_restriction_audit.py and reflection_restriction_results.json in run artifacts.

Critical open arrow: arbitrary globally polynomial SAT decider trace to source-exact, fully charged ordinary proof-system refutation. Resource contraction must charge source accesses, construction, memory, recursion, and emission. WRAPPER must pass the TQBF oracle control. UWI must have one same satisfiable input for all eligible programs.

Next assignments: Proof Transport to formalize source-exact reflection; Resource Contraction to charge decoder; Universal Obstruction to test same-input satisfiable adaptation; Nonrelativizing Simulation to audit oracle bypass.
