# Shared worst-case derivation directive (WCD) — 2026-11-06

Status: additive research directive. Changes no schedules, agent count or role ownership. P versus NP remains **OPEN**.

Objective (all five roles): study
W̄_R(N) = max over UNSAT F with |<F>|<=N of min over refutations π of cost_R(π), for a fixed multi-sign DAG hypergraph inference system R.
Free knowledge of the optimal π is granted (search cost is not charged to the minimum).

Priority bridge: SAT ∈ P ⇒ W̄_R(N) <= poly(N). Secondary: pointwise / worst-case simulation theorems.

Roles: General SAT Lower-Bound Lead (formalize W̄_R, weakest transfer theorem); SAT-Circuit Reduction Builder (fixed combined system, certified shortest DAGs); Hypergraph & Proof Certificates (hard UNSAT families vs resolution/algebraic/circuit/shared-DAG/adaptive switching); Time-Space Resource Auditor (inference costs, encodings, peak memory); Independent Proof Red Team (counterexamples, shorter derivations, failed transfers).

Living log: `research/worstcase/WCD_LIVING_LOG.md` (append-only entries, newest last). Every run checks the literature for clues and records them there.
Reports: `research/agents/claude/YYYY-MM-DD_HHMM_CLAUDE_<ID>.tex`.
