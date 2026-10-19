# MIN-FREE-SIGMA2-MERGE17: exact search-MCSP streaming oracle reduction

**Run:** 2026-10-19 23:36 Asia/Seoul, finalized 23:47. **Role:** independent :36 P/NP cross-track RED TEAM. **Status:** theorem established in stated model, independent review pending. P versus NP remains OPEN.

## Original no-gos recovered first

- OUTPUT-CARDINALITY-CEILING3: ordinary output-identity/fooling-set counting yields at most O(s log s) bits, not an MMW s^{omega(1)} workspace lower bound.
- FULL-MCSP-PREFIX-CEILING15 and REP-MAINTENANCE-CEILING5: a uniform all-input one-pass representative algorithm uses O(s log s) space but 2^{O(s log s)} worst-case update time, leaving MMW's simultaneous small-space/small-update lower-bound target open.
- SIGMA2-STREAM-GUARD16 already proposed an existential any-witness Σ2 predicate; its full primary-source-aligned query accounting and independent gate encoding audit remained to be established.
- DETREE/RS-HADAMARD/sparse-co-sparse/coding-distance results are restricted easy slices, not full-MCSP hardness; CHMY threshold descent, OPS cofinal nonuniform circuit excess, and ARC all-input arbitrary-decider contraction remain OPEN.

## Four falsifying ideas proposed *before* new primary literature

1. Attack uncharged unbounded input fan-in of arbitrary A-oracle gates and the O(s log s) witness encoding. Repair only under the exact encoding and size convention of the primary theorem.
2. Try to replace full-prefix equality with a short sample or histogram. Counterexample: C=NOT x0 and D=NOT x1 have matching first sample, and D matches the requested third bit, but disagree on the unobserved second bit; for n=3,s=1 no correct circuit for actual prefix (1,0,0) exists.
3. Check whether a smallest-circuit/lex-minimization rule is truly needed for correct one-pass witness maintenance. Replace it by an arbitrary consistent circuit and test full output on all source strings.
4. Challenge promotion of a Σ2 oracle-accelerated algorithm to an ordinary deterministic machine. Count actual Σ2 queries and demand justified P=NP collapse for A in PH, not a free oracle under ordinary resource accounting.

## Primary sources and exact model check

McKay, Murray, and Williams (STOC 2019), original author manuscript, https://people.csail.mit.edu/rrw/MCSP-MKTP-stoc19.pdf : Theorem 1.2 and Section 4 give a one-pass search-MCSP^A algorithm using Σ3SAT^A oracle gates. Their Stream-Merge^A[s] chooses the lexicographically first **minimum-size** witness circuit, with a claimed 100s log s-bit bounded witness encoding, while the correctness induction needs only some size-at-most-s consistent circuit. Their Theorem 1.3 requires *both* poly(s) streaming storage and poly(s) update time for full search-MCSP^A[s], with s>=n and A in PH, to obtain a P vs NP consequence. Their Section 2.1 also explicitly charges the minimum-size/lex choice with an additional universal competing-circuit quantifier. In this new construction the minimum-size condition is abandoned. In the absence of independently verified alternative A-gate encoding conventions, all bounds below adopt MMW's own s>=n and t=Theta(s log s) encoding.

Cheraghchi–Hirahara–Myrisiotis–Yoshida, STACS 2021, https://doi.org/10.4230/LIPIcs.STACS.2021.23 : randomized one-tape with separate one-way read-only input, threshold mu2 and two-sided error, not this oracle-streaming algorithm. Oliveira–Pich–Santhanam, Theory of Computing 2021, https://theoryofcomputing.org/articles/v017a011/ : GapMCSP nonuniform circuit lower-bound magnification quantified for sufficiently small beta; not supplied here. Fortnow–Lipton–van Melkebeek–Viglas, JACM 2005, https://doi.org/10.1145/1101821.1101822 : deterministic random-access SAT joint time-space, not supplied here.

## Theorem and proof

Fix n<=s, N=2^n, A arbitrary, and MMW's polynomial-time uniformly decodable descriptions of A-oracle circuits of size <=s using L=O(s log s) bits. Let previous circuit C agree with all source bits at addresses <i and let b=(b_0,...,b_{t-1}) be the new source block. For a partial descriptor prefix p (length <=L), define

 Q_A(C,i,b,p) = 1 iff there exists a well-formed size<=s A-oracle circuit D extending p such that
 (a) forall x in {0,1}^n with x<i, Eval_A(D,x)=Eval_A(C,x); and
 (b) forall j<t with i+j<N, Eval_A(D,i+j)=b_j.

The candidate descriptor has O(L) bits, and one assignment x has n bits. Well-formedness and all Eval_A calls are deterministic poly(L+t+n)-time procedures with oracle A. Consequently Q_A belongs to Sigma_2^{P,A}. The block conditions are polynomial-length and deterministic given D; the prefix condition requires universal x. The description of the query is O(L+t+n) bits; for t=Theta(L), n<=s, this is O(L). A deterministic client first queries Q_A(...,empty). If false it rejects permanently. Otherwise, for j=1,...,L, it asks whether a valid candidate extending the currently fixed bits plus 0 exists. If yes, append 0; otherwise append 1, preserving the existence invariant. After L queries the unique descriptor D is valid, consistent with all earlier observations, and matches the entire new block. No assumption of minimum size is made. The next round uses D as C. Induction on the blocks proves the exact witness-or-reject output for all N-bit truth tables.

