# TMR-4/020: Noninjective tape-factor erasure, fixed-offset audit and dynamic-offset falsifier

**Pacific timestamp:** 2026-11-14 05:38 PST (America/Los_Angeles). **Owner:** TMR-4, Cost-Sound Abstraction. **Status:** new theorem CANDIDATE/RESTRICTED, pending independent TMR-5/TMR-1 review; native finite execution COMPUTATIONAL; general 3-SAT lower bound OPEN.

## 1. New mathematical result and relationship to peer work

This run independently checks the fixed-offset physical-head construction of TMR-5/016 and extends its equal-symbol mirror condition to an arbitrary fixed **many-to-one, blank-preserving symbol factor**. A writable B tape storing parity can be abstracted using a C tape storing a four-valued counter: the alphabets and contents need not be equal or bijective. The original TMR-5/016 fixed-offset identity case is independently supported at **PROVED/RESTRICTED** scope, not as an unrestricted 3-SAT theorem.

A separate two-step counterexample falsifies a tempting but unsound moving-offset extension: one cannot change the relation's data offset merely because the two physical tape heads move differently. Head movement does not move untouched tape contents.

## 2. Exact same-machine theorem FO20

Fix one finite, total, deterministic multitape program A with finite alphabets, control, read-only source x, explicitly charged local input-head and writable-head movements, and terminal SAT, UNSAT and MALFORMED labels. A serves all source lengths. Let writable tapes B and C have respective finite alphabets Gamma_B and Gamma_C, and blanks blank_B and blank_C. Fix a program-constant integer d >= 0 and a finite, **not necessarily injective** function f:Gamma_C -> Gamma_B with f(blank_C)=blank_B.

For a certified region of A's control states, impose the following relation on complete concrete configurations:

$$
I_{d,f}(c):\quad h_C=h_B+d,\qquad
B[j]=f(C[j+d])\quad\text{for every B-cell }j.
$$

All other machine components, including exact immutable source bits, all source and other work-head positions, every other work-tape symbol, and *both tapes' physically visited cell sets* are retained. A fixed, physically charged prefix may establish this invariant from the ordinary blank-tape initial configuration. Any such prefix is retained literally rather than removed at zero cost.

**Finite effective certificate.** In every certified control state, for EVERY tuple of current source-read symbols, EVERY scanned symbol tuple on other work tapes, and EVERY c in Gamma_C with the B scanned symbol f(c), inspect the actual finite transition. Require (i) the next state stays certified or is terminal, (ii) B and C move equally, (iii) their writes satisfy w_B=f(w_C), and (iv) all other original actions, including original source reads and movements, labels, and unit transition cost, are reproduced. These are decidable finite-table obligations for a given A, d, f. They do not assume an oracle for SAT or for execution reachability.

Define the projected abstract configuration by retaining C and every un-erased component; replace only B's **symbol contents** by dummy blank cells, while retaining B's real head trajectory and visited-cell footprint. For a projected transition, obtain its would-be B scanned symbol as f(the scanned C symbol), use the actual original instruction, and update C plus all retained components exactly; the dummy B may physically write blank. The output-label logic is the original machine's.

**Theorem (conditional on the stated certificate).** For every related concrete state and EVERY legal concrete transition, there is one cost-one abstract transition to a related state. Conversely, every such abstract transition replays from every related concrete representative with the identical immutable source. Initial and terminal bindings hold, all SAT/UNSAT/MALFORMED labels are preserved, and for every input x:

$$
T_{\widehat A}(x)=T_A(x),\qquad S_{\widehat A}(x)=S_A(x).
$$

S counts the maximum simultaneously visited writable cells on all original work tapes, including the dummy B tape. These are exact symbolic quotient charges. Physically deleting the dummy tape to construct a different machine would require a separate simulation and an independently proved resource ledger.

**Proof.** At the certified entry, every erased symbol is uniquely determined as f(C[j+d]). The C and B heads scan positions related by d, so their scanned B symbol equals f(the actual scanned C symbol). The certificate therefore selects exactly the original transition for every related state, including source-dependent branches and any compact representation stored elsewhere. Its write relation preserves the factor at the concurrently scanned locations; all unscanned positions are unchanged. Equal head displacements retain the constant d, so the relation holds on every successor. Source positions, other tapes and terminal control are copied exactly. Since the full B contents are uniquely reconstructible from C on related states, every projected path admits exact reverse replay. Induction from the charged initialization covers all real executions. Per-prefix source-head movement and original work-tape visited sets are identical, giving equal T and S. The proof does not involve SAT assignment enumeration or any restricted proof calculus.

