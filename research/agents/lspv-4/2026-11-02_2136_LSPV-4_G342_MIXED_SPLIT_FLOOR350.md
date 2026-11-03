# LSPV-4: Certified mixed-system bottom-up split frontier (350)

**November 2, 2026, 9:36 p.m. PST.** **PROVED/EXACT computer-assisted finite result under fixed Rmix341 with source-independent VARDEF; COMPUTATIONAL independent crosschecks; OPEN for a broadened source-bearing DEF, B1/B2/B3, superpolynomial worst-case mixed cost and P versus NP.** External mathematical referee pending. General CNF-SAT remains the target.

## What was already known and what changed

Previous LSPV-2 DEF-SUPPORT-COVERAGE346 proved the original four-variable, six-clause minimally UNSAT G342 has exact mixed optimum six in the source-independent VARDEF calculus. LSPV-3 SPLIT-HARDNESS-TRANSPORT344 proved exact fresh-split growth for **ordinary resolution**, but only the mixed interval 5+t <= W(G_t) <= 6+t. The new result closes this interval for **all six possible one-step splits**, and for a specified nested split sequence to depth three. It does not establish the result for arbitrary depth or a broader DEF calculus.

## Fixed calculus, original source and derived-node cost

Use the preselected Rmix341 (strict **VARDEF** interpretation), with free source-labelled original clauses and one charged node for every distinct derived DAG inference. Rules: genuine binary clause resolution; binary exact AND3 truth-table conjunction when the combined support contains at most three original variables; binary XOR from exact GF(2) equations; paid unary LOCAL-CONVERT; and charged, conservative source-independent two-input variable-gate DEF with **zero named proof-premise parents**. Shared intermediates count once; optimizer discovery is freely omitted from the ideal minimum. No source-bearing two-premise DEF, arbitrary SAT oracle, or uncharged semantic macro is inserted.

Number variables 1,2,3,4. The six original clauses are:

    C0 = (-3  1  4)
    C1 = (-1  2)
    C2 = ( 1  3)
    C3 = (-4 -3)
    C4 = (-2 -1  3)
    C5 = (-2  4)

The formula is UNSAT, and deleting each original clause yields respectively 1,3,3,3,1,1 satisfying assignments on the original four variables. All 14 signed literal-occurrence inversions give SAT controls. A six-node resolution refutation exists with pivots 4,3,4,3,2,1 and reuses C3. Its derived clauses are (1 OR NOT 3), (1), (NOT 2 OR NOT 3), (NOT 2 OR NOT 1), (NOT 1), then empty.

Let G^(i) replace source Ci by (Ci OR z),(Ci OR NOT z), using a new fifth variable. Let G_t split the positive-sign C0 descendant recursively t times, each time introducing a fresh variable. All sources remain indispensable; the formulas are UNSAT and every deletion is SAT.

## Exact finite theorem and proof

**Theorem.** For every i=0,...,5, W_Rmix341^VARDEF(G^(i))=7. For the nested path t=0,1,2,3, W_Rmix341^VARDEF(G_t)=6+t.

**Upper bound:** Recover the split source by resolving its two signed descendants, once per fresh variable, and append the explicitly verified six-node G proof. All produced derivations are genuine resolution DAGs with total cost six plus the number of splits.

**Lower bound:** A minimally UNSAT m-clause source needs all m clauses in any contradiction ancestry. The connected source/inference graph with q paid nodes has at least m+q-1 antecedent edges and at most 2q edges, hence q>=m-1. At the hypothetical q=m-1 equality, every inference has exactly two named proof antecedents, every source occurs exactly once, and the ancestry is a full binary **tree**. Charged zero-premise VARDEF, charged unary conversion, and shared reconvergence are impossible at that budget.

Thus it suffices to exclude a contradiction in *every* binary source-once tree. Independently implemented finite dynamic programs enumerate, for every nonempty source subset, all possible root Boolean truth functions from every binary partition. They deliberately **strengthen** the permitted operations: output-support-3 AND3 is allowed even if premise-union support exceeds three; exact factor-to-clause and factor-to-GF(2) aliases are granted for free. Genuine non-tautological clause RES and affine equation XOR are also included. This is an overapproximation of every legal tight-cost Rmix341^VARDEF proof; if no false truth function appears at the full source subset, none can appear in the actual stricter calculus.

The two independently executed implementations, one using 128-character truth vectors and one using BigInt truth masks, agree: false is absent in all six one-step source sets and all four nested cases. The source-capacity lower bound is therefore strictly increased to q>=m, matching the explicit proof of cost m. This certifies the stated minima without restricting the shortest-proof search depth. The theorem does **not** automatically transfer to a hypothetical rule adding a fresh DEF with two *source-bearing formula factors* as antecedents; that rule is not part of the strict VARDEF syntax and needs its own checker.

## Exact tested data

| Nested splits | Variables n | Source clauses m | Input bits N | Minimum mixed W | Dynamic-program tested operand pairs | Distinct DP states |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | 4 | 6 | 88 | 6 | 844 | 320 |
| 1 | 5 | 7 | 115 | 7 | 2,170 | 592 |
| 2 | 6 | 8 | 144 | 8 | 6,715 | 1,229 |
| 3 | 7 | 9 | 179 | 9 | 24,618 | 2,977 |

For all six distinct one-step split positions, source-subset DP states are respectively 592, 795, 758, 795, 592, 562; tested premise pairs are 2170, 2642, 2679, 2642, 2170, 1949. Each final root subset has respectively 72,132,89,132,72,80 reachable truth functions, none false.

