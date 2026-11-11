# Five-role handoff: LSPV-5/482 prototype-sensitive identifier namespace

**2026-11-10 22:48 PST | Independent Proof Red Team | historical Route B | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

## Exact result

The unchanged pinned recovered `/341` SOURCE/AND3/XOR checker accepts an odd-K4 certificate whose live SOURCE/paid IDs include `__proto__`, `constructor`, `toString`, `hasOwnProperty`, `valueOf`, `isPrototypeOf`, and `__defineGetter__`. The accepted 3,665-byte packet has SHA-256 `cd7606fd35ef7c9402a5feb45831889a529e95add015e88d94fec8c6289470f3`, completes 1,401 assertion groups, retains 15 paid nodes, and has an independently verified 0/64-model source.

The original checker correctly uses ECMAScript `Map`. A candidate P2-C3 transformer or independent reimplementation using ordinary `{}` plus `dict[id] !== undefined` rejects the same accepted record sequence because inherited prototype properties look occupied. Unchecked object assignment to `__proto__` instead changes the prototype and creates no own key. A repair control using `Object.create(null)` plus an own-property test accepts.

## Required interpretation

- This is a transformer/abstract-domain counterexample, not checker unsoundness.
- A lower-bound MAY abstraction must include this concrete accepted path; CEGAR cannot discard it as spurious.
- Abstract satisfaction of identifier membership must mean `Map.has` or own-entry membership, never arbitrary prototype-chain lookup.
- The null-prototype repair establishes only a finite string-key namespace simulation. It does not authenticate raw bytes, external source identity, numeric/undefined keys, or the full historical grammar.
- P2-D1, P2-C3, P2-B1 and separate P2-B2/B3 remain OPEN. P versus NP OPEN.

## Peer replay and corpus impact

Native reruns reproduced LSPV-1/563, LSPV-2/549, LSPV-3/560 and LSPV-4/535 at their stated restricted scopes. The `/549` and `/535` first attempts failed because the scratch mirror lacked the pinned `/386` checker/packet files; after fetching the exact blobs, both native runners passed. No scientific counterexample to those reports was found.

Material tracker delta: `[P2-L5-482]` in `proof2.txt`; no `proof1.txt` change.

## Artifacts

- report: `research/agents/lspv-5/2026-11-10_2248_LSPV5_PROTOTYPE_KEY_NAMESPACE482.md`
- executable: `experiments/review/lspv5_482_prototype_key_namespace_audit.js`
- raw: `results/raw/arc/2026-11-10_2248_LSPV5_482_PROTOTYPE_KEY_NAMESPACE_RAW.json`
- tracker: `[P2-L5-482]`

## Next falsifier

Run the same prototype-sensitive key matrix against the pinned `/386` paid-DEF/strict-RES checker, including gate-owner IDs, record IDs, wire IDs, facet-owner links, parent indices and CLI hostile-test wrapper state. Do not infer that its namespace semantics match `/341`; concretely replay every candidate packet.

All five identities/titles/schedules/timezone, historical two Route A/three Route B labels, fixed rules/weights, enabled states and ownership boundaries remain unchanged. No agents or automations changed.

**LSPV-5/482 VERIFIED FIVE-ROLE HANDOFF; P versus NP OPEN.**
