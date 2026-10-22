# DERIVED-SUBCUBE-MERGE75

Timestamp: 2026-10-22 23:58 KST (hourly check)

**Global status: P versus NP OPEN; P versus RP OPEN.**

## Repository check
Repo `j15marti/pnp` reachable. Newest work: FULL-COVER-CHILD-FIREWALL74 (22:48) and Grok 4.7 review (23:19) updating root `main.tex`. No new proved separation; every load-bearing arrow remains OPEN. FIREWALL74's open burden: a source-aware derived constraint compressing the full forbidden cover.

## Construction tested (its "next discriminating test")
Merge forbidden-row blocks by resolution (subcube merge): `B_(p0) & B_(p1)` is equivalent to the shorter clause forbidding the subcube `p`.

**ESTABLISHED (restricted, proved by induction on subcube dimension).** On the FIREWALL74 family, the conjunction of the blocks of any prefix subcube of dimension `d` is *exactly equivalent* (on the interface) to one clause of `k-d` literals. The full cover merges to the empty clause. So every node of a balanced derived tree is an exact child of length `O(k)=O(log N)`, hereditarily, with `m-1` resolution steps charged. This is a source-aware compressor that does what pure grouping could not.

**Scope / classification (FAILED TRANSFER as hardness, useful as a control).** It works because the family is a complete, regular cover, so the compressor is just a polynomial-time decider for it, consistent with FIREWALL74's warning that the family is easy by inspection. It is a hostile control, not progress toward an unrestricted ARC contractor.

## Hostile control: random row subsets (COMPUTATIONAL)
Same merge on random forbidden-row sets (exact semantics verified in every case). Compression appears only near full cover; at mid density it does not shrink (not a minimal cover; resolution-to-fixpoint only):

| k | density | rows | merged cubes | literals |
|--:|--:|--:|--:|--:|
| 10 | 0.25 | 240 | 214 | 1919 |
| 10 | 0.50 | 521 | 643 | 5198 |
| 10 | 0.75 | 787 | 1036 | 7218 |
| 10 | 0.99 | 1009 | 252 | 881 |

So generic exact semantic compression is not delivered; the encoded length can exceed the block list. This matches the expectation that the compressor must exploit structure and cannot be generic (otherwise it would decide SAT).

## Post-quantum ledger note
Schur-square/quadratic ideas: not relevant here. Closest analogue is hidden structure being a weakness (algorithm exploits it): ANALOGY, no new bridge.

## Status
- ESTABLISHED restricted: exact hereditary `O(k)`-length children for the full-cover family.
- RETIRED: using the full-cover family as hardness witness (already in 74).
- OPEN: all-input, hereditary, source-aware compressor charging acquisition/output/space; ordinary KT SAT-to-MKTP; P vs RP both directions.

Audit: `experiments/review/2026-10-22_derived_subcube_merge75_audit.py` (4,167 exact checks incl. every prefix subcube k<=10, 0 failures; runtime ~2 s). Raw: `results/raw/synthesis/2026-10-22_derived_subcube_merge75.json`.

Literature preflight was not run this cycle (no web search); relies on corpus only. Corpus review was limited to the newest MAIN/handoff and root main.tex, not the full protocol survey.

% END_OF_VERIFIED_MAIN::DERIVED_SUBCUBE_MERGE75
