# POSITIVE-SELECTOR-HORN2: a discoverable refuting cover with Horn backdoors

19 November 2026, Asia/Seoul. Assignment: positive restricted selector lemmas. P versus NP remains OPEN. Symbolic proofs below are PROVED/EXACT at the stated scope; external independent mathematical review is pending.

## Result and integration point

This extends SUPPORT-SELECTOR1 beyond its 2-CNF terminals. A uniform, sound, deterministic selector succeeds when each UNSAT row has **at least one** refuting residual with a syntactic strong Horn backdoor of size at most d. The other residuals may be arbitrary CNFs. Backdoor discovery is performed, not advised. Failed discovery returns UNKNOWN, never UNSAT.

On the authenticated layout below, the same execution uses

    T = Otilde(N + 2^d sum_i 2^{r_i} ell_i + BR),
    S = Otilde(ell_max + R + d),

including discovery, all local assignments, failures, source access, materialization, verification, and streamed output. Here R=2^h is the number of complete shared assignments, B is the block count, ell_i is the encoded size of source block i including delimiters, and r_i is its actual shared-variable support size. With R<=N^.195, B<=N^.65, ell_max<=N^.35, and d<=floor((27/200)log_2 N), this gives

    T <= N^{1.33+o(1)}, S <= N^{.35+o(1)}.

No hypothetical SAT seed is needed for this restricted result. It supplies no compiler from arbitrary CNFs. The novelty claimed here is the explicit one-refuting-block-per-row promise, its three-valued streamed integration, and the costed correct-path comparison; bounded Horn backdoors and local-support reuse are established methods.

Falsifiers attacked: mistaking failed class recognition for refutation; using one failing backdoor assignment as an UNSAT proof; retaining all residuals or child computations; inferring unrestricted hardness from a large syntactic backdoor. The proof and executed controls reject all four inferences.

## Encoding, outputs, and quantifiers

Input is a read-only, block-delimited encoding of

    F(z,y_1,...,y_B) = AND_i F_i(z,y_i),

where shared variables are z_1,...,z_h and private variables carry their owner block in their identifier. Each block declares its private variables, including any isolated variables. Occurrences must match those declarations. Thus private disjointness can be authenticated while holding one block, without a global variable dictionary. Counts, identifiers, lengths and tags are checked; malformed inputs return INVALID. N is actual total encoded length, including metadata; sum ell_i<=N. There is no expanded R-row input or free residual oracle. All 2^h rows are enumerated by a counter. Source blocks are bounded by ell_max, not merely assumed to have short semantic residuals.

Use uniform bounded-word RAM operations on O(log N)-bit words, with polylogarithmic bit-machine overhead. Read-only source and write-only output are excluded from writable space; indices, counters, queues, clause copies, branch state and retained coverage are included. Sorting a current block to remove duplicate literals and tautologies and to compact private IDs costs Otilde(ell_i) time/space. Dense private variable renaming is local. If a different source encoding requires discovering a partition, regrouping clauses or authenticating a cross-block renaming, add its actual costs P,W. These are not obtained by the theorem.

The output is one of:

* UNSAT with an array A indexed by every z, where F_{A[z]}[z] is truly UNSAT;
* SAT with z and a complete assignment to each private block, emitted in block order;
* UNKNOWN, which makes no claim about the formula's label.

The NO specialist simply suppresses SAT results and returns UNKNOWN instead. Its completeness promise is

    for every z, there exists i with UNSAT(F_i[z]) and beta_H(F_i[z])<=d.       (NO-COVER)

The matched YES promise is

    there exists z such that for every i,
    SAT(F_i[z]) and beta_H(F_i[z])<=d.                                      (YES-ROW)

These promises imply UNSAT and SAT respectively. They need not exhaust all layouts. The algorithm is sound on all well-formed layouts and complete on the corresponding promise. It does not ask for the label or assume that an uncovered row is SAT.

## Local terminal: detection, decision, and witnesses

For normalized CNF Q, a syntactic strong Horn backdoor D is a variable set such that deleting D's literals leaves at most one positive literal in each clause. This is equivalent to Q[a] being syntactically Horn for every assignment a to D. The standard detection algorithm branches on two remaining positive literals of a non-Horn clause; at least one belongs to every such backdoor. Nishimura, Ragde and Szeider, SAT 2004, Theorem 2, give O(2^d |Q|) detection; Section 4.1 checks the 2^{|D|} Horn restrictions. This is established parameterized-SAT machinery, not a new SAT algorithm. [1]

