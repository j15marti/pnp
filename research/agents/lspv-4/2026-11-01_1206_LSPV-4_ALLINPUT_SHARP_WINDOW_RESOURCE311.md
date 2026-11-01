# LSPV-4 ALLINPUT-SHARP-WINDOW-RESOURCE311
**2026-11-01 12:06 PST. PROVED/EXACT restricted sharpening of prior LSPV-5 theorem (independent external review pending); computational no-producer-import controls; universal SAT/ARC and P versus NP OPEN.**

## Precise incremental result and preflight duplication
The user seeks representation-independent SAT decision **WORK**, not recoverable assignments, injective pin keys, or large syntactic-state counts. The sole NP-complete target remains all valid duplicate-free proper Döcker monotone 3-SAT-(2,2) originals; malformed strings reject, while pinned residuals may be noncanonical. Read the 01:48 five-role handoff and the 01:44 saturated-cycle affine theorem first, then decision-only directive, issue #3, AGENTS/CODEX/pnp-research and latest role reports.

**Priority duplication:** LSPV-4 ORDERED-WORK309 established the bigram collision. LSPV-5 **FIXED-WINDOW-HISTOGRAM-REFEREE271**, published 11:48 PST BEFORE this run, already established failure of every fixed profile-factor window histogram, with guaranteed matching windows through length k+2 for k inserted filler blocks, and four-bit Boolean streaming. LSPV-4 FULL-PAYLOAD-VALID-NEIGHBOR310, published 11:36 PST, already proved the stronger strict binary-grammar accepting-run floor **N-O(log N)**, and independently replayed valid U198 UNSAT and V198 SAT controls. These claims are **PRIOR WORK, NOT NOVELTY HERE.**

**New narrower increment:** For the same authenticated padding family, the *exact* first discriminating cyclic profile-window length is **2k+3**. Hence the two opposing inputs match every window length **through 2k+2**, improving the prior k+2 guaranteed radius by k for k>0. We also derive the complete exact positive-model-count scaling **14400·3^(6k)** per padded period, rather than only the decision-support mask. No all-input hardness inference follows.

## Source-authenticated original and four local matrices
Use F9 positive supports (156),(238),(135),(469),(247),(789), negative supports -(468),-(167),-(234),-(358),-(129),-(579). G_t is the cyclic t-copy splice replacing the x5 occurrence in the first positive clause of block i by x5 of block i+1 modulo t. This preserves three distinct same-sign literals per original clause, distinct clauses, exactly two positive and negative occurrences for every variable, and source connectedness. Therefore G_t is a **valid canonical original** with n=9t and m=12t.

The local source variables are x1..x9, with boundary bits a_i=x5_i and a_(i+1)=x5_(i+1), and eight private bits. Exhaustive original-clause enumeration over all 4 boundary choices and 2^8 private assignments yields the nonnegative exact completion matrices:
A pins {x2=1,x6=0,x7=1,x9=1}: [[0,2],[0,0]];
B pins {x1=0,x3=0,x6=0}: [[0,0],[0,10]];
C pins {x4=0,x6=0}: [[3,9],[0,3]];
D pins {x1=0,x3=0}: [[0,0],[8,18]].
The unconstrained matrix is [[34,47],[23,36]]. SAT/UNSAT are labels of different coherent **residuals of the SAME canonical G_t**, not opposite untouched roots.

## Theorem: SHARP cyclic factor deck matching and exact model counts
Let S=(A,B,C,B,D,C) and U=(A,B,D,C,B,C). Their complete cyclic ordered bigram multisets coincide. For integers k>=0 and q>=1 define h_k(X)=X C^k and S_(k,q)=h_k(S)^q, U_(k,q)=h_k(U)^q. Both are coherent original-source pin configurations of exactly the **same** connected canonical G_t where t=6q(k+1).

**Exact restricted theorem:** For every k,q and every 1<=r<=2k+2 the cyclic ordered length-r profile-window histograms agree. At r=2k+3 they differ. Nevertheless
```
#SAT(G_t | S_(k,q)) = (14400 * 3^(6k))^q  > 0
#SAT(G_t | U_(k,q)) = 0.
```

**Proof of equal histograms:** Put L=k+1. Original letters occur only at positions divisible by L, with filler C at all other positions. Every length-r window for r<=2L sees at most two original-letter positions, and if two, they correspond to adjacent base letters. Their values and starting phase determine the window. Equal cyclic unigram and bigram counts of S and U thus give equal histograms at every r<=2L, and q repetitions multiply counts by q. This holds even when an original letter is itself C, because the partition tracks source-symbol positions, not decoded characters.

**Proof of sharp difference:** The window A C^k B C^k C of length 2L+1 occurs in S_(k,q), starting at the unique A of each base period. U instead starts A C^k B C^k D. Since no filler or other profile supplies A, that window never occurs in U_(k,q). Consequently 2k+3 is the **first** distinguishing radius. This sharp bound is the incremental theorem beyond the earlier LSPV-5 radius k+2.

**Exact multiplication proof:** Write A=2E01, B=10E11, C=3[[1,3],[0,1]], D=[[0,0],[8,18]]. Then C^k=3^k[[1,3k],[0,1]], A C^k=3^k A, B C^r B=10·3^r B, A B=10 A and tr(A D C^r)=16·3^r. These identities give the one-period SAT product P_S(k)=[[14400·3^(6k),b_k],[0,0]]. The UNSAT product P_U(k) has zero first column from the final B C^(2k+1) and zero second row from leading A; it is strictly upper triangular, with P_U(k)^2=0. Trace composition over q periods gives the displayed #SAT formulas. Every term counts original-source extensions exactly once by the cyclic x5 boundary word.

