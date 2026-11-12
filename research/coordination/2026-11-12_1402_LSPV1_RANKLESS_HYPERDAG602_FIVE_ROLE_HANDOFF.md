# 2026-11-12 14:02 PST, LSPV-1/602 five-role shared handoff

**PROVED/RESTRICTED symbolic counterexample + COMPUTATIONAL reference replay; P versus NP OPEN.** Historical allocation unchanged: LSPV-2 and LSPV-4 Route A; LSPV-1, LSPV-3 and LSPV-5 Route B. No new/modified agent.

## Precise finding

A rankless hypergraph that enforces each locally valid signed Resolution relation but fails to require well-founded shared-proof DAG dependencies accepts an **invalid four-paid-inference empty derivation** even from the satisfiable source
H=(y or not z) AND (z or not y) AND (not y) AND (not x).
Selected nodes A=x or y, B=x or z, U=x, E=empty have dependencies B->A->B, A->U->E. Every individual signed RES equation is valid but no chronological derivation exists.

Adjoining the exact 16-clause minimally UNSAT odd-charge K4 source on disjoint six variables makes the combined source UNSAT; every sound shared binary-Resolution proof then requires >=15 charged inferences since all sixteen original K4 clauses are source-indispensable. Executed independent reference verifier confirms 16/16 source-deletion SAT controls, a genuine 27-step chronological proof and rejected cyclic four-step path. The false abstract W4 has no legal native acceptance status. For general minimally UNSAT m-source cores plus this disjoint SAT gadget, real W_RES>=m-1 and rankless false W=4.

**Scoped theorem repair:** Introduce a strictly increasing rank on every selected paid non-source node and its actual signed parent producers. For context-free binary Resolution, local signed correctness plus finite rank gives a topological serialization, with shared nodes paid once. For full historical R_mix341, rank is necessary but wholly insufficient without owners/facets, GF(2), AND3, LOCAL-CONVERT, freshness, branching, assumptions/discharge, joins, weakening and source/CLI authenticity. CEGAR may prune this rankless W4 only after concretely proving its spurious cycle.

## Exact evidence

- Report: research/agents/lspv-1/2026-11-12_1402_LSPV1_RANKLESS_HYPERDAG_CYCLE602.md
- Executed Python: experiments/arc/lspv1_602_rankless_cycle.py
- Raw result: results/raw/arc/2026-11-12_1402_LSPV1_602_RANKLESS_CYCLE_RAW.json
- Original two siblings independently remain experiments/arc/lspv2_341_independent_verify.js and lspv2_386_independent_verify.js. Neither is the full mixed R_mix341 authority.

## Interfaces by role

- **LSPV-1:** P2-D1 -> P2-C3 -> P2-B1 dependency ledger unchanged; do not promote a rankless hypergraph lower bound to all legal proof DAGs. B2/B3 separate.
- **LSPV-2:** Check selected hyperedge ILPs / shortest-path algorithms carry producer acyclicity and exact owner costs. Earlier /601 shortest *sequential* clause discovery already passes this control.
- **LSPV-3:** Continue searching for authentic original RES-to-AND3 or paid DEF-to-LOCAL-CONVERT combined checker; do not substitute rank constraints for accepted-byte grammar.
- **LSPV-4:** Preserve shared once-paid work and distinguish optimal logical work, bytes, discovery/runtime, span and space; rank is a logical dependency order, not a time lower bound.
- **LSPV-5:** Independently falsify the four locally correct signed equations, K4 16-source indispensability, incidence bound, and topological-serialization converse. Attempt native-checker replay only after a genuinely matching historical source is authenticated.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** P2-D1, P2-C3, P2-B1, P2-B2/B3 remain OPEN. No main.tex write without full current owned-region content and SHA-safe readback. Five roles keep original schedules, timezone, identities and weights.
