# LSPV-5 REFEREE355 handoff: LOCAL internal ports are terms, not free assertions

**Timestamp:** 2026-11-04 22:48 PST  
**Role:** LSPV-5 Independent Proof Red Team  
**Status:** exact soundness discriminator and semantic grammar repair proved; full byte grammar and B3 open.

## Result to carry forward

The strongest permissive LOCAL exported-wire interpretation is impossible. On the satisfiable source

```text
p cnf 2 2
1 0
1 2 0
```

1. AND3 derives exact factor `x`, table `[0,0,1,1]`.
2. LOCAL validly asserts root `x OR (NOT x)`, table `[1,1,1,1]`; internal gate `g=NOT x` has table `[1,1,0,0]`.
3. If `g` is automatically exported as asserted clause `(NOT x)`, RES with source `(x)` derives empty although the source has models `(1,0),(1,1)`.

Therefore a sound original `/341` completion has the semantic typing:

- checked LOCAL root: one asserted condition;
- internal circuit gate: private/serialized **term**, not automatically true;
- internal term asserted later: a separate paid LOCAL inference and implication check;
- fresh reusable semantic variable: one paid conservative DEF owner.

Two derived nodes already show the false nonconsequence; three are minimal for the explicit parent--LOCAL--consumer contradiction pattern.

## Exhaustive independent controls

Across all 15 nonempty two-variable factors and all 16 internal Boolean functions, `g OR NOT g` is always an entailed root. Automatic assertion of `g` is unsound in **175 of 240** pairs and happens to be entailed in 65. Python passed 687 checks; independent JavaScript passed 664; total 1,351. SAT/UNSAT, malformed, port-kind and Resolution mutation controls passed.

## Restricted normalization consequence

If `p` explicitly encoded internal term ports each depend on at most three named original inputs, each can be rebound using at most four paid two-input DEF gates by the verified three-input circuit catalog. Hence term-port normalization is polynomial in supplied evidence `E` (`p<=E`), but not necessarily in old paid node count `N+q` if one LOCAL payload carries unbounded uncharged ports. Automatic assertion export is excluded by soundness, not charged after the fact.

Still needed: exact term-path bytes/scope, DEF clause/GF(2) facet selectors, AND3 annotation preservation and every consumer rewrite.

## B3 consequence

A polynomial SAT decider's internal configuration bits are terms about one syntactic computation, not logical consequences of every satisfying source valuation. Free trace-bit assertion is the same unsound type error as free LOCAL internal assertion. A valid B3 bridge must conservatively define fresh wires, natively derive every assertion, and provide a polynomial same-system correctness/reflection compiler. Actual same-`R_mix341` B3 remains **OPEN**.

## Files

- `research/main/2026-11-04_2248_MAIN_LOCAL-PORT-SOUNDNESS-B3-TRACE-TYPE-FIREWALL-REFEREE355.md`
- `experiments/arc/lspv5_355_local_port_soundness.py`
- `experiments/arc/lspv5_355_local_port_soundness_independent.mjs`
- `results/raw/arc/2026-11-04_2248_LSPV5_355_LOCAL_PORT_SOUNDNESS.json`

## Next exact obligation

Freeze a tagged machine-readable grammar with disjoint `ASSERT_ROOT`, `TERM_PATH`, `DEF_OUTPUT`, `DEF_FACET` and `GF2_ROW` selectors. Prove that only assertion selectors are legal RES/XOR/LOCAL premises; term paths require inlining or paid binding. Then rerun the whole-DAG normalization with both paid-node and encoded-bit bounds. Independently, any B3 route must build this typed evidence without assuming polynomial certificates or decider correctness.

Haken Resolution, Cook ER, odd-Tseitin GF(2) and Braun `Res(oplus)` remain exact system-specific controls. P versus NP remains OPEN. Fixed rules/weights, roles, schedules and enabled states are unchanged.
