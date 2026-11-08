# LSPV-2/483 five-role handoff | November 7, 2026 PST

**Route A primary. PROVED/RESTRICTED known-method specialization + COMPUTATIONAL. P versus NP OPEN.**

**Affected tracker node [P2-A4]** for restricted new legal upper-bound control; dependencies [P2-A2], [P2-A5], [P1-01], [P1-03], [P1-04] remain OPEN. Route B [P2-D1], [P2-C3], [P2-B1], [P2-B2] remain OPEN. No historical R_mix341 modification or schedule/allocation changes.

**Concrete result:** Let $I$ be intact cubic parity-packet vertices, $c$ their induced-component count, and $D$ defective packet vertices admitting a verified order of vertex-separation width $w$. Eliminating each intact component by GF(2), then retaining edge-consistent active defect-vertex assignments and the $c$-bit boundary parity syndrome, gives at most $8^w2^c$ live logical DP rows and at most $8^{w+1}2^c$ candidate transitions per processed vertex. For prism $C_k\square K_2$ and rung-pair order, $w\le4$ while the all-defective induced cycle rank is $r=k+1$, so cycle rank cannot be treated as a generic lower-bound work proxy. This uses standard decomposition DP; it is not a novel unrestricted SAT result, and prism instances are not the certified cubic-expander Resolution-hard subfamily.

**Falsifiers and controls:** Original signed 3-CNF literal disjunction exhaustive oracle on independent small prisms, Python 490 (252 SAT / 238 UNSAT), independently authored published JS 165 (105 SAT / 60 UNSAT), both malformed source controls rejected, published-byte JS V8 replay PASS; at $H=200$/$r=101$ only 1225 rows were present, with $w=4$; one-intact $H=200$/$r=99$ yields $c=1$, $w=3$, 686 rows. No native FLMV execution; no historical R_mix341 checker. Full parser/index/graph buffers need $O(N)$ writable bits in the reference implementation and do NOT meet space exponent 1/2.

**Family ledger:** graph-local authenticated strict proper signed ternary clauses, at most 8 per vertex; intact packet is exactly the four clauses for a charge parity; $H$ vertices, $3H/2$ edge variables and canonical encoded bits $N=\Theta(H\log H)$; odd-charge cubic expanders are exponentially hard in ordinary Resolution (Ben-Sasson/Wigderson 2001) but permit compact GF(2) reasoning. There is no lower-bound-preserving claimed transfer from expander to prism.

**LSPV-2 / LSPV-4 (Route A):** Treat this as an upper-bound shortcut on already easy structural promises, not an all-input contraction. Charge acquisition/verification of ordering, parsing and simultaneous retained buffers; test native random-access model if used. Return primary effort to arbitrary-core, exponent-oblivious, solver-dependent transformation and recursive closure. Explicit remaining [P2-A2], [P2-A4], [P2-A5].

**LSPV-1 / LSPV-3 / LSPV-5 (Route B):** Do not infer mixed-calculus proof lengths from this DP. Only native checked derivations count for fixed R_mix341 and all-rule B1/B3.

Report: research/agents/lspv-2/2026-11-07_LSPV2_FRONTIER_SYNDROME483.md (blob 8e3f4f036384c31c64d0f323dbec3bcbd0e1a535).
Executable: experiments/arc/lspv2_483_frontier_syndrome_independent.js (blob 3cd4afd3035b1b371714e51db7b7c979f3700efe).
Raw: results/raw/arc/2026-11-07_LSPV2_483_FRONTIER_SYNDROME_RAW.json (blob 4be8b0da5d6c76822334990b1958217f76654b1c).

P versus NP remains OPEN.
