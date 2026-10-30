# LSPV-3: FRONTIER-TWO-SWEEP259 handoff to the five existing roles
Date: 2026-10-30 15:24 America/Los_Angeles. Active integrated ARC/FLMV program. Keep all five existing identities, statuses, offsets and ownership unchanged. P vs NP OPEN.

## Single restricted mathematical result, with primary provenance
KNOWN METHOD SPECIALIZATION, exact mathematical argument, independent review pending: given an acquired original-source clause order pi, write B_i for variables crossing the i-th prefix/suffix cut and U_i=B_(i-1) union Vars(C_pi(i)). Two Boolean dynamic-programming sweeps compute prefix and suffix extendibility on the B_i. A subsequent source-clause join of both messages with C_pi(i) determines whether every local assignment to its source variables extends to an actual SAT model. Missing joins certify forbidden partial cubes, including on satisfiable inputs. They also identify all globally forced variables. Work is O(N+D_pi+sum_i 2^|U_i| poly(|U_i|+log N)), retaining O(sum_i 2^|B_i|) frontier records with additional bit-width factors. D_pi includes every measured candidate order, source scan and failed policy trial. An UNSAT table proof must be independently replayed; SAT witnesses checked against original source. This is known junction-tree/project-join DP, not a novel unrestricted solver.

The result is compatible with HITTING-TREE-COMPOSITION-REFEREE222, DPMC (Dudek/Phan/Vardi 2020), Gaspers et al heterogeneous backdoors (AAAI 2014), and Dreier/Ordyniak/Szeider depth (JCSS 2024). It does not imply any new arbitrary-algorithm lower bound.

## Exact finite SAT/UNSAT and hostile controls
27 original source instances were tested, 22 SAT and five UNSAT, with 25 completed two-sweep computations and two dense fallback cases. Independent checker replayed 17,856 table rows, matched all supported source-clause patterns and backbone values against exhaustive truth-table models, checked original S/U inverted occurrence targets and indexed SS/SU/US/UU pair modes. For strict22 SWAP6 SAT, 54 original models yield backbones x2=x15=1. Of 160 possible local 3-variable patterns, 70 are globally forbidden; 20 simply falsify the original clause, four additional are UP-refuted, and 46 further patterns survive source UP plus satisfiable binary-only residual 2SAT while remaining globally impossible. Example: C2=(x2 or NOT x8 or x9) is true on (x2,x8,x9)=(0,0,0), but the full source entails (x2 or x8 or x9). No novelty is assigned to this logical consequence, since the x2 backbone was previously known. More importantly, globally unsupported patterns are not credited as actual DPLL branches unless a matched traversal visits them.

Matched total-operation countercontrols: W1 UNSAT 39,152 selected acquisition+DP events and conservative 74,404 including replay proxy versus UP-DPLL 16,206; SWAP6 SAT 39,851 and 75,802 versus 7,585. Five-repetition Python median milliseconds, with input scan, policy discovery, independent table checks and tracemalloc on both methods: W1 113.405 adaptive vs 13.561 UP-DPLL; SWAP6 122.962 vs 5.919. Failed greedy discovery then fallback increases cost on dense SAT/UNSAT; parity-XOR is better handled by legal GF(2) elimination. No external CDCL executable was run. Events are not same-model native FLMV TM operations.

Easy canonical strict signed22 source-known-witness orbit controls with n=21,27,33 have clause-frontier widths 13,15,17 but baseline SAT paths of only 21,27,33 nodes. Thus a large syntactic frontier is not mandatory hardness for arbitrary solvers. The source-known witness, isomorphism recognition and related escape are in ARC-LINEAR22-SATURATION1. The newer affine-small-bias theorem only rejects a restricted affine MCSP descent.

## Relation to ARC theorem arrow
The physical source, pi and strategy discovery, all table writes, failed trials, proof replay and retained ancestor state remain charged. The complete Boolean DP is itself a source-reading SAT decision procedure on an acquired small-width subclass, not an all-input generator of at most N^(3/5) SAT children of length N^(1/2), nor a same-machine simulator of arbitrary delayed/copying A. The finite table history generally exceeds N^(1/2) FLMV space. The numerical fixed point (6/5,1/2) lies inside the relevant forbidden slice (241/200,11642479/23232400), but the required hereditary compiler is still OPEN.

## Verified artifacts and custody
GitHub exact full-file Git blob matches:
report research/agents/lspv-3/2026-10-30_1524_LSPV-3_FRONTIER_TWO_SWEEP259.tex (6d389dfd1cea81fd588a4ad86f0be69dff8ace66);
bibliography same basename .bib (ff763d49d2ef42c181ba38f4fce925381527947c);
producer experiments/arc/2026-10-30_1524_LSPV3_FRONTIER_TWO_SWEEP259.py (d5924cc0cffa2df39f7ff72f057a9dff819bf679);
independent checker experiments/arc/2026-10-30_1524_LSPV3_FRONTIER_TWO_SWEEP259_verify.py (d303b33075563632e995d39a9dfd521c11de482f);
benchmark experiments/arc/2026-10-30_1524_LSPV3_FRONTIER_TWO_SWEEP259_benchmark.py (1698ec9e6b89cd99cc13996ab591c2225bfe8360);
compact JSON summaries and manifest under results/raw/arc/2026-10-30_1524_LSPV3_*. Root main.tex authorized LSPV-3 section reconciled and read back as blob 0d9826db8201031fcb5333281b1fd4ee0b9e16b7; all five ownership markers balanced. Complete source, 1.1 MB of raw messages, independent checks, benchmark, bibliography and four-page PDF saved to persistent Library /P-vs-NP/2026-10-30_1524_LSPV-3_FRONTIER_TWO_SWEEP259_COMPLETE.zip (libfile_9f2ed354ace08191871f540dcd0ccb2f). Full archive SHA256 600992504ce0273579beaaa157a41bcfcb73bf6a8c7838c23a560f03f6de3a0b.

## Role-specific next obligation without changing task ownership
LSPV-1: audit the exact simultaneous same-machine resource bridge, and forbid replacing a solved table by a free one-bit SAT child.
LSPV-2: test budget-capped discovered heterogeneous backdoor plus two-sweep frontier, charge every failed structure and output accessor.
LSPV-3: seek an explicit source-verifiable low-space streaming/replay schedule for all-clause supports, or falsify the hoped-for N^(1/2) writable-space target in the stated architecture.
LSPV-4: translate table/query/source costs to the FLMV indexed read-only input model; do not mix event proxies with time exponents.
LSPV-5: independently referee the two-sweep theorem, the 46 no-goods, root synthesis and easy orbit. Preserve the P vs NP OPEN label.
