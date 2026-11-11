# LSPV-2/551: Exact source provenance and binary arity still permit linear-cost semantic MAY refutations of all UNSAT CNFs

**2026-11-11 00:16 PST | LSPV-2 SAT-Circuit Reduction Builder | historical Route A | PROVED/RESTRICTED model theorem + COMPUTATIONAL finite controls | P versus NP OPEN**

## Candidate and precommitted falsifiers

**Candidate.** The /550 refinement repairs the one-paid-node global semantic oracle by recording original source masks and enforcing two parents per paid node. But if an unknown-rule MAY transition still allows unrestricted conjunction representation and a semantic terminal contradiction, then every UNSAT CNF with m>1 source occurrences admits a binary proof with m-1 paid nodes, exactly meeting the /341 source-capacity bound for minimally UNSAT inputs. This is a counterexample to the adequacy of a proposed abstraction, not to an authenticated native rule.

Precommitted adversaries: F1, the all-clause cube, pigeonhole and odd-K4 controls are SAT or fail minimality; F2, forged mask, nonexistent parent, duplicate paid ID or wrong source list survives replay; F3, a SAT deletion input is allowed to conclude bottom; F4, the resulting DAG exceeds m-1 distinct paid nodes or ceil(log2 m) depth.

## Exact model and theorem 551.1

Fix an ordinary CNF F=C_1 AND ... AND C_m with m>1 source *occurrences*. A free SOURCE node i denotes C_i with exact mask {i}. A paid SEM-MERGE node has two earlier parent identities, unit charge, union of their masks, and denotes the Boolean conjunction of the two parent formulas. A paid SEM-BOTTOM node has two earlier parents, unit charge and the union mask, and may conclude false if and only if the conjunction of its parents' represented formulas is UNSAT. **That terminal UNSAT test is a semantic oracle.** This is a purposefully overpowered MAY rule and is *not* the original historical R_mix341 syntax. Distinct shared paid nodes count once.

**Theorem 551.1 (PROVED/RESTRICTED).** Every UNSAT F with m>1 has a valid reference-MAY refutation costing at most m-1, with dependency span at most ceil(log2 m). If every original source occurrence is indispensable, every sound source-explicit refutation under these exact two-parent and positive unit-charge assumptions costs at least m-1. Consequently the reference-MAY optimum for every minimally UNSAT F is exactly m-1.

**Proof.** Place all m sources at leaves. Repeatedly pair adjacent live nodes, carrying forward an odd last node, and combine each pair using SEM-MERGE. For the final pair apply SEM-BOTTOM, justified because their conjunction is F and F is UNSAT. Each paid binary operation reduces the live component count by one, yielding exactly m-1 internal nodes. Exact mask union is preserved at each node. Balancing in rounds gives depth ceil(log2 m). If every clause is indispensable, each source lies in sink ancestry in any sound refutation. The connected ancestry graph of m sources and q paid nodes has at least m+q-1 undirected edges; since all derived nodes have indegree at most 2, there are at most 2q edges. Therefore q>=m-1. Equality follows. QED.

For minimally UNSAT input, m is at most encoded length N, so even the exact-mask two-parent semantic MAY relaxation cannot certify a superpolynomial lower bound: it always contains a linear paid path. Nothing here implies the actual historical R_mix341 contains the path. The terminal nonlocal SEM-BOTTOM oracle has no polynomial verification bound and is not a Cook-Reckhow proof-system rule or a free SAT oracle for B3.

## Source archaeology and prior work

Read BOTH root proof trackers, issue #3, AGENTS.md, CODEX.md, repository pnp-research SKILL.md, original /341 declaration (blob c87acd11d32ccfc3b7acd3667ef11daeb60079cb), original /341 fixture checker (blob fcb7d4ced8f922de14c0bda16263a8cc7853e8e0), independent archived /386 paid-DEF/RES checker (blob 338305c0ce101704205e57543756b8127074a986), actual LSPV-2/539 through /550 reports and latest shared /550 handoff. Reviewed latest LSPV-3/563, LSPV-4/536 and LSPV-1/566 issue #3 notices: nested paid-owner /386 grammar and arbitrary topological record order do not authenticate unified historical calculus.

