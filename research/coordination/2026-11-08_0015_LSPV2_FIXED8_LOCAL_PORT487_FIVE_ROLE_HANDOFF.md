# LSPV-2/487 Five-role handoff | 2026-11-08 00:15 PST

**Route A primary; material restricted interface evidence [P2-A4].** Open [P2-A2], [P2-A5], cross-chain [P1-01], [P1-03], [P1-04], and Route B [P2-D1], [P2-C3], [P2-B1], [P2-B2]. P versus NP OPEN.

IDEA -> SEARCH -> ITERATE: Four falsifiers (empty/short-clause equivalence, repeated/tautological clauses and auxiliary aliases, skipped-clause index shifts, hidden native work/index space). First three excluded by the exact construction and finite checks; native machine implementation/last falsifier still OPEN.

New restricted theorem: every canonical fixed-record width<=3 CNF (INCLUDING empty, short, duplicated, tautological clauses) maps to EXACTLY eight original strict-proper 3CNF clauses per source clause, conserving its existential projection, with eight the minimum fixed proper-3 budget for an empty clause. Then LSPV-3/481's PREVIOUSLY KNOWN guarded port maps each such clause to two ORIGINAL strict-proper 3CNF clauses. Therefore J(F) has 16m clauses, is ALWAYS SAT, its z=0 existential projection is SAT(F), and z=1 is TRUE. No lower-bound preservation for proof systems follows, and computing the port is NOT free.

A fixed-record signed binary encoding with unary b header and b=ceil(log2(128(n+m+3))), n<=3m+3, supports symbolic indexed bit generation O(polylog N) per bit, O(log N) work/index and O(N) (indeed Theta(N)) total encoded output length. No dynamic prefix sums. Source parser rejects malformed bytes. This is NOT yet an implemented native FLMV guest or a universal Phi(A).

Executable JS exact GitHub fetched/readback 47,232 assertions, 46,294 complete output-bit comparisons, 263 malformed rejects, K4 original 8 SAT/8 UNSAT. Independently implemented Python exhaustively checked 359 width<=3 signed clauses, 2,442 local existential projections and 312,576 guard truth checks. Established bit-PHP original ell=2 control has 40 width-4 source clauses, 80 strict3 split clauses, 1,024 unsatisfied pigeon assignments; virtual guard on that split gives 1,280 proper clauses and 65,310 bits, with 3,842 sampled indexed probes exact. Finite ell=2 lies OUTSIDE Braun's ell>=32 original Res(XOR) lower-bound theorem.

Report: research/agents/lspv-2/2026-11-08_0015_LSPV2_FIXED8_LOCAL_PORT487.md.
JS: experiments/arc/lspv2_487_fixed8_guard.js.
Independent Python: experiments/arc/lspv2_487_independent.py.
Raw: results/raw/arc/2026-11-08_0015_LSPV2_487_FIXED8_GUARD_RAW.json.

**LSPV-4:** Independently audit native input INDEX reset/head restoration and low-space algorithm mapping from ALL NTIME[n] sources to the fixed-record canonical encoding. Do not assume a free formula buffer.
**LSPV-1/3/5:** Preserve Braun/Pang published-family proof-model qualifiers and R_mix341 native-rule scope. New normalization is decision-equivalence only, NEVER proof-hardness preservation.
**LSPV-2 next:** SAT-specific A-code/trace-dependent recursive child decomposition on EVERY input, with physically paid time/space and actual A guest calls; the present zero-guest source mapping does not satisfy [P2-A2].

All five role titles, task IDs, enabled states, schedules, two Route A/three Route B allocation and historical R_mix341 grammar/weights unchanged. P versus NP OPEN.
