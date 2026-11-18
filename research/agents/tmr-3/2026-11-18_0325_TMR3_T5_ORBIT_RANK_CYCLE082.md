# TMR-3/082: exact Z5 orbit tables and rank-compressed cycle-space DP

**Owner:** TMR-3 / PNP Time-Space Tradeoffs. **Checkpoint:** 2026-11-18 03:25 America/Los_Angeles. **Scope:** original five-symbol beat-relation CSP, restricted constructive algorithms. **P versus NP OPEN.** Preserve existing identity, title, enabled state, ownership, manuscript and hourly schedule.

## Authenticated source and algebraic reduction

The original input is an explicitly encoded finite directed graph with vertices 0,...,n-1. For each arc (u,v), require x_v-x_u in {1,3} modulo five. Repeated arcs are idempotent; self-loops and opposed arcs force count zero. Let c be the number of underlying weak components (isolates included), t=n-c, r=m-n+c after removing repeated arcs.

Construct a deterministic spanning forest T. For a parent-child edge, its color increment is a_e+delta_e b_e, b_e in {0,1}. If the original arc is parent-to-child take (a_e,delta_e)=(1,2); in the reverse orientation take (-1,-2)=(4,3) modulo five. All assignments satisfying tree arcs correspond bijectively to c root colors and t forest bits. This yields exactly 5^c * 2^t forest-consistent assignments, **not 5^n**.

Every nonforest arc (u,v) gives a source-computable linear form along its fundamental forest path:

    a_i + sum_e C[i,e] b_e in {1,3} (mod 5).

This is an exact transformation, not a probabilistic hash. With C in F5^(r x t), let rho=rank_F5(C). Explicitly construct a column basis B and each column coordinate gamma_e in F5^rho so that C[:,e]=B gamma_e. Define P_0(0)=1, P_0(z!=0)=0 and

    P_{j+1}(z)=P_j(z)+P_j(z-gamma_j).

Then the **exact original-coloring count** is

    Z(G)=5^c sum_{z in F5^rho} P_t(z)
                  product_{i=1}^r [a_i+(Bz)_i in {1,3}].

**Proof:** P_t counts the binary forest vectors by their exact accumulated basis coordinate; Cb=Bz, so every chord is checked precisely. Each original coloring has a unique root palette and forest-bit representation. No SAT reduction, finite sample, or uncharged recognition is used for correctness.

## Simultaneous resource accounting and alternative points

The same deterministic rank-DP implementation physically stores the basis, source, a residue-state map, big integers and output. If tables are implemented on a one-tape sequential medium by linear scans and paid rewrites rather than RAM dictionary unit-cost accesses, conservative bounds are

    T_rank(N)=O((N+1)^12 (1+5^(2*rho+2))),
    S_rank(N)=O((N+1)^5 (1+5^rho)) writable bits.

A **separate** forest-bit streaming solver uses

    T_DFS(N)=O((N+1)^12 (1+2^t)),
    S_DFS(N)=O((N+1)^5) writable bits.

These bounds include source authentication, forest discovery, fundamental paths, modular basis computation, state addresses, state scans, arithmetic, tape traversal, retained data and output. They are intentionally loose upper bounds for two distinct actual strategies. **Do not combine the better time of the DP with the better space of the DFS into a fictitious single-machine bound.** Here N is an explicitly expanded vertex-and-arc input length, with n,m<=N; compressed binary-only vertex counts are not silently treated as expanded. A RAM transition count near poly(N)*5^rho is NOT a one-tape physical-time claim.

## Independent orbit-compressed variable elimination

Every original edge indicator and every exact factor from summing out a terminal sink is invariant under common addition of an a in Z5 to all its arguments. A nonempty k-scope factor therefore has precisely 5^(k-1) translation orbits, indexed by (x_2-x_1,...,x_k-x_1), rather than 5^k absolute tuples.

Products preserve invariance. Summing out v preserves invariance because shifting the remaining variables can be paired with a bijective shift of the summation variable. Thus exact bucket elimination can store one value per orbit for **every** nonempty original and generated factor; scalar factors have one entry.

