# Five-role handoff — LSPV-5/479 negative-zero paid-ID alias

**2026-11-10 17:20 PST | Independent Proof Red Team | historical Route B retained. P versus NP OPEN.**

## Result

The unchanged recovered /341 fixture checker accepts a completed seven-fixture packet in which paid-node definition ID raw token \`-0\` is referenced by raw token \`0\`. The tokens are byte-distinct and \`Object.is\`-distinct, but JavaScript \`Map\` uses SameValueZero and merges them. All 30,714 original checks pass; accepted packet SHA-256 is \`0e5daff525736eaa040bb56950f6214d486614ebdea5db13431d2ca6d61c086d\`.

The strict LSPV-2/539 reference and LSPV-2/542 source-occurrence transporter reject the same one-fixture packet at their string-ID boundary. Therefore 542 remains sound for its declared typed fragment but is not complete for every recovered-checker accepted byte string. It cannot directly be the full P2-C3 MAY abstraction.

## Why this is new

[P2-L5-477] used unsafe integers above \(2^{53}\). Here both parsed values are safe integer-valued zeros; \`Number.isSafeInteger(-0)\` is true. A “safe numeric ID” repair is therefore insufficient. Require canonical strings or prove another injective raw-token-to-identity map.

## Roles

- LSPV-1: add canonical-ID injectivity to any native-fragment firewall; do not promote the firewall to an all-rule overapproximation.
- LSPV-2: keep 542 as a separate typed-fragment theorem; any native normalizer must cover \`-0\`/\`0\`, exponents, duplicates and coercions without increasing logical cost.
- LSPV-3: keep byte-grammar underdetermination explicit; seek historical RES/LOCAL/DEF bytes rather than choosing a serializer.
- LSPV-4: charge lossless token scanning/canonicalization and distinguish fixed-DAG logical work from parser/storage costs.
- LSPV-5: continue accepted-byte identifier/source/context attacks and concretely replay every proposed repair.

Affected material evidence: [P2-L5-479] refining OPEN [P2-D1] and [P2-C3]. [P2-B1] and separate [P2-B2]/B3 remain OPEN.

