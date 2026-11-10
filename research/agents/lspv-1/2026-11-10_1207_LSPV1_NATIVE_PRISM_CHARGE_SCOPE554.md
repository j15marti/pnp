# LSPV-1/554: Infinite prism and odd-charge SOURCE/AND3/XOR native-checker acceptance slice

**November 10, 2026, 12:07 PST | General SAT Lower-Bound Lead | Route B | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

## IDEA, theorem and falsifiers registered before search

**Candidate NATIVE-554.** The original recovered LSPV-2/341 checker, despite checking seven prepackaged examples and failing to implement the full prose-declared mixed calculus (LSPV-1/553), accepts source-authenticated, binary-typed proof records for an **infinite parameterized family** of cubic-prism odd-Tseitin strict 3-CNFs, with arbitrary odd vertex charge vectors, after a transparent extension of the *producer alone*. The accepted proof contains exactly $8k-1$ paid AND3/XOR nodes on a prism of size $k$.

Falsifiers: **F1**, a legitimate non-prepackaged prism fails the unchanged original verifier; **F2**, a non-root, still-odd charge vector fails because the verifier hardcodes the original vector; **F3**, changing a signed original source clause or affine sink leaves a purported source-bound certificate accepted; **F4**, the test accidentally authenticates RES, DEF, LOCAL-CONVERT, branch or context rules never implemented by this verifier.

F1-F3 were falsified in the named restricted test scope (all new prisms and odd-charge vectors accepted; corruptions rejected). F4 remains a boundary: this work makes **no** full-calculus authentication claim.

## Source and actual project-state audit

Read both complete root trackers, issue #3, AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md, November 9 abstract-negative and assumed-time directives, November 10 current five-role reports and handoffs, the original /341 producer and checker, original /341 semantic specification, relevant /539-549 reports and actual Grok note 2026-11-10_1523. The latest relevant LSPV-5 /477, LSPV-1 /553, LSPV-2 /537, LSPV-3 /550 and LSPV-4 /522 are retained, not superseded. The actual Claude artifact was not uniquely located in this pass, so no Claude result is newly attributed.

Pinned exact originals:
- producer: experiments/arc/lspv2_341_mixed_tseitin_min_dag.js, Git blob **4081022e8a3841d79f751a3d3a7a10decbb026da**;
- checker: experiments/arc/lspv2_341_independent_verify.js, Git blob **fcb7d4ced8f922de14c0bda16263a8cc7853e8e0**;
- declared semantics: research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex, blob **c87acd11d32ccfc3b7acd3667ef11daeb60079cb**.

Primary references searched: Cook–Reckhow (1979), for proof-system versus checker scope; Cousot–Cousot (1977), for sound simulation; original graph/Tseitin proof-complexity literature for the restricted algebraic shortcut. External source controls re-read: konard/p-vs-np/scripts/proof_status.json (blob 93b77ed3d8fe456f81c690035f45f07910a247f2), blkph0x/p-vs-np-proof-research/METHOD_INDEX.md (18d693ea71dfa433370eb7afbebc3106e32f03e5), meelgroup/frat-xor/format.md (986a21aa92b62f844ef1fce852193142c41b2b1f). None is the missing native all-rule grammar; formalized and external proof formats must not be substituted for it.

## Theorem 554.1: positive parameterized acceptance in the recovered checker

For every integer $k\ge3$ let $G_k=C_k\square K_2$ be the $2k$-vertex cubic prism graph, with $3k$ edges. For each vertex-charge vector $\chi\in\{0,1\}^{2k}$ satisfying $\bigoplus_v\chi_v=1$, define the exact signed strict 3-CNF $F_{k,\chi}$ by inserting four clauses forbidding the four wrong-parity edge assignments at each vertex. Let $V_{341}$ be the exact recovered independent checker function.

**Claim, scoped to the recovered test-checker's integer/finite-memory execution model:** There is an explicit producer $P(k,\chi)$ such that the unmodified $V_{341}$ accepts its source-bound source/AND3/XOR proof record and checks exactly

$$
n=3k,\qquad m=8k,\qquad q=8k-1
$$

original variables, original clauses, and globally distinct paid derived nodes, respectively. The source is the exact graph-derived signed CNF inside the accepted packet. This is **not** independent binding to a separately supplied external DIMACS file.

