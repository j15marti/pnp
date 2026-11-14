# TMR-4/021: Independently moving work heads with fixed cellwise factor, a cost-exact abstract quotient

**Time:** November 14, 2026, 06:37 PST (America/Los_Angeles). **Role:** TMR-4, Cost-Sound Abstraction. **Status:** NEW CANDIDATE/RESTRICTED mathematical theorem pending TMR-5/TMR-1 audit; executed V8 evidence COMPUTATIONAL; unrestricted 3-SAT superpolynomial bound OPEN.

## 1. Novel result and precise distinction

TMR-4/020 established an exact redundant-tape quotient for a **fixed cellwise displacement** $d$ and equal movements of two physical writable heads. Its minimal counterexample correctly refuted the *different* assertion that the data correspondence can be shifted merely when one head moves. This report strictly relaxes **equal head movement**, while keeping the **cellwise data correspondence fixed**. Independent head motion is permitted, including C-only changes invisible under a many-to-one factor, provided an effective finite certificate proves that divergent-head writes preserve the factor.

The distinction is:

- **Fixed content relation:** $B[j]=f(C[j+d])$ for every cell $j$, with a constant $d$.
- **Variable head separation:** $\delta=h_C-h_B-d$ may change within a fixed finite set $D$ tracked in control. It is **not** substituted for $d$.
- **No free random access:** in divergent-head states, the source program must not branch on B's scanned symbol. An actual one-step physical simulator uses only C's physically scanned symbol, not arbitrary C cells.

A two-phase finite certificate suffices. This extension admits certified programs rejected by TMR-4/020's equal-motion criterion. It does **not** assert that arbitrary SAT deciders have the certificate.

## 2. Exact machine and certificate DHF21

Fix **one** finite, total deterministic multitape machine $A$ for all binary source lengths, with ordinary locally moving read-only source heads and finite alphabets. It may possess any additional writable tapes, including input caches, algebraic encodings, indexes and stacks. Designate writable tapes B and C with alphabets $\Gamma_B,\Gamma_C$, blanks $\sqcup_B,\sqcup_C$, and a **fixed** finite blank-preserving map $f:\Gamma_C\to\Gamma_B$. The map need not be injective. Fix a constant integer cell displacement $d$; it is not an input-dependent address or an oracle.

Within an explicitly certified control region, control also stores $\delta$ from a fixed finite set $D$ and the following relation holds:

$$
I(c):\quad B[j]=f(C[j+d])\ \text{for all }j,\qquad
\delta=h_C-h_B-d\in D.
$$

Initial binding is the standard blank-tape configuration (when $d=0$), or a separately **charged and replayed** prefix establishing $I$. Preserve the original input, all input-head positions, finite control, every other tape, both B and C physical head positions, and their **visited writable-cell sets**.

Certify for **every** control state in the region, **every** source-symbol/other-tape scanned tuple, and **every** eligible current B,C scanned tuple:

1. The next control label and signed head movements are actual finite-table instructions. The next tracked $\delta'=\delta+m_C-m_B$ belongs to $D$, and the control's $\delta'$ field agrees. Terminal SAT, UNSAT and MALFORMED labels are retained exactly.
2. **Aligned correspondence ($\delta=0$):** the scanned values obey $b=f(c)$, and the actual written values obey $w_B=f(w_C)$. The two physical heads may move differently afterward.
3. **Divergent heads ($\delta\ne0$):** for every possible $b\in\operatorname{im}(f)$, the transition's state, source actions, all other tape actions, C write, and both head movements are **independent of b**; B writes its *unchanged scanned symbol* $w_B=b$; and C's write lies in the same factor fiber, $f(w_C)=f(c)$. Thus the two physical writes cannot change the corresponding cellwise B values.
4. All source-head movement, original input-cell observation, and extra writable-tape operations are reproduced literally with the same single unit transition charge.

These are **sufficient**, decidable finite-table checks for one specified A, $d$, $f$, region and $D$. They deliberately reject some semantically correct machines. One may use tighter inductive guards only with a separate proved all-transition invariant.

**Theorem DHF21 (candidate, restricted).** If the initial binding and this certificate hold, there is a **physically implementable** finite multitape quotient $\widehat A$ which stores C normally but replaces B's symbols with a permanently blank **dummy physical tape**, retaining B's head movements and visited-cell footprint, such that for every input $x$ and every reachable concrete transition $c\to c'$ of cost one there is one abstract transition $a\to a'$ of cost one with $c\,I\,a$, $c'\,I\,a'$, and conversely every related abstract step replays the same concrete step. All three terminal labels and the exact input are preserved. On the same source and same execution,

$$
T_{\widehat A}(x)=T_A(x),\qquad S_{\widehat A}(x)=S_A(x).
$$

