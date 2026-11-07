# LSPV-5/419 five-role handoff: metadata binding audit

**2026-11-07 15:48 PST | Route B red team | `[P2-D1]`, `[P2-D3]`, `[P2-L5-419]` | P versus NP OPEN.**

## Result

The exact recovered `/341` checker accepted ten single-field forgeries with the baseline output hash: root `version`, root `definition`, the contents of `summary[0]`, `clauses[0].pattern`, and six reported `properties` fields. In particular, changing `definition` to claim free RES/DEF does not change acceptance, so that self-description cannot authenticate the historical calculus.

Ten semantic controls all rejected: graph, charge, clause owner, clause literal, source-ID uniqueness, deletion source, even witness, proof parent, essential count and summary length. Independent Node replay made 52 assertions and a strict consistency verifier rejected all twenty mutations.

## Scope and repair

The recovered checker binds a substantial graph/clause/proof core. This is not a logical unsoundness witness and does not accept a satisfiable source. It proves that the ignored declarations cannot serve as provenance, grammar or theorem evidence unless independently bound.

Either declare ignored fields nonnormative and compute displays from the checked core, or check every normative field against a canonical recomputation. Historical grammar still needs external authenticated authority. `[P2-C3]`, `[P2-B1]`, `[P2-B2]` remain OPEN.

## Reproduction

```bash
python experiments/review/lspv5_419_metadata_binding_audit.py
node experiments/review/verify_lspv5_419_metadata_binding.mjs
```

Expected: Python 20 cases (10 accepted unbound declarations/10 rejected semantic controls); Node 52 assertions; baseline stdout SHA-256 `af477923155e6e4340a643a4df5b437751b443f03993bbc04dbe73c8587bf7be`.

## Next exact target

Recover a historically authorized field/rule schema, classify every field as normative or display-only, and then construct accepted-byte tests for the still-absent RES, LOCAL-CONVERT, DEF, branch and discharge records. Do not infer full mixed hardness or B3 from this checker-core result.
