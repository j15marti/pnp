# MAIN synthesis — SOURCE-REFERENCE-FLOOR15

Timestamp: 2026-10-20 12:48 KST  
Global status: **P versus NP remains OPEN.**  
Scope: only MCSP/MKTP magnification and arbitrary-decider ARC/FLMV contraction; COMPACT-HISTORY20 remains diagnostic.

## Recovery

Governance, continuity, COMPACT-HISTORY20, `main2.tex`–`main5.tex`, current GitHub work, and the shared Google Doc were read. No new complete :00/:12/:24/:36 scientific body appeared after SOURCE-READ-SUBORDINATION14; the only newer commits were independent review annotations. The fallback document still ends at REDTEAM29. Root `main.tex` blob `6a323280f201f8849450027993c48446756a4b91` still contains a literal truncation marker and was not modified.

## Ideas proposed before literature search

1. Put the original `N`-bit SAT source into each MMW query.
2. Keep the source as shared read-only state and pass only a pointer in each query.
3. Compile the source into a `poly(p)`-size circuit included in each query.
4. Replace the source by a short SAT-monochromatic semantic fiber, charging its construction.

## Primary-source check

MMW's one-pass construction takes an already-present truth table, reads it blockwise, and asks short `Sigma_3 SAT` merge queries tied to the compression threshold. It is a solver for search-MCSP/MKTP, not a construction of the missing SAT-derived target. <https://people.csail.mit.edu/rrw/MCSP-MKTP-stoc19.pdf>. CHMY's theorem uses a randomized one-way-input, one-work-tape machine and supplies no ordinary short-query source reference for this route. <https://doi.org/10.4230/LIPIcs.STACS.2021.23>. OPS's GapMCSP/GapMKTP results are nonuniform magnification statements rather than a uniform source compressor. <https://doi.org/10.4086/toc.2021.v017a011>. Ilango's source transport uses a random oracle; deterministic hash instantiation remains heuristic rather than the needed standard-model construction. <https://eccc.weizmann.ac.il/report/2023/165/>.

## The source-reference dichotomy

Let the SAT source have length `N`, the ordinary-MKTP target have length `M=N^(a+o(1))`, and `p=M^(1/k+o(1))=N^(a/k+o(1))`.

### Branch I: source-faithful queries

If an ordinary query description permits reconstruction of every `N`-bit source, its worst-case length is at least `N`: there are `2^N` sources but fewer than `2^N` binary descriptions of length below `N`. More generally, a circuit representation of size `s` has only `2^{O(s log(N+s))}` descriptions, so representing all sources requires `s=Omega(N/log N)`.

For any fixed degree `d`, a purported `p^d` source circuit has exponent `ad/k` in `N`. It can cover arbitrary source descriptions only while `k<=ad+o(1)`. Therefore a cofinal unbounded family of large fixed `k` cannot keep arbitrary source-faithful data inside `poly(p)` of fixed degree.

If every MMW merge query explicitly carries the source, then once `k>a`, its length is `N`, not `p`. With a fixed `P=NP` query solver using time `L^C` and space `L^D`, the conservative composition becomes

`t_full >= a+a/k+C`, `s_full >= D`.

For every integer `D>=1`, this misses the strict space target `1/2`, independently of `k`. The unknown solver exponent is no longer divided by `k`.

### Branch II: semantic source compression

Source faithfulness is not logically necessary. Given the SAT answer, the source can be mapped to one of two constant descriptions. Thus no information-theoretic lower bound applies to arbitrary SAT-preserving compression.

But constructing that constant description decides SAT. Any shorter non-injective replacement must prove that each selected fiber is SAT-monochromatic and must construct the appropriate fiber without already paying an uncontrolled full-source SAT computation. This is exactly the still-open `R_k` semantic interface, not something supplied by MMW.

### Branch III: shared-source queries

A pointer to a persistent read-only source makes query syntax short, but changes ordinary `Sigma_3 SAT` into a source-indexed/oracle problem. To use `P=NP`, this interface must be compiled back to an ordinary explicit input or accompanied by a same-machine theorem showing that shared-source access retains the short-query time/space exponents. No such theorem has been recovered.

## Formal conclusion

For the cofinal MMW absorption step, at least one of the following must be proved:

1. a standard-model source-indexed short-query solver with the same exponents;
2. a cofinal family of total target generators whose next-block predicate includes all necessary source information in `p^{O(1)}` bits with degree independent of `k`;
3. a charged, deterministic SAT-monochromatic semantic-fiber construction.

Without one of these, the formula `a(1+(C+1)/k)` applies only downstream of a target that is already present. It cannot be applied to the missing SAT-to-target construction.

This is a **proved interface trilemma**, not a lower bound for SAT. Branch II explicitly blocks any claim that all correct reductions must be injective.

## Reproducible audit

`experiments/review/2026-10-20_source_reference_floor_audit.py` checks:

- every fixed/variable-length binary encoding floor for `N<=256`;
- the exact `k<=ad` coverage boundary for four target exponents, `d<=32`, and `k<=2048`;
- absorption of all `C,D<=64` by genuine `p`-length queries;
- zero FLMV-box successes when every query carries the full source;
- the fact that every fixed positive source-contamination exponent can defeat unknown-exponent absorption.

## Proof DAG

| Arrow | Status | Exact boundary |
|---|---|---|
| MMW one-pass short-query streamer | ESTABLISHED | Assumes truth-table target already present |
| CHMY one-tape threshold result | ESTABLISHED, restricted model | No ordinary source reference |
| OPS GapMCSP/GapMKTP magnification | ESTABLISHED, nonuniform models | No `R_k` constructor |
| Ilango random-oracle reduction | ESTABLISHED relative to random oracle | Standard deterministic replacement OPEN |
| Cofinal short-query exponent absorption | PROVED, conditional interface | Valid only when queries really have `p^{O(1)}` length |
| Source-reference trilemma above | PROVED interface theorem | Semantic-fiber branch remains possible |
| SAT -> deterministic total `R_k` | OPEN | Now requires a source-reference solution |
| Ordinary total MKTP without side table/replay | OPEN | Same-machine output and workspace |
| All-input hereditary ARC successor | OPEN | Separate second route |
| Matched FLMV contradiction | CONDITIONAL | Requires either route to close |
| Compact shared witness `exists W forall i` | OPEN | Small `W` does not remove source/program description costs |
| Treating a source pointer as an ordinary short query | RETIRED | Unproved model substitution |

## Role handoff

- **:00 MCSP:** produce a next-target-block predicate with ordinary encoded length `p^{O(1)}` and degree independent of `k`, or identify exactly where the SAT source enters.
- **:12 Universal Solver:** test whether shared read-only source access can be compiled to ordinary `Sigma_3 SAT` without restoring `N`-length queries or `N^(1/2)` workspace.
- **:24 ARC:** apply the same source-reference audit to child descriptors; a pointer to the parent is not a smaller ordinary input.
- **:36 Red team:** find opposite-label SAT instances colliding under any proposed short source map, or verify its fibers are source-checkably monochromatic.
- **:48 Synthesis:** do not use the `C/k` absorption until the source-reference interface is explicit.

Strongest falsifier: a concrete ordinary, total, source-checkable next-block predicate of length `p^{O(1)}` for cofinally many fixed `k`, with construction and replay costs within the prior budgets. None is known. **P versus NP remains OPEN.**
