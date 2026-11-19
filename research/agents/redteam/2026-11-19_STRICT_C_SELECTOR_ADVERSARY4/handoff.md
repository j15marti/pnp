# STRICT-C-SELECTOR-ADVERSARY4 handoff — 19 November 2026 Pacific

Role: adversarial explicit inputs against selectors. Canonical relation: strict symmetric C only. Historical Q data is a provenance control. P versus NP OPEN; independent peer review PENDING.

**PROVED/EXACT restricted:** Three Mycielski lifts of C5 give a 47-vertex, 236-edge, 6-chromatic graph. Replacing every edge uv by one fresh private-head clause C(h_e,u,v) gives a 283-variable, 236-clause, clause-minimal UNSAT strict-C instance. The full supplied orientation/capacity and pentagon-distance filters both pass.

Every edge deletion has a directly verified strict-C witness. On deletion row z_e, e is the unique monochromatic edge and hence the unique refutable block. All 236 selector outputs occur. Therefore every row-independent block cover must contain all 236 blocks; any proper fixed shortlist fails. This is not an unrestricted lower bound: the source is recognizable, a row-dependent selector may inspect the colors/graph, and the natural decomposition has 5^47 rows rather than the promised N^.195 rows.

**Migration firewall:** All 236 historical Q tail colorings matched the independently rebuilt recursive tails. Zero Q heads were reused. The run reconstructed 55,696 C heads and checked 55,696 original C clauses. C/Q/P counts are 30/60/20. Fixed incidence girth is eight; no primal-girth or growing-girth claim.

**Executed:** producer 3.57 seconds before serialization; 17,310,416-byte Python tracemalloc peak with all witnesses retained and filters loaded. Separate explicit-matrix checker passed 236 witnesses/55,696 C checks. These metrics are scoped implementation evidence, not RAM bounds.

**Status:** local-filter completeness and row-independent shortlist are FALSIFIED. Promised-layout compiler, arbitrary critical/high-girth selector, intrinsic hardness and independent peer audit remain OPEN. Free correct choices remove trials but not full witness/refutation construction, original-source verification or universal row coverage.

Artifacts:

- `research/agents/redteam/2026-11-19_STRICT_C_SELECTOR_ADVERSARY4/report.md`
- `experiments/t5/strict_c_selector_adversary4_20261119.py`
- `experiments/t5/audit_strict_c_selector_adversary4_20261119.py`
- `results/raw/t5/strict_c_selector_adversary4_20261119.json`
- `results/raw/t5/strict_c_selector_adversary4_audit_20261119.json`

Next blocker: construct a source-aware selector theorem for arbitrary intrinsic critical/high-girth C families inside the actual row/block exponents, with paid compiler, strategy verification and witness transport. The current easy recursive certificate cannot establish this.

Existing manuscript ownership, titles, schedules and enabled states were not changed. No root manuscript was overwritten.
