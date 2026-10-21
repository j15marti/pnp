# SOURCE-CUTSET22: exact source-level cutset on real WRAPPER root
Date: 2026-10-22 Asia/Seoul. Status: P vs RP OPEN, P vs NP OPEN.

## New source-grounded check
Directly read three originals:
- experiments/DOUBLE_WRAPPER_2026-10-07/example_dag.json (node0, blob 90fd76b813e6341d0a1c1b3a1dcfa620abefcbba)
- 2026-10-22_0448_MAIN_SOURCE_JOIN_COHERENCE56.md (92e9c1ee766db97bb3b53d1b1a8467d5a468e875)
- research/main/2026-10-22_0548_MAIN_SOURCE_CHANNEL_COMPLETENESS57.md (0ef1c430c219c5045446c70c70e14cc926ff4d57)

56/57 previously counted 1,948 source witnesses and identified a wrapper boundary of two, greedy clause frontier five, and 73 shared-source gates. Those are prior results, not rediscovered.

This run checked all 1+14+91 source subsets of cardinality 0,1,2 with deduplicated GYO hypergraph acyclicity reduction. Exactly one successful set: {x1,x2}. Conditioning on the pair leaves FOUR DISJOINT source components, each size three: {3,4,5}, {6,7,8}, {9,10,11}, {12,13,14}. This is a **source-level** decomposition certified for this finite original fixture; do not infer it automatically from the wrapper-DAG boundary.

Conditional three-variable block counts:
| x1x2 | B1 | B2 | B3 | B4 | product |
|---|---:|---:|---:|---:|---:|
| 00 | 3 | 4 | 5 | 6 | 360 |
| 01 | 4 | 4 | 3 | 6 | 288 |
| 10 | 5 | 4 | 6 | 5 | 600 |
| 11 | 7 | 5 | 5 | 4 | 700 |
Total 360+288+600+700=1,948, exactly matching exhaustive enumeration of all 2^14 inputs.

**Restricted theorem (established):** If a uniformly computable k-source cutset S leaves source-primal components B_j of size <=b, then #F=sum_{s in {0,1}^k} I_s prod_j #F_j|s. A direct uniform algorithm costs polynomial input handling plus 2^k sum_j 2^{|B_j|} local valuations (with arithmetic/access charged). Therefore k+b=O(log N) implies P *provided S itself is uniformly found in polynomial time*. For constant k, n^k candidate search is polynomial; for k=O(log n) naive discovery need not be. Known junction-tree counting extends this to bounded-arity alpha-acyclic residual factors; see Yannakakis 1981, Tarjan-Yannakakis 1984.

**d-DNNF certificate:** Four disjoint assignments to x1,x2; within each branch four disjoint-source blocks; within each block OR over complete accepted 3-bit cubes. Across the 16 block tables are 76 accepted rows. Each OR is deterministic, each AND is decomposable. This gives an exact polynomial-size representation for this fixture only.

**Circuit-SAT and honest gate access:** 14 primary NOT gates +40 OR +19 AND =73 fan-in <=2 gates; proper functional Tseitin 3CNF with a unique 3-variable anchor gadget has 90 variables, 213 proper three-literal clauses. Exactly one auxiliary extension for each satisfying primary assignment; 1,948 complete satisfying assignments. A uniform primary sample succeeds only 1,948/2^14=0.118896484375 (not RP for general SAT); guessing all primary+gate+anchor variables has probability 1948/2^90 approx 1.57e-24, a sampling artifact, not hardness. Source reads, trace evaluation and cutset discovery are charged, defeating digest-only q+h information claims when open gate/source access is allowed.

**Hostile control:** odd XOR cycles have locally consistent marginals but 0 global models; removing 1 source yields acyclic residual. Tested sizes 3..8, even cycles had 2 models. No recovery of global coherence from local marginals alone.

Finite standard-library Python audit: 65,578 assertion-accounted checks, zero failures. The script, DIMACS, 76-row d-DNNF certificate, raw results, coverage delta and SHA256 manifest exist in the :12 conversation's local package RP_SOURCE_CUTSET22_2026-10-22.zip; cross-runtime filesystem sharing is NOT assumed. No script publication claimed here.

## Direct handoff to :36 and :48
Compare this cutset-specific counter with the prior greedy source frontier of five. Obtain a *growing family* of executable WRAPPER instances and record whether a constant wrapper-DAG separator forces or fails to force small **source** cutsets; include hash/timer provenance, query transcript, and gate access charges. One easy 14-variable root cannot establish P=RP or P!=RP. RP separation requires a uniform one-sided RP recognizer for one L and impossibility of every deterministic polynomial decider.

Labels: ESTABLISHED restricted finite factorization and general cutset identity; CONDITIONAL transfer to growing WRAPPER; OPEN unrestricted P-vs-RP, P-vs-NP. No class separation claimed.
