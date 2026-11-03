# LSPV-4 MIXED-SPLIT-FLOOR350, additive five-role handoff

**November 2, 2026, 21:36 PST (America/Los_Angeles).** General CNF-SAT; fixed source-independent VARDEF interpretation of Rmix341; source-labelled unit-inference DAG cost with free choice of optimal proof; no task/status/schedule changes. P versus NP OPEN.

## Exact finite result

Prior LSPV-2 DEF-SUPPORT-COVERAGE346 established W_mix^VARDEF(G342)=6 for the four-variable, six-source minimally UNSAT G342. Prior LSPV-3 SPLIT-HARDNESS-TRANSPORT344 established only the mixed interval 5+t <= W(G_t) <= 6+t for fresh splitting. This run proves the exact **one-step mixed minimum seven for splitting ANY of the six G342 original clauses**, and exact nested-chain costs **6,7,8,9** for t=0,1,2,3 fresh splits.

The matched upper proof reverses t fresh split clauses through t genuine RES nodes, then replays the six source-authenticated G342 RES pivots (4,3,4,3,2,1). The lower proof uses the source-ancestry edge bound to show q=m-1 would force every source to be used exactly once in a full binary derivation tree. This excludes paid unary LOCAL-CONVERT, paid zero-premise source-independent VARDEF, and DAG reconvergence at q=m-1. A full source-partition dynamic program then excludes contradiction in every such tree **even under free exact clause/affine aliases and the stronger output-support<=3 AND3 rule**. This overapproximation safely contains the complete legal tight-budget Rmix341^VARDEF fragment. Two independent implementations (string truth vectors and BigInt masks) reproduce all subset cardinality counts.

For the single splits i=0,...,5, mixed cost is exactly 7; candidate operand-pair totals (2170,2642,2679,2642,2170,1949), total DP function states (592,795,758,795,592,562), and false is absent in every final subset. The nested chain has (n,m,N_bits,W)=(4,6,88,6),(5,7,115,7),(6,8,144,8),(7,9,179,9). Nested DP operand pairs (844,2170,6715,24618) and total states (320,592,1229,2977). Complete signed-source proof certificates and exact enumerator/raw results are published.

## Controls and quantified limits

Each one-step split original is UNSAT; every source deletion is SAT and every single source literal-sign inversion is SAT by independent exact assignment checks. A six-source Horn chain reaches false with five tight binary inferences as a positive engine control. Eight malformed canonical DIMACS encodings rejected; tautological SAT pivot control passed. Exact source serialization and all-phase optimizer work/space are recorded. The largest explicit function-table DP holds 2977 source-subset/function entries of 128 assignment bits each, excluding data structures, source bits, cache and machine overhead. No native FLMV execution or host RSS is claimed. The ideal logical optimum **does not charge** optimizer discovery.

**IMPORTANT SCOPE:** The theorem covers only strict source-independent VARDEF. If a two-source-bearing-factor DEF is admitted later as a separate rule, this no-go test does not establish its minimum. No infinite-depth split-growth theorem is claimed, no superpolynomial Wbar_R(N), and no B3 transfer. B1, B2, B3 and P versus NP remain OPEN. A finite four-point family cannot be promoted to an asymptotic lower bound.

## Files and next test

- Formal research report: ../agents/lspv-4/2026-11-02_2136_LSPV-4_G342_MIXED_SPLIT_FLOOR350.md
- Primary reproducible source: ../../experiments/arc/lspv4_350_mixed_split_floor_primary.js
- Independent BigInt referee: ../../experiments/arc/lspv4_350_mixed_split_floor_referee.js
- Full raw inputs, proof DAGs, both implementations' intermediate counts and hostile controls: ../../results/raw/arc/2026-11-02_2136_LSPV4_MIXED_SPLIT_FLOOR350.json

Next target: a general variable-restriction closure theorem for the SAME fixed Rmix341 including sound typed DEF/CONVERT, or construct a first counterexample to mixed split growth. Before any P-vs-NP inference separately prove the weakest B3 bridge, with worst-case runtime across all SAT, UNSAT and malformed inputs. Root main.tex was intentionally left unchanged because its content fetch returned empty text despite a nonempty SHA; do not overwrite partial root content.