**Construction and proof:** Each of $2k$ vertices contributes four distinct proper source clauses. Conjoin these four local factors with three AND3 nodes whose support stays on that vertex's three incident original variables. The final local factor has precisely the truth table of the charge-$\chi_v$ parity equation, so the checker authorizes a row annotation. Combine the $2k$ vertex rows in any fixed binary XOR chain with $2k-1$ paid XOR nodes. Every edge appears in exactly two rows, giving zero final mask; odd charge gives final right-hand side one. Thus the terminal node proves $0=1$. Every source is an ancestor, the paid IDs are globally fresh, and every inference has exactly two earlier parents. The checker evaluates precisely these AND3 tables, XOR rows, ancestor IDs and terminal condition. The prism is connected, cubic and bridgeless; removing any vertex leaves it connected. Standard incidence-rank reasoning therefore supplies, for every deleted original clause, an edge assignment satisfying every remaining source clause. These $8k$ deletion-witness strings pass the actual checker's source-essentiality checks. An all-zero-edge assignment is the required even/zero-charge control. All named guards exercised by the original verifier are thus satisfied for every finite representable $k$ and odd $\chi$. This is a code- and model-conditional parameterized correctness proof, not an all-rule accepted grammar.

The original /341 producer was written specifically for $\chi=(1,0,\ldots,0)$ and took its even-check witness by clearing coordinate zero. To generate *arbitrary* odd $\chi$ without changing the original verifier, the producer extension changes only: (i) the graph list; (ii) charge-vector initialization for named additional fixtures; (iii) the even-control witness to a solution of the **all-zero** charge system, which is what the original verifier actually checks. These changes are disclosed in executable code. The original verifier's mathematical body is untouched; only file/console I/O is adapted for direct V8 execution.

**Independent lower-bound check:** Since every original clause is indispensable, any sound source-explicit shared DAG with two or fewer prerequisites per paid derived node and with unit native logical cost needs at least $m-1$ such nodes. A connected graph with $m$ distinct leaf ancestors in a binary DAG needs at least $m-1$ internal nodes, regardless of reconvergence or sharing. Thus the displayed proof achieves the known declared-calculus minimum $q=8k-1$. This is a **linear upper/lower match**, not a superpolynomial hard family. The prism family is not claimed to be an expander-hard Resolution family.

## Theorem 554.2: intrinsic canonical evidence-vs-work separation

Every clause deletion has an explicit witness of **exactly $3k$ edge bits**, because each individual original source clause is essential. The recovered packet includes a deletion witness for each of its $8k$ clauses. Hence the original checker packet's deletion-assignment substrings alone contain exactly

$$
8k\cdot3k=\boxed{24k^2}
$$

binary digits, whereas native paid logical work is $q=8k-1$. This is **not** an argument for a computational time/space lower bound: the deletion-witness format is an optional checker/producer requirement in this restricted tool and can be omitted by a different authenticator. It is an exact byte-accounting result for this accepted evidence format. The original formula has binary DIMACS length $\Theta(k\log k)$ (with standard decimal variable labels); emitted JSON packet size is $\Theta(k^2)$ for this construction.

## Actual execution: original checker unchanged

Evaluated the original GitHub-fetched producer/verifier JavaScript functions directly in V8, replacing only Node I/O and transparently patching three producer generation sites specified above. The combined packet contained **46 fixtures**: the seven original fixtures, seven new prism sizes $k=3,4,5,8,12,24,40$, and all **32** odd charges on the six-vertex prism. The unchanged recovered verifier returned **234,527 assertion groups** and accepted every fixture.

| Prism $k$ | Clauses $8k$ | Paid nodes $8k-1$ | Deletion-witness digits $24k^2$ | Full fixture JSON characters |
| ---: | ---: | ---: | ---: | ---: |
| 3 | 24 | 23 | 216 | 5,090 |
| 4 | 32 | 31 | 384 | 6,893 |
| 5 | 40 | 39 | 600 | 8,759 |
| 8 | 64 | 63 | 1,536 | 14,702 |
| 12 | 96 | 95 | 3,456 | 23,365 |
| 24 | 192 | 191 | 13,824 | 54,852 |
| 40 | 320 | 319 | 38,400 | 108,909 |

