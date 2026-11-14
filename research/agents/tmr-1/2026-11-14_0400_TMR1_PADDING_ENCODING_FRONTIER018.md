# TMR-1/018: the honest-encoding boundary for an all-machine 3-SAT bottleneck

**Pacific timestamp:** 2026-11-14 04:00 PST (America/Los_Angeles). **Role:** TMR-1 Machine Model Lead. **New claim:** TMR1-PAD18, CANDIDATE/RESTRICTED pending independent TMR-5/TMR-2 review. **Actual finite execution:** COMPUTATIONAL. **Unrestricted standard-encoding 3-SAT separation:** OPEN.

## 1. Question and exact fixed-machine scope

The target of the new TMR directive is the following, on **one fixed, explicitly specified, ordinary polynomially balanced bit encoding** E of valid proper 3-CNF formulas:

$$
Q_E:\quad
\forall A\in\mathrm{TotalCorrect}(E)\;
\forall k\in\mathbb N_{\ge1}\;\forall C>0\;\forall L_0\;
\exists F\in\mathrm{Valid}(E):
\ |F|\ge L_0,\quad T_A(F)>C(|F|+1)^k.
$$

A is one fixed finite total uniform deterministic multitape program for ALL lengths; it has one locally moving read-only source head initially on a left endmarker, finitely many ordinary writable tapes, fixed alphabets, a fixed control, SAT/UNSAT/MALFORMED terminal outputs and fully charged transitions. Space is the number of *visited* writable cells of this same execution. Every read, reread, parse, address, comparison, input copy, machine translation and brute-force step is charged. The source bit length L is not the number of clauses or variables.

This report tests a possible overextension: that Q should hold for *any* injective, answer-preserving representation of the same formulas, even if the representation is exponentially padded. That overextension is false. The correction is to require polynomial-time, uniform, two-way translations when claiming model/encoding invariance.

## 2. Lemma A: the all-exponent Q target is exactly the absence of a polynomial valid-input decider

**Hypotheses:** E has a deterministic polynomial-time syntax checker; every correct A is total on binary inputs and returns the correct two labels on valid formulas (with MALFORMED on invalid encodings).

Then Q_E holds if and only if E-3SAT has no fixed deterministic polynomial-time decider.

**Proof.** If a polynomial-time tri-label decider exists, use its exponent k and a suitable constant C: the displayed universal statement fails. Conversely, failure of Q_E gives ONE fixed total correct A, ONE k,C,L0, such that all valid encodings of length at least L0 take at most C(L+1)^k. For each of the finitely many shorter valid strings, totality provides a finite maximum runtime. Increasing C gives one polynomial bound on A over *all* valid strings. Prepend E's fixed polynomial syntax recognizer and run A only on valid strings. The resulting one fixed deterministic program is polynomial on all binary strings and decides E-3SAT. The fixed finite cutoff changes a constant; it does not select a different program for every length. QED.

**Status:** elementary proved implication in this report, kept CANDIDATE pending a second role's review; importantly, it is an equivalence/reformulation, **not** independent progress toward P != NP.

## 3. Lemma B: two-way uniform polynomial encoding reductions preserve Q

Let E and D be two formula encodings, both with polynomial-time validity recognition. Suppose there are *fixed* total deterministic polynomial-time functions f and g such that each valid E formula maps under f to a valid D formula with the SAME SAT/UNSAT label, and each valid D formula maps under g to a valid E formula with the SAME label. The maps need not be bijections, nor retain exact variable names, nor have a predeclared matching size at each input length.

For a hypothetical polynomial-time D-decider B, a single compiled E-program computes f(x) on fully charged work tape and then simulates B on that tape. If f uses at most a(L+1)^d transitions, it outputs at most a(L+1)^d+O(1) bits. If B's polynomial time on valid inputs is at most b(M+1)^k, the fixed compiler's time is polynomial in L, for example O_A((L+1)^{d(k+1)+c}) with a constant c accounting for the declared standard multitape simulator. This charges representation construction, buffer space, every input reread, and the simulated B input-port movements. Thus D in P implies E in P. Apply g for the converse. Lemma A then gives

$$
Q_E\ \Longleftrightarrow\ Q_D.
$$

**Scope:** invariance of **polynomial versus superpolynomial**, not preservation of an individual runtime exponent, exact T/S tradeoff, or particular hard formula. The two fixed reductions exist before the input length varies. In particular, a proof cannot select a fresh enormous table/program independently at every L.

**Relation to literature:** the project argument uses ordinary charged polynomial many-one reductions, not the more specialized claim that all NP-complete sets are polynomial-time isomorphic. Cook (1971) establishes foundational polynomial reducibility; Berman and Hartmanis (1977) analyze isomorphisms/padding with additional conditions. Neither source provides an unrestricted SAT time lower bound. The proof above states its own hypotheses.

## 4. Concrete counterexample to unrestricted "semantic encoding independence"

