# TSEITIN-EXPANDER-PAIR83 — paired bounded-occurrence expander YES/NO control for EXPANDER-RESIDUAL-SIZE82

**Timestamp:** 2026-10-23 08:00 KST (hourly check, Claude)
**Global status:** P versus NP OPEN; P versus RP OPEN. Nothing here is a lower bound.

## Check of repository
Branch head `baf4ee4a` (Grok review 07:12 KST over EXPANDER-RESIDUAL-SIZE82). New since the last check: Lemmas 82A-C (restricted, syntax-local) and the :48 task "construct a paired bounded-occurrence expander YES/NO family without constant-size UNSAT core or trivial polarity signature."

## Corpus reviewed
SIZE82 synthesis/handoff/audit/result JSON; root `main.tex` (62 lines, all ownership markers balanced, OPEN throughout); `AGENTS.md`. Not re-read this hour: LSPV-1..5 older reports, `tasks/`, explorations (hourly scope); prior notes are relied on only for the SIZE82 statement, which was read in full.

## Construction (all items EXACT unless stated)
Take a connected cubic graph G on n vertices, edge variables x_e (m=3n/2), charges c in {0,1}^V with sum c even (YES) or odd (NO). Each vertex v gets the 4 width-3 clauses forbidding the assignments of its 3 incident edge variables with parity != c_v.
- Bounded occurrence: each variable occurs in exactly 8 clauses (Delta = 8 in the incidence graph).
- Pair distance: flipping one charge c_v replaces exactly the 4 clauses at v (symmetric difference 8 clauses).
- NO instance is **minimally unsatisfiable** at clause level (n=6,8, exhaustive): no UNSAT core smaller than the whole formula. Vertex-level argument for all connected G: dropping any vertex's constraints leaves a satisfiable parity system.
- **Lemma 83A (EXACT, extends 82A beyond monotone formulas).** For *any* partial assignment of k variables, the simplified CNF's incidence graph is H minus at most (1+Delta)k vertices (assigned variables and satisfied clauses; unsatisfied clauses merely shorten). So Lemma 82B applies to every branch, not just all-true, whenever the incidence graph H is an h-vertex expander. The syntax-local separator retirement therefore also covers this non-monotone pair, *conditional on H being an expander* (see below).

## Hostile semantic bypass (the important negative)
The pair is decided in linear time two independent ways: (i) Gaussian elimination over GF(2) on the n x m incidence system; (ii) a **polarity signature**: the total charge is (sum over clauses of [1 - (#negated literals mod 2)]) / 4 mod 2, one scan. (Naive global negation parity is degenerate — always even — which is why the first audit draft failed; fixed.) Hence this family is an easy source: it supplies no SAT runtime hardness, and it answers the :48 task only partially: the no-small-core requirement holds, the no-trivial-signature requirement **fails**. Any semantic compiler must charge such an algebraic scan. Known resolution-width lower bounds for Tseitin on expanders (Urquhart; Ben-Sasson-Wigderson) concern resolution, not algorithms with algebraic access, so they do not contradict this bypass.

## Computational audit (COMPUTATIONAL, finite)
`experiments/review/2026-10-23_tseitin_expander_pair83_audit.py`, pure python, ~2 s, single stage (no chunking needed). 21 pair trials (n in {6,8,64,128,256}), **2206 assertions, 0 failures**: YES sat/NO unsat, GF(2) agreement, 8-clause pair distance, minimal unsatisfiability, occurrence = 8, deletion bound k+|satisfied| <= (1+Delta)k over 200 random branches per graph, signature agrees with decider 18/18. Spectral measurement of the lazy-walk gap on the incidence graph: 1-lambda2 in [0.014, 0.033] with 300 power iterations (under-converged iteration only *under*-estimates the gap). This is a numerical indication of expansion, **not** a proof; random cubic graphs are expanders w.h.p. (known theorem, Bollobas), but the vertex-expansion constant h of the *incidence* graph was not certified here.

## PQ-technique / transfer classification
- Quadratic-form / GF(2) rank: Tseitin = rank-deficient linear system; EXACT OBJECT transfer, and it is exactly the weakness (algebraic structure exploitable by an algorithm).
- Resolution-width / Hilbert-function lower bounds: FAILED TRANSFER to arbitrary algorithms (algebraic access defeats them).
- Locality/VLSI separators: SIZE82 expansion argument reused; nothing new.

## Duplication / what changed relative to root main
Not new: 82A-C. New: 83A (non-monotone extension, conditional on expansion) and the negative result that the paired family has a trivial algebraic decision. Root `main.tex` status is unchanged: P vs NP OPEN, semantic acquisition OPEN.

## Next
To defeat GF(2) and polarity bypasses a hard-looking pair must be non-affine (e.g. Tseitin with mixed XOR/AND gadgets or random 3-XOR-plus-noise at constant clause density), but then the exhaustive "no small core" and "decider" facts are no longer provable here. That is the next test; OPEN.
