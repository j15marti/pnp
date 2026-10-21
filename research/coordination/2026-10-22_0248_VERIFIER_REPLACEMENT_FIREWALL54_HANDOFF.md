# VERIFIER-REPLACEMENT-FIREWALL54 handoff

**Timestamp:** 2026-10-22 02:48 Asia/Seoul  
**Global status:** P versus NP OPEN; P versus RP OPEN.

## New established result

For every deterministic polynomial-time decider `D` and every uniform balanced polynomial-size decorator `B`, the verifier `V_B(x,r)=D(x) AND B(r)` is an exact-half RP verifier for `L(D)`. The same language also has `D(x) AND r_1` and the randomness-ignoring verifier `D(x)`. Therefore certificate width, residual width, ANF degree, Tseitin trace structure, and digest portfolios of one selected verifier are not language lower bounds unless made invariant under replacement by a proved, charged canonicalization theorem.

## Circuit-SAT rule

Parsimonious Tseitin/proper-3-CNF conversion preserves primary accepting inputs and gives one trace per primary input. It does not preserve density in the full formula-variable cube: `q` forced trace bits multiply the denominator by `2^q`. Sample primary randomness and compute the trace. Gate inspection and source access remain chargeable deterministic bypasses.

## Audit

`experiments/review/2026-10-22_verifier_replacement_firewall54_audit.py`: PASS, 212,424 assertions. The finite test compares three easy languages under hard and projection decorators, checks parity certificate sensitivity and affine residual ranks, and validates unique-trace density scaling. It is not a class-separation experiment.

## Next actions

- :00: differential-test any ordinary-MKTP generator on hard/projection encodings of the same language.
- :12: enforce `exists L, for all D` before accepting a verifier obstruction.
- :24: demand matched all-input hereditary successor inequalities on equivalent encodings, including peak space.
- :36: test a proposed universal deterministic compiler on an unknown removable decorator; no advice/oracle leakage.
- :48: require representation invariance or name the exact missing canonicalization theorem.

Root manuscripts were untouched.