Fix **any standard explicit** 3-CNF source encoding E whose syntax is checkable in polynomial time and O(L) space, with at least one data bit per literal occurrence (all ordinary explicit encodings satisfy this). Define a new syntactic representation of the *same* formula:

$$
p(x)=1^L\,0\,x\,0^{2^L},\qquad L=|x|.
$$

The initial unary block specifies the length of the genuine E-source x. The single 0 delimits it. The suffix must be EXACTLY 2^L zero bits, not arbitrary free padding. The complete bit length is

$$
N=|p(x)|=2L+1+2^L.
$$

A valid padded input is one whose extracted x is a valid E-encoded proper 3-CNF and whose complete prefix/suffix structure matches. Its SAT/UNSAT label is exactly that of x. The same mapping preserves both answer labels and all formula semantics, and is injective; it *does not* preserve input size polynomially.

**Fixed deterministic polynomial-N decider, including malformed handling:**

1. Count the actual padded input length N using a charged binary work counter. Inspect the unary length prefix. If it is longer than floor(log2 N), reject MALFORMED immediately: a valid suffix would be longer than N. This prevents constructing exponential objects on invalid inputs.
2. Copy the following L-bit E-source to a work tape, and check E's proper 3-CNF grammar. Count suffix characters and reject if there is any nonzero suffix bit or the count differs from 2^L. All binary counting, local head moves and copies are charged. The counter width on a valid input is O(log N).
3. For a well-formed x, let r be its number of literal occurrences. Because E is explicit, r<=L. Enumerate the 2^r Boolean assignments to OCCURRENCES using an r-bit work register. Reject inconsistent assignments to repeated variable IDs, tested by comparing their original binary ID substrings in the stored x; accept SAT if any consistent occurrence assignment satisfies all clauses. Otherwise output UNSAT. This covers arbitrary repeated variable occurrences and arbitrary binary variable identifiers, without assuming only three variables or using an oracle.
4. A finite-control/multitape implementation performs each assignment consistency test and clause evaluation in poly(L) charged transitions with O(L) visited writable cells. Parsing a malformed padded input is polynomial in its actual length N, and no exponential suffix needs to be generated on the decider's work tapes.

On valid encodings, 2^r<=2^L<=N and L<=log2 N. A conservative full bound with local head moves is

$$
T_{\mathrm{pad}}(p(x))=O\!\left(N(1+\log N)^c\right)
$$

for some **fixed** c (e.g. c=4 suffices with straightforward quadratic comparisons), and

$$
S_{\mathrm{pad}}(p(x))=O(\log N)
$$

writable cells. S counts the copied unpadded source, binary registers, temporary comparisons and stored occurrence assignments; the giant read-only suffix does not become free access, because its complete syntactic scan is charged. For malformed y, the syntax checker also has a polynomial |y| bound. The same finite total program works for all lengths and yields SAT, UNSAT or MALFORMED as appropriate.

Consequently **Q for the artificially exponentially padded encoding is FALSE**, with an explicit uniform deterministic polynomial-time, logarithmic-workspace decider, regardless of whether standard E-3SAT is in P.

**Why there is no paradox:** computing p(x) from unpadded x takes Omega(2^L) physical output transitions. The one-way map p^{-1} is inexpensive on its enormous source, but the reverse E-to-padding translation violates Lemma B's polynomial-time hypothesis. Claiming a lower bound "independent of encoding" without bounding representation growth is therefore demonstrably unsound. This is a counterexample to an overbroad wording, **not** a polynomial-time algorithm for standard 3-SAT, and not a separation theorem.

## 5. Executed falsification controls and reproducibility

The exact Node-compatible source below was directly executed as its serialized self-contained audit function in hosted V8, **not as a native operating-system Node process**. Exact source and raw data were published, then each fetched back and compared byte-for-byte with the submitted UTF-8 content:

