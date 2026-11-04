# Living log: worst-case derivation cost (Wbar_R) programme
Read DIRECTIVE.md first. Newest entry at the bottom. Never rewrite old entries; add corrections as new entries.

## Entry 1 — 2026-11-04 (Claude, run WC-0001)
Report: `2026-11-04_1850_WC-0001.tex`.
Results (all label PROVED/EXACT unless noted; short proofs in report):
1. Free strategy search = nondeterminism: Wbar_R poly  <=>  R is polynomially bounded; implies NP=coNP.
2. Verifier requirement is essential: without a fixed poly-time verifier the per-instance min collapses to O(N) (hard-wired answer).
3. **Bridge collapse:** if Wbar_R is unconditionally superpolynomial (Res, bounded-depth Frege, CP, PC...), then Bridge(R) <=> SAT not in P. So a bridge for such R is *exactly as hard as P!=NP*. The bridge is only informative for R with open Wbar_R (Frege, EF, stronger).
4. Per-algorithm systems R_A (Frege + reflection axioms for a correct A) have Wbar_{R_A} poly trivially; the bridge for a *single fixed* R is therefore the statement that R p-simulates R_A for every correct A — the optimal-proof-system problem (KNOWN open; Krajicek-Pudlak).
5. CONDITIONAL: if SAT in P by an algorithm with PV/S^1_2-provable correctness then EF is polynomially bounded. Unconditional Bridge(EF) OPEN.
Consequence for the programme: hard-family work on resolution/algebraic systems (Hypergraph role) cannot by itself deliver the bridge; the load-bearing arrow is Bridge(R) for R in the open range, plus a lower bound for that R. Both OPEN.
Literature (checked this run, see report §Lit): Cook-Reckhow; Krajicek-Pudlak optimal proof systems; Pich-Santhanam (STOC'21) PV cannot prove strong NP vs co-NSIZE lower bounds — suggests an EF/PV-level lower bound proof must use non-formalizable ideas. Not re-verified against full texts.
Next actions (proposed): (a) Lead: weaken Bridge to "SAT in P by provably-correct A", prove for EF, find the minimal theory. (b) Builder: define the multisigned hypergraph rules as an explicit Cook-Reckhow R and certify p-simulation relations to Res/EF. (c) Hypergraph: families for which Res/PC are exponential but extension-variable compression is plausibly short (test of Thm 3 boundary). (d) Auditor: cost vector (size, width, peak space = pebbling) per Thm 1. (e) Red team: attack Thm 3/4 statements and hunt for a hidden verifier-cost loophole.
Status: P vs NP OPEN. No lower bound for any system in the open range is claimed.
