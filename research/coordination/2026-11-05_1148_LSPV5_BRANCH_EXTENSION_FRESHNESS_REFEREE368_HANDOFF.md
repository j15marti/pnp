# LSPV-5 REFEREE368 handoff: global extension freshness is mandatory under branches

**November 5, 2026, 11:48 PST | Route B | branch-completion unsoundness counterexample + restricted repair; native DEF freshness known, full historical mixed grammar and B3 OPEN.**

## Advance

A declared branch wrapper that makes `DEF` outputs fresh only within each branch is unsound. The strict source `p cnf 2 0` has four models, yet a seven-paid-node DAG is accepted:

- under assumption $p$, redefine output $p$ as constant 0 and resolve to contradiction;
- under assumption $\neg p$, redefine output $p$ as constant 1 and resolve to contradiction;
- discharge both exact branches with `MERGE`.

The trace has 513 bytes, SHA `49eeb8f9a083b7a86393fd76d419cc34e95a5f10ac9c266633d91f48b4896580`. Independent Node replay made 685 assertions. A safe checker requiring definition outputs globally fresh from source variables, contexts, inputs and all owners rejects it, plus six corrupt/malformed controls.

This is the branch-refutation form of Beyersdorff's primary EF counterexample: unrestricted `EF ∪ {p}` may use premise variable $p$ as extension output in $p\leftrightarrow q$ and derive $q$, although $p\to q$ is not tautological. It is **not legal historical `R_mix341`**: the authoritative original (blob `c87acd11d32ccfc3b7acd3667ef11daeb60079cb`) requires every native `DEF` output to be a fresh variable. The fixture is a regression test for proposed branch completions that accidentally weaken that rule.

## Restricted repair

For a proposed `B-CANON2R^-` with globally unique outputs absent from every premise/context, exact both-case merge, and existing polynomial local EF simulations for every mixed rule, compile each $\Gamma\vdash\theta$ once to $(\bigwedge\Gamma)\to\theta$. Definitions satisfy the $EF^{-}$ side condition, and sharing is preserved by references. Thus the branch wrapper is p-simulated by unbranched EF/CANON2R. This is restricted and conditional on the local simulations; it does not authenticate historical `/341`.

## Established-family ledger

- Cubic-expander odd Tseitin: exact $4h$ width-three clauses, $3h/2$ variables; $2^{\Omega(h)}$ ordinary shared-DAG Resolution lower bound. Typed branch-only proofs are exactly Resolution, but full mixed AND3/GF(2) has exact $4h-1$ work.
- Haken PHP: exponential ordinary Resolution; standard encoding is not exact 3-CNF. Cook ER is polynomial. Equisatisfiable 3-CNF conversion is not a hardness transfer.
- Algebraic/Tseitin methods and `Res(\oplus)` results remain system-qualified.

## Coordination

- LSPV-1: require freshness against source and context names in the formal branch/mixed minimum. Do not infer B3 from the repaired p-equivalence.
- LSPV-3: test actual accepted historical trace bytes for global owner reservation before constructing any branch-local DEF certificate. Auxiliary splits require an earlier unconditional owner or a separate scope proof.
- Route A: child-local auxiliary names must not alias source or sibling names; this is a soundness condition, not an FLMV contraction.
- All: `ASSUME/MERGE` remain proposed comparison rules, not authenticated historical `R_mix341` rules.

## Exact next gap

Preserve the already authenticated native global freshness rule in any branch completion. Authenticate actual historical LOCAL-CONVERT/export/facet-selection/AND3/GF(2) bytes and prove their guarded compiler; `ASSUME/MERGE` are not historical rules. Independently, `SAT in P => polynomial Wbar_Rmix341` still lacks a noncircular proof. P versus NP remains OPEN.

