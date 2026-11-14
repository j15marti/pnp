# TMR-2/015: a linear-cost physical machine with globally future-dependent crossing records

**Pacific date:** November 14, 2026, 01:18 PST (America/Los_Angeles). **Role:** TMR-2 Information Necessity, j15marti/pnp. **New result:** TMR2-PC15, a fixed-program local-head hostile construction, CANDIDATE pending independent TMR-5/TMR-3 review. **Independent peer verdict:** TMR-5/012 interval-depth conditional Kraft inequality ID12, PROVED/RESTRICTED as a coding theorem after an independent mathematical check. **Finite evidence:** COMPUTATIONAL. **Unrestricted superpolynomial SAT lower bound and P versus NP:** OPEN.

## 1. New constructive machine obstruction TMR2-PC15

### Fixed-machine model

Let A be ANY ONE fixed finite total uniform deterministic 3-CNF-SAT decider on all binary strings, using a fixed finite control and alphabet, finitely many local work tapes, and at least one read-only input head that moves at most one cell in a charged transition. The original input contains exactly L data bits between immutable endmarkers at physical positions 0 and L+1. A handles valid SAT, valid UNSAT, and malformed encodings correctly. All work-tape cells, indices, copying, processing, repeated reads and output are charged. Input-head movements cost transitions. No oracle or unbounded-word operation is available.

**Theorem TMR2-PC15 (CANDIDATE, complete symbolic construction pending independent review).** For each such fixed A there is ONE fixed finite total uniform correct decider B_A, valid on every length, with the same writable work-tape footprint on each input, such that

$$
T_{B_A}(x)=T_A(x)+2(L+1)\left(1+\mathbf 1[P(x)=0]\right),
\qquad S_{B_A}(x)=S_A(x),
$$

where P(x) is the XOR of all L original input bits. B_A makes a full paid left-to-right parity scan, returns the same source head physically to the left endmarker, optionally executes one additional complete round-trip when P=0, and then simulates A(x) from A's exact initial configuration. Its finite control records the last bit read on the outward scan and parity on its return scan. Other original source heads and work tapes remain untouched during the preliminary sweeps.

At every original-input cut between positions i and i+1, for 0<=i<=L, the designated preliminary trace has **exactly two crossings if P=1 and four if P=0**. The first return crossing carries P in the actual finite control. For i>=1, the first outward crossing after reading data bit x_i carries x_i in finite control. Hence the two finite-state projections at that physical cut give the genuine crossing-derived, fixed-length code

$$
c_i(x)=(x_i,P(x))\in\{0,1\}^2.
$$

For K independently variable source-bit fields X_1,...,X_K in increasing physical order, keeping every other source bit fixed, write P=p_0\oplus X_1\oplus\cdots\oplus X_K. Then the crossing-derived c_i has **genuine dependence on every later X_j**, j>i. Fixing all blocks except X_i leaves two distinct length-two codewords, so its conditional map X_i -> c_i is injective and prefix-free. The **minimal** permitted future horizon for these particular codes is R_i=K for every i; consequently their interval overlap depth is

$$
D=\max_j|\{i:i\le j\le K\}|=K.
$$

Every selected cut's preliminary crossing COUNT is itself globally correlated: all K counts equal 2 or all equal 4. Toggling one free bit changes P, simultaneously changing all K preliminary crossing counts and every cut's recorded return state. These crossings are genuine charged physical steps, not merely a hypothetical conditional codebook. The extra preprocessing costs at most 4(L+1) transitions and **zero additional visited writable work cells**.

For a valid SAT-only source promise, select K independent original clause-sign bits of the existing authenticated G_r strict-3CNF family, holding its headers, identifiers and filler fixed. All 2^K choices remain syntactically valid, with K=24r and encoded L=Theta(r log r). Source parity is the XOR of those independent signs plus a fixed constant, so this construction gives D=K=Theta(L/log L) on an unbounded family of genuinely valid 3-CNF encodings. SAT and UNSAT labels remain correct because the B_A suffix is the arbitrary correct A. Neither formula family recognition nor source authentication is performed for free by B_A.

### Proof and limitations

