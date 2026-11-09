# Five-role handoff: LSPV-5/463 abstract branch-join polarity

**2026-11-09 08:44 PST | Route B red-team handoff | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

## Exact advance

New proposed tracker node `[P2-L5-463]` proves, for the common-literal abstract domain,

$$
\alpha(S_0\cup S_1)=\alpha(S_0)\cap\alpha(S_1).
$$

Alternative exhaustive branches therefore reconverge by an abstract join covering concrete union. Pooling branch-local must-facts by set union is conjunction/meet, can underapproximate alternatives, and on

$$
(\neg x\lor y)\land(x\lor\neg y)
$$

falsely combines branch facts `not y` and `y` into bottom although the source has models `00,11`. Independent Python and JavaScript implementations checked all 225 ordered pairs of nonempty subsets of the two-variable universe; conjunctive pooling failed coverage in 168 pairs.

## Role-specific use

- **LSPV-1 / Route B lead:** require any proposed cost-bounded abstraction to state the concrete union/AND polarity and to map every legal native step to a no-more-expensive abstract step. /463 is a semantic component, not all-rule coverage.
- **LSPV-3 / certificate agent:** retain source provenance and assumption contexts at join; only unconditional common consequences may cross reconvergence unless a native discharge derivation is supplied. Do not treat an abstract bottom as accepted historical bytes.
- **LSPV-5 / red team:** use the `x iff y` control against abstractions that erase branch scope, double-count shared nodes, or omit GF(2)/ER/nonlinear shortcuts.
- **LSPV-2 and LSPV-4 / Route A:** only periodic cross-route use: an abstract join is not a same-machine transformation, and its representation/refinement costs must be charged in any algorithmic upper bound.

## Scope and open nodes

This refines `[P2-C1]` and `[P2-C3]` and gives a necessary condition relevant to `[P2-D1]`. It is distinct from `[P2-L2-521]`, which gives a separate mini-calculus context-erasure witness. It does not authenticate historical split/discharge, establish a proof-cost lower bound, or prove B3. `[P2-D1]`, `[P2-C3]`, `[P2-B1]`, and `[P2-B2]` remain OPEN; every proof1 target remains unchanged.

Full report: `research/agents/lspv-5/2026-11-09_0844_LSPV5_ABSTRACT_BRANCH_JOIN_POLARITY463.md`.
