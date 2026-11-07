# Living log: worst-case derivation program (P vs NP)

Shared objective (user directive, 2026-11-07):
  Wbar_R(N) = max_{F in UNSAT, |<F>|<=N}  min_{pi : F |-_R bot} cost_R(pi).
Priorities: (1) superpoly lower bound on Wbar_R in a fixed strong R, optimal sequence free (no charge for search);
(2) weakest bridge  SAT in P  =>  Wbar_R <= poly(N);  (3) test hard families against resolution, algebraic,
circuit-compressed, shared-DAG, adaptive-switching reasoning.
Roles: General Lower-Bound Lead; SAT-Circuit Reduction Builder; Hypergraph & Proof Certificates;
Time-Space Resource Auditor; Independent Red Team.  Status: P vs NP remains OPEN.

Rule: append newest entry at TOP. Statuses: PROVED/EXACT, KNOWN THEOREM, COMPUTATIONAL, CONDITIONAL, CANDIDATE, OPEN, FALSIFIED/RETIRED.

## 2026-11-07  Entry 1  (report: research/agents/claude/2026-11-07_CLAUDE_WORSTCASE-0001.tex)
- PROVED/EXACT  Bridge dichotomy: Bridge(R) <=> (P != NP) or (R p-bounded).
- PROVED/EXACT  Haken-type corollary: if R is unconditionally known not p-bounded (Resolution, Cutting Planes,
  Polynomial Calculus, bounded-depth Frege), then Bridge(R) <=> P != NP. Such a bridge is circular, NOT a weaker lemma.
- PROVED/EXACT  Free choice of derivation = nondeterminism: Wbar_R poly <=> R p-bounded => NP = coNP.
- KNOWN THEOREM (Cook translation; cite check pending) provable-soundness of a P algorithm in PV => poly EF refutations.
  Non-circular bridge lives only at R in {Frege, EF, stronger}; there it needs  P=NP => exists SAT algorithm with
  feasibly provable UNSAT-soundness (reflection gap)  -- OPEN.  Free "semantic answer" rules stay RETIRED (unsound).
- OPEN  superpoly Wbar_EF.  No unconditional Frege/EF lower bound exists (lit. check 2026-11-07).
- Literature clues: Cook-Krajicek (PV proves NP in P/poly => PH collapses); Pich et al. EF-route to P != NP;
  Khaniki-Pich-Sokolov CCC 2026 prover-adversary games, conditional EF route; Alekseev ToC 2026 PC+extension lower bound
  (algebraic analogue of EF, not EF); Proof Analysis Problem NP-complete for EF (arXiv 2506.16956).
- Next targets: (a) decide whether P=NP => EF p-bounded follows from any known uniformity (Levin search + reflection);
  (b) PC with extension rule: does Alekseev's technique transfer to the signed-hypergraph encoding;
  (c) time-space version Wbar_R^{(T,S)} for R = Res: Ben-Sasson-Nordstrom tradeoffs as controls.
