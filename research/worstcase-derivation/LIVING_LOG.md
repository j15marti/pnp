# Worst-case derivation complexity — living log

Shared objective (all five roles): W_R(N) = max_{F in UNSAT, |F|<=N} min_{pi: F |-_R bot} cost_R(pi).
Priority bridge B_R: SAT in P  =>  W_R(N) <= poly(N).
Strategy search is not charged (min over pi is free); this only makes lower bounds easier to state, not easier to prove.
Status labels per AGENTS.md. P vs NP remains OPEN. This log is additive; it changes no schedules or allocations.

Roles: (1) General lower-bound lead; (2) SAT-circuit reduction builder; (3) hypergraph and proof certificates; (4) time-space auditor; (5) red team.

## Entry 2026-11-08 (run WCD-0001, role: lead + red team)
Report: research/agents/claude/2026-11-08_WCD-0001_CLAUDE_BRIDGE-DICHOTOMY.tex
- PROVED/EXACT: for any R with an unconditional superpolynomial W_R, B_R is logically equivalent to "SAT not in P" (bridge = goal, no progress).
- KNOWN THEOREM: Cook-Reckhow: some poly-bounded system exists iff NP = coNP; Cook translation gives B_EF from PV-provable correctness of the SAT algorithm.
- Dichotomy for the multisign DAG hypergraph system H: either H is p-simulated by a system with known lower bounds (bridge fails or is equivalent to the goal), or H p-simulates EF (lower bound is the open EF problem).
- OPEN: bridge for EF without the provability hypothesis; any superpoly bound for EF; normal form of "minimal reduced state".
- Literature clue: Pich-Santhanam, "Towards P != NP from Extended Frege lower bounds" (arXiv 2312.08163) -- exact statement not verified here; read before next run.
- Next: (a) define H as a Cook-Reckhow system with an explicit extension rule or prove it has none; (b) locate H in the simulation lattice; (c) read Pich-Santhanam and Krajicek on provability gap.
