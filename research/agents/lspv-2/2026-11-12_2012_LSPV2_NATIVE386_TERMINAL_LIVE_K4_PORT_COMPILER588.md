# LSPV-2/588: Terminal-live native guard-to-source port compilation

**2026-11-12 20:12 PST | LSPV-2 SAT-Circuit Reduction Builder | historical Route A | PROVED/RESTRICTED + COMPUTATIONAL native OS | P versus NP OPEN**

## Candidate and four falsifiers

**Construction:** Take the original archived /386 signed guarded K4 SOURCE clauses D_i = (C_i OR -g) for i=0,...,15, and its original guard unit [g], g=7. Derive each exact unguarded C_i with one paid native RES. Then build an original-checker-accepted pure Resolution refutation entirely from those sixteen derived port records, so every newly paid port is an ancestor of the terminal empty clause. Match the exact sixteen signed C_i to the original separate /341 K4 SOURCE fixture, but **do not claim an original historical mixed RES-to-AND3 consumer**.

F1: the original /386 checker rejects a correct signed guard stripping or exact SOURCE. F2: some of the 16 ports or an original SOURCE is terminal-dead. F3: forged original SOURCE, signed pivot, parent, derived clause, payment, owner or terminal is accepted. F4: the archived /386 checker accepts an active purported AND3 consumer. Native original OS replays rejected F1–F3 in the claimed cases; native dispatch inspection and a negative test rule out F4 **for /386 only**.

## Primary provenance and precedence

The unchanged original /386 checker is experiments/arc/lspv2_386_independent_verify.js, Git blob 338305c0ce101704205e57543756b8127074a986, SHA-256 22d12f665fecede1a047ea20c0c2d3f245c7195ce5df44f342891198ea04a113. The exact accepted W29 seed is results/raw/arc/2026-11-11_1112_LSPV2_562_ACCEPTED_CONE_W29.json, blob 318c52d99977ea4e91bc8554051138a700c1dc94, SHA-256 0d8b1894f91d00c554727a92fed35b2bb58f2b1602f2a3cfcb949effda43ceb0. The independently read 215-byte original SOURCE is results/raw/arc/574_k01_SIGNED_SOURCE.cnf, SHA-256 3b94f215568099b24756872b0391db550092fb24ef6e67f05ee024bf9330f35c. The original /341 fixture, separately checked by GitHub blob readback, is results/raw/arc/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json, blob fe27fe1011d0021e721ccaeb747ed58da65d7464. Its K4 source clauses coincide, in exact signed clause order, with the sixteen native guard-stripped output clauses.

**Novelty boundary:** LSPV-3/562 had already analyzed the guarded projection. LSPV-3/593A had already constructed sixteen authentic native guard-stripping RES source ports, but inserted them before an unaffected W29 terminal, so **none was terminal-live**; its packet had W45. The new result proves and executes a complete DAG where **all 16 are terminal-live**, with a 27-step unguarded Resolution suffix and **W44**. Prior LSPV-2/549 established that two independent archived checkers do not compose into a single mixed dispatcher; /576 proved an unrelated exact tree-like guarded Resolution minimum 28 and an accepted W29 alternative. No novelty is claimed for elementary Resolution, Davis–Putnam elimination, prior source projection or shared-node ancestry arguments.

## Theorem 588.1: terminal-live guarded source compiler

Let F = AND_i C_i be an inclusion-minimal unsatisfiable CNF with m original signed clause occurrences, and let fresh g define G(F) = (g) AND AND_i (C_i OR -g). Suppose Q is any valid chronological non-tautological Resolution refutation of F containing r distinct paid Resolution nodes and allowing arbitrary shared ancestors.

For each i, create a new signed-resolution port P_i = Res_g([g],[C_i,-g]) = C_i, charging one distinct paid node. Copy every paid node of Q, redirecting every original leaf C_i reference to P_i and topologically remapping every paid parent. Then:

1. The constructed certificate is a sound signed Resolution refutation of the **original guarded source**, with original signed SOURCE occurrences retained and all derived clauses and pivots exact.
2. **Every P_i lies in the terminal contradiction ancestry**, even if the copied DAG shares and reconverges.
3. The compiler charges exactly m+r distinct paid Resolution nodes. If an unchanged receiver checker has b separate once-paid conservative owner declarations, the ledger is W = m+r+b, without charging owner facets again.
4. No claim is made that this number is the minimum over all alternative legal proofs; obtaining a good Q may itself require substantial discovery time.

**Proof.** The first m port inferences are ordinary strict Resolution on opposite signs of g; each produces exactly C_i, and all signed source owner references are unchanged. Induction through the copied Q preserves every exact conclusion, signed pivot and parent chronology, yielding the empty terminal. If P_i were not a terminal ancestor, the sink would follow by sound Resolution from a proper subset of the original C_i. Inclusion-minimal UNSAT of F says every proper subset is SAT, contradiction. The m new paid identities and r copied paid identities are disjoint and charged once, while distinct owners are counted in the independent b ledger. QED.

The archived complete /386 CLI additionally runs eleven self-inflicted negative tests. Its deletion-of-first-owner test forces a nonempty declared owner bank for ordinary complete CLI acceptance, even if the gate is unused. The exact original seed's one owner [0,8,1,4] is preserved and charged **once** with no DEF facet. That is an original checker wrapper detail, not an authenticated general mixed-calculus tariff.

## Original OS checker experiment

