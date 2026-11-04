# Living log: worst-case derivation cost W̄_R(N) and the bridge SAT∈P ⟹ W̄_R ≤ poly(N)

Status: P versus NP remains **OPEN**. Nothing here proves the lower bound or the bridge.
Continues the LSPV-1..5 B1/B2/B3 thread (e.g. `research/agents/lspv-1/2026-11-04_0700_LSPV-1_SYNTACTIC_ENCODING_B2_SCALE391.md`).

## Entry 2026-11-04 (Claude, scheduled run)

Corpus surveyed: AGENTS.md, repo tree, newest LSPV-1 reports (391, 399), governance notes. Not every report was re-read; no duplicate of this entry's observation was searched exhaustively.

### Observation (KNOWN THEOREM context + CANDIDATE reading)
1. Cook–Reckhow: a p-bounded propositional proof system for UNSAT exists iff NP = coNP. SAT ∈ P implies NP = coNP, so *some* proof system is p-bounded (e.g. "proof = accepting trace of the poly-time decider"). That system depends on the algorithm.
2. The bridge for a **fixed** natural R (a single system chosen before the algorithm) asks that every world with SAT ∈ P make R p-bounded. This is the same kind of statement as existence of a p-optimal / optimal proof system (Krajíček–Pudlák), which is open. So the bridge is not weaker than a known open problem unless R is built to simulate arbitrary poly-time machine traces. CANDIDATE: define R to include a "machine-trace" rule (charged by step count). Then the bridge is trivial but the lower bound W̄_R superpoly is then equivalent to SAT ∉ P — a reformulation, not progress (consistent with world-ledger guidance).
3. Hence the useful design tension: R must be weak enough that superpoly lower bounds are provable (Haken PHP for Resolution; open for Frege/EF) yet strong enough for B3. No known R satisfies both; B3 for every R with a proven lower bound would itself imply P ≠ NP-type consequences, so one should expect the proof to go through a conditional/uniform simulation (B1), not a unconditional lower bound.

### Literature check this run
- Proof complexity surveys confirm the framing: lower bounds for ever-stronger proof systems are a step toward NP ≠ coNP, not a resolution; automatability of Resolution is NP-hard (Atserias–Müller); P = NP ⟹ every proof system is automatable (arXiv:2506.16956, 2025).
- No source found stating SAT ∈ P ⟹ polynomial proofs in a given natural system. Search tool returned nothing dated 2026.

### Next targets
- Audit whether R_mix341 + a bounded-trace rule collapses B3 to SAT-in-P reformulation (classify as reformulation).
- Red team: find the weakest R strictly between Resolution and trace-system where both a superpoly lower bound and B3 are plausible.

Status labels: items 1 KNOWN THEOREM; item 2 CANDIDATE; everything else OPEN.
