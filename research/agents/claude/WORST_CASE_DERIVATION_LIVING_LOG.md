# Living log: worst-case minimum-derivation program (Claude scheduled routine)

This log tracks the shared target

`Wbar_R(N) = max_{F in UNSAT, |<F>| <= N} min_{pi : F |-_R bot} cost_R(pi)`

and the weakest sufficient bridge **B3(R): SAT in P ⇒ Wbar_R(N) ≤ poly(N)**. Status labels follow AGENTS.md. **P versus NP remains OPEN.** New entries go at the top.

> **Consolidation note (2026-11-13 19:52 PST).** Earlier runs each wrote to their own `ccr-1695bd63-*` branch, and none of those branches has been merged to `main`. They also used five different log filenames: `LIVING_LOG.md`, `WORST_CASE_DERIVATION_LOG.md`, `WORST_CASE_DERIVATION_LIVING_LOG.md`, `WCD_HANDOFF.md`, `worst-case-derivation/LOG.md` and `wr-bridge/LOG.md`. This file is the single consolidated log. Each entry below names the branch that holds its report. Use this filename for all future entries.

## Settled: do not re-derive

- **Free optimal sequence (PROVED).** Taking the minimum over derivations gives a sound lower bound for any procedure that outputs R-derivations. Because the free choice is nondeterministic, Wbar_R is a proof-complexity measure, so "Wbar_R is polynomial for some R" is equivalent to NP = coNP (Cook–Reckhow).
- **Weak R (PROVED).** If the lower bound LB(R) is known, then B3(R) is equivalent to SAT ∉ P, so it is a reformulation rather than progress. This covers resolution, which includes the multisign hypergraph merge calculus, as well as CP, PC, AC0-Frege and regular/tree-like Res(⊕).
- **Black-box barrier (PROVED).** Any proof of B3 that treats the decider as a black box also proves B3 relative to the oracle A = SAT, which makes R p-bounded. A valid B3 proof must therefore use the decider's code and must not relativize.
- **Strong R (PROVED).** If R p-simulates ER, then LB(R) is a superpolynomial EF lower bound, which has been open since 1979.
- **Exact R_T decomposition (PROVED).** Let R_T be EF together with T-proofs of clocked soundness. Then PROV_T ⇒ B3(R_T).

## 2026-11-13 19:52 PST · PROVLADDER-0001 (branch `ccr-1695bd63-3qbc8a`)
- Report: `research/agents/claude/2026-11-13_1952_CLAUDE_PROVLADDER-0001.tex`
- **PROVED/EXACT, using known theorems (Cook–Nguyen translation, Ben-Sasson 2002, PRST 2016).** No correct polynomial-time SAT decider has a V0-provable *clocked tableau soundness* sentence. If it had one, AC0-Frege would refute every UNSAT 3-CNF in polynomial size, which contradicts the known lower bound for Tseitin formulas on expanders. This holds unconditionally and covers every polynomial-time machine, not just those definable in V0, so it is stronger than the definability remark in WCD-0001.
- **KNOWN THEOREM.** S^1_2 (respectively V^1) is ∀Σ^b_1-conservative over PV (respectively VPV). So PROV_{S^1_2} is the same as PROV_PV; this answers WCDERIV-0001's next target.
- **Ladder.** The V0 rung is dead: PROV_{V0} is equivalent to SAT ∉ P. Every other rung (V0(2) / AC0[2]-Frege, VTC0, VNC1 / Frege, PV / EF) is OPEN, and its lower-bound half needs a 3-CNF lower bound at or beyond AC0[2]-Frege.
- **CANDIDATE.** A decider whose soundness proofs translate into depth-d Frege proofs of size poly(t) needs t ≥ exp(n^{Ω_d(1)}).
- **Next:** red-team Step 2 (bounded-depth closed evaluation of the tableau). Find out whether PROV_{V0(2)} already collapses by a known route.

## 2026-11-13 18:58 PST · WR-BRIDGE-0001 (branch `ccr-1695bd63-16bmvn`)
- Proved oracle collapse: for oracle-free Cook–Reckhow R, Bridge^A(R) holds for all oracles A ⇔ Bridge^SAT(R) ⇔ R is p-bounded.
- COMPUTATIONAL: Tseitin minimum resolution width compared with Gaussian XOR count on 8 graphs.
- Literature: Res(⊕) lower bounds are known only with a depth restriction (arXiv:2507.23008).

## 2026-11-14 (UTC) · WCDERIV-0001 (branch `ccr-1695bd63-j4ojj1`)
- Thm 1 (weak R ⇒ B3 ≡ P≠NP). Thm 2: R_T, with BR(R_T) ⇐ PROV_T.
- Exact tree-like resolution minima: PHP m=1..3 → 5, 21, 85; Tseitin K3..K5 → 11, 55, 463.

## 2026-11-13 16:52 PST · WCD-PVEF-0001 (branch `ccr-1695bd63-wbz52u`)
- Cook PV→EF anchoring: if PV proves the rejection soundness of some polynomial-time decider, then Wbar_EF is polynomial. The residual gap is PV-CERT.

## 2026-11-13 15:54 PST · B3-REFLECT-0001 (branch `ccr-1695bd63-o78at4`)
- B3 is proved for a size-gated reflection calculus R_KP, but LB(R_KP) is of NP≠coNP strength. Without the gate the calculus is linear (a hidden validity oracle).

## 2026-11-13 14:50 PST · B3-ORACLE-0001 (branch `ccr-1695bd63-r41ksd`)
- First oracle-collapse and black-box indistinguishability theorems. The Cook–Krajíček 2007 route is credited.

## 2026-11-13 14:00 PST · WBAR-EXACT-0001 (branch `ccr-1695bd63-0zeip0`)
- Exact Wbar_Res over all minimally unsatisfiable (MU) exact-3-CNFs on 4 variables: 50,528 formulas in 188 classes, maximum 11 steps. DAG beats tree-like resolution in only 1 class.
- Open: cross-check against Peitl–Szeider (JAIR 2021).

## 2026-11-13 10:00 PST · BRIDGE-CLASS-0001 (branch `ccr-1695bd63-nmunbf`)
- R_mix341 p-simulates ER. Bridge classification by the strength of R.

## 2026-11-13 00:51 PST · WCD-0001 (branch `ccr-1695bd63-53h6df`)
- First fixed-R status. Exact tree-like resolution experiment. Matched-theory ladder by definability.
