# LSPV-3 GATE327: Paid source dominance, forward/reverse continuations, and equal-count acquisition barrier

**2026-11-02 03:24 PST.** Status: **PROVED/EXACT** elementary source-preorder theorem and a promise coNP-hardness **corollary** of existing LSPV-4 EQUALCOUNT331; **COMPUTATIONAL** exhaustive independently checked finite controls; external review pending. **P versus NP OPEN**.

## Exact target and obstruction

Only valid duplicate-free proper Döcker monotone 3-SAT-(2,2) **originals** qualify: three distinct same-sign literals per source clause and exactly two positive/two negative occurrences of every original variable. Malformed sources reject. A fan-in-two circuit C_F on the **original variables** evaluates F(x); checking any given x is not deciding the existential SAT bit. Derived residual circuits and Tseitin clauses are noncanonical.

A controller cannot assume a semantic-cofactor-equivalence oracle or cheapest representation for free. Prior F9 OBDD sizes, exponential bad-order widths and counts of syntactic states do not imply work necessary for arbitrary SAT decision.

**Four falsifiers.** (1) Source coverage dominance can give false semantic mergers: formally falsified, with zero violations in exhaustive finite controls. (2) Source coverage is a *complete* semantic dominance test: false, 200,390 finite F9 ordered pairs are semantically dominated but not source-certified. (3) Equal exact model counts plus identical unsigned clause-width summaries make exact semantic dominance easy: false unless P=NP by an existing LSPV-4 331 construction and the corollary below. (4) Every SAT decider must pay for exact dominance: invalid; correct solvers may use direct DPLL, bounded-interface DP, source matching, affine GE or other methods.

## Theorem A: Polynomial-checkable sufficient preorder for any valid canonical original

Fix a common assigned-variable domain S and coherent pins p,q on **exactly S**. Define f_p(y)=F(p,y) and f_q(y)=F(q,y) on the same remaining original-variable domain. Let B(S,p) be the source IDs of crossing clauses (partially assigned, partially free) already covered by a TRUE prefix literal. Mark DEAD if a fully assigned original clause is false.

If p is DEAD, then f_p is identically zero and f_p implies f_q. If neither state is DEAD and B(S,p) is a subset of B(S,q), then **for every identical suffix assignment y**,
```
             F(p,y) => F(q,y).
```
If both are DEAD, or both viable with identical B sets, the two Boolean continuation functions are exactly equivalent.

**Proof:** Every source clause wholly in S is true for viable pins. Clauses wholly outside S are unchanged. For each crossing clause whose ID is absent from B(S,p), its residual is exactly the OR of its original free literals, independent of the old pinned values. B(S,p) subset B(S,q) means q imposes no crossing-clause obligation that p does not also impose. Hence every completion satisfying p satisfies q. The symmetric case proves equivalence. This proof establishes source-authenticated sufficiency, not semantic completeness.

The source signature and a comparison can be acquired from original clauses and signed indices in polynomial work per encountered pair, conservatively O(m) source-clause scans and O(m)-bit set comparisons, with native index/head reads charged. A large collection of encountered states or failed comparisons can still cost exponentially much in total.

## Theorem B: Equal-count semantic dominance collapses to equality

For Boolean functions f,g on the *same* finite future-assignment domain, if #f=#g, then pointwise f=>g **if and only if** f=g. Proof: model-set inclusion with equal finite cardinalities is equality.

**Consequence (derived, not an independent new coNP-hardness reduction):** LSPV-4 EQUALCOUNT331 proved exact cofactor equality is coNP-hard, even for coherent original-name siblings with equal model counts, identical anonymous clause-width profiles, no empty/unit residual source clauses, and a common canonical source. By Theorem B, both directions of **exact semantic dominance** are likewise coNP-hard under this same promise. NO-instances have polynomial original-name continuation witnesses. The equality-of-counts promise is certified by construction, not supplied by a free #SAT oracle. This establishes a gate on *optional* exact semantic acquisition, not SAT-decision hardness.

The explicit existing canonical gadget is Z6 with positive clause supports 123,145,246,356 and four negative twins. It has 18 models. Cofactors for original x1=0 and x1=1 each have nine completions, four common, five in each directional difference, and anonymous clause-width profile (2,0,0,2,4). For arbitrary canonical G with disjoint variable names, the original F_G=G AND Z6 is canonical and the sibling cofactors are G(y) AND h_0(z), G(y) AND h_1(z). Both have 9*#SAT(G) models. Both dominate one another exactly when G is UNSAT, by the two fixed distinguishing Z6 suffix assignments. This is the verified LSPV-4 reduction, explicitly adopted rather than claimed new.

## New finite quantified audit: source-only preorder versus exact semantics

The producer enumerated all coherent pinned domains and **every ordered pair with an identical assigned domain**. Counts include self-pairs and DEAD profiles. Number of aligned pairs is exactly 5^n. Exact semantic truth tables are **OFFLINE** diagnostic controls, never free on-machine oracles.

