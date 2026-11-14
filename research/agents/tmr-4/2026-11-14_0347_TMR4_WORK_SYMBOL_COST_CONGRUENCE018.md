# TMR-4/018: cost-exact work-tape alphabet quotient, and a parity-gate falsifier

**Pacific timestamp:** 2026-11-14 03:47 PST (America/Los_Angeles).
**Role:** TMR-4, Cost-Sound Abstraction, successor to the retired LSPV organization.
**New theorem:** CANDIDATE/RESTRICTED pending independent TMR-1/TMR-5 review; proof is given below.
**Finite experimental evidence:** COMPUTATIONAL.
**Unrestricted superpolynomial 3-SAT time lower bound and P versus NP:** OPEN.

## 1. Claim and precise fixed-machine model

Let A be any ONE fixed finite deterministic total multitape decider operating for ALL encoded input lengths L. Fix finite input and work alphabets, finitely many independently locally moving input heads and work heads, a read-only immutable binary source x with endmarkers, and exact SAT/UNSAT/MALFORMED terminal labels. Unit physical transitions count as time; every visited writable work cell, including buffer and scratch cells, counts in the same-machine space measure. No random access, unit-cost unbounded arithmetic, SAT oracle, uncharged preprocessing, or algorithm-dependent length advice is introduced.

TMR-1/017 establishes a mechanically checkable cost-exact congruence over finite CONTROL states while retaining all tape symbols. This report extends the **type of abstracted information** to work-tape SYMBOLS themselves, retaining complete source binding and all work-head positions and visited-cell footprints. This is a local algebraic quotient, not an assertion of new general bisimulation theory.

For each work tape i choose a surjective finite alphabet map rho_i:Gamma_i -> Delta_i, with an induced abstract blank symbol. Keep A's control q and all input symbols exact. Suppose, for EVERY control q, EVERY input-head read-symbol tuple u, and EVERY pair of work-head read tuples v,v' with rho_i(v_i)=rho_i(v'_i) for all i, the two prescribed concrete transitions have:

1. exactly the same next control q' and terminal/output behavior;
2. exactly the same original-input and writable-head movements and exact same unit step cost;
3. for each work tape i, writes w_i,w'_i with rho_i(w_i)=rho_i(w'_i).

This finite, all-symbol criterion is called **TMR4-WSQ18 local work-symbol congruence**. It is decidable by exhaustive comparison of the explicit finite instruction table; no reachability, correctness proof in a calculus, or runtime forecast is used. The condition can conservatively reject semantically safe erasures.

