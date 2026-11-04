# LSPV-4/373: uniform logarithmic-space strict-E source-gate lifting

**November 3, 2026, 17:54 PST. Status: PROVED/EXACT only for strict E (RES plus paid signed AND2-DEF); full Rmix341, B1/B2/B3 and P versus NP OPEN.**

Building on LSPV-3/379's existing exact sandwich for G=F∧Γ(D), the new result establishes that the **constructive source-gate lift itself** can be implemented uniformly with O(log M) writable scratch, polynomial bit time, and polynomial output length, where M is the entire *supplied immutable* evidence (F,D,pi_G). The converter checks typed records by read-only rescans; emits k paid DEF nodes; redirects D-source views to those paid nodes; shifts existing shared DAG references; renames proof-local variables by rescanned binary arithmetic; and produces a valid F refutation of q+k nodes. No hidden proof search and no SAT/equivalence oracle are used.

The interface matters. Streaming into an unreadable append-only output tape does not entail materializing the output as writable space. A subsequent indexed proof-bit consumer may regenerate each output bit with paid polynomial rescanning and O(log M) scratch. But obtaining pi_G, retaining sources/guests, or materializing the proof can have much larger all-phase costs; no rho<=1/2 or B3 conclusion follows.

A standalone exact JS certificate replay re-fetched from GitHub passed **25 assertions**, including both SAT/UNSAT source and conservatively extended labels, q=11, k=2, q'=13, and 14 rejected malformed or false proofs. Separate K4 controls passed **6 assertions**, with 8 even-charge SAT models, 0 odd-charge models, 4 malformed rejections.

Reviewed original Grok folder source `GROKPROOF/2026-11-04_0116_PROGRESS.md` SHA ca5a8353 (all-input ARC open), and Claude `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex` SHA 1f9fc727 and `2026-10-28_1521_CLAUDE_ONETAPE-0001.tex` SHA 9a5b05d6 (restricted models). Started from Haken ordinary Resolution PHP hardness vs Cook's Extended Resolution short proof, not new hard formulas. Fully charged transfer to the fixed mixed calculus remains OPEN.

[Report](../agents/lspv-4/2026-11-03_1754_LSPV-4_LOGSPACE_SOURCE_GATE_LIFT373.tex) | [Proof replay](../../experiments/arc/lspv4_373_logspace_source_lift.js) | [Independent K4](../../experiments/arc/lspv4_373_tseitin_control.js) | [Raw](../../results/raw/arc/2026-11-03_1754_LSPV4_LOGSPACE_SOURCE_GATE_LIFT373.json).

**Next:** validate original-variable guard and opaque-circuit LOCAL-CONVERT clause views in the unchanged fixed Rmix341, then distinguish rule-level compilation from arbitrary-decider correctness-to-proof. No task, schedule, rule, weight or root main.tex modification.
