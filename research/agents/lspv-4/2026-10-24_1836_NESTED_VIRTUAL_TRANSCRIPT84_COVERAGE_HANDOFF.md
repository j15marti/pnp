# LSPV-4 NESTED-VIRTUAL-TRANSCRIPT84: verified additive ARC/FLMV handoff
Date: 2026-10-24 18:36 Asia/Seoul. P versus NP remains OPEN. Independent review pending.

## Core exact construction
For d>=16, M=8d, n=6, put all eight distinct three-literal signed clauses C_0,...,C_7 on x_1,x_2,x_3 at source positions p_r=rd. Fill every other slot with identical B=(y_1 OR y_2 OR y_3). Parent U has all eight and is UNSAT. Parent V replaces C_7 with C_0, is SAT with exactly 7 models. All record sizes and identifiers match.

Choose odd coprime 3<=K1<d and 2<=K2<K1. The source clause selected at depth two is
s2(j1,j2,i)=(j1*K1+((j2*K2+i) mod K1)) mod M.
An exact canonical child bit is calculated using ordinary child header (n=6,m=K2), width ceil(log2(64(n+K2+1))), and one indexed source record read. PROVED/EXACT in this named service model: O(log^2 N) elementary bit work, O(log N) writable bits per query, charged headers and addressing; no intermediate child buffer.

Every nested leaf contains at most one distinguished source position and has 49 models if a filler and a distinguished clause occur, otherwise 56. More strongly, all source cyclic contiguous windows of length <d have identical SAT and exact-model-count replies on U,V at the same window index. Therefore every deterministic count-only or SAT-only source-blind adaptive query policy has identical complete histories on U,V, regardless of number and choice of queries. One wrong parent decision is inevitable for that restricted oracle protocol. It does NOT rule out source reads, witness-returning oracles, direct solving or different decompositions. Exact distinct second-level bitstrings across all M*K1 index pairs: D_U=1+8K2 and D_V=1+7K2. This extends, not supersedes, CYCLIC82 and PERIODIC83.

## Adaptive policy and BIT-RESOURCE1
State S0: read source header and discover widths, no label advice. State S1: choose child bit service or eager child; charge every index update, source/workspace read/write, unchanged writes, actual flips separately, failed call, cache and peak live bits. Count-only adaptive history is uninformative. State S2: switch to a charged canonical source scan, collect eight-mask of observed signed patterns, and decide UNSAT iff all eight patterns occur. Grammar-specific cost O(N) bit work and O(log N) live bits. Off-grammar total exact fallback has no contracted worst-case bound. Source is read-only, index/work tape counted, as in FLMV. Cumulative bit-time from bit service is at most O(log^3 N) per bit.

## Conditional exponent ledger, not a theorem about E
If a separately proved correct all-input parent reconstruction uses Q1<=N^(a+o(1)), Q2<=L1^(a+o(1)), L1<=N^(lambda+o(1)), L2<=N^(lambda^2+o(1)), then faithful virtual solver calls could have
t2 <= max(r0,a*(1+lambda)+lambda^2*t), s2 <= max(p0,lambda^2*s)
with r0,p0 charging discovery, reconstruction, policy, reads, child headers, cache and live ancestors. At a=3/5, lambda=1/2 the solver term is .9+t/4. The tested leaf-answer-only reconstruction is FALSE, so there is no achieved E successor.

## Test provenance
Full local standard-library audit (current runtime only): /mnt/data/arc_nested_virtual84.py ; SHA256 eef2f790ed54488aa71d1f224f508c1dbdaaa2337c3bdd6ff7ba17dd76269448 ; raw /mnt/data/arc_nested_virtual84_results.json. 269,564 assertion-accounted checks, zero failures, deterministic seed 202610241836. All 52,608 two-level leaf pairs per label at d=16,32,64,128,256; small-case all-bit checks and large-case sampled bits, exact content orbits, matched SAT/UNSAT controls, 30-step adaptive transcripts per size; hostile affine, Horn, padded, random controls with exact fallbacks. Independent compact GitHub reproducer exercises exhaustive paired model counts and bit-service checks through d=128. Do not assume local paths are available to other scheduled agents.

## Source manifest and continuation
Inherited pinned audit: 3,532 files at commit 55a3fcc10f74419c9c3e1a577ed0f8ce83e2f640 hash/keyword searched previously, NOT all mathematically read. Current direct reads: AGENTS.md c5265db0, CODEX.md 754999f5, repo skill b8df83a7, main13.tex 87dbaad5, root main.tex 7ebe988e initial, main SMALL-INTERFACE-EXACT-JOIN64 and ROOT-LABEL-QUOTIENT85; latest ROLE2 CHILD-SCALE-PREFIX117/FALLBACK-PADDING118, ROLE1 VIRTUAL-FENCE124, ROLE3 STREAM-WITNESS-BITTIME86, ROLE4 PERIODIC83. Exact Drive URL reads: ARC existential-region document 1QirzuNPCG-CrE3EX6WweqsPdDbtoblCDEE4YI0HGyC0 and continuity log 1TselU5xLzVf7nbD2R0r-XZz_8t-S_WNrkiOZxNpbR5E, full text. Original HEREDITARY-SCOPED10 source code not found in accessible peer paths; continuity summary has nonpersistent /mnt/data references only. Broad Drive pagination and manual 3,532-file proofs remain unread. Primary FLMV PDF model section 2.1 and Cor 5.8 visually inspected; correct endpoint t<241/200, s<11642479/23232400. Retired 2*cos(pi/7) universal SAT endpoint stays retired.

FILLED restricted: two-level bit service and exact adaptive count transcript collision.
PARTIAL restricted: no required child materialization, conditional two-level exponent arithmetic.
FALSIFIED/RETIRED: isolated short-window SAT/count oracle replies determine parent label; changing selector indices forces distinct child formula content.
OPEN: all-input source-coherent parent-label reconstruction with same-machine strict time and space contraction, model transfer, universal compiler or cofinal existential ARC edge; hence P versus NP OPEN.

## Next peer experiment
Recover source bytes of original arc_hereditary_scoped10.py and inspect actual child serialization, width denominator, boundary sharing, two-level reconstruction, source read indices, caching/replay and peak live ancestors on connected high-width both-label controls. Do not upgrade restricted scoped-stream promises or fixed-orbit arithmetic to arbitrary SAT.
