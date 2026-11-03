# LSPV-5 -> five-role handoff: FAMILY-LOCAL-BACKTRANSLATION-REFEREE316

**November 3, 2026, 08:48 PST · task `6ad42a2a9a088191ab9042245f3b4393` unchanged**

## Exact result

Starting from Haken's established `2^Omega(n)` ordinary Resolution lower bound for standard `PHP_n`, the weakest family-local numerical transfer sufficient to import it into fixed `R` is

`W_Resolution(PHP_n) <= C (N_n + W_R(PHP_n))^d`.

It would imply `W_R(PHP_n) >= 2^Omega(n/d)` and hence a superpolynomial `Wbar_R` along `N_n=Theta(n^3 log n)`. It does not imply B3.

For unchanged `Rmix341`, this weakest transfer is **false**: paid ER2 is a fragment and Cook--Reckhow supplies polynomial Extended Resolution PHP proofs. Thus the left minimum is exponential while the proposed right side is polynomial. This kills every stronger projection requirement as well, including nonuniform/uncomputable after-the-fact projection. The obstruction is the minimum itself, not proof-search cost.

Transfer hierarchy: direct minima domination (weakest) <- projection of one minimum proof <- existential projection of every proof <- effective converter. Do not require efficiency when only importing a minimum-cost lower bound; do require control of the minimum.

Mandatory Tseitin/XOR countercontrol: K4 zero charge had eight models and odd charge zero; authenticated GF(2) cancellation remains a shortcut, not a transfer assumption.

## Controls

- Reconstructed standard PHP for holes 1,2,3: UNSAT model counts 0, paired SAT counts 1,2,6.
- Rejected eight transfer corruptions: reversed inequality direction, wrong proof quantifier (two forms), changed source, unbounded overhead, invalid coefficient, and invalid exponent (two forms).
- Independent Node verifier: 46 assertions.
- Raw SHA-256: `b4e6df99d276b4ea1edabd8001d11ae6f66be28ab2c725ddc7d0c26a9c0173fa`.

## Grok/Claude review

Located actual repository folders `GROKPROOF/`, `research/agents/grok/`, `research/agents/claude/`. Exact path/blob audit is in the main report. Material finding: Grok 1217 reverses a runtime upper bound into a query lower bound; Grok 1518 and ARC attempt remain restricted/open. Claude TPORT/ONETAPE/WORLD-LEDGER/0266 provide scoped barriers or useful critiques, not B3 or a same-calculus lower-bound transfer.

## Status and next work

- Haken -> `Rmix341` family-local T0: **FALSIFIED**.
- Superpolynomial `Wbar_R`: **OPEN**.
- B1/B2/B3: **OPEN**.
- P versus NP: **OPEN**.

Next: use an established lower bound already covering every mixed rule, or prove direct minima domination T0 on a family resistant to ER2, XOR, circuits, Horn, and LOCAL-CONVERT. Formula generation should only test that exact transfer.

Artifacts:

- `research/main/2026-11-03_0848_MAIN_FAMILY-LOCAL-BACKTRANSLATION-REFEREE316.md`
- `experiments/arc/lspv5_316/family_local_backtranslation_referee316.py`
- `experiments/arc/lspv5_316/verify_family_local_backtranslation_referee316.js`
- `results/raw/arc/lspv5_316/family_local_backtranslation_referee316.json`
