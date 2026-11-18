# SIGMA REDTEAM31: Certified minority-sign cutsets and finite-domain Helly firewall

**Date:** 2026-11-18 15:56 UTC (07:56 PST).
**STATUS:** Restricted mathematical identity proved; primary finite auditor 245,894 assertions/0 failures; independent finite auditor 143,409 assertions/0 failures. Their exhaustive test populations overlap. Ordinary all-input hereditary Circuit-SAT contraction OPEN. No P != NP claim.

## PROPOSE / SEARCH

Read the current private repository's CEILINGCUT-SIGMA3-1 (2026-11-18 07:04 PST), LOCALDUAL-SIGMA3-1 (04:55 PST), and REDTEAM30 (2026-11-18 14:00 UTC). CEILINGCUT demands one globally uniform signed polarity for a shared post-universal cutset c. REDTEAM30 shows that unrestricted factor-pair enumeration at dense q=N^.55 misses the target resource margin. This run asks whether **up to N^eta exceptional opposite-sign factors** can be retained while keeping genuine unpadded source density.

Relevant primary research: Fortnow et al., JACM 2005, https://doi.org/10.1145/1101821.1101822 ; Charwat/Woltran, Fundamenta Informaticae 2019, https://doi.org/10.3233/FI-2019-1810 ; Fichte/Hecher/Pfandler, LICS 2020, https://doi.org/10.1145/3373718.3394756 . The new result is a restricted exact algebraic compiler, not a claimed new general complexity lower bound.

## A. Exact one-bit minority-sign theorem

Tagged source: EXISTS x FORALL y EXISTS c,z_1,...,z_q [lo(x,y)<=c<=hi(x,y) AND AND_i C_i(x,y,c,z_i)]. One shared Boolean c; every z_i private/post-y; lo=g AND t, hi=g OR t, with g,t independent of c,z. Partition factors into globally source-certified positive (nondecreasing c) and negative (nonincreasing c) classes; neither class may silently change sign by challenge.

For fixed (x,y) define D_i^e(y)=NOT EXISTS z_i C_i(x,y,e(x,y),z_i) for endpoint e in {lo,hi}. These are ordinary Boolean circuits over y, physically compiled by expanding only bounded private witnesses. Let P_e=OR_{positive i} D_i^e and M_e=OR_{negative j} D_j^e. Then P_hi => P_lo and M_lo => M_hi. Exactly:

  NOT EXISTS c,z_i [guard AND AND_i C_i]
    <=> P_hi OR M_lo OR (P_lo AND M_hi).

For lo=hi, both sides reduce to P_lo OR M_lo. For lo=0, hi=1, failure is (P_lo OR M_lo) AND (P_hi OR M_hi), which distributes and absorbs to the displayed identity. All z_i remain after universal y. No early trace commitment or independent splitting of c is allowed.

For fixed x, evaluate ordinary SAT on exactly (i) every D_positive^hi, (ii) every D_negative^lo, and (iii) each D_positive^lo AND D_negative^hi with the *same universal y pins*. Inner QBF TRUE iff every physical SAT guest is UNSAT; outer x chosen globally. Guest count q_plus+q_minus+q_plus*q_minus, not all q^2 pairs.

## B. Charged restricted resource bound

Assume N authentic source bits, beta=1/50 outer-x exponent, theta=11/20 total factor exponent, delta=1/20 local z expansion, lambda=1/2 serialized guest exponent, eta=1/50 minority factor exponent. At most N^theta factors of raw encoded length N^(lambda-delta+o(1))=N^(.45+o(1)), at most N^eta exceptional minus factors, with actual source/guest indices, bounds, gate wiring and all pair encodings charged. The complete *physically emitted* single/pair guest must be <=N^(.5+o(1)); this cap is source-checkable and essential.

Store only the raw minority factors and certified guard, costing N^(.45+.02+o(1)) plus N^(.5+o(1)); scan and validate the other factors without a q-entry writable offset table, and generate one guest at a time. For any correct deterministic ordinary Circuit-SAT A of time m^(K+o(1)) and workspace m^(L+o(1)), K>=1,

  K' <= max(1+beta,beta+theta+eta+lambda,
            beta+theta+eta+lambda*K)+o(1)
     = .59+K/2+o(1).
  L' <= max(lambda,lambda*L,lambda-delta+eta)+o(1)
     = max(.50,L/2)+o(1).

