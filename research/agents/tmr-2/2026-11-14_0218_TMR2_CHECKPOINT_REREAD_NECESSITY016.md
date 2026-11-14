# TMR-2/016: source-aware checkpoint indistinguishability and charged reacquisition

**Pacific timestamp:** 2026-11-14 02:18 PST, America/Los_Angeles. **Role:** TMR-2 Information Necessity. **Repository:** j15marti/pnp, main. **New mathematical status:** CANDIDATE/RESTRICTED, subject to TMR-5/TMR-1 independent mathematical review. **Native finite evidence:** COMPUTATIONAL. **General superpolynomial SAT lower bound:** OPEN.

## 1. Exact machine model, source and theorem

Fix a *single* finite total deterministic one-original-input-head multitape Turing machine A deciding both SAT and UNSAT correctly on a fixed explicit 3-CNF encoding for every binary source length, including a designated correct malformed-input outcome. Its input has L data bits at physical positions 1,...,L, with immutable endmarkers at 0 and L+1. The head reads **only its current cell**, moves at most one source cell per charged transition and starts at position 0. A has finite control, a fixed finite alphabet and finitely many ordinary writable work tapes. All work contents and head positions are counted as part of the internal configuration. T_A(x) counts physical transitions, S_A(x) counts visited writable work cells. No source-copy, oracle, word-RAM operation, external advice or free address lookup is assumed.

Let I(c) denote complete finite control, all work-tape contents, all writable-head positions and the source-head position **but not the immutable input string**. This is deliberately *not* a full concrete configuration; a full state also contains or is explicitly bound to x.

**Lemma TMR2-CR16 (conditional source-aware reacquisition).** Suppose x,y have the same encoded length and distinct correct decision labels. Suppose at possibly different checkpoints of executions of the *same fixed correct A*, their internal configurations agree, I(c_x)=I(c_y), with the common original-input head at position p. Put D={j in {1,...,L}:x_j != y_j}. Then **both** remaining executions must reach and read a position in D before terminating with their respective correct labels. In particular, if every source-head transition moves at most one cell and the observed symbol is that of the current cell, the number of remaining transitions on each source is at least

$$
1+\min_{j\in D}|j-p|.
$$

The claim makes **no** online or one-pass assumption. It explicitly permits the entire source to have been visited before the checkpoints, unrestricted writable history before the checkpoint, future rereads, algebraic processing, caching and recomputation. It is conditional on an *equal complete internal state* at the checkpoint. Different source strings are not identical full machine configurations.

**Proof.** Couple the two deterministic executions starting from their equal internal configurations. Until the first current-cell read of a position j where x_j differs from y_j, both machines see the same local input symbols, have the same full work contents and head positions, and therefore make identical transitions. If neither continuation reads D, both halt with the same label, contradicting correct opposite labels. The first distinguishing read is the same physical read event in the coupled traces. From p, reaching any j in D requires at least |j-p| unit head moves, and a transition reading that cell then distinguishes the sources. This gives the bound for both continuations. Work-tape rewrites and any preprocessing only consume additional transitions. QED.

For multiple physically read-only input heads at positions p_h, the direct counterpart replaces the geometric term by min_{h,j in D}|j-p_h|. No multitape conclusion follows if an unmodeled nonlocal source port or additional preloaded input copy is granted for free.

## 2. A fixed all-input wash wrapper shows why internal-state equality does NOT prove indistinguishability

**Construction TMR2-WASH16.** Given **any one** eligible fixed correct total A, compile **one** fixed uniform machine B_A. It performs one fully charged outward sweep to the right marker, reads all L original bits at their actual cells, returns the original head left, erases its finite-control observation and enters A's exact initial state, with every original work tape untouched. A then executes without change. The prepass has precisely L+1 forward and L+1 backward transitions, including marker travel. Thus, under the declared composition convention,

$$
T_{B_A}(x)=2(L+1)+T_A(x),\qquad S_{B_A}(x)=S_A(x).
$$

The checkpoint after the prepass has the **same** I(c) for every source x, indeed across all lengths, even though every bit was physically read in the past. The immutable source tape is still different. Both SAT and UNSAT are decided correctly after the checkpoint because A rereads as needed. This is a constructive counterexample to the claim that two input histories reaching the same finite-control/workspace/head configuration must have identical future outputs. The computation can retain *zero* acquired bits at that checkpoint and later reacquire them. A source-blind abstraction that merges these checkpoints cannot infer a unique future terminal label: a conservative MAY abstraction must preserve both branches unless it proves a source-bound reachable-state invariant.

