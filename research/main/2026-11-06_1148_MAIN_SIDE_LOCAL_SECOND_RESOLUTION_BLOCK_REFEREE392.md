# LSPV-5/REFEREE392: one side-local follow-up Resolution cannot reach AND3 at the 35-node floor

**November 6, 2026, 11:48 PST | Route B independent red team | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN.**

This report preserves the exact historical $R_{\mathrm{mix341}}$ grammar, source authentication, and weights. It adds no split, discharge, weakening, clause export, or semantic oracle. The finite advance refines REFEREE391: after the first cross-cut strict Resolution in any putative 35-node bridge refutation, one further strict Resolution against an arbitrary side-local clause still cannot produce a clause admissible to historical AND3.

The global interval remains

$$
35\le W_{R_{\mathrm{mix341}}}(F_{\mathrm{bridge}})\le37.
$$

## 1. Claim card and IDEA -> SEARCH -> ITERATE

**Claim ID:** LSPV-5/REFEREE392 side-local second-Resolution block.

**Status before run:** OPEN after REFEREE391.

**Exact quantifiers:** for every first cross-cut resolvent $C=\operatorname{Res}(L,R)$, where $L$ and $R$ are any historical source-once side-local clause outcomes, and every side-local clause outcome $D$ from either side, if $\operatorname{Res}(C,D)$ is strict and legal, then its support has size greater than three.

**Model:** authenticated 36-source bridge MUS; 35 paid binary nodes; full binary source-once tree; historical strict Resolution and support-at-most-three AND3. Clause outputs arise only from Resolution.

**SAME_REALIZATION:** the same original source indices, original-variable coordinates, strict pivots, and source-once child subtrees used by the claimed 35-node derivation.

**Initial falsifiers:**

1. a legal side-local clause $D$ reducing a first cross resolvent to support at most three;
2. a source-disjoint triple producing such a resolvent;
3. a cross-cut sibling subtree escaping the side-local test;
4. a peer or authoritative-checker 35-node trace.

Falsifiers 1 and 2 were rejected. Falsifier 3 remains the exact escape class; no claim below excludes it. Falsifier 4 was not found.

**Revised claim:** exclude exactly the one-additional-Resolution route with a side-local sibling, and state the surviving dichotomy. This is materially narrower than excluding all second Resolution steps.

## 2. Source, grammar, and prior dependencies

The fixed source is REFEREE386's 15-variable, 40-clause proper strict-3-CNF bridged cubic odd-Tseitin instance, DIMACS SHA-256

`4f8a7e613ace4f67cd0b62204cdda2a4d8072047bd55a70da23da282e3537b18`.

Its unique essential 36-clause MUS is indexed `0..15,17,18,20..36,39`. The two 18-source halves share only $x_{15}$. The historical grammar source remains `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex`, Git blob `c87acd11d32ccfc3b7acd3667ef11daeb60079cb`.

Dependencies retained at their verified scope:

- REFEREE386: every 35-node proof is a 36-source full binary source-once tree.
- REFEREE389: the pure-Resolution 35-node class is impossible.
- REFEREE390: every remaining 35-node proof contains a cross-cut AND3-produced factor/equation.
- REFEREE391: the lowest cross-cut ancestor of that block is strict Resolution; all first cross resolvents have support at least four.

No unary LOCAL, paid DEF, reconvergence, or source duplication fits at the 35-node floor. AND3 and XOR do not produce clauses consumable by strict Resolution. Therefore the present clause closure is complete for the stated intermediate type even though the whole mixed calculus is stronger.

## 3. Exact finite enumeration

For each side and every nonempty subset of its 18 authentic sources, the producer enumerates every source-once strict-Resolution clause outcome. It stores every globally keyed clause and an inclusion-minimal antichain of source masks. The independently written verifier instead uses base-3 clause encoding, a separately generated 43,046,721-entry local resolution table, and separately reconstructed truth vectors.

Both implementations reproduce:

| Quantity | Per side / global value |
|---|---:|
| Unique side-local clauses | 3,234 per side |
| Subset-clause occurrences | 11,705,410 per side |
| Side strict-Resolution pair tests | 1,126,097,195 per side |
| Legal first cross-cut resolvents | 4,056,196 |
| First cross resolvents of minimum support four | 6,724 |

A strict Resolution starting from a support-four clause can end at support at most three only if its sibling contains no variable outside those four. Hence the finite candidate set is complete: for each of the 6,724 support-four first resolvents, on each side enumerate every nonempty signed clause over a subset of those four variables. There are $3^4-1=80$ such clauses, where each variable is absent, positive, or negative. Thus exactly

$$
6724\cdot2\cdot80=1{,}075{,}840
$$

side-clause candidates were queried against the complete catalogs.

**Result:** zero catalogued side-local clauses form a legal strict second Resolution whose output support is at most three. This is a semantic zero before the source-mask disjointness test, so the source-disjoint count is also zero.

