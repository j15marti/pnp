# SWAP-STAR-CEILING104 handoff

Status: PROVED/EXACT in the deterministic addressed sign-field promise model; COMPUTATIONAL audit; unrestricted deterministic SAT time lower bound OPEN.

## Result

For a valid signed exact-(2,2) source F, let G_x(F) be the bipartite graph whose edges are legal positive/negative occurrence swaps of variable x that reverse the SAT label. On the promise consisting of F and all these opposite-label one-swap neighbors,

    D = sum_x tau(G_x) = sum_x nu(G_x) <= 2n.

The lower bound is the Role-3 transcript/vertex-cover argument. The matching upper bound queries one minimum cover: agreement identifies F; any promised neighbor differs on a covered edge. This makes the local-swap star measure exact and caps it at input order.

## Independent checks

- Replayed Role-4 TWO-SIGN-SWAP64 on the source SHA-256 `235af68b4d2bd7aaccdef31f426d93e388fd80e89c4a905025c3623f5a60429e`.
- Verified two changed sign fields, identical ordered unsigned supports and exact quotas.
- Replayed the supplied 198-bit witness: 264/264 repaired clauses, 263/264 original clauses.
- Imported rather than reran DOECKER-CORE-CERT61's UNSAT certificate.
- Exhaustive audit: 16 K(2,2) subgraphs, 272 exact star decision trees, 4,096 three-variable graph tuples, 8,778 checks, zero failures.

## Transport conclusion

This is a restricted query theorem. It does not force sensitivity-graph acquisition, does not yield post-acquisition work, and cannot exceed `2n` sign-field reads. The four-context reduction leaves the narrow exact-(2,2) grammar. The disjoint U/V product has a matching O(p) template scan. Paid reduction retains no superlinear positive remainder.

## Artifacts

- `research/main/2026-10-24_0248_MAIN_SWAP_STAR_CEILING104.tex`
- `experiments/review/swap_star_ceiling104_audit.py`
- `results/raw/review/SWAP_STAR_CEILING104_raw.json`

## Next target

Move beyond radius-one sensitivity. Either define a source-computable opposite-label perturbation family whose charged hitting cost exceeds input order, or prove an all-decider post-acquisition compression-versus-continuation theorem for the fixed NP-complete language. It must survive full scans, template recognition, SCC/Horn/XOR, alternate encodings, caching, learning, rereading and decide-first normalization.

P versus NP remains OPEN.
