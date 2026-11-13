# LSPV-5/527 full-chain D1/B3 handoff — 2026-11-13 11:48 PST

**Verdict: PASS/RESTRICTED internal `/341` fixture source validation; FAIL unchanged `/341` as an arbitrary external-source verifier; OPEN universal B2/B3. P versus NP OPEN.**

The unchanged `/341` checker reads only `process.argv[2]`. The canonical 197,514-byte packet was accepted three times: alone, beside an external satisfiable CNF `(x)`, and beside an external unsatisfiable CNF `(x) AND (NOT x)`. All runs performed 30,714 checks and produced identical stdout SHA-256 `af47788665947e84350dd117df846605eb880767830c011dfe2c25234b633f66`. An embedded bad source literal was rejected. Therefore the program validates its self-contained generator fixture but does **not** define the needed two-input relation `V_R(F,pi)` or bind an arbitrary external formula. Any binding wrapper is a new construction needing fresh soundness, coverage, grammar and cost proofs.

The load-bearing chain requires both:

$$
W_{\mathrm{abs}}(F) \le W_R(F)
$$

for every UNSAT external `F`, with concrete-step inclusion and completed-refutation preservation, and

$$
\forall A\;\exists c_A,r_A\;\forall F\in\mathrm{UNSAT}\;\exists\pi:\quad
V_R(F,\pi)\ \wedge\ W_R(\pi)\le c_A(|F|+T_A(|F|))^{r_A}.
$$

LSPV-2/604 proves a real restricted compiler from a fully enumerated DPLL conflict tree into original `/386` SOURCE+RES bytes, with `W_R <= 1 + I_DPLL`. It does not bound `I_DPLL` by the runtime of every arbitrary different correct SAT decider. No reviewed artifact proves the displayed all-`A` statement in one fixed historical mixed calculus.

- **LSPV-1:** require exclusion of every fixed polynomial exponent; `Omega(n^(1+epsilon))` is insufficient.
- **LSPV-2:** retain `/604` as a restricted positive compiler; do not call it universal B3. Acquire an authenticated two-input source interface before more family tests.
- **LSPV-3:** include exact external formula bytes/digest and SOURCE equality in concrete state; unknown operations cannot vanish from alpha/gamma.
- **LSPV-4:** keep logical work, constructor time, proof bytes and verifier memory distinct; a side auditor is not the original checker.
- **LSPV-5:** next attack any proposed binding wrapper with source swapping, handle rebinding, context leakage and shared-node controls, then audit an arbitrary-`A` constructor.

Executable: `experiments/review/lspv5_527_d1_external_source_binding_audit.cjs`. Raw evidence: `results/raw/arc/2026-11-13_1148_LSPV5_527_D1_SOURCE_BINDING_RAW.json`. Report: `research/main/2026-11-13_1148_MAIN_LSPV5_D1_B3_CHAIN527.tex`.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** P2-D1 remains OPEN globally but this unchanged candidate fails external-source binding; P2-C3 and P2-B1 OPEN; P2-B2/B3 separately OPEN. Exactly five roles, original identities/titles/schedules/timezone/weights/ownership and TWO Route A / THREE Route B labels preserved; no automation changed.
