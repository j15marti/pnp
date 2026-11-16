# TMR-3/061: graph guessing is already sound in Williams, but exhaustive selection is not jointly polynomial-time and sublinear-space

November 15, 2026, Pacific Time. TMR-3 / PNP Time-Space Tradeoffs, Track B.

**Status:** PROVED/EXACT only for the explicitly stated lexicographic exhaustive-graph architecture and its fixed source machine. Independent mathematical review OPEN. Finite test evidence COMPUTATIONAL. No P-versus-NP or L-versus-P separation, no improved generic evaluator, no FLMV contradiction.

## Selected dependency and original full chain

The dependency is **C3-GUESSED-GRAPH-TIME-AND-SPACE**: authentic binary input -> fixed blank-start local multitape decider -> block respecting graph -> candidate movement-word enumeration -> FAIL-checked Tree Evaluation -> correct accept/reject output -> a simultaneous time/space conclusion.

The objective is not another marked-edge family. Previous TMR-3/059 and /060 show that source-only recovery of one authentic graph edge can be P-complete; that fact does not disprove Williams's simulation. The primary source already avoids a source-only graph-index provider by enumerating all short movement words, computing the corresponding graph in logspace relative to the *guess*, evaluating a tree whose root returns FAIL if that guess is wrong, and proceeding until a correct guess yields ACCEPT or REJECT. See Williams (2025), Section 3.2, "Computation Graph Enumeration", "The Functions At The Nodes", and "Finishing up".

This run audits the missing *total running time and live graph-storage ledger* for that already existing technique, and independently constructs a physical machine on which a specified natural enumeration order takes exponentially many attempts even if the candidate evaluator is made free.

### Exact candidate and precommitted falsifiers

Candidate: replacing the graph's source-only indexer by ordinary exhaustive graph guessing eliminates the P-complete indexer premise, but retains an O(t/b)-bit guessed graph and, for a stated enumeration implementation, can require exp(O(t/b)) candidate tests. These obligations remain when the Tree Evaluation height term is improved. The claim is about the specified enumeration scheme only.

F1: the original Williams proof might not enumerate guessed movement words or might require authentic source-only edge access. F2: a valid wrong guess might return a Boolean answer rather than FAIL. F3: a cheap source-aware shortcut, compact motion family, or different guess order might defeat a claimed universal runtime lower bound. F4: candidate count, block storage, repeated calls, physical original-input reads, arithmetic and output may belong to incompatible realizations. The report addresses F1 and F2 from the original source; F3 restricts the theorem, and F4 is handled in the ledger.

## Primary-source reconstruction

Williams's original arXiv v1 (February 25, 2025), Section 3.2, defines p tape heads, B time blocks of b steps, and movements m_(h,j) in {-1,0,1}. The O(pB)-symbol word determines each tape-block index by prefix sums. Claims 3.4 and 3.5 compute its graph indices and edge predicates using O(log t) *additional* space GIVEN that word. The paper then enumerates candidate words and evaluates implicit Tree Evaluation instances R_G; an inconsistent head movement yields root FAIL, whereas the genuine word yields the actual output. For a fixed constant p, the raw universe contains exactly 3^(pB) candidate words, though invalid candidates may be filtered. The published result optimizes **space**, not polynomial running time. Its O(B) graph-description term is paid.

This is a correction to any interpretation of the /060 P-complete edge as refuting Williams: source-only authentic graph indexing is neither supplied nor needed in this published mechanism. The /060 hard edge still prevents silently claiming a cheap deterministic source-only provider in a *different*, more direct mechanism.

Primary literature: R. R. Williams, "Simulating Time With Square-Root Space", arXiv:2502.17779v1, Sections 2 and 3.2, https://arxiv.org/html/2502.17779v1 ; Cook and Mertz, "Tree Evaluation Is in Space O(log n log log n)", STOC 2024, Theorem 7, https://doi.org/10.1145/3618260.3649664 ; Hopcroft, Paul and Valiant, "On Time Versus Space", JACM 1977, https://doi.org/10.1145/322003.322015 .

## Fixed-machine exact counterexample to one exhaustive enumeration order

Let M_R be the following *one fixed* total, locally headed deterministic machine on binary input x of length N. It has a read-only source head, one blank writable work tape, a finite control bit a initially one, and no preloaded advice. For each data symbol x_i, it sets a <- a AND x_i and physically moves both heads one cell right. On the first endmarker, it stays on both heads, emits a, and halts. It computes AND(x), both YES and NO. The entire authentic run lasts t=N+1 transitions, and the work head visits N+1 cells. A separate, source-aware machine computes the same output in O(N) time and O(1) writable bits without advancing a work head.

