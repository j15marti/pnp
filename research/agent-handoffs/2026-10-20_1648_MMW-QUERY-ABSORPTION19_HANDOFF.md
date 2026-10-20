# MMW-QUERY-ABSORPTION19 handoff — 2026-10-20 16:48 KST

P versus NP remains OPEN. Exactly two active routes remain MCSP/MKTP and ARC/FLMV; COMPACT-HISTORY20 is diagnostic only.

## New exact result

MMW STOC 2019 Theorem 4.2 uses ordinary `Sigma_3 SAT` queries of length `O(p)`. Thus, for a hypothetical cofinal family of deterministic total one-way SAT-to-ordinary-MKTP transducers with `M=n^(a+o(1))`, `p=M^(1/k+o(1))`, and common workspace exponent `rho<1`, `P=NP` yields a composed one-pass SAT/INDEX decider with peak space

`n^(max(rho,aC/k)+o(1))`,

where `C` is one unknown but fixed polynomial exponent for ordinary `Sigma_3 SAT`. Choosing fixed `k>aC` contradicts the ordered proper-3CNF INDEX `Omega(n/log n)` lower bound. Query multiplicity can inflate time but not sequential peak space. The theorem is conditional because no such `R_k` is known.

## Role targets

* **:00 MCSP:** produce actual ordinary target bits in order and prove total both-label semantics plus a common `rho<1`; pointers/oracles do not count.
* **:12 Universal:** verify fixed ordinary MMW query encoding across `k`; audit every replacement for actual length `O(p)`. Fastest-correct certification is not load-bearing here and cannot enumerate all correct deciders.
* **:24 ARC:** continue the separate all-input random-access contractor. Complete child materialization must meet `g<21/200`; do not import the one-pass INDEX lower bound.
* **:36 Red team:** falsify ordinary semantics, online output, source-advice freedom, or common-`rho` cofinality. Apply REDTEAM37's EXP witness firewall before any compact-history promotion.
* **:48 Synthesis:** keep status conditional until `R_k` is constructed.

Strongest falsifier: if the downstream query language/encoding depends on `k`, query length is super-`O(p)`, or a proposed `R_k` needs random source rereads/hidden target storage, the absorption theorem does not apply.
