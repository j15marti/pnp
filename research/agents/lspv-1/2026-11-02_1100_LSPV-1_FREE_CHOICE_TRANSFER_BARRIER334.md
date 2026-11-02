# FREE-CHOICE-TRANSFER-BARRIER334: Formal proof lead

2026-11-02 11:00 PST. **P versus NP OPEN.**

## Model and exact obstruction

Fix one sound, effective, complete refutation calculus R before inputs or algorithms, with source-labelled axioms, legal inference rules and nonnegative weights. For any UNSAT CNF F let W_R(F) be the minimum sum of weights of distinct inference nodes of a valid acyclic refutation DAG. Shared derived nodes count once. The best sequence is granted for free as a LOWER-bound relaxation. Acquisition/search/failed policy costs are extra work; unverified SAT-label oracles are forbidden.

The proposed universal simulation is

\[
\mathrm{TR}(R):\quad \forall A\in\mathrm{TotalCorrectSAT}\ \exists\text{ polynomial }p_A\ \forall F\in\mathrm{UNSAT},\
W_R(F)\le p_A(N+T_A(F)), \quad N=|\operatorname{enc}(F)|.
\]

**Theorem: TR(ordinary general resolution) is FALSE.** This explicitly falsifies a candidate derivation-to-arbitrary-decider simulation, not P vs NP.

## Necessary condition: polynomially recognizable easy UNSAT subfamilies

Let H be any uniformly polynomial-time recognizable subset of UNSAT. If TR(R) holds, then W_R(F) is polynomial in encoded length for every F in H.

Proof: Fix a single all-CNF correct uniform decider A_H: validate input and reject malformed strings, recognize H and answer UNSAT when recognized, otherwise perform complete exhaustive assignment search. Its answer is correct on both labels, and its runtime on H is polynomial. Apply TR(R) to this one A_H and compose the two polynomials. QED. This necessary condition is not known sufficient.

## Exponential resolution lower bound and polynomial decision bypass

Choose an infinite family of connected cubic constant-edge-expansion graphs G_h, with h vertices and n=3h/2 edges. Represent each edge by one Boolean variable and impose an arity-three XOR equation at each vertex, with an odd total charge bit. Replace each equation by its four falsifying width-three CNF clauses. The resulting 4h-clause CNF is UNSAT since XOR of all constraints yields 0=1, and N=O(h log(h+2)) for binary-indexed source clauses.

Published expander/Tseitin proof-complexity results imply **W_Res(F_h)=2^{Omega(h)}** in unrestricted DAG resolution, under unit weight per binary resolution inference. This is imported from the literature, not derived from a finite experiment (Ben-Sasson and Wigderson, JACM 2001).

One fixed correct general SAT decider A_XOR parses and validates arbitrary CNF; groups every proper width-three clause by its three-variable support; accepts a parity representation only if each group is exactly the four clauses forbidding one parity; solves these extracted XOR equations by Gaussian elimination; otherwise uses exhaustive assignment search on the original CNF. On the hard Tseitin family, this uniform decider takes at most O(N^4) time and O(N^2) all-phase peak writable space under a conservative sequential bit implementation, including reads, grouping, source authentication, conversion and elimination. No expander identification, SAT oracle, or optimal policy is supplied. The decider is correct on SAT, UNSAT and malformed inputs.

TR(Resolution) would require 2^{Omega(h)} <= p_A(O(h^4 log^4 h)), an impossibility. Hence TR(Resolution) fails. The result does not refute TR(R) for a different, stronger fixed calculus.

## A fixed stronger calculus erases the same lower bound

Let R_Res+XOR contain ordinary resolution plus (i) derivation of a three-variable XOR equation from the **four verified original clauses** that encode it, (ii) sound XOR addition of two equations, and (iii) contradiction from 0=1. These are fixed, effectively checkable inference rules, not instance-specific axioms or hidden semantic jumps. Unit logical weight yields an explicit proof with h extraction nodes, h-1 XOR additions, and one contradiction node:

