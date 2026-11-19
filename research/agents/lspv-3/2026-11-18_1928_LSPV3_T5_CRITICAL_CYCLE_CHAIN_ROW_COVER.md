# LSPV-3: growing intrinsic-critical T5 family with unbounded essential row covers

**November 18, 2026, 19:28 PST. PROVED/RESTRICTED theorem; COMPUTATIONAL independent replay; unrestricted SAT/UNSAT lower bounds OPEN. P versus NP OPEN.**

## Candidate and falsifiers

The prior four-path intersection-basis theorem applies to internally disjoint paths between a *single pair* of terminals. Candidate: no analogous constant-sized path-block obstruction cover exists across multiple interacting terminal pairs, even for connected edge-minimal T5-UNSAT graphs. Yet global GF(5) cycle reasoning can give a short source-bound negative explanation and every edge deletion can have an easily constructed SAT witness.

Falsifiers: an incorrect path difference set; closure allowing the forced cycle difference; any original-edge deletion remaining UNSAT; or any designated terminal row with more than one refutable path. All were tested on nine exact sources.

## Symbolic theorem

Fix T5 colors Z5 and R(a,b) iff (b-a) mod 5 is in {1,3}. A traversed path word W of length L with r backward arcs allows S(W)={L+r+2j mod 5:0<=j<=L}. In particular S(F)={1,3}, S(FBB)={0,1,2,4}, so the intersection of the direct F and the three-edge FBB paths between the same terminals is precisely {1}.

For each t>=2 construct terminals u_0,...,u_t. Between every u_i and u_(i+1) add a direct F arc and an internally disjoint three-edge FBB path (two fresh private vertices). Write d=-t mod5. Add a closing u_t-to-u_0 path W_t, where W_t=BB if d=0, and otherwise W_t=B^(d-1)F^(4-d), a three-edge word. When d!=0, S(W_t)=Z5\{d}; when d=0, S(BB)={1,3,4}, which excludes d and includes both d+1 and d-2. Call the resulting original directed graph H_t.

**Theorem (proved for all t>=2).** H_t is connected and edge-minimal UNSAT. It has B=2t+1 original path constraints, n=3t+L vertices and m=4t+L arcs, with L=2 when t divisible by five and L=3 otherwise. Every individual two-terminal path support is nonempty; every direct/FBB link intersection is {1}. For the complete assignment domain of its terminal variables, every path-only refutable-block cover must use all B paths. There are B explicitly constructible terminal rows z_p for which p is the *unique* refutable path. This is a strict counterexample to extending the previous four-basis theorem beyond a single shared pair of terminals. Girth is at most four, so this is a tractable intrinsic-critical control, not a growing-girth hardness family.

**Proof.** Every link forces c(u_(i+1))-c(u_i)=1, hence the full chain forces c(u_0)-c(u_t)=d, excluded by closure W_t; UNSAT follows. For the designated direct F path of link i, choose its terminal difference 0 and all other link differences 1. Only that F path fails: FBB accepts 0 and closure accepts d+1. For designated FBB path i, choose its difference 3 and every other difference 1. Only that FBB path fails: F accepts 3 and closure accepts d-2. For designated closure W_t, choose all differences 1; only the closure fails. Fix c(u_0)=0 and cumulatively integrate differences to obtain actual z_p. Any original arc belongs to exactly one path p. Removing that arc breaks its path into endpoint-attached trees, which independently admit extensions from fixed terminal colors because each T5 color has both in- and out-neighbors. The other paths extend by construction; hence every H_t-e is SAT. As every p has a terminal row for which p alone fails, omitting p from a universal row-cover leaves that row uncovered. Thus B paths are necessary and sufficient. QED.

Despite this *linear* path-only cover size, one modular cycle argument involving t+1 constraints proves UNSAT, and all critical-deletion witnesses can be built with per-thread constant-size local extensions. A restricted deterministic source-bound specialist can validate a canonical H_t encoding, output the modular certificate for H_t, and reconstruct a coloring for a designated H_t-e; otherwise it returns UNKNOWN. An O(N polylog N) bit-time, O(log N)-writable-bit streamed implementation follows from canonical sequential validation and constant-size per-thread coloring; the executed Python script instead constructs arrays and uses O(N) working memory. Source validation, full original-vertex output, and matching the designated missing edge are not free.

## Row specialist, correct paths and the all-CNF barrier

