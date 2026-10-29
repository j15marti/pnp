# LSPV-3 -> LSPV-1 and LSPV-5: PORT-QUANTIFIER-CLOSURE161

Date: October 29, 2026, Los Angeles. Status: RESTRICTED/EXACT on a fixed source grammar, dependent on an exhaustive finite 81-template lemma; independent mathematical review and kernel verification pending. P vs NP OPEN.

## Proven conditional on the finite source lemma

Take k copies of LSPV-2 PORT-WIRES221's fixed 15-variable, 20-clause connected proper strict signed exact-(2,2) gadget G with distinguished p=x4. Arbitrarily permute all 4k signed occurrences of the p_i variables into the 4k original port-bearing clause slots, preserving each signed occurrence as a token. Every resulting source-annotated formula is still proper strict signed exact-(2,2), with n=15k and m=20k, and a polynomially recognizable canonical block representation.

Exact existential projection over the 14k private variables is a Boolean formula D(p_1,...,p_k) with at most 3k 2CNF clauses, constructible deterministically in polynomial time, **regardless of the graph topology, sign permutations, or number of simultaneously used ports**. There are 3^4=81 signed-slot patterns; the exhaustive fixed-source audit computed the exact local relations and verified that each equals a conjunction of at most three width-two implicates. After substitution of the actual incoming port variables, the conjunction of all local factors gives the exact global projection.

A single deterministic 2SAT algorithm handles SAT and UNSAT. SAT witnesses are reconstructed by the source-profile tables, and UNSAT is witnessed by two opposing source-tagged SCC paths in the compiled implication graph. The source-aware verifier authenticates the 20-clause template and all local projection entries. This is not a formally verified original-clause LRAT refutation, and the source-to-LRAT lift remains pending.

## Falsifier to naive equality composition

Each of 12 isolated same-sign swaps enforces pairwise port equality. However, their simultaneous application on an 8-module cubic connected structure yields precisely four port vectors: 00000000, 01111110, 10000001, 11111111. The nonuniform p=01111110 has directly checked 15-bit module witnesses [1730,616,616,1864,616,616,1738,1730], satisfying all 160 original clauses on 120 variables. Isolated edge equality is not a compositional semantics theorem.

## Reproduction and limitations

The standard-library reproducer passed all 81 signed-slot truth-table equivalence checks, 700 deterministic permutation cases (171 SAT, 529 UNSAT), the 8-module counterexample and SCC certificate checks. Two independent invocations produced byte-identical raw JSON (SHA-256 511836ad46f19e32a76c01fdcc8d2f0a8a54c3aab8073f5ec2722e106773b124). Independent SciPy/HiGHS full-CNF MILP confirmed a connected 30-variable SAT and UNSAT control and 10 pinned cubic controls. The original Connected_Interface_Audit.zip audit was rerun with identical parsed JSON (4680,7191,139).

Input bit length N=Theta(k log(k+2)); the 2CNF child still has O(k log k) bit length, not N^lambda for fixed lambda<1. No reduction from arbitrary strict signed exact-(2,2) formulas to the generated family is shown. This is a restricted upper-bound theorem, not general SAT hardness or a P=NP implication. Do not conflate low-variance finite source tables with arbitrary NP-hard semantic acquisition.

The designated next LSPV-3 target is either (a) construct a genuinely cofactor-preserving uniform polynomial reduction from arbitrary signed exact-(2,2) 3CNF into a tractable source grammar, which would be a major constructive breakthrough, or (b) identify an invariant that forbids such an extension only under explicitly stated hypotheses. Also pursue a finite machine-checkable or LRAT validation of all 81 local templates. Preserve the existing five agents and schedules.
