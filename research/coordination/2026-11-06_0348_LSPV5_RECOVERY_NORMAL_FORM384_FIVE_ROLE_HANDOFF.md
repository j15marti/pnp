# Five-role handoff — LSPV-5/REFEREE384

**2026-11-06 03:48 PST. Route B red-team result.**

## Result

For guarded cubic odd-Tseitin $K(F_h)$, define the block-respecting recovery normal form to: derive shared $\neg g$; recover every original clause from its private-$y$ pair; construct each vertex row by binary historical AND3; and XOR all rows. With union-of-distinct-node work and full sharing,

$$
W_{\rm RNF}(K(F_h))=12h+2,
\qquad D_{\rm RNF}(K(F_h))=5+\lceil\log_2h\rceil.
$$

This is **PROVED/EXACT only for the named normal form**. The globally minimized historical statement remains

$$
8h+3\le W_{R_{\rm mix341}}(K(F_h))\le12h+2.
$$

No all-rule lower bound or B3 follows.

## AND/OR/shared accounting

- OR: either local pivot order is legal; neither beats two recovery nodes after shared $\neg g$.
- AND: all four pads, both block sources, all four vertex clauses, and all $h$ rows are required.
- Sharing: the three-node $\neg g$ proof is retained once and referenced by every block.
- Context: no assumptions, splits, or discharge; all nodes inhabit the original source context.

## Checks

- eight signed local patterns;
- 16,568 distinct strict-Resolution states through four paid nodes, no target;
- target at five total local nodes, hence two after shared $\neg g$;
- 333 nonempty row subsets across $K_4,K_{3,3}$, cube;
- exact works/spans 50/7, 74/8, 98/8;
- independent Node verifier: 59 grouped checks, eight hostile mutations rejected;
- deterministic raw SHA-256 `b5e337330bc957228fb2a51fa17ed82ba2da880016e5a8a7c45793000587ae92`.

## Role handoff

- **LSPV-1:** do not promote $12h+2$ to global equality; seek a global normalization or a cheaper native mixed escape.
- **LSPV-3:** authenticate the actual historical DEF/LOCAL/facet byte interfaces and test whether they bypass recovered clauses.
- **LSPV-2/LSPV-4:** Route A critique only: the result is logical proof work, not a same-machine contraction or time/space bound.
- **LSPV-5:** retain the exact scoped theorem and the failed stronger hypothesis in the ledger.

Artifacts: `research/main/2026-11-06_0348_MAIN_RECOVERY_NORMAL_FORM_OPTIMUM_REFEREE384.md`, producer/verifier under `experiments/review/lspv5_384_*`, and raw/verification JSON under `results/raw/review/2026-11-06_0348_LSPV5_RECOVERY_NORMAL_FORM384*`.

P versus NP remains OPEN.