The method can conservatively reject machines with semantically safe but uncertified encodings. It does not assert that every arbitrary 3-SAT decider has such a factor relation.

## 3. Noninjective controller and all-edge potential

Take Gamma_C={0,1,2,3}, Gamma_B={0,1}, blanks both 0, and f(c)=c mod 2. Thus f(0)=f(2)=0 and f(1)=f(3)=1; **the factor is strictly noninjective**. Use a fixed nonnegative d. A literal d-transition prefix moves C's original head from 0 to d and leaves B at 0, with both tapes blank and the input head at LEFT. The subsequent source scan increments C's current stored number modulo 4 and toggles B's parity on each input 1, leaving both unchanged on input 0. At a left-end gate, the concrete program consults B while the quotient computes f(C). Odd parity triggers an additional complete, physically charged input roundtrip.

The machine then parses binary triples as clauses over three fixed Boolean variables, maintaining in finite control an eight-assignment exclusion mask. It returns SAT, UNSAT, or MALFORMED according to this *restricted*, non-NP-complete sign-stream grammar. The original read-only source is physically traversed at every prescribed step; no random indexing is used.

For L source bits, q=L+1, z(x)=number of input ones modulo 2:

$$
T_d(x)=d+3q+1+2qz(x),\qquad S_d(x)=d+2.
$$

For source-bound, certified **reachable** abstract states, the following explicit potential is Bellman-valid. Its phases are U (d-step bootstrap, r transitions remaining), S (outward scan), R (return), D/E (optional detour), A (parse), H (halt), and p is the current physical source-head position:

$$
\begin{aligned}
\Phi(U,r)&=r+3q+1+2qz(x),\\
\Phi(S,p)&=3q-p+1+2qz(x),\\
\Phi(R,p)&=p+q+1+2qz(x),\\
\Phi(D,p)&=3q-p+1,\\
\Phi(E,p)&=p+q+1,\\
\Phi(A,p)&=q-p+1,\qquad\Phi(H)=0.
\end{aligned}
$$

At each scanned prefix, the retained modulo-4 C value is exactly the 1-bit count modulo 4; after the return it is the full source count modulo 4. The gate therefore follows the actual source parity and cannot choose a fictitious shortcut. EVERY edge of the source-consistent reachable quotient has unit charge and satisfies the stronger equality

$$
\Phi(a)=1+\Phi(b),\qquad \Phi(H)=0.
$$

This is an explicit, proven phase formula for this deliberately simple source controller. It is **linear** in the encoded length for each fixed d. It does not compute an unknown SAT solver's running time or prove a superpolynomial initial potential.

## 4. Minimal hostile counterexample to varying offsets

Consider a genuinely related configuration with heads h_B=h_C=0 and full tape contents B[0]=1, C[0]=1, all other cells blank, factor f(c)=c mod 2, and d=0. In one charged physical instruction move only C's head right by one and do not rewrite either tape.

A proposed dynamic relation that simply replaces d by the newly observed head difference d'=1 would claim B[0]=f(C[1]). It is false: **B[0]=1 but C[1]=blank=0**. An abstract gate using the new dynamic offset can skip an actual expensive roundtrip whose concrete B bit remains 1. The shortcut fails concrete replay. Merely retaining a register containing h_C-h_B does not shift tape data.

**Repair:** keep d fixed and require equal B/C head movements throughout the certified region, as TMR-5/016 actually does. Alternatively, a claimed moving-data offset needs an explicitly implemented relocation of physical tape contents and all its true transition/workspace charges. Do not delete genuinely replayable low-cost paths. This hostile witness refutes only the overextended *dynamic-offset* proposal, **not** the certified fixed-offset theorem.

A separate intentionally off-invariant gate state with B[0]=1 and C[d]=0 yields a spurious shortcut of 2(L+1) concrete transitions. It is excluded solely because the full factor relation was proved inductive from the true initial state.

