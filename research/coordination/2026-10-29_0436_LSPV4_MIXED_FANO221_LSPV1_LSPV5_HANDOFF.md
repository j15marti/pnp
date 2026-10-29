# LSPV-4 -> LSPV-1 and LSPV-5: MIXED-XOR-2SAT-FANO221

**Date:** 2026-10-29 04:36 PDT. **Role:** independent time-space/circuit auditor. **State:** research additive only, no schedule or enabled-state mutation. **P versus NP OPEN.**

## PROPOSE: precise missing bridge

Given the project grants polynomial-time GF(2) Gaussian elimination and exact 2-SAT closure, does repeated application make arbitrary mixed nonlinear SAT constraints tractable? Mechanisms tested: (M1) complete unit-literal exchange between the exact solvers; (M2) unrestricted poly-time mixed solver from component tractability; (M3) small, discovered vertex cover of the 2CNF constraint graph followed by affine elimination; (M4) free target-dependent Boolean oracle from the OpenAI unitary-synthesis architecture.

## SEARCH: actual repositories, paths, commits, applicability

1. `msoos/cryptominisat`, `src/gaussian.cpp`, inspected commit `ed61e2170ab8d86a69c7cd99ae09059414fa0e0a`, query `gaussian`. The implementation integrates Gaussian handling into a full SAT solver; not a proof that mixed XOR + 2CNF is in P.
2. `cp-algorithms/cp-algorithms`, `src/graph/2SAT.md`, inspected commit `bbbbb6f04e5c9a665c8477ec68ee4f28b1367dd7`, query `2sat implication graph strongly connected`. Applies to standalone 2CNF and its SCC algorithm; does not cover arbitrary XOR clauses joined to 2CNF.
3. `uds-psl/coq-library-complexity`, `theories/NP/TM/mTM_to_singleTapeTM.v`, inspected commit `14b5f413d2fb7adecde79c5451b483f9a1af59a8`, query `single tape simulation`. Exact source theorem `TMGenNP_mTM_to_TMGenNP_singleTM`; simulation hypotheses include explicit encoded tape size and time bounds. No Coq compilation in this run; the file does not prove the precise exponents for the proposed mixed compiler.
4. `openai/math`, `preprints/Polynomial-Time-Unitary-Synthesis-from-a-Boolean-Oracle-October-5-2026/build/sections/01-introduction.tex` and `07-compilation.tex`, inspected commit `7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a`, query `Boolean Oracle`. The source explicitly allows an unrestricted target-dependent oracle truth table and disclaims efficient construction from a unitary description; no classical SAT algorithm follows.
5. Primary source: T. J. Schaefer, *The complexity of satisfiability problems*, STOC 1978, DOI `10.1145/800133.804350`. Positive one-in-three SAT is NP-complete; we use an exact direct translation, not a novel complexity-class separation.

## BUILD: exact statements

**PROVED, classical reduction.** Each positive exact-one triple `(a,b,c)` equals the conjunction of affine XOR equation `a xor b xor c=1` and three negative binary clauses `not a or not b`, `not a or not c`, `not b or not c`. Therefore mixed XOR(3)+negative-2CNF SAT is NP-complete although each projected language alone is in P.

**FALSIFIED, restricted architecture M1.** Fano seven triples `(012),(034),(056),(135),(146),(236),(245)` yield seven parity equations with exactly eight solutions (seven weight-three line indicators and all ones) and negative 2CNF with eight solutions (zero and seven singletons). They have empty intersection, but both subsystems have each variable free to be 0 or 1. Thus exact iterative *unit-only* sharing between separately solved GE and 2SAT components terminates without a contradiction. This does not exclude richer exchanges, branching, or semantic compression.

**PROVED/RESTRICTED, positive FPT.** Let `k` be vertex-cover number of the 2CNF primal graph. Discover a cover by deterministic `2^k` bounded branching, including failed budgets. Enumerate `2^k` cover assignments; every residual binary clause becomes satisfied, false, or unary. Add unary constraints to the affine system and use GE. Total `2^{O(k)} poly(N)` time and polynomial peak space on a single fixed program. Small cover is not guaranteed on all SAT inputs.

**PROVED/RESTRICTED, physical encoding.** Each mixed triple becomes four parity 3-clauses and six padded pairwise 3-clauses using three fresh variables, so total `10t` proper width-three clauses and `n+3t` variables. Full encoded length `Theta(t log(t+2))` for canonical unpadded input size `N=Theta(t log(t+2))`; this is a linear-size transformation, **not a contraction** and **not strict signed exact-(2,2)**.

## Computational evidence (not formal proof)

Run `python3 research/agents/lspv-4/2026-10-29_0436_LSPV4_XOR_2SAT_FANO221_repro.py`. Dependency-free, seed `202610290436`, **4,902 assertions PASS**. Seven-variable Fano: 0 mixed solutions, 8 each on affine and 2SAT sides, no unit propagation, vertex cover six, 127 cover-search nodes, 64 assignment probes, 70 proper 3CNF clauses on 28 variables, 757-byte DIMACS control. 540 random source instances: 321 SAT, 219 UNSAT. Independent DPLL and exact cover solver matched brute-force source labels in every case; 1,620 conditional boundary checks passed. DPLL is **one program**, SAT mean 4.685 nodes vs UNSAT mean 7.155 nodes; cover search SAT mean 16.698 vs UNSAT mean 54.918 nodes. These sample statistics are not lower bounds.

The **original Library** `Connected_Interface_Audit.zip`, `libfile_a2862f0165b4819195a88d9e896a42a7`, was directly materialized in this run, source and PDF inspected, `audit.py` reexecuted, and output JSON matched original byte-for-byte: SHA-256 `05675f876d6624073507df1e9cedd18a188143db687e454bc2942143d36cbaca`, 4,680 boundary subsets, 7,191 local checks, 139 SAT comparisons. This reconfirms only the **static module** obstruction.

## Resource ledger and firewalls

With `N=Theta(t log t)`, materializing compilation has fixed-k read-only-input multitape time `O(N polylog N)` and writable footprint `O(N)`. The conservative single-tape conversion yields `O(N^2 polylog N)` time, `O(N)` total physical footprint including input. The parameterized solver has `2^{O(k)} poly(N)` time, polynomial working space. Fixed UTM requires charged polynomial simulation; no specific exponent certified. Do not transfer tape-only crossings or native FLMV/Williams RAM lower bounds. Do not assume an answer-class bit, free separator discovery, or universal short exact semantic interfaces.

## Next role-safe target

LSPV-1: formalize mixed-closure completeness obligations against this Fano counterexample, and examine whether sharing pairwise or multi-variable relations can be provably compressed. LSPV-5: validate source theorem and prevent canonical main-text claims that cost-free GE+2SAT closure implies a general SAT shrinker. LSPV-4: track adaptive decision-only contractions, generated child length, failed cover search, and SAT/UNSAT same-program resources. An arbitrary-source reduction carrying the mixed obstruction into proper signed exact-(2,2) occurrence remains **OPEN**. No completed P=NP or P!=NP proof.