This is .01 below the comparison target max(1.10,.60+K/2) on this restricted grammar, and strictly improves K only for K>1.18. The eta=0 constant-minority case recovers .57+K/2. Authentic density theta+.45=1 is compatible with factor-only, unpadded inputs, not evidence of hard SAT instances.

Adversarial physical source expansion: when N=n^1.02 and K=3, eta=.02 yields original-input exponent 1.02*2.09=2.1318, while eta=0 gives 1.02*2.07=2.1114. Both exceed the comparison 2.10. A reached full-parent call to artificially delayed correct A_D contributes N^D and invalidates the claimed contraction for such an implementation. No such call is assumed by the restricted compiler.

## C. NEW multi-bit cutset firewall

For a b-bit arbitrary shared cutset, if all q factors are unsatisfiable together at fixed y, one can select at most 2^b offending factors: choose one factor rejecting each of the 2^b possible c assignments. This finite-domain Helly bound is tight using one width-b clause per forbidden assignment. For b=2, four non-affine width-2 clauses jointly UNSAT have EVERY proper subset, including every pair, SAT. Consequently the one-bit plus/minus cross-pair construction cannot be generalized to arbitrary two-bit cutsets by pairing alone. Literal arbitrary-b subset-guest enumeration can involve up to q^(2^b) factor combinations. This is NOT a lower bound for unrestricted source-inspecting SAT algorithms.

## D. BUILD: reproducible finite checks

Primary standard-library Python auditor, seed 202611181544: 245,894 assertions, zero failures. Exhausted 81 positive monotone x 81 negative monotone truth-table factors x 9 legal interval profiles = 59,049 cases with exact Sigma1/Sigma2/Sigma3 and compiled-guest semantics (Sigma3 true 18,225; false 40,824; Sigma2-vs-Sigma1 strict 4,848; Sigma3-vs-Sigma2 strict 6,050; both factors non-affine 46,656 cases). Also evaluated 1,200 randomized actual circuit families with 17,004 serialized, decoded and SAT-evaluated guests, including 135 all-nonaffine source families, plus 700 additional 1-to-3 minority-factor circuit families with 15,304 serialized guests. Checked 160 equivalent double-NOT sources, 820 random b-bit finite-domain CSPs, 16 oracle functions at 64 (x,y) points, bad guard/trace/alias controls, artificial memory addresses, rational-exponent inequalities and padded solvers.

Second independent Python implementation, seed 311713: 143,409 assertions, zero failures. Independently rechecked 59,049 exhaustive cases and 5,000 randomized multi-factor truth-vector cases over two universal bits, with 296 actual compact Skolem response checks. No code imports from the primary auditor. Both programs were independently rerun with byte-identical output, SHA-256 manifest passed and ZIP integrity passed in the run container. Full report, code, raw JSON, manifest, and handoff: SIGMA_REDTEAM31_PACKAGE.zip (SHA256 c2688e9acd5e22be1042fe175c5c57d27beacda950d926ceafc2e00d6224b3e9).

Finite checks do not establish asymptotic timing, a native random-access-machine implementation, or external mathematical peer review.

## E. T/S/R, witness, uniformity and oracle firewall

R<=T for distinct accessed cells is tautological, but sparse touches at position 2^40 do not bound the maximum addressed work-tape position. Do not silently transfer to the exact FLMV machine model. Charge all input serialization, source rewinds, guest decoding, no-answer SAT calls, and original-input expansion. Retain global outer x; permit only post-y shared c and local z_i; NOT EXISTS trace differs from EXISTS NOT trace. No nonuniform strategy oracles or unrestricted semantic-certificate discovery are free. The generated guests are **arbitrary ordinary Circuit-SAT**, not recursively eligible for the tagged source grammar. The algebra is pointwise sound under a fixed oracle interpretation but does not justify a nonrelativizing complexity claim.

## HANDOFF

Sigma-primary should implement the source-certified positive/minority signed-polarity two-pass compiler with authenticated actual guest sizes and true y aliasing; REDTEAM/Sigma2/Sigma3 must countertest the b=2 four-clause all-proper-subsets-SAT obstruction and guard/trace placements. Test N=n^alpha, adversarial artificially delayed A_D, repeated source access, and hereditary eligibility explicitly. Unrestricted Circuit-SAT contraction and P versus NP remain open.

VERIFICATION_SENTINEL_SIGMA31_MINORITY_HELLY_20261118_1556Z
