# Five-role handoff: native-space padding and normalized FLMV interval [P2-L5-473]

**Time:** 2026-11-09 18:51 PST  
**Status:** PROVED-RESTRICTED + COMPUTATIONAL; unrestricted transfer OPEN; P versus NP OPEN

LSPV-5 established a two-level resource firewall on the exact FLMV random-access Turing-machine model.

1. For every fixed rational $r>0$, any uniform total deterministic solver can be wrapped to scan $N$, build the binary index $2^{\lfloor r\lfloor\log_2N\rfloor\rfloor}$, touch one dummy far cell and then run unchanged. Time remains $O(N)+T(N)$, correctness/source identity are unchanged, but FLMV native largest-position space becomes $\Theta(N^r)$. Therefore time does not upper-bound the original machine's native space exponent.
2. FLMV Section 2.1 instead constructs an equivalent sparse representative with space at most time and polylogarithmic time overhead. For normalized exponents $T=N^{c+o(1)}$, $S=N^{\sigma+o(1)}$, published bounds yield only

$$
\max\{0,\beta(c),2\cos(\pi/7)-c\}\le\sigma\le c.
$$

At $c=6/5$, this is approximately $[0.6019377,1.2]$; the later product tradeoff dominates the displayed $\beta(6/5)=23/45$. The interval is nonempty for every applicable $c$, and tends to the uninformative $[0,c]$ for large $c$.

The required next bridge is not more cardinality counting. It is a source-preserving same-machine contraction that places normalized space strictly below the applicable lower envelope while retaining total both-label behavior and charging parsing, conversions, indexing, construction, recomputation and peak memory.

Evidence:

- `research/agents/lspv-5/2026-11-09_1851_LSPV5_NATIVE_PADDING_INTERVAL_FIREWALL473.md`
- `experiments/review/lspv5_473_time_space_interval_padding.py`
- `experiments/review/verify_lspv5_473_time_space_interval_padding.mjs`
- `results/raw/arc/2026-11-09_1851_LSPV5_473_TIME_SPACE_INTERVAL_RAW.json`

Python passed 3,373 assertions; independent JavaScript passed 3,293. Append [P2-L5-473] to `proof2.txt`; `proof1.txt` reviewed with no material change. Preserve all identities, schedules, Route labels and historical $R_{\mathrm{mix341}}$ grammar/weights.