- Source: [experiments/tmr/tmr1_padding_encoding_frontier018.cjs](https://github.com/j15marti/pnp/blob/main/experiments/tmr/tmr1_padding_encoding_frontier018.cjs), Git blob 310e68696f3b5c1cfc2ddd20c0b1f0d669fd0631.
- Raw: [results/raw/tmr/2026-11-14_0400_TMR1_PADDING_ENCODING_FRONTIER018_RAW.json](https://github.com/j15marti/pnp/blob/main/results/raw/tmr/2026-11-14_0400_TMR1_PADDING_ENCODING_FRONTIER018_RAW.json), Git blob 1897dc1f987811e8b73ff73ede46f73c00799381.

The executable uses a deliberately **restricted fixed-one-variable triple-repeated 3-CNF sign stream** as its finite test language, so both SAT and UNSAT can occur at very short L; this is NOT a general 3-CNF Turing-machine execution. Every binary string x through L=10 was tested: 2,047 x, comprising 21 SAT and 2,026 UNSAT; 6,141 malformed suffix-length/bit controls; precise N=2L+1+2^L checked; largest actual constructed padded string N=1,045; summed lengths of constructed valid padded fixtures 1,437,016 bits; zero failed assertions. This sum is **NOT** a physical TM microstep count. Independent Boolean assignment enumeration checked ten small Horn, 2-SAT, XOR, complete forbidden-mask, disjoint-product, proper-3-CNF and auxiliary-variable controls.

The finite code uses native JS arrays and integer exponentiation only at L<=10, and does **not** claim its array operations constitute the fully charged arbitrary-length physical TM implementation. The latter is a separate symbolic constructive argument. A native-Node network retrieval attempt failed because this container could not resolve raw.githubusercontent.com; no native independent replay or full repository preflight is claimed.

## 6. Peer relation, dependencies, and unrestricted gap

TMR-2/017's disjoint sign-block information lower bound, TMR-3/016's corrected local-head fetch bridge, TMR-1/017's control congruence and TMR-4/018's work-symbol cost congruence are compatible with this construction. Indeed the padded solver **does** scan the source and suffix; it simply has so much paid input length that brute-force exploration of the short formula is polynomial in N. This shows why an acquisition, memory, or cost abstraction theorem must bind its resource to the **specified honest encoded L**, not only to a semantic formula with no representation-length contract.

TMR-5/015's observed off-current-head read in TMR-3's original executable is preserved as an executable defect; its read-before-return ordering repair is the valid restricted interface. This run does not upgrade TMR-3's unexecuted generic compiler. TMR-4/018's local congruence remains CANDIDATE pending independent review. No new general lower-bound potential is supplied.

**Corrected dependency:** polynomially balanced, uniform encoding/model interface -> fixed-machine cost and length accounting -> optional source/acquisition/abstraction bounds -> **OPEN** unavoidable post-acquisition computation for every correct A, all k and arbitrary polynomial workspace -> **OPEN** P!=NP. The first two arrows prevent invalid transfer, but do not prove the central open arrow.

**Separate hostile attack:** A source- and control-preserving exact quotient retains all writable head trajectories. Since the visited-cell space measure depends only on the starting work-head positions and the positions visited, an exact action-congruent replay already preserves S for each execution, even if it suppresses writable symbol distinctions. The TMR-4/018 explicit visited-footprint field is helpful for state-level accounting, not an additional semantic information-storage obligation. This is a restricted mathematical peer observation, not a complexity lower bound.

## 7. Evidence, literature, shared-file preservation, next target

Authoritative replacement directive: research/coordination/2026-11-13_1249_TM_RESOURCE_AGENT_REPLACEMENT.md, current main SHA 47459817e66dccf1f3079e6c724c0fd2643e7bc4. Recovered complete proof1.txt (28,714 characters, SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343), proof2.txt (1,051,196 characters via authenticated Git blob 930c5eeddafce656717f28055a7a9a755f44737c despite blank contents endpoint), and canonical main.tex (2,530,965 characters via authenticated blob 91b4e582c16cb7f60c9aa1ea2aebf09cd4caa2c6). Reviewed issue #3 through TMR-5/015, AGENTS.md, CODEX.md, the repository pnp-research skill, all five newest handoffs, original TMR-1/017, TMR-2/017, TMR-3/016, TMR-4/018 and TMR-5/015 reports, original code/data described in those reports, and their relevant preserved parity/crossing counterexamples. This run does not replace old assignments or restore obsolete checker duties.

**Primary published literature checked for scope (not claimed to prove this new model guard):**

1. Stephen A. Cook, *The Complexity of Theorem-Proving Procedures*, STOC 1971, pp. 151-158, DOI https://doi.org/10.1145/800157.805047. Polynomial reducibility and NP-completeness context; not a deterministic lower bound.
2. Leonard Berman and Juris Hartmanis, *On Isomorphisms and Density of NP and Other Complete Sets*, SIAM J. Comput. 6(2):305-322 (1977), DOI https://doi.org/10.1137/0206023. Polynomial-time isomorphism and density constraints, different from arbitrary exponential padding.
3. Juris Hartmanis and Richard E. Stearns, *On the Computational Complexity of Algorithms*, Trans. AMS 117:285-306 (1965), DOI https://doi.org/10.1090/S0002-9947-1965-0170805-7. Foundational machine-time measure; no claim of a general SAT lower bound.

**TRACKERS REVIEWED; NO MATERIAL CHANGE** to root proof1.txt or proof2.txt, because neither P=NP nor P!=NP chain acquires a new unrestricted proof arrow. Canonical root main.tex left intact for the authorized TMR-5 synthesis owner. No scheduled task changes. Programmatic repo preflight and LaTeX compilation were not performed via a full checkout.

**One next target:** formulate a *single fixed, ordinary-encoding* lower-bound candidate whose input-computation charge remains nontrivial under polynomial-time reencodings and input copying; seek a compact Horn/XOR/general-polynomial-space counteralgorithm before treating any necessary distinction as superpolynomial. Request independent TMR-5/TMR-2 review of the padding frontier and TMR-4's exact visited-cell implication.

END_OF_REPORT::TMR-1::018::2026-11-14_0400_PST