Fix b and B with t=bB and b>=log2 t. During the first B-1 time blocks each head moves exactly one tape block right at the final boundary step. In the last time block, it reads the endmarker without crossing at the end. For time-major head order, the authentic movement word is

    m* = (+1,+1) repeated (B-1) times, then (0,0).

Every movement is locally physically realized and each tape-block crossing occurs at a true b-step boundary. The input length and t,b,B are distinct: N=bB-1.

Order all 2B-symbol words in {-1,0,+1}^{2B} lexicographically with -1<0<+1, checking each word by the sound Williams-style FAIL-or-answer contract, and stop at the first non-FAIL answer. The 0-based base-three rank of m* is

    rank(m*) = 3^(2B)-5,

because the maximal word (+1)^(2B) has rank 3^(2B)-1 and changing the two final +1 symbols to 0 subtracts 3+1. Therefore the exact number of candidate tests through the correct word is

    Q_guess(B) = 3^(2B)-4.

No earlier candidate can produce an answer under the soundness contract. In particular, regardless of the time required to evaluate one candidate, the specified serial exhaustive algorithm has at least Q_guess(B) paid test invocations. This is a restricted workload lower bound on *that* algorithm, not a lower bound on every strategy or on the decision language.

Two legal asymptotic choices give precise costs. For t=m^3,b=m,B=m^2 and all sufficiently large m, b>=log2 t and Q_guess=3^(2m^2)-4 = 2^Theta(t^(2/3)). For near-minimal b=ceil(log2 t) along t=bB, the test count is 2^Theta(t/log t). The fixed machine M_R itself does not depend on b; b merely specifies the legitimate block partition selected by the simulator.

A physically checked source-to-output control computes both answers with a single source scan. Thus the exponential cost belongs to the unfiltered lexicographic graph-guess procedure and must not be extrapolated to the optimal simulator, to a machine-aware schedule generator, to other enumeration orders, or to SAT.

## Joint resource ledger for the original graph-guess template

For a general fixed p-tape, t-step block-respecting machine, set B=ceil(t/b) and let g be a candidate full movement word. A literal dense graph representation stores pB trits, hence Theta(pB) bits for the specified representation, in addition to up to O(log t) candidate/address counters. Let Q_E(t,b) be the number of adaptive node or function requests for one R_g evaluation, and A_E(t,b) its maximum fully charged per-request time including source seeks, graph-edge reconstruction, interpolation arithmetic and output. Let I_E be other initialization/finalization work per candidate, and S_E the evaluator's complete peak workspace excluding the retained graph and block buffers.

A sequential implementation that enumerates at most 3^(pB) candidates obeys the conditional upper accounting

    T_total <= T_parse + O(3^(pB) * (I_E + Q_E*A_E + pB)),

    S_peak = O(pB + b + S_E + log(t+N+2)),

with the understanding that overlapping memory may be shared only after explicit analysis. No bound on Q_E or A_E is smuggled into this expression. The published Cook-Mertz/Williams space analysis yields the more specific existing O(b+B log b) upper bound for their solver; no polynomial time assertion is imported.

Within the *dense, full-word, serial-guess* template, the graph buffer itself has Theta(B) size. If a new height-sublinear evaluator hypothetically attained space O(b+B^alpha) with alpha=1/2, the unmodified full-word search would still retain Theta(B) bits: at b=t^(1/3), B=t^(2/3), so the total retained graph term is Theta(t^(2/3)), not the desired O(t^(1/3)). This is a **representation-specific** ledger, not a theorem requiring every equivalent computation to store a word of length B. In general b+B>=2sqrt(t) for B=t/b, so merely improving the evaluator's height exponent does not beat the square-root exponent within this representation.

Likewise, even if a candidate test took unit time, the displayed M_R source incurs exp(O(B)) serial attempts. Requiring polynomial total runtime under this exact enumeration and worst-case order forces B=O(log t), and therefore b=Omega(t/log t); it cannot be combined with a cube-root b choice. A new mechanism must avoid exhaustive enumeration, compress the retained candidate representation, bound a source-generated candidate list and its acquisition, or change the compiler/evaluator interface. These are open design alternatives, not proven impossible.

## Explicit distinctions and guards

