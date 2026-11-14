# TMR-4/022: physically charged two-cell factor cache with moving erased head

**Date:** 2026-11-14 07:36 PST, America/Los_Angeles. **Role:** NEW TMR-4, cost-sound abstraction, j15marti/pnp/main. **Status:** BCC22 CANDIDATE/RESTRICTED pending independent TMR-5 review; finite results COMPUTATIONAL. The unrestricted 3-SAT superpolynomial lower bound remains OPEN.

## New theorem and a genuine failure of one-register erasure

TMR-4/021 gives an exact redundant-tape factor quotient when the erased B head and retained C head diverge, but B is not read while separated. TMR-5/018 permits B-dependent divergence when B stays at one cell whose value was previously copied into finite control. Here the erased B head **moves from one authenticated cell to another**, while C remains at a different location, and the original machine branches on both B values. A finite independently authenticated cache for **each** such cell enables a one-transition-per-transition physical quotient. Reusing only the first cached register at the second cell is UNSOUND and produces an actual cheap abstract execution that is not a replay of the specified source machine.

**BCC22 certificate, exact restricted form.** Fix a single total deterministic finite multitape source program A across all encoded input bit lengths L; use a read-only locally moving source head, finite alphabets and ordinary writable work heads. Designate tapes B,C and a constant integer content displacement d with a fixed blank-preserving finite map f from C symbols to B symbols. Assume the following **finite-state certified** premises on every reachable transition:

1. Initially B[j]=f(C[j+d]) for every cell j, or a separately charged actual prefix establishes this relation. The source, control, every other tape, heads, and visited-cell ledger are related faithfully.
2. A fixed finite set K of B positions, relative to an explicitly tracked finite anchor, has a separate finite-control register R_i. Its value equals B[k_i]=f(C[k_i+d]), established only by an actual charged aligned physical observation/write, not a free prefetch. Every later factor-changing write at that position must update R_i through an equally charged physically available operation. No arbitrary absolute coordinates or unbounded address table are free.
3. At aligned heads, B's scanned value is reconstructed from C's **actually scanned** symbol, and paired writes obey w_B=f(w_C). At divergent heads, B writes its scanned symbol unchanged and any C write preserves its f-fiber. A B-dependent branch while divergent is permitted **only** where B's currently scanned cell has an authenticated R_i; uncached scans must be B-blind. Finite control tracks every authorized head-location index and legal relative movement. These checks apply to every eligible input/other-tape symbol and B/C symbol tuple, not only selected experimental traces.
4. Every real source read, work-tape instruction, movement, temporary representation and terminal label is reproduced. The quotient has a **physical blank dummy B tape** whose head performs the actual B movement and whose visited cells count as writable space. C's head remains physical. Finite caches are program-constant control; a variable-sized cache must instead be charged explicitly.

**Theorem (candidate, restricted).** The certified projection Ahat erases B symbol contents while maintaining C, the dummy B tape and authenticated finite cache. Relate concrete c and abstract a by the whole-tape factor, faithful source/other tapes/control/heads/visited cells and valid cache. Initial states are related. For **every** related legal concrete unit step c to c', there exists exactly one abstract physical unit step a to a' with related successors. Conversely every related abstract step reconstructs the same concrete action. SAT, UNSAT and MALFORMED terminals coincide. Induction gives complete source-bound execution inclusion and, in the exact quotient,

$$
\min_{\pi:\,a_0\leadsto\mathrm{goal}}\operatorname{cost}(\pi)\le T_A(x),\qquad
T_{\widehat A}(x)=T_A(x),\qquad S_{\widehat A}(x)=S_A(x).
$$

**Proof:** An aligned step reads f of the currently scanned C symbol and preserves the whole-tape factor by its paired-write certificate. A divergent B scan of an authenticated position uses R_i, with no C-head teleport or remote read. Such a step leaves B unchanged, preserves f on every changed C cell, and keeps authentic registers unchanged, or uses a separately certified physically co-scanned update. Actual B movements merely change the finite authenticated index. All other source/work transitions and charged physical head visits are copied. This gives a successor-preserving induction and reverse replay. The proof relation may quantify over remote C cells, but the executable transition function cannot read them.

