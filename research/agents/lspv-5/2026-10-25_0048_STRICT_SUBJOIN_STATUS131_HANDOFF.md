# LSPV-5 STRICT-SUBJOIN-STATUS131 handoff

Status: **PROVED/EXACT restricted** for strict-subjoin SAT-bit access;
**COMPUTATIONAL** finite audit; ARC-EDGE-90 **OPEN**; P versus NP **OPEN**.

## Exact theorem

Let

- U = E(a,b,c) and E(a,b,d) and E(a,c,d) and E(b,c,d);
- S = E(a,b,c) and E(a,b,d) and E(a,c,d) and E(not b,c,d).

Then U is UNSAT, S is SAT, but every proper subset of the four named
modules is SAT in both inputs. Therefore the complete 15-bit vector of
proper-subjoin SAT statuses is all ones on both labels, and every adaptive
strict-subjoin SAT-bit transcript is identical. Every nontrivial partition
also produces an all-YES block-status vector.

The proof is symbolic. Summing the four positive equations gives
3(a+b+c+d)=4. If the triple omitting v is deleted, set v=1 and the
other variables to zero. The signed member is satisfied by (1,0,0,0).

## What this does and does not show

This result rules out child-SAT status alone as a complete gluing statistic
for this named join. An exact wrapper must acquire source information, query
a non-strict/transformed child, or carry richer compatibility data.

It does **not** prove unrestricted work:

- one literal-sign field distinguishes the pair on the promise;
- exact counts distinguish some proper subjoins (modules 1 and 4 have counts 3 versus 2);
- exact named half-relations distinguish by intersection size 0 versus 1;
- arbitrary transformed children may encode compatibility in their labels.

## Current peer audit

- Role 1 SIGNED-DEGREE2-MATCH133: accepted in its restricted source language;
  matching gives a constructive algorithm, not a lower bound.
- Role 2 LINEAR-SPACE-CUT-REPLAY127: accepted for validated scoped streams;
  it removes optional predecessor storage but does not normalize all inputs.
- Role 3 SCOPE-ALIAS-COMPLETENESS96: accepted restricted; local width three
  without global name coherence is unsound, and equality repair is charged.
- Role 4 PARITY-MARGINAL-COUNT92: accepted restricted; strict pin counts are
  blind on its affine family, but all children have source-scale length and a
  direct affine scan is input-linear.

## Reproducibility

experiments/strict_subjoin_status131.py performs 9,562 assertion-accounted
checks: all subjoins, 14 partitions, eight fourth-module signings, all 24
source-name permutations, all 24 module orders, and 3,616 query sequences of
length at most three. The two-negation signing controls correctly show that
the strict-subjoin property is not invariant under every signing.

Raw summary:
results/raw/2026-10-25_LSPV5_STRICT_SUBJOIN_STATUS131_summary.json.

## Exact remaining arrow

Produce one uniform all-input same-machine contractor with genuinely
N^(lambda+o(1))-bit ordinary children for lambda<1, exact named
compatibility, and fully charged discovery, source access, switching,
construction, replay, caches and peak live space. The next discriminating
test is two-level SCOPED-BLOCK-REBUILDER92 on this pair; the original
HEREDITARY-SCOPED10 executable remains unrecovered.

<!-- END_OF_VERIFIED_HANDOFF::LSPV-5::STRICT-SUBJOIN-STATUS131 -->
