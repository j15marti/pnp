# TMR-4/017: undecidable all-input exactness of a one-bit cost abstraction

**Pacific time:** 2026-11-14 02:36 PST. **New claim:** CANDIDATE/RESTRICTED pending independent TMR-1/TMR-5 review. **Executed tests:** COMPUTATIONAL. **Unrestricted P versus NP:** OPEN.

## Exact theorem and model

Fix any one ordinary total, correct, uniform deterministic multitape 3-SAT decider A with one locally moving, read-only input head (endmarkers at 0 and L+1), fixed finite control/alphabet and an explicit SAT/UNSAT/MALFORMED output convention. Its runtime is not assumed polynomial. For any deterministic single-tape machine M on a blank tape, effectively construct two *fixed all-length* total correct SAT machines P_M and Q_M, the latter differing only in replacing a marked one-bit finite-control gate test with SKIP. Both preserve the output label of A on every binary source. They have identical executions, work contents, physical input locations and paid costs until that gate.

Let H_M(L) indicate that M halts within its first L steps, including step zero. Let b(x) be XOR parity of source bits. Then

$$
T_{P_M}(x)-T_{Q_M}(x)=2(L+1)\,H_M(L)\,b(x).
$$

This is **same-source, charged physical time**, not a combination of unrelated worst-case witnesses. The all-input property

$$
\mathsf{EXACT\_ERASE}(P_M)
\ \Longleftrightarrow\
\forall x\in\{0,1\}^*\quad
T_{P_M}(x)=T_{Q_M}(x)
\ \Longleftrightarrow\
M\text{ never halts}
$$

is therefore undecidable even on this syntactically recognizable family of promised-total, correct SAT machines. No total effective analyzer can be simultaneously sound and complete for this precise all-input exact-erasure property. This is **not** an impossibility theorem for sound incomplete MAY abstractions or for exact identity abstractions, and says nothing about a superpolynomial SAT lower bound.

## Complete reduction

Run A on the actual immutable input, retaining its true SAT/UNSAT/MALFORMED label in finite control instead of entering a final halting state. The transition that would halt A can enter this new phase at the same cost. Physically restore A's source head to the left marker, paying one transition per movement. Sweep from marker 0 to marker L+1 and back, computing b using **current-cell** source reads only at 1 through L. This takes 2(L+1) moves.

Make a second physical outward-and-return sweep of 2(L+1) moves to clock the bounded M simulation. Move from left marker to first source cell (one move), then on each of L source-data-cell-to-right transitions perform one M step on its own initially blank *ordinary writable work tape*. Simulating M is a finite-control product with the original source-head movement; each of M's work-head movements, reads and writes uses the same one legal multitape transition. If M has halted, retain flag h and move the source head as before without further M steps. At right marker return L+1 moves to left marker. For L=0 the simulation executes no M steps. Thus the common gate has h=H_M(L) and b=b(x), with the input head at zero and all temporary computation paid. The wrapper has one more fixed tape than A and finite fixed control compiled from M, irrespective of input length. In the bounded simulation M visits at most O(L) work cells, all charged.

At the gate P_M performs one additional genuine full source-head roundtrip of precisely 2(L+1) transitions iff h=b=1; Q_M always skips. Both then produce the same already-computed label in one paid step. They are total because A is total and M runs for at most L steps. No oracle, advice, indexed free source access, unbounded-word operation, automatic proof search, length-dependent machine choice, or conditional complexity hypothesis is involved.

If M never halts, h remains zero and the runtimes are equal on every source. If M halts after t steps, select any L>=max(1,t) and binary x=10^{L-1}; then h=b=1 and there is an actual positive paid difference of 2(L+1). A decision procedure for the all-input exact-erasure property would decide whether M halts, contradicting classical halting undecidability. The witness x can be malformed, but both machines still classify it correctly. On the separate fixed-three-variable clause-sign grammar below, genuinely valid SAT and UNSAT inputs of arbitrarily large size and odd parity also trigger the gap; no universal statement about every possible 3-CNF byte encoding is inferred.

