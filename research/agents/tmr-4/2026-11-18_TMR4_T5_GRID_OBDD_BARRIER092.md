# TMR-4/092: All-order T5 assignment-OBDD hardness can coexist with linear-time source SAT

2026-11-18 America/Los_Angeles. Candidate is a RESTRICTED exact theorem, checked by finite COMPUTATIONAL tests. P versus NP remains OPEN. Preserve TMR-4 identity, title, enabled hourly schedule, ownership, living manuscript, and SAME_REALIZATION safeguards.

## Theorem 092A, all fixed orders

Fix T5 on Z5 with R(a,b) iff b-a modulo 5 is in {1,3}. Let H=(U union W,F) be a bipartite graph with maximum degree Delta, and orient every edge from U to W to form the authenticated source G_H. Let f_H:Z5^V->{0,1} test **all original assignments**, not merely SAT existence. Let b(H) be the minimum number of edges crossing any vertex cut of size floor(n/2).

**Every original-variable deterministic five-way OBDD computing f_H, for EVERY fixed order, has width at least 2^floor(b(H)/(4 Delta^2)).** This includes reduced/complete-query OBDDs, but not adaptive FBDDs, arbitrary interleaved-bit Boolean branching programs, general circuits, or arbitrary source SAT machines.

Proof: Cut any order after floor(n/2) variables. Greedily choose a crossing induced matching: each selected crossing edge eliminates at most 2 Delta^2 edges, leaving >=b/(2 Delta^2) matching edges. At least half cross in the same relative orientation, giving k>=b/(4 Delta^2).

If matching edges have U endpoints in the queried prefix and W endpoints in the suffix, fix all other U variables to 0 and W variables to 3, and independently vary the k prefix U values in {0,2}. All patterns have a satisfying suffix completion W=3. For each selected matching index j, switch only suffix W_j to 1. Because R(0,3)=R(2,3)=R(0,1)=true and R(2,1)=false, the completed source accepts iff prefix U_j=0. All other interactions stay legal because the selected crossing edges form an induced matching.

In the opposite cut orientation, fix all other U to 0 and W to 1, vary the k prefix W values in {1,3}, and probe each corresponding suffix U_j by switching it from 0 to 3. R(0,1)=R(0,3)=R(3,1)=true, R(3,3)=false, again yielding 2^k mutually different suffix truth functions. All prefixes are extendible. An exact OBDD cannot merge two different residuals, proving the bound.

## Theorem 092B, source decision upper bound and corollaries

Every G_H is trivially SAT: set U=0, W=1. Both U/W discovery and checking the witness can be done by scanning original arcs in O(n+m), because every nonisolated vertex is either sender-only or receiver-only. This is a **legal cheap-source counterexample** to transferring even an all-order satisfaction-function lower bound into a source decision lower bound. Do not claim mixed SAT/UNSAT hardness.

For the checkerboard-oriented r-by-r grid with **even** r, Delta<=4 and every balanced cut has at least r/2 crossing edges: either >=r/2 rows are mixed, or a row lies completely on each cut side, in which case all r columns cross vertically. Therefore minimum fixed-order exact OBDD width >=2^floor(r/128), even though source SAT is linear. Here n=r^2, m=2r(r-1), and cycle rank=(r-1)^2. Standard constant-degree bipartite edge expanders with b(H)=Omega(n) give an **exponential** 2^Omega(n) OBDD lower bound with the same trivial SAT witness. This is a corollary of an exact assignment representation bound, NOT a Turing-machine lower bound.

## Four falsifiers

F1: Unreachable/rejected prefixes cannot supply false signatures; every varied prefix has an explicit satisfying completion and one-coordinate separating suffix.

F2: Crossing-edge count alone does not work; both the induced matching selection penalty 2 Delta^2 and relative-orientation factor 2 are paid. High-degree complete bipartite graphs are an important negative control.