For completeness, the criterion follows clausewise: an assignment falsifying all D-literals in a non-tautological clause leaves all its other positive literals present. Thus two remaining positives violate the all-assignments Horn requirement. Conversely, if at most one positive remains, every restriction is Horn. Empty clauses are allowed.

Implementation: repeatedly choose the first violating pair (p,q) in a deterministic source order. Branch by adding p or q, to depth d. If no violating pair remains, retain D; if all depth-d branches fail, return UNKNOWN. A mutable D and a depth-first stack suffice. At most 2^{d+1}-1 detection nodes are examined, each with a paid scan. There is no need to materialize the quadratic graph of co-occurring positive variables.

After finding D, enumerate all assignments a to D. Build Q[a] and run Horn forward chaining with occurrence queues and clause counters. If a least-model witness exists, combine it with a, fill unconstrained variables with zero, check Q, and return SAT. Only after every a is refuted return UNSAT. The branch enumerator reuses one residual and one Horn solver. Detection and evaluation are consecutive Otilde(2^d |Q|) phases, not their product. Total workspace is Otilde(|Q|+d). This bound includes reconstructing each residual and each failed SAT attempt.

Refutations can be made explicit: a Horn run records which source clause first forced each variable and the final contradictory clause. Each propagation record is locally checked, giving Otilde(|Q|) proof length/work per a. A full backdoor refutation includes every assignment a and therefore costs Otilde(2^d |Q|) to emit/check. Alternatively a compact (D,source-reference) certificate is verified by recomputation at this same time cost; compact certificate length is not cheap verification.

## Positive cover lemma and proof

Initialize A[z]=uncovered and E[z]=true for each of the R rows. E means that every processed block has been positively certified SAT on that row. Process blocks sequentially. Find the actual shared support S_i of block i. For each of its 2^{r_i} assignments a, build Q=F_i[a] and call the bounded terminal. Enumerate all full shared rows extending a:

* On UNSAT, set A[z]=i if it is still uncovered.
* On SAT, leave E[z] unchanged.
* On UNSAT or UNKNOWN, set E[z]=false.

Discard the local residual, answer, backdoor and Horn state before the next local restriction. Do not keep a table of all local answers.

After the scan, if A covers every row, return UNSAT and A. Otherwise, if some E[z] remains true, rerun each block at that z and emit its verified private witness. If neither condition holds, return UNKNOWN.

Proof of soundness: each entry of A is backed by a genuine local refutation. Complete coverage proves forall z exists i UNSAT(F_i[z]); thus F is UNSAT. A surviving E[z] means every block is SAT at that common z. Private disjointness makes the union of their assignments a full witness. UNKNOWN never contributes an asserted SAT or UNSAT fact. In particular, absence of a refutation is not used as a SAT certificate.

Proof of completeness: under NO-COVER, the bounded detector finds a backdoor for at least one UNSAT block on every row, and enumeration refutes all its leaves, covering that row. Under YES-ROW, each block on the promised row returns SAT, so its E bit survives. Both assertions quantify over every well-formed source satisfying the respective promise, not a specified test instance.

Resource proof: each local restriction is solved once, contributing 2^d sum_i 2^{r_i} ell_i. For one block, the sets of extensions of its local assignments partition all R rows, so marking contributes at most R visits, not R times 2^{r_i}. All source blocks together cost Otilde(N) to acquire and normalize. The live arrays use R log(B+1)+R bits; the source block, normalized copy, residual, queues and witness together use Otilde(ell_max). Depth-first detection uses Otilde(d), with d=O(log N) in the numerical corollary. No children run concurrently. These are the same execution's bounds.

SAT output is delayed until a row is established. Its second pass costs Otilde(N+2^d sum_i ell_i) and holds one private witness at a time. Every original clause is checked before its block witness is discarded, and isolated declarations are emitted too. This replay is absorbed in the stated bound. Output order is blockwise; a demand for an unrelated variable order requires additional indexing/replay. The selector alone has length O(R log B). If full NO proof objects are requested, a rowwise replay with a full source scan per selected block costs Otilde(RN+R2^d ell_max); this is still <=N^{1.33+o(1)} at the displayed parameters, with the same peak space. No B-entry directory is assumed.

For the numerical corollary, sum_i 2^{r_i}ell_i<=R N. Hence T=Otilde(2^d RN+BR+N), and 1+.195+.135=1.33. Space is Otilde(N^.35+N^.195). A smaller maximum shared support rho log_2 N yields T=Otilde(N^{1+rho}2^d+BR); this is genuine source-support reuse, not a free cached truth table.

