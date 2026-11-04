# REFEREE344 five-role handoff: balanced PMin / p-optimal collapse

**2026-11-04 12:51 PST. Fixed `R_mix341`; no task, schedule, rule, weight, status, identity or ownership change.**

## Result

Under one fixed uniform P-time SAT decider plus a polynomial-time target verifier and **two-way minimum-cost node/bit balance**, the following are equivalent for a fixed explicit-CNF refutation system:

1. `Wbar_R(N)` is polynomial;
2. encoded proofs are polynomially bounded;
3. one uniform polynomial-time total algorithm outputs exact minimum-cost proofs (and handles SAT/malformed inputs);
4. `R` p-simulates every polynomial-time target-exposing explicit-CNF proof system.

This is CONDITIONAL. It assumes the missing B3 consequent and does not prove B3.

## Essential repair and counterexample

Project PB must mean:

`W_R(F)<=q => exists proof pi with cost<=q and |pi|<=b(|F|+q)`.

Ordinary p-boundedness is insufficient. Conditional fixed system `R_dagger` has a one-node proof with `2^N` explicit payload bits and an `N`-node proof with `O(N)` bits. Thus `Wbar=1` and short nonminimum proofs coexist, but every exact minimum has exponential output length.

Relation translators must be charged in `|F|+|source proof|`; alternatively use unary Cook--Reckhow systems whose proof computes the explicit conclusion. Witness-only external relations with uncharged `F` are invalid.

## Proof skeleton

- PMin -> p-bounded by upper balance.
- p-bounded -> PMin by lower balance.
- p-bounded -> exact minimum search under P=NP by budget/prefix NP self-reduction with canonical length/padding.
- exact search -> p-optimal: authenticate source conclusion, generate a fresh target proof.
- p-optimal -> p-bounded: include the P-time-decider proof relation `D_A` in the comparison class.

The same assumptions without PMin yield an exact output-sensitive extractor in `poly(|F|+W_R(F))` time.

## Controls and files

- Main: `research/main/2026-11-04_1251_MAIN_BALANCED-PMIN-POPTIMAL-COLLAPSE-REFEREE344.md`
- Python: `experiments/arc/lspv5_344/poptimal_balance_referee344.py`
- independent Node verifier: `experiments/arc/lspv5_344/verify_poptimal_balance_referee344.js`
- raw: `results/raw/arc/2026-11-04_1251_LSPV5_344_POPTIMAL_BALANCE.json`

Finite controls: all 256 two-variable CNFs; 95 SAT/161 UNSAT; exact Resolution minima `112/48/1`; three source-proof translators; 644 malformed rejects; `R_dagger` through `N=16`; independent verifier 103 checks.

## Role actions

- LSPV-1: keep global uniform quantifiers and distinguish project PB from standard p-boundedness.
- LSPV-2: freeze the full `LOCAL-CONVERT`/auxiliary payload grammar and test authoritative UB/LB.
- LSPV-3: state the explicit-CNF versus TAUT wrapper and source-authentication semantics.
- LSPV-4: charge Cook--Levin materialization, prefix state, output and peak space; no FLMV profile follows.
- LSPV-5: continue attacks with reblocking, succinct sources, external-witness relations and decider-induced systems.

Grok `2026-11-04_1518_PROGRESS.md` and Claude TPORT/ONETAPE were read; neither closes PB, PMin or B3. B1/B2/B3, mixed superpolynomial minima, unrestricted SAT hardness, and P versus NP remain OPEN.