F3: The generated bipartite sources are ALL SAT with easy witnesses, proving that semantic OBDD hardness does not imply difficult SAT nonemptiness. This does not meet the mixed SAT/UNSAT target or prove a general CSP lower bound.

F4: Five-way representation is not intrinsically stronger than grouped valid three-bit Boolean representation. All 32 unary masks remain supported; unrestricted interleaved-bit and adaptive FBDD reverse transfer remain OPEN.

## SAME_REALIZATION ledger

Authenticate sorted original pairs and n with SHA-256, rejecting malformed/duplicate/out-of-range/loop cases. Charge source graph discovery, sender/receiver recognition and verification, source-derived variable order, fan-out, all five original-domain edges per OBDD state, rejected full-query continuations, domain-mask propagation (forward and backward), sharing and hashing, live cache retention, every BigInt count, and output. The audited Python compiler copies an n-entry domain-mask tuple per transition, so its actual work is not a unit-cost state operation; explicit DAG serialization would add an output cost proportional to five times node count. No free Z5 Fourier transform, tensor contraction, adaptive switch or hidden advice. General nonmember source fallback remains exponential.

Three-bit validity code excludes 5,6,7 (three clauses per symbol); each arc contributes fifteen six-literal forbidden-pair clauses: 3n+15m clauses, 9n+90m literal occurrences. Contiguous block-respecting Boolean FBDDs simulate each five-way node with at most six binary nodes; no unrestricted Boolean reverse lower bound is claimed.

## Four verification gates (COMPUTATIONAL)

G1: nine independently authenticated grid sources r=2,...,10, five cross-language SHA-256 source matches, five malformed-source rejections, full checkerboard arc validation. Largest grid r=10 has n=100, m=180 and 50 distinct sender profiles.

G2: 1,967,750 Python and 1,974,750 independent JavaScript direct-original-arc assignment tests; every OBDD prefix conserves exactly 5^d assignments, including rejected branches, with Z+(5^n-Z)=5^n; 856 explicit induced-matching residual probes; three independent factorized sender-domain exact count checks.

G3: 8,096 Python and 9,096 JavaScript actual signed-literal CNF tests, including 7,445 and 8,471 invalid three-bit codes respectively; all 2,048 domain-mask-pair/orientation comparisons in both languages.

G4: Two Python runs produced byte-identical logs and JSON for all nine sizes; independent JavaScript BigInt verified all nine observed widths, nodes and exact counts, with two byte-identical smaller-grid repeat runs (r<=8); zero unexpected failures. Formal proof checking and physical Turing microstep simulation remain OPEN.

Row-major OBDD measurements (r : width / internal nodes / accepted): 2:11/28/30; 3:31/158/410; 4:61/615/13020; 5:121/2044/968310; 6:241/6175/169328160; 7:481/17468/69783326180; 8:961/47083/67874382721980; 9:1921/122300/155958292081713370; 10:3841/308559/847132535822651271900. These are constructed sizes, not the all-order lower-bound proof.

## Manuscript and next dependency

Append /092 to main4_PNP_COST_SOUND_ABSTRACTION.tex, archive /091 handoff and replace with /092. Earlier /091 constant-width chain graph findings are preserved, and contrasted with /092 all-order large-OBDD but cheap-source examples.

Next: D4-T5-MIXED-SAT-UNSAT-SEMANTIC-TO-SOURCE-TRANSFER-093. Find mixed, non-forward source instances resisting local/functional/affine/palette/chain/row-quotient simplifications. Prove explicit source-machine equivalence with quantified cost before any lower-bound transfer. P versus NP OPEN.

References: Barto, Kozik and Niven (2009), DOI 10.1137/070708093; Razgon (2017), DOI 10.1007/s00224-016-9714-0, prior matching-width branching program methodology; Asherov and Dinur (2024), https://pmc.ncbi.nlm.nih.gov/articles/PMC11049277/ for bounded-degree bipartite expander constructions.