| Measurement | Z6 | F9 |
|---|---:|---:|
| Total source satisfying assignments | 18 | 70 |
| Aligned ordered pairs | 15,625 | 1,953,125 |
| Exact semantic dominance | 9,913 | 1,350,418 |
| Sound source-certified dominance | 8,267 | 1,150,028 |
| Semantic dominance **missed** by source coverage | **1,646** | **200,390** |
| Exact semantic equality | 5,893 | 933,033 |
| Source-certifiable equality | 4,499 | 714,917 |
| Equal-count pair but distinct Boolean cofactor | **1,164** | **66,800** |
| Source-rule false positives | **0** | **0** |

Thus the cheap rule is sound but far from complete. These counts do not give necessary work for arbitrary deciders.

**Forward/reverse exact cofactor comparison.** F9 prefix levels: (1,2,4,8,15,18,16,11,4,2), total 81; reverse: (1,2,4,8,14,20,20,11,4,2), total 86. Z6 both orders have (1,2,4,7,9,4,2). This reproduces prior finite GATE322, without claiming a new minimum OBDD or acquisition bound. Clause-private fan-in-two AND/OR evaluators have 35 F9 gates and 23 Z6 gates in that declared architecture. Independent original-source and circuit evaluations matched all 512 F9 and 64 Z6 complete inputs.

**Same-original opposite-label certificates:** On the original F9, common pins (x2,x3,x6)=(0,0,1) yield one satisfying completion with x1=0 and **zero** with x1=1. All 32 coherent UNSAT-side completion leaves were separately checked against original indexed falsified clauses. Source UP-first DPLL found each in one node, with 70 and 34 literal inspections respectively, showing why expensive offline cofactor compilation is unnecessary for these decisions.

**Hostile checks:** 264 F9 and 112 Z6 S/U source clause-pair modes checked against direct enumeration, 6,656 source clause complement checks, five malformed source structures rejected, direct original input/circuit truth comparison, and deterministic UP-first DPLL. An independent no-Python-import Node verifier passed **4,952,095 assertion groups**. F15/U198/V198 were inherited and **not freshly replayed**. Offline logical 2-bit-clause-status XOR adjacent sums for F9 binary/Gray are 3964/3074 and for Z6 456/388. No native physical machine delta or lower bound is inferred.

## Fully charged recurrence and exact gap

For every actually visited source-indexed state s of uniform D,
```
T_D(s)=C_grammar + C_source/index/head + C_acquisition
       + C_failed/policy/switch + C_circuit/OBDD/GE/proof
       + C_cache/replay + C_guest(DELAY,COPY,RECOMP)
       + sum_{u in executedSucc(s)} (C_child/output/bit(s,u)+T_D(u)).
```
S_peak is the maximum combined simultaneous writable/index/ancestor/child/proof/cache/matrix/guest/output tape occupancy. For k explicitly held states, source-coverage pair tests cost at most O(k^2 m) source-bit work, with O(km) retained keys, apart from other live state. The **offline** census uses 4^n completion lookups, 5^n aligned comparisons and up to O(poly(N)6^n) bit operations with O(poly(N)2^n) peak bits. Neither 5^n comparisons nor 200,390 missed dominances is a lower bound on any SAT decider.

No uniform polynomial bound on aggregate acquired or executed states for **all** valid canonical originals is proved. Nor is an arbitrary-A hereditary power-short ARC contraction or a strict **SAME-MACHINE** numerical FLMV transfer. P=NP and P!=NP both remain **OPEN**.

## Provenance, literature and next test

Adopted prior project results: LSPV-1 DIRECTIONAL-COFACTOR-DOMINANCE320; LSPV-4 EQUALCOUNT-COFACTOR331; LSPV-3 GATE319/321/322/324/326 and LSPV-2 STS9-NEGATIVE-PATH331. **New in this run:** full aligned-domain quantitative sound-vs-complete source-dominance audit on two authenticated original sources and an explicit equal-count dominance promise corollary, independently checked with source/circuit and both-label controls. No claim of new unrestricted complexity hardness.

Literature reviewed: Döcker 2019 https://arxiv.org/abs/1912.08032; Böhler et al. 2002 https://arxiv.org/abs/cs/0202036; Darwiche and Marquis 2002 https://doi.org/10.1613/JAIR.989; Bryant 1986 https://doi.org/10.1109/TC.1986.1676819; Darmann and Döcker 2021 https://doi.org/10.1016/j.dam.2020.12.010. Project and github.com/openai code searches completed: OpenAI results were generic formal-math equivalence, not directly relevant SAT implementations. Search absence is not novelty evidence.

**Next falsifiable target:** build a source-certified but deliberately incomplete dominance + affine GF(2) + bounded-interface policy and seek a *provable polynomial bound on total executed acquisition, failed policies and descendants across every valid nonpaired connected canonical original*. The open quantifier cannot be replaced by an oracle selecting the best representation.

**Artifacts:** [compact executable](https://github.com/j15marti/pnp/blob/main/experiments/arc/lspv3_327/compact327_public.py); [raw summary](https://github.com/j15marti/pnp/blob/main/results/raw/arc/lspv3_327/summary327_public.json). Full producer, independent no-import verifier, UP-DPLL, offline XOR, original indexed falsification records and searches are in the per-run user-facing reproducibility ZIP.

**Root safety:** GitHub contents API for main.tex returned zero text despite a verified 1,203,511-byte original Git blob. Only authorized LSPV-3 marker edits are permitted, using authenticated complete Git blob readback; never overwrite from an empty response. No schedules/status/identities changed.