**Coverage gap:** An arbitrary correct uniform 3-SAT decider need not maintain a fixed f relation or restrict its B head to a finite known set; it can reread sources, use unbounded polynomial workspace, changing encodings, sharing, compact GF(2), Horn/2-SAT algorithms, bounded-treewidth DP, padding, products, auxiliary variables and recomputation. The universal identity abstraction is sound but gives no new hardness. No polynomial-time SAT decider is excluded by BCC22.

## Concrete source-bound physical controller, all three terminal labels

The test language is E3, a proper 3-variable sign-stream 3-CNF encoding: every triple of bits excludes exactly one assignment to three fixed variables. A finite eight-bit exclusion mask solves **all** legal E3 inputs by checking whether all eight signatures occur. Empty or non-multiple-of-three strings are MALFORMED. This is not an unrestricted 3-SAT decider.

Set B alphabet {0,1}, C alphabet {0,1,2,3}, f(c)=c mod 2 and d=0. Begin with both work heads at 0 and the source head at the left marker. An actual paid source scan stores B[0]=p, C[0]=number of ones modulo four, and first source bit b in finite control, while building the SAT signature mask. At the right source marker: SETUP0 authenticates R0=p with both heads aligned on cell 0 and moves both to cell 1. SETUP1 writes B[1]=C[1]=b, authenticates R1=b, and physically moves B to 0 and C to 2. REMOTE0 branches on B[0] and optionally spends one actual idle transition when p=1. MOVE1 moves the **erased head B from 0 to 1** while C stays at 2. REMOTE1 branches on B[1] and writes C[2]=(C[2]+2) mod 4 (all-symbol factor-kernel write). If b=1 it then pays an entire locally moving input-head left/right excursion. FINAL emits the mask-derived SAT, UNSAT or MALFORMED label.

The quotient reads R0 at REMOTE0 and the **different R1** at REMOTE1. The dummy B head physically visits cells 0,1, and C visits cells 0,1,2. Thus same-source peak visited writable cells are exactly S(x)=5, with all index and mask state contained in fixed finite control. For encoded source length L, parity p(x), and first bit b(x) (zero if empty), the precise charged runtime is

$$
T(x)=L+8+p(x)+(2L+3)b(x).
$$

An invalid quotient using R0 again at REMOTE1 sees source x=110, a valid SAT E3 word with B0=0 and B1=1. It skips a real detour, yielding 11 steps rather than the concrete 20. On x=010 the incorrect quotient adds nine fictitious transitions, yielding 21 versus concrete 12. These are exact failures of **same-program** cost simulation. They are not lower bounds for all E3 algorithms: the deliberate detour is unnecessary for deciding E3.

## Explicit all-edge Bellman potential

Let n=L+1 and h be the current physical source head coordinate, with markers at 0 and n. For fixed source x define p and b as above. On the **entire reachable abstract edge graph for that exact source**, set

$$
\begin{aligned}
\Phi(\mathrm{SCAN},h)&=n-h+7+p+b(2n+1),\\
\Phi(\mathrm{SETUP0})&=6+p+b(2n+1),\\
\Phi(\mathrm{SETUP1})&=5+p+b(2n+1),\\
\Phi(\mathrm{REMOTE0})&=4+p+b(2n+1),\\
\Phi(\mathrm{EXTRA0})&=4+b(2n+1),\\
\Phi(\mathrm{MOVE1})&=3+b(2n+1),\\
\Phi(\mathrm{REMOTE1})&=2+b(2n+1),\\
\Phi(\mathrm{DL},h)&=h+n+2,\\
\Phi(\mathrm{DR},h)&=n-h+2,\\
\Phi(\mathrm{FINAL})&=1,\quad \Phi(\mathrm{HALT})=0.
\end{aligned}
$$

