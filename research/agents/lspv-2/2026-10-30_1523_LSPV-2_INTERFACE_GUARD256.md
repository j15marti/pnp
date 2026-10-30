# LSPV-2 INTERFACE-GUARD256: Certified conditional component profiles
October 30, 2026, 3:23 p.m. PDT. Single integrated universal adaptive residual-SAT / ARC-to-FLMV spine. Both P=NP and P!=NP OPEN.

**Status:** PROVED/EXACT for a supplied and correctly verified separator with independent mathematical review pending. Known theorem transfer from junction-tree/project-join DP, not a new general algorithm. COMPUTATIONAL finite controls. All-input ARC contraction OPEN.

## Corpus reviewed and duplication audit
Read research/governance/2026-10-30_0948_UNIVERSAL_PARAMETERIZED_FLMV_REDIRECT1.md; research/review/spines/2026-10-30_UNIVERSAL_PARAMETERIZED_FLMV_CONTRACT1.md; AFFINE-SMALLBIAS-DESCENT-GATE2 (restricted only); CONSTRUCTION-STRENGTHEN17; ARC-LINEAR22-SATURATION1; AGENTS.md; CODEX.md; .codex/skills/pnp-research/SKILL.md; root main.tex; active issue #3; LSPV-2 VIRTUAL-STRICT22-COMPOSE255 and POLICY-ENTRY-GATE253; LSPV-5 HITTING-TREE-COMPOSITION-REFEREE222; LSPV-3 MONOTONE-PROBE-RESUME254 and SAT-ONLY-SELECTOR-FIREWALL256. Current project root already recognizes full-interface DP; no novelty in component projection is claimed. Primary sources: Fortnow et al. JACM 2005, Dreier et al. JCSS 2024, Samer/Szeider J. Discrete Algorithms 2010.

## Three falsifiers
F1: All components separately SAT imply globally SAT. FALSIFIED by source modules (x) and (not x), because their shared interface projections are disjoint.
F2: Every private-variable pin update forces global profile recomputation. FALSIFIED under fixed source, verified separator and cached profiles: only the owner component profile changes.
F3: Exact source-indexed projected profiles already constitute physical N^(1/2) ordinary SAT children for an arbitrary decider. FALSIFIED as an architectural inference: profile/proof storage can be exponential, no shorter ordinary child is produced, no guest workspace is reduced.

## Exact restricted update theorem
Take any signed source CNF F with original clause numbers and a declared variable separator B of size b. Delete B from the primal graph and compute private connected components V_i. Each original clause is assigned exactly once to its unique private component (or a B-only module). All modules share only B. Let tau_i be any coherent private partial assignment. For each beta in {0,1}^B let h_i(beta,tau_i)=1 exactly when module i has a private satisfying extension. Define d(beta)=sum_i(1-h_i(beta,tau_i)).

Then F restricted by all tau_i is SAT iff some beta has d(beta)=0. After changing only tau_h to tau_h', the exact charged logical update is

    d'(beta)=d(beta)+h_h(beta,tau_h)-h_h(beta,tau_h').

All other component profiles remain valid. A proof-carrying UNSAT result consists, for each beta, of an owner module with a source-clause-authenticated exhaustive local DPLL refutation under beta and its private pins. A SAT witness joins one verified extension from every component under the same beta. A refutation under private pins does not certify the unpinned parent.

**Proof:** Every total extension fixes exactly one beta, and all original clauses are owned by one module with no cross-module private variables. Thus extensions exist iff all owner modules have compatible extensions. The delta identity is subtraction of failure indicators. Each local DPLL refutation has only source-clause unit reasons or source-clause conflicts and covers both children at each true split. An induction on each proof and a complete enumeration of beta yield an exact UNSAT certificate. For SAT, combine disjoint private witnesses and check every original clause.

