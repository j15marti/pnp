# EXPANDER-RESIDUAL-SIZE82 — exact CNF-size obstruction to logarithmic separator acquisition

**Role:** :48 synthesis  
**Timestamp:** 2026-10-23 06:48 KST  
**Global status:** P versus NP OPEN; P versus RP OPEN.

## Repairs fixed before source review

1. Choose separators in the actual clause-variable incidence graph.
2. Choose separators after faithful Circuit-SAT/Tseitin expansion and charge every clause removed by an assignment.
3. Permit deterministic semantic preprocessing before separator search, but charge its complete source access and require exact both-label behavior.

Advance falsifier: if a bounded-occurrence expanding incidence graph loses only (O(k)) vertices when (k) cut variables are assigned, an (O(\log N)) cut cannot create (N^\beta)-size residuals.

## Sources actually reviewed

1. `research/main/2026-10-22_1348_MAIN_EQUALITY_LOCALIZATION_MINOR_BARRIER65.md`;
2. `research/main/2026-10-23_0548_MAIN_RECURSIVE_CONE_FIXED_POINT81.md` and the independent 06:13 KST review at commit `1facc67`.

Barrier65 proves minor preservation for exact occurrence localization and a wall/treewidth obstruction. Fixed-point81 proves that, if hereditary separators are supplied, their cumulative incidence already equals the FLMV call fixed point. The result below strengthens the hostile control by placing variable assignment and residual encoded size in one explicit inequality.

## Model

Let (F) be an explicitly encoded monotone 3-CNF. Its clause-variable incidence graph (H(F)) has one vertex for each source variable and clause, and an edge for each literal occurrence.

Assume:

- (H(F)) has (n) incidence vertices;
- maximum variable occurrence and graph degree are at most the constant (\Delta);
- for every (S\subseteq V(H)) with (|S|\le n/2),
  [
  |N_H(S)\setminus S|\ge h|S|
  ]
  for a constant (h>0).

The ordinary explicit encoding length is (N=\Theta(n\log n)). Constant-degree bipartite expander families provide the structural hypothesis. The theorem is stated for any family satisfying it.

## Lemma 82A — assignments delete only boundedly many incidence vertices

Assign a set (X) of (k) source variables **true** and simplify the monotone CNF. Each assigned variable vertex is removed, and only its incident clauses can be satisfied and deleted. Hence the set (R) of removed incidence vertices obeys
[
|R|\le(1+\Delta)k.
]

Clauses not incident to (X) are unchanged. This all-true branch is sufficient to refute a promise that **every** cut assignment yields only small residual components.

**Status: ESTABLISHED.**

## Lemma 82B — expander deletion leaves a giant component

Let (H) be an (h)-vertex-expander on (n) vertices in the sense above. If
[
|R|<\frac{hn}{4+h},
]
then (H-R) has a connected component containing more than (n/2) vertices.

**Proof.** Suppose every component of (H-R) has size at most (n/2). One can select a union (S) of components satisfying
[
\frac{n-|R|}{4}\le |S|\le\frac n2.
]
Indeed, use a component already in that interval, or greedily combine smaller components until reaching the lower endpoint; the final union remains below (n/2). No edge of (H-R) leaves (S), so every external neighbor of (S) lies in (R). Expansion gives
[
|R|\ge h|S|\ge\frac{h(n-|R|)}4,
]
equivalently (|R|\ge hn/(4+h)), a contradiction. □

**Status: ESTABLISHED graph lemma.**

## Corollary 82C — logarithmic cutsets fail at the ARC size measure

Combining Lemmas 82A and 82B, every cutset satisfying
[
k<\frac{hn}{(4+h)(1+\Delta)}
]
has an all-true branch whose simplified incidence graph contains more than (n/2) vertices.

Because a connected bounded-degree residual with (\Omega(n)) vertices has (\Omega(n)) incidences, its ordinary explicit CNF encoding has length
[
\Omega(n\log n)=\Omega(N).
]
Therefore it exceeds (N^{\beta+o(1)}) for every fixed (\beta<1).

In particular, the separator allowance from SEPARATOR-CONE-COVER80,
[
k\le0.1\log_2N+o(\log N),
]
is asymptotically far below the (\Omega(n)=\Omega(N/\log N)) variables needed to force all residual components below half size on this family.

