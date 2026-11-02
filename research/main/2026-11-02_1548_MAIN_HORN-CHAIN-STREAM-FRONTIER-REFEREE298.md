# PNP Independent Proof Red Team — REFEREE298

**Run:** 2026-11-02 15:48 America/Los_Angeles  
**Task identity/status:** preserved exactly; no task or schedule operation was performed.  
**Scientific status:** P versus NP remains **OPEN**.

## Result at a glance

This run fixes the same preselected binary-premise mixed calculus
$R_{\mathrm{mix341}}$ and proves an exact growing-family derivation/schedule
frontier.  For $n\ge 1$, let

$$
F_n=(x_1)\land\bigwedge_{i=1}^{n-1}(\neg x_i\lor x_{i+1})\land(\neg x_n).
$$

The $n+1$ source clauses are clause-minimally UNSAT.  In
$R_{\mathrm{mix341}}$, every sound conservative derived node has at most two
explicit premises and unit logical weight.  Then

$$
\boxed{W_{R_{\mathrm{mix341}}}(F_n)=n.}
$$

In a separate execution model charging one unit for every source-record load
and every inference, with a conclusion inserted while its premises remain
live, the exact schedule frontier is

$$
\boxed{Q_{\min}(F_n;S\ge3)=2n+1,\qquad S_{\min}=3\text{ live records}.}
$$

The records contain only one or two literals in the exhibited Resolution
schedule.  With canonical ordered line-DIMACS input, the proof can therefore
be generated and checked in $O(N)$ time and $O(\log N)$ writable bits, where
$N=\Theta(n\log n)$ is encoded input length.  This **falsifies the proposed
invariant that minimum derivation-node cost itself forces comparable peak
writable space**.  It does not falsify proof-space lower bounds for other
families or systems.

The result gives only

$$
\overline W_{R_{\mathrm{mix341}}}(N)=\Omega(N/\log N)
$$

along an explicit length subsequence.  This is linear up to encoding and is
not a superpolynomial worst-case lower bound.

## Fixed calculus and two cost models

The logical system is exactly the previously declared
$R_{\mathrm{mix341}}$: free source-labelled CNF axioms; charged RES, AND3,
XOR, LOCAL-CONVERT and conservative two-input DEF nodes; every derived node
has at most two explicit parents and cost one.  Ordinary Resolution is the
only rule used by the upper bound.  Free optimal proof selection remains
granted.

The logical metric is

$$
W_R(F)=\min_\pi |V_{\mathrm{derived}}(\pi)|.
$$

The scheduling metric is intentionally separate.  A source record costs one
load, a derived node costs one inference, erasure is free, and a conclusion is
inserted before its premise records are erased.  Thus $Q$ is not silently
identified with $W_R$, and record capacity is not silently identified with
encoded proof length or physical RAM.

## Exact proof

### Minimal UNSAT and source necessity

Write the sources in order as $C_0=(x_1)$,
$C_i=(\neg x_i\lor x_{i+1})$ for $1\le i<n$, and
$C_n=(\neg x_n)$.  They are jointly inconsistent by forward implication.
Each source is indispensable:

* deleting $C_0$: set every variable false;
* deleting $C_n$: set every variable true;
* deleting $C_i$, $1\le i<n$: set $x_1,\ldots,x_i$ true and
  $x_{i+1},\ldots,x_n$ false.

Every displayed assignment satisfies all remaining sources and falsifies the
deleted source.

Consequently every sound conservative refutation root must have all $n+1$
sources in its ancestry.  In the undirected ancestry graph, if there are $q$
charged nodes, connectivity gives at least $(n+1)+q-1$ edges.  At-most-binary
premises give at most $2q$ edges.  Hence $q\ge n$.

### Matching derivation

Resolve $(x_1)$ successively with
$(\neg x_1\lor x_2),\ldots,(\neg x_{n-1}\lor x_n)$ to derive
$(x_2),\ldots,(x_n)$, then resolve $(x_n)$ with $(\neg x_n)$.
This uses exactly $n$ derived nodes, proving the logical optimum globally over
all legal mixed derivations—not merely over Resolution proofs or a bounded
optimizer search.

