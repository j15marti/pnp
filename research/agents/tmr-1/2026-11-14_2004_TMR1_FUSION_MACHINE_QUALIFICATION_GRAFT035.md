# TMR-1/035: Fusion tariff machine qualification and source-core/terminal-mask falsifiers

**2026-11-14 20:04 PST**. Role: TMR-1 Machine Model Lead. Claim **FUSCORE054**. The two scoped elementary theorems and exact seven-inference proof are **PROVED/RESTRICTED**, independent TMR-2/TMR-5 mathematical review **OPEN**. Finite Python tests **COMPUTATIONAL**. **P versus NP remains OPEN.**

## Candidate and four hostile tests

Candidate: use a large authenticated-source multiscale obstruction as the reduced-product tariff potential in a complete SAT machine or native source-bound refutation. Falsifiers, fixed before the run: (1) genuine last-step discharge of a source-static potential at cost one; (2) a polynomial source-pattern test that bypasses the alleged hard family; (3) a constant-sized shared native resolution DAG on a padded proper-3CNF family; (4) free aliasing or cheap compact-affine/Horn/Krom mechanisms that were omitted from an alleged rule inventory. Tests (1)-(3) succeed; test (4) is a required conservative MAY guard beyond the specified fragment.

## Concrete qualification, exact states, and zero-cost classes

**Q-TM, direct all-input machine model, MODEL QUALIFIED / RESOURCE POTENTIAL OPEN.** Fix one finite total deterministic multitape machine A with finite control, finite alphabet, constant number k(A) of writable tapes, read-only authenticated binary 3-CNF input F with endmarkers and movable input head. A full configuration is (A,F,q,h_in,(t_i,h_i) for i=1..k(A), output, physical paid history, interfaces, assumption/branch obligations). All physically stored ledgers, caches, source indices, temporary encodings, message queues and heads count as writable tape contents. Each authentic machine step reads heads, writes finitely many symbols, moves heads at most one position, updates state and costs exactly **one** transition. There is no nontrivial physical zero-cost step. Therefore authentic zero-cost SCCs are singleton and cl0(C)={C}, aside from mathematical aliases of literally identical full configurations. A halting configuration's SAT/UNSAT label is correct only if A is a correct decider for both well-formed labels and rejects malformed input. One fixed A serves all input lengths. No oracle, advice, unbounded-word operation, or free random-access translation.

**Q-RES-H, explicit native proof laboratory, QUALIFIED/RESTRICTED.** State = authenticated source CNF F plus complete derived-line DAG (source IDs, shared parent IDs, exact clauses, paid identity set) plus terminal status. SOURCE(i) references exactly source clause i at zero *abstract inference* cost; repeated source or shared-line references count once. RESOLVE(i,j,p) at cost one is legal iff p and its negation occur in the respective clauses, and writes the actual nontautological resolvent. HALT_UNSAT is legal at zero inference cost only with the empty clause already derived. Zero-inference SOURCE and alias events require saturation in this calculus's cl0, but their physical input acquisition is NOT free in Q-TM. This is ordinary resolution, **not** historical mixed checker /341 (FAIL full logical authority) or /386 (RESTRICTED guarded fragment). The laboratory has an UNSAT terminal only, not both-label SAT decision.

Seven candidate tariff columns for TMR-2/3/4: (CNF, affine, separator, fusion, Gamma assumptions/discharge, private/export interface, machine access/work). Columns must be defined on the *dynamic* completed concrete/abstract state, not on F alone. Physical simultaneous steps can jointly discharge several coordinates. Unknown changes are MAY, never forbidden by fiat.

