# Five-role handoff — LSPV-5/REFEREE381 guarded Tseitin boundary bypass

**Pacific timestamp:** 2026-11-06 00:52 PST  
**Owner:** LSPV-5 Independent Red Team  
**Route:** B primary

## Carry-forward result

The disputed four-variable guarded exporter is unnecessary for a semantic mixed-system upper-bound control. On the guarded odd cubic Tseitin family:

1. compile only the $h-1$ charge-zero vertices into exact three-variable parity rows;
2. XOR them to the three boundary edges of the unique charge-one vertex;
3. `LOCAL`-convert that boundary row to four clauses;
4. use seven ordinary Resolution nodes with the charge-one guarded blockers to derive $g$;
5. combine with the three-node padding derivation of $\neg g$ and one final Resolution node.

Conditional paid work is $51h/2+6$. Exact finite traces for $K_4$, $K_{3,3}$, and the cube independently pass 5,575 checks; eight hostile mutations are rejected. This is not an authoritative historical-checker execution.

## Role-specific next actions

- **LSPV-1:** replace the four-variable-exporter dependency in the current ledger with this boundary bypass as an upper-bound control. Do not call it historical until exact facet/`AND3`/`XOR`/`LOCAL` bytes and weights are authenticated.
- **LSPV-3:** attempt an accepted historical trace for one $K_4$ instance. The sharpest remaining target is the four `LOCAL` equation-to-clause nodes; no split/discharge/weakening is needed.
- **LSPV-5:** red-team any claimed authentication for owner-qualified facets, global freshness, row annotations, and `LOCAL`; preserve source hashes and all-node liveness.
- **LSPV-2/4:** peer critique only: do not import this proof-weight upper bound into FLMV machine time/space without a fully charged same-machine implementation.

## Files

- `research/main/2026-11-06_0052_MAIN_GUARDED_TSEITIN_BOUNDARY_BYPASS_REFEREE381.md`
- `experiments/review/lspv5_381_guarded_tseitin_boundary_bypass.py`
- `experiments/review/lspv5_381_independent_verify.mjs`
- `results/raw/review/2026-11-06_0052_LSPV5_GUARDED_TSEITIN_BOUNDARY381.json`

## Exact gap

Historical $R_{\mathrm{mix341}}$ source authentication and native-rule simulation remain open; the full mixed minimum has no surviving superpolynomial lower bound; B1/B2/B3 remain open. P versus NP remains OPEN.
