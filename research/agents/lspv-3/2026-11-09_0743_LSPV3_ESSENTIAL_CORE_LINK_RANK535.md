# LSPV-3/535 | Essential-core KT linking rank versus optimal declared mixed proof work

**2026-11-09 07:43 PST | Route B | PROVED/RESTRICTED theorem + COMPUTATIONAL original-source controls | P versus NP OPEN.**

Affected node: **[P2-L3-535]**, refining [P2-L3-531] and the topology-transfer countercontrols in [P2-C3]. Historical full accepted-byte [P2-D1], source-retracting [P2-C3], all-rule superpolynomial [P2-B1], and same-calculus noncircular B3 [P2-B2] remain OPEN. Route-A [P2-A2], [P2-A4], [P2-A5], and proof1 nodes [P1-01], [P1-03], [P1-04] unchanged.

## IDEA -> SEARCH -> ITERATE and prespecified falsifiers

Initial hypothesis: restricting topological linking rank to an indispensable UNSAT core might defeat the padding counterexample [P2-L3-531]. Four falsifiers: (F1) a minimally UNSAT proper signed 3CNF family with unbounded KT rank has a linear-cost legal mixed refutation; (F2) the claimed Hopf principal submatrix is absent from the actual published reduction; (F3) some local source clause is dispensable; (F4) the short derivation smuggles in a non-native rule. **F1 is established within the declared semantic model; F2 is checked against Koenig-Tsvietkova's original reduction; F3-F4 by /341's pre-existing proofs plus new finite replay.** The new advance is the *core-minimal rank-only obstruction*, not the already published /341 work optimum or /469 depth theorem.

Primary literature: Koenig–Tsvietkova, *NP-Hard Problems Naturally Arising in Knot Theory*, Transactions AMS B 8 (2021), Theorem 1, DOI 10.1090/btran/71, arXiv:1809.10334v3, pp. 3–4. For a proper strict three-variable 3CNF with n variables and m clauses, their polynomial reduction builds n disjoint Hopf pairs plus m clause components: 2n+m components, (n+m)-component unlink target. Their initial 2n-variable-component linking submatrix consists of n disjoint Hopf blocks. This is a decision reduction, NOT a proof-calculus simulation. Urquhart 1987 (JACM 34:209–219, DOI 10.1145/7531.8928) proves exponential ordinary-Resolution hardness on qualifying expander Tseitin families; Pang arXiv:2610.00837v2 gives distinct fixed-degree polynomial-proof bounds. Neither lower bound automatically survives GF(2)/DEF/LOCAL-CONVERT. Project LSPV-2/498 cites Viola–Wigderson 2018, *Local Expanders*, for an explicit cubic bipartite family; this report's theorem requires no particular expander.

Prior project artifacts actually reviewed: LSPV-2/341 (declared five-rule semantics, source indispensability, exact W); LSPV-1/423 and /469 (balanced ideal depth and ancestry rigidity); LSPV-3/491 (recovered checker only SOURCE/AND3/XOR); LSPV-3/531 (rank padding, NOT minimal core); LSPV-4/521 and LSPV-5/461 (torsion pooling). The current issue #3, both complete root proof trackers, November 2 five-role refocus, November 9 topology handoff, AGENTS.md, CODEX.md, and repo pnp-research skill were read. Current peer LSPV-1/536, actual GROKPROOF progress and Claude world-ledger file reviewed. GitHub direct sources: konard/p-vs-np README.md 0e0ec77f and scripts/proof_status.json 93b77ed3; blkph0x/p-vs-np-proof-research METHOD_INDEX.md 18d693ea and REVIEW_ADDENDUM.md 6a7cc2f8; meelgroup/frat-xor/format.md 986a21aa; tanyongkiam/cake_lpr/README.md e94f45e9; peitl/short-proof/README.md 93d2090d; berkeley-abc/abc/README.md 88a9d1a3; openai/math/README.md cc5b0a03; anthropics/formal-math/README.md 1df53bfc. These are comparison sources, not historical grammar authorities. Public web/primary-source search was used; a separate Google-branded interface was unavailable.

## Theorem 535.1, PROVED/RESTRICTED

Let G be connected, simple, bridgeless, cubic with h vertices, e=3h/2 edge variables and an odd GF(2) vertex-charge vector. Write **four original proper signed clauses per vertex**, exactly those excluding the opposite parity triples. The original strict-3CNF F has m=4h clauses. Every source clause is individually indispensable, by /341's deletion-witness theorem (G-v connected, and one wrong local triple restores consistency). All original edge variables have distinct incident support in each clause.

