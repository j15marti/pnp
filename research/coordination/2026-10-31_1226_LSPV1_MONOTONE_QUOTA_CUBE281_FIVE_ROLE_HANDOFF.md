# LSPV-1 MONOTONE-QUOTA-CUBE281: five-role ARC/FLMV handoff

**October 31, 2026, 12:26 PDT. P versus NP OPEN.** The target remains all valid instances of D\"ocker's NP-complete proper duplicate-free monotone 3-SAT-(2,2); malformed inputs rejected. No task identities, schedules, status or ownership changed.

## Restricted exact theorem and falsifiers

For any coherent partial assignment with t fixed TRUE and f fixed FALSE original variables, let q_{r,-} and q_{r,+} count original negative and positive clauses with exactly r literals not fixed false. Each sign has 2n/3 original clauses and every source variable exactly two occurrences of each sign. Consequently,

q_{0,-} = 2(t-2n/3) + q_{2,-} + 2q_{3,-},
q_{0,+} = 2(f-2n/3) + q_{2,+} + 2q_{3,+}.

Both q_0 counts are **actual falsified original-clause indices**. Quota checks t>2n/3 or f>2n/3 reject no coherent partial cube beyond an already full original-clause-checking UP/DPLL policy. Conversely, falsifying one original negative clause by setting its three variables TRUE need not cross the weight quota when n>=6 (analogously for positive clauses). Neither observation proves a complexity lower bound.

Every valid F has original four-bucket histogram (2n/3,0,0,2n/3) at both coherent endpoints 0^n and 1^n, and (2n/3-2,2,2,2n/3-2) after every singleton flip from either endpoint. Hence any endpoint/one-flip *aggregate-histogram-only* classifier is uninformative across valid same-size SAT/UNSAT instances; this is not a statement about source-aware deductions.

## Matched SAT/UNSAT evidence

Actual U198 (D\"ocker Appendix C, n=198,m=264) is UNSAT by the **prior independently replayed six-module 64-row source refutation**. V198 swaps positive occurrences in original clauses 2 and 44 and is SAT by a newly replayed 198-bit witness whose full-source histogram is (0,158,80,26). All endpoints and 396 singleton flips match exactly despite different labels. Each has 34,716 original indexed clause pairs and 780 non-tautological source-parent resolvents. Y6 and Z9 were exhaustively checked on all 3^6=729 and 3^9=19,683 coherent partial cubes, respectively. Direct DPLL on the two large sources reached a 1,000-node cap and returned UNRESOLVED, not a false UNSAT verdict.

An independent no-import verifier checked 278,104 clause-pair S/U modes, every stored signed-occurrence target and inversion, all sampled impossible partial cubes, source-parent resolvents, and verified full SAT witnesses. Four deliberate corruptions were rejected. The report includes source scanning, failed strategies, literal probes, and printed/retained output counts as host-language proxies, not native FLMV machine exponents.

## Published artifacts, all exact readback verified except oversized aggregate

- Formal theorem: https://github.com/j15marti/pnp/blob/main/research/agents/lspv-1/2026-10-31_1226_LSPV-1_MONOTONE_QUOTA_CUBE281.tex
- Executable producer: https://github.com/j15marti/pnp/blob/main/experiments/arc/2026-10-31_1226_LSPV1_MONOTONE_QUOTA_CUBE281_repro.js
- Independent verifier: https://github.com/j15marti/pnp/blob/main/experiments/arc/2026-10-31_1226_LSPV1_MONOTONE_QUOTA_CUBE281_independent_verify.js
- Four separately readback-verified raw JSON files and source blob provenance: https://github.com/j15marti/pnp/blob/main/results/summaries/arc/2026-10-31_1226_LSPV1_MONOTONE_QUOTA_CUBE281_manifest.json

The aggregate ~1.36MB raw file exceeds GitHub's normal contents-API readback threshold; the four smaller case JSONs have exact readback. Container-to-Library upload was attempted but failed with an unshared session.

## Corpus and role-specific next steps

Reviewed root main, issue #3, AGENTS/CODEX/pnp-research skill, REDIRECT1, CONTRACT1, AFFINE-SMALLBIAS-DESCENT-GATE2 (restricted MCSP only), CONSTRUCTION-STRENGTHEN17, ARC-LINEAR22-SATURATION1, current LSPV1 PORT_CUT280, LSPV2 COMPONENT_CLOSURE279/TARGET_SCOPE278, LSPV3 GATE280, LSPV4 NEAR_FULL_TRUE249, and LSPV2 SECOND_ORDER_FLIP243. Existing endpoint weight bounds, clause-extreme compatibility and two-flip vector work are explicitly credited. Google/web primary searches: Doecker arXiv:1912.08032, Darmann-Doecker DOI 10.1016/j.dam.2020.12.010, FLMV 2005 original PDF, conflict-graph and local SAT research. GitHub searches covered j15marti/pnp and OpenAI; the latter returned no relevant SAT implementation. No novelty inferred from this absence.

LSPV-1: attempt authenticated genuinely new-clause/auxiliary-variable target-preserving hereditary successor. LSPV-2: audit exact cofactor rebalancing and indexed child access. LSPV-3: falsify cheap policy selection on connected valid target sources. LSPV-4: certify actual same-machine SAT-to-M22 local transfer and all simultaneous costs. LSPV-5: independently challenge quota identities, SAT/UNSAT controls and source/space assumptions.

**Load-bearing OPEN:** a fully charged all-valid-target uniform arbitrary-A hereditary contraction with power-short target children or sound terminal rules, AND a quantitative same-machine FLMV SAT-to-target bridge (or direct target forbidden-region bound). P versus NP remains OPEN.
