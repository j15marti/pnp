# ONEWAY-REORDER-BUFFER18 (:00 MCSP role, hourly check-in run)
Timestamp: 2026-10-20 ~16:00 KST. **P versus NP remains OPEN.** Nothing here is a lower bound for unrestricted computation.

## Repo check
origin/main = ca1d9add (15:34 KST, ARC materialization gate audit). No newer commits on any branch. Newest peer artifacts: ACCESS-MODEL-COMPOSITION17 (14:48), REDTEAM35 (15:01, randomized INDEX synopsis bound), UNIVERSAL_CERT_CAP2 summary (15:10), ARC materialization gate (15:34). Root `main.tex` still reported placeholder-bearing by ACCESS17; not touched here.

## Question (ACCESS17 :00 target)
Is a SAT-derived MKTP/MCSP target stream *order-compatible* with a one-way source (CHMY model), or is some coordinate necessarily requested after its source position has passed?

## Lemma (PROVED, elementary, restricted model)
Model: deterministic, one read-once pass over x in {0,1}^N; output y_1..y_N in order, y_i = x_{pi(i)}; y_i may be emitted only once x_{pi(i)} has been read. Let M(i)=max_{j<=i} pi(j), e(t)=|{i: M(i)<=t}|. Then exact minimal memory (up to O(log N) counters) is
`B(pi) = max_t |{ j > e(t) : pi(j) <= t }|`.
*Lower:* at time t the retained bits x_{pi(j)} (j>e(t), pi(j)<=t) are independent free bits; any two distinct values must be distinguished by a later output, so 2^B states are needed (fooling set). *Upper:* emit y_i at time M(i) and keep only still-needed bits.
Consequences: identity B=0; block-reversal of window w has B=w-1; **bit-reversal and matrix transposition on N=m^2 bits have B=(sqrt N -1)^2 = N-O(sqrt N)** — linear.

## Executable check (COMPUTATIONAL)
`experiments/review/2026-10-20_oneway_reorder_buffer_audit.py` (runtime < 30 s, single stage) -> `results/raw/mcsp/2026-10-20_oneway_reorder_buffer.json`. 5,913 assertions, zero failures: closed form agrees with an independent state simulation on all permutations of N<=7 and on window/bit-reversal/transpose cases (bit-reversal N=1024: 961=31^2; transpose 32x32: 961).

## Interpretation / firewall
- A one-way MCSP route needs R_k's target-bit dependency map to have small B (local window w = p^{O(1)} suffices for the ordinary-query model; nothing in MMW forces more). Any construction whose target bit i reads a far-earlier source coordinate with Theta(N) crossings is *retired* for CHMY unless replay is charged (consistent with ACCESS17 synopsis bound and REDTEAM35).
- This does NOT show SAT->MKTP reductions must be non-local: it only turns "order-compatible" into a checkable criterion B(pi)=N^{o(1)}. Whether a correct both-promise R_k with such a dependency map exists is OPEN. Duplicate caution: the linear-synopsis consequence for post-pass replay is already in ACCESS17; the new item is the exact in-order permutation memory formula.
- Transfer class (external analogy, VLSI/streaming): ANALOGY — corner-turn/transposition buffers in signal processing have the same sqrt-N^2 buffer; not a complexity theorem.

## Next falsifier for :36
Exhibit a *correct* SAT-to-ordinary-MKTP target whose dependency map on the SAT source has B>=N^{Omega(1)}, or show every correct generator can be re-sequenced to B=N^{o(1)}.
