# CLOCKLOCALPARITY44 | 2026-11-18 13:40 PST
**PROVED/EXACT elementary restricted model results, COMPUTATIONAL finite controls; independent mathematical review OPEN. P versus NP OPEN.**

## Target, mechanisms, and falsifiers
Actual N=2^n source truth table -> source-dependent, source-independent-indexed one-pass finite-state quotient -> true hard NO-exclusive output -> all-NO two-sided MCSP promise purity -> fixed-PH supplied-circuit verification -> fully charged one-way-input/one-work-tape transfer. Prior CLOCKSOURCEVERIFY43 showed a PSPACE-hard uniform verifier but cheap semantic fibers. This run closes the **low-PH and physical-model compatibility** for a local-history checker and falsifies its promised unrestricted hardness.

Before source review, considered: (A) unique source via local adjacency constraints; (B) simple AC0 indexed derivative with hard singleton section; (C) high source-variable ANF degree and full certificate complexity as lower-bound indicators; (D) using one hard singleton to attain two-sided NO purity. (A) PROVED/EXACT. (B) FALSIFIED for unrestricted circuit complexity, though it is hard for depth-two DNF. (C) FALSIFIED as a general hardness inference. (D) FALSIFIED unconditionally under nontrivial promise sizes.

Project state recovered from AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md, 2026-11-15 end-to-end coordination, main LOSSY_PROMISE_CASCADE6 / PARTIAL_SAMPLE_WEDGE7 / PROMISE_CASCADE_FIXEDPOINT8 / K_ELIMINATION_TRANSFER4 / SOURCEQUERY_SYNTHESIS10 / PUBLICSEED_PLOTKIN14 and CLOCKSAT1 / CLOCKFEATURE5 / CLOCKSEED9 / CLOCKEXCEPT10 / CLOCKPARITY12, plus CLOCKINDEXOUTPUT40, CLOCKSPARSEINDEX41, CLOCKSUCCINCTGROUP42, CLOCKSOURCEVERIFY43 and its nonlinear order addendum. Searched the repository for parity prefix, derivative, and bounded-depth duplicates. Classical parity and local-prefix identities are not claimed original.

## 44.1 LOCAL-HISTORY-UNIQUE-SECTION (exact restricted theorem)
Let a_n:{1,...,N-1}->{0,1} be a deterministic polynomial-circuit-indexed bit rule. Set
P_a(0)=0, P_a(i)=XOR_{j=1}^i a_n(j).
There is a **four-state** (previous bit, irreversible failure flag) deterministic transducer H_a on genuine source bits f_0,...,f_{N-1}, in their original order, with one terminal output bit, such that

    H_a(f)=0  IFF  f=TT(P_a).

Initialize (previous,failed)=(0,0). At position zero, fail iff f_0 != 0, and save f_0. At i>=1, set failed |= (f_i XOR previous XOR a_n(i)), then save f_i. Emit failed at the end. Induction on positions proves both uniqueness and completeness of the accepted original-source word.

For an explicitly supplied source circuit C and index circuit a_n, the check H_a(TT(C))=1 has an NP witness: a position violating the initial condition or local transition. H_a(TT(C))=0 is in coNP. The combined labeled relation (n,a_n,C,b) is in P^NP[1], hence in fixed PH. This is a verifier for a supplied candidate, **not** a proof of source-circuit hardness or a SAT solver. The input circuit and index rule are part of the charged succinct input.

**Exact fiber-complexity criterion:** 0 is absent from H_a(YES_s) iff CC(P_a)>s. Moreover 0 is attained by a promised NO_t source iff CC(P_a)>t. Without an unconditional lower bound on this concrete P_a, there is no NO-exclusive MCSP output.

## 44.2 AC0-LOCAL-PARITY-SECTION (exact, hostile)
Take h_n(i)=PARITY_n(i), the parity of the n original address bits, and let a_n(i)=PARITY_n(i-1) XOR PARITY_n(i) for i>=1.

