# TMR-1/052: A restriction-stable width-three compression census barrier

**2026-11-15 13:04 PST (America/Los_Angeles) | PNP Machine Model Lead | Track C / cross-track audit**

**Status:** PROVED/EXACT for the explicitly scoped finite-width representation theorem below, subject to independent mathematical peer review; COMPUTATIONAL for finite V8 verification; CONDITIONAL on pinned October 2026 #SAT machine results when discussing algorithmic implications. Arbitrary Circuit-SAT compression, NP-level circuit lower bounds, and P versus NP remain **OPEN**.

## 1. Candidate and precommitted falsifiers

**Candidate C052 (restriction-stable compression census).** Fix a width-at-most-three CNF target, retain the original n Boolean input variables as named variables, and allow an arbitrary number of existential auxiliary variables and clauses. Ask whether EVERY n-input, g-gate shared fan-in-two AND/OR/NOT circuit can have a function-preserving encoding H(x,z) on V=O(n polylog n) total variables, uniformly over ALL polynomial source gate-size ranges g<=n^D. Function-preserving means pointwise: for every x, C(x)=1 iff there exists z with H(x,z)=1. This is stronger than global equisatisfiability or equality of total #SAT counts. A per-input unique-extension encoding also satisfies it.

**Potential falsifiers:**
1. A legal SAT-equivalent compilation need not preserve any input's function. A result against pointwise existential projection must NOT be promoted to all Circuit-SAT algorithms or #count-equivalent compression.
2. Allowing an arbitrary remapping of the n original inputs or an external decoding algorithm changes the counted class. Preserve named input variables and account separately for any proposed remapping.
3. DISJ_k has grouped rank 2^k over every field but O(k) ordinary gates; a representation census must not infer hard SAT computation from rank or from the mere number of functions.
4. A compiler that outputs clauses with unbounded width is outside the fixed-width clause count. Width reduction may add auxiliary variables and must be charged.

## 2. Sources and scope

[1] R. R. Williams, *Thinking Algorithmically About Impossibility*, CSL 2015, Theorem 2.1, https://drops.dagstuhl.de/storage/00lipics/lipics-vol041-csl2015/LIPIcs.CSL.2015.14/LIPIcs.CSL.2015.14.pdf : all polynomial circuit-size ranges and a 2^n/n^10 SAT algorithm imply NEXP not subset P/poly, not an NP separation. Exact PDF theorem page 19 inspected.

[2] OpenAI, *The Exponential Time Hypothesis is False*, revised 2026-10-25, https://github.com/openai/math/tree/main/preprints/The-Exponential-Time-Hypothesis-is-False-October-25-2026 : claimed fixed-width exact-counting algorithm with polynomial input-size space and variable-dependent subexponential time. Sharper manuscript bound and narrower documented Lean scope must not be conflated. The existing TMR-1/050/051 pinned sources are retained; no new Lean build.

[3] Anthropic, `anthropics/formal-math`, commit `16a5ce41304fcdaea4e0be7c132e1c361dc26da5`, `eth/MainResults.lean` blob `1c62a550fa1e4cbec65bb7112f92ad67589afddc`: `MainTheorem` states a single exact counting machine with exponent proportional to min(km/sqrt(lg m), k^2 V lg lg V/sqrt(lg V)), subject to its n/m/NoDup/AllOccur guards. The definitions file explicitly contains NO proofs; separate formal proof artifacts were not rebuilt. Polynomial space does not follow from this definition alone.

[4] Project TMR-1/050: standard functional Tseitin conversion with V=n+g; TMR-1/051: class-target firewall; TMR-5/047: deletion of DEAD source gates and live-gate upper-bound threshold; TMR-4/051-052 and TMR-2/051: exact ordered BDD and field-dependent rank controls. This report provides a different, representation-only impossibility for **universal near-linear-variable pointwise existential projection** when source g is sufficiently large.

## 3. Theorem and proof

**Theorem C052-A (PROVED/EXACT, RESTRICTED; independent mathematical review OPEN).** There are absolute constants c>0 and g_0 such that for all sufficiently large n and all integers g with g>=g_0 n and log_2 g <= n-O(1), among the Boolean functions computable by shared fan-in-two AND/OR/NOT circuits with n named input variables and at most g live gates is a function f such that EVERY width-at-most-three CNF H(x,z) representing f by existential projection requires

```text
V(H) >= c*g^(1/3),
where f(x)=1 iff there exists z with H(x,z)=1, for every x.
```

In particular, for g=n^4 there are circuits with at most n^4 gates for which any such encoding needs V=Omega(n^(4/3)). Thus no universal projection-preserving all-polynomial-gate-size compiler with V=O(n*(log n)^a), for any fixed a, exists. This is an existential **representation** lower bound, not a SAT runtime lower bound.