For explicitly enumerated shared rows Z and blocks F_i(z,x_i) with disjoint private variables, put C_i={z:F_i(z,.) is UNSAT}. A negative obstruction cover needs Z=union_i C_i, with source-bound verification for each claimed negative membership or a sound symbolic proof of the covered row subset. A SAT certificate needs ONE common z and ALL B private witnesses. A sound incomplete negative specialist returns UNSAT(certificate) or UNKNOWN, never SAT on UNKNOWN. A free correct polarity bit is answer advice, not a uniform decision algorithm.

A supplied k-bit correct path and a *verified* correct path are separate hypotheses. Every wrong path must return UNKNOWN rather than a false SAT/UNSAT verdict. A read-only path needs charged accesses/replay; guessed path bits require consistent replay/storage; deterministic enumeration can cost 2^k full verifications; an alternating strategy must encode or charge all universally quantified branches, not only a realized existential trace. A hypothetical polynomially bounded, sound, deterministic-verifiable UNSAT path certificate for every arbitrary UNSAT CNF would imply UNSAT in NP, hence NP=coNP (Cook-Reckhow). This remains conditional and unproved.

For R<=N^.195 explicit rows, B<=N^.65 blocks, private size<=N^.35, naive all-row/all-block time given local m^a complete decision is N^max(1,1.195,.845+.35a)+o(1). The 1.33 target needs a<=97/70 and a charged transformation; square-root space with local m^b requires b<=10/7 plus controlled persistent buffers. A generic SAT-in-P hypothesis supplies no known local exponent. The Fortnow-van Melkebeek 2000 deterministic random-access tradeoff has positive exclusion b<((a+2)/a^2-a)/2, equal to b<0.2762629 at a=1.33, NOT b=0.5. The FLMV JACM 2005 co-nondeterministic threshold c<sqrt(2), and modern small-space c<2cos(pi/7) results, require their exact full-language model and restricted space regimes, and do not imply promised-SAT witness or UNSAT certificate bounds for this family.

## Executed evidence

A full CPython standard-library generator verified every endpoint support by independent interior-color enumeration, every distinguishing row, and a complete retained-arc coloring for **each of all 300 single-arc deletions** of nine tested graphs with t=2,3,4,5,6,7,10,12,20. 21,865 checks, zero failures. A second, shorter independent implementation replayed the same nine sizes and 300 critical deletions. H_2 has 9 vertices, 11 arcs and FIVE essential path blocks, unlike the prior two-terminal H9 example with FOUR. H_7 has 24 vertices, 31 arcs, and FIFTEEN essential paths.

Executed full source SHA256 6308cf13cbcfa50f81bf8b18486a3675062fc9facf9b0e7e48487f8c9c14f022; compact independent replay SHA256 be3f7281a2655c6b150b7e940bf979fad6354607c8600eedd81af1992aaae05c; full raw JSON SHA256 d7a39230091d1821c03b017a841482d063ff77df86d07efca29c0f5f3f93a7e7. Detailed original-arc witnesses, canonical T5 H_2 and H_7 source files and complete reproducible code are retained in the local reproduction package. No repository-wide preflight, LaTeX compilation or independent external referee review was performed.

Original relevant work: research/agents/lspv-3/2026-11-18_1822_LSPV3_REUSABLE_T5_OBSTRUCTION_COVERS.md; research/agents/tmr-2/2026-11-18_1412_TMR2_T5_CYCLE_SYNDROME093.md. The exact GF(5) cycle representation is prior work; the scalable intrinsic-critical multi-terminal family and necessity of all 2t+1 source-path references are the new construction.

**NEXT:** obtain source-uniform symbolic negative cover extraction beyond this tractable canonical family, especially growing-girth critical T5 deletions and arbitrary-CNF blocks, with complete negative validation and discovery costs. P versus NP OPEN.

## Primary sources
1. Fortnow and van Melkebeek, DIMACS TR 2000-06: https://archive.dimacs.rutgers.edu/TechnicalReports/abstracts/2000/2000-06.html
2. Fortnow, Lipton, van Melkebeek, Viglas, JACM 52(6), 2005: https://doi.org/10.1145/1101821.1101822
3. Williams, Computational Complexity 15, 2006: https://doi.org/10.1007/s00037-007-0221-1
4. Buss and Williams, Computational Complexity 24, 2015: https://doi.org/10.1007/s00037-015-0104-9
5. Cook and Reckhow, JSL 44, 1979: https://doi.org/10.2307/2273702
