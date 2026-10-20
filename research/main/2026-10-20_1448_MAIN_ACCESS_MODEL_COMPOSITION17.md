# MAIN synthesis — ACCESS-MODEL-COMPOSITION17

Timestamp: 2026-10-20 14:48 KST  
Global status: **P versus NP remains OPEN.**  
Scope: only MCSP/MKTP magnification and arbitrary-decider ARC/FLMV contraction. COMPACT-HISTORY20 remains a supporting diagnostic, not a third route.

## Recovery

The governing portfolio, continuity protocol, COMPACT-HISTORY20 addendum, current `main2.tex`–`main5.tex`, the shared fallback document, and the newest visible peer artifacts were checked. The current root blobs are `main2` `56464cb3...`, `main3` `d82342d2...`, `main4` `0281dcfc...`, and `main5` `05d9adae...`. Root `main.tex` is blob `2b73364d...` and still contains the literal `Full content continues` placeholder; it was not modified.

New peer evidence after VIRTUAL-ORDINARY-INPUT16 consists of:

- `UNIVERSAL_SOURCE_REPLAY1_SHORT` (:12): an exact post-pass replay lower bound, a local bit-query escape, and a counterexample to naive round-robin portfolio space. The full executable package was not visible on GitHub; the short report explicitly says it remains in the conversation bundle.
- `REDTEAM34` (:36): 2,046 source streams, 18,434 ordinary local queries/source reads, 49,335 affine serial checks, 36 large-clock checks, 508 unit-witness checks, three quantifier-swap checks, and 95 early-negative checks, with zero finite-control failures. These are restricted computational checks.
- The latest visible :24 body remains `ARC-HISTORY-INPUT-GATE2`; no later complete :00 body was found.

The shared fallback log independently records the :12 result as pending full GitHub publication. No unavailable body is reconstructed here.

## Ideas proposed before literature search

1. Compose local virtual-input generators recursively and test whether their access exponents add or form a geometric series.
2. Memoize only a bounded working set of generated bits; compare this with fully stateless regeneration and with the space cost of caching all children.
3. Flatten a stack of deterministic generators into one base-source transducer and charge every base-input probe.
4. Separate random-access base inputs from one-way sources: seek an order-compatible generator, or prove that arbitrary post-pass coordinate replay requires a linear synopsis.

The intended falsifier was a nested coordinate request whose source bits cannot be regenerated in the native model without either a full retained table or an exponent at least the ARC slack.

## Primary-source model check

- CHMY's STACS 2021 theorem is explicitly for a one-tape Turing machine with an additional **one-way read-only input tape**; its randomized lower bound is near `N^1.99` for a fixed MCSP threshold. This does not grant random rereads of a derived target.
- MMW's STOC 2019 construction begins with an already-present `N`-bit truth table, reads successive blocks, and makes ordinary short `Sigma_3 SAT` queries. The theorem does not construct a SAT-derived target or a replay synopsis.
- FLMV's 2005 lower bound is for deterministic random-access Turing machines. Its model permits charged on-demand evaluation of input bits, so a total local transducer can stand in for materialization.
- Hutter's certified fastest-program theorem controls time relative to a fixed provably correct competitor. Its streaming extension caches the input prefix; it does not prove a sublinear-space replay theorem and does not bound the unknown polynomial exponent of the winning solver.

Primary sources: <https://doi.org/10.4230/LIPIcs.STACS.2021.23>, <https://people.csail.mit.edu/rrw/MCSP-MKTP-stoc19.pdf>, <https://lance.fortnow.com/papers/files/tst.pdf>, and <https://arxiv.org/abs/cs/0206022>.

## The access-model composition theorem

Let `Q_0=x` be an explicit read-only string of length `N`. For `j>=0`, let `Q_{j+1}` have length

`|Q_{j+1}| = |Q_j|^(v+o(1))`, where `0<v<1`.

Assume there is one uniform deterministic total transducer `G_j` that, given an index and random access to `Q_j`, returns the corresponding bit of `Q_{j+1}` in time `|Q_j|^(g+o(1))`, live workspace `|Q_j|^(h+o(1))`, and at most that many source-bit probes. Then a requested bit of `Q_r` can be answered directly from `x` with

`q_r = g(1+v+...+v^(r-1)) = g(1-v^r)/(1-v)`

as its base-`N` time/probe exponent. Its live generator workspace exponent is at most `h` (plus logarithmic indices and a depth-`r` call stack) when the nested calls are sequential.

**Proof.** At depth one the exponent is `g`. If a depth-`r` source bit costs `N^(q_r+o(1))`, then `G_r` makes at most `|Q_r|^(g+o(1))=N^(g v^r+o(1))` such calls. Hence `q_{r+1}=q_r+g v^r`. The closed form follows by induction. Only one recursive call and one generator workspace need be live at a time, so summing the geometrically smaller workspaces does not increase the largest polynomial exponent. Determinism and totality make the flattened answer identical to materializing every intermediate string.

For `v=1/2`, the cumulative bit-generation exponent is strictly below `2g` at every finite depth and tends to `2g`. Thus the VIRTUAL-ORDINARY-INPUT16 recurrence

`t' <= max(11/10, e, 3/5+g+t/2)`,  
`s' <= max(1/2, h, s/2)`