One left-to-right traversal from the left marker to the right marker uses exactly L+1 local transitions, reading each data bit at its current cell before moving. Store its running parity and last bit in finitely many control states. The physical return costs L+1 further transitions, during which every backward crossing retains final P. If P=0, repeat a right and left traversal, costing another 2(L+1). The genuine input head ends at zero and the original A program, all work-tape cells and all A head positions are unchanged. Redirect control into A's original initial state. From that point, reproduce each A transition, with its original output. No input length is hardcoded; scanning stops on the right endmarker. The claimed time equality, unchanged visited writable cells, uniformity, terminal correctness, and all-transition charging follow by construction.

For each free sign bit X_i, the forward crossing after its actual source cell transmits its just-read bit in finite control; the first return crossing transmits complete-source parity. This is a projection of a **tagged portion of the full actual crossing sequence**; later A activity may add arbitrary crossings but cannot erase the earlier phase-tagged records. The length count 2/4 refers to this designated preliminary portion, **not** necessarily to A's complete crossing sequence after the suffix. For every i<K, toggling X_K while fixing earlier sources changes the return state at cut i, so no horizon R_i<K can describe these selected codes. The conditional two-word fixed-length codebook remains prefix-free. Thus TMR-5's ID12 with D=K holds but gives only its K-free exponent. Nothing establishes that all possible normalized crossing encodings must have D=K: a representation-specific normalization could discard this useless parity prepass, but must prove soundness and pay any associated work. This refutes an inference of sublinear D from input read-only-ness, independent free blocks, correct labels or local-head motion **alone**, not all conceivable processing invariants.

The construction is compatible with a solver using Horn propagation, 2-SAT SCC, GF(2) Gaussian elimination, bounded-treewidth DP, disjoint-product decomposition, arbitrary sharing, auxiliary variables, reencoding, caching, input copying and recomputation because it simply composes with A, unchanged. No claim that each of those algorithms was physically implemented in the finite test follows. The input is only L bits, the answer is one label, and globally correlated records are cheaply creatable. Crossing-record multiplicity or nonlocal dependence is not intrinsically a SAT computational lower bound.

## 2. Independent peer proof of TMR-5/012 ID12

TMR-5's original ID12 report was read rather than inferred from a chat summary. Let independent uniform q_i-bit blocks X_i have codewords c_i(X_1,...,X_{R_i}), with i<=R_i<=K, and require the conditioned map in X_i to be prefix-free for every fixed assignment to its other arguments. Put Y_i=2^{q_i-|c_i|}, F_j=sigma(X_1,...,X_j). Conditional Kraft gives E[Y_i | F_{i-1}]<=1, even if the codebook depends on arbitrary earlier blocks.

Color each interval [i,R_i] with D colors, where D is the maximum number of intervals covering any index. A greedy interval coloring exists with D colors. In each color class, successive starts i<j obey R_i<j, so all earlier Y_i factors are F_{j-1}-measurable and iterated conditional expectation yields E[product_{i in class}Y_i]<=1. Generalized Holder across the D classes gives E[(product_iY_i)^{1/D}]<=1. Markov on the event product_iY_i>2^b yields

$$
\Pr\left[\sum_i|c_i|<\sum_i q_i-b\right]\le2^{-b/D}.
$$

This independently validates the exact stated bound for its conditional prefix-free coding model, with variable q_i and heterogeneous R_i. **Peer verdict: PROVED/RESTRICTED for ID12's stated coding hypotheses.** It is not a physical crossing-record theorem, a general SAT runtime lower bound, or an argument that D=o(K). The new PC15 construction exhibits why that last unproved transfer is substantial.

## 3. Actual independent executions and controls

**Published exact standalone JavaScript, executed in hosted V8 before publication:** experiments/tmr/tmr2_physical_suffix_crossing015.cjs (Git blob dc1e65f3f39b7eb45c9f7d83ffd727dec6dd926b). **Published immutable raw:** results/raw/tmr/2026-11-14_0116_TMR2_PHYSICAL_SUFFIX015_RAW.json (blob 0cf0d5be1b4a594b1fd1cea58e804083914b26e2). Both were reread and matched the generated content byte-for-byte.

The finite physical model is one locally moving original-input head with finite control. Its core is a single fixed authentic restricted 3-variable proper 3-CNF classifier: each three-bit sign triple forbids exactly one of the eight assignments to three named variables; SAT iff some assignment is not forbidden, UNSAT iff all eight are forbidden, and non-multiple-of-three source lengths are MALFORMED. The classifier uses only a fixed 8-bit finite-control mask, not a free SAT oracle or an unbounded word. A separate truth-table evaluator independently checked each output. Every input-head step and optional prepass crossing was counted. This is **not an arbitrary-variable general SAT simulator**.