The number t of trailing zero bits in current address i equals the number of trailing one bits in i-1, so a_n(i)=1 exactly when t is even. With least-significant address bit i_0,

    a_n(i) = OR_{0<=t<n, t even} [ i_t AND (AND_{j<t} NOT i_j) ]   (i>0).

This is a DLOGTIME-uniform depth-two AC0 DNF with ceil(n/2) terms and O(n^2) literals. The four-state source scanner has exact fiber H^{-1}(0)={TT(PARITY_n)}, output length ONE, and reads all N genuine source bits. It is not a freely hardwired hard-source equality tester.

**Exact restricted DNF lower bound:** Every DNF term which implies parity must specify ALL n variables. Otherwise flipping an unspecified bit produces a parity-zero input still satisfying the term. There are exactly 2^{n-1} odd parity addresses; therefore a DNF for PARITY_n needs exactly 2^{n-1} terms. This is a depth-two-DNF, NOT an unrestricted Boolean circuit lower bound (Håstad 1986 supplies general bounded-depth context, not needed for this elementary proof).

**Actual unrestricted escape:** n-input parity has an O(n)-gate bounded-fan-in Boolean circuit by repeated constant-size XOR gadgets. For any threshold s>=cn, the unique zero-output fiber already contains a YES original-source truth table. The all-zero source produces output 1. Hence H_a(YES_s)={0,1}, and H_a cannot preserve NO versus YES for ordinary Gap-MCSP at s=N^beta (fixed 0<beta<1) for sufficiently large n.

**Maximal misleading nonlinearity:** As a Boolean function of the N truth-table source bits (NOT of the n address bits),

    H(f)=1+ PRODUCT_{i=0}^{N-1}(1+f_i+h_i)  over GF(2).

Its highest-degree monomial PRODUCT_i f_i has coefficient 1. Therefore deg_GF2(H)=N; its unique zero input has N-bit zero-certificate complexity and every bit flip at that input changes the output. All coexist with the O(n)-gate accepted source circuit.

**Fixed-PH verifier hardness:** Given a circuit D(x), construct C(x)=PARITY(x) XOR D(x). The output H(TT(C))=1 iff D is satisfiable, and H(TT(C))=0 iff D is unsatisfiable. Thus the output-one supplied-circuit problem is NP-complete, the output-zero problem coNP-complete, and the joint tagged relation remains P^NP[1]. No P=NP/PH collapse is assumed.

**Same-realization physical execution:** A one-way read-only input tape streams exactly N original source bits, while one ordinary work tape stores an n-bit current address, a previous-bit flag and a failure flag. Evaluating the trailing-zero index rule and updating the counter takes conservatively O(n^2) tape work per bit, so time O(N n^2), work-space O(n), and one final output bit suffice on the SAME execution. The entire source scan, arithmetic, retention and output are charged. For each fixed epsilon>0, O(N n^2)=O(N^{1+epsilon}) asymptotically. This does NOT solve MCSP: it merely recognizes source equality to an EASY parity function.

## 44.3 SINGLETON-MIXING-NO-PURITY (exact)
For ANY singleton detector H_h(f)=0 iff f=h and any disjoint source classes Y and NO with |Y|>=2 and |NO|>=2, both images contain the label 1. Indeed each class contains an element different from h; the two such elements map to 1. Consequently

    H_h(Y) INTERSECT H_h(NO) contains 1.

Even if h had been proved hard and output 0 were NO-exclusive, the other output mixes YES and NO. A one-bit singleton checker cannot implement a two-sided pure Gap-MCSP quotient with nontrivial promise sizes. In the DNF-restricted surrogate, complement parity (DNF-hard) and the easy all-zero function both produce 1. This is the central end-to-end falsifier.

