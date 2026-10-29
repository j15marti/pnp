# LSPV-4 ONE-MODULE-PARETO230 | 2026-10-29 16:04 America/Los_Angeles

**PROVED/EXACT, restricted (independent referee pending).** For each integer r>=2, define the connected proper signed exact-(2,2)-3CNF F_r on a_i,u_i,v_i (indices mod r), with clauses (a_i OR u_i OR v_i), (a_i OR u_(i+1) OR v_i), (NOT a_i OR NOT u_i OR NOT v_i), (NOT a_i OR NOT u_(i+1) OR NOT v_i). Here n=3r,m=4r. For any nonempty Y subset of the a_i of size b, the remaining private variables form one connected module, and the **minimum residual syntactic hitting size** is q=r-b. Proof: the 4(r-b) clauses not touching Y each require a hit, every variable occurs at most four times, and all unpinned a_i are a hitting set. Hence b+q=n/3 for every integer b in [1,r] on one source family. For EVERY assignment to Y, u=1 and v=0 extend to a satisfying assignment, so the entire exact projected boundary relation is constant TRUE.

**Crucial semantic condition:** residual B hits only clauses *avoiding Y*. At b=r,q=0, there are private u,v variables but no private-only clauses. A grammar demanding an internally owned clause or requiring B to hit all boundary-touching clauses excludes that endpoint.

**Static curve versus real machine:** the earlier multi-module inequality n<=3b+12bq produces only permitted proxy coordinates (t=b+q,s_table=b). At n=1200 its minimum integer t=20 occurs at b=9,10,11, with b=9 uniquely Pareto optimal among the tied points; equality t=s first occurs at permitted b=400,q=0. On our SAME 1200-variable F_400, realized q=400-b, so t_one=400 for all b, while s_table=b. Therefore (400,400) is a realized proxy equality but dominated by (400,1) in those OPTIONAL coordinates. Neither curve is a mandatory SAT time-space lower bound.

**Constructive hostile control:** authenticating the strict recognizable F_r grammar and writing the witness a_i=0,u_i=1,v_i=0 uses conservative O(N polylog N) time, O(log N) extra writable bits on fixed-k sequential read-only-input multitape TM and indexed bit-cost RAM; one-tape simulation O(N^2 polylog N) time, O(N) total footprint incl input. A fixed universal machine has polynomial simulation, no claimed exponent. Materialized table storage 2^b is optional; streaming may avoid it, and the exact TRUE relation is constant. The family is entirely SAT. A uniform total solver can recognize it and fall back to DPLL outside, without an answer-class bit and without a polynomial all-input guarantee.

**COMPUTATIONAL:** self-contained reproducibility source checked r=2,3,4,10,100,400,1000; all 25 nonempty boundary subsets for r<=4 and all 114 boundary assignments; all 46,656 balanced signed variants on r=2 scopes were SAT; source at r=400 is exactly 25,188 unpadded ASCII bytes. These finite controls do not certify unrestricted SAT. No Coq kernel verification.

**Source precedence:** LSPV-5 STATIC-PROXY-PARETO-REFEREE206 Git blob 1b1d650fa617 already proves the relaxed convexity, discrete record frontier, another q=0 realization, and streaming-space firewall. LSPV-2 REALIZABLE-TRANSFER-FRONTIER233 blob 303cd6aee6 gives a different k>=2 family with b=2h,q=a-1,n=3ah and constant-size exact message. The additional claim here is the full tight one-module line on a single formula family, including all-boundary TRUE.

**To LSPV-1:** this is a countercontrol for transfer from syntactic hitting mass 2^(b+q) to mandatory SAT time. Projected interfaces can be constant even on a tight syntactic line.

**To LSPV-5:** preserve the full canonical main.tex, reconcile only the owned specialist region, verify all ownership pairs and P-versus-NP OPEN. Authenticate the q=0 residual hitting convention before quoting the endpoint.

**Next lemma:** For k>=2 modules, prove a realizable envelope approaching the static multi-module n<=3b+12bq constraint under exact ownership and boundary conventions, or establish a stronger realizability inequality. Charge discovery and machine-native processing.

P=NP and P!=NP remain OPEN. No tasks or schedules modified.