Theorem is about source-authenticated **restricted pinned residuals**. It falsifies only the adequacy of fixed profile-window histograms; it does not imply high necessary work, since the ordered transfer has small width.

## Decision-only quotient, grammar and native indexed-machine firewall
**KNOWN from LSPV-5 and LSPV-3:** For nonnegative matrices, the entrywise positivity map is a semiring homomorphism into Boolean matrices. A four-bit 2×2 Boolean product suffices to DECIDE existence of an extension once authenticated ordered profiles have been acquired. No assignment reconstruction or #SAT integer is required. Recognizing the family, discovering pins/profile supports, reading original clause bits, proving exact compatibility, and retaining source order **must all be paid**.

**Independently corroborated, not newly discovered:** Under this run's strict ASCII canonical header/decimal-clause encoding, each ASCII byte has one bit flip that makes the entire source malformed, so a YES-run must read at least N/8 pivotal source bits. The *earlier stronger* LSPV-4 FULL-PAYLOAD310 proves N-O(log N) bit reads in its fixed-width gamma grammar for ALL valid SAT originals. Neither forces superlinear SAT time or writable space. Malformed versus valid UNSAT are both NO, so that binary-acceptance pivot proof is YES-side only.

**Actual FLMV model, no fabricated timing:** The source is a read-only bit tape with an index tape. The input/output tapes are exempt from its workspace accounting, but input reads, index-cell writes/erasure, head moves, address arithmetic, output writes, child translations, Gaussian/matroid proof memory, policy discovery/failed routes, caches/ancestor retention and guest DELAY/COPY/RECOMP are charged. Indexed moves can atomically clear index contents, so whole-index XOR is not a one-bit-per-step lower bound. This experiment measured source-clause and DPLL logical operations, NOT complete native FLMV TM steps.

Honest all-input recursion must charge
```
T(z) <= C_grammar/source/index/head(z)
      + SUM_attempted_policy C_acquire/select/switch/failed/check(z,pi)
      + C_GE/matroid/proof/cache/replay(z)
      + SUM_evaluated_children [C_encode/bit/guest(z,y) + T(y)].
```
Peak space is the maximum **simultaneous** combined live writable/index/guest/ancestor/matrix/proof/cache/output-staging occupancy. Free-variable count decreases under exact Shannon fallback, proving termination but only an exponential worst-case aggregate-work bound; signed delta may increase.

**Exact FLMV Theorem 5.7 rational check:** d*(6/5)=23/45 and d*(241/200)=11642479/23232400, uniquely maximizing at k=2 with strict k>=4 tail exclusion. The original Fortnow et al. PDF Theorem 5.7 and indexed input machinery were reviewed, including screenshot of PDF p.17. A hypothetical target solver (time,space) exponents (6/5,1/2) needs a separately proved same-machine local-bit SAT-to-Döcker reduction of length exponent b and per-guest-bit cost exponent rho with (6/5)b+rho<241/200 and b/2<11642479/23232400; at rho=0, b<11642479/11616200≈1.00226227. Strict little-o space and paid setup/peak remain mandatory. NP-completeness does **not** provide the numeric transport, and arbitrary A->Phi(A) remains OPEN.

## Independent tests, literature and next falsifier
Stand-alone producer and **separate no-producer-import independent verifier passed 7,747 assertions**, re-enumerated all four source profiles and unconstrained F9, verified k=0,1,2,3,4,5,8,16 with matching windows through r=2k+2 (maximum checked r=34), first mismatch at r=2k+3, exact integer #SAT, Boolean decision, and q=2,3 repetitions for k<=4. Direct original-source UP-DPLL both-label controls at n=54,108,162 had SAT 12/18/24 nodes and **UNSAT one node** each; exact witnesses checked; thus this family is easy, not a hardness witness. F9 original has 70 models; 264 original SS/SU/US/UU pair-extreme compatibility cases, 512 complementary full assignments, all 12 source-clause S/U extremes and inversions, ten-step flip trail and changed clause IDs passed. Exactly 1001 separate single-bit invalid strict-ASCII byte controls passed. Earlier U198 UNSAT/V198 SAT remain inherited and **were not independently replayed in this run**.

Primary literature: Döcker arXiv:1912.08032; FLMV JACM 52(6), 2005 DOI 10.1145/1101821.1101822; Nisan decision trees DOI 10.1137/0220062; Slivovsky-Szeider SAT2020 DOI 10.1007/978-3-030-51825-7_19. Project GitHub searches included ORDERED-WORK309, LSPV-5 FIXED-WINDOW-HISTOGRAM271, FULL-PAYLOAD310 and prior connected G_t. Separately searched github.com/openai/math for SubexponentialSAT ProgramLogic. Web queries covered Döcker bounded-occurrence NP completeness, FLMV indexed Theorem 5.7, and CNF regular incidence compilers. No novelty inferred from absent matches. Only the **sharp window radius and #SAT scaling** are new relative to verified role reports.

Root main.tex exceeds 1MB: path-based fetch returned an EMPTY content field despite nonempty SHA. Its authenticated Git blob can be read through fetch_blob; any edit must preserve all unowned regions and use safe blob/tree/commit mechanics or remain PENDING. Preserve all five tasks/statuses/hourly Pacific staggers. **P versus NP OPEN.**

END_OF_LSPV4_REPORT::ALLINPUT_SHARP_WINDOW_RESOURCE311::P_VS_NP_OPEN
