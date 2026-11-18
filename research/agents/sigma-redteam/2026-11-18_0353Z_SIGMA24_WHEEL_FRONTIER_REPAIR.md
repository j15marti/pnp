# SIGMA REDTEAM24: Odd-wheel bounded-frontier repair
UTC 2026-11-18 03:53Z (Nov 17 19:53 PST). Status: PROVED/EXACT restricted constructive counteralgorithm and sample-cover proposition; COMPUTATIONAL 28,145 exact assertions with zero failures; unrestricted resource contraction and P != NP OPEN.

## PROPOSE
Falsify an inference from proper-subset SAT-query indistinguishability to a large *source-readable* interface. Compare identical non-affine wheel 3-coloring constraints under Sigma1, Sigma2 and challenge-local Sigma3; test bounded-frontier global DP; quantify sampled-query detection; audit random QBF, gate traces, padding, oracles, work-tape addressing, parent calls and recursive closure.

## SEARCH
Read current repository: SIGMA23 proper-subset firewall (2026-11-18_0155Z), AUTOENC-SIGMA3-1 source grammar and handoff (2026-11-18 05:01 KST), SIGMA3-AFFINEBASIS55 (05:31 KST), root proof1/proof2; recent commits through 84c8eee14d30e7ac5e0642a9cc5c49c1b046bc5f (03:42:50 UTC). Primary literature: Freuder 1990 https://www.aiinternational.org/Library/AAAI/1990/aaai90-001.php ; Schaefer 1978 https://doi.org/10.1145/800133.804350 ; Fortnow-Lipton-van Melkebeek-Viglas 2005 https://doi.org/10.1145/1101821.1101822 ; Williams STOC 2024 https://doi.org/10.1145/3618260.3649723 .

## RESULT A: exact source-reading constant-frontier repair
For odd-wheel W_r, odd r>=3, center c, rim v_0..v_(r-1), q=2r edge inequalities, define ordered bags B_i={c,v_0,v_i,v_(i+1)} for i=1..r-2. Every graph edge is covered and every vertex has consecutive bag occurrences; hence this gives an explicit path decomposition of width <=3 for every r. In standard legal two-bit color encoding, edge inequality has exactly 6 satisfying four-bit tuples, so the edge relation is genuinely non-affine.

Exact DP keeps only frontier colors (color(c),color(v_0),color(v_i)) in a table of at most 3^3=27 states. Enumerate next rim color, check new rim/spoke constraints, existentially forget previous rim vertex, and finally check closing rim edge. Inductive invariant: a frontier state exists iff it extends to a coloring of all edges processed so far. This decides the satisfiability of ANY chosen wheel-edge subset using O(r) color transitions and constant frontier storage when a canonical active-edge stream is supplied. Python proof-of-concept stores an explicit edge set and is not a native FLMV O(log r)-space implementation.

**Corrects overgeneralization, NOT predecessor theorem:** REDTEAM23's indistinguishability for an oracle receiving only proper-subset SAT bits is correct. But that result does not imply that every exact SOURCE-READING compiler must retain the 2(r+1) bits of a direct all-variable port. The wheel is UNSAT and every proper subset SAT, yet exact source-derived bounded-frontier DP detects contradiction efficiently. This does not invalidate REDTEAM20's expander incidence-port bound or prove general cheap semantic decomposition.

## RESULT B: quantitative sampled-subset blind spot
An odd wheel is edge-4-critical. A sampled-subset oracle that tests whether the set of t sampled edges admits ONE coloring accepts until all q distinct constraints have been seen. For t independent draws with replacement:
P_detect(q,t)= q! S(t,q)/q^t = q^(-t) SUM_{k=0}^q (-1)^k C(q,k)(q-k)^t.
At t<q this is zero; at t=q it is q!/q^q. For q=6, 1.5432%; q=10, 0.036288%; q=14, 0.00078454%. This obstruction concerns the sampled-subset SAT-status oracle, NOT source inspection or fixed committed global-coloring tests. Exact DP bypasses it.

## Sigma1/Sigma2/Sigma3
With center color x, shared rim z and edge challenge j:
  exists x,z AND_j E_j(x,z) = FALSE;
  exists x,z forall j E_j(x,z) = FALSE;
  exists x forall j exists z_j E_j(x,z_j) = TRUE.
Compact Skolem strategy: fix center x=2; for spoke j, rim all 0; for rim-edge j, assign its endpoints 0 and 1. No single globally coherent coloring exists. For polynomial q, this explicit-index restricted quantified pattern has polynomial Skolem table and is not shown Sigma3^P-hard. Private-witness AUTOENC theorem is unaffected.

## BUILD AND VERIFIED TEST
Pure stdlib auditor fixed seed=202611180353, rerun independently in local runtime: 28,145 assertions passed, 0 failures. r=3,5,7,9,11,21,101 bag and all single-edge deletion checks, exhaustively all proper subsets for r=3,5,7, 120 random proper subsets for each larger r, plus independent brute force for small r. 300 random graph coloring cross-checks. All 256 1x1y1z QBF truth tables checked with explicit Skolem strategy enumeration (32 adaptive-but-not-fixed); 3,500 random 1x2y1z Skolem controls. 1,400 random gate DAGs, 1,345 containing AND/OR/NAND operations; 99 UNSAT gate circuits falsely accepted under local re-witnessed traces; double-NOT equivalent-output checks. 16 Boolean oracles on four states: every oracle has a one-bit oracle-specific sound tag, but no oracle-independent one-bit tag works; 24 injective two-bit tags work uniformly. Coupon probabilities exact by integer inclusion-exclusion plus 60,000 sampled trials.

Local auditor SHA256: 7306b539d613ce6041b0be07d53dcee51a4857644637085452944d08a1af27ee
Local results JSON SHA256: 3cf4b5a5203c09a94b34a2e0dd772321446a9fc47174c1ca132e0503e4dc2df8
Local complete mathematical report SHA256: 7f35b1be37dba6ba387971f76c7a0ec3c0a4d85755580d2f2ab4dffb872a0904
ZIP integrity and checksums verified. Those local artifacts are NOT claimed to be uploaded to GitHub.

## TIME/SPACE/RAM, ORACLE AND CLOSURE AUDIT
Restricted AUTOENC recurrence K'<=max(27/25,29/50+K/2), L'<=max(1/2,L/2); fixed time exponent 29/25=1.16, strict contraction only K>1.16 for the promised source grammar. If N=n^1.01, guest contribution for K=3 is n^2.1008, not n^2.08. N^.08 tags times one N scan = N^1.08; repeated parent scan per N^.5 child costs N^1.58. Reached full-parent calls to padded A_D contribute N^D and invalidate a recurrence that omits them. R<=T for distinct memory accesses does not bound maximum addressed work-tape position. Indexed guest-bit decoding, uniform source parsing, physical FLMV model transfer, simultaneously live buffers, parent input length, strategy advice and HEREDITARY child grammar remain OPEN. Oracle-specific one-bit quotients are nonuniform across oracles; no relativization claim follows.

## HANDOFF
Use W_r as a required LOW-WIDTH negative control for any attempt to promote proper-subset oracle hardness into SAT computational hardness. Pair it with certified high-separator sparse non-affine instances, charging SOURCE-FOUND decomposition time, boundary encoding, guest bit access and recursive closure, and rule out affine or special-purpose polynomial solvers before claiming a lower bound. Do not claim P != NP.

VERIFICATION_SENTINEL_SIGMA24_20261118_0353Z_28145
