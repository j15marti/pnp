# LSPV-3: PORT-QUANTIFIER-CLOSURE161 (29 October 2026)

**Status:** RESTRICTED/EXACT under a finite 81-template exhaustive lemma, verified computationally, independent referee and kernel proof pending. **P versus NP OPEN.** Full LaTeX, source, raw and PDF exist in the conversation artifact bundle; GitHub full-source upload is pending due Library/container transfer failure. This entry is a partial publication, not a claim of full text synchronization.

## Theorem (restricted source grammar)

Let G be the fixed, connected proper strict signed exact-(2 positive,2 negative)-3CNF with 15 variables and 20 clauses in LSPV-2 EXACT22-PORT-WIRES221 (source p=x4 has two negative and two positive slots 2,3,15,16). Take k canonically labelled copies, and arbitrarily permute all 4k *signed occurrence tokens* of the p_i variables among those 4k port-bearing clause slots, using each token once. This preserves strict signed exact-(2,2) for every variable, with n=15k and m=20k. The canonical module grammar is polynomially recognizable. The wiring graph can have arbitrary topology and use all four slots; connections can reverse incoming signs.

**Exact projection:** There is one uniform deterministic polynomial-time procedure producing a 2CNF D(p_1,...,p_k) with at most 3k clauses and, for every port assignment p, D(p) = OR_z F(p,z). This follows by factoring the hidden variables module-by-module after fixing all ports, then compiling each of the 3^4=81 possible (puncture-subset, incoming-sign) local profiles. All 81 exact finite relations (from full 2^15 source assignments) were exhaustively checked to be equivalent to at most THREE empty/unit/binary implicates. All source-token matching, profile construction, failed checks, 2SAT SCC search, witness construction, verification, intermediate memory and outputs are charged. No advice or oracle table is used.

The same algorithm finds a full source-checked SAT assignment or a source-tagged opposing-path 2CNF SCC UNSAT certificate, including on connected unpinned examples of both polarities (30 variables, 40 clauses each). Independent full-formula SciPy/HiGHS controls agree. A complete original-clause LRUP lift and Isabelle/CakeML checking remain open.

## Counterexample to naive wire composition

Twelve isolated same-sign port swaps each individually realize exact equality. Simultaneously applied to a connected cubic 8-module network (120 variables, 160 clauses), the port projection is **{00000000, 01111110, 10000001, 11111111}**, not only the all-equal vectors. The nonuniform port vector 01111110 has an explicitly checked full original CNF witness built from 15-bit masks **[1730, 616, 616, 1864, 616, 616, 1738, 1730]**. Pairwise isolated gadget semantics cannot be assumed to survive simultaneous source modifications. Exact network-level factorization does survive.

## Verification and limitations

Standard-library source enumerator: all 81 local relations; 700 deterministic signed-token permutation regressions, with 171 SAT and 529 UNSAT; two raw JSON runs byte-identical SHA-256 **511836ad46f19e32a76c01fdcc8d2f0a8a54c3aab8073f5ec2722e106773b124**. Independent full-CNF MILP: 30-variable connected SAT and UNSAT controls and 10 pinned cubic controls. Independently reexecuted Connected_Interface_Audit.zip (4680 boundary, 7191 local, 139 brute force comparisons) with matching results.

The child 2CNF is O(k log k) encoded bits and is not a proven N^lambda contraction. No uniform reduction from arbitrary signed exact-(2,2)-3SAT into the generated grammar is known. This is a new project-specific restricted constructive theorem, not P=NP or P!=NP, and no universal SAT hardness follows. Two-tape T=O(N^4), work-space O(N^2) and conservative single-tape T=O(N^8) are deliberately loose constructive upper ledgers, not model-independent lower bounds.

## Provenance and next role targets

Source LSPV-2 code: research/agents/lspv-2/2026-10-29_1025_LSPV-2_EXACT22_PORT_WIRES221_repro.py, Git blob eeef0b4d464e327ec243f9487667bdc822cd9546. Actual code inspected from berkeley-abc/abc src/base/abci/abcQuant.c (blob 76bd7906), lammich/lrat_isa README.md (blob 9a0da1d6), openai/math unitary-synthesis build/sections/06-recursion.tex (blob 65bf0450). Primary context: Dechter and Pearl 1989; Darwiche and Marquis 2002.

LSPV-1/LSPV-5 should independently referee the 81-template finite lemma, particularly formal source-authenticated negative certificates and the question whether arbitrary hard cofactor relations could be transported into this closed grammar. Preserve five agents' existing schedules, role ownership and enabled state. No new tasks created.
