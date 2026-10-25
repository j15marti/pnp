# ARC177: M22 projected-child closure
Run anchored to the user's 2026-10-25 10:16 Los Angeles instruction. ARC/FLMV remains the single active spine. No task/schedule/enablement changes.

## Actual new construction
Every monotone short-clause residual H with at most two occurrences per sign can now be compiled, without deciding it, into an equisatisfiable proper unique monotone exact-(2P,2N)-3CNF. Output is also non-fully-paired. This is NOT the earlier XOR grammar.

Use three disjoint source copies. Delete positive clause (194,196,197) from original Doecker U to obtain a satisfiable 263-clause factory forcing its three deficient positive ports false; use the sign-dual for negative padding. Pad corresponding short clauses with these ports. Restore each missing signed occurrence on the three copies using the previously proved NEUTRAL-PORT100 nine-clause gadget. Attach the fixed six-variable SAT Y to ensure nonpaired membership. All source copies and all factories/fillers have exact quotas after assembly.

For n,m,L and E=3m-L, D=4n-L, exact output counts are n'=3n+198E+6D+6 and m'=3m+263E+9D+8. Bounds: n'<=417m+6, m'<=556m+8. For a q-clause block of a genuine M22 source with b shared variables, the sharper nonconstant bound is m'<=3q+789b+8. Constants use Y or U. Last-use placement of deficit fillers gives ordered frontier w'<=3w+210, not unchanged width.

Correctness: every satisfying output restricts to satisfying H copies because padded literals are forced false; any three satisfying H assignments extend through neutral fillers. The compiler acts on the actual fixed-value residual, unlike the old renaming repair that erased branch semantics.

## Executed audit
582 explicit assertions; 44 small source controls (41 SAT, 3 UNSAT); 113 satisfying extensions independently replayed; all neutral port truth assignments; freshly generated and independently checked 89-node refutation of the 32-variable internal template; all six template copies and all 64 assignments of the core yielding U UNSAT.

Connected target-class SAT mate V swaps variable occurrences 194 and 5 in U's positive clauses 1 and 7. It has the same 198 variables/264 clauses and exact quotas, with a checked full witness. It is not the earlier mixed-sign SAT mate.

Five first-level and nine second-level restriction/restoration children are genuinely M22. Connected examples grow 264 -> 1356 -> 4632 clauses: these validate closure, not contraction. Another 32 block assignments were sampled and compiled. The full original-U partition would require 259015808 boundary queries, so it was NOT exhaustively executed. Large compiled UNSAT outputs rely on the checked U proof and compiler theorem, not separate general SAT runs. Physical FLMV work/space was not measured.

## Exact remaining arrow and role requests
Role 2: exploit the now-explicit class compiler, but construct a paid A-dependent boundary compression or decomposition with acceptable fanout on all sources. No original-scale A fallback may be free.
Role 3: independently check triple-copy semantics, constant factory, signed deficits, named gluing and w'<=3w+210. Audit two levels against high-boundary sources.
Role 4: account for eager output, source passes, discovering last-use positions, boundary acquisition, all writes including unchanged writes, actual guest calls and peak live buffers. The ordinary-3CNF adapter has linear-size writable storage and is not automatically a strict-FLMV transport.
Role 5: retain OPEN. The source-order example costs hundreds of millions of literal boundary queries; this is not a lower bound on all algorithms. No all-input favorable successor has been established.

## Publication and preservation
Report: research/agents/lspv-1/2026-10-25_1016_LSPV-1_ARC_M22_PROJECTED_CLOSURE177.tex.
Complete code/raw data/full proof/source/refutation are attached to the conversation as ARC177_M22_construction.zip. Script SHA-256 c567523504f2ac5ba0b1afb9e63be6ca69b6b52d1cd49c023d19040f589b0ed8. Repository code/raw mirrors are NOT claimed in this handoff.
Root main.tex has not been changed: this connector session did not perform a full-file fresh-SHA merge of its large LSPV-1 region. This additive handoff records the pending root reconciliation; no peer region was overwritten. No peer review or receipt is claimed.

END_HANDOFF::ARC-M22-PROJECTED-CLOSURE177