**Theorem TMR4-WSQ18 (symbolic proof, independent audit pending).** The quotient configurations retain (x, q, exact input heads, exact work heads, every work-tape cell's rho-image, and exact visited-work-cell footprint). The initial quotient is the exact projection of A's initial state. Every concrete legal transition projects to one quotient transition of EXACTLY the same cost, and every quotient transition can be replayed from EACH concrete representative with the same source, head positions, q and projected tapes, reaching another related state of the same cost. SAT, UNSAT and MALFORMED terminals are preserved. Consequently, for every input x,

$$
T_{A/\rho}(x)=T_A(x),\qquad S_{A/\rho}(x)=S_A(x).
$$

**Proof.** The criterion makes the proposed abstract next-state map independent of the choice of representatives for the symbols currently scanned. The exact x and exact head positions determine the input symbols; projected tape cells determine a rho-fiber for each scanned writable symbol. All concrete transitions in the fiber have the same next control, physical displacements and projected writes, hence the same abstract successor. Induction from the related initial pair proves all-step forward simulation. Conversely, the same equality for EVERY representative gives a concrete step for any abstract step, and induction gives whole-path replay. Terminal labels depend on unmerged control and are identical. Input accesses, physical head trajectories and visited writable cell sets are identical at every corresponding prefix; thus both time and the same-run peak space are exactly equal. The abstract machine does NOT skip the original cost-one instructions just because a particular stored bit has become semantically invisible. QED.

This is a stronger kind of quotient than TMR-1/017's control-only certificate. It does NOT claim to find every safe memory erasure, nor prove a superpolynomial initial lower-bound potential. If abstract alphabet storage itself is physically implemented, initialization, rewriting, construction and simulation costs must be charged separately.

## 2. Nontrivial single-head, single-work-cell instantiation

Use an unbounded, explicitly declared three-variable proper ternary sign-stream CNF language. Each three source bits designate one signed clause over three distinct fixed variables; the clause excludes its indexed one of eight assignments. An incomplete final triple is MALFORMED, all eight forbidden assignments present means UNSAT, otherwise SAT. This restricted language is NOT NP-complete.

A fixed finite-state classifier records the eight-bit forbidden-assignment mask and at most two pending source bits in FINITE control. In front of it, a wrapper uses one ordinary locally moving input head and one one-cell writable tape with alphabet {0,1} and work head fixed at that cell. It scans the complete source outward, maintaining its XOR parity by a physical read-and-write of this cell on each data-bit transition, moves physically back to the left marker, then parses and classifies the same original input. Every input movement, reread, scratch write, gate and final terminal instruction costs one. The all-zero initial scratch symbol is the physical blank, and visited writable workspace is exactly one cell.

Erase the WHOLE scratch-cell alphabet by rho(0)=rho(1)=*. The parity updates differ as concrete work writes, so TMR-1/017's **full-action control-only** congruence does not by itself erase this information. Under TMR4-WSQ18, both writes project to *, while next control, source and work-head motions, output, and unit cost agree for ALL source/work symbol combinations. The quotient is therefore exact on every source.

Let q=L+1 denote the number of original-source moves from left to right endmarker. The inert parity wrapper satisfies

$$
T_{\mathrm{inert}}(x)=3q+1,\qquad
S_{\mathrm{inert}}(x)=1.
$$

This is not a claim that a better solver must perform the scan. The chosen machine deliberately performs it, and the quotient still charges it.

## 3. Hostile gated twin and all-edge Bellman analysis

Replace the return-to-parser gate by: if the actual scratch parity equals 1, execute one additional completely paid outward/return input roundtrip before parsing. Both versions are fixed total correct machines over all sign-stream lengths and output the same SAT/UNSAT/MALFORMED labels. The true source-bound machine time is

$$
T_{\mathrm{gated}}(x)=3q+1+2q b(x),
\qquad b(x)=\bigoplus_{i=1}^Lx_i.
$$

At the return gate (phase R, left-marker read L), the two work-symbol representatives prescribe different successor controls, A versus D. The local work-symbol congruence therefore correctly FAILS. An ordinary existential MAY quotient erasing the cell must retain BOTH gate edges; the false skip edge is replay-spurious on odd sources, but the true detour remains a genuine possible execution and cannot be deleted globally.

Here is an explicit Bellman-valid potential on EVERY edge of that full MAY graph with immutable source x and physical input-head position p (0 <= p <= q):

$$
\begin{aligned}
\Phi(S,p)&=3q-p+1,&\Phi(D,p)&=3q-p+1,\\
\Phi(R,p)&=p+q+1,&\Phi(E,p)&=p+q+1,\\
\Phi(A,p)&=q-p+1,&\Phi(H)&=0.
\end{aligned}
$$

S and R denote scanning and returning, D and E the extra outward and return detour, A the original classifier, and H any SAT/UNSAT/MALFORMED terminal. Every ordinary head move decreases Phi by exactly one. The S-right-endmarker to R and D-right-endmarker to E transitions also decrease it by exactly one, as do the E-left-marker to A and A-right-endmarker to terminal transitions. The erased gate's cheap R-to-A transition has equality; its R-to-D edge satisfies Phi(R,0)=q+1 <= 1+Phi(D,1)=3q+1. Thus for EVERY abstract edge a->a' of cost 1,

$$
\Phi(a)\le 1+\Phi(a'),\qquad \Phi(H)=0.
$$

The shortest abstract decision path is the physically genuine initial scan and return followed by its MAY-only cheap gate and classifier, giving

$$
d_{\rm MAY}(a_0,H)=\Phi(a_0)=3q+1.
$$

On odd-parity sources, the real physical machine requires another 2q transitions. In particular, cost soundness and a fully Bellman-valid potential DO NOT imply path replay or exactness of a permissive quotient.

A restricted, source-aware repair is possible WITHOUT pretending that the scan was free: inductively, at outward-scan source position p, the scratch symbol is the parity of the first max(0,p-1) data bits; throughout R it equals b(x). Retain this gate invariant, permitting only the actual branch. Adding 2q b(x) to Phi for the S and R phases, with the same D/E/A/H formulas, gives equality along every source-reachable refined edge and initial value 3q+1+2q b(x). This formula is a STATIC, explicitly proved property of this deliberately simple controller, not an oracle for arbitrary SAT runtime or a general computable cost potential. Any operational evaluation of b(x) from scratch must still pay for its input reads.

## 4. Executed direct evidence and independent arithmetic audit

**Hosted V8 direct execution:** the exact self-contained JavaScript audit function, subsequently serialized verbatim to the Node-compatible repository file, exhaustively compared ALL 1,799 control states against every input symbol L,0,1,R and both scratch values. It made 7,196 inert quotient equality checks and 7,196 gated checks. The inert certificate has zero violations; the gated certificate has precisely ONE violating symbol/control pair, (R,L), selecting A on scratch 0 and D on scratch 1.

Across 2,056 binary source fixtures (all 2,047 strings of length 0 through 10 and nine longer controls), 589 were SAT, three UNSAT and 1,464 MALFORMED. A separate assignment-mask semantic evaluator checked classifications. The physical simulator verified same-source current-cell reads, one-head legal moves, actual scratch updates, SAT/UNSAT/MALFORMED terminal labels, 150,980 concrete charged transitions and all actual-edge Bellman inequalities. Forward abstract-state exploration checked 344,448 abstract MAY-graph edges and Bellman inequalities, representing 176,336 reachable abstract states. All 2,056 inert quotients were cost exact. Of the gated runs, 1,026 odd-parity runs had an actual unreplayable cheap gate; these would omit exactly 20,784 concrete transitions. **Zero assertions failed.**

**Independent native CPython, LOCAL-ONLY:** a separately written arithmetic enumerator checked all five structural phase/head transition types for source lengths 0 through 300, both scratch values and every legal head position. It checked 457,520 potential inequalities with zero failures. This native script and results were NOT uploaded to GitHub; it is not a native replay of the original peer implementation. Neither the general symbolic A-to-quotient compiler nor the full repository preflight or LaTeX compilation was executed as an operating-system program.

**Verified GitHub evidence paths:**
- Executed source: experiments/tmr/tmr4_work_symbol_quotient018.cjs (blob 8b50a88e28b4f30deed2b8f249480f86ecb6e6fe).
- Raw counts: results/raw/tmr/2026-11-14_0343_TMR4_WORK_SYMBOL_QUOTIENT018_RAW.json (blob cfab8e147045ee4634e2c1b9b7eedefc7318bcbf).

All finite results remain COMPUTATIONAL. The symbolic theorem is independently reviewable but not promoted to general SAT lower-bound status.

## 5. Prior work, historical counterexamples, sources and limitations

TMR-1/017's original report and executable were read rather than inferred from a chat account: research/agents/tmr-1/2026-11-14_0309_TMR1_COST_EXACT_CONTROL_BISIMULATION017.md and experiments/tmr/tmr1_control_bisimulation017.cjs. TMR-4/017's original undecidability reduction and TMR-4/016 and TMR-5/013's original parity/MAY replay notes were also reviewed. Their limitations remain: any universally terminating complete exact-erasure criterion would decide an undecidable all-input property, but conservative sufficient criteria like WSQ18 are possible. WSQ18 extends the local alphabet that may be quotiented, not the class of computationally expensive SAT tasks proved unavoidable.

Original historical evidence: LSPV-5/511 accepted string-valued supports by the unchanged recovered /341 checker; LSPV-5/514's edge-suffix normalization is exact ONLY for the pinned checker; LSPV-5/523 found real accepted literal-order aliases with different probe counts; and LSPV-3/551 found a checker-accepted SAT source, while LSPV-3/544's cost abstraction covers a separately declared restricted proof language. Those real checker behaviors are NOT erased as fictitious branches, nor transplanted into unrestricted TM cost claims.

Primary foundational literature, verified at the stated scopes: Patrick and Radhia Cousot, Abstract Interpretation, POPL 1977, https://doi.org/10.1145/512950.512973 (general sound abstraction, not SAT lower bounds); Paige and Tarjan, Three Partition Refinement Algorithms, SIAM J. Comput. 16(6), 973-989 (1987), https://doi.org/10.1137/0216062 (finite partition refinement); Clarke, Grumberg, Jha, Lu and Veith, Counterexample-Guided Abstraction Refinement, CAV 2000, https://doi.org/10.1007/10722167_15 (replay-spurious counterexamples).

**Falsification firewall:** The theorem structurally accepts whatever correct uniform SAT machine A is supplied, including compact Gaussian GF(2), Horn and 2-SAT reasoning, bounded-treewidth DP, original-source rereads, disjoint products, sharing, padding, renaming, auxiliary variables, caching and recomputation. But only the above three-variable restricted controller was EXECUTED. It cannot force A to use a scratch parity cell, scan twice, compute a proof, or materialize a chosen algebraic representation. Arbitrary polynomial workspace remains permitted. No entropy or assignment-count argument has been converted into a compulsory processing cost.

**Scientific dependency remaining OPEN:**

$$
\text{certified cost-exact quotient of a given }A
\;\not\Rightarrow\;
\text{a noncircular superpolynomial initial potential valid for EVERY correct }A.
$$

The exact team target remains: for every fixed total correct uniform 3-SAT A, every integer k>=1, C>0 and L0, find a valid F with L>=L0 and T_A(F)>C(L+1)^k. No load-bearing arrow toward that all-exponent claim is closed.

## 6. Reconciliation, publication and next request

Read the 2026-11-13 12:49 PST replacement directive first and again before shared publication, SHA 47459817e66dccf1f3079e6c724c0fd2643e7bc4. Recovered root proof1.txt fully (28,714 characters, blob 06f7ebc8c2283304a0f5200b518c6e48fa41e343); root proof2.txt fully via authenticated Git blob (1,051,196 characters, blob 930c5eeddafce656717f28055a7a9a755f44737c, despite blank contents endpoint body); canonical main.tex fully via authenticated Git blob (2,528,412 characters, blob 31f68fe0fc5dcfb4f7947fb2dacd7d285074e2f5). Also read AGENTS.md, CODEX.md, the pnp-research skill, all five newest TMR handoffs and issue #3, including TMR-3/016.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Canonical root main.tex left unchanged for its whole-document owner TMR-5, pending synthesis. No scheduled tasks or historical roles were modified.

**ONE NEXT TARGET:** TMR-1/TMR-5 independently check WSQ18's forall-work-symbol criterion, especially exact writable-cell preservation and the source-aware parity-gate refinement. Then seek richer, finitely checkable inductive summary certificates on movable and multiply indexed work tapes, without removing genuine cheap computations or claiming general SAT hardness.

END_OF_REPORT::TMR-4::018::2026-11-14_0347_PST
