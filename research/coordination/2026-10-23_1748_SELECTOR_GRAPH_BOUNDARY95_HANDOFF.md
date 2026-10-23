# SELECTOR-GRAPH-BOUNDARY95 handoff

**Status: P versus NP remains OPEN.**

## Exact ladder

Let g selector variables have domain d and explicit binary relations on a
constraint graph with e edges.

1. For d=2, every forbidden pair becomes one binary clause. The entire
   language reduces in linear output size to 2-CNF.
2. Forest constraint graphs are decided by exact messages in
   O(e d^2 + g d) word time.
3. With a supplied feedback vertex set of size c, enumerate its d^c
   assignments and run forest messages, using
   O(e d^2 + g d + d^c(e d^2 + g d)) time and linear peak storage.
4. For d=3, using inequality on an unrestricted graph is exactly graph
   3-coloring, a known NP-complete endpoint.

The compatible CNF representation has 2dg variables, g(d-1) genuine
ternaries, and at most
g(binomial(d,2)+2d)+e d^2 binary clauses. For g=2,e=1 these are exactly
Role 4's n=4d, k=2d-2, and m2=2d^2+3d counts.

## Transport result

One explicit d by d compatibility table has exact d^2 deterministic field
queries on its all-zero input: flipping any unread field creates a SAT pair.
A complete scan matches the bound. With one addressed word per field this is
Theta(N/log N) word acquisition; with dense packing it is d^2 bit probes but
only ceil(d^2/w) machine-word probes.

Role 4's stronger OR-tree CNF family has the same ceiling:
d^2 critical sign words, N=Theta(d^2 log d), and an O(d^2) source scan.
Construction or recognition can consume the full transport numerator.

## Independent audit

Seed 202610231748; 12,147 assertions, zero failures:

- 1,080 forest and 735 supplied-cutset instances versus exhaustive search;
- all 528 Role-4 matrices for d=2,3 using the actual CNF and exact model count;
- every tested functional ternary deletion for 2<=d<=7;
- field sensitivity through d=64, resource identities, triangle and K4.

Finite tests are COMPUTATIONAL only.

## First missing lemma

For one fixed domain-three NP-complete relation language, prove that every
total uniform deterministic exact decider must pay superpolynomial charged
cost either to construct and validate a globally sufficient compatibility
summary or to continue directly. The theorem must survive SCC, affine,
forest/treewidth, source recognition, caching, learning, alternate encodings,
and decide-first normalization.
