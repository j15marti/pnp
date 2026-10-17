DUALTRACK-SHAREDRESERVOIR1 | 2026-10-17 12:51 KST | P versus NP OPEN.

PROPOSE before search: (A) solver-specific factored checkpoint extraction and exact gluing; (B) test whether the local 28-petal HUBSUNFLOWER49 trigger can be summed over overlapping hubs; (C) separate Liu exact-algorithm gains from arbitrary SAT lower bounds.

LITERATURE: Liu, ICALP 2018, doi:10.4230/LIPIcs.ICALP.2018.88, Algorithm 4 and Theorem 21; Fortnow et al., JACM 2005, doi:10.1145/1101821.1101822, Cor. 5.8. PROJECT: GLUECOVER1, AFFINEEPOCH1, SEMQUOTIENT38, BRIDGECOVER39, COMPOSEPOWER1, SYMPLECTICPATCH1, DISJPOWER40, GUARDSTAR46, SPREAD4-COV44 and latest HUBSUNFLOWER49.

SHAREDRESERVOIR1, PROVED/EXACT scoped, independent review pending. For integers q,p>=1, form q disjoint positive 3-clause hubs H_j and 3p disjoint positive leaf clauses A_i,B_i,C_i, add a fresh y_{ji} for every hub-petal pair, and add proper 3-clauses (h_j0 OR a_i0 OR y_ji) AND (b_i0 OR c_i0 OR NOT y_ji). There are 3q+9p+qp variables and q+3p+2qp clauses. Every mediator occurs twice, opposite signs; every selected chain projects to all 7 nonzero states (fix that chain and set all other chain bits to 1 and all y to 0). Elimination of y_ji yields the rank-4 chain relation H_j OR A_i OR B_i OR C_i on selected first literals. Every hub has p off-hub-disjoint petals, but two global petals intersect iff they have the same hub j or leaf-triplet i. Thus maximal vertex-disjoint rank-4 packing size is exactly min(q,p). Independent 10-petal bundles are at most min(q,floor(p/10)). Set p=28 and q->infinity: every hub triggers the local HUBSUNFLOWER49 condition, but globally only <=112 of q+84 chains can be covered in disjoint rank-4 blocks. The positive-density tensorization inference is FALSIFIED/RETIRED. This does not rule out overlap-aware covering gains; formula is trivially SAT.

COMPUTATIONAL: 10 parameter pairs, 3052 exact state-extension tests; properness, mediators and counts verified; brute-force matching on qp<=16. Code SHA256 7916a63e4e23698535bee26a0090d18771c4391181aacf12ae4879a3afe17637. Raw SHA256 c95d4a15db41b38d1459130624af55e29aaded7b99b6d95931a3d533859bba4e.

TRACK A OPEN: all-input solver-dependent, fully charged, recursively iterable SAT-child contraction into FLMV forbidden (6/5,1/2). Next: A-specific factored checkpoint acquisition with exact gluing and all reads charged.

TRACK B OPEN: integrate signed star/matching blocks into Liu Algorithm 4 with global overlap accounting and branch stop/overshoot. Next: an overlap-aware hub-petal shared-reservoir recurrence falsified against this construction.

RETIRED: timing/hash races, status-only oracle adaptivity, UWI separation-equivalent common-input obstruction, untransported proof-system lower bounds, expanded representation => runtime.

ROOT ISSUE: default main.tex has literal omitted-body placeholder. Verified full predecessor at commit 290c060b2ecfcc35056e533f911bcc30522d796b. Do not overwrite without verified full-body recovery.
END_DUALTRACK_SHAREDRESERVOIR1_STATUS