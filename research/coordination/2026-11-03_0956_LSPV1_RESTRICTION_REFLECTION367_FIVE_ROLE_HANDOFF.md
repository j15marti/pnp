# LSPV-1 367 to five existing specialists
November 3, 2026, 09:56 PST. Same task, same fully fixed Rmix341, same schedule, no role change.

**Established theorem first:** Urquhart (1987) and Ben-Sasson/Wigderson (2001) imply expander odd-Tseitin strict 3-CNF has ordinary DAG-Resolution complexity $2^{\Omega(h)}$ for h-vertex cubic expanders. That same original formula has the previously certified Rmix341 proof cost $4h-1$ using GF(2). Therefore it cannot seed a full-mixed hardness claim without a valid reverse transfer.

**New scoped theorem, PROVED/EXACT in ordinary Resolution:** For any fixed total correct A and clock b, form the witness-transparent source CNF H_{A,v,m,b}: one-hot source selector on the $8\binom v3$ proper signed 3-clauses at each of m slots, guarded **original** clauses $(\neg s_{j,C}\lor C(y))$, and a paid-bits deterministic clocked rejecting tableau with wires disjoint from witness y. When A rejects a selected F in b steps, assigning all selector and deterministic trace wires leaves *literally the original F* as the residual. Strict Resolution DAG restrictions cost no additional inference nodes. Hence

$$
W_{\mathrm{Res}}(H_{A,v,m,b})\ge\max_{F:\ A(F)=\mathrm{UNSAT}\text{ by }b} W_{\mathrm{Res}}(F).
$$

One fixed correct Tseitin-recognizer with exhaustive fallback runs in polynomial time on the published hard family, so its clocked H source has polynomial encoded size but exponential strict Resolution complexity. This is **NOT** an all-rule Rmix lower bound, B1, B2, B3 or SAT decision-time result. The older LSPV-1 361 conditional ER2 universal-reflection specialization is a different direction. LSPV-5 317 Cook--Reckhow B3 equivalence remains OPEN as a same-fixed-R length simulation.

**Falsifiers:** witness-dependent evaluator gates break literal source identity; one-hot scope covers strict width-three, not arbitrary-width CNF; the known 4h-1 XOR proof destroys simple restricted-to-mixed hardness; a rejecting trace alone never proves machine soundness. Test any candidate all-rule cost transfer against ALL four.

**COMPUTATIONAL:** standalone V8 producer 120 assertions, separately authored V8 verifier 121 assertions. Odd/even K4 0/8 models, 16 deletion SAT, 48 sign-flip SAT, 160 templates x 16 slots = 2560 guarded clauses and exact syntactic specialization, four malformed source fixtures and three bad-pivot controls. No new finite optimum or expander asymptotic is inferred.

**External folders actually reviewed:** `GROKPROOF/2026-11-03_1518_PROGRESS.md` blob 234fc189, `GROKPROOF/2026-11-03_1217_PROGRESS.md` blob acf9fbee, `research/agents/grok/2026-10-23_1915_GROK_REWIRE.tex` blob d06a2d56, `research/agents/claude/2026-09-30_CLAUDE-0266_review.tex` blob 694c1c81, `research/agents/claude/2026-10-28_0924_CLAUDE_WORLD-LEDGER-0001.tex` blob 79e4d4e7. Grok's per-call lower-bound-from-upper-runtime flaw and Claude's AI=1 iff affine flaw are corroborated. None resolves B3.

**Exact outbox:**
- `research/agents/lspv-1/2026-11-03_0956_LSPV-1_RESTRICTION_STABLE_REFLECTION367.tex`
- `experiments/arc/lspv1_367_restriction_selector_controls.js`
- `experiments/arc/lspv1_367_independent_verify.js`
- `results/raw/arc/2026-11-03_0956_LSPV1_RESTRICTION_REFLECTION367.json`
- `research/coordination/2026-11-03_0956_LSPV1_RESTRICTION_REFLECTION367_FIVE_ROLE_HANDOFF.md`

**Allocation:** LSPV-2 audit source selector and fully fixed LOCAL-CONVERT typing; LSPV-3 hunt any published hard system with all-rule backward simulation; LSPV-4 preserve logical nodes/proof bytes/optimizer/runtime distinctions; LSPV-5 red-team 367 (especially witness wires and strict-RES restriction) and independently pursue B3. LSPV-1 remains responsible for weakest B3 from SAT in P, with no gratuitous assumption of bounded-arithmetic soundness.

**Next precise gap:** polynomial loss-free source- or proof-specialization for every charged rule of Rmix341, or a valid nonrelativizing bridge B3 for the same fixed system. No new hard formula has been claimed. P versus NP OPEN.
