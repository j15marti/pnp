# TMR-1 MACHINE-SLICE-FIREWALL-001: Uniform machine quantifiers and two falsification lemmas

**TMR-1 REPORT::MACHINE-SLICE-FIREWALL-001::2026-11-13T13:07:00-08:00**
**Research date:** Friday 2026-11-13, 13:07 PST (America/Los_Angeles).
**Repository:** j15marti/pnp, main.
**Scientific status:** **CANDIDATE** for two fully written elementary symbolic proofs, pending independent TMR-5 verification; **COMPUTATIONAL** for executed finite regression. **OPEN** for every representation-independent superpolynomial 3-SAT lower bound. P versus NP remains OPEN.

## 1. Authority, corpus and change audit

Read first the 2026-11-13 12:49 PST new-team directive at research/coordination/2026-11-13_1249_TM_RESOURCE_AGENT_REPLACEMENT.md (blob 47459817e66dccf1f3079e6c724c0fd2643e7bc4; final sentinel checked again before publication). New TMR identities supersede older LSPV work allocation and main.tex ownership instructions. Do not modify automation schedules.

Read root proof1.txt (blob 06f7ebc8c2283304a0f5200b518c6e48fa41e343, 28,714 text characters), root proof2.txt through the authoritative Git blob API (930c5eeddafce656717f28055a7a9a755f44737c, 1,051,196 characters), and root main.tex through its Git blob API (600f00f4bfaf05d09c136c40edc6e22f1cce9d96, 2,479,448 characters). The ordinary fetch_file returned empty content for proof2.txt and main.tex, so no content-file update was attempted; the Git blob API recovered complete contents for review. Read issue #3 including the 12:56 PST replacement notice and recent /621, /624, /605, /592 historical work; AGENTS.md (4ae902888754d0b06ba4ce1aaeca0657a92b46a9), CODEX.md (754999f50de93cdb693ed37bc8110d31e9e698ef), and .codex/skills/pnp-research/SKILL.md (b8df83a7b0b1428f349b0e02ce1387d979e8db7f). Surveyed relevant original reports: research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex, research/agents/lspv-1/2026-11-13_LSPV1_PA_CORRECTNESS_CERTIFICATION_TRAP_GATE.md, research/agents/lspv-4/2026-11-13_1236_LSPV4_GUARD_ERASURE_DAG_TRANSFER592.md and GROKPROOF/2026-11-06_2316_PROGRESS.md. The research/agents/tmr-1/ and /tmr-5/ paths did not yet exist on main when checked; therefore no current TMR handoff was available to inherit.

**Duplication / contradiction:** earlier one-tape crossing-sequence bounds and legacy historical proof-system bounds are restricted-model results. They are not direct evidence for this report's unrestricted multitape resource bottleneck. The prior /341 satisfiable-source acceptance counterexample and legacy correctness-certificate barrier remain preserved but do not instantiate the machine bottleneck. No historical result is reclassified. Root main.tex already declares P versus NP OPEN and has no authorized TMR-1-owned region.

**Changes:** proved-form counterexamples to two *proposed objectives* are formulated below. The stronger unrestricted machine complexity target remains unsolved. **TRACKERS REVIEWED; NO MATERIAL CHANGE** to either proof chain. main.tex intentionally not edited: TMR-5 owns whole-document synthesis and has not established a TMR-1 region.

## 2. Explicit language and fixed machine model

Use this fixed binary encoding E for testing and as the reference 3-SAT language. A valid input is

$$
1^n 0\;1^m 0\;\prod_{j=1}^{m}\prod_{i=1}^{3}
(s_{j,i}\;\mathrm{bin}_{w}(v_{j,i})),\quad
w=\max(1,\lceil\log_2 n\rceil).
$$

Here n>=3, m>=1 are unary; each sign bit s is 0 (positive) or 1 (negated); each variable index v is zero-based and lies in [0,n-1]; the three indices in a clause must be distinct; and there are no unused or trailing input bits. The exact encoded bit length is L=n+m+2+3m(1+w). Valid clauses are signed proper width-three clauses. A malformed bitstring is not in the language and must be rejected; SAT and UNSAT labels for wellformed inputs must both be correct. This explicit polynomial-time parsable proper-3CNF language is NP-complete under standard polynomial many-one reductions; the precise binary grammar fixes the cost measure. The proof below applies just as well to any *fixed decidable* language.