**Status: ESTABLISHED for syntax-local variable assignment on the stated expander family.**

## Exact scope and hostile semantic control

The formulas used above are monotone and hence have an easy deterministic SAT decision: assign every variable true. Thus:

- this is **not** a SAT runtime lower bound;
- it is **not** an arbitrary-decider ARC obstruction;
- it is **not** an MKTP HIGH construction;
- it is **not** an RP separation.

It falsifies only a universal **syntax-local** claim that (O(\log N)) source-variable assignment must decompose every explicit CNF into (N^\beta)-size components.

A semantic compiler may inspect the source and accept this easy family immediately. Such a repair remains OPEN for arbitrary SAT and must charge that full source inspection. This easy bypass is intentional: it distinguishes structural decomposition failure from language hardness.

## Tseitin, equality and Circuit-SAT audit

The input is already ordinary 3-CNF, so no Tseitin encoding is needed to obtain the obstruction. Exact occurrence splitting plus connected equality gadgets cannot remove it generically: Barrier65 shows that the original incidence graph survives as a minor. Merely dropping equality changes the witness relation, as CLAUSE-COHERENCE20 demonstrates.

Circuit gate sharing can recognize the monotone bypass, but that is a semantic source inspection, not evidence that arbitrary Circuit-SAT has a small separator. Independent clause-occurrence witnesses remain invalid.

**RETIRED:** syntax-preserving occurrence localization or logarithmic variable separators as a universal ARC acquisition method.

**OPEN:** nonlocal, solver-dependent semantic contraction with source-checkable exact labels and fully charged acquisition.

## MKTP audit

These expander formulas can themselves be generated by a short uniform expander program. Their structural largeness therefore points toward ordinary-KT LOW, not HIGH. No label-sensitive ordinary-MKTP threshold follows from expansion or residual size.

**SAT-to-ordinary-MKTP status: OPEN.**

## P/RP audit

The monotone family lies in P and cannot witness an RP language outside P. Hashes of its source do not create hardness. SOURCE-CHANNEL21 must count any direct scan that recognizes monotonicity or reconstructs the expander. PARITY-FIBERS45 remains a separate restricted derandomization theorem; neither result extends to every RP verifier.

**P=RP and P!=RP remain OPEN.**

## Finite audit

The executable audit generated connected cubic bipartite clause-variable graphs with 128 to 512 incidence vertices. For 120,000 seeded trials, it assigned up to four variables true, removed the assigned variables and incident clauses, and checked:

- at most (4k=(1+\Delta)k) incidence vertices were removed;
- the largest residual component remained larger than half the original incidence graph.

Result: **240,000 assertions, zero failures**. The minimum observed largest-component fraction was (0.867188). These random finite graphs validate the deletion implementation and provide a hostile control only; the asymptotic theorem uses the explicit expansion hypothesis.

## Route ledger and next tests

- **:00 SAT-to-ordinary-MKTP — OPEN.** Upper-bound ordinary KT of the uniform expander-family generator, including indexed output time; structural expansion must not be misclassified as HIGH.
- **:12 P!=RP — OPEN.** Replace the easy monotone family by a source-faithful paired YES/NO control and record every deterministic source bypass before applying SOURCE-CHANNEL21.
- **:24 ARC/FLMV — local acquisition RETIRED; semantic transformer OPEN.** Run one proposed semantic contractor on this family and charge the monotonicity/source scan that permits the bypass.
- **:36 P=RP — OPEN.** Test whether the PARITY-FIBERS45 affine-operand certificate survives a verifier encoding of the same expander source and an equivalent gate-reordered encoding.
- **:48 synthesis — Lemmas 82A-C ESTABLISHED restricted.** Construct a paired bounded-occurrence expander YES/NO family with no constant-size UNSAT core or trivial polarity signature; failure would delimit this hostile control to easy sources.

## Bottom line

A logarithmic separator cannot even structurally shrink every bounded-occurrence explicit CNF: on an expanding incidence graph, the all-true cut branch retains an (\Omega(N))-length connected residual unless (\Omega(N/\log N)) variables are assigned. This precisely retires syntax-local separator acquisition at the ARC size measure. It leaves the intended load-bearing target unchanged: an all-input, hereditary, fully charged **semantic** contraction. P versus NP and P versus RP remain OPEN.
