<!-- LSPV-1 REPORT::520::2026-11-09T04:00-08:00 -->
# LSPV-1/520: B3 is vacuous-if-P≠NP; what it demands of a fixed R

**Status: PROVED/EXACT (elementary logic, B3 equivalence) + KNOWN THEOREM (reflection route) | P versus NP OPEN. No lower bound on W̄_R is claimed.**

## Scope
Directive: 2026-11-02_1204 five-role worst-case minimum-derivation refocus (B1⇒B2⇒B3; B3 primary). Read: that directive, AGENTS.md, newest LSPV-1/516, knot/link handoff (2026-11-09; separate graph-vs-knot topology track, not used here). Root main.tex and trackers were NOT reconciled this run (see Limits).

## Result 1 (PROVED/EXACT): B3 equivalence
Let R be a fixed Cook–Reckhow-style system (poly-time proof checker, sound, complete). Then
B3(R) ⟺ [P=NP ⇒ W̄_R is polynomially bounded].
Consequences:
1. If P≠NP, B3(R) is vacuously true for every R. A proof of B3 is therefore only informative in the world P=NP.
2. In the world P=NP, B3(R) says R itself is p-bounded (then NP=coNP by Cook–Reckhow). So B3(R) + "W̄_R superpolynomial" ⟺ P≠NP, trivially. The bridge carries no content beyond the separation unless it is proved by a route that does not itself assume P≠NP. Any proof of B3 must exhibit, uniformly in an unknown polynomial algorithm A, polynomial R-derivations. That is a simulation-of-unknown-A statement, i.e. B2 in disguise, not a weaker one.
3. Hence the weakest sufficient bridge is not "weaker" in difficulty than the lower bound unless R is chosen so that B3 has an independent proof (item below).

## Result 2 (KNOWN THEOREM, route): reflection
If A decides SAT in poly time and the theory T_R associated with R (e.g. PV for EF) proves "A is correct", then R is p-bounded (Cook; Krajíček). Provable correctness of A is exactly the missing hypothesis: P=NP alone gives no proof of A's correctness in T_R. For B3 one would need R to carry a uniform schema "if M is poly-time and T_R-correct then …", which is A-dependent and therefore not a fixed R unless R is the universal/reflective system; for universal systems the lower bound becomes at least as hard as Krajíček–Pudlák optimal-proof-system questions.

## Literature (searched this run)
- Pich–Santhanam, [arXiv:2312.08163](https://www.arxiv.org/abs/2312.08163): extra hypotheses under which "EF not p-bounded ⇒ P≠NP" — the contrapositive of B3 for R=EF, valid only with additional assumptions; closest published analogue of our bridge, and it confirms B3 is not free.
- Krajíček, [Frege/EF survey](https://msekce.karlin.mff.cuni.cz/~krajicek/frege.pdf): p-bounded system ⟺ NP=coNP; no nontrivial Frege/EF lower bounds known.
- Krajíček forcing paper ([Cambridge JSL](https://www.cambridge.org/core/journals/journal-of-symbolic-logic/article/abs/forcing-on-bounded-arithmetic-ii/82967C3232A39E14976AE50347B422E8)): uses a consequence of P=NP stronger than NP=coNP — a possible template for what B3 would need.
- No 2025–26 result settling B3 was found by one standard search; classification: Pich–Santhanam = USEFUL ANALOGY requiring a transfer theorem to the project's R_mix341; the rest KNOWN THEOREM.

## Next targets
(a) Check Pich–Santhanam's hypotheses against R_mix341: which of them hold for the project's fixed system. (b) State which fragment of B3 is provable for restricted R (e.g. resolution: unconditionally false as stated? W̄ exponential, so B3 would force P≠NP — equivalent to the separation for that R; red-team should confirm). 

## Limits / audit
No duplication found in the lspv-1 titles scanned, but search was filename-level only. Root main.tex and proof1/proof2 trackers not updated; owned-region reconciliation is deferred to the next LSPV-1 run. This is a CANDIDATE-level framing note plus elementary equivalences, not new lower-bound progress.

<!-- END_OF_VERIFIED_REPORT::LSPV-1::520 -->