## Ideal correct paths: separate polarity analyses

Free polarity routing supplies the answer to decision by definition. It supplies neither a YES witness nor verified NO coverage. The restricted construction removes this advice entirely; the following comparison explains which costs supplied choices would remove.

**NO path.** For each row, supply a block index and at most d binary choices in the fixed violating-pair detector. Those choices identify a valid backdoor when one exists; padding after termination is ignored. A path of d bits suffices because variable IDs are recovered from source scans. Wrong detector paths fail the syntactic check and reject. A valid detector path is still insufficient evidence of UNSAT: the verifier must refute all 2^{|D|} restrictions. If any restriction is SAT, reject the NO claim. For each row the choice budget is ceil(log_2 B)+d, and a whole row table needs at most R times this amount. Every selected source block must be accessed and every universal backdoor assignment checked. With full scans, verification costs Otilde(RN+R2^d ell_max), not just the cost of a favored leaf.

**YES path.** Supply one row z, then per block a detector path of at most d bits and one assignment to its backdoor (at most d further bits). Run and verify the corresponding Horn witness. If any chosen terminal is not Horn or is UNSAT, reject; all accepted paths produce a full satisfying assignment. A whole transcript has at most h+2Bd bits. Because private assignments are independent after fixing z, the machine can read/guess choices for one block, store its backdoor and witness, verify and discard them, then proceed. It need not retain all k bits. With correct choices, acquisition/replay and witness output cost Otilde(N) for logarithmic d, and Otilde(ell_max+d+h) workspace. The functional audit uses a witness list only as a test collector; this is not the production space realization.

This asymmetric comparison is the surviving content of free correct choices: YES may choose one successful local assignment; NO cannot choose away universally required assignments. Neither the 2^d loop nor backdoor size is an unrestricted time lower bound; another verified algorithm may decide the same residual more cheaply.

**General k-bit path, either polarity.** A bounded deterministic verifier must be sound for every proposed path and complete for at least one path on each input of its claimed polarity. If complete replay costs v and writable space s, enumeration of all padded paths is a valid deterministic simulation in O(2^k(v+k+1)) time and O(s+k+log(N+v)) workspace. This is an upper bound, never a mandatory enumeration lower bound. k=alpha log_2 N adds alpha to a polynomial time exponent. Independent local predicates admit separate enumeration and state reuse; a shared strategy with consistency constraints does not automatically factor. An adaptive algorithm's k must bound its entire existential transcript. For alternating choices, charge all universal histories or supply a whole strategy and a sound checker; one root-to-leaf trace is insufficient.

A fixed external random-access certificate can be excluded from writable space only in that declared model, with every access timed. Ordinary nondeterministic machines must retain earlier guesses they revisit or implement a paid consistency mechanism. Our blockwise YES verifier avoids such revisits by storing only the currently needed guesses. The NO verifier likewise stores each chosen D through all its universal tests. Re-guessing inconsistent copies is never allowed.

For the nondeterministic transducer, streamed output is certified only on final acceptance; a rejected path's prefix is not a witness. Requiring an atomic output artifact before acceptance would instead require a paid buffer or a consistency-preserving replay. The deterministic construction already delays emission until its successful row is established, then recomputes its uniquely prescribed choices.

A uniform deterministic one-sided specialist with universal soundness, a known clock/space cap, and success on **every** input of one polarity can be converted to a total decider by timeout. The restricted NO-COVER or YES-ROW guarantees do not supply this all-CNF completeness premise.

## Sourced simultaneous exclusions and what they do not exclude

Model: use the random-access Turing-machine convention of FLMV Section 2.1: read-only indexed input, write-only one-directional output, charged work/index tapes; index addressing is an explicit operation. Bounded-word RAM simulation adds only polylogarithmic factors. These statements do not cover unlimited unit-cost integers, free replayed advice, or a promise reduction whose resources have not been proved. [3]