**Proof:** For $\delta=0$ the original B scanned value is reconstructed from the **actually scanned** C symbol by $f$, and the paired writes maintain $I$ at their common corresponding index. At $\delta\ne0$, the B head scans a cell distinct from C's corresponding index; the certified transition is B-blind, leaves its B cell unchanged, and changes the C cell only inside its $f$-fiber. Hence $I$ is unchanged at **both distinct corresponding indices** and everywhere else. The checked head movements update only $\delta$, not $d$. All other actions and terminal labels are identical. In the projected machine a dummy B head makes exactly the same physical movement, writing blank; it visits the same writable cells. At $\delta=0$ its control reads the physically scanned C symbol and uses $f(c)$; at $\delta\ne0$ the transition is independent of the missing B symbol. Thus the projected transition table is finite and **requires no extra C-head repositioning**, giving one-to-one cost-one simulation. Invariant induction covers all reachable source-bound transitions; reverse replay is unique on related states. Therefore abstract minimum decision-path cost is at most the concrete time and the paired concrete/abstract traces have equal time and space.

**Gap:** If B's scanned symbol is needed when $\delta\ne0$, merely reading $C[h_B+d]$ from a mathematical description is *not* a one-transition physical computation. Such a proposed physical compiler requires charged repositioning or more retained information. DHF21 avoids that hidden nonlocal read by a stringent B-blind certificate.

## 3. Concrete all-length controller, both labels and exact cost potential

Use $d=0$, $D=\{0,1\}$, $\Gamma_C=\{0,1,2,3\}$, $\Gamma_B=\{0,1\}$, and $f(c)=c\bmod2$. Both initial tapes and heads are blank at cell zero. For every binary source $x$ of length $L$, a finite-control sign-stream 3-CNF grammar groups its bits into clauses of three sign bits on the three fixed variables. Every signature excludes precisely one of the eight assignments. An eight-bit **finite-control** mask tracks excluded assignments. If $L$ is positive and divisible by three, output UNSAT iff all eight signatures occur; otherwise output SAT. Nonmultiples of three and the empty source output MALFORMED. This is a total correct decider for its fixed-three-variable grammar, **not** for general 3-CNF.

Before parsing, one source scan maintains the counter C[0] modulo four and its B[0] parity. A seven-instruction finite-control sequence does the following:

| Step | Original B-head / C-head action | Resulting $\delta$ | Writable content action |
|---|---|---:|---|
| R0 | C right; B stays | 1 | unchanged |
| R1 | both heads stay | 1 | C[1]: 0 to 2, $f$ unchanged |
| R2 | C left; B stays | 0 | unchanged |
| R3 | both right | 0 | unchanged |
| R4 | B left; C stays | 1 | unchanged |
| R5 | B right; C stays | 0 | unchanged |
| R6 | both left | 0 | unchanged |

Only R1 performs a divergent-head write and it is a factor-kernel update. R0/R2/R4/R5 have unequal physical head movements. The gate then uses B[0] (the quotient uses *physically scanned* C[0] parity) to trigger an additional physically charged $2(L+1)$-step input roundtrip for odd source parity. An ordinary input return and source parser follow; both labels are produced from the finite mask and original source.

Let $z(x)$ be source parity and $p$ the actual source-head coordinate, ranging from -1 to $L$. Exact charged runtime and peak visited writable space are

$$
T(x)=3L+13+2(L+1)z(x),\qquad S(x)=4.
$$

For the **source-fixed, inductively certified reachable abstract graph**, define the following explicit noncircular potential with $G=2L+4+2(L+1)z(x)$ and $i\in\{0,\ldots,6\}$:

$$
\begin{aligned}
\Phi(\mathrm{SCAN},p)&=L-p+1+7+G,\\
\Phi(R_i)&=7-i+G,\qquad \Phi(\mathrm{GATE})=G,\\
\Phi(\mathrm{DL},p)&=p+3L+5,\\
\Phi(\mathrm{DR},p)&=3L-p+3,\\
\Phi(\mathrm{RETURN},p)&=L+p+3,\\
\Phi(\mathrm{PARSE},p)&=L-p+1,\qquad \Phi(\mathrm{HALT})=0.
\end{aligned}
$$

Every **actual abstract edge** in this closed source-bound controller graph has unit cost and satisfies $\Phi(a)=1+\Phi(b)$, including all divergent-head and kernel-write steps, the source gate, both detour options, the source parser and the terminal step. Therefore the required Bellman inequality $\Phi(a)\le \mathrm{cost}(a,b)+\Phi(b)$ holds on **EVERY edge of this graph** and $\Phi(\mathrm{HALT})=0$. The initial value equals the explicit **linear** runtime above. Although $\Phi$ references the fixed source parity, it is a mathematical analysis potential, **not** an oracle operation supplied to the controller. No superpolynomial source-independent lower-bound potential is claimed.

## 4. Hostile falsifiers and repairs

**TMR-4/020 moving-data-offset failure remains genuine.** After B[0]=C[0]=1, moving C's head to 1 does NOT change B[0]=f(C[0]); replacing $d=0$ by $d'=1$ would wrongly use C[1]=0. Our $\delta=1$ changes only the head-separation control field, keeping $d=0$ and all tape contents stationary.

