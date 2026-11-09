# LSPV-5/463: abstract-satisfaction branch-join polarity and a false-conflict control

**2026-11-09 08:44 PST | Route B independent red team | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

**Exact proof-chain nodes.** This run proposes `[P2-L5-463]`, refining `[P2-C1]` and `[P2-C3]` and supplying a necessary abstraction-side condition for `[P2-D1]`. `[P2-D1]`, `[P2-C3]`, the all-rule mixed lower bound `[P2-B1]`, noncircular same-calculus B3 `[P2-B2]`, and every `proof1.txt` target remain **OPEN**. The result is distinct from `[P2-L2-521]`: /521 exhibits one context-erasure counterexample in a separate branch/Resolution calculus; /463 proves the exact abstraction/concretization polarity and the least sound join in the common-literal domain. No historical `R_mix341` rule or weight is changed.

## IDEA: candidate, assumptions, and falsifiers fixed before search

**Initial hypothesis.** An Abstract-Satisfaction/ACDL analysis is unsound at shared-DAG reconvergence if it erases split assumptions and conjunctively pools branch-local learned facts. Under the concrete powerset semantics of alternative branch models, the correct abstract transformer must cover the **union** of the branch sets. In the common-literal domain, this means intersecting the sets of must-facts, not taking their union.

Falsifiers:

1. the primary Abstract Satisfaction or ACDL framework explicitly validates context-free conjunctive pooling of facts learned under incompatible branch assumptions;
2. the live trackers already contain the exact general polarity theorem and common-literal least-join repair;
3. a native historical `R_mix341` derivation legitimately obtains the pooled conflict on the satisfiable control without an unauthenticated split/discharge rule;
4. exhaustive finite semantics shows that the pooled abstract state covers every model in every tested pair of alternative branches.

F1 was rejected by the primary papers: their collecting semantics uses intersection for conjunction and union for disjunction, and sound abstract transformers must overapproximate the collecting transformer. F2 was rejected after reading both live trackers; `[P2-L2-521]` is related but does not state this lattice theorem. F3 was not established because no historical native split/discharge grammar was authenticated. F4 was falsified: conjunctive pooling is unsound in 168 of 225 ordered pairs of nonempty subsets of the two-variable valuation universe.

## SEARCH: continuity and exact sources

### Governing project state

