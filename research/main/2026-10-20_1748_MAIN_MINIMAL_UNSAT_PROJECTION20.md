# MINIMAL-UNSAT-PROJECTION20 — semantic-fiber firewall for both active routes

**Date:** 2026-10-20 17:48 Asia/Seoul  
**Scope:** exactly two active directions: MCSP/MKTP hardness magnification and arbitrary-SAT-decider ARC contraction into a matched FLMV endpoint. COMPACT-HISTORY20 remains supporting-only.  
**Status:** **P versus NP remains OPEN.**

## 1. Recovered state

This run read the governing portfolio, continuity protocol, COMPACT-HISTORY20 addendum, current `main.tex` and `main2.tex`--`main5.tex`, newest GitHub commits, and the shared Google Docs fallback handoff.

New peer results after MMW-QUERY-ABSORPTION19:

* **MCSP-SPARSE-TEMPLATE-KT-FIREWALL1 (:00):** an efficiently indexed template plus `polylog(M)` explicitly listed exceptions has ordinary KT `polylog(M)` for every source. One-bit tags, sparse hash patches, and sparse affine/parity corrections therefore put both SAT labels on the low-KT side. Report commit `6af039e...`; raw audit reports 2,702,404 assertions and zero failures.
* **ARC-SIGN-COLOR-GLUE4 (:24):** Horn/dual-Horn sign projections of every proper 3-CNF are separately satisfiable, even when their conjunction is UNSAT. Its square-root child packing is resource-correct but semantically incorrect. Full details were recovered from the shared Doc; minimal code and raw counts are on GitHub (`7eb41b3...`, `5f1a23b...`), with 1,545 checks and zero failures.
* No newer :12 body than UNIVERSAL-UNDECIDABLE-CERT3 and no accessible 17:36 body appeared in the GitHub/Doc readback as of this run. This is an accessibility statement, not a claim that those roles did no work.

Root `main.tex` has newer independent-review annotations and was not modified.

## 2. Ideas proposed before primary-source search

1. **Minimal-UNSAT barrier:** every strict clause-subformula of a clause-minimal UNSAT formula is SAT, so status-only projection children produce an all-YES transcript.
2. **Matched-pair strengthening:** build SAT and UNSAT proper 3-CNFs with identical variable and clause counts whose complete one-clause-deletion status vectors coincide.
3. **Boundary-witness repair:** attach separator assignments to children and test whether their consistency information fits the square-root space and `241/200` time budgets.
4. **Cross-track semantic-fiber criterion:** sparse MKTP patches and ARC status projections fail for the same reason—opposite source labels land in one target semantic fiber.

## 3. Primary-source model check

* Minimal unsatisfiability means UNSAT with every one-clause deletion SAT; this standard notion is the exact property used below. See Hoory--Szeider, *Computing Unsatisfiable k-SAT Instances with Few Occurrences per Variable*: <https://www.satisfiability.org/SAT04/programme/43.pdf>.
* MMW Theorem 4.2 supplies a one-pass MKTP streamer after the target exists, using `O(p)` ordinary `Sigma_3 SAT` queries; it does not construct the SAT-derived target: <https://people.csail.mit.edu/rrw/MCSP-MKTP-stoc19.pdf>.
* CHMY's lower bounds concern a randomized one-tape machine with an additional one-way read-only input, not FLMV random access: <https://doi.org/10.4230/LIPIcs.STACS.2021.23>.
* OPS concerns nonuniform Gap-MKtP/Gap-MCSP magnification, not the missing total standard-model `R_k`: <https://theoryofcomputing.org/articles/v017a011/>.
* Ilango's SAT/MCSP transport remains random-oracle-relative: <https://eccc.weizmann.ac.il/report/2023/165/>.
* FLMV's endpoint is deterministic random-access SAT with simultaneous time and space in one realization: <https://lance.fortnow.com/papers/files/tst.pdf>.
* Levin search and Hutter's fastest-program construction do not supply the missing semantic reduction; Hutter ranges over provably correct programs. Blum speedup/correctness-enumeration issues therefore remain diagnostic, not a construction.
* Easy-witness results are conditional complexity tools and do not create the project-specific shared witness `exists W forall i`.

## 4. Built theorem: matched minimal-UNSAT projection collision

### Construction

For a literal `l` and fresh variables `a,b`, define the four-clause proper-3CNF unit block

`U(l;a,b) = AND_{s,t in {+1,-1}} (l OR s*a OR t*b)`.

It is equivalent to `l`. For literals `-x_i,x_{i+1}` and fresh `c_i`, define

`P_i = (-x_i OR x_{i+1} OR c_i) AND (-x_i OR x_{i+1} OR -c_i)`,

equivalent to the implication `x_i -> x_{i+1}`.

For `m>=2`, let

`F_m = U(x_1;a_0,b_0) AND P_1 AND ... AND P_{m-1} AND U(-x_m;a_m,b_m)`.

This has `2m+6` distinct proper clauses on `2m+3` variables.

Create `G_m` by replacing the end clause

`(-x_m OR a_m OR b_m)`

with

`(-x_m OR a_m OR x_1)`.

The two formulas have the same numbers of clauses and variables.

### Theorem

For every `m>=2`:

1. `F_m` is minimally unsatisfiable.
2. `G_m` is satisfiable.
3. Every strict clause-subformula of either `F_m` or `G_m` is satisfiable.
4. Consequently, the complete vectors of SAT answers to all one-clause deletions are identical and all YES, although `SAT(F_m)=0` and `SAT(G_m)=1`.

### Proof

The first unit block forces `x_1=1`. Every `P_i` forces `x_i -> x_{i+1}`, hence all `x_i=1`. The last unit block forces `x_m=0`; therefore `F_m` is UNSAT.

