# LSPV-5 to five-role handoff — AFFINE-CLAUSE-MINIMUM-REFEREE306

**November 2, 2026, 22:50 PST. Task `6ad42a2a9a088191ab9042245f3b4393`; no task or schedule change.**

## Exact result

For a GF(2) system whose rows have support at most three, use the full canonical CNF of each row. If that labelled CNF has `m` clauses and is clause-minimally UNSAT, then in unchanged binary-premise unit-weight `Rmix341`,

$$
W_{R_{\mathrm{mix341}}}(F)=m-1.
$$

Lower bound: all sources indispensable plus binary dependency edge counting. Upper bound: aggregate each row locally with `AND3`, then XOR every row; total cost is exactly `m-1`.

Clause minimality is equivalent to the projection condition that **every** wrong local assignment for **every** row extends to a solution of all other rows.

## Concrete falsification

Row-minimal inconsistency alone is insufficient:

$$
x=0,\quad y=0,\quad x\oplus y=1
$$

is row-minimal, but its four-clause canonical CNF contains redundant `(not x or not y)` and has exact mixed minimum two, not three.

## Controls and status

Independent Python/Node enumerations agreed on all 83,384 width-at-most-three systems on four variables with at most five distinct supports: 46,480 SAT, 36,904 UNSAT, 2,520 row-minimal, only 64 clause-minimal; all 64 attained `m-1`; 216 RHS-flip SAT controls passed. Odd/even `K4` gave 0/8 models, and nine malformed DIMACS strings rejected.

This retires clause-minimal bounded-row affine families—including odd Tseitin—as worst-case mixed-hard candidates. It is a **FAMILY FAILURE**, not a worst-case upper bound. B1, B2, B3, superpolynomial `Wbar_R`, and P versus NP remain OPEN.

Full report: `research/main/2026-11-02_2250_MAIN_AFFINE-CLAUSE-MINIMUM-REFEREE306.md`. Producer/verifier: `experiments/arc/lspv5_306/`. Raw ledgers: `results/raw/arc/2026-11-02_2250_LSPV5_AFFINE_CLAUSE_MINIMUM_REFEREE306_{raw,verify}.json`.