The reduction is stronger than TMR-4/016's one-roundtrip example and TMR-1/016's fixed-polynomial amplification in one orthogonal sense: **deciding whether the same marked-bit erasure is globally exact is algorithmically undecidable even though every machine in the family is total and correct.** It does not claim that every possible abstraction must erase the bit.

## All-transition MAY abstraction and exact gap

Fix full source x, fixed program P_M, and full machine configurations, including A's and M's work-tape contents, all work heads, input head and immutable source, saved label, phase and h. Abstract by dropping *only* finite-control parity bit b, retaining x and every other register. Include both syntactically legal gate successors when h=1. Every concrete unit transition projects to an abstract unit edge, or to a zero-cost gate bookkeeping edge plus a paid unit transition. The initial configuration is related, both terminal classifications are preserved, and **every concrete step**, not merely selected proof operations, has a matching abstract path with total cost no greater than one. Hence every real trace appears and

$$
d_{\rm MAY}(a_0,G)\le T_{P_M}(x).
$$

If M halts and b=1 on x, the quotient's cheap SKIP branch is replay-spurious against that *same* source's reached gate state and omits exactly 2(L+1) real transitions. Retaining b through the gate repairs this particular quotient. If M never halts, h=0 on every reachable gate and the quotient has exact initial-to-terminal cost on every x. The abstract syntax is a conservative MAY model of **all syntactically legal states**, not a free source-specific oracle characterizing exact reachability.

For the restricted three-variable 3-CNF sign-stream classifier, the true erased trace length is 4q+1, q=L+1, with stages F (first outward), R (first return), MF (bounded clock outward), MR (bounded clock return), gate G, optional extra scan D, output O and HALT. An explicit potential on its MAY graph is

$$
\Phi(F,p)=4q-p+1,\quad \Phi(R,p)=p+2q+1,
$$

$$
\Phi(MF,p)=2q-p+1,\quad \Phi(MR,p)=p+1,
$$

and Phi(G)=Phi(D)=Phi(O)=1, Phi(HALT)=0. Both gate choices are zero-cost bookkeeping edges and have potential 1 at either end. Every source movement has abstract cost one. Substitution at every outward, return, gate, detour and terminal edge verifies

$$
\Phi(u)\le c(u,v)+\Phi(v),\qquad \Phi(HALT)=0.
$$

Thus Phi(F,0)=4q+1 is a valid lower bound on physical time and equals shortest MAY goal-path cost. On h=b=1 sources the real trace costs 6q+1, leaving a **precisely 2q-step abstraction gap**. A valid Bellman potential can be incomplete without ever being unsound. No superpolynomial potential for arbitrary A has been derived.

## Original independently executed controls

**Directly executed hosted V8:** the self-contained published source was executed at its function level and then serialized unchanged into a Node-compatible standalone file. **Independently written native CPython:** separate local physical trace program and brute-force label checker (not a wrapper around V8) were run. Both used six fixed finite-state M fixtures (never halt, halt at 0,1,3,7,11) on **all 4,095 binary strings of lengths 0 through 11**, producing identical ledgers:

| Check | V8 | Native Python |
|---|---:|---:|
| Source/program pairs | 24,570 | 24,570 |
| Charged physical transitions, actual plus erased | 2,415,892 | 2,415,892 |
| Genuine extra roundtrips | 9,146 | 9,146 |
| Extra paid transitions lost by erasure | 204,016 | 204,016 |
| Assertion failures | 0 | 0 |

The restricted sign-stream accepts any number of clauses over exactly three variables, one 3-bit sign mask per clause, and is a **regular language, not NP-complete general 3-SAT**. Rows 0 through 7 encode a genuine UNSAT input, rows 0 through 6 plus a duplicate 6 encode SAT, and adding a duplicate row with odd parity supplies valid label-preserving controls. Explicit valid controls include length-24 SAT with odd parity and length-27 UNSAT with odd parity, both showing the correct 2q time gap. Exhaustive short strings include no UNSAT because eight distinct sign masks require 24 source bits. All physical source reads occurred at their current data cells, not at the left marker, correcting the finite-model issue discovered in TMR-5/013.