In the previously DECLARED sound, source-explicit, unit-weight, at-most-two-premise semantic /341 calculus, **not the unauthenticated complete historical accepted-byte grammar**, the prior /341 and /469 theorems give

$$
W_{\mathrm{sem341}}(F)=4h-1,\qquad
D^{\mathrm{ideal}}_{\mathrm{sem341}}(F)=2+\lceil\log_2 h\rceil .
$$

An optimal derivation pays 3h AND3 nodes combining original local source clauses, h-1 GF(2) additions joining rows to 0=1, and 8h-2 explicit parent references. All m indispensable source clauses occur in ancestry, so binary-arity lower bound q>=m-1 applies to every legal shared-DAG derivation in this DECLARED calculus. Balanced scheduling attains the ideal depth. Actual code-bit generation, verification, refs and retention cost more and are separate.

The Koenig–Tsvietkova link L(F) contains 2e+m=7h components. Its mod-2 linking matrix has a **principal** 2e by 2e submatrix containing e disjoint Hopf blocks [[0,1],[1,0]], so

$$
3h\le r_h:=\operatorname{rank}_{\mathbb F_2}\operatorname{Lk}(L(F))\le7h.
$$

For EVERY nonnegative function g on positive integers satisfying g(r)/r -> infinity, the proposed universally valid lower bound W_sem341(F)>=g(rank Lk(L(F))) **fails even within this minimally UNSAT source family**: r_h>=3h grows unbounded, so g(r_h)>4h-1 eventually, whereas an actual legal proof costs exactly 4h-1. Thus merely removing redundant clauses does not repair a *superlinear rank-only* topology-to-proof transfer. A stronger topology-sensitive quantity might behave differently; no all-topology impossibility is claimed.

The exact *historical* R_mix341 byte grammar for full RES/LOCAL-CONVERT/DEF/exported facets remains unverified, so this result does not assert historical accepted-byte minimality or any unrestricted algorithm lower bound. No full link diagram or complete linking matrix was generated; the invariant proof needs only the Hopf principal block established in the primary paper.

## Original-source and hostile verification

Five graphs: K4 and prisms with h=6,8,10,12. The independently constructed complete Python certificates contain 15,23,31,39,47 paid nodes and verify 16,24,32,40,48 individually indispensable source clauses, respectively. Their KT component counts are 28,42,56,70,84; principal block ranks are at least 12,18,24,30,36; ideal spans 4,5,5,6,6. Full odd inputs through e=15 were brute-forced; larger source UNSAT follows from charge parity. Even-charge all-zero witnesses checked. The independent Python verifier accepted all five complete original-source typed packets and rejected **50** deliberate packet mutations (source signature, parent, truth bit, XOR mask/RHS, reused ID, missing sink, invented rule, witness, charge). Producer counted 6195 instrumented assertions and 20 negative controls. Producer measured 0.101s host execution and ~97MiB peak RSS; independent verifier 0.029s. Host measurements are not a same-machine time/space theorem. Full locally reproduced original-source packets and independent Python code are in the companion reproduction ZIP; the repository JavaScript is a lighter independent finite family/status cross-check, not a native historical checker.

Dense explicit GF(2) row materialization costs O(h^2) bits for h-1 intermediate length-e masks. Indexed clauses, DAG IDs and parent references use O(h log h) bits. Keeping all deleted-clause satisfying assignments costs O(h^2) bits, separate from the optimal UNSAT proof DAG. A real solver must pay discovery, graph acquisition, input parsing, checks, failed policies, output and simultaneous peak memory, and cannot substitute offline logical optimum for its runtime.

**Remaining gap:** [P2-D1] authenticate native accepted grammar and provenance for all historical rules; [P2-C3] rule-by-rule lower-bound potential/source-retracting simulations on a genuinely all-mixed hard family, allowing compact GF(2) and extensions; [P2-B1] prove superpolynomial Wbar_R over ALL legal mixed DAGs; [P2-B2] noncircular same-calculus B3. Nothing is promoted to P versus NP resolution. Five roles, 2 Route A / 3 Route B, all weights, titles, schedules and enabled states unchanged. Root main.tex was not modified because fetch_file returned zero readable characters despite a blob ID; an outside-byte-preserving edit was unsafe.

Primary refs: Koenig–Tsvietkova 2021 DOI 10.1090/btran/71; Urquhart 1987 DOI 10.1145/7531.8928; project /341 blob c87acd11d32ccfc3b7acd3667ef11daeb60079cb.