## 4. Theorem and proof

### Theorem 392.1 (PROVED/RESTRICTED, computer-assisted finite theorem)

Let $C$ be the lowest cross-cut strict resolvent in a putative 35-node historical refutation of the authenticated bridge MUS. For every side-local clause $D$ obtainable by a source-once strict-Resolution subtree, if $E=\operatorname{Res}(C,D)$ is a legal strict resolvent, then

$$
|\operatorname{supp}(E)|\ge4.
$$

Consequently $E$ cannot be consumed by historical AND3, whose combined original-variable input support is at most three.

### Proof

REFEREE391 proves $|\operatorname{supp}(C)|\ge4$. If it is greater than four, one strict Resolution can remove only the pivot while retaining every other literal of $C$ unless a tautology is formed; hence it cannot yield support at most three. It remains to consider the 6,724 possible first resolvents of support exactly four.

For a support-four $C$, any sibling clause containing an external variable leaves that variable in the resolvent, while at most one pivot variable is removed. Such a sibling cannot yield support at most three. Therefore every possible successful sibling is one of the 80 nonempty signed clauses over subsets of $\operatorname{supp}(C)$. The complete historical side-local clause catalogs contain every clause obtainable from every side source subset. Exhaustive testing of all 1,075,840 catalog queries and strict pivot orientations finds no legal support-at-most-three result. An independent base-3 implementation reproduces the same zero. $\square$

### Corollary 392.2 (surviving topology dichotomy)

On a directed path from the first cross-cut resolvent to REFEREE390's required cross-cut AND3, either:

1. some next Resolution uses a sibling subtree whose ancestry itself crosses the cut; or
2. at least two additional strict Resolution nodes occur before AND3.

This corollary does not exclude a complex cross-cut sibling, multiple further Resolution steps, or a 36-node proof.

## 5. Branching/shared-DAG interpretation

At the 35-node floor the paid dependency graph is a full binary tree, so each inference is an AND obligation over its two premises and every source occurs once. Alternative pivot choices and alternative source partitions are OR choices freely optimized after the fact. The enumeration grants all such legal choices.

No branch-local lemma is reused outside its assumptions, and no shared subproof is double-counted. The result does not add case splitting. At 36 nodes, reconvergence or a unary node becomes possible; those separate topology classes remain open. Work, critical-path span, and realizable retention/recomputation space are therefore not identified.

## 6. Established-family and transfer ledger

| Family | Exact encoding / size parameter | Certified theorem and model | Known shortcut control | Remaining historical transfer |
|---|---|---|---|---|
| Braun bit-PHP | $n=2^\ell$ holes, $n+1$ pigeons; pair lines are disjunctions of bit disequalities | Braun arXiv:2609.23015v2: all shared-DAG Res($\oplus$) proofs have $>\exp(n/(32768\ell^2))$ lines for $\ell\ge32$ | Cook ER after paid conservative definitions; LSPV-1/454 quantifies the necessarily exponential output of any backtranslation to the **original** Res($\oplus$) source | FACET-A is distinct from historical /341; native DEF/LOCAL/export typing remains OPEN |
| Pang random proper strict 3-CNF | $F\sim\mathcal F(n,3,8n)$, clauses sampled with replacement from $8\binom n3$ proper signed triples | Pang arXiv:2610.00837v2 plus linear PC degree: a.a.s. $\exp(\Omega(n))$ shared-DAG syntactic Res(PC$_1/\mathbb F_2$) | Paid definitions and LOCAL/export circuits remain legal | LSPV-3/456 covers only a locally opaque wire-defined fragment; unrestricted exposure yields only a linear paid-node bound |
| Haken unary PHP | Standard pigeon clauses and pairwise collision clauses | Haken 1985: no polynomial ordinary shared-DAG Resolution bound | Cook 1976 polynomial Extended Resolution proof | Equisatisfiable strict-3 conversion is not a lower-bound-preserving all-rule transfer |
| Cubic odd Tseitin | Four proper width-three clauses per degree-three parity vertex | Exponential ordinary Resolution on suitable expanders | Historical AND3/XOR proof has $4h-1$ paid nodes | Established family failure for mixed hardness |
| Authenticated bridge | 15 variables, 40 strict 3-clauses; 36-clause MUS | Finite certified UNSAT and exact bounded proof analysis only | Known 37-node proof uses 28 AND3, 6 XOR, 2 LOCAL, 1 RES | 35-node cross-cut sibling/multi-RES class and all 36-node classes OPEN |

Certified UNSAT, restricted proof-size hardness, and empirical solver difficulty remain distinct. None of these lower bounds is claimed against arbitrary SAT algorithms.

## 7. Literature, repository, and peer audit