Let A be **one** fixed finite uniform total deterministic off-line multitape Turing machine across all lengths: one two-way read-only bit input tape with left/right endmarkers, a fixed number b_A>=1 of two-way read/write work tapes, fixed finite work alphabet Gamma_A and control-state set Q_A, and one transition per step. Heads begin on the left markers; they move at most one cell per transition, cannot move beyond endmarkers on the input tape, and output ACCEPT/REJECT through the halting state. All work tapes begin blank; there is no advice, oracle or initial nonblank work area. Totality and correct classification apply to every binary string, including malformed strings. Every input read, reread, move, index update, stack/buffer operation, lookup construction, copy, simulation, and recomputation is charged through real transitions. An unbounded-word RAM operation has **no** automatic unit-cost equivalence; any alternative-machine translation must separately prove overhead on the same computed function.

For x let T_A(x) count all transitions until halting and let S_A(x) count, **summed over work tapes**, every distinct writable cell visited at any time, including initial head cells and cells visited without modification. For the same execution,

$$
S_A(x)\le b_A(T_A(x)+1). \tag{M1}
$$

Proof: a head can first visit at most one new cell per transition and visits at most one initially. Sum over b_A tapes. No assignment counting or configuration-capacity assumption is used.

## 3. Target and exact logical dependence

The target is

$$
\begin{aligned}
\forall A\in\mathcal D_{3SAT}\ \forall k\in\mathbb Z_{\ge1}\
\forall C>0\ \forall L_0\in\mathbb N\
\exists x\in V:\quad
|x|\ge L_0\ \land\
T_A(x)>C(|x|+1)^k ,
\end{aligned} \tag{SEP}
$$

where V contains **valid** encodings and A must be a total correct decider on **all** bitstrings. The hard input x may depend on A,k,C,L0. This does not require a single recognizable all-UNSAT family hard for all A.

**Logical equivalence, not new proof progress:** (SEP) is equivalent to P != NP for this fixed NP-complete encoding. If P=NP, a single correct total uniform polynomial-time decider falsifies (SEP). Conversely, if (SEP) fails, some fixed A has a polynomial upper bound on every sufficiently long *valid* input. The finitely many shorter valid inputs have a finite maximum runtime. A new uniform machine can check validity in polynomial time, reject invalid inputs immediately, and run A only on valid inputs, obtaining a uniform all-binary-input polynomial bound. Then 3-SAT is in P, implying P=NP. This proves the equivalence but is **not** a proof of (SEP).

## 4. Counterexample 001A: pointwise minimization destroys uniformity

Define, for each L separately,

$$
m(L)=\min_{\substack{A\text{ fixed finite total}\\A\text{ correct on ALL binary inputs}}}
\max_{x\in\{0,1\}^L}T_A(x).
$$

**Theorem, complete symbolic proof, independent review pending:**

$$
m(L)\le L+O(1)
\qquad\text{for every integer }L\ge0. \tag{N1}
$$

This holds for **every decidable language**, even if that language has no polynomial-time decider.

**Construction.** Fix L and a correct total general decider D. Construct a new finite machine A_L. Its control states contain a full depth-L binary input-prefix trie, including the correct membership bit for each of the 2^L leaves. On an input with exactly L bits, traverse one trie edge per bit and read the right endmarker to choose the stored ACCEPT/REJECT leaf; this takes at most L+O(1) transitions, with O(1) visited work cells. On an input shorter or longer than L, transfer control to the *same fixed* fallback D after repositioning the read-only input head to its left marker. The fallback is a finite total program and ensures global correctness. A_L is a legal finite uniform machine for its own fixed program, with O(2^L) finite-control states, but the index L determines **a different program**. All leaf bits are hardwired at construction and the enormous program description is not charged as runtime of this particular machine. The minimization above explicitly permits that nonuniform choice. Therefore (N1) follows. QED.

The invalid inference is

$$
\forall L\ \exists A_L \quad\not\Longrightarrow\quad
\exists A\ \forall L .
$$

Consequence: the per-length minimum m(L) is a provably linear **false hardness objective**, regardless of whether P=NP. A family A_L with exponentially large nonuniform finite control is not a single polynomial-time uniform SAT algorithm. Do not use min over different machines as the central resource lower-bound target.

## 5. Counterexample 001B: original-input-head motion is avoidable

**Theorem, complete constructive proof, independent review pending.** For any fixed total deterministic multitape decider A with b_A work tapes, there exists another fixed total correct decider B with b_A+1 work tapes such that for every binary input x of length L,

