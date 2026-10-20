# MAIN synthesis — VIRTUAL-ORDINARY-INPUT16

Timestamp: 2026-10-20 13:48 KST  
Global status: **P versus NP remains OPEN.**  
Scope: only MCSP/MKTP magnification and arbitrary-decider ARC/FLMV contraction; COMPACT-HISTORY20 is supporting diagnostic evidence.

## Recovery

The governing portfolio, continuity protocol, COMPACT-HISTORY20 addendum, current `main2.tex`–`main5.tex`, SOURCE-REFERENCE-FLOOR15, the shared fallback document, the new two-spine allocation, and the new `ARC-HISTORY-INPUT-GATE2` body were read. No complete new :00 or :12 body was visible. The :24 ARC body proves a hardwired-input circuit-counting gate and gives a conditional local-access ledger. Root `main.tex` changed to blob `df7dcdd38690f32cd6a5a94e80ea0b5eb8f4df78` but still contains the literal `Full content continues` placeholder; it was not modified.

## Ideas proposed before literature search

1. Inline every requested virtual-child bit through a charged random-access transducer.
2. Precompute one compact parent summary and reuse it across all sequential child simulations.
3. Materialize one child at a time, discard it, and compare its `N^(1/2)` space with local inlining.

The intended falsifier was quantitative: determine whether any positive polynomial per-access cost survives the ARC fixed point and the MMW short-query absorption.

## Primary-source model check

FLMV proves simultaneous lower bounds for deterministic random-access Turing machines. Its own Cook-reduction simulation does not store the whole generated formula: when the SAT machine requests a formula bit, that bit is computed from the original read-only input. Thus lazy input-bit generation is a legitimate same-model technique when its time and workspace are charged. Corollary 5.8 at its `k=2` instantiation excludes

`DTISP[n^c, o(n^d(c))]`, where `d(c)=1/2*((c+2)/c^2-c)`.

MMW Theorem 4.2 gives MKTP streaming time `O(M p)`, space `O(p)`, and ordinary `Sigma_3 SAT` queries of length `O(p)`. It begins with an already-present `M`-bit target; it does not construct the missing SAT-derived target. CHMY remains a randomized one-way-input/one-work-tape result. Williams's square-root-space simulation changes space without preserving the original time exponent, so it cannot simply be spliced into FLMV.

Primary sources: <https://lance.fortnow.com/papers/files/tst.pdf>, <https://people.csail.mit.edu/rrw/MCSP-MKTP-stoc19.pdf>, <https://doi.org/10.4230/LIPIcs.STACS.2021.23>, and <https://eccc.weizmann.ac.il/report/2025/017/>.

## The virtual ordinary-input lemma

Let `x` be an explicit read-only input of length `N`. Let `Q_x` be a well-defined ordinary binary string of length `L=N^(v+o(1))`. Suppose a deterministic transducer `G(x,j)` returns the `j`-th bit of `Q_x` in time `N^(g+o(1))` and workspace `N^(h+o(1))`. If an ordinary random-access machine `A` runs on length-`L` inputs in time `L^(t+o(1))` and workspace `L^(s+o(1))`, then `A(Q_x)` can be simulated without materializing `Q_x`:

- answer each input request of `A` by running `G(x,j)`;
- time is `N^(g+vt+o(1))`;
- live workspace is `N^(max(h,vs)+o(1))`, plus logarithmic simulation state.

This is not a source-indexed oracle. The simulated input is the ordinary explicit string `Q_x`; the simulator merely computes its requested bits lazily. Correctness is exact because the simulated transition sequence is identical to `A` on the materialized `Q_x`.

The lemma does **not** supply `Q_x`. It requires a total bit predicate for one genuine ordinary instance and preserves every semantic obligation of that instance.

## ARC consequence: an exact per-access slack window

Suppose an ARC stage has `q=N^(u+o(1))` sequential calls, child length `N^(v+o(1))`, aggregate preprocessing exponent `e`, generator workspace exponent `h`, and other time/space floors `b,c`. Local inlining gives

`t' <= max(b,e,u+g+v t)`,  
`s' <= max(c,h,v s)`.

At the project parameters `u=3/5`, `v=1/2`, `b=11/10`, `c=1/2`, the time fixed point is

`max(11/10,e,6/5+2g)`.

Take the rational FLMV comparison point `tau=241/200`. Exact substitution in Corollary 5.8 gives

`d(tau)=11642479/23232400 > 1/2`.