Five deliberate faults were **rejected** by the unmodified checker: signed original clause mutation, false affine sink, even-charge mutation, unsupported RES tag, and deletion of an original source clause. The first three directly challenge source/goal soundness; RES rejection is **evidence of missing grammar**, not an argument that RES is illegal in declared historical $R_{\rm mix341}$.

The original V8 bodies and three source-patch sites were executed in this run. The newly committed standalone Node executable has **not** been run from a complete local Git checkout. No historical all-rule executable, repository-wide preflight, or independent peer review was executed.

## Full-calculus abstract relation and quantifier ledger

For a fully authenticated native grammar $R$, the required complete configuration remains $C=(F_{\rm bytes},D,\mathrm{Paid},\mathrm{Contexts},\mathrm{Defs},\mathrm{Fresh},\mathrm{Provenance},\mathrm{Available},q)$, including full shared DAG, all exact fixed rule weights and active/discharged assumptions. Define

$$
W_R(F)=\inf_{\pi\text{ accepted, source-bound refutation of }F}
 \sum_{v\in\mathrm{Paid}(\pi)} w_R(v)
$$

with any authenticated reference tariffs charged separately. A sound abstraction must simulate **every** legal native transition, preserve completed goals, and assign no greater path cost. The present source/AND3/XOR positive slice only permits an exact restricted projection $(F,D,\mathrm{Paid},\text{factor masks},\text{affine rows})$ with $\alpha$ mapping its typed, globally unique nodes and $\gamma$ including the byte-accepted packets matching that projection. The trace maps to equal paid count, never twice-charge a shared node, and empty contexts in this subset; all unknown genuine full-calculus steps remain unexcluded.

| Obligation | Status |
| --- | --- |
| P2-D1 | **OPEN.** Positive parameterized accepted-byte subset now established, but no external DIMACS binding, RES, DEF/facet, LOCAL-CONVERT, wire-scope, branching/discharge, WEAKEN/JOIN/DELETE grammar, or full checker. |
| P2-C3 | **OPEN.** Restricted exact trace projector is not an all-step abstraction. |
| P2-B1 | **OPEN.** This family has linear $W$ in the declared two-premise calculus; no mixed hard-family superpolynomial lower bound. |
| P2-B2 / B3 | **OPEN.** No same-calculus transfer from arbitrary deterministic SAT algorithms. |

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Full current root proof1.txt blob **96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b** (18,553 characters) and proof2.txt blob **6b2cbbe7b8686a0d4dd7d8a14b22263712bb1ab0** (898,762 characters) were fetched and checked; no load-bearing theorem status or dependency changed. Root main.tex fetch returned SHA **eac3e36f3d2576ac5e6f830457194cb73479eddd** but **zero content bytes**; no manuscript edit was attempted and outside-region integrity was preserved.

**Peer handoff:** LSPV-3 should authenticate whether any actual full-parser entrypoint accepts a signed external DIMACS with a native RES record, then verify DEF-facet owner/freshness and branch discharge. LSPV-5 should independently rerun the pinned code, examine the parameterized acceptance proof (especially deletion witnesses), and try an odd non-root charge and hostile source mutation. LSPV-2/4 retain Route A identities; neither this accepted fragment nor proof size discharges their computational resource bridges.

**Actual advance:** A source-sensitive, non-prepackaged infinite family of accepted original SOURCE/AND3/XOR proof records, including all tested odd charges, plus a precise quadratic canonical evidence-bits separation, with actual verifier replay and negative controls. **Remaining gap:** authoritative accepted-byte semantics for *all* historical rules and the full mixed proof-cost lower bound. P versus NP remains **OPEN**.

### Primary references
1. Cook S, Reckhow R (1979). The Relative Efficiency of Propositional Proof Systems. *J Symbolic Logic* 44(1):36–50. DOI 10.2307/2273702.
2. Cousot P, Cousot R (1977). Abstract Interpretation: A Unified Lattice Model for Static Analysis of Programs by Construction or Approximation of Fixpoints. POPL. DOI 10.1145/512950.512973.
3. LSPV-2/341 original declared graph-Tseitin source and exact two-premise lemma, linked above.
