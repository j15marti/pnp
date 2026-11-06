# LSPV-5/REFEREE388: exact read-once Resolution obstruction at the bridge cut

**Role:** LSPV-5 independent red team (Route B)  
**Pacific timestamp:** 2026-11-06 07:48 PST  
**Status:** **PROVED-RESTRICTED** exact finite non-derivability in strict source-once Resolution; **COMPUTATIONAL** exhaustive closure and independent replay. The global mixed minimum, all asymptotic full-mixed lower bounds, B1/B2/B3, and P versus NP remain **OPEN**.

## 1. Idea -> search -> iterate

REFEREE386 proved that any 35-node proof of the bridge-cut control must be a 36-source full binary tree. REFEREE387 excluded the tempting mixed tree obtained by treating two LOCAL implications as exact affine annotations. The next strongest known construction is purely Resolution: use all 18 essential left sources once to derive $x_{15}$, all 18 essential right sources once to derive $\neg x_{15}$, then resolve once. This would have $17+17+1=35$ paid nodes.

Precise falsifiers were:

1. either 18-source side has an exact strict read-once Resolution derivation of its required unit;
2. the enumerator drops or reuses a source, admits a tautological resolvent, weakening, or reversed pivot;
3. the two side contexts share a source or fail to semantically entail their target units;
4. current LSPV-1/3 work already gives a legal authenticated 35-node trace.

Falsifiers 2--4 did not fire. Falsifier 1 also failed: exhaustive closure finds no target unit on either side. The revised result excludes the canonical pure-Resolution realization of the 35-node topology. It does not exclude a global read-once Resolution tree that interleaves the two sides before its final stages, nor any mixed AND3/XOR/RES tree.

## 2. Exact source/family/theorem ledger

The finite control is the same native proper 3-CNF used in REFEREE386--387: two $K_4$ graphs, edge $(0,1)$ subdivided in each by vertices 4 and 9, joined by bridge edge 15. There are 10 vertices, 15 original edge variables, and 40 proper ternary Tseitin clauses with charge vector $(1,0,\ldots,0)$. Exact DIMACS SHA-256:

`4f8a7e613ace4f67cd0b62204cdda2a4d8072047bd55a70da23da282e3537b18`.

The unique 36-clause minimally UNSAT core was exhaustively authenticated in REFEREE386. The side source sets are

$$
L=\{0,1,\ldots,15,17,18\},\qquad
R=\{20,21,\ldots,35,36,39\}.
$$

They are disjoint, each has 18 sources, and share only original variable $x_{15}$. Complete truth-table evaluation confirms $L\models x_{15}$ and $R\models\neg x_{15}$.

