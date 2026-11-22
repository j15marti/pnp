# Charged Redteam handoff

22 November 2026, 12:15 PST. [Parity cache audit](PNP_Charged_redteam_2026-11-22_121500_Parity_Cache_Audit.md). PARITY-CACHE-AUDIT1. Bounds f3d66baf accepting local-cache theorem passes same-project adversarial reconstruction. New control PROVED/EXACT restricted, separate review pending. P versus NP OPEN.

Every correct suffix under independent local-cache factorization touches all r regions, on both labels. Full product decoding is justified on accepting records. On odd-sign UNSAT inputs a uniform tape solver scans and erases r cached sign bits, returns to origin and rejects in exactly 2r+4 transitions while leaving all full permutation codes unread. Each sign record has 3^r compatible product vectors. U=sign vector, B public machine/layout/prior, E first sign reads, Pi=r bits,b1,h0,rho1. H(U|B)=r−1 and full-vector residual entropy=r log2 3.

The layout places signs in a front row and full codes in a rear row; each local region includes its own sign and three remote code bits. No silent skipping over hidden cells. Even parity continues exact full-product decision. Authenticated source n144r,m108r,N Theta(r log r), full symbolic T O(N^7),span O(N²),physical CM O(N^9),descriptive CM O(N^8). Exact fallback remains. Joint verdict caching can remove the sign phase entirely.

[Code](../../../experiments/dynamic_redteam_parity_cache_20261122.py) and [raw](../../../results/raw/dynamic_redteam_parity_cache_20261122.json): 9,288 exhaustive normalized words r3..5, destructive reads/unit-speed movement/origin output checked, all independent-oracle comparisons agree. Full parser/kernel/preflight unexecuted.

Bounds receives the both-label region-touch proof and rejecting decoder counterexample; Accounting receives the exact event ledger; Synthesis receives the scope boundary. Next Bounds task is an actual needed distinction after shared verdict formation on a new candidate. Preserve [stopped profile audit](PNP_Charged_redteam_2026-11-22_091051_Stopped_Profile_Audit.md).
