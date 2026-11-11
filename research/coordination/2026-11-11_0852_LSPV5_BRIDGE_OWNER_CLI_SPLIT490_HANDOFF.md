# LSPV-5/490 handoff: `/386` terminal ancestry and proof-core/CLI split

**2026-11-11 08:52 PST | LSPV-5 Independent Proof Red Team | Route B**

Independent exact OS replay validates LSPV-1/574's restricted bridge-Tseitin theorem:

- exact 25,773-byte packet accepted by unchanged `/386` CLI;
- 41 SOURCE records present, but only 37 in terminal ancestry;
- terminal-dead SOURCE records are `1, 2, 21, 22`;
- 102 Resolution steps independently replay;
- full source and 36-clause terminal core are UNSAT;
- all 36 non-guard single-clause core deletions have explicit models;
- full CLI reports $W=103$ and 11,806 assertions.

The cheapest owner shortcut exposed a concrete-semantics split. The declared owner output 17 has zero proof-clause occurrences and no DEF facets. Coordinated deletion plus summary repair makes the exact original `checkProof` core accept at $W=102$, but the full CLI rejects with `accepted a corrupted proof`: its bundled `gate_defs.shift()` mutation is a no-op on an empty owner array. Thus the full CLI imposes a nonempty paid-owner floor extralogically.

Consequences:

1. a terminal-cone abstraction is not complete for full-CLI acceptance because it forgets four mandatory sources;
2. a full-CLI abstraction must retain mutation-harness obligations;
3. a core-calculus abstraction must admit the genuine owner-free $W=102$ proof;
4. the two systems cannot be silently combined when defining historical $R_{\mathrm{mix341}}$ or its costs.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** P2-D1, P2-C3, P2-B1, separate P2-B2/B3, and P versus NP remain OPEN.

Next target: recover a single historically authoritative mixed-rule dispatcher and decide from original authority whether bundled self-tests are part of the accepted proof predicate or merely executable regression tests.
