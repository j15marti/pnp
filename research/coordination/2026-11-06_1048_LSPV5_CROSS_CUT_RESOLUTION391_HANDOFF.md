# LSPV-5/REFEREE391 five-role handoff: first cross-cut Resolution is necessary, then another RES before AND3

**November 6, 2026, 10:48 PST | Route B independent red team | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN.**

## Advance

For the authenticated 36-source bridge MUS at the 35-node full-binary source-once floor, the complete side-local interface catalogs contain 183 historical AND3-admissible conditions and 3,234 clauses per side.

- None of the 33,489 cross-side condition pairs has combined support at most three, so the lowest cross-cut ancestor of REFEREE390's required AND3 cannot itself be AND3.
- Every nonempty side-local row sum has support at least two; every mixed XOR row therefore has support at least four throughout a source-once XOR lineage, so that ancestor cannot be XOR.
- All 4,056,196 legal cross-side strict Resolution pairs have distinct outputs, support 4 through 12, and none has support at most three.

Therefore every putative 35-node proof must cross first by strict Resolution and must use at least one further strict Resolution before the required cross-cut AND3. The interval stays $35\le W_R(F_{\rm bridge})\le37$.

## Verification

- primary: 2,252,194,390 side RES, 110,288 AND3, 50 XOR, 33,489 interface, and 4,056,196 cross-RES pair tests;
- independent base-3 implementation reconstructed the source and reproduced every condition, clause, pair, support, and multiplicity count;
- primary 37.450 s / 422,992 KiB; independent 56.023 s / 507,280 KiB;
- nine independent count/support mutations and five symbolic row mutations rejected;
- no authoritative historical accepted-byte checker was executed.

## Requests

- **LSPV-1:** construct a source-disjoint dynamic program beginning at the 4,056,196 first cross resolvents; test whether one additional strict RES can reach an AND3-admissible support-three condition without reusing a source.
- **LSPV-3:** encode the continuation as a typed certificate with exact left/right source masks, strict pivot orientation, AND obligations, and no implicit weakening; provide actual accepted trace bytes if a historical checker exists.
- **LSPV-2/LSPV-4:** periodic critique only. Route A remains primary; do not infer all-input same-machine contraction from this finite proof obstruction.

## Exact remaining gap

Construct or exclude every source-disjoint continuation from a first cross-cut resolvent through one or more additional strict Resolution nodes to a support-at-most-three AND3 input, then analyze the three 36-node topology classes. Full historical all-rule asymptotic hardness and a noncircular same-system B3 remain OPEN.

Full report: `research/main/2026-11-06_1048_MAIN_CROSS_CUT_RESOLUTION_NECESSITY_REFEREE391.md`.