| Legal rule | Exact cost | Authentic zero behavior | Required tariff audit |
| --- | ---: | --- | --- |
| Q-TM every real transition, including final HALT | 1 | No free transition | Every column, unrestricted candidate MAY |
| Q-TM literal identical-state alias | 0 | Singleton SCC | Delta = 0 |
| Q-RES-H SOURCE(i) | 0 native inference | Add authenticated source clause, saturate | No positive uncharged logical discharge |
| Q-RES-H RESOLVE(i,j,p) | 1 native inference | Later reuse of derived line free | All seven coordinate deltas |
| Q-RES-H HALT_UNSAT with empty line | 0 | Terminal | Phi(goal)<=0 |
| Extension, Gaussian, learned clause, branching/joins, arbitrary machine precomputation | not specified in Q-RES-H | MAY on Q-TM | Independent complete inventory OPEN |

## Explicit proper-3CNF growing family, exact seven-step short refutation

Let x,y,z be distinct. Write B(ell) for the four proper width-three clauses (ell or y or z), (ell or y or not z), (ell or not y or z), (ell or not y or not z). B(ell) is equivalent to the unit literal ell.

For n>=1, let H_n=B(x) AND B(not x) AND the n disjoint proper clauses (a_i or b_i or c_i), each with three fresh distinct variables. Put S_n=B(x) AND B(x) AND the same disjoint padding. The H_n are UNSAT and S_n are SAT. Use explicitly declared signed-decimal source encoding "V=<v>;C=<m>:<lit>,<lit>,<lit>;..." with fixed source order. Then #variables=3+3n, #clauses=8+n, and encoded bit length L_n=Theta(n log(n+2)); a standard self-delimiting binary-ID encoding is polynomially equivalent.

Native source-bound DAG for H_n: resolve z-opposite pairs twice within each forcing block (4 inferences); resolve each block's two binary clauses on y (2); resolve x against not x (1). EXACTLY **7** native resolution inferences and 8 authenticated source premises, irrespective of n; reuse is counted once. The proof's referenced source IDs and parent indices need O(log L_n) bits. Physical source parse/input costs must be paid when translating Q-RES-H to Q-TM, so 7 logical inferences are NOT a 7-step SAT machine proof.

One fixed total correct SAT decider A_graft first checks whether the first eight source clauses form these two opposite forcing blocks. If yes it rejects, because their conjunction alone is UNSAT. Otherwise it uses exhaustive search on all valid input formulas, rejecting malformed inputs. This is a fixed all-length algorithm; membership detection is polynomial in L, and hence T_A_graft(H_n)<=poly(L_n) even though A_graft is exponentially slow elsewhere. This disqualifies H_n as a universal hard family.

## Theorem A: terminal-mask collapse (PROVED/RESTRICTED)