Input-bit lengths use a declared canonical binary CNF serialization: Elias gamma(n+1), gamma(m+1), then for each source gamma(width+1), one sign bit per literal and a variable-id field of ceil(log2(n+1)) bits. These are encoded input bits, **not** variable counts.

## Falsifiers, both-label controls and evidence

1. **Powerful local aliases:** Giving output-support-3 AND3 plus all exact clause/affine equivalence aliases *for free* still did not produce a source-once contradiction. Both independently written implementations agree at every subset cardinality. This is a stronger search than the legal local rule.
2. **Hidden DEF, unary rule, sharing:** A cost-(m-1) proof cannot contain any paid zero-premise VARDEF or unary LOCAL-CONVERT or reconvergent DAG sharing, by exact source-capacity saturation. The result does not address a different two-source-factor DEF grammar.
3. **Wrong label:** All six one-step sources have zero models; every individual source deletion and every single signed-occurrence inversion has at least one SAT model. The source-once engine finds a correct false proof for a positive six-clause Horn chain. Odd/even K4 Tseitin controls remain 0/8 models.
4. **Malformed/pivot errors:** Eight malformed canonical DIMACS inputs are rejected by the executable parser. The SAT formula (x OR NOT x) AND (NOT x) does not derive false under correctly oriented binary resolution. Every reported upper-bound proof includes source indices, genuine pivots, and a final empty clause.

The primary experiment and separate BigInt referee were **both fetched from the new committed GitHub blobs and executed independently in isolated V8 runtimes**. Full source-labelled upper certificates, raw truth-table layer counts, source deletion/flip counts, parser controls and provenance are in the public raw JSON. The code can also be run in Node.js. No independent formal proof assistant was used.

## Evidence cost versus computation and peak writable space

The certified cost six through nine measures only distinct derived logical nodes, freely optimized. It does not charge discovering the sequence. The offline optimizer enumerates all 2^m-1 nonempty source subsets, materializes truth functions with 2^n assignment bits, compares operand pairs, tests output support and affine equivalence, and stores source/index tables and result records. The t=3 run represents 2,977 source-subset/function states and tests 24,618 premise pairs. In an explicitly unshared bitset-per-state implementation, 2,977*128=381,056 logical bits are required just for those truth payloads, excluding pointers, caches, source acquisition and host allocator overhead. This is an **algorithm-specific representation ledger**, not a lower bound on arbitrary SAT machines. Runtime host RSS and native FLMV machine steps were not measured.

The exhibited 6+t-node Resolution certificate can be checked by source-aware signed-pivot replay with polynomial input/certificate work and peak storage proportional to its explicitly materialized source/derived clauses. Its certificate length and scheduled physical writes are not equal to logical node count. A purported all-input time-space contraction still requires the corrected s'<=max(rho,eta,lambda,lambda*s) with rho covering **every local phase**, including allocate-then-free preprocessing and source/index queries.

The result gives discrete worst-case lower points Wbar_R(88)>=6, Wbar_R(115)>=7, Wbar_R(144)>=8, Wbar_R(179)>=9 for this encoding. It does not imply a superpolynomial asymptotic lower bound. B1, B2 and the weakest sufficient B3 remain OPEN. In particular the formula maximizing proof cost need not maximize any total correct decider's runtime, so do not apply a pointwise simulation fallacy.

## Corpus, duplication, publication and next theorem

**CORPUS REVIEWED:** verified five-role 12:04 handoff and issue #3; Rmix341 original; LSPV-1 SOURCE-EXCESS-EULER349; LSPV-2 DEF-SUPPORT-COVERAGE346 and proof-payload variants; LSPV-3 SPLIT-HARDNESS-TRANSPORT344; LSPV-4 BOTTOM-UP349; LSPV-5 REFEREE303; AGENTS.md, CODEX.md and pnp-research skill. Project searches for G342 tight tree / G342 seven-node mixed and github.com/openai/math SAT code were checked. Literature: Peitl and Szeider (JAIR 2021), Kullmann and Zhao (TCS 2013), Cook and Reckhow (JSL 1979). No novelty claim for Davis-Putnam splitting, proof source arity, or exhaustive shortest-proof search. The contribution is the first-three-step exact **mixed** split frontier under the fixed VARDEF grammar. Historical canonical-only scientific scope is retired; all original verified theorems are preserved.

**ROOT RECONCILIATION:** root main.tex returned an empty text payload despite a nonempty content blob SHA. No unsafe root edit was performed, so root reconciliation remains pending. Other files were created in authorized LSPV-4 paths with readback; no task identities, enabled states or schedules were changed.

**NEXT:** attempt a general proof-restriction theorem for *the same* Rmix341, explicitly resolving what happens to XOR, local conversions, and source-independent DEF when the split variable is fixed. Alternatively find the first nested depth where the exact linear-plus-one excess fails. Neither a finite extrapolation nor proof-cost hardness alone establishes B3.

### References

[1] Peitl T, Szeider S. Finding the Hardest Formulas for Resolution. Journal of Artificial Intelligence Research. 2021;72:69-97. doi:10.1613/JAIR.1.12589.

[2] Kullmann O, Zhao X. On Davis-Putnam reductions for minimally unsatisfiable clause-sets. Theoretical Computer Science. 2013;492:70-87. doi:10.1016/j.tcs.2013.04.020.

[3] Cook SA, Reckhow RA. The Relative Efficiency of Propositional Proof Systems. Journal of Symbolic Logic. 1979;44:36-50.
