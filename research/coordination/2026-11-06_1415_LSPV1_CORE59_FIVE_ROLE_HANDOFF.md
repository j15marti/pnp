# LSPV-1/456: five-role handoff, 2026-11-06 14:15 PST

**Five existing roles unchanged**: LSPV-2/4 primary Route A; LSPV-1/3/5 primary Route B. No task, title, schedule, timezone, enabled-state, ownership, historical calculus, or inference weight mutation. **P versus NP OPEN.**

**PROVED/RESTRICTED advance:** For the existing Chvátal--Szemerédi / Pang random proper signed width-three CNF distribution, exactly `m=8n` iid indexed clauses sampled with replacement from `8*C(n,3)` choices on *n ambient labels*, the minimum UNSAT original-source subset has more than `floor(n/59)` clauses with high probability. Previous LSPV-3/443 and /457 certified n/64 and n/60. The refinement retains the finite-population factor `exp[-r(r-1)/(2n)]` when bounding `C(n,r)`.

Exact integer-rational threshold:

$$
\frac{8e^2}{59}e^{-1/118}
<\frac{127682512}{128361875}<1.
$$

Tarsi's minimum-UNSAT deficiency lemma and a union bound imply the result. For any *sound, source-explicit, conservative-DEF, at-most-binary-premise, unit-paid* refutation DAG, with all legal mixed rules and optimal sharing/branch selection included, this entails

$$
W_R(F)\ge\lfloor n/59\rfloor,\qquad
\operatorname{span}_R(F)\ge\left\lceil\log_2(\lfloor n/59\rfloor+1)\right\rceil
$$

with probability `1-o(1)`. This is **only linear work and logarithmic ideal span**, not a superpolynomial mixed-calculus lower bound, same-machine computation bound, or B3.

**Published-family ledger:** Ordinary Resolution exponential lower bounds on random 3-CNF [Chvátal--Szemerédi 1988]; Pang arXiv:2610.00837v2 reports DAG `Res(PC_r/F_p)` lower bounds for fixed parameters (2026 preprint); both are restricted systems without unrestricted conservative DEF. Cubic odd Tseitin has known linear semantic AND3/GF(2) upper proofs; Haken PHP has Cook ER shortcuts; Braun bit-PHP requires an actual lower-bound-preserving strict-3 conversion, not mere equisatisfiability. Never exclude known shortcuts or double-charge shared inference nodes.

**COMPUTATIONAL:** n10/m80 and n12/m96 original strict-3 sources were exhaustively UNSAT, greedy inclusion-minimal (NOT globally minimum) cores have sizes 19/21, and all 40 individual core deletions are SAT. Separate JS verifier passed **1,599** original-source and theorem arithmetic assertion groups, rejected **5 corrupted source records** and **6 malformed DIMACS** controls. Original DIMACS SHAs `a7907e77...ab3357` and `493b6039...ede8e485`. Local host Python work about 18s with ~96MB peak RSS; Node verifier 0.10s and 33,144 KiB RSS. No historical Rmix accepted-byte checking and no FLMV same-machine resource inference.

**Next cross-role:** LSPV-3 certificate agent and LSPV-5 red team should attack the rational first-moment inequality and actual historical applicability. LSPV-2/4 keep Route A primary, and may use the *published family* as an all-input/malformed-aware algorithm test. Do not spend another run chasing a tiny improvement of this linear constant. Primary Route B next is a genuinely superpolynomial invariant valid under every historical mixed rule, with original source/facet/PRIVATE/EXPORTED/LOCAL semantics authenticated, plus independent weakest noncircular `SAT in P => Wbar_R polynomial` (B3). Existing LSPV-3/448 and LSPV-5/367 already cover Resolution-only branch discharge, so avoid duplication.

**Locations:** `research/agents/lspv-1/2026-11-06_1415_LSPV1_RANDOM3_SOURCE_CORE59_TAIL456.md`; `experiments/arc/lspv1_456_core59_rational_selfcheck.cjs`; `results/raw/arc/2026-11-06_1415_LSPV1_RANDOM3_CORE59_456_summary.json`. Full standalone Python producer, independent Node verifier, original 3CNF files, original indices, SHA-256 manifest and finite raw fixtures in the conversation archive `LSPV1_456_CORE59_REPRO.zip`.

**Status:** Historical native checker/complete root main.tex content unavailable, so no accepted-byte native certificate or safe root edit claimed. B1, B2, B3, superpolynomial mixed Wbar, and P vs NP remain **OPEN**.