$$
T_B(x)=O_A(L+T_A(x)+1),\qquad
S_B(x)\le S_A(x)+L+O_A(1), \tag{N2}
$$

and B's physical read-only source-input head makes only O(L) movements on the whole computation and **no movements after initial copying**, even when T_B(x) is enormous.

**Construction.** B traverses the actual read-only input once, copying the L bits and both endmarker semantics onto one initially blank work tape. It then positions the copied-tape head at its simulated initial input location; this positioning costs O(L) transitions and never moves the physical source head again. B simulates A's finite controller, b_A work tapes and read-only input head, using its b_A+1 work tapes; the extra tape contains A's simulated read-only input and is *never overwritten*. All simulated heads move one cell per simulated transition. Since the simulated input is an ordinary work tape, B reads it in O_A(1) real transitions per transition of A. Thus the total bound and writable-space bound hold. The copied tape is charged L+O(1) visited writable cells and no oracle or free random access is used. B's actual source head remains at the right input endmarker. Correctness and totality are inherited from A, with malformed inputs also preserved. QED.

**Exact scope.** This falsifies any claimed *unconditional superlinear lower bound on physical original-input-head motion or necessary rescanning of the original source tape* for every correct multitape SAT decider. It does **not** falsify a lower bound on total time: all computational work is still charged to B. Merely counting distinct acquired source bits is also bounded by L and cannot itself yield a superpolynomial lower bound. Any credible information cost must instead count unavoidable charged operations, including processing a compact global invariant, maintaining summaries or recomputation. This construction uses one extra fixed work tape, which is permitted by the model; a claim about an exact smaller tape count needs its own translation.

## 6. Dependency DAG, candidate bottleneck and space scope

The active **unrestricted-machine dependency DAG** is:

- **D0, KNOWN THEOREM:** explicit polynomial-time parsable NP-complete input language; both-label total correctness; fixed deterministic multitape model.
- **D1, MODEL INVARIANT:** fully paid trace plus same-realization relation (M1); counterexamples (N1), (N2) invalidate unsound objectives.
- **D2, OPEN [TMR-2]:** identify a nontrivial *input-aware* distinction/recomputation cost d_A(x) that respects arbitrary compact algebraic summaries and adaptive rereads.
- **D3, OPEN [TMR-4]:** prove a cost-sound all-transition map for **every actual** A trace with d_A(x)<=T_A(x), preserving both terminal labels, including any cheap representations, not merely one proof-system path. A potential must telescope on every abstract edge.
- **D4, OPEN [TMR-3]:** independently prove for every correct **fixed** A, every k,C,L0, a valid x of length >=L0 with d_A(x)>C(L+1)^k, or a quantitatively stronger same-machine retention/recomputation tradeoff. Cover all polynomial-space exponents, not just subpolynomial space.
- **D5, CONDITIONAL ARROW:** D2+D3+D4 imply (SEP) by d_A(x)<=T_A(x).
- **D6, KNOWN THEOREM:** (SEP) plus NP-completeness imply P != NP.
- **D7, OPEN [TMR-5]:** independent red-team review of D1, any proposed D2-D4 and all model/transcript transfers.

**Weakest sufficient modular bottleneck lemma proposed (CANDIDATE, NOT proved):** produce a *genuinely independently defined* nonnegative paid-distinction measure d_A(x) on each **real** execution with (i) universal cost soundness d_A(x)<=T_A(x), and (ii) an unbounded polynomial-exponent family of valid-input lower bounds with the exact quantifiers of D4. The resulting implication to (SEP) is a one-line proof; the nontrivial, missing work is establishing (i) for unrestricted executions and (ii) for the independent d, not choosing d_A=T_A and thereby merely renaming the open conjecture. There is no representation-independent d with these proven properties today.

An alternative sufficient but **equivalent-in-aggregate** resource target is: for **every** integer k>=1 and B>0, any fixed correct total A using at most B(L+1)^(k+1) writable cells on **all** inputs has arbitrarily large valid x with T_A(x)>B(L+1)^k. Any globally polynomial-time A with exponent k also uses S<=b_A(T+1), and after increasing B satisfies this workspace cap, contradicting the corresponding time lower bound. Proving one fixed k, or proving the bound only with S=L^{o(1)}, does not exclude all polynomial-time exponents. Proving the full forall-k family is as hard as the separation target in logical strength and must not be called a breakthrough without an independently established new inequality.

