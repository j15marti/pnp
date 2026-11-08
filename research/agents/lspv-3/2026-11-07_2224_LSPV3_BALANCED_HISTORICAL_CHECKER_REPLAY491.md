# LSPV-3/491 | Historical SOURCE/AND3/XOR acceptance of a simultaneously work/span-optimal balanced Tseitin packet

**2026-11-07 22:24 PST | LSPV-3 Hypergraph & Proof Certificates | Route B primary.**
**Statuses:** PROVED/RESTRICTED native accepted-subgrammar replay; COMPUTATIONAL 30,714 assertion replay and finite controls; OPEN historical full mixed grammar, full mixed normalization, B3, and P versus NP.

**Relevant exact tracker IDs:** [P2-D1], [P2-D3], [P2-C3], [P2-B1], [P2-B2], [P2-F13], [P2-L3-490], [P2-L5-413], [P2-L5-426]. Newly reported restricted evidence intended as [P2-L3-491]. Companion [P1-01], [P1-03], [P1-04] remain OPEN.

## IDEA: precommitted hypothesis and falsifiers

**Initial hypothesis:** The *actual recovered* /341 independent verifier, previously authenticated as an accepted SOURCE/AND3/XOR subgrammar, might accept a re-ordered, balanced proof of the identical original signed strict 3-CNF Tseitin source, retaining all original source and deletion witnesses, lowering longest dependency path without changing any paid node count. This would authenticate an already proved ideal-span construction through an original historical checker rather than a convenient independent new checker.

**Falsifiers:** (F1) original checker requires left-associated XOR chain, not arbitrary earlier two-parent rows; (F2) balanced four-clause AND3 changes the original three-variable truth-table or affine-annotation semantics; (F3) rewriting IDs/order loses source provenance, DAG ancestry, corruption controls, or the internal source; (F4) the claimed work/span theorem is new when earlier project reports already proved it, requiring a narrower, non-duplicative result. F1-F3 were refuted by exact recovered-verifier logic replay; F4 was confirmed by discovering LSPV-1/423 and LSPV-1/469, so **no novelty is claimed for the work/span mathematics**.

## SEARCH: governing controls, existing result, primary research

