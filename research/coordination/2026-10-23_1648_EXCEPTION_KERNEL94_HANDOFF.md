# EXCEPTION-KERNEL94 handoff

**Status:** P versus NP remains OPEN.

## Exact new rung

For a three-valued CSP with affine/permutation constraints and p arbitrary
binary-relation exceptions:

- charged holonomy contraction either detects inconsistency or represents each
  affine component by one three-valued root;
- at most 2p roots remain incident to nontrivial exception records;
- selecting one endpoint of every exception gives a vertex cover of size
  c <= p;
- exact continuation costs O(3^c p) after linear acquisition and uses
  linear peak storage;
- the decision kernel has at most 6p one-hot Boolean variables and 23p
  clauses of width at most three.

This is a **PROVED/EXACT upper bound**, not evidence that 3^p is necessary.
For p=O(log N) it is polynomial. Unrestricted p contains graph 3-coloring
through the inequality relation, a known NP-complete endpoint.

## Transport ledger

There is an equal-metadata family of p disjoint relation records whose SAT
label is AND of p designated table bits. Every deterministic exact field-query
algorithm reads all p fields on the all-one input. A direct scan also decides
the family in O(p) word time and O(1) extra words. Since
N=Theta(p log p), this is only Omega(N/log N) acquisition. Any explicit
normalization can spend Theta(p), so the positive transport remainder is not
established.

## Cross-role reconciliation

- CUTVERTEX68: exact critical clauses still give only input-order acquisition;
  recognized affine parity has a polynomial bypass.
- WIDTH-CERT52: linear feedback sets coexist with constant certified
  elimination width.
- QUANTIFIER-CERTIFICATE-BARRIER60: hard all-completion validation is not
  compulsory work for a one-completion SAT decider.

## Audit

Seed 202610231648; 1,820 exhaustive-reference random instances, plus holonomy,
same-component, K4, size, cover, leaf-count, and field-sensitivity controls.
**7,438 assertions, zero failures.** Finite testing is COMPUTATIONAL only.

## First missing lemma

For one fixed NP-complete relation language, prove an all-decider source-aware
compression-or-continuation theorem that survives affine contraction,
bounded-width/cutset algorithms, source recognition, caching, alternate
encodings, and decide-first normalization. No unrestricted lower bound
currently crosses this arrow.