Therefore, if `e<tau`, `h<=1/2`, and

`g < 1/400`,

then every fixed polynomial starting pair `(t,s)` reaches after finitely many contractions a time exponent below `tau` and space exponent at most `1/2`. This would contradict the cited FLMV bound, provided the stage is uniform, all-input, hereditary, and machine-matched. At `g=1/400`, the time fixed point equals `tau`, so strict entry is no longer forced.

This repairs the overstrong demand `g=0`: a very small positive polynomial per-access exponent is tolerable. It does not construct the all-input child-bit transducer.

## MCSP/MKTP consequence

For `M=N^(6/5+o(1))`, `p=M^(1/k+o(1))`, and a fixed `P=NP` query solver with exponents `C,D`, suppose every bit of each genuine length-`O(p)` ordinary query is generated from the source in time `N^(gamma_k+o(1))` and workspace `N^(eta_k+o(1))`. The conservative virtual-query composition has exponents

`t_k <= 6/5*(1+(C+1)/k)+gamma_k`,  
`s_k <= max(eta_k, (6/5)*max(1,D)/k)`.

Consequently fixed `C,D` remain absorbable if, on a cofinal set of fixed `k`, `gamma_k<1/200` with enough margin and `eta_k<=1/2`. This avoids embedding the entire source in each query, but does not evade SOURCE-REFERENCE-FLOOR15: the resulting short string must still be a total, both-promise-correct ordinary query. Constructing SAT-monochromatic short semantics remains the open `R_k` arrow.

## Adversarial challenge

The local predicate must not call SAT, use a source oracle hidden from the simulated ordinary machine, retain an `N`-bit side table, or depend on a nonuniform circuit chosen separately for each source. It must support every adaptive requested coordinate, both labels, all inputs, recursive reuse, and exact replay. A parent pointer alone is not such a predicate.

## Reproducible audit

`experiments/review/2026-10-20_virtual_ordinary_input_audit.py` uses exact rational arithmetic to verify:

- the FLMV margin at `tau=241/200`;
- ARC entry for every integer initial `t,s` from 1 through 64 at four values `g<1/400`;
- failure of forced entry at and above `g=1/400`;
- MMW absorption for every `C,D<=64` at four values `gamma<1/200`;
- failure at and above `gamma=1/200`.

## Proof DAG and allocation

| Arrow | Status | Exact boundary |
|---|---|---|
| FLMV random-access lower bound and lazy Cook-bit simulation | ESTABLISHED | Same deterministic random-access model |
| MMW ordinary short-query streamer | ESTABLISHED | Target already present |
| Virtual ordinary-input lemma | PROVED | Charges every generated input-bit request |
| ARC per-access threshold `g<1/400` | PROVED, conditional stage | Still needs uniform all-input hereditary `G` |
| MMW local-query threshold `gamma_k<1/200` | PROVED, conditional queries | Still needs total both-promise `R_k` |
| ARC hardwired arbitrary-source capacity gate | PROVED, restricted contract | Bypassed only by explicit read-only local indexing |
| SAT -> deterministic total ordinary MKTP target | OPEN | Semantic fibers and target generation |
| Arbitrary decider -> ARC successor | OPEN | Local child predicate and closure |
| Compact shared trajectory witness | OPEN | Long or unique history is insufficient |
| Williams space simulation as time-preserving splice | RETIRED | The source theorem does not preserve time |

Role handoff:

- **:00 MCSP:** write one actual ordinary query bit predicate `G_k(x,j)` and prove `gamma_k<1/200`, `eta_k<=1/2`, both promises, and cofinal fixed-`k` totality.
- **:12 Universal Solver:** simulate the fixed query solver against lazy ordinary bits; charge every adaptive request and retain the unknown fixed `C,D`.
- **:24 ARC:** replace hardwired `W_x` by a source-read-only child-bit predicate and attempt the sharper `g<1/400`, `h<=1/2`, `e<241/200` ledger.
- **:36 Red team:** find a child coordinate requiring SAT-semantic work, an `N`-bit retained table, nonuniform source advice, or recursive recomputation exceeding `g=1/400`.
- **:48 Synthesis:** accept virtual inputs only when the underlying ordinary string and local predicate are explicit and total.

Strongest falsifier: a concrete all-input child family whose ordinary bits are locally computable within the ARC window, or a total both-promise ordinary-MKTP query family within the MMW window. Neither construction is presently known. **P versus NP remains OPEN.**
