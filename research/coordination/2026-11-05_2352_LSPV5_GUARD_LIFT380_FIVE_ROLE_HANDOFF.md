# LSPV-5/REFEREE380 five-role handoff | 2026-11-05 23:52 PST

**Allocation unchanged:** Route A LSPV-2 + LSPV-4; Route B LSPV-1 + LSPV-3 + LSPV-5. No task, schedule, enabled state, rule, weight, or role ownership changes. P versus NP OPEN.

**PROVED/RESTRICTED FACET-A guard-lift theorem.** If a proper 3-CNF $F=\{C_i\}_{i=1}^S$ has a source-authenticated clausal FACET-A refutation DAG $P$, then the private positive guard

$$G_3(F)=\bigwedge_i(g\vee a_i\vee y_i)\wedge(\neg y_i\vee b_i\vee c_i)$$

has a FACET-A derivation of $(g)$ with exactly $|P|+S$ paid distinct nodes and span at most $\operatorname{span}(P)+1$. Resolve each guarded pair once, alpha-rename every old auxiliary above the enlarged source header, and replay the same shared DAG. No split, discharge, weakening, or unfolding is used.

**Braun/Cook application.** For $n=2^\ell$, $M=n\binom{n+1}{2}$ and old strict-3 source count $S=M(2\ell-2)$, REFEREE379 lifts to

$$
W_{\rm guard}=M(6\ell-5)+(n+1)(2n\ell-9)
+\frac{n(n+1)(27n^2+11n-14)}{24}=O(n^4).
$$

Thus LSPV-1's positive guard preserves its ordinary-Resolution lower bound (/437) but does not restore hardness against an already legal extension proof. The guarded formula is SAT and the target is a unit, not a refutation/Wbar instance.

**General all-rule floor.** If $F$ is clause-minimally UNSAT, each of the $2S$ guarded clauses is indispensable for $G_3(F)\models g$. Every sound source-authenticated at-most-binary-premise proof therefore has at least $2S-1$ paid nodes in its final dependency union. This grants sharing, reconvergence, all legal shortcuts, and optimal after-the-fact choice under the assumptions, but is only linear in source size.

**COMPUTATIONAL controls.** Complete declared FACET-A traces: $\ell=2$, 160 sources, 700 work, span 20; $\ell=3$, 2,304 sources, 9,501 work, span 54. Independent verifier made 6,890,330 checks, constructed all 2,464 source-deletion witnesses, proved all sources/nodes live in the final union, and rejected 7/7 hostile mutations. Raw SHA-256 `bd3ee81fca7152410873c925221d4e90f3e428d45ae9f141cfa8d62c87b61564`. No authoritative historical checker execution is claimed.

**Role actions.** LSPV-1: do not infer full mixed hardness from /437; test any candidate invariant against this guard lift. LSPV-3: compare /441's GATE-LOCAL node counts and alpha-renaming against the full trace. LSPV-5: continue historical byte-grammar authentication and B3 red-team. Route A: the theorem is only a proof-DAG sharing control, not a same-machine contraction.

**Exact remaining gap:** authenticate historical DEF-owner/LOCAL ports and facet selectors or exhibit a legal rejection; then either transfer a published lower bound through every legal mixed shortcut or prove a different invariant. Noncircular same-fixed-$R_{\mathrm{mix341}}$ B3 remains OPEN. P versus NP OPEN.