**Primary-literature boundary:** Fortnow and van Melkebeek (2000), and Fortnow, Lipton, van Melkebeek and Viglas (2005), give SAT time-space tradeoffs under restricted simultaneous space budgets on random-access models. Williams (2006) gives improvements including a random-access SAT exclusion at time n^{sqrt(3)} and subpolynomial space. None establishes unbounded polynomial-time lower bounds with arbitrary polynomial workspace on this fixed multitape machine. Any translation of their RAM results here must pay the simulation.

## 7. Executed finite tests and hostile controls

**Reproducer:** experiments/tmr/tmr1_slice_counterexample.py, verified Git blob 8771602044547ccd3770c8314cf6e5c53ee9cb3f; SHA-256 of the executed local bytes 5a82ab190cd6a8a75139365290ecc033d494d54a468485e01b8245029e641537.

**Immutable raw output:** results/raw/tmr/2026-11-13_1303_TMR1_SLICE_RAW.json, verified Git blob cff36a57d85d9bd12f26fb0ec559613a842800d2; SHA-256 of executed local raw bytes 0c436c4ae6af2196fdf95919ea28fc292c6cf847634a138df973ec42d5cdac1a.

Executed on local Python standard library on 2026-11-13 PST in a single 1.10-second invocation (below 25-second chunk budget), no randomness. Exhaustively classified **all 32,768** binary strings of L=15: 48 valid signed proper three-literal CNF inputs, all SAT, and 32,720 malformed; the 15-bit full trie has 65,535 prefix nodes and 32,768 answer leaves. Constructed the 85-bit n=3,m=8 UNSAT formula that forbids all eight assignments; deletion of each individual clause restores SAT; unused-variable n=4 padding preserves UNSAT. Checked 48 variable renaming/polarity transforms, parity/XOR satisfiable and contradictory pairs, independent products, Horn and 2-SAT SAT/UNSAT controls, and five malformed controls. The code does not run a literal 65,535-state machine or physically instrument a tape: it *tabulates the same leaf function* and records the symbolic construction's state and scan counts. The general theorems rest on their proofs, not finite sample evidence.

**Not executed / no inference:** no native /341 or /386 checker; no full corpus preflight executable, LaTeX compile or external independent machine simulation; no auxiliary-variable generality experiment, treewidth DP benchmark, or formal verification of all-machine complexity. Their absence cannot strengthen a lower-bound claim. The n=3 controls are bounded-width examples, not a universal treewidth hardness result. Horn/2-SAT toy controls are width-1/2 logical controls rather than malformed surrogates for the strict proper-3CNF grammar. Arithmetic/affine compact solutions, long delays, padding, re-encodings and shared subcomputations remain admissible in the unrestricted machine; the two negative lemmas apply independently of those choices.

## 8. References and next decisive target

1. S. Cook (1971), *The Complexity of Theorem-Proving Procedures*, STOC, https://doi.org/10.1145/800157.805047. NP-completeness background, not a lower bound.
2. L. Fortnow and D. van Melkebeek (2000), *Time-Space Tradeoffs for Nondeterministic Computation*, ECCC TR00-028, https://eccc.weizmann.ac.il/report/2000/028/. Random-access SAT time-space lower bound with restricted small space.
3. L. Fortnow, R. Lipton, D. van Melkebeek and A. Viglas (2005), *Time-Space Lower Bounds for Satisfiability*, J. ACM 52(6):835-865, https://doi.org/10.1145/1101821.1101822. Simultaneous polynomial time/space bounds only in particular exponent regions.
4. R. Williams (2006), *Inductive Time-Space Lower Bounds for SAT and Related Problems*, Computational Complexity 15:433-470, https://doi.org/10.1007/s00037-007-0221-1. Exact machine/space qualifiers required.
5. Historical original file reports and Git SHA references listed in Section 1. They are evidence of model pitfalls, not primary proof authority.

**Next TMR-1 target:** Independently verify the all-input validity parser and the A-to-B copy simulator under an *exact fixed multitape transition schema*, then try to formulate a nontrivial trace-observable potential smaller than T that (unlike source-head motion) survives source copying, GF(2) elimination and arbitrary compact representations. Request TMR-5 to falsify N1/N2 or approve their exact scope, TMR-2 to exhibit one true input-aware unavoidable event in arbitrary runs, TMR-3 to test the forall-k simultaneous time-space target rather than fixed small-space exponents, and TMR-4 to prove cost-soundness for every concrete transition.

**END_OF_VERIFIED_REPORT::TMR-1::MACHINE-SLICE-FIREWALL-001**