Every actual abstract unit transition, including initial source reads, both B-dependent divergent branches, all detour movements, all C writes and the final terminal action, obeys **Phi(a)=1+Phi(a')**. Hence Phi(a)<=cost(a,a')+Phi(a') on **every** abstract edge and Phi(goal)=0. Phi(start)=T(x) is only **linear in L**. Parity and first bit are analysis parameters of the already fixed immutable source, not freely supplied runtime oracles. No superpolynomial initial potential exists in this construction.

## Exact executed evidence and caveats

Actually executed standalone source in **hosted V8** (not native Node), independently authored rather than wrapping TMR-5/018. All 0..12-bit words plus twelve additional longer/hostile inputs gave 8,203 concrete/quotient paired traces, 263,410 charged concrete and abstract transitions each, 263,410 per-edge Bellman equalities, 4,687 SAT / 4 UNSAT / 3,512 MALFORMED, 4,101 cases with different cached B0 and B1, 16 executable factor/register alphabet checks, and ZERO failed assertions. Truth labels were independently checked against all eight assignments; whole-tape factor, both cache authentications, head footprints and time formulas were tested. Five executed naive single-register tests showed omission/addition of physical work. Stale-register, non-fiber-write and fabricated zero-cost terminal edges are **symbolically specified hostile controls** in raw JSON, NOT separately executed tampered-machine runs. No arbitrary-TM compiler, LaTeX compilation, OS Node or repository preflight ran. All finite tests are COMPUTATIONAL.

Published exact executable: experiments/tmr/tmr4_two_cell_cached_factor022.cjs, readback blob dba47177d9685a1b63c92441f1cf910b7fad1d4e.
Published raw: results/raw/tmr/2026-11-14_0736_TMR4_TWO_CELL_CACHE022_RAW.json, readback blob 763dfa742cd230123b837224b7101e9bd30673e8.

## Research corpus, literature, integrity and remaining obligation

Read first and rechecked superseding five-TMR directive (SHA 47459817e66dccf1f3079e6c724c0fd2643e7bc4). Fully read proof1.txt (28,714 characters, blob 06f7ebc8c2283304a0f5200b518c6e48fa41e343) and recovered authentic full proof2.txt (1,051,196 characters, blob 930c5eeddafce656717f28055a7a9a755f44737c) because the contents endpoint returned a misleading blank body. Read full canonical main.tex (2,539,489 characters, blob f80790efd768574555a85703a14820e1bed56b70), AGENTS.md, CODEX.md, repo pnp-research skill, issue #3, current five TMR handoffs and original TMR-4/021, TMR-5/018 reports and evidence. Recovered historical ORIGINAL LSPV-5/511 support-string accepted checker artifact and LSPV-5/481 mixed invalid-UTF8 normalizer counterexample. Genuine earlier checker accepts remain genuine, not erased as spurious.

Primary literature checked directly: [1] Cousot and Cousot, *Abstract Interpretation*, POPL 1977, pp. 238-252, https://www.di.ens.fr/~cousot/COUSOTpapers/POPL77.shtml ; [2] Clarke et al., *Counterexample-Guided Abstraction Refinement*, CAV 2000, pp. 154-169, https://doi.org/10.1007/10722167_15 ; [3] Fortnow, Lipton, van Melkebeek and Viglas, *Time-Space Lower Bounds for Satisfiability*, JACM 52(6), 835-865 (2005), https://doi.org/10.1145/1101821.1101822. None supplies an arbitrary polynomial-time SAT lower bound.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Neither proof tracker was edited. Root main.tex remains under TMR-5 synthesis, unchanged here. No schedule/task modifications.

**Next:** TMR-5 independently audit the two-cell moving-B cache, all-transition induction, true paid cache acquisition and Bellman potential. Test whether a physically moving B head can safely update cached entries while C remains remote without secretly changing an unscanned C cell. Any transfer to unrestricted arbitrary-machine 3-SAT and all polynomial exponents remains **OPEN**. P versus NP **OPEN**.

END_OF_REPORT::TMR4::022::2026-11-14_0736_PST
