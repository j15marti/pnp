# CROSS-TRACK T5-RESRETRACT50 | 2026-11-17 18:34 PST

**STATUS:** PROVED/EXACT scoped T5 one-hot Resolution transport and boundary count identity, finite computational audit. Independent mathematical review OPEN. **P versus NP OPEN.**

## Four pre-search integration ideas
1. Resource Contraction + Proof Transport: Repair BOUNDARY-PROMISE49 with an actual, byte-accounted two-way Resolution proof transformation.
2. Nonrelativizing Simulation: Delayed terminal colors versus genuinely status-changing edits; four-edge support saturation is a falsifier of endpoint-color necessity.
3. Same-input UWI: Test identical final satisfiable graph and common clock against source-aware witness lift/projection rather than swapping program/input quantifiers.
4. Counting vs rank: Does the full-rank 25-entry endpoint counting tensor have any information beyond the original whole-graph count?

## Targeted source review
Read GitHub TMR-2/072 connected mixed YES/NO gauge ring (17:18 PST), TMR-4/074 feedback-edge original-source OBDD/count compiler (open PR #237), LSPV-5 COREPEEL1 source-authenticated low-degree elimination (17:36 PST), SIGMA3 RESIDUAL59 (18:01 PST), Clock Gate CLOCKASYMTRANSFER24 (conditional MCSP transfer, no quotient), older TRACEAUDIT23 and DIAGONALLIST34, the PC22-ORCLOSURE38 proof-system-specific transport, and BOUNDARY-PROMISE49 predecessor. Consulted project chat summaries, Library, Google Drive continuity and KRYLOVGUARD41; newest suitable Drive files are older than current GitHub. Primary literature: Bang-Jensen/Hell/MacGillivray 1988, Cook/Reckhow 1979, Atserias/Mueller 2019/2020, Kozik bounded-width CSP. General Resolution projection and Frege substitution are established techniques; no novelty claimed for them.

## Theorem: exact SAT support, counting profile, and Resolution proof neutrality

Let R(c,d)=1 iff (d-c) mod5 lies in {1,3}. Given any nonempty T5 input G with root r, add **two disjoint all-forward private paths of length four**, a->a1->a2->a3->r and b->b1->b2->b3->r, retaining G verbatim. Call the result H_r(G). It has n+8 vertices and m+8 arcs and is connected whenever G is connected. Since A^4 has strictly positive entries, the two-terminal SAT-support table S_H is J5 if G SAT and 0 if G UNSAT. The previous BOUNDARY-PROMISE49 connected NP-completeness reduction applies to this all-or-none promise.

Use the **direct one-hot exactly-one CNF** F_X with five atoms X_(v,c) per T5 vertex; at-least-one, at-most-one, and every forbidden-pair arc clause. Define sigma(X_(v,c))=X_(v,c) on G; on each private path define offsets delta=(0,3,1,4) for its terminal and three internal vertices, and sigma(X_(t,c))=X_(r,c-delta_t mod5). Differences of successive offsets are 3,3,3,1, all legal. Every private-vertex one-hot axiom maps to the corresponding root axiom; every private arc forbidden-pair clause maps to a root at-most-one clause for **different** colors; every G axiom maps to itself. Therefore **sigma(F_H) subseteq F_G**.

Given any standard DAG Resolution refutation of F_H, literal-substitute all clauses. At a resolution step retain a subclause of each premise image; resolve if both mapped pivot polarities remain, otherwise reuse the premise that already loses its pivot. The result subsumes the image of the source resolvent. Initial images are actual F_G axioms, and the final empty clause stays empty. This produces an F_G refutation with at most the same number of derived steps and no greater width. Conversely F_G is a literal axiom subset of F_H, so every G refutation replays in H. Thus **minimum Resolution refutation inference count and width are EXACTLY EQUAL** for F_H and F_G, under this fixed encoding and standard resolution/subsumption normalization. The translator is uniformly polynomial in fully materialized source+proof bit length; a conservative O((L+|pi|+1)^4) time and O((L+|pi|+1)^3) space ledger charges parsing, source authentication, proof checking, clause copying, substitution and output. This is not a translation from arbitrary SAT deciders.

Let W=A^4, row0 W=(4,4,1,6,1), B=WW^T, row0 B=(70,36,57,57,36), det B=256, each B row sums to 256. T5 global color translation acts freely on G's satisfying assignments, so each root color occurs Z(G)/5 times, for n>=1. The **exact** fixed-terminal count matrix is C_H=(Z(G)/5) B. Consequently **Z(H)=256 Z(G)**. If G SAT, C_H is positive and full rational rank, but all its graph-dependent information is the scalar Z(G). With external terminal constraints, the entrywise weights matter. No easy general counting or SAT algorithm follows.

## Hostile audit
Executed standalone CPython stdlib verifier on **294 G sources** (136 SAT, 158 UNSAT), n<=4. **163,622 assertions, ZERO failures**, including 61,152 extended-source axiom mappings, 57,710 original-source assignments checked for every private-path gauge assignment, 1,745 random Resolution inference projections, 5,500 independently enumerated exact terminal counts, 7,350 count-template checks, two complete opposite-arc 30-step Resolution refutations (one including unused private-path inference detour), false-offset and short-path controls. The symbolic theorem is separate from finite evidence. No large graph, complete physical TM microtrace or independent referee review claimed.

Local complete report: 2026-11-17_1834_T5_RESRETRACT50_REPORT.md; complete Python audit SHA256 ad60ffe90ec8f846577fd2826e365530c449b45f7c2dbb241134f3e75bf183c1; raw result SHA256 9f5b431f8542ed275434cfa71134c3fc81e9d2a5e72f5e690ef63a565168b076. The local files are conversation artifacts, **not** claimed accessible to other agents through the repository.

## Proof DAG
- ESTABLISHED: T5 semicomplete-target CSP NP-complete (Bang-Jensen et al.).
- PROVED restricted: four-edge full support; H_r(G) all-or-none support; sigma(F_H) subseteq F_G; exact two-way Resolution size/width retraction; C_H=(Z(G)/5)B; Z(H)=256 Z(G).
- FALSIFIED as universal inference: full-rank boundary / tiny output / restricted proof complexity forces expensive unrestricted SAT decisions.
- OPEN: arbitrary-input affordable resource contraction with acquisition, generation, recursion, workspace and validation fully charged; SAT-correctness-forced nonrelativizing WRAPPER hinge; same-final-input common-clock UWI; arbitrary SAT decider to proof system transport; P != NP.

## Next four specialists
- **Resource Contraction:** reconcile sigma retraction with TMR-4/074 and COREPEEL1; seek a nontrivial, fully charged hereditary contraction beyond single-root private paths.
- **Nonrelativizing Simulation:** separate delayed terminal colors (no SAT change) from delayed source edits (often cheap direct contradiction); demand oracle and precomputation controls.
- **Universal Obstruction:** same final satisfiable H_r(G), same clock, all eligible programs, explicitly including core witness projection/lifting via sigma.
- **Proof Transport:** independent proof of subclause-normalized Resolution translator including loops and proof conventions; investigate PC/PCR only with field, width, degree and encoding explicit.

**Single next implication:** establish a genuinely global source-grounded necessary-work statement that survives these exact proof-neutral, representation-rich but semantically easy attachments. All agents keep P versus NP OPEN. No schedules, titles, roles or other agent files changed.

## Sources
- https://doi.org/10.1137/0401029
- https://doi.org/10.2307/2273702
- https://arxiv.org/abs/1904.02991
- https://doi.org/10.1137/18M117577X
- https://github.com/j15marti/pnp/blob/main/research/agents/cross-track/2026-11-17_1725_T5_BOUNDARY_PROMISE49_STATUS.md
- https://github.com/j15marti/pnp/blob/main/research/agents/tmr-2/2026-11-17_1718_TMR2_T5_CONNECTED_GAUGE_MIXED072.md
- https://github.com/j15marti/pnp/pull/237
- https://github.com/j15marti/pnp/blob/main/research/main/2026-11-17_1736_MAIN_LSPV5_COREPEEL1_CONDENSED.tex
- https://github.com/j15marti/pnp/blob/main/research/agents/clock-gate/2026-11-17_CLOCKASYMTRANSFER24.md
- https://github.com/j15marti/pnp/blob/main/research/agents/cross-track/2026-10-17_0900_CROSS-TRACK_PC22_ORCLOSURE38_SHORT.md

END T5_RESRETRACT50, P_VERSUS_NP_OPEN
