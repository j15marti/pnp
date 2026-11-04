# LSPV-5 REFEREE328: five-role handoff

**November 3, 2026, 20:48 PST.** Fixed `R_mix341`, five identities, enabled states, schedules, ownership and safeguards unchanged. P versus NP OPEN.

## Proved result

The declared 341 `LOCAL-CONVERT` is unary from an already-derived local parent and requires explicit constant-support implication checking. It does not license arbitrary `F -> false`: a conversion to false is legal only when the explicit parent is already empty.

This guard is necessary. If a completion may consult the whole source semantically, then for fresh `z`, `(H AND not z) => z` iff `H` is UNSAT, yielding a two-node refutation of every UNSAT `H`; direct false output gives one node. Bounded conclusion support is therefore insufficient. Explicit local source ancestry is the firewall.

For the conditional private-root completion, arbitrary circuit payloads on at most constant `c` original inputs and canonical `2^c` truth-table outputs have exactly equal minimum paid-node cost: evaluate and replace each private root at the same node; conversely tables are circuits. This survives adaptive proof choice and shared outer DAGs. It fails if uncharged inner wires are exported.

Physical cost is separate. A `k`-constant AND payload has `k` independently sensitive bits and `2k+1` gate records at a fixed two-node skeleton, forcing `Omega(k)` exact payload reads. Charge encoded lengths, construction, accesses, updates, checking, output and peak live space. Permit streaming/recomputation and compact tables; do not infer writable space from streamed length.

## Established anchor and transfer status

Haken's `2^Omega(h)` theorem is for standard unary PHP in ordinary shared-DAG Resolution, explicit `N=Theta(h^3 log h)`, every sufficiently large `h` and every refutation. It is not an ER, Res(XOR), full `R_mix341` or arbitrary-machine lower bound. Polynomial ER PHP and linear authenticated GF(2) Tseitin proofs are mandatory controls.

B1, B2, B3, superpolynomial full-mixed `Wbar`, and P versus NP remain OPEN. The quotient is a restricted logical representation-independence theorem; the global-antecedent construction is an explicit counterexample to overbroad semantics, not a SAT lower bound.

## Reproducibility

- Main: `research/main/2026-11-03_2048_MAIN_ANTECEDENT-LOCALITY-ROOT-QUOTIENT-REFEREE328.md`
- Producer: `experiments/arc/lspv5_328/local_convert_root_quotient_referee328.py`
- Independent verifier: `experiments/arc/lspv5_328/verify_local_convert_root_quotient_referee328.js`
- Raw: `results/raw/arc/lspv5_328/local_convert_root_quotient_referee328.json`

Producer: 67,850 assertions. Independent verifier: 32. Exhaustive 256-by-256 local implication presentation equivalence; sensitive payloads through `k=128`; K4 odd/even `0/8`; eight malformed/global-source rejects.

## Role assignments

- LSPV-1: freeze exact quantifiers and prove source-ancestry for the final machine grammar.
- LSPV-2: test canonical tables against GF(2), compact circuits and paid DEF wires.
- LSPV-3: specify transitive support, private roots, exported-wire certificate semantics.
- LSPV-4: give a fully charged streaming/materialized checker and peak-space schedule.
- LSPV-5: attack every proposed completion with the global semantic antecedent, fresh-`z`, hidden-wire and payload-sensitivity falsifiers.

Current Grok `GROKPROOF/2026-11-04_0413_PROGRESS.md` (`09396ad9...`) and Claude DIRECTPRODUCT/TPORT/ONETAPE (`95c2649...`, `1f9fc727...`, `9a5b05d6...`) were actually read; none supplies B3. No task or schedule mutation is requested.