### Matching schedule and lower bounds

All $n+1$ indispensable sources must be loaded at least once and every
refutation needs at least $n$ inferences, so

$$
Q\ge(n+1)+n=2n+1.
$$

The chain schedule loads $C_0$ and $C_1$, inserts the first unit resolvent,
erases both parents, and repeats with the retained unit and the next source.
It uses exactly $n+1$ source loads and $n$ inferences.  Its peak is three live
records: two premises plus the newly inserted conclusion.  Conversely, some
binary node is necessary to merge more than one indispensable source, so the
declared insertion-before-erasure model requires at least three records.

Thus the full frontier in this model has no hidden time/space tradeoff:
capacity below three is infeasible, and every capacity at least three attains
$Q=2n+1$.

## Why this matters for the proposed time–space scatterplot

A plotted point must name its semantics:

| quantity | exact value here | what it does **not** imply |
|---|---:|---|
| minimum logical DAG nodes $W_R$ | $n$ | $n$ simultaneously stored nodes |
| minimum scheduled loads + inferences $Q$ | $2n+1$ | arbitrary-machine time lower bound |
| minimum live records | $3$ | three physical bits |
| writable payload in streamed verifier | $O(\log N)$ bits | general-SAT space upper bound |
| proof-search/optimizer work | not in $W_R$ | free implementable solver |

The correct scatterplot can contain a linear-work/logarithmic-space point for
this family even though the logical proof has $n$ distinct derived nodes.
Conversely, known pebbling formulas show that other Resolution families with
short proofs can require much larger proof space.  The axes must be measured,
not inferred from proof length alone.

The machine point is family-restricted.  A recognizer plus arbitrary exact
fallback is still a total SAT decider, but its global worst-case coordinates
are governed by the fallback.  The point therefore does not enter or refute a
general SAT forbidden region.

## Four falsifiers and outcomes

1. **Treat $W_R$ as a peak-space lower bound.** Falsified on $F_n$: the exact
   logical cost is $n$, while three live records and $O(\log N)$ writable bits
   suffice to stream the canonical proof.
2. **Add a unit-cost global Horn-UNSAT rule.** This collapses the family to one
   derived node, but changes the fixed calculus and hides a whole-formula
   validity check.  It is not a counterexample inside $R_{\mathrm{mix341}}$.
3. **Use a multi-source unit-cost semantic jump.** This evades the binary
   source-arity proof only by changing rule arity/weight.  LSPV-2's concurrent
   fan-in-weighted audit correctly requires weight at least $r-1$ for an
   $r$-premise rule if the source-union bound is to survive.
4. **Infer B1/B2/B3 from a fast Horn-chain recognizer.** Rejected.  A family
   recognizer is not a polynomial all-CNF algorithm, and the current linear
   $W_R$ is already polynomial.

## Both-label, malformed and certificate controls

The same-shaped SAT control replaces only the last source $(\neg x_n)$ by
$(x_n)$; the all-one assignment satisfies it.  For every UNSAT case, the
producer checks all $n+1$ same-original source-deletion witnesses described
above.  It rejects eight malformed encodings: missing/bad/nonnumeric header,
nonpositive count, missing terminator, out-of-range literal, clause-count
mismatch and trailing tokens.  Three corrupted proof DAGs—wrong parent, wrong
resolvent and missing root—are rejected.

Cases $n=1,2,3,4,8,16,64,256,1024$ passed.  At $n=1024$, the exact values are
$N=11{,}116$ input bytes, $W_R=1024$, $Q=2049$ and peak three live records.
The independent verifier replayed **1,121,543 assertion groups**, including
the complete 64-variable emitted proof and every deletion witness.

## Work and all-phase peak-space ledger

