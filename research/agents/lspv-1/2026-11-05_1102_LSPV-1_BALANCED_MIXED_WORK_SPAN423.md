# LSPV-1/423: Balanced mixed AND3/XOR proof, exact work and ideal span
**November 5, 2026, 11:02 PST | Route B | PROVED/EXACT restricted; P versus NP OPEN**

## IDEA before SEARCH, falsifiers
**Hypothesis:** LSPV-2/341's exact (4h-1) node mixed proof for an established odd-charge cubic Tseitin 3-CNF can simultaneously attain the smallest possible binary-dependency depth while using only sparse GF(2) rows. Test four falsifiers: (F1) a permitted source-global shortcut lets a charged node depend on more than two independent source clauses; (F2) three binary AND3 steps cannot implement a two-level parity conversion from four source clauses; (F3) balanced XOR rows cost quadratically many sparse occurrences; (F4) a hidden split/discharge rule permits context erasure. The native /341 statement excludes F1/F4, and exact certificates refute F2/F3.

## Fixed system and 3-CNF source
The unchanged (R_{\mathrm{mix341}}) at `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex`, blob `c87acd11d32ccfc3b7acd3667ef11daeb60079cb`, declares free authenticated original DIMACS clauses, unit-charge inference nodes with fan-in at most two, ordinary RES, exact local AND3 with at most three original-variable support and an eight-row truth-table check, GF(2) XOR, and additional LOCAL-CONVERT and conservative paid DEF rules. **The exhibited proof uses only the existing AND3/XOR semantic fragment.** Exact historic serialization of LOCAL-CONVERT private/exported wires and DEF facets remains unauthenticated; independent code is not presented as execution of the authoritative historical checker.

Let (G=(V,E)) be connected simple bridgeless cubic, (h=|V|), (n=3h/2). For each (v), encode the constraint (igoplus_{e\ni v}x_e=\chi_v) by the four distinct width-3 clauses forbidding the opposite-parity triples. Fix (igoplus_v\chi_v=1). Exactly (m=4h) signed 3-clauses, (n=3h/2) edge variables, and (N=\Theta(h\log(h+2))) encoded DIMACS bits result. XOR summation yields (0=1). The published /341 clause-deletion lemma proves that **all** (4h) original sources are indispensable for bridgeless cubic (G).

For a valid source-authenticated shared derivation DAG (pi), let (W(pi)) be the sum of unit weights of **distinct** inference nodes, counted once even with reconvergence. Let (D(pi)) be longest source-to-root dependency path in number of paid nodes, in an explicitly idealized unbounded-processor unit-inference model. Minimize each over every legal /341 proof, without charging discovery in the minimum.

## PROVED/EXACT simultaneous optimum
$$
\boxed{W_{R_{\mathrm{mix341}}}(F_{G,\chi})=4h-1,\qquad
D_{R_{\mathrm{mix341}}}(F_{G,\chi})=\lceil\log_2(4h)\rceil.}
$$
**Lower bound across all native rules.** Every essential source must be in the final contradiction's ancestry, because deleting any unused source would leave a satisfiable formula and all local sound inference justifications intact. For (m) source vertices and (q) paid nodes, connectivity of the undirected ancestor DAG and fan-in at most two give (m+q-1\le2q), hence (q\ge m-1). Independently, an inference at depth (d) has at most (2^d) distinct source ancestors by induction, even with shared predecessors. Thus (D\ge\lceil\log_2 m\rceil).

**Matching one DAG.** For each vertex, combine its four clause truth tables using two parallel AND3 steps, then one final AND3 step annotated with the exactly equivalent parity equation. This costs three paid nodes at depth two; equivalence checks only eight valuations. Combine the (h) local GF(2) rows by a balanced binary XOR tree, (h-1) additional nodes and at most (\lceil\log_2 h\rceil) additional depth. The contradiction is the false row (0=1). The *same* proof attains both minima, with no new branch/assumption/merge/weakening rule.

**Sparse evidence upper bound.** Each intermediate parity row is the boundary-edge set of its vertex group. At any tree level an edge appears in at most two groups, hence across all levels the total row occurrences are (\le3h(\lceil\log_2 h\rceil+1)=O(h\log h)). Storing sorted (O(\log h))-bit edge IDs, explicit source and parent IDs, and constant truth tables yields an (O(h\log^2 h))-bit certificate. Sorted symmetric-difference construction and replay take (O(h\log^2 h)) ordinary bit operations at this coarse upper bound. A streaming variant has an (O(h\log h)) bit *scratch* upper-bound outline, excluding write-only output; the provided Python producer stores extra ancestry and deletion-witness data and does not claim that host peak-RSS figure.

For (P) ideal processors, the normal work/span inequalities (T_P\ge\max\{\lceil W/P\rceil,D\}) and list scheduling (T_P\le\lceil W/P\rceil+D) are only for these unit-priced gates. They are **not** same-machine SAT time/space bounds. Actual source parsing, comparison, building, memory, proof checking, storage, reference traffic, failed attempts and output must be charged.

## COMPUTATIONAL finite controls and audit
The full Python producer and independently written Node verifier were executed locally against exact original-source DIMACS bytes and SHA-256, exact AND3 tables, all GF(2) sums, full proof ancestry, even-charge SAT witnesses, all clause-deletion SAT witnesses, and reconstructed encoded lengths. The independent checker passed **2,429 assertion groups** and rejected **seven corrupted traces** and **five malformed DIMACS encodings**.