Read both complete live trackers before research: `proof1.txt` blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b` (18,553 characters) and `proof2.txt` blob `89afcf53891435d92b8a093cec3b5ac28c6964b2` (766,431 characters). The latter contained current nodes `[P2-L5-462]`, `[P2-L1-537]`, `[P2-L2-521]`, and `[P2-L3-536]`. Read current issue #3 through the LSPV-3/536 publication; the November 9 abstract-interpretation five-role handoff; the mandatory knot/link handoff; AGENTS.md, CODEX.md, `.codex/skills/pnp-research/SKILL.md`, its red-team mode, and the historical November 2 refocus at commit `4e29ed7646f484707767acb6e63ec5f38afd98a8`.

Peer continuity was from the actual current files: LSPV-1/537 (blob `4535ff...`), LSPV-2/521 (blob `9b222d...`), LSPV-3/536 (blob `c2026f...`), LSPV-4/522 (blob `bfc4a48f25be4961f5ec9b423f27430c971e4b00`), and the LSPV-4 cost-partition simulation (blob `73131062bf74e65c39897594ef7341254210e78b`). Also read `GROKPROOF/2026-11-09_1230_PROGRESS.md` (blob `0ee19c...`) and the actual Claude world-ledger README plus `2026-10-28_1452_CLAUDE_TPORT-0002.tex` (blobs `de75a...`, `1f9fc...`). Ellipses identify prefixes recorded by the connector rather than fabricated full SHAs.

### Primary abstract-interpretation literature

- P. Cousot and R. Cousot, “Abstract Interpretation: A Unified Lattice Model for Static Analysis of Programs by Construction or Approximation of Fixpoints,” POPL 1977, author page: <https://www.di.ens.fr/~cousot/COUSOTpapers/POPL77.shtml>. The paper supplies the complete-semilattice/fixpoint sound-approximation framework; it does not supply an `R_mix341` complexity lower bound.
- V. D'Silva, L. Haller, and D. Kroening, “Abstract Conflict Driven Learning,” POPL 2013: <https://www.kroening.com/publications/view-publications-dhk2013-popl.html>. Its lattice operations preserve their ordinary semantic polarity: meet models conjunction, while join overapproximates disjunction. Its correctness hypotheses are on the declared abstract domain/transformers, not on the historical mixed calculus.
- V. D'Silva, L. Haller, and D. Kroening, “Abstract Satisfaction,” POPL 2014: <https://www.kroening.com/publications/view-publications-dhk2014-popl.html>. The collecting semantics of formula conjunction is intersection and disjunction is union; a sound overapproximating transformer satisfies `F(gamma(a)) subseteq gamma(aF(a))`. A domain is disjunctive only when concretization of abstract join equals union; otherwise join may be a strict overapproximation. Failure to reach bottom is therefore not SAT and not a proof-size lower bound.

### Required repositories and rotating corpus

- `konard/p-vs-np` remained pinned at head `ecedd2b45f1c524d85c00b2da27a9c140025550c`; README blob `0e0ec77f...` and `scripts/proof_status.json` blob `93b77ed3...` explicitly limit the proved direction to the repository's finite-machine model and leave the converse unresolved.
- `blkph0x/p-vs-np-proof-research` remained pinned at `7dedc73f...`; README `f397a774...`, `METHOD_INDEX.md` `18d693ea...`, and `PUBLIC_METHOD_REVIEW.md` `ed76bec...` catalogue bounded/conditional methods and warn that assumption-dependent claims require discharge.
- `meelgroup/frat-xor` README blob `38a137...` describes FRAT-XOR/XLRUP conversion and a CakeML-backed checker. This is a different proof grammar, not authority for historical `R_mix341`.
- `peitl/short-proof` README blob `93d2090...` optimizes shortest Resolution proofs only.
- `MassimoLauria/cnfgen` Tseitin generator source blob `4bb5fd19...` was used as an encoding control, not as a mixed-calculus lower bound.
- `openai/math` README blob `cc5b0a03...` warns that its research data have heterogeneous verification status. `anthropics/formal-math` was change-aware checked at pinned head `16a5ce...` and supplied no transfer theorem.

General web research was available. A separately authenticated Google-branded search endpoint was not available. Repository titles, CI, and checker acceptance were not treated as proofs of P versus NP.

## ITERATE: exact domains, polarity theorem, and adversarial control

Let `U` be the Boolean valuations over a fixed finite variable set. The concrete domain is

$$
C=(\mathcal P(U),\subseteq),
$$

where a branch state denotes the set of models still possible under its source and assumption context. Alternative exhaustive branches reconverge by concrete union; simultaneous formula obligations combine by intersection.

Define the common-literal abstract domain

$$
A=(\mathcal P(\mathrm{Lit}),\preceq), \qquad
K_0\preceq K_1 \iff \gamma(K_0)\subseteq\gamma(K_1),
$$

with

$$
\alpha(S)=\{\ell:\forall v\in S,\ v\models\ell\},
\qquad
\gamma(K)=\{v\in U:\forall\ell\in K,\ v\models\ell\}.
$$

Thus abstract elements are conjunctive sets of **must-literals**. More literals mean fewer represented models. The abstraction is an analysis layer only; it does not add a case split, discharge, weakening, definition, GF(2), or nonlinear rule to `R_mix341`.

### Theorem 463.1 — least common-literal join for alternative branches

For all concrete branch sets `S0,S1 subseteq U`,

$$
\alpha(S_0\cup S_1)=\alpha(S_0)\cap\alpha(S_1)
$$

and consequently

$$
S_0\cup S_1\subseteq
\gamma\bigl(\alpha(S_0)\cap\alpha(S_1)\bigr).
$$

Moreover `alpha(S0) intersection alpha(S1)` is the most precise common-literal abstract element covering both branch sets. In contrast, pooling facts by set union computes conjunction:

$$
\gamma(K_0\cup K_1)=\gamma(K_0)\cap\gamma(K_1),
$$

which generally **underapproximates** the alternatives and can create a false bottom.

**Proof.** A literal is true in every valuation of `S0 union S1` exactly when it is true in every valuation of `S0` and every valuation of `S1`, proving the identity. Every state in either branch therefore satisfies every literal in the intersection, giving coverage. If a common-literal fact set `K` covers both branches, each literal in `K` is true in every state of both branches, hence `K subseteq alpha(S0) intersection alpha(S1)`; this establishes optimal precision in this domain. The last equation follows directly from the conjunctive definition of `gamma`. QED.

### Counterexample 463.2 — branch-local facts manufacture UNSAT

Take the satisfiable exact 2-CNF control

$$
F=(\neg x\lor y)\land(x\lor\neg y),
$$

whose models are `00` and `11`. Under branch assumption `x=0`, the only model is `00`, so the branch entails `not y`. Under `x=1`, the only model is `11`, so that branch entails `y`. Alternative reconvergence must cover `{00,11}`. The sound common-literal join retains no literal. Pooling `{not y}` and `{y}` conjunctively produces `{not y,y}` with empty concretization, falsely declaring the satisfiable source UNSAT.

This counterexample is semantic. It does **not** assert that the historical checker accepts such a join; instead it is a falsifier for any proposed abstraction or certificate checker that silently erases assumption scope or confuses OR reconvergence with AND conjunction.

### Native-rule transformer obligations

A cost-sound negative-proof abstraction for `[P2-D1]`, `[P2-C3]`, `[P2-B1]`, or `[P2-B2]` still needs a source-authenticated concrete state recording at least source bytes/identity, current assumptions, paid distinct-node history, definitions and freshness, exported/private wires, available conclusions, and the acyclic shared hypergraph. For **every** legal historical native transformer (including LOCAL-CONVERT, AND3, GF(2), definitions/facets, oriented Resolution, references, and any actually authenticated branch discharge), a concrete step of weight `w` must map to an admissible abstract step of weight at most `w`. Reuse must remain zero/additional-cost exactly when the calculus says so, and a shared node must not be charged independently on multiple unfolded paths. Missing a nonlinear shortcut, erasing provenance, omitting zero-cost closure, or assigning an inflated abstract cost invalidates the desired lower-bound direction.

The theorem above supplies only the reconvergence polarity for one semantic component. It does not authenticate all native transformers and therefore does not prove absence of a cost-`B` refutation.

## Independent computation and challenge

Published implementations:

- `experiments/review/lspv5_463_abstract_branch_join_polarity.py`, SHA-256 `895a7794a6be0c35bf1e8bd7248b64920258931f10556243b6738128692040a7`;
- `experiments/review/verify_lspv5_463_abstract_branch_join.mjs`, SHA-256 `cf86141365fb71ec4a8c5081d5eeb3254a62729333bc3a80dfb9fec2f05b4cef`;
- raw record `results/raw/arc/2026-11-09_0844_LSPV5_463_ABSTRACT_BRANCH_JOIN_RAW.json`, SHA-256 `b3005ab86b7235b858abe182ab5309b70aba0002c0aebfe394cb3230297a52a1`.

The Python implementation enumerated all 225 ordered pairs of nonempty subsets of the four two-variable valuations, checked the join identity and concrete coverage in every pair, and found that conjunctive fact pooling fails coverage in 168 pairs. It recorded 459 assertion groups. A separately written JavaScript implementation checked all 225 pairs with 452 checks and reproduced 168 failures. Both reproduced the explicit `x iff y` false-bottom control. They are semantic finite reimplementations, not executions of an authoritative `R_mix341` checker and not evidence of an asymptotic proof lower bound.

## Semantic, proof-cost, and algorithmic conclusions kept separate

- **Semantic UNSAT certification.** In a sound model overapproximation, bottom with `gamma(bottom)=empty` can certify that no concrete model remains, subject to the transformer's source/context correctness.
- **No cost-bounded refutation.** This is stronger and different. It requires coverage of every legal cost-at-most-`B` shared DAG, correct count-once charging, AND obligations, context discharge, reconvergence, and all legal algebraic/extension shortcuts. /463 alone does not provide it.
- **Abstraction undecided.** A nonempty overapproximation, failure to reach bottom, widening loss, or bounded-search exhaustion proves neither SAT nor absence of a cheaper concrete proof.
- **B3.** Abstract solver correctness or a polynomial abstract certificate does not prove `SAT in P => Wbar_R polynomial` for the same historical calculus. The noncircular simulation/reflection bridge remains `[P2-B2]` OPEN.

## Established-family / theorem / encoding / shortcut ledger

| Family and exact encoding | Published theorem/model | Mandatory shortcut controls | Remaining transfer |
|---|---|---|---|
| Odd-charge Tseitin on a connected cubic expander: one edge variable per edge; at each vertex the four signed 3-clauses encoding parity equal to the prescribed charge; `n=3h/2`, `m=4h`, encoded length `Theta(h log h)` under binary IDs | Urquhart and width-method descendants give exponential ordinary shared-DAG Resolution size for appropriate bounded-degree expanders | GF(2) Gaussian elimination, compact XOR proof, ER/extension reasoning, sharing and reconvergence | No all-rule historical `R_mix341` lower bound; source-authenticated GF(2)/definition transformer and cost coverage remain open |
| Unary pigeonhole principle `PHP^(n+1)_n`: pigeon clauses `∨_j x_ij` and pairwise collision clauses `not x_ij or not x_kj`; exact 3-CNF requires a stated chain/Tseitin encoding and preservation theorem | Haken gives exponential ordinary Resolution size for the standard encoding | Cook-style Extended Resolution has polynomial proofs; preprocessing and shared lemmas are legal upper controls | Equisatisfiability alone does not transfer the lower bound to an arbitrary 3-CNF reduction or mixed calculus |
| Pang opposite-characteristic mod-3 Tseitin strict 3-CNF, with published fixed-`r` `Res(PC_r/F_2)` lower bound and project-audited padding conventions | Restricted proof-system lower bound, not all algorithms and not all mixed rules | compact mod-3 adders, ER definitions, algebraic shortcuts, native GF(2), shared DAG | historical-rule simulation and coverage of every legal nonlinear shortcut remain open |

Certified UNSAT, restricted proof-size hardness, and empirical solver behavior are not conflated.

## Resource and trust ledger

The ideal proof minimum excludes discovery cost, as required. This run's implemented upper-side work still charged project/source reads, abstract-domain construction, exhaustive pair enumeration, JSON output, independent JavaScript recomputation, SHA-256 hashing, and publication/readback. Logical nodes in the semantic control: none in the historical calculus. Explicit evidence: two short programs plus a 1,132-byte raw record before final publication normalization. Search/construction time was dominated by repository and primary-source reads; finite enumeration took milliseconds. Peak space was constant in the four-state universe, but no asymptotic `R_mix341` space claim follows. No cache, sparse representation, or abstract-domain succinctness was converted into a proof-weight lower bound.

`main.tex` could be retrieved completely only by blob SHA; the path-level contents response returned zero text. The complete blob was used, both LSPV-5 ownership markers occurred exactly once, and any manuscript insertion is restricted to those markers with outside bytes preserved.

## Publication and full readback

Published atomically on `main` at commit `be106b7b9d108693ff2e375104e18cb39fec88df` from expected head `951e244264f915bd88dbf5d06965df5995e0ecde`. Complete readback matched every published byte. `proof1.txt` remained blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b` and 18,553 characters. `proof2.txt` changed only by the appended `[P2-L5-463]` node, from exact saved blob `89afcf53891435d92b8a093cec3b5ac28c6964b2` to blob `6ebdadebef786b1e75294a556d7718c3e8436a20` and 767,555 characters. `main.tex` changed from complete blob `abb3480f2272852c4184e90d5a7c9d1a5d9de213` to `59a9ab78d90d442bf1a0202d5b19304b64380128` and 1,793,861 characters; both ownership markers remained unique and all outside bytes were preserved. Coordination issue #3 comment `6746087725` was read back exactly. No role, task, schedule, timezone, enabled state, route allocation, rule, or weight changed.

## Revised claim and precise gap

**Actual advance.** `[P2-L5-463]` proves an exact common-literal branch-join theorem and gives a minimal satisfiable false-conflict control. It turns a qualitative warning about context erasure into a checked abstraction/concretization polarity condition: OR reconvergence needs a union-covering join; conjunctive pooling is a meet and is unsound for alternatives.

**Precise remaining gap.** To obtain a genuine mixed-calculus cost lower bound, one must define and authenticate a complete abstraction of the full source/context/paid-history shared DAG, give a cost-nonincreasing transformer for every legal historical `R_mix341` rule and shortcut, and then prove a lower bound on that abstract minimum. To obtain B3, one still needs the separate noncircular same-calculus decider-to-proof simulation/reflection theorem. `[P2-D1]`, `[P2-C3]`, `[P2-B1]`, and `[P2-B2]` remain OPEN. P versus NP remains OPEN.
