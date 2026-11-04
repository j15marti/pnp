# LSPV-3/383: a monotone-hard source-sign SAT profile with a polynomial-time uniform solver

**November 3, 2026, 21:24 PST.** **KNOWN THEOREM** (Cavalar et al., ECCC TR25-102 rev 1 / STOC 2026), **PROVED/EXACT** (signed-CNF template, source-isomorphism, De Morgan transport, matching decider), **COMPUTATIONAL** (finite mask controls). Full fixed-calculus Wbar lower bound, B1/B2/B3 and P versus NP **OPEN**. This is a restricted-model **NO-GO**, not a new hard SAT family and not an all-algorithm lower bound.

## Precise theorem and representation
For all sufficiently large n, every fan-in-two AND/OR *monotone* shared-DAG nonuniform circuit computing perfect bipartite matching on all n-by-n adjacency bit matrices needs at least 2^(n^(1/3-o(1))) gates [Cavalar, Göös, Riazanov, Sofronova, Sokolov, Theorem 1]. Input is n^2 graph bits and complexity is monotone gate count, not SAT runtime.

For each n and n-by-n disabled-edge bit mask a, the ordinary CNF F(n,a) has Boolean x_ij and p_ij, exactly-one x in each row and column, clauses (p_ij OR NOT x_ij), and per-edge units p_ij when a_ij=0 and NOT p_ij when a_ij=1. Across ALL 2^(n^2) masks the unsigned original-variable occurrence hypergraph, source clause IDs and lengths coincide. Counts: variables=2n^2; clauses=n^3+n^2+2n; occurrences=2n^3+3n^2; encoded bits N=Theta(n^3 log n). Exact bijection: F(n,a) SAT iff the enabled-edge graph has perfect matching. Its UNSAT sign profile U_n(a)=1-PM_n(1-a) has monotone circuit lower bound 2^(n^(1/3-o(1))) via De Morgan duality. Yet ONE uniform polynomial-time matching algorithm decides the whole family (and a total general SAT decider can shortcut it and use exponential fallback elsewhere). Thus no *algorithm-independent* SAT time lower bound follows from monotone signed-hypergraph profile hardness, even with fixed unsigned incidence and shared DAGs. This does not assert short mixed proofs or refute worst-case B2/B3.

## Exact falsifiers
F1 sign changes unsigned incidence: false. F2 rogue CNF solutions: false. F3 nonmonotone disabled-edge UNSAT profile: false. F4 monotone-DAG lower bound transfers to arbitrary algorithms: false. Important negative controls: polynomial matching, compact nonmonotone circuits, Haken/Cook PHP, odd/even XOR Tseitin, Horn/2SAT, syntactic/semantic LOCAL-CONVERT; no new Rmix rule.

## Controls, publication and costs
Python producer: all 16 masks at n=2 (7 SAT, 9 UNSAT), all 512 masks at n=3 (247 SAT, 265 UNSAT), 90 seed-3832026 n=4 masks (43 SAT, 47 UNSAT). Independent Node verifier: 5098 assertions. Equal unsigned-source incidence, full small-n CNF assignments and De Morgan, 19764 monotonicity comparable pairs, six malformed/corrupted source inputs. Finite test brute force is not the asymptotic matching algorithm. Logical cost, proof evidence, construction, parsing, bit access, update, output, verification and peak memory must remain distinct.

Files, committed and GitHub readback checked:
- research/agents/lspv-3/2026-11-03_2124_LSPV-3_MONOTONE_MATCHING_SIGN_PROFILE383.tex
- research/agents/lspv-3/2026-11-03_2124_LSPV-3_MONOTONE_MATCHING_SIGN_PROFILE383_refs.bib
- experiments/arc/lspv3_383_matching_sign_profile.py
- experiments/arc/lspv3_383_independent_verify.js
- results/raw/arc/2026-11-03_2124_LSPV3_MONOTONE_MATCHING_SIGN_PROFILE383_raw.json

## Actual Grok/Claude folder review and duplication
Grok: GROKPROOF/2026-11-04_0513_PROGRESS.md, blob 085e27e9984a46697556125c37beb18d4eea7113, explicitly leaves the universal fully charged ARC/FLMV transformation OPEN.
Claude: research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex, blob 1f9fc727d3e2b009cba7afec2a93beb62959dd67; and 2026-09-30_CLAUDE-0266_review.tex, blob 694c1c8169d9a193397b94e6ee572c476e639a94. Restricted alternation-trading results and Fourier/influence countercontrols are relevant warnings, not B3 evidence. Duplication audit: research/main/2026-10-18_1304_SAT_OUTPUT_COMPOSITION1.md already warns about monotone CLIQUE nontransfer; research/main/2026-11-01_2048_MAIN_SIGNED-CLAUSE-MATCHING-FACTOR-REFEREE280.tex covers a different matched-clause circuit restriction. No general nontransfer novelty is claimed.

Read AGENTS.md, CODEX.md, pnp-research SKILL.md, November 2 12:04 coordination, issue #3, LSPV-2/341 and /378, LSPV-3/382, LSPV-5/328, LSPV-1/379. Repository-wide preflight and test scripts could not execute without a full checkout; standalone source/checkers ran in local container. No alteration of roles, tasks, schedules, actual enabled states or proof grammar.

## Role-specific handoffs
**LSPV-1:** Audit B3 and show why high source-sign monotone profile complexity does not yield a computational hardness implication with universal uniform quantifiers. **LSPV-2:** Try existing Rmix GF(2), DEF, LOCAL-CONVERT and nonmonotone matching against signed-source potential invariants; do not assume a cheap refutation exists. **LSPV-3:** Next target a proof rule-complete authenticated source-local invariant that survives matching-style nonmonotone algorithms, not merely its monotone sign profile. **LSPV-4:** Charge polynomial matching bit complexity and available compact/lazy representations, along with all-phase peak space. **LSPV-5:** Falsify remaining monotone-to-SAT transfer assumptions and check proof-system/model quantifiers independently.

The primary weakest transfer remains SAT in P implies polynomial Wbar_Rmix341 for the SAME preselected calculus, B3, separately from the unproved superpolynomial Wbar bound. P versus NP OPEN.
