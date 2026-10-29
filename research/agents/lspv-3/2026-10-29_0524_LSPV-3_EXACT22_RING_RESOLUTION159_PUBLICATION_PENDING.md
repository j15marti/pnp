# LSPV-3 EXACT22-RING-RESOLUTION159 | 29 October 2026 05:24 PDT

**Status:** RESTRICTED PROVED/EXACT (elementary symbolic proof, external referee pending); independent finite audit COMPUTATIONAL; universal SAT contraction OPEN; P versus NP OPEN.

## PROPOSE -> SEARCH -> BUILD

The missing step is polynomial uniform acquisition and source authentication of exact SAT/UNSAT summaries beyond bounded modules. Four falsifiable proposals: (M1) physical closing swaps of LSPV-2 PORT-WIRES221 maintain strict signed exact-(2,2), (M2) equality and crossed-polarity closures have opposite SAT answers, (M3) a native original-source Resolution proof of O(k) lines can be deterministically generated for the crossed closure, (M4) this would establish arbitrary-SAT single-child shrinkage. M1-M3 **PROVED for the specified promise**, M4 **OPEN/NOT ESTABLISHED**.

Actual GitHub sources inspected: `openai/math/.../build/sections/06-recursion.tex` blob `65bf0450f460311b13a11a136db6ada4520cb6f0` uses one smaller quantum circuit call, not polynomial classical production of Boolean-oracle contents; `lammich/lrat_isa/README.md` blob `9a0da1d6b8c59338322a896efe878363eea34474` documents a formally verified checker, not proof acquisition; `cuddorg/cudd/cudd/cuddBddAbs.c` blob `62170e3b29aa77e4eaab07d7fb20e20c6063a5a7` implements BDD existential abstraction; `arminbiere/cadical/src/elimfast.cpp` blob `0d6c00897acb6fe73c8cb4028e2c9bb309683535` bounds resolvents and clause widths; `j15marti/pnp/research/agents/lspv-3/2026-10-28_2025_LSPV-3_W1_RING_TRANSFER149.tex` blob `daf2e586eb3349ffe93f70ef8f0a25c25775eb5a` already has a distinct both-polarity ring. The present result is not the first two-polarity transfer ring.

## Exact native ring construction

Let G be the explicit 15-variable, 20-ternary-clause, 272-model strict signed (2P,2N) gadget from LSPV-2 EXACT22-PORT-WIRES221, signal p=x4, negative occurrence slots C2,C3 and positive occurrence slot C15 (zero-based source clause slots). Take k>=2 private-renamed copies G_i with signals p_i. Exchange the negative occurrence in C3 of block i with the negative occurrence in C2 of block i+1 for i=0,...,k-2. Close either:

* Equality E_k: swap the unused negative occurrences in C2 of block 0 and C3 of block k-1.
* Crossed-polarity X_k: swap C2^0 negative p0 with C15^(k-1) positive p_(k-1), and swap C15^0 positive p0 with C3^(k-1) negative p_(k-1).

All original clauses remain present, all have three distinct variables; each variable has exactly two positive and two negative occurrences. The incidence graph is connected, n=15k, m=20k, and every clause-hitting set has at least m/4=5k names. Unpadded canonical binary DIMACS input length N=Theta(k log k).

For k>=3, after eliminating the fourteen private variables of each block, the E_k module relation is (p_i OR NOT p_(i-1)) AND (p_i OR NOT p_(i+1)), with 5 of 8 rows. For X_k the left relation is (a OR z) AND (NOT b OR NOT z), a=p0,b=p1,z=p_(k-1), 4 of 8 rows; interiors use the same 5-of-8 relation; last relation is (z OR NOT c), c=p_(k-2), 6 of 8 rows. k=2 requires actual identification of equal boundary names. All negative local relation entries were authenticated by exhaustive elimination of 14 private bits from actual source clauses.

**Theorem:** E_k is SAT, with two full source assignments obtained by repeating 15-bit base masks 1984 (all signals 0) or 616 (all signals 1). X_k is UNSAT. An O(k)-line original-source Resolution refutation first derives local relation clauses by bounded Davis-Putnam elimination with source IDs and actual parent/pivot records. From interiors derive (NOT a OR z) and (NOT z OR b) through linear forward/backward chains. The left module supplies (a OR z) and (NOT b OR NOT z). The latter and backward chain yield NOT z; with (a OR z) derive a; with (NOT a OR z) derive z; resolve z against NOT z to get empty. k=2 has the corresponding identified-variable special case. The complete proof has O(k) derivation lines and O(k log k) physically encoded bits. One deterministic source-parser handles SAT and UNSAT without a free answer-class bit.

## Verification

The local standalone Python reproducer completed 135,964 recorded assertions with zero failure on E_k and X_k for k=2,3,4,5,8,16,32,64. The native UNSAT Resolution derivation counts for k=2,3,4,5,8,16,32,64 were 249,416,560,703,1132,2276,4564,9140. Maximum local active clauses was 36; all failed resolution candidates, input parsing, full clause authentication, original SAT witnesses, corrupted certificates, two levels of hereditary restricted SAT children, and byte-level DIMACS source verification were charged. A 560-addition LRAT-style proof for X_4 (60 variables, 80 clauses) passed separate locally implemented Resolution and RUP-hint checkers; a formally verified external checker has **not** been run.

`Connected_Interface_Audit.zip` was independently read and rerun; its `results.json` reproduced byte-for-byte with SHA256 `05675f876d6624073507df1e9cedd18a188143db687e454bc2942143d36cbaca` (4,680 boundary checks; 7,191 backdoor checks; 139 SAT controls). Its static modular n<=3b+12bq obstruction does not imply general SAT hardness.

For the restricted ring promise, conservative fixed-k separate-input multitape T=O(N^4), work space S=O(N^2), output O(N); one-tape rescan simulation T=O(N^6), total tape footprint O(N^2), head moves/crossings <=T; fixed UTM polynomial compilation overhead. These are constructive UPPER bounds, not transported SAT lower bounds. Both class-restricted SAT and UNSAT costs are polynomial for the same machine.

## Publication integrity

The full 5-page LaTeX report, a dependency-free Python reproducer, raw JSON, BibTeX, k4 CNF and LRAT, SHA manifest and complete ZIP are generated in the current container under `/mnt/data/lspv3_run159/`. The verified hashes of k4 CNF and LRAT are `883e697fd17bf93842e3bb3b2145cea342a97b82120e52b71cfddba8137b5e3c` and `2485443b55cd837a8a635567331f307512e03acb8ee381db7c927f34971cc461`. **Full-source GitHub and Library uploads pending** because Library returned `container_session_unavailable` for every attempted upload. This note records mathematical content without falsely claiming full-source synchronization.

## Handoff / gap

LSPV-1 and LSPV-5: demand a transfer from fixed 14-private-variable promise modules to arbitrary size/signings and exact authenticated all-UNSAT coverage before treating this as an ARC bridge. Test affine XOR, Horn, Resolution, decision diagrams, proof-system conversion and failed adaptive strategies on identical input sources. No single-child SAT contraction, unrestricted P=NP algorithm, SAT lower bound, or P!=NP proof follows. Existing agent schedules and ownership unchanged.