Earlier /341 proved the lower source-capacity inequality; /550 showed a one-paid global semantic shortcut and a binary-mask refinement excluding that *particular* shortcut. The contribution here is the matching *universal upper bound* even after retaining exact source masks and two-parent arity, if the terminal semantic inference remains admitted. No new historical opcode, parser or accepted-byte claim is made.

Primary literature: Cook and Reckhow, The Relative Efficiency of Propositional Proof Systems, JSL 44 (1979), 36–50, https://doi.org/10.2307/2273702 ; Clarke, Grumberg, Jha, Lu, Veith, Counterexample-Guided Abstraction Refinement, CAV (2000), https://doi.org/10.1007/10722167_15 ; Cousot and Cousot, Abstract Interpretation, POPL (1977), https://doi.org/10.1145/512950.512973 ; Haken, The Intractability of Resolution, TCS 39 (1985), 297–308 ; Gocht and Nordström, Certifying Parity Reasoning Efficiently Using Pseudo-Boolean Proofs, AAAI (2021), https://doi.org/10.1609/aaai.v35i5.16494 . Those results do not authenticate project native grammar. Repository and proof-complexity searches checked source provenance, global MAY and binary merge. No DRAT/FRAT/XOR language is substituted for historical R_mix341.

## Executable reference replayer and finite checks

Executable: experiments/arc/lspv2_551_binary_semantic_merge_barrier.cjs (readback-confirmed Git blob **7f58a14cdebc40f84a955147102f08e650a6ad48**). Raw: results/raw/arc/2026-11-11_0016_LSPV2_551_BINARY_SEMANTIC_MAY_RAW.json. The **reference-only** interpreter tracks source identities, union masks, actual source lists, parent links, unique paid IDs and dependency span, and brute-forces the finite terminal UNSAT decision. Deterministic, no random seed.

| Original source | Variables | Clauses m | Models | Models after any one deletion | Paid MAY nodes | Span |
|---|---:|---:|---:|---:|---:|---:|
| All signed width-3 cube clauses | 3 | 8 | 0 | 1 | 7 | 3 |
| PHP(3 pigeons, 2 holes) | 6 | 9 | 0 | 1–2 | 8 | 4 |
| PHP(4 pigeons, 3 holes) | 12 | 22 | 0 | 2–6 | 21 | 5 |
| Odd K4 Tseitin | 6 | 16 | 0 | 2 | 15 | 4 |

Every original-source deletion was exhaustively confirmed SAT, establishing minimality for all four controls. Eleven hostile controls were rejected: nine malformed ancestry, identity, conclusion and accounting changes, plus two SAT source-deletion certificates. F1-F4 all failed as threats *in the reference model*. A local Node.js 22.16.0 experiment executed equivalent four-case and eleven-hostile logic with cryptographic source hashes; the exact published script was read back and executed under the connected V8 JavaScript runtime with Node assertion/crypto shims, confirming all graph and semantic results (the shim omits SHA-256 computation). This does **not** constitute a separate OS Node CLI invocation of the remote file.

The abstract logical cost is m-1. Certificate bits, exponential semantic terminal checking, construction time, span and physical peak space remain separate. The compact source-mask label is not a historical local-factor representation.

## Status and CEGAR obligation

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** [P2-D1] lacks full historical accepted-byte grammar; [P2-C3] lacks a sound complete-calculus concrete-to-abstract alpha/gamma simulation, including paid owners, zero-additional-cost facets, freshness, contexts, branches and discharge; [P2-B1] and separate [P2-B2]/[P2-B3] remain OPEN. [P1-01]/[P1-03]/[P1-04] and P versus NP remain OPEN.

**CEGAR implication:** exact source mask and two-parent constraints exclude the /550 one-node global jump but do *not* suffice for superpolynomial bounds. Remove SEM-BOTTOM only upon authenticated local-rule evidence; retain genuine XOR, extension, learned clauses, reconvergence and all unknown historical shortcuts until their semantics are settled.

Next: recover one single original full-rule accepted-byte dispatcher for RES-to-AND3 or DEF-to-LOCAL-CONVERT and establish the non-overcharging transition transformer for the actual rule. No five-role identity, schedule, timezone, route label, fixed weight or ownership change; no automations modified.

**P versus NP remains OPEN.**
