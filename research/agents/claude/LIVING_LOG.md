# Claude living research log

Append-only. One entry per scheduled Claude run. Status labels follow AGENTS.md. **P versus NP remains OPEN.**

## 2026-11-12 10:49 PST — BRIDGE-0001 (shared objective: worst-case minimum derivation cost W̄_R)

- Report: `research/agents/claude/2026-11-12_1049_CLAUDE_BRIDGE-0001.tex`. LaTeX source only; no TeX toolchain in the container, so it was not compiled.
- PROVED/EXACT (elementary): B(R) ⇔ (SAT ∉ P ∨ PB(R)). Once R has a known lower bound, B(R) *is* P ≠ NP. This covers Res, CP, PC and AC0-Frege.
- PROVED/EXACT: the bridge gets easier and the lower bound gets harder as R gets stronger. Strategy switching can only lower the minimum.
- PROVED/EXACT (new): **relativization/algebrization barrier.** For a fixed oracle-free R, the bridge relativized to a PSPACE-complete oracle is equivalent to PB(R). So a relativizing (or algebrizing) proof of B(R) would prove NP = coNP. Black-box solver-to-derivation extraction (PQ ledger item 5) therefore fails for every known-hard calculus.
- PROVED/EXACT: if SAT ∈ P, every Cook–Reckhow system is automatable. The "free optimal sequence" relaxation is then exact, and W̄_R equals the running time of the best R-based solver.
- KNOWN THEOREM: the only known code-using bridge goes through Extended Frege (Cook 1975, Krajíček–Pudlák). A PV-provably-sound polynomial SAT algorithm makes EF polynomially bounded. CANDIDATE replacement target (T): SAT ∈ P ⇒ some polynomial SAT algorithm is PV-provably sound. Status OPEN.
- Ledger rows L41–L43 added and regenerated. Categories: B(Res) ≡ P ≠ NP; "Res automatable" ≡ P = NP; B(EF) is a half-win.
- Root `main.tex` was not edited: there is no Claude ownership region. This is suggested input for the LSPV-5 arbiter.
- Next gap: a nonrelativizing code-using bridge (T), or an EF-strength lower bound. Both OPEN.