**Proof.** Choose r=2^k the largest power of two no greater than g/8. For sufficiently large g, g/16<r<=g/8, k<=n and r>=8. For every subset S of {0,1}^k of cardinality r/2, define

```text
f_S(x_1,...,x_n)
 = [all of x_(k+1),...,x_n are 1] AND [first k bits belong to S].
```

The functions f_S are distinct, by setting suffix bits to one and evaluating each prefix. A shared binary trie of positive/negative prefixes realizes every chosen minterm. At most 2r prefix nodes require AND computation, at most k NOT gates can be shared across all chosen paths, at most r/2-1 OR gates combine selected leaves, and n-k additional AND gates enforce the suffix. Therefore the number of gates is at most 2r+k+(r/2-1)+(n-k) <= 3r+n <= g for g sufficiently larger than n. Prune unselected trie branches; every created gate can be made syntactically live. The construction uses the same n original inputs and a single output.

There are binom(r,r/2)>=2^r/(r+1) distinct f_S. For r>=8, their binary logarithm is at least r/2>g/32. The inequality follows from sum_j binom(r,j)=2^r and the middle binomial coefficient being maximal.

Now normalize any width-at-most-three CNF on V named variables: drop tautological clauses, repeated literals, repeated clauses, and ignore order within clauses. The possible distinct non-tautological clauses of sizes 0,1,2,3 number at most

```text
Q(V)=1+2V+4*binom(V,2)+8*binom(V,3) <=8 V^3.
```

This counts the optional empty clause. Hence there are at most 2^Q(V) normalized CNF Boolean formulas, independently of how many redundant input clauses the original file contains. For fixed n named original variables, each such H determines at most ONE projected function f_H(x)=exists_z H(x,z). If the family were all represented with at most V variables, 2^Q(V) must be at least binom(r,r/2). Consequently 8V^3 >=g/32, giving V>=(g/256)^(1/3) for at least one function (rounding constants are harmless). Taking g=n^4 gives Omega(n^(4/3)). QED.

**Theorem C052-B (restriction gate).** Any hypothetical compiler guaranteeing H(x,z) has at least one extension for exactly those fixed original inputs x accepted by C, even if H is produced using arbitrarily large preprocessing time, is subject to C052-A. The same holds for unique-extension / per-assignment parsimonious compilations. A compiler preserving ONLY the total number of satisfying input assignments or ONLY whether C has any satisfying input is **NOT** covered. The latter may map every satisfiable circuit to a constant YES formula and every unsatisfiable circuit to a constant NO formula, given unlimited (possibly exponential) construction work. This explicitly blocks any inference of SAT-algorithm hardness from this counting argument.

**General width w.** With w fixed, the clause inventory is at most sum_{j=0}^w 2^j binom(V,j)=O_w(V^w). The same family yields V=Omega_w(g^(1/w)). There is no uniform-in-w assertion; growing width can evade this particular barrier.

## 4. Algorithm-to-lower-bound implication ledger and precise missing ingredient

1. **KNOWN/PROVED restricted:** Standard functional Tseitin: n original inputs + l live gate records gives V=n+l and m<=3l+n+1. Compiler work is polynomial in source serialized length O((n+g)log(n+g)); shared gate IDs counted once. This preserves every fixed assignment, exactly one auxiliary extension, and total #SAT.
2. **PROVED/RESTRICTED new negative:** No replacement by **any** width-three, pointwise projection-preserving V=O(n polylog n) encoding can work for all n^4-gate circuits. This is true even if the encoding routine were computationally unbounded and even with arbitrarily many clauses.
3. **OPEN alternative:** A uniform *decision-equivalent* or *total-count-equivalent but not pointwise* compression to V=n polylog n could evade this census. Such an algorithm requires explicit construction, time, memory, encoded output length, recoverability as needed, and exact-count semantics. A native Circuit-SAT/#Circuit-SAT algorithm avoiding the CNF intermediate also evades the theorem.
4. **KNOWN class firewall:** If such a uniform native fast Circuit-SAT were established with Williams's savings over every fixed polynomial-size range, source theorem [1] yields a **NEXP** vs P/poly lower bound, not NP vs P/poly. Bathie-Williams has separate formula-class and E^NP target. Nothing here closes an NP hierarchy or proves P!=NP.
5. **Cross-track:** TMR-2/4 may use this as a necessary encoding audit, not as a dynamic cut-rank charge; TMR-3 must separately show a SAME deterministic machine satisfying BOTH strict DTISP coordinates for any time-space contradiction; TMR-5 should try a small SAT-equivalent-but-not-projection-preserving compiler to verify the scope firewall.

## 5. Same-realization resource ledger

