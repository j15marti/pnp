# LSPV-3/435: Two-paid-node exact LOCAL port restoration

**2026-11-05 17:31 PST. Route B. PROVED/RESTRICTED in the printed historical semantic R_mix341 rules; COMPUTATIONAL independent checks; full historical byte grammar, polynomial global translation, B3 and P vs NP OPEN.**

## Hypothesis, falsifiers and material revision

LSPV-3/434 and LSPV-5/373 show that ordinary-Resolution restriction strengthens a derived clause (u OR v) to the unit u, invalidating downstream exact AND3 parity annotations. The hypothesis was that **two already justified clauses on <=3 original variables** can produce their exact conjunction with paid AND3, then use one paid LOCAL-CONVERT to derive an **exact desired clause implied by that conjunction**. Falsifiers: wrong local truth implication; incorrect exact affine table; changed source identity or antecedent scope; corrupt source/row/pivot accepted.

Historical duplicate review found stronger paid DEF-based clause weakening already established in LSPV-2/352 and LSPV-3/360. This run **does not claim to invent general weakening**. The specific advance is a DEF-free, shared-DAG, exact-port reconstruction for the previous /434 failure, with an 11-node proper-3CNF typed mixed certificate and complete semantic replay. Proposed CANON2R checker acceptance of this NEW eleven-node certificate is NOT claimed.

## Lemma: bounded-local two-node consequence macro

For source-authenticated clauses C,D with combined original support S of cardinality <=3 and a target clause E over S with C AND D logically implying E on *all* 2^|S| valuations, the printed R_mix341 rules authorize:

$$
P=\\operatorname{AND3}(C,D),\\qquad Q=\\operatorname{LOCAL-CONVERT}(P\\Rightarrow E).
$$

Every derived node is charged once. The first is the exact truth-table conjunction, the second an explicit constant-support implication. There is no new weakening axiom, private port, DEF facet, or model-only equivalence. Attached branch assumptions, if any, must follow both parents and are not silently discharged.

Choose C=(u) and D=(NOT u OR v). AND3 derives exact factor u AND v, which implies **both** (u OR v) and (u OR NOT v). Two paid LOCAL outputs from the **same** shared factor allow the exact opposite affine annotations: (u OR v) AND (NOT u OR NOT v) iff u XOR v=1, whereas (NOT u OR v) AND (u OR NOT v) iff u XOR v=0. One paid GF(2) XOR concludes 0=1.

## Exact source and paid certificate

Source is the previous /434 complete signed padding of (u) AND (NOT u OR v) AND (NOT u OR NOT v). Six numbered original variables (u,v,z,w,t,s)=(1,2,3,4,5,6). Eight strict proper-3CNF original clause IDs are

```text
S0=(1,3,4) S1=(1,3,-4) S2=(1,-3,4) S3=(1,-3,-4)
S4=(-1,2,5) S5=(-1,2,-5) S6=(-1,-2,6) S7=(-1,-2,-6)
```

Eleven paid DAG nodes:

| ID | Rule | Parents and conclusion |
| --- | --- | --- |
| 1 | RES | S0,S1 on w -> (u OR z) |
| 2 | RES | S2,S3 on w -> (u OR NOT z) |
| 3 | RES | S4,S5 on t -> (NOT u OR v) |
| 4 | RES | S6,S7 on s -> (NOT u OR NOT v) |
| 5 | RES | 1,2 on z -> (u) |
| 6 | AND3 | 5,3 -> exact factor u AND v |
| 7 | LOCAL | 6 -> exact clause (u OR v) |
| 8 | AND3 | 7,4 -> exact GF2 row u XOR v=1 |
| 9 | LOCAL | 6 **shared** -> exact clause (u OR NOT v) |
| 10 | AND3 | 3,9 -> exact GF2 row u XOR v=0 |
| 11 | XOR | 8,10 -> 0=1 |

Every source clause is an authenticated ancestor; no branch assumption, case-split, uncharged weakening, auxiliary definition or altered original-source ID occurs. Nodes 8 and 10 are exactly the GF(2) factors on **all four assignments**, not merely on UNSAT source models. Logical paid work=11, critical-path depth=6 under the specified ideal unit-per-node model; this is not physical time or space. The **pre-existing exact global minimum is seven nodes**, so this explicitly typed mixed proof is not optimal. The earlier 13-node mixed diagnostic is reduced by two nodes.

## Strict-RES obstruction and stronger native repair

From unpadded clauses (u), (NOT u OR v), (NOT u OR NOT v), strict RES can never produce the exact clause (u OR v): by induction the only derived clause carrying positive u is the singleton (u), which cannot resolve on a non-u pivot. Its full non-tautological strict-RES closure contains seven clauses. This is a RES-only obstruction, **not** a full-mixed obstruction: paid AND3+LOCAL repairs it in two nodes, and earlier paid-DEF macros already repaired wider weakening cases.

## Checks, sources, resources

Local full Python checker passed 90 certificate assertions, 64 UNSAT assignment controls, eight source-deletion SAT witnesses and 10/10 deliberate negative controls. A separately written Node checker passed 167 assertions. The compact, separately published self-contained replay returned **128 assertions passed**. Only the printed semantic rule fragment is checked, not an authoritative historical parser. Compact original-source bytes=129; complete typed certificate=1,166 JSON bytes. Distinct paid nodes=11, plus eight free source leaves; 5 RES, 3 AND3, 2 LOCAL, 1 XOR. Explicit evidence verification has polynomial cost in its stored bit size; search, failed paths, reading, caches, machine time and peak space are separately charged for any algorithmic interpretation. Ideal proof optimum has free after-the-fact choice.

Research audited actual original `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex` blob c87acd11; /434 report b8028c05; LSPV-5 /373 report 143a97a4; earlier /352 and /360 weakening; governing five-role directive current blob c3889a3e; issue #3; AGENTS/CODEX/pnp-research skill; Grok `GROKPROOF/2026-11-05_1428_PROGRESS.md` and Claude `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex`. Both newly required research repos reviewed: konard/p-vs-np `proofs/experiments/README.md` blob 4c8752aa discloses admitted gaps; blkph0x/p-vs-np-proof-research `METHOD_INDEX.md` blob 18d693ea distinguishes scoped results, and `RESIDUAL_EQUIVALENCE_BARRIER_REPORT.md` blob 46413596 explains global exact equivalence cost. FRAT-XOR `format.md` blob 986a21aa; CakeML/LPR `README.md` blob e94f45e9; actual Github searches in openai/math, ABC, mockturtle. Indexed primary source is de Rezende et al., CCC 2020, DOI 10.4230/LIPIcs.CCC.2020.28, which establishes ordinary DAG-Resolution lower bounds for specified sparse expander PHP formulas, **not** full mixed-calculus hardness. Cubic odd-Tseitin has the already known linear GF(2) shortcut, and PHP has ER/Frege shortcuts. The strict padded instance here is only a focused proof-transfer diagnostic. No direct Google-branded search or local git clone was available. 

**OPEN next step:** audit actual CANON2R byte acceptance for this exact repair, then authenticate historical LOCAL/export semantics; seek a polynomial bound on repairs across all mixed shared DAGs including high-width GF(2), nested paid DEF and reconvergence. Nothing here proves B3 or superpolynomial full-mixed Wbar_R. P vs NP OPEN.

References: [1] de Rezende et al., CCC 2020, DOI 10.4230/LIPIcs.CCC.2020.28. [2] Buss, JSL 1987, polynomial Frege PHP. [3] Cook, SIGACT News 1976, Extended Resolution PHP. [4] Ben-Sasson and Wigderson, JACM 2001, resolution width/size.
