# Living log: worst-case derivation complexity W̄_R(N) and its bridge

Shared objective: W̄_R(N) = max over UNSAT F with |F| ≤ N of the minimum R-refutation cost.
Target bridge: SAT ∈ P ⇒ W̄_R(N) ≤ poly(N). P versus NP remains **OPEN**.
Newest entry first. Each entry links its report, code and raw data.

---

## 2026-11-13 18:58 PST · WR-BRIDGE-0001

- **Report:** `research/agents/claude/2026-11-13_1858_CLAUDE_WR-BRIDGE-0001.tex`
- **New, PROVED/EXACT (independent review pending): oracle collapse.** For every fixed oracle-free Cook–Reckhow system R, "SAT ∈ P^A ⇒ W̄_R poly" holds for all oracles A ⇔ it holds for A = SAT ⇔ R is p-bounded. Since SAT ∈ P^SAT is trivial, any bridge proof that uses the decider only as a correct, polynomially clocked black box also proves NP = coNP and so destroys the lower-bound half. A valid bridge proof must be white-box: it must translate the decider's actual transitions into R-inferences. It must also be nonrelativizing.
- **The user's free-sequence point (PROVED):** taking the minimum over derivations is a sound lower bound for any procedure that outputs R-derivations. The same free knowledge on the solver side is exactly the oracle that the collapse theorem rules out.
- **KNOWN THEOREM, adopted:** for the resolution-type multisign hypergraph calculus, W̄ is already exponential (Urquhart 1987; Ben-Sasson–Wigderson 2001). The bridge for this calculus is therefore *equivalent* to P ≠ NP, not weaker (as already noted in Codex 11-11).
- **Literature clue:** Res(⊕) is resolution combined with parity reasoning, so it handles Tseitin. Exponential lower bounds are known only for depth-restricted Res(⊕) proofs (arXiv:2507.23008v2). Unrestricted Res(⊕) is a concrete candidate R whose lower-bound half is OPEN.
- **COMPUTATIONAL:** exact minimum resolution width for Tseitin formulas compared with Gaussian-elimination XOR counts on 8 small graphs. Code: `experiments/claude_wr/tseitin_width_vs_gauss.py`. Raw data: `results/raw/claude_wr/2026-11-13_1858_TSEITIN_WIDTH_GAUSS_RAW.json`. One graph per run, each capped at 25 s.
- **Next:** find the weakest white-box hypothesis that gives Bridge(Res(⊕)), and look for a 3-CNF family that is hard for unrestricted Res(⊕) yet survives Gaussian elimination and treewidth dynamic programming.