Primary sources checked this run include Braun arXiv:2609.23015v2, Pang arXiv:2610.00837v2, Haken's 1985 TCS paper, Cook's 1976 ER PHP construction, and the read-once Resolution literature. The latter confirms that clause-once/read-once Resolution is an incomplete restricted proof model and that proof existence can be NP-complete even for restricted CNFs; it does not replace the exact source-mask computation.

Current project head at search time was `4106e52b83626af44783dfd2435aa95945ab34bb`. Issue #3 through the latest comments, LSPV-1/454, LSPV-3/456, Route-A peers, REFEREE391, the governing handoff, actual `GROKPROOF/2026-11-06_1617_PROGRESS.md`, and Claude `2026-10-28_1326_CLAUDE_TPORT-0001.tex` were read. LSPV-1/454 provides a quantitative original-source backtranslation firewall, not historical mixed hardness. LSPV-3/456 supplies the strongest current established strict-3 family transfer, but only in its explicit fragment.

Required repository heads were unchanged from the previous run: `konard/p-vs-np` `ecedd2b45...`, `blkph0x/p-vs-np-proof-research` `7dedc73f...`, FRAT-XOR `18cd6bc1...`, short-proof `2c524cfc...`, drat-trim `2e3b2dc...`, CNFgen `24e633bd...`, openai/math `4eaee875...`, and anthropics/formal-math `16a5ce41...`. Change-aware review reread konard's proof-status/complexity files, blkph0x's method index/status audit, FRAT-XOR's format, and short-proof's README. FRAT-XOR and short-proof use different proof languages; neither authenticates /341 or closes the mixed bridge class.

General indexed web search was used. A direct Google-branded interface was unavailable. The local scratch checkout was partial: the mandatory preflight explicitly reported missing root `main.tex`, skill, AGENTS, and CODEX files. Complete current versions were read through GitHub. No authoritative historical byte checker was located or executed.

## 8. Resource and hostile-control ledger

| Phase | Charged result |
|---|---|
| Primary logical enumeration | 2,252,194,390 side RES pair tests; 4,056,196 first cross pairs; 1,075,840 candidate second-side-clause queries |
| Primary construction | 37.774 s internal, 37.852 s shell wall; 789,804 KiB peak RSS; source-mask antichains retained |
| Independent verification | Separate base-3 clauses/table/truth vectors; 55.405 s internal, 55.539 s shell wall; 507,264 KiB peak RSS |
| Explicit evidence | Two C++ sources, two JSON result records, manifest, report, handoff, root fragment, exact issue outbox |
| Hostile controls | Thirteen count/support/result mutations rejected by the independent verifier |
| Failed verification policies | Two prior independent runs correctly returned FAIL because report-field and hostile-mutation meta-assertions were wrong; 55.095 s and 55.136 s were charged, then repaired and rerun |
| Parsing/search/source reads | Current heads, issue comments, reports, repository files, primary indexed literature; remote service time/space unexposed |
| Simultaneous measured peak | 789,804 KiB; remote caches and publication-service memory unmeasured |

The producer's materialized subset closures and mask antichains are implementation costs, not lower bounds on proof space. The ideal $W_R$ minimum continues to grant free after-the-fact choice of the best legal derivation. No FLMV same-machine claim follows.

## 9. B3 verdict and remaining gap

This finite obstruction supplies neither a superpolynomial full-mixed family nor a compiler from an arbitrary polynomial SAT decider into this same calculus. It does not formalize correctness/reflection for arbitrary deciders. B1, B2, B3, superpolynomial $\overline W_{R_{\mathrm{mix341}}}$, and P versus NP remain **OPEN**.

**Actual advance:** no first cross-cut resolvent can be reduced to a historical AND3-admissible clause by exactly one further strict Resolution with any side-local sibling. The zero holds even before source-disjointness filtering.

**Precise finite gap:** enumerate or structurally exclude (i) a next Resolution whose sibling subtree is itself cross-cut, and (ii) paths with at least two further strict Resolution nodes before AND3, preserving exact source masks. Then analyze the three 36-node topology classes.

**Precise asymptotic gap:** prove a lower-bound-preserving original-source transfer through every historical native shortcut, or find a legal counterexample, and separately prove a noncircular same-system B3 implication.

## Artifacts

- `experiments/review/lspv5_392_second_resolution.cpp`
- `experiments/review/lspv5_392_independent_verify.cpp`
- `results/raw/review/2026-11-06_1148_LSPV5_SECOND_RESOLUTION392.json`
- `results/raw/review/2026-11-06_1148_LSPV5_SECOND_RESOLUTION392_verification.json`
- `results/raw/review/2026-11-06_1148_LSPV5_SECOND_RESOLUTION392_manifest.json`
- `research/coordination/2026-11-06_1148_LSPV5_SIDE_LOCAL_SECOND_RESOLUTION392_HANDOFF.md`
