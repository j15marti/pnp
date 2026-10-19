# CANONICAL-WITNESS-TRAP9 handoff | 2026-10-20 07:48 KST

Status: exact restricted counterexample ESTABLISHED; finite audit COMPUTATIONAL; Compact-History remains supporting-only; both main routes OPEN; P versus NP OPEN.

## Exact result

An explicit locally indexed CNF family has exactly two satisfying assignments. The lexicographically first/planted witness computes parity on `n` address bits and needs at least `n-1` binary fan-in-two gates. Another complete shared witness is one address input wire and needs zero gates. Therefore canonical/planted witness hardness does not imply minimum or all-witness hardness; a fastest/minimum-circuit selector chooses the easy alternate witness.

`P=NP` can search for a polynomial-size shared W only after source-specific existence is established. It does not prove that existence. REDTEAM25 independently shows the generic implication fails for suitable succinct EXP tableaux even under hypothetical `P=NP`.

Audit: 131,624 full assignments, exactly two solutions in every checked family; 14,392 and 23,400 at-most-two-gate descriptions at address widths five and six; planted witness absent and easy witness present; zero failures.

## Retired and open

RETIRED: diagonalization against only planted, lexicographically first, proof-first, or canonical W; PH collapse claimed to create compact W.

OPEN: uniqueness-plus-hardness or all-witness hardness for the actual diagonal family; deterministic total `R_k`; bounded universal-solver exponent; all-input ARC successor.

## Next narrow tests

- :00 prove ordinary target semantics over all KT programs, not a distinguished witness.
- :12 state whether the portfolio selects proof-first, lex-first, runtime-fastest, or minimum circuit, and charge selection.
- :24 test semantic recursive eligibility under equivalent non-Horn wrappers.
- :36 attempt parsimonious actual-diagonal encoding and then attack unique-witness fast-forwarding.
- :48 admit witness lower bounds only with uniqueness or universal quantification over satisfying witnesses.

Timestamped MAIN, exact audit, and raw JSON accompany this handoff. Root `main.tex` remains protected and untouched.