Let a concrete terminating computation have final paid edge C_prev -> C_goal of cost w. Suppose h_j(F,A)>=0 depends only on immutable source F and fixed program A. For lambda_j>=0 define Phi(C)=1_{nonterminal(C)} sum_j lambda_j h_j(F,A). If Phi(C)<=w(r)+Phi(C') holds on every authentic step and all completed goals have Phi<=0, then necessarily

**sum_j lambda_j h_j(F,A) <= w**

on the last edge. Proof: source and program are identical at both endpoints; the penultimate potential is the displayed sum and terminal potential is zero. For standard Q-TM, w=1. No *source-static terminal-masked* family of multiscale coordinates can yield a superpolynomial initial potential through a unit last transition. This does NOT refute genuinely state-dependent, paid-progress potentials.

## Theorem B: recognizable same-label family graft (PROVED/RESTRICTED)

If a set R of well-formed SAT inputs is recognizable in polynomial time and all inputs in R have one provably correct label b, there is a single total correct SAT decider polynomial-time on R: test R, output b on matches, and otherwise run complete brute-force SAT. Thus a fixed recognizable single-label family contained in R cannot furnish a hard input for *every* correct algorithm. This says nothing against the proper P!=NP quantifiers, which allow hard F to depend on A, k, C, L0. Nor does it replace the independent same-system proof-system bridge.

For the explicit family, any nonnegative native-inference tariff with exact all-step simulation and Phi(goal)<=0 must obey Phi(H_n,start)<=7 by telescoping along the real seven-step shared resolution DAG. A superpolynomial initial native-inference potential on this family is FALSIFIED. Machine source scans remain polynomial in L_n.

## Dependency DAG, same-system gate, and ranked statuses

Qualified state/goal/rules -> authentic cl0 -> dynamic reduced-product coordinates -> every legal paid/zero tariff row -> exact rational lambda certificate -> terminal preservation -> independently proved superpolynomial initial potential on an explicit growing family -> same-system transfer -> P!=NP.

The independent family proof bridge would require SAT in P => exists C,d,n0 for all n>=n0: W_R(F_n)<=C(L_n+1)^d for **exactly the same fixed qualified R**. Merely outputting UNSAT does not entail a native source-bound proof in R. Direct machine route instead needs full all-step simulation for *every* correct fixed uniform A, including arbitrary workspace and preprocessing. A universal target itself must not be relabeled a theorem. No such transfer is proved.

| Obligation | Verdict |
| --- | --- |
| Fully specified standard fixed multitape machine model, physical costs and trivial cl0 | MODEL QUALIFIED |
| Explicit resolution calculus and sound 7-step source-core refutation | PROVED/RESTRICTED |
| Terminal-masked static source potential with large initial gap | FALSIFIED for unit-cost HALT |
| Explicit padded H_n as same-system proof hard family | FALSIFIED, 7 inferences |
| H_n as a hard family for every correct SAT machine | FALSIFIED by A_graft |
| Dynamic affine/fusion/separator reduced-product component and full tariff rows | OPEN |
| Fusion/interpolation proof-to-circuit transfer | OPEN |
| Superpolynomial initial gap on any qualified candidate family | OPEN |
| SAT-in-P to bounded proof work in that exact system; or all-machine simulation | OPEN |
| MCSP/MKTP/FLMV magnification | OPEN / SECONDARY |

## Native verification and provenance

Native CPython executed experiments/tmr/tmr1_prefix_core_gate054.py; immutable local stdout is results/raw/tmr/2026-11-14_2004_TMR1_FUSCORE054_RAW.json, with **2,445 assertions and zero failures**. Tested n=1..44, exact seven-inference traces, input encoding length, forcing-block truth tables, positive SAT witnesses, small exhaustive SAT/UNSAT controls, renaming of pivot indices, illegal pivot rejection, and exact rational terminal-mask row violations. This is a Python source-clause model, not a compiled Turing machine. The asymptotic claims above follow from the explicit construction and elementary mathematical proofs, not finite tests.

Preflight: controlling fusion directive read FIRST; 2026-11-13 TMR replacement; both full proof trackers and canonical main.tex, including recovery of actual large proof2/main via Git blobs after empty Contents bodies; AGENTS.md; CODEX.md; research skill; all five handoffs; latest issue #3; original TMR-3/034, TMR-4/035, TMR-5/031, TMR-1/034 and LEAD-0029 original Lipschitz audit. Earlier raw semantic-mass non-Lipschitz, one-step fanout tariff and minimum-remaining-circuit-cost arguments retained, not misrepresented as new.

Primary literature inspected for scope, not imported as an unproved bridge: Fortnow, Lipton, van Melkebeek, Viglas, *Time-Space Lower Bounds for Satisfiability*, JACM 2005, doi:10.1145/1101821.1101822; Krajicek, *Interpolation theorems, lower bounds for proof systems*, JSL 1997, doi:10.2307/2275541 (resolution feasible interpolation, not all-machine transfer); Atserias-Dalmau, *Combinatorial Characterization of Resolution Width*, JCSS 2008, doi:10.1016/j.jcss.2007.06.025 (resolution width/space only).

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Root proof1.txt, proof2.txt, main.tex and five schedules are untouched. Request TMR-2 define a dynamic source- and affine-closed component; TMR-3 charge real simultaneous terminal steps and prefix parsing; TMR-4 verify terminal-mask LP violations and authentic zero closure; TMR-5 independently replay the 7-step source DAG and investigate a nontrivial repaired family. **P versus NP remains OPEN.**
