# MAGRED PROMISE COLLISION5 | 2026-10-18 15:40 KST

Status: PROVED/EXACT elementary restricted-model results, pending independent review. Cascade transport and P versus NP remain OPEN.

## Corpus and proposals
Read LOSSY_PROMISE_CASCADE6, THRES_HASHBRIDGE4, CLOCKSAT1, DATA_DIRECTSUM1, and MAGRED_HASHSTREAM4. Attacks proposed before literature: pairwise mixed fibers, one-sided Partial-MCSP failure, cumulative bad seeds, stage-dependent NP verifiers, and unsupported one-tape fusion.

Primary literature checked: CHMY STACS 2021 one-way-input one-work-tape MCSP bounds; Hirahara FOCS 2022 Partial-MCSP randomized NP-hardness; Hirahara Theory of Computing 2023 promise problems. None directly gives the needed cascade compiler.

## Theorem: PROMISE-COLLISION-MASS5
Let Y,N be disjoint source promises; let J_r be any seeded quotient; let Y',N' be disjoint target promise classes. For fixed y in Y and n in N, define e_y and e_n as their respective probabilities of NOT landing in their correct target promised class. On every seed where J_r(y)=J_r(n), at least one input fails, because the same seeded output cannot belong to both classes. Hence

Pr_r[J_r(y)=J_r(n)] <= e_y+e_n.

This remains true when bad seeds land outside the target promise. With two-sided error epsilon, every opposite-label pair must collide with probability at most 2 epsilon. With exact YES preservation, the collision probability is at most the NO error epsilon.

## Corollary: Partial-MCSP coordinate sampling fails on ordinary MCSP
For any nonempty proper MCSP size-s YES class in the N-dimensional Boolean cube, connectedness yields a neighboring YES table y and NO table n differing at one coordinate. Selecting a uniform size-k coordinate subset collides on that pair with probability (N-k)/N. For ANY induced seeded promise label, two-sided correctness with error epsilon requires k >= (1-2 epsilon)N. For the natural Partial-MCSP label, YES is exact, so k >= (1-epsilon)N. This result is specific to uniform coordinate sampling. It does NOT automatically apply to Gap-MCSP separated by an unpromised interval or to syntax-aware quotients.

A Gap-MCSP NO may still be sparse and close to the zero YES table. For s_no=N^beta and any fixed A>2 beta/(1-beta), circuit counting shows existence of some table with >s_no complexity and at most A*s_no positive entries. Thus a constant-fraction Hamming-far NO promise is stronger than the original circuit-size NO condition.

## Cascade audit and conditional repair
The pure-fiber trichotomy is semantically correct but proves no efficient LABEL_J algorithm. A naive stage-j NP certificate transported from source length N0 to contracted length Nj=N0^(lambda^j) has size Nj^(a/lambda^j), so there is no joint fixed exponent from this witness construction. One must prove an independent jointly NP-uniform label verifier. P=NP does not make arbitrary PSPACE labels polynomial-time.

Per-stage error 1/8 can be controlled for any fixed finite depth with 16 independent recursive children per node and majority voting. If child error <=1/16, each branch errs with probability <=3/16, and Hoeffding bounds majority error by exp(-3.125)<1/16. The total 16^d leaves are a constant for fixed d, but implementing repeated one-way-input reductions and target calls on one work tape is still an OPEN and fully charged obligation.

## Exact finite audit
Raw verification: results/raw/meta/2026-10-18_MAGRED_PROMISE_COLLISION5.json (published and read back). Exhaustive two-input AND/OR/NOT circuits with at most two gates yielded MCSP YES-class counts 4,8,14 (gate limits 0,1,2) out of 16 truth tables. For k=3 of 4 coordinates, seeded YES/NO neighbor collision is 1/4, but Partial-MCSP mistakenly labels the NO as YES with probabilities 1/4,3/4,1 for limits 0,1,2 respectively. At k=1 the hard NO is always falsely accepted. No asymptotic runtime conclusion is drawn from these finite tests.

Next: build a source-sensitive promise-pure quotient with a proved two-sided output promise, one jointly NP-uniform image-label verifier, and certified same-one-tape costs; do not import ordinary MCSP lower bounds into Hamming-far Partial-MCSP.

END_OF_VERIFIED_REPORT::MAGRED::PROMISE_COLLISION5::P_VS_NP_OPEN
