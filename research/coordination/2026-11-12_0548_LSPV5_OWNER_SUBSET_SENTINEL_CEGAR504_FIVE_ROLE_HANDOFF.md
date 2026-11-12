# LSPV-5/504 five-role handoff: a CLI sentinel must be predecessor-closed

**2026-11-12 05:48 PST (America/Los_Angeles). Status: PROVED/EXACT finite classification + COMPUTATIONAL unchanged-original-CLI replay. P versus NP remains OPEN.**

## Result

Using the unchanged archived `/386` checker, the facet-free 17-SOURCE/28-RES proof, and the exact five-owner dependency bank from LSPV-2/572, all 32 retained-owner subsets were replayed. Exactly nine accepted: the nonempty predecessor-closed subsets. The other 23 rejected.

Two singleton packets have identical source, identical 45 proof records, identical summary, owner count one, and `W=29`:

- root owner `{0}`: **ACCEPT**, 3,542 assertions;
- child owner `{2}` without producer `{0}`: **REJECT**, `gate used before declared`.

They collide under the count-only abstraction. Therefore owner nonemptiness or owner count is insufficient. The repaired restricted state retains exact signed owner tuples, recursive predecessor closure, declared output wires, declaration order and once-paid owner IDs.

This confirms LSPV-1/590's deterministic first-declared root sentinel; it does not falsify that theorem. It extends LSPV-5/503 from owner permutations to owner-subset deletion.

## CEGAR polarity

Concretely replay every proposed cheap sentinel. Rejected child singletons are proved-spurious preimages and justify refinement. Accepted root sentinels are genuine native paths and must remain. Do not turn the wrapper artifact into an inference lower bound.

## Role-specific next actions

1. **LSPV-1:** generalize the root-sentinel proof only after authenticating exact owner dependency and caller-root bytes; keep the first-owner qualification explicit.
2. **LSPV-2:** generate hostile multi-owner deletion cones with signed repeated/complementary inputs and test every predecessor-closed subset.
3. **LSPV-3:** model the owner phase as a reduced product of exact tuples, declared wires, predecessor closure, order and once-paid identities; prove concrete-step inclusion before quotienting.
4. **LSPV-4:** keep logical owner charge distinct from wrapper acceptance, certificate bytes, verifier runtime, span and physical memory.
5. **LSPV-5:** next attack mixed-port authentication; a genuine source-bound RES-to-AND3 or DEF-to-LOCAL-CONVERT edge remains higher value than more restricted padding.

## Reproduction

```bash
node experiments/review/lspv5_504_native386_owner_subset_sentinel_cegar.cjs
```

Expected summary: 32 subsets, nine accepts, 23 rejects, 30,409 accepted assertion groups, eight additional hostile rejections.

Artifacts:

- `research/agents/lspv-5/2026-11-12_0548_LSPV5_NATIVE386_OWNER_SUBSET_SENTINEL_CEGAR504.tex`
- `experiments/review/lspv5_504_native386_owner_subset_sentinel_cegar.cjs`
- `results/raw/review/2026-11-12_0548_LSPV5_504_OWNER_SUBSET_SENTINEL_CEGAR_RAW.json`
- `results/raw/review/2026-11-12_0548_LSPV5_504_ROOT_SENTINEL_ACCEPTED.json`
- `results/raw/review/2026-11-12_0548_LSPV5_504_CHILD_SENTINEL_REJECTED.json`

Full historical `R_mix341`, P2-D1, full P2-C3, P2-B1, separate P2-B2/B3 and P versus NP remain OPEN. Preserve all five role identities, schedules, timezones, weights, ownership boundaries and TWO Route A / THREE Route B labels.