The mathematical streaming algorithm needs a fixed parser, two small clause
records, one output record, counters and source/head positions: $O(\log N)$
writable bits on the canonical ordered family.  It scans all $N$ source bits,
validates every rule and may stream its proof output; output storage is not
silently counted as writable workspace when written sequentially to a
separate output tape.  If the whole proof is materialized internally, the
space becomes $\Theta(n\log n)$ bits—an implementation choice, not the
minimum schedule.

The producer additionally constructs every deletion witness and rechecks all
remaining clauses, intentionally doing $\Theta(n^2)$ simple finite-control
work across the largest cases.  Its host run took 9.45 seconds and had a
1,183,968-byte traced Python peak.  Those are reproducibility diagnostics,
not native-machine bounds and not part of $W_R$.

No child contraction is claimed.  Any later materialized-child construction
still obeys the corrected all-phase envelope

$$
s'\le\max\{\rho,\eta,\lambda,\lambda s\},
$$

with $\rho$ covering preprocessing, conversion, generation and combination.

## B1/B2/B3 classification

| obligation | status after REFEREE298 | reason |
|---|---|---|
| B1 | **not falsified; OPEN generally for $R_{\mathrm{mix341}}$** | on this easy family, both runtime and $W_R$ are polynomial |
| B2 | **OPEN** | no domination theorem for every total correct decider is proved |
| B3 | **OPEN** | no implication from SAT in P to polynomial $\overline W_R$ for this fixed $R$ is supplied |

This run proves neither a superpolynomial $\overline W_R$ lower bound nor any
one of the bridges.  P versus NP remains open.

## Literature and repository search log

Searches were performed before finalizing the proof.

* `Paul Tarjan Celoni 1976 space bounds fast computation pebbling graphs
  primary paper` found Paul, Tarjan and Celoni,
  [*Space Bounds for a Game on Graphs*](https://doi.org/10.1145/800113.803643),
  STOC 1976.  Pebbling is the classical model behind live-DAG scheduling.
* `Ben-Sasson Nordstrom short proofs may be spacious resolution size space
  tradeoff primary paper` found Ben-Sasson and Nordström,
  [*Short Proofs May Be Spacious*](https://eccc.weizmann.ac.il/report/2009/002/),
  showing that linear Resolution length need not imply small Resolution
  space.  REFEREE298 is an easy exact opposite control, not a replacement for
  that theorem.
* `Cook Reckhow 1979 relative efficiency propositional proof systems primary
  paper` found Cook and Reckhow,
  [*The Relative Efficiency of Propositional Proof Systems*](https://www.cs.toronto.edu/~sacook/homepage/cook_reckhow.pdf).
  It supports the separation between proof-system completeness and a fixed
  system's quantitative bounds.
* Project searches `Horn chain streaming proof space frontier` and `HORN chain
  minimal UNSAT source arity` found prior Horn/frontier work, especially
  HORN-FRONTIER273 and the concurrent CLOCK-SUBCORE-B2-FIREWALL339.  The latter
  uses minimally UNSAT Horn chains to falsify B2 for an intentionally altered
  clocked calculus.  REFEREE298 instead keeps the unchanged
  $R_{\mathrm{mix341}}$ and proves its exact scheduled frontier.
* The project search also found LSPV-1 EXACT-WORKSPACE-FRONTIER, a finite
  five-variable pure-Resolution optimizer.  REFEREE298 contributes a closed
  form for an unbounded family in the mixed binary-premise calculus.
* Searches of `openai/codex`, `openai/openai-python` and
  `openai/openai-cookbook` for `DIMACS proof resolution pebbling` returned no
  relevant implementation.  This is a negative search result, not evidence
  of novelty.

No novelty claim is made for Horn propagation, source-arity counting,
pebbling or streaming proof verification.

## Exact next gap

Find a non-Horn, non-affine family whose **same fixed mixed-system** Pareto
frontier forces superpolynomial logical cost despite RES/XOR/AND3/DEF and
representation switching.  Separately prove B3 for that same system.  The
present chain calibrates the axes and rejects a false space inference; it does
not close either gap.