already charges nested regeneration: after `r` stages its unfloored time is

`(1/2)^r t_0 + (3/5+g)(1-(1/2)^r)/(1-1/2)`,

with limit `6/5+2g`. Therefore `g<1/400`, `e<241/200`, and `h<=1/2` still give finite entry below `tau=241/200` in time and at most `1/2` in space. This confirms the arithmetic of the prior conditional ARC window; it does not construct `G_j`.

## The one-way replay separation

Suppose an `N`-bit source is consumed once and, only after the pass ends, an algorithm must answer every possible coordinate request exactly from a retained synopsis. That synopsis needs at least `N` bits: otherwise two distinct sources share a synopsis, differ at some coordinate, and force the same answer for two different correct bits.

In contrast, with random access to the source, bit `x_i` can be carried through one constant-size ordinary SAT instance after one source read: output a satisfiable unit instance when `x_i=1` and a contradictory one-variable instance when `x_i=0`. Repeating this for all coordinates transports all `N` bits using `N` reads and constant query size; it does **not** compress the source or eliminate the linear total acquisition cost.

Consequences:

- Stateless local regeneration is a legitimate candidate interface for FLMV-style random-access ARC.
- It cannot be transplanted to CHMY's one-way tape unless requests are generated in stream order, answered during the pass, or an `N`-bit replay cost is explicitly charged.
- Hutter-style caching restores replay but carries the cached input in live space.
- Short ordinary queries do not imply source compression; they can transmit many bits over many calls.

## Reproducible adversarial test

`experiments/review/2026-10-20_access_model_composition_audit.py` uses exact rational arithmetic and exhaustive finite controls. It verified 103,298 assertions with zero failures:

- 576 geometric-composition cases for `v` in `{1/2,2/3,3/4}`, three `g` values, and depths 1–64;
- 16,384 ARC recurrence cases and strict entry below `241/200` for four `g<1/400` values and initial exponents 1–64;
- 3,586 local ordinary-query checks for every bit of every binary string of lengths 1–8;
- all 65,536 maps from eight three-bit inputs to four two-bit synopsis states; every map collided, with minimum four colliding pairs.

The finite tests illustrate the exact lemmas; they are not lower bounds for unrestricted computation.

## Proof DAG

| Arrow | Status | Exact boundary |
|---|---|---|
| FLMV deterministic random-access SAT lower bound | ESTABLISHED | Same machine and simultaneous resources required |
| CHMY one-way-input MCSP lower bound | ESTABLISHED | One-way input; not a random-access target oracle |
| MMW one-pass search-MCSP/MKTP streamer | ESTABLISHED | Target already present; ordinary short queries |
| Hutter provable fastest-program time competition | ESTABLISHED | Fixed competitor; stream caching is charged space |
| Geometric generator-composition theorem | PROVED | Uniform deterministic total local generators |
| Exact post-pass synopsis lower bound | PROVED | Arbitrary coordinates after a one-way pass require `N` bits |
| Finite composition/replay audit | COMPUTATIONAL | 103,298 exact assertions; restricted controls only |
| ARC window `g<1/400`, `h<=1/2`, `e<241/200` | CONDITIONAL | Missing all-input hereditary local successor generator |
| SAT -> charged total ordinary MKTP/KT target | OPEN | Both promises, semantic fibers, keys, replay, output |
| MMW unknown solver exponent `C` | OPEN | Certified portfolio relocates rather than bounds `C` |
| Compact shared-history witness | OPEN | Requires one `exists W forall i` circuit of size `tau(n)^o(1)` |
| Random-access generator transferred unchanged to CHMY | RETIRED | Violates the one-way source model absent order compatibility |
| Static synopsis inferred from short queries | RETIRED | Many short queries can transmit all source bits |

COMPACT-HISTORY20 is unchanged: exact oracle-query and truth-table-history lower bounds do not imply an unrestricted time lower bound for explicit succinct transitions such as modular increment. The required single shared witness quantifier remains open.

## Allocation

- **:00 MCSP:** formulate an order-compatible one-way `R_k` bit stream, or prove that some required query coordinate is necessarily requested after its source position has passed. Do not import random-access regeneration into CHMY.
- **:12 Universal Solver:** replace the naive round-robin race by the exact selective Hutter scheduler and record cached input, solver workspace, output, and whether the unknown exponent `C` changes. Treat a fixed competitor's exponent as still unknown.
- **:24 ARC:** give one uniform all-input `G_j(x,i)` with `g<1/400`, `h<=1/2`, and total acquisition `e<241/200`; include recursive calls and source rereads in the ledger.
- **:36 Red team:** construct an adaptive request order forcing either a forbidden one-way reread, an `N`-bit retained synopsis, or a generator exponent at least `1/400`.
- **:48 Synthesis:** accept local virtual inputs only after the source-access model is named and nested generator costs are flattened to the base input.

Strongest falsifier: one load-bearing child/query family whose correct adaptive coordinates cannot be scheduled in source order and whose random-access generator needs `g>=1/400` or `h>1/2`. Strongest positive target: a single uniform total ARC bit predicate inside the strict window. Neither is currently proved. **P versus NP remains OPEN.**
