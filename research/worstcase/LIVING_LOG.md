# Living log: worst-case derivation complexity (W_R) programme

Directive (user, scheduled routine): study
  W_R(N) = max_{F in UNSAT, |F|<=N} min_{pi: F |-_R bot} cost_R(pi)
with free choice of the optimal derivation (search is not charged). Priority: the weakest sufficient bridge
  B(R):  SAT in P  =>  W_R(N) <= poly(N).
Five roles: General Lower-Bound Lead; SAT-Circuit Reduction Builder; Hypergraph & Proof Certificates; Time-Space Resource Auditor; Independent Red Team.
Status of P vs NP: **OPEN**. Nothing below proves a lower bound or the bridge.

| Date | Entry | Report | Net status |
|---|---|---|---|
| 2026-11-07 | WC-0001: bridge dichotomy, Cook-Reckhow normal form, what B(R) can and cannot be | `2026-11-07_WC-0001_BRIDGE_DICHOTOMY.md` | PROVED/EXACT (elementary) + OPEN targets listed |

## Open targets after WC-0001
1. Find R (not world-dependent) with a *proved* B(R) and an *unproved* L(R) - see report section 4 for what "proved B" must look like.
2. Time-space variant: B_{t,s}(R) with cost = (DAG size, peak clause space); test against Res/PC/CP/EF-with-space.
3. Red team: attack Lemma 3 (dichotomy) and the formalisation claim in Lemma 4.