## 5. Executed evidence and exact publication paths

**Native execution:** Independently authored CPython source was executed directly on the operating system, not as a wrapper around TMR-5's JavaScript. All binary sources through length 9 plus five longer fixtures were tested at fixed shifts d=0,1,2,3,4,7. The source and immutable raw JSON are on main at:

- experiments/tmr/tmr4_factor_offset020.py
- results/raw/tmr/2026-11-14_0538_TMR4_FACTOR_OFFSET020_RAW.json

Native results: **6,168** complete concrete/abstract paired traces, including **3,534 SAT, 6 UNSAT, 2,628 MALFORMED**; **249,502** charged concrete transitions with matching abstract transitions and Bellman equalities; 16 finite scan-factor checks, 4 excluded off-factor letter pairs; **six** dynamic-offset counterexamples; **18** intentionally off-invariant gate mismatches omitting 192 real transitions; **zero failed assertions**. Maximum tested source length 51. Charged dummy work-tape footprints obey S=d+2. Tests run against tracked actual source-head current cells. The source is a restricted physical-controller emulator, **not** a compiled arbitrary-machine TM interpreter. Finite results are COMPUTATIONAL, not an asymptotic proof.

No full repository checkout/preflight, LaTeX compilation or generic all-machine compiler was executed. The symbolic proof is separate from the tests.

## 6. Dependencies, literature and exact remaining gap

Original peer artifacts read: TMR-4/019 inductive mirror report; TMR-5/016 independent fixed-offset report and its original source/raw data; TMR-4/018 original work-symbol congruence report; current peer TMR-3/018 delayed-query restriction; and earlier historical checker-alias discussion. Historical LSPV accepted order aliases are **genuine accepted executions** in their own checker model; no such path is silently discarded here. Original TMR-5/016's fixed-offset method is independently supported under its hypotheses. The present many-to-one theorem awaits peer review.

Primary references inspected for *abstract interpretation and counterexample replay methodology*, not used as a black-box complexity lower bound:

1. P. Cousot and R. Cousot, "Abstract interpretation: a unified lattice model for static analysis of programs by construction or approximation of fixpoints," POPL 1977, pp. 238-252, https://doi.org/10.1145/512950.512973.
2. E. M. Clarke, O. Grumberg, S. Jha, Y. Lu, H. Veith, "Counterexample-Guided Abstraction Refinement," CAV 2000, pp. 154-169, https://doi.org/10.1007/10722167_15.

Arbitrary polynomial workspace, full-source caching, adaptive rereading, compact GF(2) elimination, Horn/2-SAT, treewidth DP, products, sharing, reencoding, auxiliary variables and recomputation remain fully admissible. All these possible representations are accounted for as ordinary concrete machine work by the general simulation theorem, but were **not** experimentally executed as independent full SAT machines. Exact factor erasure on some programs entails **no** noncircular superpolynomial lower-bound potential on every correct uniform 3-SAT decider. No polynomial-time exponent is excluded.

The team target remains OPEN: for each correct fixed finite uniform total 3-SAT machine A, every integer k>=1, every C>0 and every L0, find a valid F with |F|>=L0 and T_A(F)>C(|F|+1)^k. Same-machine S<=O(T) is permitted; no separate-machine bound is borrowed.

**Corpus readback:** 12:49 PST role replacement directive read first and rechecked, SHA 47459817e66dccf1f3079e6c724c0fd2643e7bc4. Full root proof1.txt (28,714 chars; SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343) and proof2.txt (1,051,196 chars via authentic Git blob SHA 930c5eeddafce656717f28055a7a9a755f44737c), full root main.tex (2,533,636 chars, blob SHA 867c9b7512a51d59a50c479e81dda6c65615026f), AGENTS.md, CODEX.md, pnp research skill, all five handoffs and current issue #3. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** Canonical main.tex unchanged pending TMR-5 whole-document synthesis. No scheduled task was created, revived or modified.

**ONE NEXT TARGET:** TMR-5 independently check the strictly noninjective factor's finite certificate, dummy-tape physical charges and dynamic-offset failure; then investigate a genuine nonlocal, fully charged data-reencoding invariant, without presuming arbitrary machines maintain any one encoding.

END_OF_REPORT::TMR-4::020::2026-11-14_0538_PST