| Family/control | Exact encoding and parameter | Established theorem/model | Known shortcut | Remaining transfer |
|---|---|---|---|---|
| Cubic-expander odd Tseitin | Proper 3-CNF; $h$ vertices, $3h/2$ variables, $4h$ clauses | **PROVED-RESTRICTED:** Urquhart, *Hard examples for resolution*, JACM 34(1), 1987, DOI [10.1145/7531.8928](https://doi.org/10.1145/7531.8928), exponential ordinary Resolution lower bounds | Historical AND3+GF(2) gives a $4h-1$ mixed proof on bridgeless cubic instances | No lower-bound-preserving transfer through all mixed rules |
| Bridge-cut finite control | Fixed $h=10$ proper 3-CNF above | **COMPUTATIONAL:** unique 36-source MUS; **PROVED-RESTRICTED:** 35-node binary ancestry floor | Legal work-37 mixed proof; LOCAL implications cannot be coalesced as exact rows | Exact mixed minimum remains 35--37 |
| Pigeonhole principle | Standard wide pigeon clauses and binary collisions; not native 3-CNF | **PROVED-RESTRICTED:** Haken, TCS 39 (1985), DOI [10.1016/0304-3975(85)90144-6](https://doi.org/10.1016/0304-3975(85)90144-6), exponential ordinary shared-DAG Resolution | Extended Resolution has polynomial proofs | No reverse proof simulation for a chosen 3-CNF reduction into full $R_{\rm mix341}$ |
| Clause-read-once Resolution | Every source and derived clause is consumed at most once; a full proof is a binary tree | **KNOWN restricted model:** Kleine Büning--Zhao, *The Complexity of Read-Once Resolution*, AMAI 36 (2002), DOI [10.1023/A:1016339119669](https://doi.org/10.1023/A:1016339119669); recognizing read-once refutability is NP-complete. The 2-CNF specialization remains NP-complete in TCS 729 (2018), DOI [10.1016/j.tcs.2018.02.002](https://doi.org/10.1016/j.tcs.2018.02.002). | DAG sharing, repeated clauses, AND3, XOR, LOCAL, and DEF are stronger controls | This finite ROR obstruction is not a lower bound for general Resolution or the mixed calculus |

Certified UNSAT, restricted proof-size obstruction, and empirical solver difficulty are separate. This report proves the second only for the exact finite side-unit task and exact restricted proof model.

## 3. Exact closure theorem

For a nonempty subset $S$ of one side's 18 source IDs, let $D(S)$ be the set of non-tautological clauses derivable by a full binary strict-Resolution tree whose leaves are exactly the sources in $S$, each used once. No weakening, source copying, derived-clause reuse, split, or discharge is allowed.

The recurrence is

$$
D(S)=\bigcup_{A\mathbin{\dot\cup}B=S}
\{\operatorname{Res}_p(C,D):C\in D(A),D\in D(B),
\text{ exactly one complementary pivot and non-tautological resolvent}\}.
$$

Singleton sets contain exactly their source clause. To remove symmetric duplication, the enumerator requires the least source bit of $S$ to lie in $A$.

**Lemma (closure completeness).** The recurrence gives exactly all strict source-once Resolution-tree outcomes for $S$.

**Proof.** Induct on $|S|$. Every generated clause joins two legal disjoint-source child trees, so it is legal. Conversely, the root of any full binary source-once tree partitions its leaves into two nonempty disjoint sets $A,B$ and strictly resolves the two child-root clauses. The induction hypothesis places those clauses in $D(A),D(B)$, and the canonical orientation enumerates that partition. $\square$

**Theorem (side-unit obstruction).** For the authenticated bridge source,

$$x_{15}\notin D(L),\qquad \neg x_{15}\notin D(R).$$

The exhaustive closure performs 1,126,097,195 clause-pair tests per side. It produces 154,950,040 valid strict resolvents per side before deduplication, and 1,888 distinct full-source outcomes per side. Neither target unit occurs. The per-leaf-count state totals are

$$
(18,48,304,1344,5664,22904,77872,232508,594832,
1239844,2045120,2567624,2386384,1588000,713376,
197992,29688,1888).
$$

Therefore the canonical 35-node construction consisting of two 17-node source-once side-unit trees and one root Resolution does not exist.

## 4. Independent implementation and adversarial controls

The producer uses positive/negative 8-bit masks for local clauses and constructs each subset closure directly. The independent verifier uses a different base-3 encoding (trits absent/positive/negative) and a separately built 43,046,721-entry strict-resolution table. It independently reconstructs both side sources and repeats both exhaustive closures. It reproduces exactly 1,888 full outcomes and 1,126,097,195 pair tests per side, with both targets absent.

Four corrupt controls are rejected: a forged target-present result, full-outcome count 1,887, pair count off by one, and deletion of the producer conclusion. The independent checker also requires the original DIMACS hash and both semantic-entailment records.

The computation is finite and exhaustive for this explicit rule/subset scope. It is not execution of an authoritative historical accepted-byte checker and not a finite optimizer over AND3, XOR, LOCAL, DEF, reconvergent DAGs, or interleaved global Resolution trees.

## 5. Branch/shared-DAG interpretation

At the 35-node ancestry floor, all 36 essential sources and 35 binary paid nodes form a source-once tree: no unary node, nullary node, or reconvergence is available. The tested construction respects every AND obligation: all 18 sources on each side and both unit subproofs are required. The choice of a Resolution-tree shape, child partition, and pivot is an OR alternative; the closure minimizes over all such alternatives after the fact.

No assumption context occurs. No branch-local unit is reused outside its source ancestry. No case-split/discharge or weakening rule is added. A DAG with sharing cannot fit the 35-node topology because reconvergence would add cycle-rank excess under the already-proved ancestry identity. However, a 36-node candidate may spend its single excess on one reconvergence, one unary step, or one extra source; none is excluded here.

## 6. Search/project/repository ledger

Read or change-checked at current project head: governing five-role handoff; issue #3 through LSPV-4/441; REFEREE386--387; LSPV-3/450--451; AGENTS.md; CODEX.md; the research skill; actual `GROKPROOF/2026-11-06_1520_PROGRESS.md`; and actual Claude `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex`. LSPV-3/451's multi-assumption XOR projection is explicitly restricted to supplied pure-XOR contextual proofs and does not construct the missing side units or legalize mixed discharge.

Primary indexed search authenticated the read-once Resolution literature above, Urquhart's expander-Tseitin theorem, and Haken's PHP theorem/ER shortcut statement. Direct Google-branded UI was unavailable; indexed search was used and is not reported as Google execution.

Required repository deltas were unchanged:

| Repository | Head | Result |
|---|---|---|
| `konard/p-vs-np` | `ecedd2b45f1c524d85c00b2da27a9c140025550c` | No read-once bridge certificate, historical `/341` authority, or full mixed transfer theorem found |
| `blkph0x/p-vs-np-proof-research` | `7dedc73f758dfbdc072e7aa29dfc08505761ebd5` | No read-once bridge certificate or all-rule transfer; affine experiments remain controls |
| `meelgroup/frat-xor` | `18cd6bc17af10a9891c10a846ce966166f9fe0dc` | Concrete mixed clause/XOR checking in a different format, not historical `/341` |
| `peitl/short-proof` | `2c524cfceecf68b56f51d23f6b63255b502856d3` | Restricted shortest-Resolution tooling; no matching read-once artifact found |
| `openai/math` | change-aware project search | No read-once Resolution result or native mixed bridge found |

## 7. Resource ledger

| Phase | Charged result |
|---|---|
| Logical candidate | Two 17-node source-once side trees plus one root RES: 35 paid nodes if it existed. It does not. |
| Enumeration | 1,126,097,195 pair tests and 154,950,040 legal pre-dedup resolvents per side; 2,252,194,390 pair tests total. |
| Explicit evidence | 1,888 full outcomes per side plus complete layer counts; raw JSON 72,877 bytes; verification JSON 340 bytes. |
| Producer | Final run 16.9751 s; 34,608 KiB maximum RSS. |
| Independent verifier | Final run 29.5706 s; 118,528 KiB maximum RSS, including the 43,046,721-entry base-3 resolution table. |
| Compilation | Two separate optimized C++20 builds; compile errors from missing headers/one malformed declaration were repaired and charged as failed setup work. |
| Failed policy | A separate top-down goal recurrence was attempted, produced no certificate after at least 135 s, and was interrupted. It is not used as evidence. Earlier random tree search from REFEREE386 is likewise non-load-bearing. |
| Parsing/source reads | Original graph/source reconstruction, exact side IDs, repository/issue/head reads, peer/Grok/Claude files, literature and repository deltas. |
| Caches/recomputation | Producer stores sparse subset closures. Verifier independently recomputes with a dense base-3 resolution table; it does not trust producer states. |
| Output/publication | Serialization, hashes, report, handoff, root fragment, Git-object writes, issue comment, and exact readback are separate charged phases. |
| Simultaneous measured peak | At least 118,528 KiB locally. Connector/publication memory is unmeasured and not claimed. |

Artifact SHA-256 values before publication:

- producer: `2063701a6c14d511c5b4cd956cc97126e53e6af99d50dbbbd08ea36f37dd932a`;
- independent verifier: `28ae54313419543f61850267aefe65577ccd265959de9e7107cf42ba6377ef16`;
- raw closure: `051f0c0596b788c3b14116d1acfaf35ca1a2325c22d55ec8e756f4ef1cf2e470`;
- verification: `db9ec0acd0390cfa75a4e4f91e016fd15c469b036faa0a2b5bac84ad7f16487c`.

## 8. B3 verdict, advance, and remaining gap

This exact non-derivability concerns a restricted finite proof class. It neither proves a superpolynomial $\overline W_R$ bound nor supplies B3. A polynomial SAT decision bit still does not construct source-authenticated proofs or establish arbitrary-decider reflection inside the same fixed calculus.

**Actual advance:** the most direct pure-Resolution 35-node construction is exhaustively excluded. Although each side semantically forces its bridge unit, neither unit has a strict Resolution tree using all 18 side sources exactly once.

**Precise remaining gap:** exclude (or construct) an interleaved global 35-node RES/AND3/XOR tree, then the three 36-node topology classes, under exact historical rule semantics. Separately, transfer an established asymptotic lower bound through every legal mixed shortcut and prove a noncircular same-system B3 bridge. P versus NP remains **OPEN**.

## Artifacts

- `experiments/review/lspv5_388_readonce_resolution.cpp`
- `experiments/review/lspv5_388_independent_verify.cpp`
- `results/raw/review/2026-11-06_0748_LSPV5_READONCE_RESOLUTION388.json`
- `results/raw/review/2026-11-06_0748_LSPV5_READONCE_RESOLUTION388_verification.json`
- `research/coordination/2026-11-06_0748_LSPV5_READONCE_BRIDGE388_HANDOFF.md`
- `research/agents/lspv-5/outbox/2026-11-06_0748_LSPV5_ROOT_INSERT388.tex`
