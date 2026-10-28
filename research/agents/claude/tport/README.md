# T-PORT: time–space lower bounds for SAT portfolios (CLAUDE TPORT-0001)

Added 2026-10-28 at the user's request. Reference/research artifact; changes no schedules, allocations or ownership. **P versus NP remains OPEN.**

Report: `research/agents/claude/2026-10-28_1326_CLAUDE_TPORT-0001.tex`.

## Question

Does `SAT ∉ ∃^{d log N + b0} DTISP[N^c, N^{o(1)}]` hold for some c > 1? That is a portfolio of about N^d small-space programs, one of which must accept each satisfiable formula. The UWI portfolio has **d = 1**.

## Results

| Result | Status |
|---|---|
| Barrier: in the alternation-trading system S (Williams' Speedup Rules 1 and 2, portfolio slowdown leaving a residual of width d·M, free absorption, brute force), no proof refutes the assumption when c ≥ 1 and c + d ≥ 2. At d = 1 nothing beyond the trivial c < 1. At d = 0 this is Williams' quadratic barrier. | PROVED/EXACT |
| Same barrier with Skolemization added | COMPUTATIONAL (0 of 47,938 proofs of length ≤ 18 beat c = 1); proof OPEN |
| For d < 1: SAT ∉ ∃^{d log N}DTISP[N^c, N^{o(1)}] whenever c(c+d) < 2 | PROVED/EXACT |
| Better computer-found bounds, e.g. (d, c) = (9/10, 21/20), (3/4, 57/50), (1/2, 261/200) | PROVED/EXACT (exact rational replay) |
| T-PORT through alternation trading | FALSIFIED/RETIRED for S |
| Asymptotics (TPORT-0002): 1 + (1−d)/3 ≤ c*(d) ≤ 1 + (1−d) on [0,1], and c*(1−ε) ≥ 1 + (29/50)ε for small ε; exact cost match for one speedup round trip | PROVED/EXACT (slope 29/50 by exact ε-polynomial certificate) |

## Files

| File | Purpose |
|---|---|
| `atp.py` | Rule engine and LP per proof string (ops S, T, K, D, B). `python atp.py` reruns Williams' checkpoints √2 and 1.6004. |
| `search.py` | Exhaustive search over proof strings, chunked (`--chunk i --nchunks k`). |
| `curve.py` | Best c versus d. |
| `verify_exact.py` | Exact Fraction replay with the real input length; strict final inequality. |
| `asymptotic_certify.py` | Exact certificate (polynomials in ε, lexicographic order) that a proof works at c = 1 + gε, d = 1 − ε for all small ε. |
| `potential_check.py` | Randomized monotonicity tests of the barrier potential (and of two failed Skolem-aware variants). |
| `*.jsonl`, `*_results.json` | Raw outputs cited in the report. |

Each invocation runs in under about 25 seconds; larger searches are split by index modulo the chunk count.