The exact published JS tested all 2,047 binary inputs of lengths 0 through 10, plus 259 fixed/seeded length-24 fixtures, for 2,306 total inputs. It checked 18,434 single-bit flips, 18,434 conditional prefix-free crossing-code fibers, 18,434 physical crossing-state projections, and 109,156 counted transitions; outputs were 842 SAT, two UNSAT, and 1,462 MALFORMED. There were zero failed assertions. Two distinct actual UNSAT 24-bit permutation inputs and a SAT repeated-mask input were among the fixtures.

**Independently authored and natively executed CPython** was run on the same 2,047 exhaustive short inputs and 259 separate length-24 fixtures, with 18,434 bit-flip and 18,434 conditioned-code checks, 109,856 counted transitions and zero failures. It used a separately seeded fixture generator, so its transition total differs by 700 from JS; this is not a claim of matching fixture-by-fixture test vectors. This Python source/raw audit is LOCAL-ONLY, not claimed published to GitHub. Neither execution ran a native instruction-level compiler for arbitrary A. Both finite results are COMPUTATIONAL and support only the explicitly tested physical controllers; the arbitrary-A theorem is the separate symbolic machine composition.

Exact input-measure and label controls: L is the total encoded bits, never the number of clauses or variables. Two independent UNSAT permutations have all eight three-bit masks; repeated all-zero masks are SAT; malformed lengths are rejected. No advice, uncharged indexing or assumed proof certificate is used.

## 4. Corpus, primary sources and publication boundary

Controlling replacement directive research/coordination/2026-11-13_1249_TM_RESOURCE_AGENT_REPLACEMENT.md read first and rechecked unchanged blob 47459817e66dccf1f3079e6c724c0fd2643e7bc4. Full current proof1.txt recovered at 28,714 characters, blob 06f7ebc8c2283304a0f5200b518c6e48fa41e343; the connector's empty proof2 body was NOT interpreted as an empty file: authentic Git blob 930c5eeddafce656717f28055a7a9a755f44737c recovered all 1,051,196 characters. Likewise the full canonical main.tex was recovered from authentic Git blob 903092cd483c0b17694c9f500fa03b5a703508cc (2,522,180 characters), despite an empty contents-body response. Read AGENTS.md, CODEX.md, pnp-research SKILL.md, all five newest TMR handoffs, the current issue #3 with its newest TMR-1/015 comment, original TMR-5/012 report, original TMR-3/012 and /013, TMR-1/015, TMR-4/015 and TMR-2/014. The old LSPV role assignments in root guides are superseded by the 12:49 PST directive, while historical findings remain evidence.

Primary sources inspected for model and coding context:
- F. C. Hennie, "Crossing sequences and off-line Turing machine computations", SWCT/FOCS 1965, 168-172, doi:10.1109/FOCS.1965.5, https://dblp.dagstuhl.de/rec/conf/focs/Hennie65.html . Actual crossing sequences on locally moving input are the relevant original methodology, not random-access queries or a prescribed SAT proof calculus.
- B. McMillan, "Two Inequalities Implied by Unique Decipherability", IEEE Trans. Information Theory 2(4), 115-116 (1956), doi:10.1109/TIT.1956.1056818 . Only the elementary per-fiber prefix-code/Kraft inequality is used.
- TMR-5/012's original interval-depth manuscript and TMR-3/012's original correlated coding counterexample, cited above. No theorem about unrestricted SAT machines is imported from those papers.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Root proof1.txt and proof2.txt remain unchanged since no all-exponent proof arrow is closed; root main.tex remains under TMR-5's synthesis ownership. No scheduled tasks were created, revived or modified. The new counterexample PC15 is CANDIDATE pending independent TMR-5/TMR-3 formal review. ID12 passes independent review at PROVED/RESTRICTED coding scope. All subsequent transfers from physically necessary distinctions to superpolynomial all-input processing time remain OPEN.

**One next target:** TMR-5 should independently validate the tagged-crossing full-suffix PC15 construction and determine whether a nontrivial canonical normalization of arbitrary complete crossings can erase the parity prepass with a *fully charged, all-transition* simulation. TMR-3 should seek a causal restriction that survives this wrapper and arbitrary rereads, rather than assuming interval overlap D=o(K).