This construction is adjacent to TMR-3/014's parity-prepass compiler and TMR-4/015's late-copy compiler. The **new scoped contribution here** is the explicit source-aware common-checkpoint necessity lemma, its geometric reacquisition cost and the unbounded opposite-label instance family below. The wash wrapper alone is not advertised as an independent SAT complexity breakthrough.

## 3. Exact unbounded SAT/UNSAT last-bit sibling family

For independently reproducible concrete evidence, use a restricted **sign-stream** encoding of unbounded numbers of proper three-literal clauses over *exactly three fixed variables* x0,x1,x2. Each 3-bit row m in {0,...,7} encodes one clause falsified by exactly assignment m. Thus SAT iff at least one of the eight masks is not present; UNSAT iff all eight are present. Nonmultiples of three data bits are malformed. This restricted problem is a regular language, **not general NP-complete 3-SAT**.

For each integer r >= 0, define the common row prefix

$$
P_r=(0,1,2,3,4,5,6,\underbrace{0,\ldots,0}_{r\text{ additional rows}})
$$

and the genuine valid same-length siblings

$$
x_r=P_r\mathbin{\|}110,\qquad
y_r=P_r\mathbin{\|}111,\qquad
L=24+3r.
$$

Here vertical concatenation means 3-bit mask-row concatenation, not logical OR. The input x_r is SAT (mask 7 never occurs); y_r is UNSAT (all eight occur). Their *only* differing original-source position is the final bit j=L. For a common erased checkpoint with head at p=0, Lemma CR16 demands at least **L+1 physical post-checkpoint transitions** before correct opposite outputs can diverge, on both sources. Arbitrarily many duplicate-mask rows simply move this required revisit farther away. This is a linear source-transport necessity, not superpolynomial logical consistency work.

One explicit fixed finite-control physical controller first performs the erased wash sweep/return, then performs a second outward sweep accumulating an eight-bit forbidden-assignment mask, 2-bit partial clause and mod-3 parsing phase, returns left, and outputs SAT, UNSAT or MALFORMED. All registers have constant size, with zero visited writable work cells. The physical execution takes exactly

$$
T_M(x)=4(L+1)+1,\qquad S_M(x)=0
$$

for every binary source, regardless of label. Its checkpoint after 2(L+1) transitions is literally the same internal configuration on all sources. The actual post-checkpoint time is 2(L+1)+1, within a factor of two of the source-distance bound on the siblings. This controller is correct for unbounded clause count but only three variables.

## 4. Independent TMR-3/014 audit and model limitations

The original TMR-3/014 report, **original native Python source** and **original raw JSON** were inspected. Independently reconstructing its physical two-crossing projection gives, for each cut after original bit i, an outward crossing containing x_i and a returning crossing containing full-source parity:

$$
c_i(x)=(x_i,\bigoplus_{j=1}^{L}x_j).
$$

On a one-head locally moving input model, before a *first outward crossing* of cut i the machine cannot have read a future source cell beyond that cut. Therefore a **one-crossing complete record at that cut cannot depend on previously unread suffix values**. Two crossings suffice via the parity return. My independently written verifier checks the current-cell reading rule, every crossing tag, and two per-cut events. This substantiates the **one-versus-two suffix-dependence threshold** of TMR-3/014 as **PROVED/RESTRICTED for the declared physical single-head model** after independent argument. It does not assert bounded dependence of all *normalized* full solver crossing codes or a general SAT lower bound. TMR-5/013 independently identified a one-cell off-head flaw in **TMR-4/016's different original V8 emulator**; the present independent native implementation reads only source cell p when 1<=p<=L, not an adjacent cell.

Literature context: Buhrman and de Wolf (2002) formalize deterministic decision-tree/certificate complexity, a *query* notion. Such a certificate does not charge subsequent source-head movement or arithmetic reconstruction. Hennie's 1965 off-line one-tape crossing-sequence analyses use their declared tape geometry, not a free bridge to arbitrary modern multitape computation. Neither paper supplies the unproved all-polynomial-exponent SAT processing lower bound.

- H. Buhrman and R. de Wolf, *Complexity Measures and Decision Tree Complexity: A Survey*, Theoretical Computer Science 288 (2002), 21-43, DOI: https://doi.org/10.1016/S0304-3975(01)00144-X ; author's preprint: https://homepages.cwi.nl/~rdewolf/publ/qc/dectree.pdf .
- F. C. Hennie, *One-tape, off-line Turing machine computations*, Information and Control 8 (1965), 553-578, original reprint catalog: https://ntrs.nasa.gov/citations/19660041785 .

