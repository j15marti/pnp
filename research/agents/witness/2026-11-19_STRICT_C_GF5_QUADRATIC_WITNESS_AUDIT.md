# STRICT-C-QF5-1: quadratic identity and SAT witness audit (2026-11-19)
Role: fresh-context SAT witness specialist. **PROVED/EXACT** for mathematical lemmas, **COMPUTATIONAL** for replays, **FALSIFIED** for unrestricted degree-two linearization, **OPEN** for general witness algorithms and P vs NP. Mathematical peer review pending.

Canonical R(a,b) iff (b-a)%5 in {1,3}; C(a,b,c) iff a,b,c form a directed triangle; exactly 30/125 allowed value triples, with three distinct variable names per clause.

## Theorem A: exact quadratic encoding (PROVED)
For all a,b,c in Z5,
C(a,b,c) iff [(a-b)^2+(b-c)^2+(c-a)^2] mod 5 = 1.
The five accepted unordered sets are {0,1,2}, {0,1,4}, {0,3,4}, {1,2,3}, {2,3,4}, which are translates of {0,1,2}; each has E=1. All five distinct transitive triples have E=4. Repeated-value triples yield 0,2,3, never 1. Exhaustive 125/125 verification independently confirms.

## Theorem B: private-head completion (PROVED)
For fixed u,v, let m=(u+v)/2 in F5. If u=v no h satisfies C(h,u,v). If (u-v)^2=1, exactly h=m-1,m+1 are valid; if (u-v)^2=4, exactly h=m is valid. Because E(h,u,v)=2(h-m)^2+4(u-v)^2. Verified all 25 ordered pairs. A private-head C clause projects exactly to u!=v, with constant-time reconstruction, but graph 5-colorability is still the general residual problem.

## Theorem C: the naive quadratic monomial linearization is always feasible (PROVED, invalid approach FALSIFIED)
Lift M_ij intended as x_i*x_j to independent symmetric linear variables, without rank or multiplicative consistency. Every strict C clause (i,j,k) becomes 2(M_ii+M_jj+M_kk)-2(M_ij+M_jk+M_ki)=1 over F5. The uniform assignment M_ii=1, M_ij=0 for i!=j satisfies *every* clause because 6=1 mod5. Thus quadratic linearization alone never rejects UNSAT, even the strict-C encoding of K6. This pseudo-moment matrix has rank n, while a real assignment produces xx^T of rank <=1. Stronger polynomial, higher-degree, and combinatorial methods are NOT excluded.

## Executed evidence
Standalone standard-library Python script: SHA256 d9a3ba94e39d6a47451e3aca955d1b89c43a9d16958f3b45143b87bddae0f588. PRNG seed 20261119. 125 local triples and 25 endpoint pairs checked; K6 private-head graph instance (21 variables/15 C clauses) has certified pigeonhole UNSAT and all 15 original-clause deletions with complete constructive SAT witnesses, checking 210 retained clauses. Rebuilt the canonical Mycielski^3(C5) and Mycielski^3(C7) source graphs and replayed 236+328=564 archived direct-C deletion colorings: 162,716 retained C clauses true and 564 deleted clauses false, with the quadratic predicate independently agreeing on each. **Replay is not acquisition cost.** The archive source fixture SHA256 is 6d9718bb8eff63a7b574eb166959ae40b4fdae704d06bd759cd2ac91e1e40f6e.

New complete deterministic strict-C DFS controls: 90 explicit n=9 instances with m cycling over {4,6,8,10,12}; 45 planted SAT, 45 uniform, results 65 SAT and 25 UNSAT (no UNKNOWN). 2,049 recursive calls, 43,385 clause checks, 1,274 two-known-equal early rejections. Full original-C verification of all SAT output vectors and complete DFS exhaustion of UNSAT instances. Every source clause/witness/check count in local JSON. Whole-run Python tracemalloc peak 8,290,322 bytes includes retained evidence ledger and is **not** a formal peak-live-workspace lower bound. All calls and verification are charged for these finite experiments; no oracle children.

Local reproducibility archive: T5C_GF5_Quadratic_Witness_Audit_20261119.zip. Raw JSON SHA256 b52329fee11f3d7ee5fb416f1cc52346062fb176bd640c5eb6f3ddcee2084f42. Only this report and handoff were published to GitHub; full code, ledger and compressed witnesses remain in the locally produced archive.

## Resource firewall
For R<=N^.195 explicit rows, B<=N^.65 blocks of private size <=N^.35, naive complete local decision m^a repeated over all RB gives N^(.845+.35a), so N^1.33 needs a<=97/70, before source/preprocessing/materialization/reconstruction, full witness output and concurrent space costs. Neither the quadratic identity nor cheap private-head projection gives a total generic child decider. A free correct polarity, a supplied successful k-bit path, or a resolution lower bound cannot substitute for a uniform deterministic execution bound.

Related work: Dell, Haak, Kallmayer, Wennmann, *Solving Polynomial Equations Over Finite Fields*, SODA 2025, DOI 10.1137/1.9781611978322.90, obtains randomized low-degree finite-field algorithms faster than exhaustive search, not a proved deterministic N^1.33 strict-C witness constructor with sqrt-space. Prior local source: t5_strict_research.pdf (sha256 c98555f85657395e450d832a0e4f9ef03ae3036a1389dbce250f6b5cfbf17633), and LSPV-3 strict-C criticality source report. The named strict research package zip was not independently recovered; no claim about its unseen contents.

**Next blocker:** test source-uniform mixed C/disequality separator elimination with full reconstruction, measure primal width and charged search on intrinsic critical deletions vs easy private-head graph constructions. Independent peer audit remains OPEN. P vs NP OPEN. No agent schedules or ownership changed.
