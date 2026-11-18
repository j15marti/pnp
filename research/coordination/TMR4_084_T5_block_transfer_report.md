# TMR-4/084: Tight three-bit block transfer for T5-CSP

Status: restricted mathematical theorem, finite computational audit; no unrestricted lower bound. Primary object is the explicitly authenticated five-symbol digraph homomorphism CSP with R(a,b) iff (b-a mod 5) is 1 or 3.

## Exact candidate D4-T5-BLOCK-REVERSE-084

A *complete* five-way adaptive FBDD has one five-valued query per original variable on every root-to-terminal path, with adaptive variable order permitted. Fix valid three-bit values 000, 001, 010, 011, 100 and reject invalid 101, 110, 111. A Boolean FBDD is full-decoder **block respecting** if the three bits of each queried source variable are read contiguously on valid paths, all original source variables are queried once, and invalid codewords cannot accept.

**Theorem.** For optimal diagram sizes in precisely these models, S5 <= S_block <= 6 S5. Forward: replace each five-way node by six binary internal nodes, decoding the prefixes 00 -> ports 0/1, 01 -> ports 2/3, 10 -> port 4/reject, 11 -> reject. This preserves every original assignment, exactly Z accepted valid codewords and 8^n-Z rejected codewords. Reverse: collapse each recognizable Boolean three-bit block to one five-way query by evaluating its five valid codewords; invalid words reject and adaptive block order remains read-once. This does not apply to arbitrarily interleaved Boolean FBDDs.

The factor six is *locally sharp for a standalone independent decoder* with five pairwise distinct continuation ports and invalid-code rejection: five valid leaves plus at least two invalid leaves require at least seven leaves and six binary internal nodes. An actual one-arc T5 source x->y gives five distinct residual predicates in y after reading x. This is **not** a universal Boolean FBDD lower bound.

**32-mask commutation theorem.** For every pair D,E of the 32 subsets of Z5 and for each of R and its transpose, the exact support filter F_R(D,E) commutes with injection of the five valid values into the three-bit codes. Thus validity-restricted Boolean codeword masks have exactly the same 32 unary-domain states as direct T5, not an asymptotically larger alphabet. Direct auxiliary-free CNF uses 3n Boolean variables and 3n+15m clauses (3 invalid-code clauses per vertex; 15 disallowed ordered pairs per arc).

## Four adversarial falsifiers

1. Naively accepting before checking invalid codes miscounts the empty one-variable source: five native accepts versus eight binary accepts.
2. Source-derived adaptive rejecting continuations cannot merge states that have queried *different sets of source variables*, or they may reread or skip variables. This issue was detected and corrected in the executed audit.
3. Arbitrary interleaved binary bit order violates the reverse theorem's block hypothesis; a large reverse simulation is not ruled out.
4. Six is optimal for the local independent decoder with distinct continuation ports, **not** an unconditional minimum for globally shared or reduced Boolean diagrams.

## SAME_REALIZATION resource ledger and verification gates

The same source-authenticated run charges canonical UTF-8 parsing, graph discovery and explicit arcs, all variable-order choices, memoized state including visited-set identity, five-way transitions and reject tails, creation of six binary nodes per native node, exact source and code assignment counts, every code-validity check, CNF materialization/evaluation, live cache, big integer precision, and output. No uncharged Fourier transform, external SAT oracle or free source certificate. The *reference source compiler* is exhaustive and can cost O(poly(L) 5^n), even when its resulting DAG is small. Conditional on an already correct complete explicit FBDD with S nodes, the standalone bit-block transducer costs O(S polylog(S+n)) bit operations, in addition to source validation and any requested CNF output. All upper estimates are paired to a real implementation, not an unrestricted time-space lower bound.

Gate 1: 138 canonical n<=5 source graphs, with ten malformed rejections and independent source hashes.
Gate 2: 109,330 pointwise native/forward/reverse comparisons, 1,048,528 exhaustive binary-code evaluations, 45,008 actual forbidden-clause checks; 21 additional adaptive FBDDs with 2,625 native and 10,752 code evaluations, of which 17 show genuinely branch-dependent variable order.
Gate 3: 2,048 directed/reversed 32-mask pairs, exact adaptive three-bit decoder optimizer reporting six nodes, and genuine x->y five-distinct-residual source.
Gate 4: independent JavaScript audit performed 109,330 native evaluations, 1,048,528 coded evaluations, 1,048,528 CNF checks and 2,048 mask tests, with identical results. Python and JS repeated byte-identically, unexpected failures zero.

Python raw JSON audit SHA-256: b4bfa7e335387bdbdbfb26229c53a8474f23514222485a0e64af6247093f148d. Full executable Python/JavaScript, sources, checksums and exact results are included in the run evidence ZIP. This draft branch contains the theorem/report/handoff, not the full executables. FINITE EVIDENCE = COMPUTATIONAL; native physical Turing-machine microsteps and independent mathematics peer review remain OPEN.

**Next: D4-T5-INTERLEAVED-CODE-FBDD-SEPARATION.** Search for a genuine source-authenticated asymptotic interleaving advantage, or prove a quantified simulation, after all legal simplifications and with source compiler costs charged. The 2009 Barto-Kozik-Niven NP-completeness theorem for this template stands, but no result here establishes P!=NP. P versus NP remains OPEN.