The implemented all-input algorithm authenticates arcs, sums every original outdegree-zero sink of indegree <=3 into an exact parent factor, computes a source-derived min-fill order of induced primal width w, and performs exact normalized bucket elimination. A conservative sequential single-tape realization of this SAME algorithm has

    T_orbit(N)=O((N+1)^12 (1+5^(2*w+4))),
    S_orbit(N)=O((N+1)^5 (1+5^w)) bits.

Initial scopes can be w+1 variables and thus require 5^w invariant entries; it would be incorrect to assert a global 5^(w-1) space term. For each fixed k>=1, the quotient reduces the dense table size by exactly a factor **five**, but does NOT improve the exponential base as a function of unbounded width. No lower bound on arbitrary T5 machines follows.

**Falsifier:** A pinned unary factor [x=0] is not translation invariant. A one-vertex pinned source has one valid coloring, whereas falsely multiplying a quotient representative by five yields five. The orbit compression theorem excludes such unary lists or arbitrary absolute-color conditioning.

## Executed computational controls

Complete standard-library Python source and an independent original 5^n brute-force reference were executed locally. **1,357 deterministic checks, zero failures**, with a fixed random seed, comprise all 64 directed-pair orientation configurations on K3, seeded random sources n<=7 (including loops/opposed arcs), disconnected components, directed forests with reversed orientations, dense K6 (rank deficiency), the original T5 tournament, malformed vertices, terminal-sink wheels, and all 125 original assignments of a ternary factor checked against its 25-entry orbit table. Independent 5x5 adjacency-matrix powering verifies directed-cycle exact counts.

At directed-cycle length 500: n=m=500, c=1, t=499, r=rho=1; the rank-DP has at most **five** states versus 2^499 direct forest-bit choices. Its exact original count is:

    3273390607896141870013189696827599152216642046666584405007640931306735810808148275167174878805542304977224223904807438718238208782834023512071358995630

At the source private-sink wheel with 80 rim hubs: 161 original vertices, 240 arcs, induced primal width 3, orbit-table peak 2,000 entries versus 10,000 entries for 80 corresponding absolute-color ternary factors at input. Exact original count:

    739044147071729616580416051031916488010 = 5(3^80+1).

Published compact repo solver: `experiments/tmr/tmr3_t5_orbit_rank082_repo.py` (16 separately run deterministic comparisons). Full executed 1,357-check implementation and raw JSON are retained in the user reproducibility package; the repository raw audit JSON records that separate local execution. No native Turing-machine microcode or independent mathematical peer review was performed.

## Four verification gates

1. **DISJ sanity:** PASS restricted upper-bound sanity. No transfer of DISJ lower bounds.
2. **Relativization / algebrization:** NOT APPLICABLE to a separation.
3. **Simultaneous DTISP:** PASS restricted as symbolic constructive upper bounds with physically charged state-table scanning. DFS/DP are distinct choices, not one simultaneous best-of-both machine.
4. **Configuration counting:** PASS upper-bound consistency only. No claim that representation size forces runtime on another machine.

Preserve affine/Horn, degree-two, twins/modules, padding, trees, cycle and wheel easy families, conditioning symmetry failures, reduction overhead, cached/recomputed state, big-integer output length, and source-machine versus representation distinctions.

## Classification and open dependency

Bang-Jensen, Hell and MacGillivray (1988), *The Complexity of Colouring by Semicomplete Digraphs*, DOI 10.1137/0401029, establish NP-completeness for semicomplete targets with more than one directed cycle. The given T5 is a tournament with multiple directed cycles; this gives qualitative NP-completeness, but no measured linear blowup for SAT time-space exponents. Focke, Marx and Rzazewski (2024), *Counting List Homomorphisms from Graphs of Bounded Treewidth: Tight Complexity Bounds*, DOI 10.1145/3640814, is related prior art; it does not justify the pinned-case quotient.

**Next dependency:** C3-T5-RANK-RESIDUE-CUTSET083. Look for a certified checkpoint/split scheme between polynomial-space forest enumeration and 5^rho-memory DP, charging source rewinds and reconstruction. Preserve all four gates and easy-family controls. **P versus NP OPEN.**
