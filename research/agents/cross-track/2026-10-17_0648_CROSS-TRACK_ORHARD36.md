# CROSS-TRACK ORHARD36 | 2026-10-17 06:48 KST

STATUS: PROVED/EXACT restricted proper-3CNF OR shield and Resolution restriction. COMPUTATIONAL finite audit. Arbitrary-decider transport OPEN. P versus NP OPEN.

PRE-SEARCH COMBINATIONS: (1) GAUGEORBIT35 odd-charge Tseitin + proof-transport OR shield; (2) charge H -> source B extraction versus universal contraction; (3) test delayed causal challenge against two-branch precomputation; (4) test same-final-input UWI against source-visible witnesses.

LATEST SPECIALISTS READ:
RESOURCE GUARDCOVER1: guarded decomposition survives only on marked inputs; arbitrary-decider padding defeats parent fallback.
NONREL ESSENTIALSLOT21: source-slot sensitivity gives at most linear bit probes and not SAT hardness.
UNIVERSAL DIAGONALLIST34: public excluded-witness tables admit direct final-formula witness reconstruction; Google Drive handoff read.
PROOF SEMDEG-FIREWALL1: semantic polynomial degree is coNP-hard but not a forced decider artifact. Additional exact ALLFIELD-SHIELD-RETRACTION1 and LOCALSHIELD1 compiler records examined.
Also consulted earlier GAUGEORBIT35, signed frontend, GitHub history, Google Drive cross-track ledger, and primary Urquhart/Ben-Sasson-Wigderson/Tseitin literature.

FORMAL OBJECT: For proper 3-clauses C=(a v b v c), put G_g(C)=(a v b v u_C) AND (~u_C v c v g), with private u_C and selector literal g. Let H(A,B) be the conjunction of G_s(C) for C in A and G_~s(D) for D in B, using disjoint original variable sets.

THEOREM 1: H(A,B) is proper 3CNF with exactly 2(m_A+m_B) clauses, and SAT(H)=SAT(A) OR SAT(B).

THEOREM 2 (actual Resolution transport): If H is UNSAT, every Resolution refutation of H projects to a refutation of A and to one of B with polynomial overhead. For the A projection set s=0, every A private auxiliary u_C to the third source literal c, every B auxiliary to 1, and every B variable to 0. Every input clause maps to an exact A axiom or a tautology. The B projection is symmetric. Standard literal substitutions and restrictions preserve Resolution inference by a polynomial simulation.

THEOREM 3 (restricted strong negative-control family): Let T_n be any uniform odd-charge cubic expander Tseitin 3CNF with Resolution size at least 2^{Omega(n)} (Urquhart; Ben-Sasson/Wigderson). For any source 3CNF B, build H(T_n,B), with n chosen proportional to B's canonical input size. Then SAT(H(T_n,B)) iff SAT(B). Hence this is an NP-complete family in which *every UNSAT member* has exponential Resolution size 2^{Omega(n)}, or 2^{Omega(L/log L)} with L=O(n log n) encoded output length. Yet a source-aware decider can extract B in polynomial time and solve B without constructing a Resolution proof. This gives no unconditional polynomial-time SAT decider, no general lower bound, and no P != NP proof.

CAUSAL NEGATIVE CONTROL: A delayed bit selecting between two publicly preannounced B0,B1 need not force SAT work after release: under a hypothetical polynomial SAT decider precompute both statuses before release, then select one bit in O(1) post-release work. The preprocessing must be charged. With k=O(log N) preannounced bits, 2^k cases can still be precomputed in polynomial time (exponents may be large). No claim about unbounded streams.

HOSTILE AUDIT: K4 odd-charge T, all 256 subsets of its companion full eight-clause three-variable cube as B, 20,480 projected clause images, 23 independent DPLL checks, 256 offline choice tests, negative selector-polarity corruption. 50,971 assertions PASSED, zero failures. Only finite identities are experimentally tested; asymptotic hard Resolution bound rests on the cited literature.

PROOF DAG:
ESTABLISHED: expander Tseitin Resolution lower bound in its specified system.
PROVED: proper-3CNF shield semantics; source clause/tautology retraction; polynomial Resolution translation; SAT-hard family with all UNSAT members Resolution hard.
CONDITIONAL: transport through actual exact-(2,2) PC22 requires separately checked clause-level retraction, not merely algebraic degree.
OPEN: arbitrary SAT decider -> necessary proof artifact; all-input charged semantic contraction; compulsory nonrelativizing WRAPPER operation; unconditional same-input UWI; P != NP.

NEXT ASSIGNMENTS:
RESOURCE: fully charge canonical H recognition, B extraction, scans, space, recursion, and arbitrary-input fallback.
NONREL: break preannounced-branch precomputation and exhibit a correctness-forced post-release SAT operation.
UNIVERSAL: same final formula, same clock, source-aware witness extraction; distinguish conditional P!=NP implications.
PROOF: verify actual 72m/96m PC22 selector compiler's Boolean clause-level Resolution retraction, or produce a counterexample; never substitute PC degree for Resolution without proof.

AUDIT LOCAL:
2026-10-17_0648_CROSS-TRACK_ORHARD36_FULL.md
2026-10-17_0648_orhard36_audit.py
2026-10-17_0648_orhard36_results.json
FULL REPORT SHA256 94e33d654e986203df580fb73bea16b6a2512fd36e718099c776211d71ddce59

REFERENCES:
[1] Urquhart, Hard Examples for Resolution, JACM 34(1), 1987.
[2] Ben-Sasson and Wigderson, Short Proofs Are Narrow, JACM 48(2), 2001, DOI 10.1145/375827.375835.
[3] Itsykson et al., Tight Bounds for Tseitin Formulas, SAT 2022, DOI 10.4230/LIPIcs.SAT.2022.6, regular-Resolution scope distinguished.
[4] Jahanjou, Miles, Viola, Local Reductions, Information and Computation 261, 2018.

END_ORHARD36_0648_KST