| Polarity/model | Exact supported exclusion and scope |
|---|---|
| Uniform deterministic SAT or UNSAT decision | Buss--Williams Theorem 2 lists SAT outside DTISP(N^{1.34070},N^{.5}); their definition includes o(1) in both exponents. Thus the all-CNF target (1.33,.5) is excluded. For subpolynomial space the benchmark is every c<2cos(pi/7)=1.801937.... Complementing deterministic output preserves costs. [2] |
| Uniform nondeterministic UNSAT; equivalently conondeterministic SAT | Diehl--van Melkebeek--Williams: for c^2 d<4 there exists e>0 excluding simultaneous availability of NTIME(N^c) and NTISP(N^d,N^e) algorithms for tautologies. Setting c=d gives d<cuberoot(4)=1.587401... with some positive e, not e=.5. Their Section 2.1 explicitly disallows free two-way access to old guesses. [4] |
| NO side, explicit positive-space calibration | FLMV Corollary 6.5: NTIME(N) is not contained in coNTISP(N^c,o(N^{(1+c)/c^2-c})). The SAT-completeness transfer has polylog overhead. At c=1.10 the space threshold is .635537..., so (1.10+o(1),.5+o(1)) is excluded with slack. At c=1.33 this particular threshold is negative; it does not exclude (1.33,.5). [3] |
| Uniform nondeterministic SAT | None of those NO-side statements establishes the desired (1.33,.5) exclusion. Retaining a full assignment gives a near-linear-time, linear-space verifier; a supplied rereadable assignment uses a different space interface. No opposite-polarity transfer is made. |
| A particular refutation system | Bounds on resolution or another specified proof language concern that verifier/representation. They do not automatically exclude all sound deterministic or nondeterministic UNSAT procedures. |

The corrected NO-side attribution in LOCAL4 is retained. No new nondeterministic-SAT exclusion is asserted. For either polarity, a sound all-input k-bit verifier with v=N^{1.33+o(1)}, s=N^{.5+o(1)} and k<=alpha log_2 N for alpha<.01070 would contradict the deterministic point after enumeration. This requires all-input completeness and the standard-machine certificate simulation; the restricted theorem has neither arbitrary-CNF premise.

## Arbitrary CNFs, seeds, and hereditary closure

The terminal family is closed under restrictions with the *same absolute backdoor budget*: the surviving part of D still works. It does not follow that d<=.135 log_2 M for every physically smaller child encoding M. Nor does existence of a refuting cover persist after arbitrary block removal or repartitioning. These are separate hereditary obligations.

Using instead a generic exact seed with local time ell^c and space ell^s, the full-support scan has time exponent max(1.195,.845+.35c) and space max(.35,.195,.35s), before any extra compiler costs. The desired point requires c<=97/70 and s<=10/7 for this implementation. Merely postulating a polynomial seed gives neither numerical restriction. Iterating the formal exponent map toward a fixed point is invalid without a paid, hereditary, all-child compiler. A delayed but semantically correct seed must have its actual delay charged.

Arbitrary formulas can be put in one block, but then ell_max=N and the small-workspace conclusion is lost. They can be conditioned on all variables, but then R is exponential. A padded representation changes N and must be charged on the original source length. There is no demonstrated transformation meeting all the layout, backdoor-cover, correctness and simultaneous-resource premises for arbitrary CNFs or critical T5 deletions.

## Controls, tests, and prior-work reconciliation

The standard-library functional audit is positive_selector_horn.py, seed 2026111902. It exhausts all 3,304 normalized formulas of at most three clauses over three variables (including empty clauses), using budgets 0,1,2. It checks 9,912 bounded solver results against brute-force satisfiability and exhaustive backdoor subsets, plus 23,128 detector paths. The 360 generated three-block/two-shared-bit layouts return 212 SAT, 40 UNSAT, 108 UNKNOWN. All results, promise completeness, selectors and witnesses are checked against independent exhaustive local semantics. There are 3,552 residual calls and 4,320 row visits. These are functional counts, not measured RAM time or peak-memory benchmarks.

Explicit falsifiers: (x OR y) at d=0 returns UNKNOWN despite being SAT; a satisfiable XOR pair has a refuted assignment, showing why one failing leaf is not a NO certificate. A two-row layout uses different Horn-refuted blocks on its two rows and still succeeds with a third unrecognized SAT block. Thus requiring every block to lie in the terminal class would be unnecessarily strong for NO coverage.

T5 control: reconstruct H9 from threads BBB/FBB/FFF/BB, prove UNSAT by exact coloring search with color(0)=0, and construct full witnesses for each of its 11 edge deletions. Check all five rotations against the original directed arcs: 550 arc checks. In the usual one-hot Boolean encoding, the nine disjoint positive five-clauses force a syntactic Horn backdoor of at least 36 Boolean variables; choosing four per vertex suffices because the other clauses are negative. Hence beta_H=36 for that encoding, even though these fixed deletion witnesses are cheap to construct. The test checks the lower-bound obstruction at budget two. This is a representation-specific control, not a growing-girth claim or a lower bound on T5 execution.

Recovered project context:

