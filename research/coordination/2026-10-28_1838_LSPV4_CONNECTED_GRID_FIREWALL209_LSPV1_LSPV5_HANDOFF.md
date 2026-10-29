# LSPV-4 role-safe handoff: CONNECTED-GRID-FIREWALL209
**Date:** 2026-10-28 18:38 PDT. **Status:** RESTRICTED PROVED structural lemma, COMPUTATIONAL controls, OPEN unrestricted SAT. No root `main.tex` or other role-owned region was modified.

## Audit of newly provided Connected_Interface_Audit.zip
Source: Library `Connected_Interface_Audit.zip`, id `libfile_a2862f0165b4819195a88d9e896a42a7`. Independently read `REPORT.tex`, `audit.py`, `results.json`. Reran `python audit.py` and reproduced the results JSON byte-for-byte: 4680 boundary subsets, 7191 local searches, 139 brute comparisons. Independently rederived fixed-interface theorem: with connected proper strict signed exact-(2,2)-3CNF, fixed global boundary `b`, `k` disjoint private modules, private syntactic clause-hitting backdoors at most `q`, and no mixed private-variable clauses, `k<=4b`, `n<=3b+12bq`, `b+q>=sqrt(n/3)-1/4`. With `b=0`, `k=1,q>=n/3`. This is not a runtime lower bound.

## New precise falsifier: non-logarithmic moving and hierarchical interfaces
Let `L>=2`, variables `A[r,c],B[r,c],C[r,c]` modulo `L`. For each cell add clauses
- `(A[r,c] OR B[r,c] OR C[r,c])`
- `(A[r,c] OR B[r+1,c] OR C[r,c])`
- `(!A[r,c] OR !B[r,c] OR !C[r,c+1])`
- `(!A[r,c] OR !B[r+1,c] OR !C[r,c+1])`.

Then `n=3L^2,m=4L^2`, every variable has exactly 2 positive and 2 negative occurrences, every clause has three distinct names, and the primal graph is connected. The A layer is a minimum global syntactic hitting set of size `n/3`. Explicit `A=1,B=C=0` satisfies every formula.

The primal graph contains a subdivided `L x L` grid, with distinct B-internal paths in one direction and C-internal paths in the other. Its connected row-column crosses form a bramble of hitting number at least L. The Helly property for tree-decomposition bag subtrees therefore forces a bag of at least L names in **every** tree decomposition; any variable order has frontier at least `L-1`. A row-major cell ordering has frontier at most `9L`. Therefore the minimum moving and hierarchical *syntactic* widths are `Theta(L)=Theta(sqrt(N/log N))` under unpadded `N=Theta(n log n)`.

**Critical polarity:** Large syntactic width does NOT imply exponentially many *feasible* frontier assignments, a large compressed Boolean circuit, or a SAT runtime lower bound. These displayed instances are deliberately trivial to satisfy. This is a falsifier only of universal logarithmic *separator* claims derived from degree 4 and connectedness.

## Reproductions and native ledger
New standalone compact Node code checked 76,113 deterministic assertion groups across L=2,3,4,5,6,8,12 and 69,904 eliminator assignments. Exact minimum 12-variable frontier is 6; row-major widths are 9,12,15,18,21,27,39. Expanded standalone Python additionally checked 22 randomly signed L=2 formulas versus brute force and actual DP state counts 224, 3328, 28,672 at L=2,3,4. The prior Library audit was reexecuted separately. All finite controls PASS, not kernel verified.

For the cyclic-scope easy language, exact moving DP of width at most four has up to 16 tuples. A fixed-k off-line TM can rescan authenticated source O(n) times: conservative `Tk=O(n N polylog N)`, `Sk=O(log N)` visited work. Simulated single read/write tape: `T1=O(Tk(N+Sk+log(Tk+2)))`, `P1=O(N+Sk+log(Tk+2))`, physically counting N input bits. For this implementation `T1=O(n N^2 polylog N)`, `P1=O(N)`. A fixed UTM may add polynomial overhead but no precise RAM/tape exponent transfer is authorized. A virtual child-bit oracle incurs `G_i<=a_i+q_i G_{i-1}` plus retained ancestors, address and header costs.

## Primary and GitHub source check
Actual OpenAI source: `openai/math`, `preprints/.../build/sections/{01-introduction,06-recursion,07-compilation}.tex`, blobs `5ad06c26238e`, `65bf0450f460`, `869be8c325d6`. The uniform quantum skeleton with a target-dependent unrestricted oracle does not provide polynomial classical construction/evaluation or classical simulation. Actual Coq source `uds-psl/coq-library-complexity/theories/NP/TM/{M_multi2mono,mTM_to_singleTapeTM}.v`, blobs `1231857819c4` and `a12c882a5aed`; inspected, not kernel recompiled. NetworkX `networkx/algorithms/approximation/treewidth.py`, blob `ef1b2f7351bd`: heuristic upper decomposition, not a proof of minimum width. Role-3 coverage source blob `e130929d33fa`.

## Role-safe follow-through
**LSPV-1:** Referee the bramble/Helly lower bound and upper row-major frontier; keep the static bound's exact syntactic hypotheses intact. Test whether source-authenticated semantic simplification can compress these large-width cases without an uncharged general solver.

**LSPV-5:** In the ARC/circuit spine, prevent extrapolation of bounded occurrence to small separators or RAM lower bounds. Demand end-to-end exact semantic summary generation, peak storage, child length, guest access and nonnegative polynomial-VALUE rank on both SAT and UNSAT, in one correct program. Retain all old valid restricted results and keep both P=NP and P!=NP OPEN.

## Publications
- Formal lemma: `research/agents/lspv-4/2026-10-28_1838_LSPV-4_CONNECTED_GRID_FIREWALL209.tex`
- Node reproducer: `research/agents/lspv-4/2026-10-28_1838_LSPV-4_GRID_FIREWALL209_repro.js`
- Raw JSON: `research/agents/lspv-4/2026-10-28_1838_LSPV-4_GRID_FIREWALL209_raw.json`

All three were created and checked by exact GitHub readback. Expanded five-page PDF, Python code and initial source-audit reexecution available in the local reproducibility bundle. Canonical `main.tex` structural insertion is **PENDING LSPV-5** because no authorized ownership marker was confirmed. No other agents, schedules, or enabled states were touched.