Read complete root `proof1.txt` (blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`, 18,553 characters) and `proof2.txt` (prewrite blob `08ad1e11f9f570841c7a0164eaad793555973c33`, 331,910 characters), governing historical handoff at commit `4e29ed7646f484707767acb6e63ec5f38afd98a8`, `AGENTS.md`, `CODEX.md`, and `.codex/skills/pnp-research/SKILL.md`. Read issue #3 body and recent comments through LSPV-1/496 (2026-11-07 22:00 PST); LSPV-1/495 and /469 and /423, LSPV-3/490, LSPV-5/413 and /426; Grok `GROKPROOF/2026-11-06_2316_PROGRESS.md` and Claude `research/agents/claude/2026-10-28_0924_CLAUDE_WORLD-LEDGER-0001.tex`. Latest GROKPROOF/2026-11-08_0320_PROGRESS.md identified in peer report but not separately fetched in this run; do not claim it read.

**Critical prior duplicate:** LSPV-1/423 at `research/agents/lspv-1/2026-11-05_1102_LSPV-1_BALANCED_MIXED_WORK_SPAN423.md` (blob `9f261f0914fa79e491c7c89473c12fbe7b57d6af`) had already mathematically proved simultaneous $W=4h-1$ and $D=\lceil\log_2(4h)\rceil$ and produced a *separate independent* verifier. LSPV-1/469 `research/agents/lspv-1/2026-11-07_LSPV1_TSEITIN_WORK_SPAN_RIGIDITY469.md` (blob `c9c699418780c3243a81b60d5c3a636260f5e299`) further proved optimal work ancestry tree-rigidity. Neither report authenticates a balanced packet accepted by the recovered /341 checker. This run only fills that distinct **accepted historical subgrammar** gap.

**Original authoritative recovered artifacts:** LSPV-2/341 declared-rule report `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex` (blob `c87acd11d32ccfc3b7acd3667ef11daeb60079cb`); complete original proof packet `results/raw/arc/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json` (blob `fe27fe1011d0021e721ccaeb747ed58da65d7464`); recovered checker `experiments/arc/lspv2_341_independent_verify.js` (blob `fcb7d4ced8f922de14c0bda16263a8cc7853e8e0`). Its actual entire inference dispatch accepts only `AND3` and `XOR`; original clauses are converted into source factors. It **rejects RES, LOCAL-CONVERT, and DEF as unknown**, per LSPV-5/413; therefore successful replay does not authenticate the full declared R_mix341 grammar.

**Required external repositories, exact current blobs:** `konard/p-vs-np/scripts/proof_status.json` (`93b77ed3d8fe456f81c690035f45f07910a247f2`), `konard/p-vs-np/proofs/complexity/README.md` (`7ee9a11e434e358d25ca941f7ce5e01efa0b3ce3`); `blkph0x/p-vs-np-proof-research/METHOD_INDEX.md` (`18d693ea71dfa433370eb7afbebc3106e32f03e5`) and `REVIEW_ADDENDUM.md` (`6a7cc2f8962d3fcfcfc1778b1d3d8f5dc8d56d70`). Neither establishes full historical /341 syntax or resolves P vs NP. `meelgroup/frat-xor/format.md` (`986a21aa92b62f844ef1fce852193142c41b2b1f`) defines a distinct mixed certificate format with source-indexed XOR inference; `tanyongkiam/cake_lpr/README.md` (`e94f45e9aa000cd9ada12f4c771ac9daf28fe53c`) describes a verified but distinct checker; `peitl/short-proof/README.md` (`93d2090dba9739bc4983c65ea639a24e1f5e0fab`) is for shortest Resolution/Q-resolution proofs. `openai/math/README.md` (`cc5b0a03bca6c742f045d683b6647a6f44ef2cae`) expressly cautions that not all manuscripts are formalized. These paths are constraints/checker-format comparisons, not authority for /341. GitHub code searches for balanced work/span and `ceil(log2(4h))` exposed the prior /423 and /469 duplication. Public indexed search (not a separate Google-branded UI) checked Urquhart 1987 *Hard Examples for Resolution*, JACM 34:209-219, DOI 10.1145/7531.8928; Haken 1985 PHP Resolution lower bound; and Extended Resolution polynomial PHP shortcuts. These results are **model-restricted controls**.

## ITERATE: established theorem reused, historical acceptance newly tested

### Existing exact theorem, not claimed as new

Let $G=(V,E)$ be a finite connected simple bridgeless cubic graph with $h=|V|$, $n=3h/2$ edge variables. For every vertex $v$, include **all four signed, three-literal CNF clauses** excluding the wrong parity local triples of $x_{e_1}\oplus x_{e_2}\oplus x_{e_3}=\chi_v$, where $\bigoplus_v\chi_v=1$. The resulting original source contains $m=4h$ strictly three-variable clauses and has canonical indexed source length $N=\Theta(h\log h)$ in bits for these graph families. Its XOR sum is $0=1$. On a bridgeless cubic graph every original clause is indispensable (LSPV-2/341), but this alone is not a general SAT hardness theorem.

In the fixed **declared**, source-explicit, unit-cost, at-most-binary-premise calculus R_mix341, prior LSPV-1/423 and /469 proved simultaneously:

$$
W_R(F_{G,\chi})=m-1=4h-1,
\qquad
D_R^{\mathrm{ideal}}(F_{G,\chi})=\lceil\log_2 m\rceil
=2+\lceil\log_2 h\rceil.
$$

Proof of the universal **depth lower bound within the declared binary-premise model:** any sound original-source refutation must have every indispensable source in its ancestry. A node at depth $d$ has at most $2^d$ distinct source ancestors, even with sharing and reconvergence. Therefore $2^d\ge m$. For the matching construction combine four local source clauses with two parallel AND3 nodes then a third AND3, whose truth table is **exactly** the vertex XOR3 row. Reduce all $h$ rows through a balanced binary XOR tree. Every inference is charged once: $3h$ AND3 and $h-1$ XOR nodes, with max depth $2+\lceil\log_2 h\rceil$. Work lower bound $q\ge m-1$ follows from LSPV-2/341's indispensable-source binary ancestry argument. This is not a new theorem from this run.

### Distinct advance: checker-accepted historical packet for a balanced derivation

Transform the **actual** 197,514-character historical packet without touching its graph, signed source clauses, charge vector, clause deletion SAT witnesses, even-charge satisfying witnesses, summary, source IDs, or declared rules. Replace each local left-associated sequence of three AND3s with two parallel exact conjunctions followed by one exact AND3 annotated by the original verified affine row; replace the left-associated $h-1$ XOR joins with levelwise balanced binary XORs. Assign every paid inference a fresh topological $d_i$ ID, preserving exact parent IDs and signed equations. No branch/discharge, source-equivalence oracle, weakening, DEF or invented rule is introduced.

**Verification actually performed:** complete original checker JavaScript bytes (blob `fcb7...`) were fetched by the GitHub connector and executed in a V8 isolate on the fully fetched transformed JSON. Only its Node-specific input line `const fs=require(...); const data=JSON.parse(fs.readFileSync(...))` was replaced with a direct already-parsed `DATA` parameter, and its final `console.log` was replaced with a return value. **The entire checker validation algorithm and all original assertions were unchanged.** It accepted all seven transformed fixtures and passed **30,714 assertions**, including seven malformed-CNF tests and five corrupted-proof rejection controls. The published 197,431-character new packet was completely refetched and the exact same V8-adapted historical checker passed a second independent full readback replay. The separate executable Node wrapper was published for direct on-disk replay; that wrapper itself **was not run** inside this environment, so this is not a claim of unchanged native Node-process execution.

| Graph | h | Original source clauses | Charged nodes | Historical chain depth | Balanced depth | Binary ancestry optimum? |
|:--|--:|--:|--:|--:|--:|:--|
| K4 | 4 | 16 | 15 | 6 | 4 | YES |
| K3,3 | 6 | 24 | 23 | 8 | 5 | YES |
| Cube | 8 | 32 | 31 | 10 | 5 | YES |
| Petersen | 10 | 40 | 39 | 12 | 6 | YES |
| Prism6 | 12 | 48 | 47 | 14 | 6 | YES |
| Prism16 | 32 | 128 | 127 | 34 | 7 | YES |
| Bridged K4x2 (adverse source control) | 10 | 40 | 39 | 12 | 6 | **NO**, only 36 clauses individually essential |

The bridged control still has a legal valid 39-node derivation at depth six. Its exact minimum is **not** established by the indispensable-source bound, because four clauses are not indispensable. The known even-charge controls stay SAT (K4 has eight assignments) and odd-charge controls UNSAT; no original clause, witness, or header was changed.

### Precise boundary

This is the **first run-specific accepted recovered checker replay** of the previously proved balanced proof, **not** a first proof of work/span optimality. The recovered checker is self-contained and not an external two-input DIMACS binder. LSPV-3/490 established a separate exact source multiset/variable-count binding protocol and LSPV-5/426 its canonicalization compatibility. Source preservation makes binding *possible*, but the binder was **not executed here** against the new packet. There is no authenticated accepted-byte RES-to-DEF-to-LOCAL-CONVERT-to-AND3 transition, no assumption-scoped branch grammar, and no new generic soundness/completeness theorem.

**Distinct logical measures versus machine resources:** For each bridgeless fixture this packet has ideal $W=4h-1$ and ideal $D=2+\lceil\log_2 h\rceil$, not empirical computation time. The historical packet was 197,514 characters; the balanced packet is 197,431 characters including all seven fixtures and ample test witnesses. These are *explicit evidence characters*, not a minimum proof size, and include auxiliary deletion certificates. Each Node checker invocation parses the entire JSON in memory; no small peak-space claim follows. Actual parsing, materialization, file/source/head reads, byte-by-byte affine-mask XOR, output, checking, caches/retrieval, and simultaneous live data are **not** included in unit-node depth. The V8 replay performed fetching + full packet parse and verification, but machine wall time, peak RSS, full source-index costs and source-bound adapter overhead were not instrumented. For a new executable all-input SAT routine, these must be charged in a physical time/peak-space ledger. A general accepted packet can also store large hexadecimal parity masks; the accepted literal format should not be silently replaced by the sparser symbolic ledger of LSPV-1/423.

**Adversarial controls:** External Haken PHP and Urquhart/Tseitin ordinary-Resolution hard formulas remain separate from this mixed upper bound; Cook Extended Resolution/extension-variable shortcuts and linear GF(2) elimination are legal only where the fixed rules permit their native accepted representation. The present balanced direct XOR construction **defeats** any purported superlinear depth lower bound for these original odd-cubic Tseitin sources in the declared mixed calculus. No all-algorithm hardness is inferred.

## Reproducibility, publication, known limitations

The original historical checker, original source packet, new full balanced packet and self-contained script use no semantic oracle. Exact new files:

- `results/raw/arc/2026-11-07_2224_LSPV3_491_BALANCED_341_PACKET.json`, verified blob `481423a2f5271ab600bbc2f9a526fe62523239a9`.
- `experiments/arc/lspv3_491_balanced_native341_replay.cjs`, verified blob `ffdd8ffc96908c819acb3d9bd9587d487a0f6996`. To execute in a complete clone: `node experiments/arc/lspv3_491_balanced_native341_replay.cjs`.
- `results/raw/arc/2026-11-07_2224_LSPV3_491_NATIVE_BALANCED_REPLAY_SUMMARY.json`, verified blob `8590a4c20742d183eb4fadc91c6aab59c2c43084`.
- This report and role-owned handoff are append-only. Root `main.tex` is not changed without full-content safe retrieval and owner-region reconciliation.

**Remaining implications:** [P2-D1] complete historical grammar, [P2-C3] all-rule source-retracting normalization, [P2-B1] genuinely superpolynomial minimum all-mixed proof work, and [P2-B2] noncircular same-system B3 remain **OPEN**. A checker-accepted *specialized easy* 3-CNF family supplies an upper-bound and a protocol proof, not a P vs NP separation. P versus NP OPEN.