The client uses O(L+t+n)=O(s log s) workspace, makes at most L+1 membership queries of length O(L) per block, and has O(L^2 polylog(L)) local time per block by serial query construction, with polynomial update/reporting time relative to unit-cost Sigma_2^{P,A} oracle answers. No source replay is needed. For A in PH, under P=NP one has PH=P and Sigma_2^{P,A}=P, so this gives a genuine polynomial-update algorithm. Without such a collapse, the queries are NOT free: this is an oracle-relative upper bound only. This is a weaker oracle **level** than the published specific Sigma_3-minimization construction, not an unconditional improvement to ordinary SAT time or a strict oracle-hierarchy separation.

All algorithmic bounds depend on the MMW size/description convention. A different library allowing arbitrary-fanin oracle gates with free pin lists may have larger descriptions and must be separately charged; its `s` is not silently identified with the MMW parameter.

## Independent finite test, reproducible source

`/mnt/data/pnp_sep_redteam17/sigma2_arbitrary_merge17.py`, seed 202610192336; raw results `SIGMA2_ARBITRARY_MERGE17_raw.json`. The finite gate library is 2-input AND/OR and unary NOT with explicit padded circuit descriptions and output pointers. No actual A-oracle was executed, and no polynomial ordinary-world oracle evaluator is claimed.

- n=2,s=1: 32 descriptions, 6 distinct YES tables, all 16 source words tested.
- n=3,s=2: 3867 descriptions, 40 YES tables, all 256 source words tested.
- n=4,s=2: 12064 descriptions, 90 YES tables, 32 seeded source words tested.
- In total 304 source words, 2624 stream positions, 3810 existential feasibility calls, 30743 descriptor-bit oracle queries and 20079721 candidate constraint checks. Zero false accepts/rejects or assertion failures.
- The intentionally nonminimum circuit selector used a larger-than-necessary circuit at 1205 streamed steps. The full output remained correct. Another 671 steps exhibited nonminimum size relative to all currently consistent circuits for a lexicographic-bit selector.
- The sample-only attack has n=3,s=1, C=NOT x0 producing prefix (1,0,1), D=NOT x1 producing (1,1,0): sample position 0 and new position 2 pass, but position 1 fails and no size-1 circuit realizes (1,0,0).

Finite n,s controls include s<n and serve only to check mechanism correctness; the asymptotic MMW claim explicitly assumes s>=n and relies on the symbolic argument above. The Python operation counts are not RAM peak-memory measurements.

## Proof DAG

- ESTABLISHED in declared MMW encoding/model: any-consistent-witness streaming merge belongs to Sigma_2^{P,A}; full one-pass exact search-MCSP^A algorithm with O(s log s) client workspace and polynomial client update time relative to that oracle, with minimum-size requirement eliminated.
- COMPUTATIONAL: 304 finite sources, 20,079,721 explicit candidate constraints, zero failures.
- FALSIFIED/RETIRED: sample-only earlier-prefix equivalence; claim that MMW's *minimum-size witness selection* is necessary for semantic correctness; any direct promotion of an oracle-relative upper bound to an unconditional SAT-machine lower bound.
- OPEN: uniform unconditional polynomial-time evaluation of the existential/universal relation, MMW-model superpoly(s) simultaneous workspace/update lower bound, CHMY same-one-tape cofinal threshold descent, OPS every-small-beta GapMCSP circuit excess, and all-input hereditary ARC/FLMV contraction. P vs NP OPEN.

## Required role-targeted next falsifiers

:00 CHMY: instantiate the exact local generator and prove/refute both source/target MCSP promises with retained random-error and single-work-tape fusion. Refuse any inference from Σ2 streaming oracle to CHMY one-tape.

:12 MMW: determine whether the min-free Sigma2 membership query can be computed uniformly in poly(s) on ALL source prefixes without assuming P=NP. Test dense, sparse, affine and pseudorandom families; do not treat relative oracle operations as free updates.

:24 ARC: try delayed/padded solvers and include the cost of Σ2 answers; check whether an alleged contractor repeats parent-scale queries or retains multiple ancestor states. No shortcut from this streaming oracle to FLMV.

:36 RED TEAM: independently inspect the O(s log s) A-oracle circuit encoding of MMW, variable arities, canonical padding, oracle-query length, serial bit self-reduction and malformed descriptors. Try to disprove Sigma2 class membership by a concrete A-oracle encoding, not a changed machine without explanation.

:48 SYNTHESIS: compare prior SIGMA2-STREAM-GUARD16 with new explicit MMW primary theorem and reproducible padded-gate code. Record an independently supported level reduction for **this** merge task, but no complexity separation and no assertion of first discovery. Maintain root main.tex read-only while incomplete.

## Source references

[1] McKay DM, Murray CD, Williams RR. Weak Lower Bounds on Resource-Bounded Compression Imply Strong Separations of Complexity Classes. STOC 2019. https://people.csail.mit.edu/rrw/MCSP-MKTP-stoc19.pdf
[2] Cheraghchi M, Hirahara S, Myrisiotis D, Yoshida Y. One-Tape Turing Machine and Branching Program Lower Bounds for MCSP. STACS 2021. https://doi.org/10.4230/LIPIcs.STACS.2021.23
[3] Oliveira IC, Pich J, Santhanam R. Hardness Magnification Near State-of-the-Art Lower Bounds. Theory of Computing. 2021. https://theoryofcomputing.org/articles/v017a011/
[4] Fortnow L, Lipton R, van Melkebeek D, Viglas A. Time-Space Lower Bounds for Satisfiability. JACM 2005. https://doi.org/10.1145/1101821.1101822

<!-- END_OF_VERIFIED_REPORT::REDTEAM::MINFREE_SIGMA2_MERGE17::P_VS_NP_OPEN -->