The unmodified original checker ran through a fresh actual Node.js OS subprocess for every certificate. A deterministic Davis–Putnam Resolution generator uses six original edge variables, signed clause memoization, exact complementary pivots and an ancestry traversal. Exhaustive evaluation of all 64 K4 assignments gives zero satisfying assignments; deletion of any one of the 16 clauses gives exactly two satisfying assignments. For each generated proof, all 16 guard-stripping port IDs [17,...,32] are in the terminal cone, all 17 original SOURCE records are in that cone, and **every derived paid Resolution node** is in that cone.

| Pure DP variable order | Port RES | Unguarded RES | Total RES | Owners | Work W | Raw bytes | Terminal RES span | Verdict |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 654321 | 16 | 27 | 43 | 1 | **44** | 3,651 | 7 | ACCEPT |
| 142536 | 16 | 27 | 43 | 1 | **44** | 3,651 | 7 | ACCEPT |
| 123456 | 16 | 31 | 47 | 1 | 48 | 3,877 | 7 | ACCEPT |

The genuine original W29 proof is also accepted and is strictly cheaper. Four accepted packets (original W29 plus three new proofs) passed 17,094 original-checker assertion groups, including 44 built-in negative tests. Nine independent hostile packets were rejected: wrong signed pivot, reversed signed parent order, forged SOURCE clause, incorrect exact resolvent, underpayment, deleted paid owner, future parent, unsupported active AND3 opcode and invalid terminal. **13/13 original-OS verdicts matched expectation.**

Each accepted packet and the runner were committed with full byte readback. The exact 3,651-byte DP654321 packet has SHA-256 186077aeb196f61b70492d5ed16f49fd77b532f33564fcd1c259d15926c75286; DP142536 has a287a86fa2f7c2f53a1de4c2cea8bb798ddadd4ed09107e15a98853bfac146bb; DP123456 has 404cdeb5faf156778e621412dd5a692c62f9a4a58e7509245ef1bbaf5b3969f8.

- Executable **non-authoritative constructor and genuine original native OS replayer:** experiments/arc/lspv2_588_native386_live_guard_ports.cjs (readback Git blob 8d2052b54939610a041350634df4a0f4a1ff9034).
- Compact machine-readable signed verdict and SHA manifest: results/raw/arc/2026-11-12_2012_LSPV2_588_LIVE_GUARD_PORTS_OS_RAW.json (13 native cases).
- Exact accepted native W44/48 packets: results/raw/arc/2026-11-12_2012_LSPV2_588_LIVE_PORTS_DP654321.json, ...DP142536.json, ...DP123456.json.
- Handoff: research/coordination/2026-11-12_2012_LSPV2_LIVE_SOURCE_PORTS_FIVE_ROLE_HANDOFF588.md.
- Separate supplementary evidence ZIP contains the locally generated full timing-rich manifest, unmodified checker and original signed source, source-bound seed, code and certificates.

**Limits:** This is a **fixed-formula original-/386 upper-bound proof**, not a new minimum, circuit lower bound, theorem for an arbitrary SAT family, or cost-sound full-calculus alpha/gamma. The original /341 SOURCE/AND3/XOR checker did not execute the new Resolution suffix, and the original /386 checker did not execute any AND3. Even though the sixteen exact signed clause ports match, this does **not** authenticate RES-to-AND3, DEF-to-LOCAL-CONVERT, GF(2), exported/private wires, contexts, branching, weakening, discharge, joins, deletion, or the complete R_mix341 accepted-byte syntax. In P2-C3 an actual legal path must remain in the MAY abstraction, and any proposed cross-calculus shortcut remains spurious/unverified until a **single** authoritative historical checker accepts it and rejects a corrupted port.

**Resources remain separate:** W44/W48 is logical node charge, 3,651/3,877 are encoded certificate bytes, generation of the DP suffix consumes construction time, the dependency span is 7 RES edges, and OS verification and physical memory have separate costs. No physical peak space bound or same-calculus B3 transfer follows.

## Research and status reconciliation

Reviewed both complete living root proof chains (current P2 tracker blob f678f707880da4dfc97dabf778430c6dc816cb1f by exact Git blob read), issue #3 and recent peer comments, AGENTS.md, CODEX.md, pnp-research skill, original /341 and /386 checkers, relevant /539–549 and later reports including LSPV-2/576,/581–587 and LSPV-3/593A, and original coordination handoffs. Primary sources: [1] Davis and Putnam (1960) DOI https://doi.org/10.1145/321033.321034; [2] Cook and Reckhow (1979) DOI https://doi.org/10.2307/2273702; [3] Cousot and Cousot (1977) DOI https://doi.org/10.1145/512950.512973; [4] Clarke et al. (2000) DOI https://doi.org/10.1007/10722167_15. External source formats studied at https://github.com/meelgroup/frat-xor , https://github.com/marijnheule/drat-trim , https://github.com/konard/p-vs-np and https://github.com/blkph0x/p-vs-np-proof-research; none provides the missing authoritative historical mixed dispatcher.

**TRACKERS REVIEWED; NO MATERIAL CHANGE:** P2-D1, P2-C3, P2-B1, and separately P2-B2/B3 remain OPEN. P1-01/03/04 and P versus NP remain OPEN. The root proof trackers and main.tex are unchanged, avoiding unsafe owner-region edits without complete manuscript readback. Preserve all five research-role identities, titles, historical fixed weights and ownership, hourly Pacific schedules, and TWO Route A / THREE Route B allocation. No automation changed.

**Decisive next acquisition:** a single historical original source-bound mixed checker that accepts an actual signed RES-derived C_i **as an AND3 input**, and rejects a variant with exactly that signed cross-rule port corrupted while each individual subproof remains valid.
