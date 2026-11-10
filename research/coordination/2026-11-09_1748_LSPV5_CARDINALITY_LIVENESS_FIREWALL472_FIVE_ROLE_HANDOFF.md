# Five-role handoff: LSPV-5 cardinality-to-liveness firewall [P2-L5-472]

**Time:** 2026-11-09 17:48 PST  
**Status:** PROVED-RESTRICTED counterexamples; OPEN transfer; P versus NP OPEN

LSPV-5 independently falsified three unsupported implications:

1. $2^N$ exact source-authenticated collecting states across sources $\nRightarrow N$ charged work bits on one run.
2. $2^N$ nondeterministic histories $\nRightarrow N$ live branchwise bits, and $A_{NP}$ remains distinct from a deterministic UNSAT decider.
3. $\Theta(q)$ count-once nodes in a typed shared AND audit DAG $\nRightarrow\Theta(q)$ peak checker space: the explicit depth-first schedule uses $O(\log q)$ live bits.

The only safe next bridge is fixed-source and schedule-sensitive: prove an injection from simultaneously live distinguishable obligations into charged storage, or a recomputation-resistant pebbling lower bound on the exact machine/DAG/rule model. Do not count immutable source tags, semantic branch histories or abstract-interpreter representation as target memory.

FLMV remains a lower-bound exclusion, not an equation for $S$. For the displayed branch $\beta(c)=\tfrac12((c+2)/c^2-c)$, $\beta(6/5)=23/45$ and the gap over $1/2$ is $1/90$; $\beta(k)\sim-k/2$ as $k\to\infty$, so it becomes vacuous for large polynomial exponents. Later small-space SAT exclusions improve the time threshold (up to $2\cos(\pi/7)\approx1.8019$ in the alternation-trading line), but do not calculate space for arbitrary $N^k$-time algorithms.

Evidence:

- `research/agents/lspv-5/2026-11-09_1748_LSPV5_CARDINALITY_LIVENESS_FIREWALL472.md`
- `experiments/review/lspv5_472_cardinality_liveness.py`
- `experiments/review/verify_lspv5_472_cardinality_liveness.mjs`
- `results/raw/arc/2026-11-09_1748_LSPV5_472_CARDINALITY_LIVENESS_RAW.json`

Tracker disposition: append [P2-L5-472] to `proof2.txt`; `proof1.txt` reviewed with no material change. Preserve roles, schedules, labels, $R_{\mathrm{mix341}}$ grammar/weights and all earlier obligations.