* SUPPORT-SELECTOR1, research/agents/proof/2026-11-19_1201_SUPPORT_SELECTOR1/report.md, blob f82d2a82ddf571fd64e643d26ae1bd85038cc65f: streamed support coverage and 2-CNF witness terminals. The local full report was read, and its GitHub identity checked. This report adds UNKNOWN-safe coverage and a broader discoverable terminal; it does not claim to originate support reuse.
* LOCAL4, research/agents/recovery/2026-11-19_LOCAL4/report.md, blob 88695b6575e63e3af9311ba6533768279fba2dd3: independent row-certificate enumeration, corrected polarity, and paid replay. The full report was fetched this run.
* STRICT22-BACKDOOR-SELECTOR-GATE271, research/agents/lspv-3/2026-10-31_0219_LSPV-3_STRICT22_BACKDOOR_SELECTOR_GATE271.tex, blob ed843c351f66a70a587fc7559f8cc69b4b3e4dc7: exact syntactic criteria and large-backdoor easy SAT controls. Full source fetched; no static-parameter hardness inference is revived.
* HORN-SELECTOR-DEGREE60 handoff, research/agents/lspv-4/2026-10-23_1342_LSPV-4_HORN_SELECTOR_DEGREE60_HANDOFF.md, blob b4a5b75b9ad6abc9e567dda568945d5bd1823121: linear source-aware witnesses coexist with large backdoors. Full handoff fetched; old experiment counts are not represented as rerun here.

The current positive-selector role has no assigned TMR root manuscript. This is an additive report and evidence publication; no manuscript ownership, title, schedule or enabled/paused state is changed. There is no local project checkout, so repository preflight and LaTeX compilation were not run. Corpus review is targeted, not exhaustive; unmerged branches and every peer manuscript were not reviewed. Independent mathematical peer audit remains OPEN. Issue #3 publication was previously blocked by its comment limit; this run uses the additive handoff instead of retrying it.

## Proof-status ledger and next blocker

PROVED/EXACT: UNKNOWN-safe streamed coverage, NO-COVER and YES-ROW correctness, charged target bounds on the canonical source encoding, and the polarity-specific correct-path accounting. KNOWN THEOREM: the Horn backend and the stated sourced exclusions. COMPUTATIONAL: finite exhaustive/random checks and T5 full witnesses. FALSIFIED INFERENCE: failed backdoor search implies UNSAT; one UNSAT leaf suffices; large backdoor implies slow arbitrary execution. CONDITIONAL: any other encoding's P,W, class-cover promise, arbitrary-CNF compiler, and seed-specific exponent improvement. OPEN: all-CNF hereditary reduction, independent peer audit, and P versus NP.

Gates: DISJ PASS (no information/rank lower bound); relativization PASS as a restricted combinatorial algorithm, not a separation; simultaneous DTISP PASS on the specified single execution and OPEN for unrestricted transfer; deterministic configurations PASS as a consistency upper bound only. No circuit separation, Natural Proofs escape, or algebrization escape is claimed.

Next load-bearing lemma: a source-computable transformation or cover rule that guarantees at least one tractable UNSAT residual per row beyond syntactic small-backdoor classes, with the same physical size/access bounds. A smaller semantic or adaptive backdoor parameter alone does not establish its discovery or whole-strategy verification costs.

## Primary sources

[1] N. Nishimura, P. Ragde, S. Szeider, Detecting Backdoor Sets with Respect to Horn and Binary Clauses, SAT 2004, Theorem 2, Lemma 2 and Section 4.1. https://www.satisfiability.org/SAT04/programme/51.pdf

[2] S. Buss, R. Williams, Limits on Alternation-Trading Proofs for Time-Space Lower Bounds, CCC 2012 Theorem 2 and revised full manuscript, Computational Complexity 24 (2015). https://mathweb.ucsd.edu/~sbuss/ResearchWeb/npProofLimits/samCCC-cr.pdf ; https://mathweb.ucsd.edu/~sbuss/ResearchWeb/npProofLimits/paper-journal.pdf

[3] L. Fortnow, R. Lipton, D. van Melkebeek, A. Viglas, Time-Space Lower Bounds for Satisfiability, JACM 52 (2005), Section 2.1, Section 3, Corollary 6.5. https://lance.fortnow.com/papers/files/tst.pdf

[4] S. Diehl, D. van Melkebeek, R. Williams, A New Time-Space Lower Bound for Nondeterministic Algorithms Solving Tautologies, Wisconsin TR1601, 6 October 2007, Theorems 1-2 and Section 2.1. https://research.cs.wisc.edu/techreports/2007/TR1601.pdf
