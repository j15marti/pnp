# Living log: worst-case derivation complexity Wbar_R

Status of P vs NP: OPEN. No lower bound or transfer theorem below is claimed beyond its label.

## 2026-11-05 17:00 UTC  (run CLAUDE-WCD-0001)
Report: research/agents/claude/2026-11-05_1700_CLAUDE_WCD-0001.tex

Findings
- [PROVED/EXACT] Wbar_R(N) with cost = proof length is exactly the Cook–Reckhow proof-size function s_R(N). Free strategy choice adds nothing new; the DAG/"reduced state" view is a representation of R-proofs.
- [PROVED/EXACT] Bridge(R) <=> (SAT not in P) or (s_R poly). Hence for any R with an unconditional superpolynomial bound (resolution, cutting planes, bounded-depth Frege) Bridge(R) is EQUIVALENT to SAT not in P. The "weakest bridge" is not weaker than the goal there; it is the goal.
- [CONDITIONAL] For R = EF (or any R containing PV reasoning): if some poly-time SAT algorithm A has poly-size R-proofs of the propositional translations of "A(F) rejects -> F unsat", then s_R is poly. So Bridge(EF) is open exactly where P=NP could hold with an algorithm whose correctness EF cannot certify cheaply.
- [HOSTILE CONTROL] A system R*_A whose verifier simply runs A makes Bridge trivial and a lower bound for it equivalent to A being incorrect: "sufficiently powerful" must be defined without reference to any SAT algorithm.
- [OPEN] superpolynomial s_EF. Time/space version: no fixed-R space bounds beyond known resolution results.
Literature note: search results confirm Cook–Reckhow (poly-bounded system iff NP=coNP). One summary claimed P=NP does not yield a poly-bounded system; that is wrong as stated (P=NP => NP=coNP => some, possibly unnatural, system), the real gap is naturalness/provable soundness. Next targets: Pich–Santhanam / Krajíček on unprovability of upper bounds in PV; proof-complexity generators (Razborov, Krajíček) for hard families.
Next: formalize "R proves soundness of A" bridge as a hypothesis on candidate A; Red Team: look for a natural R and algorithm A where reflection provably fails.