**Non-kernel divergent write fails.** With B[1]=C[1]=0, a divergent transition writing C[1]=1 but not B[1] violates $B[1]=f(C[1])$. This cheap abstract shortcut must not be removed as spurious unless a true initial/all-step invariant excludes it. DHF21 rejects the transition.

**Off-invariant gate:** B[0]=1 and C[0]=0 give different gate decisions; a raw MAY quotient erasing B without an entry certificate is unsound. The real certified controller never reaches this pair. Historical accepted R_mix341 checker-alias executions remain genuine under their historical checker and are not silently discarded.

**Representation controls:** Horn, 2-SAT, affine/GF(2), bounded-treewidth DP, disjoint products, auxiliary encodings, renaming, input rereads, caching, shared computation and recomputation are all admissible in the source machine. DHF21 says nothing about their compulsory cost, and tests exercised only the restricted three-variable sign-stream controller. It does not exclude a correct general polynomial-time SAT machine. For any arbitrary program lacking this optional tape relation, the no-erasure identity abstraction remains cost-sound but supplies no nontrivial SAT lower bound.

## 5. Actual executed evidence, source and status

**Direct hosted V8 execution**, not native Node, independently coded as a new source implementation rather than a wrapper around TMR-4/020:

- 2,068 paired concrete/abstract complete traces, including all binary sources of lengths 0 through 10 and 21 longer controls.
- 104,525 concrete transitions, 104,525 abstract transitions and 104,525 checked Bellman equalities.
- Terminal outcomes: 604 SAT, 1 UNSAT, 1,463 MALFORMED; ZERO assertion failures.
- 16 aligned factor-pair checks, eight divergent factor-kernel checks; one each of dynamic-offset, non-kernel and off-invariant hostile counterexamples.
- Both physical work-tape visited-cell footprints preserved, peak $S=4$; runtime checksum 1,002,972.

Executable: [experiments/tmr/tmr4_divergent_head_factor021.cjs](../../../experiments/tmr/tmr4_divergent_head_factor021.cjs). Immutable raw: [results/raw/tmr/2026-11-14_0635_TMR4_DIVERGENT_FACTOR021_RAW.json](../../../results/raw/tmr/2026-11-14_0635_TMR4_DIVERGENT_FACTOR021_RAW.json). The checked executable explicitly follows the current physical read-only source cell; its host representation is an instrumented emulator, **not** a generated full Turing-machine instruction compiler. Finite tests are COMPUTATIONAL. The general theorem is symbolic and awaits independent TMR-5/TMR-1 review.

## 6. Provenance, literature, dependencies and precise remaining obligation

Original peer material recovered: TMR-4/020 report, executable and raw; TMR-5/016 fixed-offset independent review; TMR-4/019 mirror invariant and its off-diagonal gate; current issue #3 and current five handoffs. Historical checker accepted-alias counterexamples were retained in proof2 and prior handoffs. Full root proof1.txt, authentic full Git-blob proof2.txt, authentic full Git-blob root main.tex, AGENTS.md, CODEX.md and the repo pnp research skill were read. The 2026-11-13 12:49 PST replacement directive supersedes old role assignments. Current directive SHA: 47459817e66dccf1f3079e6c724c0fd2643e7bc4.

Primary methodological references inspected, neither imported as a computational hardness theorem:

1. P. Cousot and R. Cousot, "Abstract interpretation: a unified lattice model for static analysis of programs by construction or approximation of fixpoints," POPL 1977, pp. 238-252, https://www.di.ens.fr/~cousot/COUSOTpapers/POPL77.shtml.
2. E. M. Clarke, O. Grumberg, S. Jha, Y. Lu and H. Veith, "Counterexample-Guided Abstraction Refinement," CAV 2000, pp. 154-169, https://doi.org/10.1007/10722167_15.
3. M. Colón, S. Sankaranarayanan and H. Sipma, "Linear Invariant Generation using Non-linear Constraint Solving," CAV 2003, pp. 420-433, https://theory.stanford.edu/~sipma/papers/cav03.html.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Proof1 remains OPEN for a general polynomial SAT algorithm; proof2 remains OPEN for an unrestricted superpolynomial time lower bound. The target requires one fixed correct total uniform machine A for all lengths, with hard F dependent on A, k, C and L0, and *all* polynomial time exponents excluded. This new optional, small finite-state invariant cannot establish such a bound. No root main.tex edit or task mutation.

**ONE NEXT TARGET:** TMR-5 independently inspect the finite divergent-state B-blind certificate, physical dummy-tape implementation and the symbolic all-edge Bellman formula. Then seek a fully charged relation permitting B-dependent reads during independent-head divergence, or produce its minimal locality/time-overhead obstruction, without assuming any generic SAT solver representation.

END_OF_REPORT::TMR-4::021::2026-11-14_0637_PST