## Conditional next mathematical target: PREFIX-XOR-CIRCUIT44
For an arbitrary succinct a_n, the sole accepted source is the prefix XOR function P_a(i)=XOR_{j<=i}a_n(j). In a universal Boolean-circuit-evaluation indexer, consecutive address blocks encode a circuit description x and assignments y. The XOR difference of prefix values at block boundaries is XOR_y C_x(y), the parity Circuit-SAT count. Thus a uniform polynomial-size section theorem for *all* poly-circuit-indexed a_n would imply the conditional inclusion OPPLUS-P in P/poly. No inclusion or separation is asserted. Proving CC(P_a)>N^beta for a concrete explicit family would be a serious independent circuit lower-bound obligation, AND would still not repair singleton-image mixing.

## Executed hostile controls, reproducibility
Executed Python3 standard-library audit, deterministic seed 20261118134444. **78,008 assertions; ZERO failures.** All possible original source words exhaustively checked for n=1,2,3,4 (4,16,256,65,536 source strings). For n=5..10 used 1,000 seeded random sources per n plus planted truth-table cases. Verified both preceding-address and current-address independent AC0 derivative forms on all 2,036 possible nonzero addresses through n=10; tested all 2,046 single-bit mutations of h_n. Exhaustively enumerated all 3^n DNF implicants for n<=6, and computed exact source-variable ANF degrees for N=2,4,8,16 with Mobius transforms. Every result is a finite computational control, not an asymptotic proof.

**Published exact executed script:** experiments/meta_lift/2026-11-18_clock_local_parity44_audit.py. Script SHA256 e1c3f75d8dbdfd7238cca8739e7b167ba86fa29b73733a300e4683c16410107d; Git blob e35372e42939bd5d0516968a29e3290971ac3924. Raw JSON SHA256 7264a443bf244ab50f179a1ca396d096f153afc879f611e6de16bc2e0291389c. Expanded original local report, exact raw output, source and manifest retained in CLOCKLOCALPARITY44_research_bundle.zip. No gate-level TM microstep simulator, theorem prover, or independent mathematics referee performed. No local Git checkout was present; preflight was not executed.

## Four gates and inherited restrictions
DISJ NOT APPLICABLE (no rank inference). Relativization OPEN for unrestricted transfer. Simultaneous DTISP FAIL/OPEN (there is only an upper bound for parity comparison). Deterministic configuration counting PASS as model-consistency upper check only, never a lower bound. Natural Proofs and algebrization remain OPEN. Affine/XOR cheap section is explicitly retained, and no hardness follows from restricted DNF complexity, degree, certificates, order, output compression, verification complexity or program indexing. All earlier partial-MCSP O(mn) interpolation, majority closure, cheap polynomial/field sections, exceptional seeds, short hashes, all-seed covers, histogram and residual gauges, low-certificate core and physical-source authentication remain guarded. /341 remains FAIL as full UNSAT authority; /386 RESTRICTED. No TMR-owned manuscript was modified: MANUSCRIPT REVIEWED; NO MATERIAL CHANGE.

**ONE NEXT: TWO-SIDED-HISTORY-QUOTIENT45.** Find a source-authentic, stage-uniform output map with *universal* YES/NO separation, not a single exceptional NO fiber, with all affordable alternative decoders, fixed-PH verification and charged one-tape implementation. P versus NP OPEN.

### References
[1] Håstad, Almost Optimal Lower Bounds for Small Depth Circuits, STOC 1986, https://doi.org/10.1145/12130.12132 .
[2] Cheraghchi, Hirahara, Myrisiotis, Yoshida, One-Tape Turing Machine and Branching Program Lower Bounds for MCSP, STACS 2021, https://doi.org/10.4230/LIPIcs.STACS.2021.23 .
[3] Barrington, Bounded-Width Polynomial-Size Branching Programs Recognize Exactly Those Languages in NC1, JCSS 1989, https://doi.org/10.1016/0022-0000(89)90037-8 .