| Object/action | Exact measure or upper-bound accounting | Status |
| --- | --- | --- |
| Source C | n named input bits; g<=n^D live shared binary gates, each written once; standard source encoding O((n+g)log(n+g)) bits | Constructed family |
| Minterm-trie circuit for S | r<=g/8, k=log2 r, <=3r+n live gates; every shared prefix and negation counted once | PROVED/EXACT |
| H(x,z) | V=n+|z| named bits, at most Q(V) nonredundant clauses of width<=3; source/output literal indices cost O(log V) bits each | Representation only |
| Compiler/generator | NONE supplied; could consume arbitrary work and storage | OPEN, no algorithmic time claim |
| Counting/decision after compiler | NONE supplied; cannot inherit #SAT runtime savings without a SAME-realization composed machine | OPEN |
| Native V8 audit | 10,544 assignment evaluations, 206 circuit distinctness checks, 206 gate-size checks, 509 integer clause-budget checks, zero failures. All one self-contained Node process, no seed; <30 sec | COMPUTATIONAL |
| DTISP forbidden rectangle | No constructed machine, no simultaneous time-space pair | NOT CLAIMED |

The lower bound concerns variable count in existential CNF representations and does NOT assert expensive SAT decision, high circuit complexity, space lower bounds, memory-access tariffs, or direct rank hardness. It is compatible with cheap Horn, equality, affine, DISJ, bounded-treewidth, padding and alternative circuit computations.

## 6. Mandatory four gates

| Gate | Status and reason |
| --- | --- |
| DISJ sanity | **PASS (restricted).** DISJ_k has 2^k grouped rank but O(k) gates and straightforward small 2-CNF. This theorem has SOME hard-to-encode g-size functions, not a universal SAT cost; DISJ remains a legal cheap input. |
| Relativization/algebrization/Natural Proofs | **PASS restricted; OPEN for unrestricted promotion.** The information-theoretic formula census is purely syntactic and would relativize as a representation fact, but it separates no P/NP oracle worlds. Any step to a P-vs-NP lower bound needs a separately proved nonrelativizing ingredient. No efficient constructive large hard-function property is inferred. |
| Simultaneous DTISP | **NOT APPLICABLE to census; OPEN for machine transfer.** This theorem compares Boolean representations, not a paid decider. There is no same T,S forbidden pair. |
| Configuration counting | **PASS consistency.** For a total deterministic read-only-input machine T<=2^O(s+log N), but this upper bound is not a work lower bound and is not used here. |

## 7. Exact computational evidence and provenance

Standalone executable: `experiments/tmr/tmr1_compression_census052.js` revision `TMR1_COMPCENSUS052_v1`; no random seed; standard Node/V8 BigInt and assert, no external libraries. Raw machine-readable output: `results/raw/tmr/2026-11-15_1304_TMR1_COMP_CENSUS052_V8_RAW.json`. Local executed source SHA-256: `09039aec0e22f7b587c18d4173aada092e2d52740a3bec7c6ad74741c584ef74`; raw SHA-256: `1bd845f322fccd383d08b70c21b61e8f58f6f5b83e0e5a2173d054655a7b12c3`. Small k=1,2,3 exhaustive half-subset families; k=4 deterministic first 128 half-subsets; each circuit is exhaustively evaluated on all 2^n inputs. BigInt budget rows n=2^8,...,2^40 do not enumerate exponentially large circuits. They are finite integer illustrations, not the asymptotic proof.

Repo root `proof1.txt` full (blob `06f7ebc8c2283304a0f5200b518c6e48fa41e343`), `proof2.txt` metadata-only blob `930c5eeddafce656717f28055a7a9a755f44737c`, `main.tex` metadata-only blob `6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34`, `AGENTS.md`, `CODEX.md`, skill, five TMR handoffs, issue #3 and relevant originals reviewed. Connector returned empty bodies for oversized proof2/main files. Local network DNS prevented repository clone; mandatory repository preflight/full test suite and native Lean builds were NOT run. No shared root edit, no tracker ownership change, no agent schedule changes. /341 remains FAIL for full logical UNSAT and /386 remains RESTRICTED.

**TRACKERS REVIEWED AT AVAILABLE CONTENT/METADATA; NO MATERIAL CHANGE.**

## 8. Next falsification / weakest lemma

Build an explicit uniform, time-and-space-charged **SAT-equivalence-only** compiler or native Circuit-SAT algorithm for LIVE g=n^4 gate sources with a 2^{n}/n^{10} worst-case bound in ORIGINAL n. It is permitted to lose pointwise input-function preservation and must count output wire records, discovery, any interpolation, exact arithmetic/coefficient bits, repetitions, and source/goal access. First test a deliberately trivial SAT-equivalence-only (but computationally expensive) oracle/truth-table compiler to illustrate why C052 does not preclude it. Only a fully uniform efficient realization can satisfy Williams's premise. A subsequent independent NP-level bridge remains OPEN.

**P versus NP remains OPEN.**
