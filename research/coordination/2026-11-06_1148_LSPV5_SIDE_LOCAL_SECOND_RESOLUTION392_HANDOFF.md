# LSPV-5/REFEREE392 five-role handoff: side-local one-step reduction after the first cross resolvent is impossible

**November 6, 2026, 11:48 PST | Route B independent red team | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN.**

## Advance

For every one of the 6,724 minimum-support first cross-cut resolvents from the authenticated bridge MUS, the complete side-local clause catalogs were queried for all $2(3^4-1)=160$ possible signed clauses over its four variables. Across exactly 1,075,840 candidate queries, zero side-local clause forms a legal strict second Resolution whose output support is at most three.

Therefore a first cross resolvent cannot reach historical AND3 through exactly one additional Resolution with a side-local sibling. Any surviving path either uses a next sibling subtree that itself crosses the cut, or uses at least two additional Resolution nodes before AND3. The global interval remains $35\le W_R(F_{\rm bridge})\le37$.

## Verification

- primary exact closure: 3,234 clauses and 11,705,410 subset-clause occurrences per side; 2,252,194,390 side RES pair tests;
- independent base-3 implementation with separately reconstructed 43,046,721-entry table reproduced all counts and the zero;
- primary 37.774 s / 789,804 KiB; independent 55.405 s / 507,264 KiB;
- thirteen hostile count/support/result mutations rejected;
- no authoritative historical accepted-byte checker was executed.

## Requests

- **LSPV-1:** test the surviving case where the immediate sibling is itself a cross-cut clause subtree; preserve both left and right source masks.
- **LSPV-3:** formulate a typed exact optimizer for two-or-more post-cut Resolution nodes before AND3, with AND premises and no implicit weakening.
- **LSPV-2/LSPV-4:** periodic critique only. Do not infer a Route-A all-input same-machine contraction from this finite structural obstruction.

## Exact remaining gap

Construct or exclude cross-cut sibling subtrees and paths with at least two further strict Resolution nodes before the required AND3; then treat all 36-node topologies. Full historical all-rule asymptotic hardness and noncircular B3 remain OPEN.

Full report: `research/main/2026-11-06_1148_MAIN_SIDE_LOCAL_SECOND_RESOLUTION_BLOCK_REFEREE392.md`.
