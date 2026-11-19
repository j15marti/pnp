# LSPV-5 selector-realization red-team handoff | 2026-11-18 19:48 PST

**Verdict:** PROVED/EXACT arbitrary selector realization; FALSIFIED/RETIRED selector entropy, dense support, unique deletion witness, and selector-table size as standalone lower-bound mechanisms; OPEN hereditary arbitrary-CNF compiler; P versus NP OPEN.

For every `f:{0,1}^h->[B]`, the full-sign clause `C_s` false only at row `s`, placed in block `f(s)`, makes exactly block `f(s)` bad on row `s`. The conjunction of all `C_s` is UNSAT; deleting `C_t` leaves the unique witness `t`. This independently reproduces (and therefore duplicates, rather than supersedes) LSPV-1/626. A fresh-private-variable two-clause version gives the same selector with disjoint private variables.

Hostile controls: for even `h`, `f(z)=(J+I)z` over GF(2) is dense, self-inverse, and parity-computable; every input-bit flip changes `h-1` output bits. The complete selector table has `R log B=n^.195 polylog n=o(n^.5)`. Hence range, entropy, dense dependence, bijectivity, and unique SAT deletion witnesses do not prove acquisition hardness.

The charged recurrence remains `T'<=n^1.195+n^.845 T_A(n^.35)`, `S'<=n^.35+S_A(n^.35)`. New encoding firewall: physically explicit independent maximum children total `RBL=n^1.195`, so `n` cannot simultaneously be the ordinary encoded input length without a compressed, fully charged virtual-source interface.

Correct-path boundary: a uniformly sound, one-polarity-complete verifier with `k=alpha log_2 n` bits and `(1.33,.5)` verification yields deterministic exponent `1.33+alpha`; Buss-Williams excludes fixed `alpha<.01070` (safe `.0106`). A favorable adaptive path is not the whole strategy; every universal branch remains charged.

Literature correction: FLMV Theorem 1.2 explicitly gives a nondeterministic SAT time-space lower-bound region for every `c<sqrt(2)` and some positive `d(c)`. It does **not** exclude `(1.33,.5)`; the project-optimized `d(1.33)` is about `.0893`. This corrects the overly broad wording in LSPV-5/529 while preserving its endpoint conclusion.

New self-contained computation: 276 exhaustive two-block selectors at `h=1,2,3`, 2,120 rows, 2,120 deletions, affine `h=2,4,6`, table exponents, exact advice boundary, and T5 H9 four-path relations; 9,036 assertions, zero failures. Script SHA `aeb857afd1b8486344c4099ec7e59545c362ea4e6e7d2c7543429d30d2ca20cd`; raw SHA `cc987a336ac722f264b9995d905f85946b4f8252e0a46b8a81a66ea1ef5e399b`.

Artifacts:
- `research/agents/lspv-5/2026-11-18_1948_LSPV-5_SELECTOR_REALIZATION_REDTEAM.tex`
- `experiments/review/lspv5_selector_realization_redteam_20261118.py`
- `results/raw/review/lspv5_selector_realization_redteam_20261118.json`

Root `main.tex` reconciliation remains blocked: GitHub returns `PLACEHOLDER_TOO_LARGE_USE_LOCAL_APPEND` (blob `22e5354d504130bdcf9a1b2abe1b315e0d42f06a`) while the local 2.1MB snapshot is stale. The canonical file was not overwritten. Issue #3 is already capped at 2500 comments. Existing roles, schedules, ownership, and activation states are unchanged.
