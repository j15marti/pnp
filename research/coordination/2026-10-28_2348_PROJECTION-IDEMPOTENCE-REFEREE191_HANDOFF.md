# PROJECTION-IDEMPOTENCE-REFEREE191 handoff

Timestamp: 2026-10-28 23:48 Los Angeles  
Owner: LSPV-5 independent red team  
Global status: **P versus NP OPEN; ARC-EDGE-90 OPEN**

## Additive result

- **PROVED, restricted:** If the supplied boundary retains every name shared by a 2CNF component and an affine GF(2) component, private existential quantifiers distribute exactly. The canonical componentwise projection is then idempotent on a second call with the same boundary.
- **FALSIFIED:** A first compact exact projection does not automatically provide a smaller second child. The unbounded two-answer family `K_b` stalls for both SAT and UNSAT after one padded shrink.
- **FALSIFIED:** Separately deleting a shared variable is unsound. Minimal witness: 2CNF `(z)` plus affine `z=0`; joint projection is FALSE, while separate projections are TRUE and TRUE.
- **COMPUTATIONAL:** 143,026 assertions pass; 480 random exact-relation checks and padded fixed points through `b=64`.
- **Library audit upheld:** exact archive SHA-256 `a826f34b4caa3dce1d6a060079316a462b775fe3fb1f14674ab62b2e7299dfff`; rerun reproduced `results.json` byte-for-byte.

## Role-addressed requests

- **LSPV-1:** ARC215 mathematics is upheld. Add the explicit shared-variable firewall: a boundary reduction must project the conjunction jointly or retain every shared name. Do not infer repeated contraction from the first compact child.
- **LSPV-2:** ARC216's affine resolvent fixed orbit is upheld as a compiler falsifier, not a hardness result. Please test whether any proposed joint representation strictly decreases a polynomial-value rank on that family.
- **LSPV-3:** BUCKET-PROVENANCE153 reproduces and is mathematically useful under a supplied width order, but the current TeX lacks the required opening report marker and final sentinel. Please republish marker-safe without changing the content. The two actual ordinary-3CNF descendants grow and therefore do not close the one-child recurrence.
- **LSPV-4:** Audit every joint-compatibility summary for physical output length, generation time, and model-specific access. A succinct circuit/oracle is not a shorter child unless the closed recursive representation and next-call costs are proved.

## Decisive next lemma

Construct, or falsify, a polynomially discoverable **joint moving projection** for arbitrary SAT that either decides directly or emits one explicit child of size at most `N^lambda`, preserves compatibility, stays in a recursively closed language, and decreases a nonnegative integer rank of polynomial value. A polynomial-bit-length rank alone is insufficient.

## Reproducer

- `research/agents/lspv-5/2026-10-28_2348_PROJECTION-IDEMPOTENCE-REFEREE191_repro.py`
- `research/agents/lspv-5/2026-10-28_2348_PROJECTION-IDEMPOTENCE-REFEREE191_raw.json`
