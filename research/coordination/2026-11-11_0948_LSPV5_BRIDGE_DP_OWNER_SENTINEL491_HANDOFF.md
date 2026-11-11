# LSPV-5/491 five-role handoff — bridge DP replay and paid-owner sentinel

**2026-11-11 09:48 PST | LSPV-5 Independent Proof Red Team | historical Route B | P versus NP OPEN**

## Exact result

The exact LSPV-1/575 6,764-byte packet, Git blob `d5de0f477cd736ec5fd7b01be18350f9cb594fd2`, was replayed in an actual OS Node subprocess against unchanged checker blob `338305c0ce101704205e57543756b8127074a986`. It accepts at $W=63$: 41 SOURCE, 62 strict RES, one paid owner, 103 records and 8,194 assertion groups. Independent replay verified all 62 signed oriented resolvents. Every RES node is terminal-live; SOURCE indices 2, 3, 20 and 21 are terminal-dead. Exhaustive enumeration found zero models among all $2^{15}=32{,}768$ original edge assignments.

## New restricted theorem and counterexample

The owner has zero clause occurrences and no DEF facets. For the fixed proof, every parsed single-owner tuple

$$
[i,z,a,b],\quad i\ge0,\quad z>15,\quad z\ne16,\quad
1\le |a|,|b|\le15
$$

with safe-integer coordinates is accepted by the full CLI at the same $W=63$. Six representatives passed, including repeated inputs, complementary inputs, a large gate ID, and `[9007199254740991,9007199254740991,15,-15]`. The exact hostile packet is published and passes all 8,194 assertions. Six invalid boundary tuples reject.

Deleting the owner and repairing summaries is accepted by the exact original mathematical core at $W=62$, but the full CLI rejects because its `gate_defs.shift()` corruption becomes a no-op. Therefore the one-unit owner is a wrapper sentinel for this family, not terminal proof-DAG work. A full-CLI abstraction must retain owner nonemptiness/paid count; a core abstraction may erase the dead owner with cost 62. Accepted owner variants are not CEGAR-spurious.

A deterministic search tested 4,106 Davis--Putnam orders; 19 used 62 RES and none used fewer. This is not an optimality proof.

## Consequences and role routing

- **LSPV-1 Route B:** retain $W_{\mathrm{CLI}}\le63$ and distinguish the logical-core $W=62$ representative; do not state optimality.
- **LSPV-2 Route A:** cone normalization may delete the dead owner only for core semantics; full CLI needs an explicit one-unit wrapper repair.
- **LSPV-3 Route B:** source-slot transformations must retain the wrapper predicates separately from source/RES semantics.
- **LSPV-4 Route A:** keep logical work, paid-result slots, literal slots, bytes and physical RSS separate; this audit's 185,820 KiB parent-process high-water mark is not proof space.
- **LSPV-5 Route B:** next attack a genuine accepted mixed-rule port or a lower-cost native shortcut, not another unqualified wrapper-to-calculus identification.

## Artifacts

- report: `research/agents/lspv-5/2026-11-11_0948_LSPV5_BRIDGE_DP_OWNER_SENTINEL491.md`;
- executable: `experiments/review/lspv5_491_bridge_dp_owner_sentinel_audit.js`, blob `76a19604163a533999fca6e064d664d33b35a23d`;
- raw: `results/raw/arc/2026-11-11_0948_LSPV5_491_BRIDGE_DP_OWNER_SENTINEL_RAW.json`, blob `4c88852b98f888942755c2d6d44dce59fe8e9b80`;
- accepted hostile: `results/raw/arc/2026-11-11_0948_LSPV5_491_MAX_SAFE_OWNER_ACCEPTED.json`, blob `4778d473df8ea0bd433df33d1cea3785770f04da`.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Current `proof1.txt` blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b` and `proof2.txt` blob `d79f9fa101127412aeca2c807353e1d0dbfc262b` already retain all load-bearing obligations as OPEN. P2-D1, P2-C3, P2-B1 and separate P2-B2/B3 remain OPEN. The five identities, titles, Pacific schedules, weights, ownership boundaries and TWO Route A/THREE Route B labels are unchanged. **P versus NP remains OPEN.**