Remove a clause from the first unit block. Set all `x_i=0`; the three remaining block clauses admit the unique auxiliary setting that would have falsified the removed clause. Remove one of the two clauses in `P_i`. Set `x_1,...,x_i=1` and `x_{i+1},...,x_m=0`, choosing `c_i` to satisfy the remaining padded implication clause. Remove a clause from the final unit block. Set every `x_i=1` and choose `a_m,b_m` to satisfy the other three clauses. Thus every one-clause deletion of `F_m` is SAT, and every smaller proper subformula is SAT by monotonicity.

For `G_m`, set all `x_i=1`, `a_m=b_m=0`, and choose the other unit auxiliaries consistently. The replacement clause is satisfied by `x_1`; the three remaining end clauses are satisfied by the chosen auxiliaries. Hence `G_m` is SAT, and all its subformulas are SAT.

Therefore both deletion transcripts are the same all-YES vector. QED.

### ARC corollary (restricted but exact)

Consider an ARC successor whose only semantic calls are SAT queries on strict clause-subformulas of the parent and whose final gluing rule receives only those Boolean statuses plus source-independent size metadata. It cannot be correct on both `F_m` and `G_m`.

More generally, on `F_m`, **no number of strict clause-subformula SAT calls yields a negative answer**. A correct arbitrary-input successor must therefore do at least one of the following:

* query a child containing the full minimal core;
* add new coupling/boundary constraints whose correctness is proved;
* carry compatible witness/boundary information rather than statuses alone; or
* perform source-dependent semantic work outside the child calls.

The last option must be charged and cannot simply be called “selection.” The theorem does not exclude a sophisticated source-dependent compiler and is not an unrestricted SAT lower bound.

## 5. Cross-track synthesis

The new MCSP and ARC no-gos are instances of one necessary condition:

> **Semantic-fiber separation.** A correct reduction must map every opposite-label source pair to observables with opposite target predicate values. Syntactic target diversity is irrelevant if the target predicate is constant on the image.

* Sparse-template MKTP: every target is low KT, so both source labels map to MKTP-YES.
* Strict-subformula ARC: every child status is SAT-YES on the minimally-UNSAT family, so the observable status transcript carries no UNSAT evidence.

This does not itself construct the missing maps. It supplies a mandatory pre-resource audit: prove opposite-label semantic separation before optimizing time, space, caching, or query length.

## 6. Proof DAG v20

| Arrow/result | Status | Qualification |
|---|---|---|
| MMW short ordinary queries and cofinal exponent absorption | **ESTABLISHED / CONDITIONAL COMPOSITION** | Load-bearing only after a total ordinary target exists |
| Sparse-template ordinary-KT ceiling | **PROVED, RESTRICTED** | Retires one-bit tags, sparse hash edits, and polylog exception dictionaries |
| Matched minimal-UNSAT deletion-transcript collision | **PROVED, RESTRICTED** | Retires status-only strict-subformula gluing |
| Finite audit, 4,812 categorized checks | **COMPUTATIONAL** | Exhaustive SAT/minimality for `m=2,...,7`; shape checks to `m=1000`; zero failures |
| Deterministic total both-label SAT -> ordinary MKTP `R_k` | **OPEN — MCSP weakest arrow** | Must be dense/semantically separating without a short ordinary index program |
| Arbitrary-decider all-input hereditary ARC successor | **OPEN — ARC weakest arrow** | Must add correct coupling or compatible boundary information and meet same-machine budgets |
| ARC recurrence -> matched FLMV forbidden point | **CONDITIONAL** | Resource windows do not repair semantic collisions |
| Compact witness for the specified diagonal family | **OPEN diagnostic** | Unique/long histories can fast-forward; generic EXP tableaux have no universal fixed-poly guarantee under P=NP |
| Sparse tags or strict-subformula status vectors as separators | **FALSIFIED / RETIRED** | Target predicate constant on the tested image |

## 7. Allocation and strongest falsifier

* **:00 MCSP:** test dense/proof-of-work targets for a short ordinary indexed description. Before resource analysis, exhibit one explicit SAT/UNSAT source pair whose outputs provably fall on opposite MKTP sides.
* **:12 Universal Solver:** treat exponent `C` as already cofinally absorbable for MMW. Audit ordinary query encodings and reject source pointers or sparse descriptors; do not use correctness certification as the semantic bridge.
* **:24 ARC:** construct a mixed child carrying separator assignments or coupling clauses. Test first on `F_m`; if every child is a strict source subformula, the attempt is already falsified.
* **:36 Red team:** attack any proposed coupling rule on `F_m/G_m`, minimally-UNSAT cycles, and shared-boundary inconsistency. Charge selection if it encodes source semantics.
* **:48 Synthesis:** require a semantic-fiber certificate before accepting further resource-only improvements.

**Strongest falsifier:** if a proposed child family gives the same SAT-status transcript on `F_m` and `G_m`, or a proposed MKTP family has one short ordinary indexed decoder covering both labels, it cannot be load-bearing regardless of its resource ledger.

## 8. Reproducibility

The accompanying standard-library checker exhaustively verifies UNSAT/SAT, every one-clause deletion, proper-clause shape, and transcript equality for `m=2,...,7`, and checks formula shape through `m=1000`. It records 4,812 categorized checks and zero failures. The asymptotic theorem is proved symbolically above; finite tests are controls only.

**Conclusion:** the latest peers produced two complementary semantic-fiber no-gos. They eliminate sparse target tagging and status-only subformula gluing, but do not supply either missing constructive arrow. **P versus NP remains OPEN.**
