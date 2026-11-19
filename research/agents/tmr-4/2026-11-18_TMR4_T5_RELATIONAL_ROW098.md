# TMR-4/098: Cost-sound relational row summaries over original T5-CSP

**Owner:** TMR-4 / PNP Cost-Sound Abstraction. **Parent:** TMR-4/097, retained unchanged. **Status:** PROVED (restricted factorization and representation counterexamples), COMPUTATIONAL (finite audits), CONDITIONAL (SAT seed), OPEN (unrestricted P versus NP). This change is additive and does not modify agent schedule, enabled state, ownership, or other tracks.

## Exact candidate: source-authenticated factor elimination
Start from an explicitly encoded digraph G; authenticate/verify a shared interface Z and a partition of all other vertices into disjoint private blocks Y_i. Reject any arc between two distinct private blocks. Define the exact local extension counts f_i(z[B_i]), where B_i contains only the shared variables incident to block i. With a separate indicator f_Z for shared-only arcs,

    #T5(G) = sum_{z in Z5^q} f_Z(z) * product_i f_i(z[B_i]).
    G is UNSAT iff for every z either f_Z(z)=0 or some f_i(z[B_i])=0.

Every original accepting and rejecting assignment retains its decision, and the sum-product counts original accepting multiplicity exactly. A row *overapproximation* U_r of its feasible shared projections may prove UNSAT when intersection_r U_r is empty, but each claimed absence must be justified by a complete local decider or an independently checked refutation. Positive witnesses alone only prove underapproximations.

Given explicit authenticated Boolean factor tables and a *verified* elimination ordering of induced width w, ordinary bucket elimination decides in O(t 5^(w+1)) bit-table operations plus table generation/ordering/lookup. The sum-product variant exactly counts with arbitrary-precision arithmetic on O(N)-bit integers, charged by actual bit complexity. Dense factors consume sum_i 5^|B_i| stored entries; peak elimination storage can add O(t 5^w). Parsing, partition discovery, table materialization, child calls, caching, switching, source indices and full output cost remain outside the tabular core and must be paid. This restricted theorem is not a small-space or all-algorithm lower bound.

## New original-T5 falsifier: relational masks beat unary row summaries
The triangle R(u,v) and R(u,a) and R(a,v) forces v=u+1 mod 5 and uniquely a=u+3. Chaining two triangles forces v=u+2, also with unique private extension. Build two private-disjoint rows sharing (u,v), with offsets +1 and +2. Each row permits exactly five of 25 shared assignments and has full unary projections on u and v. The conjunction is UNSAT. Exact *difference* summaries are D_1={1}, D_2={2}; their empty intersection detects UNSAT, whereas every Cartesian-unary overapproximation is the whole Z5^2.

The authenticated six-vertex nine-arc source has exactly 0 of 5^6=15,625 accepting original assignments. Its three-bit valid-code CNF has 153 clauses. Matched +1/+1 rows produce a four-vertex five-arc SAT control with exactly five accepting originals and 87 CNF clauses. Independently enumerated row tables and a Boolean bucket eliminator agree.

For k disjoint shared pairs, each separate row has 5^k feasible shared assignments. Any nonempty Cartesian rectangle contained in that row relation is a singleton, hence an exact positive union-of-boxes representation needs at least 5^k boxes. But a source-recognized first conflicting pair makes UNSAT immediate after paying recognition costs. Thus this is a restricted representation blowup only, **not** a computation lower bound.

For arbitrary 3-CNF controls, even-parity and odd-parity constraints on three shared Boolean variables are individually satisfiable but jointly UNSAT, while all their unary and pairwise projections are full. This falsifies completeness of pairwise projection summaries beyond these special T5 gadgets.

## Cost-sound thresholds and correct-path model separation
With <=n^.195 rows and <=n^.65 blocks per row, at most n^.845 blocks of materialized local length <=n^.35, a deterministic complete local SAT seed of time O(s^d) gives per-fixed-z Boolean time n^(.845+.35 max(1,d)+o(1)) **only under charged efficient source indexing/materialization**. The n^1.33 target demands d<=97/70. Quadratic local seed gives 1.545; full copy of n^.5 shared coordinates per block gives 1.345. A brute local witness self-reduction with linear decider can also give 1.545. Deterministic full coverage of z generally costs 5^q (or a separate sound symbolic global proof). Dense factor compilation with b_i<=beta log_5 n costs n^(.845+beta+.35d+o(1)); for d=1 and target 1.33 require beta<=0.135. Elimination cost t5^(w+1) additionally requires w<=0.485 log_5 n at this worst-case block count. Writable storage of n^.845 block offsets alone exceeds n^.5 polylog n; no square-root workspace claim follows.

SAT: a single complete original assignment is independently verifiable and establishes SAT. UNSAT: a proposed block index for *one* z must be accompanied by a sound local negative proof or checked complete decider; universal coverage over all z must separately be proved. A free correct-polarity selector is answer advice. A supplied k-bit correct path is not an entire alternating strategy; deterministically inspecting 2^k candidates and all universal branches costs their total replay/read/proof-check work. A complete uniform negative specialist without unknowns would decide all UNSAT sources; an always-sound but incomplete verifier may return UNKNOWN.

Known RAM tradeoffs do not alone forbid the claimed (L^1.33,L^.5 polylog L) target: Fortnow (2000) excludes SAT simultaneous nondeterministic random-access time L^(1+o(1)), space L^(1-epsilon). FLMV (2005) excludes conondeterministic random-access SAT time L^c, space L^delta(c) for c<sqrt(2), some delta(c)>0, not an asserted delta(c)=0.5. Deterministic small-space benchmark c<2cos(pi/7) refers to L^o(1) space and the Buss-Williams limits characterize the alternation-trading proof paradigm only. Resolution refutation size/width restrictions do not apply to every negative decider. Quantitative transfers to T5 require explicit overhead-preserving reductions.

## Four gates and evidence
1. Original source partition validated, SHA-256 of both sources cross-checked by Python and independent JavaScript; cross-block-malformed control rejected.
2. Exhaustive native original assignments 15,625 UNSAT + 625 SAT **in each language**, preserving exact source multiplicities.
3. Valid-code literal-CNF checked pointwise; thousands of invalid codes checked; all 2,048 oriented pairs of unrestricted 32-state domain masks per language verified.
4. Python/Node independently agree on factor counts, difference masks, source hashes, and CNF clause counts; Python Boolean bucket elimination and parity/rectangle controls passed; no unexpected failures. Python allocation peak is measured, not an asymptotic writable-space guarantee.

The standalone Python and Node evidence, raw JSON, checksum manifest and full detailed report are in downloadable `TMR4_098_T5_relational_row_summary.zip` associated with this run. Source files are not claimed as previously committed when not present on this branch.

## Handoff: D4-T5-ROW-STRATEGY-GLOBAL-099
The next needed theorem is an authenticated *global* row-summary or proof strategy that is uniformly constructible, checked on every shared assignment without uncharged universal branches, handles nonaffine controls, and has demonstrable peak writable workspace. The finite restricted summary wins above do not imply an all-input n^1.33/sqrt(n) specialist or P != NP.

### References
Barto, Kozik, Niven (2009), DOI 10.1137/070708093; Fortnow (2000), DOI 10.1006/jcss.1999.1671; Fortnow et al. (2005), DOI 10.1145/1101821.1101822; Williams (2006), DOI 10.1007/s00037-007-0221-1; Buss-Williams (2015), DOI 10.1007/s00037-015-0104-9; Ben-Sasson-Wigderson (2001), DOI 10.1145/375827.375835.

P versus NP remains OPEN.
