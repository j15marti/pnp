# LSPV-5 to five-role handoff — REFEREE326

**November 3, 2026, 18:48 PST. No task/schedule/calculus mutation.**

## New exact result

Fix a reasonable universal deterministic machine `U` and the total binary CNF-SAT language, rejecting malformed strings. Over programs globally total and correct on every binary string, define

`K_U(N)=min_p (|p|+max_(|x|<=N)T_U(p,x))`,

with parse, code/source access, construction, updates, verification and output charged. Then

`K_U(N)=N^O(1) for all N  iff  CNF-SAT is in P/poly.`

Program-to-circuit simulation gives `C_SAT(n)<=poly(n+K_U(n))`. Conversely, hardwire `C_0,...,C_N` into a program and use a fixed exhaustive fallback beyond `N`; the program remains globally correct and has polynomial prefix description/time.

The quantifier is `for every N there exists p_N`, not one fixed program. Description charge prevents a free exponentially long table but recovers nonuniform circuit complexity, not uniform P. A superpolynomial `K_U` lower bound would prove `NP not subseteq P/poly`, stronger than P versus NP.

## Trilemma

1. Per-source minimization collapses to `O(|F|)` by hardcoding `F`'s label plus a complete fallback.
2. Cutoff minimax with description charge is `P/poly`.
3. Source-rooted proof carrying returns to native `W_Rmix341` by macro splicing.

No present candidate is simultaneously source-intrinsic, all-representation/all-algorithm robust and weaker than circuit lower bounds. This is proved for these definitions, not a universal impossibility theorem.

## B bridges

No B1/B2/B3 result follows. In particular, the varying `p_N` cannot be substituted into the `A`-dependent polynomials in B1/B2. A uniform-in-program bridge

`Wbar_R(N)<=q(N+|p|+T_p^wc(N))`

for one fixed `q` would be a strictly stronger obligation and is OPEN. `SAT in P => K_U` polynomial, but `K_U` polynomial means only `SAT in P/poly`.

## Mandatory controls

- Haken: canonical unary PHP, ordinary unrestricted shared-DAG Resolution, `2^(Omega(h))` lines, `N_h=Theta(h^3 log h)`; not ER, `Rmix341` or machine time.
- Tseitin: ordinary Resolution hardness is defeated by compact GF(2); fixed mixed proof costs `4h-1`; expanded-row mass has a compact pointer DAG.
- Logical nodes do not equal physical time; payload, construction, access, checking, output and peak space remain separate.
- Exponential representations are allowed and charged; compact alternatives remain admissible.

## Exact current reviews

All five roles checked:

- `GROKPROOF/2026-11-04_0116_PROGRESS.md`, blob `ca5a835356eb918b8cb4ab94d14de6174edeab03`;
- Claude `DIRECTPRODUCT-0001`, blob `95c2649b29ae7efac79e9400effffd2c3bdeb2fc`;
- Claude `TPORT-0002`, blob `1f9fc727d3e2b009cba7afec2a93beb62959dd67`;
- Claude `ONETAPE-0001`, blob `9a5b05d6ec0d5580fffe4687b82b4e3dd227de4a`.

All are restricted or explicitly leave the fully charged transfer open; none supplies B3.

Current peer handoffs reviewed: LSPV-1/376 blob `05f10de...`, LSPV-2/376 blob `4e87561...`, LSPV-3/380 blob `8d7db5c...`, and LSPV-4/372 blob `43f2d2e...`.

## Reproducibility

- `experiments/arc/lspv5_326/description_time_minimax_referee326.py`
- `experiments/arc/lspv5_326/verify_description_time_minimax_referee326.js`
- `results/raw/arc/lspv5_326/description_time_minimax_referee326.json`
- `research/main/2026-11-03_1848_MAIN_DESCRIPTION-TIME-MINIMAX-POLY-CIRCUIT-REFEREE326.md`

Producer 281 assertions; independent verifier 277. Ten malformed records, 254 SAT/one UNSAT tiny controls, corrupted advice rejection, and K4 odd/even 0/8 controls passed. Offline advice-table XOR delta is one; no native `d_phys` is claimed.

**PROVED:** minimax/circuit equivalence. **FALSIFIED:** characterization of uniform P or automatic B3. **OPEN:** superpolynomial `Wbar_Rmix341`, B1/B2/B3, `NP not subseteq P/poly`, and P versus NP.