## 5. Native execution, hostile controls, provenance

**Exact independently authored and OS-native executed CPython script:** `experiments/tmr/tmr2_checkpoint_reread016.py`. **Exact raw execution:** `results/raw/tmr/2026-11-14_0218_TMR2_CHECKPOINT_REREAD016_RAW.json`. Both were read back after GitHub publication and had the same Git blob IDs as the actual tested local bytes: source `59b068d55aabdab6337df8ee6a497c84451f75e9`, raw `26a22a1daffa6c44a80b2ca52f567b5a03acc08e`. Runtime approximately 1.64 seconds, one chunk.

- All **8,191** binary strings of lengths 0..12; classification **4,681 SAT, 3,510 MALFORMED** (UNSAT requires at least eight completed rows, so none occur within 12 bits); one identical erased checkpoint at every tested length.
- Every one of **40,320** permutations of all eight forbidden masks at L=24, correctly UNSAT, with the same erased checkpoint.
- **129** different SAT/UNSAT last-bit sibling pairs, r=0..128 and L=24..408, exactly one physically final-bit difference, with the same checkpoint and the proved distance obligation.
- **4,697,933** charged physical-model transitions, **2,227,044** physical current-cell source reads, and **180,228** independent two-crossing-prepass events over exhaustive inputs; **zero failed assertions**.

This finite test validates the declared *restricted* model, not any arbitrary deterministic 3-SAT machine compiler. **Executed hostile controls** include valid SAT, valid UNSAT, malformed, length extension via duplicate clauses, both opposite labels and physically correct last-position read. Variable renaming, auxiliary-variable encodings, Horn/2-SAT/GF(2) Gaussian-elimination solvers, bounded-treewidth DP, unrelated products, other word-RAM models and actual all-variable SAT solvers were **not executed**. They are not excluded: arbitrary A is allowed inside the symbolic wash wrapper, but no algorithm-specific asymptotic runtime claim is made.

## 6. Dependency and corpus state

Required sources read before analysis: superseding five-TMR directive on main (blob `47459817e66dccf1f3079e6c724c0fd2643e7bc4`); root proof1.txt complete 28,714 chars (blob `06f7ebc8c2283304a0f5200b518c6e48fa41e343`); root proof2.txt **complete 1,051,196-character authentic Git blob** (blob `930c5eeddafce656717f28055a7a9a755f44737c`, because the contents API returned a blank body); root main.tex **complete 2,525,134-character authentic Git blob** (blob `d3db01d221df39f096f31237643268132edfcd87`, because the contents API returned a blank body); AGENTS.md, CODEX.md, repository pnp-research skill, issue #3 through TMR-5/013, five newest TMR handoffs, original TMR-2/015, TMR-3/014 (including code/raw), TMR-4/016 (including code/raw), and TMR-5/013. Historical work is preserved; superseded LSPV ownership is not revived.

**PROVED/RESTRICTED after independent proof audit:** TMR-3/014 one-versus-two physical crossing observation, at precisely declared scope. **CANDIDATE/RESTRICTED:** CR16 and WASH16, pending TMR-5/TMR-1 proof review. **COMPUTATIONAL:** the exact native finite execution above. **OPEN:** finding *any* unconditional computational necessity invariant on full executions of arbitrary A which cannot be neutralized by compact algebra, speculative computation before observation, source rereads, retention/recomputation or polynomial workspace. The exact P!=NP target still has quantifiers: for every correct fixed uniform A, each k>=1, C>0 and L0, there exists a valid F with |F|>=L0 and T_A(F)>C(|F|+1)^k. None of these results comes close to that all-exponent obligation.

**Trackers:** TRACKERS REVIEWED; NO MATERIAL CHANGE. No new P=NP algorithm, P!=NP implication or theorem dependency changed their node status; neither root proof tracker was edited. Root main.tex has TMR ownership markers but is left unchanged for TMR-5 synthesis after peer review. No schedules/tasks were changed.

**ONE NEXT TARGET for TMR-2:** formulate an *input-aware* common-checkpoint necessity measure that accounts for source retrieval, retained state and compact computation **without assuming two runs merge internally**. TMR-3 should charge source-head distances on the *same execution*, TMR-4 should preserve immutable source binding in every all-transition abstraction, and TMR-5 should adversarially audit CR16/WASH16 and try algebraic/recomputation falsifiers before manuscript promotion.

END_OF_REPORT::TMR-2::016::2026-11-14_0218_PST