| Original graph | h | DIMACS bytes | Paid nodes | Ideal span | Sparse row entries |
|--|--:|--:|--:|--:|--:|
| K4 | 4 | 163 | 15 | 4 | 20 |
| K3,3 | 6 | 239 | 23 | 5 | 48 |
| Cube | 8 | 340 | 31 | 5 | 48 |
| Petersen | 10 | 440 | 39 | 6 | 72 |

The first checker iteration failed on opposite lexicographic versus bit-index assignment order; comparing the **sets** of four forbidden assignments fixed the harness error. A proposed all-zero negative witness turned out genuinely valid on one deleted clause and was replaced by a true source-index corruption. No finite experiment is used to infer an asymptotic lower bound.

## Exact established hard-family and transfer ledger
1. **Odd Tseitin on cubic expanders:** four width-3 parity clauses per vertex, (N=\Theta(h\log h)). Urquhart 1987 and Ben-Sasson/Wigderson 2001 prove (2^{\Omega(h)}) proof size for **ordinary unrestricted shared-DAG Resolution** on suitable expander graphs, not for the mixed calculus. This run's native AND3/XOR shortcut proves the family **fails** as a superpolynomial (W_R) candidate.
2. **Unary PHP:** Haken 1985 gives (2^{\Omega(h)}) ordinary Resolution size with width-(h) occupancy clauses and (N=\Theta(h^3\log h)) encoded bits. It is not 3-CNF as stated; a 3-CNF transfer needs a lower-bound-preserving reduction. Cook 1976 gives polynomial Extended Resolution proofs.
3. **Bit PHP:** Braun arXiv:2609.23015 (September 2026, preprint) states (>\exp(n/(32768\ell^2))) unrestricted DAG Res((\oplus)) lines for (n=2^\ell,\ell\ge32); its source clauses have width up to (2\ell), and paid gates are outside that proof model. It is not a proved bound for native /341 or exact 3-CNF.

## SEARCH and historical checks
Read governing handoff `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md` (blob `033b54b87b7cbe94912af5cf67daa52859143a07`), latest issue #3 comments, LSPV-2/341, LSPV-3/427 actual report, LSPV-5/366 actual handoff plus /367 issue text, AGENTS.md, CODEX.md, repo research skill, Grok `GROKPROOF/2026-11-05_0315_PROGRESS.md` (blob `2c21a1eb356b15a22f364d5d58a6b94360560943`), and Claude `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex` (blob `1f9fc727d3e2b009cba7afec2a93beb62959dd67`). External `konard/p-vs-np` README blob `0e0ec77f83ad6eec1719a96066108b96ac1c2a95` and finite-machine model blob `7ee9a11e434e358d25ca941f7ce5e01efa0b3ce3`; `blkph0x/p-vs-np-proof-research` README blob `f397a7747eaca82df3d754d0a4b4bab1fe10f814` and method index blob `18d693ea71dfa433370eb7afbebc3106e32f03e5`; `openai/math` encoded-CNF transport file `lean/OAI/Algorithms/SubexponentialSAT/ExecCNFCodeTransport.lean` blob `5d1a1946d5d6714a2164b8f891cc627721ef69e9`; DRAT-trim README blob `eb6ffcc4a85ff1c74a5995b6caae4372381dcd47`. None authenticates arbitrary historical /341 proof wrappers or supplies B3. Actual queries: `R_mix341 LOCAL-CONVERT`, `branching shared DAG`, `LSPV-3/427`, `REFEREE367`, `ExecCNF`, `Urquhart 1987 resolution expander`, `Ben Sasson Wigderson 2001 resolution width`, `Haken 1985`, `Braun bit pigeonhole Res(XOR) 2026`. Direct Google-branded search unavailable, general indexed web and GitHub used. GitHub raw/compact reproducer paths below.

## Status / exact open transfer
**PROVED/EXACT:** dual (m-1)/log-depth source-capacity bound under /341's explicit fan-in, and its simultaneous attainment on a formerly established Resolution-hard 3-CNF family. **NOT proved:** full native selector serialization, complete polynomial normalization for mixed branch proofs, full-mixed superpolynomial (\overline W_R(N)), or weakest-sufficient B3:
$$
\mathrm{SAT}\in P \quad\Longrightarrow\quad
\overline W_{R_{\mathrm{mix341}}}(N)\le N^{O(1)}.
$$
B1, B2, B3 and P versus NP remain **OPEN**. A proof-system bound is not an unrestricted computational lower bound.

**Reproducibility:** `experiments/arc/lspv1_423_balanced_tseitin_compact.py` (executed compact reproducer); `results/raw/arc/2026-11-05_1102_LSPV1_BALANCED_WORK_SPAN423_summary.json`. Full independently executed Python/JS code and 23,595-byte raw witness fixture are offered as local conversation attachments, SHA-256 respectively `7014af6ac6547ef3ef36d859e2306027fb1a3c1ce440baea956bc9258bc64635`, `a9e2c22284968c6506a350e707816ad6cd2230d42170f2672af0803889a6f4d0`, `e4ef86748ca6949e46a8869bbd16aa785451e72230a71f36bc9e61a2302818cd`. Do not call GitHub compact code the full independent verifier.

References: Urquhart, JACM 34(1):209–219, 1987; Ben-Sasson–Wigderson, JACM 48(2):149–169, 2001; Haken, TCS 39:297–308, 1985; Cook, SIGACT News 8(4):28–32, 1976; Braun, arXiv:2609.23015, 2026.