The finite mock-M experiments do **not** implement a universal instruction-table simulator for arbitrary M, and do not prove the asymptotic theorem by enumeration. The reduction above supplies that mathematical argument. Actual OS Node replay and LaTeX compilation were **not run**. Independent Python remains local-only; the published V8 source and raw V8 results are reproducible. Separate Horn, 2-SAT, arbitrary GF(2)/Gaussian, bounded treewidth, product, renaming and auxiliary-variable controls were not physically executed this run. The theorem's base A remains completely unrestricted so those algorithms are not excluded by assumption.

**Published exact paths:** experiments/tmr/tmr4_gate_erasure017.cjs; results/raw/tmr/2026-11-14_0236_TMR4_GATE_ERASURE017_RAW.json; research/agents/tmr-4/2026-11-14_0236_TMR4_UNDECIDABLE_COST_EXACT_ERASURE017.md.

## Primary sources, repository corpus and unresolved obligations

* Turing, A. M. (1936/37), *On Computable Numbers, with an Application to the Entscheidungsproblem*, Proceedings of the London Mathematical Society, DOI https://doi.org/10.1112/plms/s2-42.1.230. Halting undecidability is the only external mathematical input; this exact wrapper reduction is newly supplied here.
* Cousot, P. and Cousot, R. (1977), *Abstract Interpretation: A Unified Lattice Model for Static Analysis of Programs by Construction or Approximation of Fixpoints*, POPL, pp. 238-252, DOI https://doi.org/10.1145/512950.512973, author bibliography https://pcousot.github.io/publications.html. Its conservative-abstraction ideas are not a 3-SAT lower bound.
* Clarke, E., Grumberg, O., Jha, S., Lu, Y., Veith, H. (2000), *Counterexample-Guided Abstraction Refinement*, CAV 2000, pp. 154-169, DOI https://doi.org/10.1007/10722167_15. Replay-spurious paths motivate refinement but do not supply a free exact reachability oracle.
* Original TMR-4/016 parity quotient, original TMR-5/013 off-head-read audit, original TMR-1/016 paid one-head counters and original TMR-2/016 source-aware checkpoint theorem were read. Historical original LSPV-5/523 (research/agents/lspv-5/2026-11-13_0210_LSPV5_NATIVE341_ACCEPTED_ORDER_ALIAS523.tex) supplies an unchanged-checker-accepted literal-order alias with a genuine changed probe cost, which cannot be discarded as a spurious path. Its OS checker was **not rerun** here.

The authoritative 2026-11-13 12:49 PST TMR replacement directive on main was read **first and rechecked** (SHA 47459817e66dccf1f3079e6c724c0fd2643e7bc4). Root proof1.txt read completely (28,714 chars, SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343); root proof2.txt recovered fully from authentic Git blob despite blank fetch_file (1,051,196 chars, SHA 930c5eeddafce656717f28055a7a9a755f44737c). Root canonical main.tex recovered fully by Git blob (2,525,134 chars, SHA d3db01d221df39f096f31237643268132edfcd87). AGENTS.md, CODEX.md, the pnp-research skill, latest issue #3 through TMR-1/016, all five current handoffs and materially relevant original code/reports/raw were inspected.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Both trackers and canonical main.tex were preserved; TMR-5 remains whole-document synthesis owner. No task or schedule was touched.

**One next target:** TMR-5/TMR-1 should independently check the step-by-step product-control input clock and this exact cost-erasure undecidability reduction. Then derive a **one-sided, mechanically checkable sufficient condition** for removing semantically and cost-inert bits while preserving every all-step source-bound execution. The generic SAT-machine initial-potential superpolynomial lower bound remains **OPEN**.
