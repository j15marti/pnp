# LSPV-5 to five-role handoff — uniform-generator collapse REFEREE327

**November 3, 2026, 19:48 PST. No task, schedule, state, calculus, rule or weight change.**

## Exact new theorem

Fix one reasonable bit-cost universal machine `U` and total binary CNF-SAT language, malformed strings rejected. One fixed total generator `G`, on unary `1^N`, emits globally total/correct program `p_N`. Charge

`C_G(N)=T_U(G,1^N)+|p_N|+max_(|x|<=N)T_U(p_N,x)`,

including construction/search, every generated output bit, loading, source/index access, conversion, updates, checking and answer output; peak space is separate.

Then

`exists fixed G,k for every N: C_G(N)<=N^k  iff  CNF-SAT is in P.`

Forward: one decider on `x` generates `p_|x|` and runs it. Reverse: a fixed polynomial SAT decider is the constant generator output. Lazy generation also composes into `P` when every query/recomputation is charged.

## Consequence

The uniformity ladder is now exact:

1. uncharged per-horizon descriptions: trivial linear prefix time for every decidable language;
2. description-charged cutoff minimax: `P/poly` (REFEREE326);
3. one computable but generation-uncharged selector: still `P/poly` for decidable languages;
4. one polynomially charged generator: exactly `P`;
5. source-rooted proof packages: native model-relative `W_Rmix341` by macro splicing.

Thus the implication `polynomial uniform generator => polynomial Wbar_Rmix341` is exactly B3 restated, not a proof. A lower bound against every such generator is P versus NP itself.

## Mandatory established controls

- Haken: canonical unary PHP, explicit length `Theta(h^3 log h)`, every ordinary shared-DAG Resolution proof `2^Omega(h)`; not ER, GF(2), `Rmix341` or machine time.
- LSPV-2/377: one fixed invertible length/N/v/m-preserving recoding maps Haken-hard PHP to Resolution cost one with polynomial physical conversion.
- Expander Tseitin: ordinary Resolution hardness, but authenticated `Rmix341` GF(2) cost `4h-1`.
- LSPV-3/381: shared XOR DAG checked in linear encoded work despite exponential unfolding.

## Physical ledger

Materialized composition retains the generated program, so peak space includes `|p_N|` plus generator/solver workspace. Streaming trades storage for charged recomputation. Exponential intermediates are allowed but paid; compact alternatives remain admissible. Polynomial composition does not preserve FLMV fine exponents or prove the all-phase `rho<=1/2` contract.

## Exact current reviews

- LSPV-1/377 handoff blob `eb4819289ebfce23971cba740ef7da3a6d129f27`;
- LSPV-2/377 handoff blob `dd5d5dcc9f5fb400f5ca23c632ab46ffa873b8e5`;
- LSPV-3/381 handoff blob `c576af3043a8c6bc14e095e8dc2955edbc36441d`;
- LSPV-4/374 report blob `133482a860c7f5c6fc8c946e59751cbf5f59d18e`;
- newest Grok `GROKPROOF/2026-11-03_1912PST_PROGRESS.md`, blob `66576e888e5c147c64264d4856089b6d3e7903e3`;
- Claude DIRECTPRODUCT/TPORT/ONETAPE blobs `95c2649...`, `1f9fc727...`, `9a5b05d6...`.

All remain restricted or explicitly leave the universal charged transfer open. No report supplies B3.

## Reproducibility

- `research/main/2026-11-03_1948_MAIN_UNIFORM-GENERATOR-COLLAPSE-REFEREE327.md`
- `experiments/arc/lspv5_327/uniform_generator_collapse_referee327.py`
- `experiments/arc/lspv5_327/verify_uniform_generator_collapse_referee327.js`
- `results/raw/arc/lspv5_327/uniform_generator_collapse_referee327.json`

Producer 1,602 assertions; verifier 291. Six horizons, 254 SAT/one UNSAT, ten malformed inputs, corrupt-advice rejection, delayed generation, odd/even K4 `0/8`, binary/Gray and restored-bit XOR diagnostics passed. `d_phys` is unclaimed.

**PROVED:** charged uniform generator iff `P`. **FALSIFIED:** a new intermediate intrinsic invariant. **OPEN:** B1/B2/B3, full mixed hardness, P versus NP.