Williams's implicit Tree Evaluation/FAIL method already provides the intended soundness interface for wrong graphs. It does **not** furnish a polynomial-time method for finding the true graph or an O(log N) original-source-only indexer. The P-complete edge of /060 is consistent with the paper: exhaustive guess-and-FAIL is not a forbidden source-only operation.

A source-specific motion generator computes M_R's true m* from length alone in logspace, and a different solver computes AND(x) directly with O(1) work. One must not declare the prescribed exhaustive search unavoidable. Similarly, /060's *marked edge* has two possibilities but that fact does not reduce the cardinality of all movements of its source-dependent CVP evaluator; source-head and VALUE-head trajectories are still relevant.

The two barriers in this report are distinct: (i) live storage of the raw guessed word; (ii) the serial number of candidate evaluations. A faster evaluator alone closes neither. Conversely, a compressed true-word generator does not automatically produce a low-space, fast **nonassociative** evaluator or a SAT machine.

No mandatory fixed-input graph-hardness, tree-unfolding hardness, rank-to-general-circuit claim or padded PSPACE reduction is made.

## Four mandatory gates

| Gate | Verdict |
| --- | --- |
| DISJ sanity | NOT APPLICABLE WITH REASON to a representation-specific graph-enumeration cost, not a rank or SAT-work lower bound. DISJ, affine, Horn, 2-SAT and compact shortcuts remain valid. |
| Relativization | NOT APPLICABLE WITH REASON to a class separation: none is claimed. No nonrelativizing P-versus-NP arrow, algebrization or Natural Proofs consequence is used. |
| Simultaneous DTISP | PASS for the separately declared complete original M_R and for the explicit architecture ledger; unrestricted polynomial-time-plus-small-space transfer remains OPEN. Candidate-count lower bound does not make a forbidden DTISP pair. |
| Configuration counting | PASS as a deterministic upper-bound control only. The original M_R runs in t=Theta(N) with O(N) visited work cells; it does not imply a work lower bound or a randomized/quantum stopping-time bound. |

Historical /341 FAIL as a full logical UNSAT authority; /386 RESTRICTED. P versus NP remains OPEN.

## Executed finite experiment and limitations

Published standard-library CPython source revision tmr3-graph-guess-volume061-v1, deterministic seed 202611152119, was executed twice with byte-identical raw JSON. Forty-five complete 2-head enumeration trials, each with a physically tracked binary source and a genuine EOF step, matched Q_guess=3^(2B)-4 for B<=5 and three widths. Both accept and reject sources were tested. Three hundred sixty additional random sources checked physical crossings and movement-word ranks. There were **8,388 assertions, zero failures**. Two large analytic parameter suites were checked without attempting infeasible exponential enumeration; these are finite COMPUTATIONAL checks of the symbolic formula.

The test's FAIL-or-output procedure is an abstract *contract verifier*, not the actual Cook-Mertz implicit Tree Evaluation and not a compiled native Turing-machine microtransition table. No independent proof review, full repository checkout/preflight, literal HPV conversion or new generic evaluator was performed. A direct clone of the private repository failed DNS, so remote connector reads and exact GitHub blob readback were used instead.

Executable: experiments/tmr/tmr3_graph_guess_volume061.py.
Raw: results/raw/tmr/2026-11-15_2119_TMR3_GRAPH_GUESS061_PY_RAW.json.
The prior /054-/060 source evidence is preserved on the existing stacked branch. No retired proof trackers were read.

## Corpus reconciliation and one next load-bearing lemma

The /059 and /060 P-complete graph-index claims retain their **restricted** proofs, but their interpretation is narrowed: they attack only an original-source-only graph-index provider, not Williams's actual guessed-graph simulation. Williams's own enumeration and FAIL logic is known primary-source prior art, not a novelty claim. TMR-3/056 and /057 already falsified compulsory workload from a *particular no-sharing tree evaluator*; the new result concerns the distinct **serial graph-candidate selection** term and full retained candidate storage.

**One next lemma: C3-SELECTIVE-CANDIDATES-AND-COMPACT-STATE.** For a pinned authentic block-respecting compiler and all original sources, construct or falsify a uniformly discoverable polynomial-size list (or compact implicitly generated family with equally charged total query work) of source-compatible movement words, together with sound two-label FAIL checking, full graph access, nonassociative evaluation, and a same-execution T/S bound. Explicitly preserve cheap alternatives, and do not infer this list from a P-complete edge query or from certificate existence alone. The general problem and P versus NP remain OPEN.
