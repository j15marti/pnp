# Living log: worst-case derivation complexity W̄_R (Claude)

Directive: study W̄_R(N) = max_{F∈UNSAT, |F|≤N} min_{π: F⊢_R ⊥} cost_R(π); priority bridge SAT∈P ⇒ W̄_R ≤ poly. **P versus NP remains OPEN.** Entries are append-only, newest last. Related roles: LSPV-1..5 reports under `research/agents/`.

## 2026-11-06 — BRIDGE-0001
- File: `2026-11-06_CLAUDE_BRIDGE-0001.md`.
- Result: dichotomy for the bridge. Through any R with an unconditional superpolynomial lower bound it is equivalent to SAT∉P (circular). Through R_M it is also circular. The only informative route is eF-strength R with a provability hypothesis (PV-provable correctness), which yields only "no provably correct polytime SAT algorithm".
- Literature: no Frege/eF superpolynomial lower bound found; efficient-adversary (CCC 2026) and Implicit-eF/circuit-lower-bound reductions are the live conditional lines.
- Next: formalise the weakest theory T whose proofs translate into R and still yield Bridge_prov; check whether Bridge(eF) can be refuted relative to an oracle.
