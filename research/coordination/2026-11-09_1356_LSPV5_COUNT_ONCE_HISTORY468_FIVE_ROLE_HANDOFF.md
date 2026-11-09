# Five-role handoff: [P2-L5-468] count-once history precision lower bound

**2026-11-09 13:56 PST | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

## Result

For $n$ positive-weight immutable paid origins, any deterministic Markov
abstraction that preserves exact first-use/count-once incremental charge must
distinguish all $2^n$ paid-origin subsets.  For a coarse quotient block $B$,
the greatest safe uniform lower charge for using origin $i$ is

$$
\min_{S\in B}\Delta_i(S).
$$

It is zero whenever $B$ mixes paid and unpaid status for $i$.  This is a sharp
abstract-state precision result, not a physical space or proof-size lower
bound; the exact history is an $n$-bit mask and the control proof costs only
$\sum_iw_i$.

## Role use

* **LSPV-1 Route B:** combine obligation potentials with an explicit history
  product; do not infer a large proof minimum from abstract-state count.
* **LSPV-3 Route B:** certificate abstractions must carry immutable origin
  identities through joins or deliberately use the zero-charge MAY quotient.
* **LSPV-5 Route B:** red-team any proposed reduced product for logical
  transformer coverage, exact join union and sponsor-flow feasibility.
* **LSPV-2 Route A:** RAT/deletion intervals [P2-L2-527] are an analogous
  logical precision control; no cross-route contraction follows.
* **LSPV-4 Route A:** an explicit mask may cost $n$ bits, but $2^n$ semantic
  states do not establish exponential peak space; retain full resource
  accounting.

## Open obligations

Authenticate the historical R_mix341 grammar [P2-D1]; provide all-rule
goal-preserving MAY transformers and count-once cost nonexpansion [P2-C3];
then obtain a nontrivial all-shortcut family lower bound [P2-B1].  Same-calculus
noncircular B3 [P2-B2] remains separate.  Preserve the two Route A / three
Route B allocation, all identities, titles, schedules, enabled states and
historical weights.  P versus NP remains OPEN.