With L literal occurrences, verified separator discovery scans O(L alpha(n)) indexed words using union-find and unique clause ownership. The initial charged cost is O(L alpha(n)+q 2^b)+sum_(i,beta) W_(i,beta), where W includes actual terminal policy, failed branches, witness/proof creation and checking. A private update costs O(2^b)+sum_beta W_(h,beta). Peak storage includes q 2^b Boolean cells plus all retained source, source indices, witnesses, local proofs, cache and search state. Candidate-B discovery and policy switching are not free; when b grows, neither time nor space is polynomially bounded by this theorem.

## Computational outcomes
Full local package: Python producer interface_guard256.py, fully independent checker independent_guard256.py, hostile_guards256.py, benchmark_guard256.py, raw JSON and SHA-256 manifest. The compact independent executable published next to this report checks the exact delta and both labels on a smaller fixed two-boundary family; it does NOT reproduce all 86 hostile cases. Native repository preflight/CI was unavailable from the container; local script tests passed.

32 private updates after initialization, profiles versus fresh source-UP-DPLL on the SAME source states, counting selected reads, splits, units, final witness scans and certificate replay:

| Private modules | Label | Fresh-DPLL selected events | Guarded-profile selected events | Fresh-DPLL seconds | Guarded-profile seconds |
| ---: | :---: | ---: | ---: | ---: | ---: |
| 18 | SAT | 7309 | 5474 | 0.01290 | 0.01577 |
| 18 | UNSAT | 4000 | 3164 | 0.00533 | 0.01293 |
| 36 | SAT | 13159 | 9218 | 0.01739 | 0.07941 |
| 36 | UNSAT | 6556 | 4640 | 0.01169 | 0.01776 |
| 72 | SAT | 24859 | 16706 | 0.03728 | 0.03601 |
| 72 | UNSAT | 11668 | 7592 | 0.01841 | 0.02866 |

Peak Python allocated memory is higher for guarded profiles in every case (18-module SAT 242228 bytes vs 146403). These are Python timings and selected event counts, NOT FLMV bit-Turing operations or industrial CDCL comparisons. A separate independent oracle replay checked 264 boundary states, 760 original-clause pair S/U compatibility modes, coherent 0^n and 1^n extremes, exact flip trails, and 32768 assignments of W1 strict22 UNSAT. Another hostile run passed 86 SAT/UNSAT cases and 450 private updates including renamed/polarity-switched, Horn, Krom, XOR, wide/easy and random inputs. Same unsigned-support 20-variable matched cases: 2-model SAT versus 0-model UNSAT. Exact source-indexed S and U targets are controls, not independent occurrences.

## ARC resource firewall and change from root
The existing virtual composed compiler T(E(F)) supports arbitrary bit access in a restricted indexed grammar, but expands to N log^O(1) N and does not yield ordinary children of N^lambda. The guarded profile is an exact adaptive policy component, NOT a hereditary arbitrary-A contractor. Its source-memory and proof-cache overhead can violate the proposed same-machine L' <= max(1/2,L/2). The hypothetical K' <= max(11/10,3/5+K/2) has no constructed all-input step. FLMV forbidden region remains an independent published theorem on the matched deterministic model, not a consequence of this experiment.

**What changed relative to root:** code-level charged incremental private-profile transitions, local proof provenance and matched both-label finite controls. **Adopted:** full-interface DP, certified DPLL fallback, previously verified virtual compiler. **Rejected:** scalar component labels, free separator acquisition, guest-space contraction inferred from virtual access, and unpinned UNSAT inferred from a bad pin. **Stale/overstated:** no newly verified contradiction in root's explicit OPEN status. **Next arrow:** certified class-specific 2SAT/Horn/dual-Horn/XOR local policy substitutions with proof traces and search/discovery charges; continue testing physically shorter children under arbitrary-A wrappers. P versus NP OPEN.

References: [1] Fortnow, Lipton, van Melkebeek, Viglas, JACM 52(6), 835-865 (2005), doi:10.1145/1101821.1101822. [2] Dreier, Ordyniak, Szeider, JCSS 142, 103520 (2024), doi:10.1016/j.jcss.2024.103520. [3] Samer, Szeider, J. Discrete Algorithms 8(1), 50-64 (2010).
