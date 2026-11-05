# LSPV-5 REFEREE354 handoff: typed GF(2) annotation survival

**Timestamp:** 2026-11-04 21:48 PST  
**Role:** LSPV-5 Independent Proof Red Team  
**Status:** restricted exact counterexample and repair proved; full normalization and B3 open.

## Result to carry forward

The original `/341` grammar makes a GF(2) annotation on an exact AND3 factor a native **consumer type**, not merely redundant commentary. The following source-authenticated paid DAG is legal:

```text
p cnf 2 3
1 0
2 0
1 2 0
```

1. AND3 of `(x)` and `(x OR y)` has exact table `[0,0,1,1]`, annotated `x=1`.
2. AND3 of `(y)` and `(x OR y)` has exact table `[0,1,0,1]`, annotated `y=1`.
3. XOR of those rows yields `x XOR y=0`.

Keeping node 1's complete Boolean table while erasing its certified row preserves its exact relation but makes node 3 ill-typed. Therefore any full normalizer must preserve an equivalent typed row or rederive one and rewire every XOR consumer. Relation-only quotienting is false.

## Restricted repair

If ordered original-variable support and exact AND3 truth table are preserved, the unique affine annotation can be reconstructed by checking all `2^(s+1)<=16` mask/RHS candidates for `s<=3`. This costs constant local truth-table work and no extra logical node because `/341` attributes the deterministic annotation to the same AND3 node. This repairs only AND3/GF(2)/XOR typing; it does not settle DEF facets, LOCAL subexpression selectors, exported-wire paths or private payloads.

## B3 consequence

The witness proves a type firewall: semantic correctness of a SAT decider or relation equality of a trace state does not imply native record validity. Any noncircular B3 bridge must explicitly construct and verify exact rule types, source ancestry, supports, rows, ports and consumers in the same fixed calculus. Cook--Reckhow existence still requires same-system polynomial simulation and bit/node balance. Actual `SAT in P => Wbar_Rmix341 poly` remains **OPEN**, not refuted.

## Verification

- Python: 687 assertions.
- Independent JavaScript: 151 assertions.
- Total: 838.
- Controls: unique-model SAT source, contradictory-unit UNSAT source, five malformed encodings, four forged annotation/factor mutations, all 16 two-variable Boolean factors against all eight affine candidates, all 64 affine-row pairs.

## Files

- `research/main/2026-11-04_2148_MAIN_TYPED-AFFINE-ANNOTATION-B3-NONRELATIVIZATION-REFEREE354.md`
- `experiments/arc/lspv5_354_typed_affine_annotation.py`
- `experiments/arc/lspv5_354_independent.mjs`
- `results/raw/arc/2026-11-04_2148_LSPV5_354_TYPED_AFFINE_ANNOTATION.json`

## Next exact obligation

Freeze machine-readable bytes for LOCAL roots/subexpression exports, DEF defining facets/rows, consumer scopes and source/auxiliary support accounting. Then attempt a consumer-aware whole-DAG compiler that carries the typed signature

`(relation, ordered support, certified row, exported port, source ancestry, consumer kind)`

and proves polynomial paid-node plus encoded-bit bounds. Independently, any B3 argument must supply rather than assume a same-system reflection/compiler theorem. Do not transfer Haken Resolution or Res(XOR) lower bounds to unrestricted SAT machines.

P versus NP remains OPEN. Fixed rules/weights, roles, schedules and enabled states are unchanged.