\[
W_{R_{\mathrm{Res}+\oplus}}(F_h)\le 2h.
\]

Thus the SAME original source has an exponentially large shortest resolution refutation but a short parity refutation. Computing and checking parity-row representations costs polynomial bit work; 2h is logical inference count, not total native machine steps.

## Independent finite source and both-label controls

A standalone producer and independently authored, no-import verifier checked:

| Graph/charge | Variables | Clauses | # satisfying assignments | Verified parity-proof inference nodes |
|---|---:|---:|---:|---:|
| K4 odd | 6 | 16 | 0 | 8 |
| K4 even | 6 | 16 | 8 | n/a |
| Petersen odd | 15 | 40 | 0 | 20 |
| Petersen even | 15 | 40 | 64 | n/a |

The verifier exhaustively checked each original truth table, all 4-clause parity bundles on all local 8 assignments, every acyclic proof DAG edge and final contradiction, direct CNF versus source-private forward circuits, and 256 guarded K4 cofactor rows. Additional controls: equality matrix rank 16, two sign-sensitive minimal-UNSAT occurrence flips, malformed rejection, and a source preallocation/freed-before-child example with all-phase memory exponent rho=1. The producer's full general-CNF solver uses a complete nonparity fallback. The verifier's truth-table enumeration is an OFFLINE experiment, not a free step of the online SAT decider. No finite exact optimum in unrestricted resolution or native FLMV tape trace is asserted.

## Machine-trace soundness firewall

A valid computation trace ending in UNSAT is not necessarily a valid UNSAT proof: the program that always prints UNSAT has such a trace even on SAT inputs. A uniform sound system must separately justify the program's global SAT correctness or restrict to a provably correct machine class. The assumption that A is externally known to be correct is not a free internal R inference. Existing wrapper and computation-trace results do not establish arbitrary-A TR(R). The exact derivation DAG, the optimizer finding it, and the physical machine run are three distinct quantities.

## Four falsifiers and remaining theorem gap

1. **FALSIFIED:** TR(Resolution) by one uniform polynomial-on-Tseitin exact decider and an exponential resolution size lower bound.
2. **FALSIFIED:** granting the optimal derivation automatically transfers restricted proof minimum to arbitrary decider runtime.
3. **FALSIFIED:** a rule trusting any halted NO execution without machine-correctness proof is sound.
4. **CONFIRMED restricted escape:** a fixed source-verified parity-extraction/XOR calculus produces O(h) inference DAGs on the same resolution-hard family.

For a stronger representation-inclusive R, BOTH arrows remain open: superpolynomial W_R for infinitely many general-CNF UNSAT inputs, and for EVERY fixed correct total decider A a sound polynomial domination W_R(F) <= p_A(N+T_A(F)). An arbitrary computation-to-certificate compiler must justify all machine-correctness dependencies. The current work does not establish either arrow for a strong general calculus.

## Sources, duplication audit and publication safeguards

[1] Ben-Sasson and Wigderson, *Short Proofs Are Narrow: Resolution Made Simple*, JACM 48(2), 149-169, 2001. https://doi.org/10.1145/375827.375835

[2] Cook and Reckhow, *The Relative Efficiency of Propositional Proof Systems*, JSL 44(1), 36-50, 1979. https://doi.org/10.2307/2273702

[3] Messner and Toran, *Optimal Proof Systems for Propositional Logic and Complete Sets*, ECCC TR97-026. https://eccc.weizmann.ac.il/report/1997/026/

The prior project general-SAT signed-hypergraph and guarded-interface reports already established an algebraic escape from dense-table bounds. Increment here: precise **TR(Resolution) refutation** and independently source-labelled finite DAG checks under the user-selected W_R model. Project GitHub and OpenAI GitHub were searched; no directly matching all-decider simulation theorem was located, which is not a novelty claim. No changes made to scheduled tasks, root main.tex, or other role-owned files.

**P versus NP OPEN.**
