# LSPV-5/441: final-index counterexample and repair for the `/507` CAST certificate generator

**2026-11-08 10:51 PST | Route B independent red team | COMPUTATIONAL counterexample + PROVED/RESTRICTED repair | P versus NP OPEN**

**Affected tracker IDs:** new `[P2-L5-441]`; corrects executable-coverage evidence in `[P2-L3-507]` while preserving its separately declared-calculus theorem; refines `[P2-L3-503]`, `[P2-L3-504]`, `[P2-L3-505]`, `[P2-D1]`, `[P2-C3]`. `[P2-B1]`, `[P2-B2]`, `[P2-D1]`, `[P2-C3]` remain OPEN. `[P1-01]`, `[P1-03]`, `[P1-04]` were reviewed with no material change.

## IDEA and falsifiers fixed before search

The initial hypothesis was that the new `17..19` finite exact-Resolution range could be advanced by representing a peeled 17-node proof as a one-cycle residual with exactly one paid cross-edge. Four falsifiers were fixed before search:

1. an explicit legal 17-node proof;
2. a unicyclic residual not representable by the marked-edge recurrence;
3. rejection of a valid positive unicyclic control;
4. any branch-local source or clause counted twice across the cross-edge.

The fresh tracker read then exposed a new, more role-relevant peer claim `[P2-L3-507]`: an executable exact charged clause-to-factor comparison. Its published generator tested only clause positions `0,1,3`, while its theorem describes replacing an arbitrary original clause $C$. I therefore revised the run to the sharper falsifiable prediction: **every legal clause replacement index should generate and pass the claimed typed certificate, including the final index**. Falsifiers became an index-specific rejection, an accepted corrupt CAST, a cost mismatch, or failure of an independent reconstruction.

This revision follows evidence rather than abandoning the established-family priority: `/507` acts directly on the established odd-charge cubic-expander Tseitin strict 3-CNF and audits a proposed mixed-rule shortcut.

## SEARCH: complete continuity and exact sources

- Starting `main` head `fabce626794a6f04f010411297e097a85dd81b3e`, tree `66cb4d5a4f5e300f805e0c56446d703eb5bdbba8`.
- Complete `proof1.txt`: blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`, 18,553 characters.
- Complete `proof2.txt`: blob `b5236fb14c2a16061a1f447ce24d29702b615ba9`, 477,304 characters. The material new peer node was `[P2-L3-507]` after `[P2-L5-440]`.
- Current issue #3: all 1,362 comments read across 14 pages. Latest returned material included `[P2-L5-440]`; the new peer tracker/report was read directly even though its issue comment was not yet in the returned page set.
- Historical governing handoff at commit `4e29ed7646f484707767acb6e63ec5f38afd98a8`, blob `033b54b87b7cbe94912af5cf67daa52859143a07`, read completely. Current expanded handoff blob on `main`: `c3889a3e514ddbd747150dcb68607013a3b2d154`.
- Governance files read completely: `AGENTS.md` blob `19656af102604d5f0a721d548cf2e4e72a063561`; `CODEX.md` blob `754999f50de93cdb693ed37bc8110d31e9e698ef`; `.codex/skills/pnp-research/SKILL.md` blob `b8df83a7b0b1428f349b0e02ce1387d979e8db7f`.
- Peer/current files actually read: LSPV-1 `/510` blob `b5041eb141d814f1d3d82aa1d3ed90e5734edb5a`; LSPV-2 `/497` blob `51272c1031372adabb3e254ff4a3638eefb672f7`; LSPV-3 `/507` report blob `157666772469fe8eba3880421d73d77abc2ebd13`, source `experiments/arc/lspv3_507_paid_cast_exact.cjs` blob `f20a598c2c7bd76bb7e244817c147dbbf2827875`, raw blob `cc897c7a717338d420b984d2d1a54a5dc0595f9f`; LSPV-4 `/498` blob `46f726cafd6ddbee8cb370a1f394c76dedc68d8b`; own `/440` blob `45ca90a771e889b6474258b32caf29a332713561`.
- During execution, `main` advanced through LSPV-4 `[P2-L4-499]`; the complete report `research/agents/lspv-4/2026-11-08_1047_LSPV4_TSEITIN_CRITICAL_SIGN_BITPROBE499.md` blob `6b280192125e6260695736725ca8b59e8d288fd8` was read before publication. It is a restricted Route-A source-bit sensitivity result and does not alter this CAST audit or close any OPEN Route-B node.
- Actual Grok `GROKPROOF/2026-11-08_1130_PROGRESS.md`, blob `6942a99f176e996e9542f0386b7aa7fe2ce89e70`; Claude `research/agents/claude/world-ledger/README.md`, blob `de75a371ce3143a4495e6892df7fb04794a6b708`. Neither authenticates historical `R_mix341` bytes or supplies B3.

### Primary literature and queries

Actual public queries included `unicyclic underlying graph resolution proof DAG exact minimum multi conclusion`, `shortest resolution proof SAT encoding DAG sharing`, and `proof complexity lower bounds Res XOR tree-like dag-like Tseitin 3-CNF`.

- Sidorov et al., *How to Discover Short, Shorter, and the Shortest Proofs of Unsatisfiability* (arXiv:2411.07955; JAIR 86, 2026), provides exact Resolution minimization with proved branch-and-bound pruning, but no theorem automatically covering the proposed multi-target one-cycle state.
- Peitl and Szeider's shortest-proof SAT encoding remains a relevant exact optimizer control, not an authentication of project-specific typed rules.
- Itsykson, Riazanov and Smirnov, *Tight Bounds for Tseitin Formulas* (SAT 2022, DOI `10.4230/LIPIcs.SAT.2022.6`), is explicitly system-qualified and includes constructive shortcut comparisons.
- The inspected Res(PC)/Res(XOR) sources distinguish tree-like, regular and general DAG-like systems. In particular, restricted parity lower bounds cannot be promoted to the full historical mixed calculus.
- Search found no published unicyclic multi-conclusion Resolution recurrence with the exact required context semantics. No novelty is inferred from that absence.

A separate Google-branded client was unavailable; public web search and primary-source pages were used.

### Change-aware repository ledger

| Repository/path | Current head/blob | Result |
|---|---|---|
| `konard/p-vs-np/scripts/proof_status.json` | head `ecedd2b45f1c524d85c00b2da27a9c140025550c`; blob `93b77ed3d8fe456f81c690035f45f07910a247f2` | Unchanged; no historical mixed transfer or B3. |
| `blkph0x/p-vs-np-proof-research/METHOD_INDEX.md` | head `7dedc73f758dfbdc072e7aa29dfc08505761ebd5`; blob `18d693ea71dfa433370eb7afbebc3106e32f03e5` | Unchanged restricted-method inventory. |
| `blkph0x/p-vs-np-proof-research/INDEPENDENT_AUDIT.md` | blob `b30515cced93d8911a6415555ee9ec1444502d93` | Uniform constructive transfer remains open. |
| `peitl/short-proof/short.py` | head `2c524cfceecf68b56f51d23f6b63255b502856d3`; blob `6508dae79e341d7015949d5919de29a132fbf267` | Exact ordinary-Resolution optimizer control. |
| `meelgroup/frat-xor/format.md` | head `18cd6bc17af10a9891c10a846ce966166f9fe0dc`; blob `986a21aa92b62f844ef1fce852193142c41b2b1f` | Explicit separate theory types; not historical grammar. |
| `tanyongkiam/cake_lpr/README.md` | head `033aad53d1733bd4b8ca41cf6f1b5fb5d84f8de2`; blob `e94f45e9aa000cd9ada12f4c771ac9daf28fe53c` | Verified checker control, not minimum-proof or B3 theorem. |
| `marijnheule/drat-trim/README.md` | head `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`; blob `eb6ffcc4a85ff1c74a5995b6caae4372381dcd47` | DRAT control; different grammar. |
| `MassimoLauria/cnfgen/README.org` | head `24e633bdbed0d0998493bee99c42faf480c7dc96`; blob `9fba4e26f2a4cd10444a7226a7a3a7caa1762721` | Established formula generator; no mixed transfer. |
| `openai/math/README.md` | head `4eaee87548250b2682affda7d05d947c05554bae`; blob `cc5b0a03bca6c742f045d683b6647a6f44ef2cae` | No relevant theorem. |
| `anthropics/formal-math/README.md` | head `16a5ce41304fcdaea4e0be7c132e1c361dc26da5`; blob `1df53bfc14a022088d1b5757698f692bf79390b4` | No relevant theorem; repository status is not target proof. |

## ITERATE: exact counterexample and repair

The `/507` source builds the vertex-factor input IDs using

```js
j === d.sourceIndex.length - 1
  ? d.sourceIndex[j]
  : j === d.origin.indexOf(d.C) ? cast : d.sourceIndex[j]
```

When the replaced original clause is also the final original clause, the first arm wins. It selects the replacement source clause $A=(a\lor b\lor u)$ rather than the paid `CAST(C)`. The fresh variable $u=n+1$ then reaches `AND3`, whose own guard requires every factor variable to be an original variable at most $n$. The generated certificate is therefore rejected.

### Complete finite replay

For K4, K3,3 and the cube, all $16+24+32=72$ original clause indices and fees $w\in\{1,2,4\}$ were tested, for 216 parameter cases:

| Executable | Accepted valid cases | Rejected valid cases | Corrupted CASTs rejected |
|---|---:|---:|---:|
| Published `/507` generator/checker | 207 | 9 | 207 |
| One-line repaired generator with replaced-index test first | 216 | 0 | 216 |

The nine failures are exactly:

- K4 replacement index 15, fees 1, 2, 4;
- K3,3 replacement index 23, fees 1, 2, 4;
- cube replacement index 31, fees 1, 2, 4.

The upstream's original 27 advertised cases and 27 corrupt rejections also replayed exactly.

An independently authored Python reconstruction does not import the JavaScript implementation. It reconstructs every graph, strict signed 3-CNF factor, replacement source index and local parity table. It confirms that only the final-index selector exposes fresh $u$ to the original-support guard, while the repaired selector recovers exact parity on all 216 cases.

### What changes—and what does not

**COMPUTATIONAL counterexample:** the published executable does not cover every clause position described by the mathematical construction.

**PROVED/RESTRICTED repair:** selecting `CAST(C)` whenever $j$ is the replaced origin index removes the special-case failure. This is a syntactic selector repair; the independent truth-table check proves exact local parity for every finite tested position.

**Theorem not refuted:** `[P2-L3-507]`'s separate-calculus equality remains supported by its mathematical construction and lower-bound argument. The bug is in generator coverage, not a short proof bypass, B1 failure, B2 failure or B3 proof.

**No accepted-byte claim:** `/507` checks in-memory JavaScript objects. `packet_bytes` is the byte length of `JSON.stringify(nodes)` after generation; no parser for hostile external trace bytes is present. Thus this replay is actual published-code execution, but not execution of an authoritative historical accepted-byte checker.

## Established-family/theorem/encoding/shortcut ledger

| Family | Exact encoding and size | Established theorem/model | Known shortcut/control | Remaining transfer |
|---|---|---|---|---|
| Odd-charge cubic-expander Tseitin | For each degree-3 vertex, four signed width-3 clauses falsifying assignments of the wrong incident-edge parity; $h$ vertices, $3h/2$ edge variables, $4h$ clauses, $N=\Theta(h\log h)$ bits. | Exponential ordinary shared-DAG Resolution on suitable expanders; model-qualified. | SOURCE/AND3/GF(2) yields a linear proof in declared typed fragments; `/507` adds two RES steps and one paid CAST after one strict gadget replacement. | Authenticate every historical `R_mix341` transition and prove all-rule transfer. |
| Haken PHP | Pigeon clauses $\bigvee_j p_{i,j}$ and collision clauses $\neg p_{i,j}\lor\neg p_{i',j}$; not native 3-CNF without a preservation proof. | Exponential ordinary shared-DAG Resolution. | Cook extended Resolution has polynomial proofs. | Exact 3-CNF lower-bound preservation and mixed-rule transfer OPEN. |
| `/507` one-clause replacement | Replace $C=(a\lor b\lor c)$ by $A=(a\lor b\lor u)$, $B=(\neg u\lor c\lor v)$, $D=(\neg u\lor c\lor\neg v)$ with globally fresh $u,v$; $m=4h+2$. | Ordinary-Resolution hardness survives the stated substitution direction; `/507` equality is for separate $R_{CAST507}(w)$. | Two RES steps recover $C$, then paid CAST and algebraic linear proof. | Historical RES-to-factor path, fee, provenance and byte grammar OPEN. |

Certified UNSAT, proof-size hardness and empirical solver difficulty remain separate. These restricted proof-system results are not all-algorithm hardness.

## AND/OR, source scope and resource ledger

- Every original source is externally fixed by the generated instance object; the repaired CAST is used only where its recovered clause is exactly the replaced $C$.
- The exhibited proof is a shared acyclic DAG. No branch split/discharge, weakening, semantic oracle or new historical opcode was introduced.
- Logical work remains $m-1+w$ only in the separately declared calculus. Construction, all-index enumeration, failed cases, corruption tests, serialization, parsing, source/index reads, output, publication and readback are separately charged.
- Node replay: 216 parameter cases plus 216 corrupt controls and the upstream 27+27 controls; 0.262 s internal wall time; 69,660 KiB maximum RSS.
- Independent Python: 216 reconstructed cases and exact truth-table checks; 0.027 s; 8,960 KiB maximum RSS.
- Explicit new evidence comprises 11,824 bytes across two auditors and two raw JSON files, excluding the exact upstream and repaired source snapshots. SHA-256 digests: Node auditor `d2abb7e6da6b691300b25f44153399bdc6936052c3da946a964337eeca685e7a`; Python auditor `3832942bca2315ddcd2a2044e8f0b28f43bd56030fbba943421b7a1d1b4ecb33`; Node raw `db8f2a375780b24cdf795362d578cebd7c34d360e0f640ec1b2069c81c6b3be7`; Python raw `8d498e0527bb6702326eb8f8871495401046803671d31cf58ef1d2705f9feb3e`.
- Work, evidence bits, weighted critical path, realizable time and peak space are not conflated. No proof weight is interpreted as an FLMV machine lower bound.

## Actual advance, verification, publication status and precise gap

**Actual advance:** a final-index generator bug was reproduced and isolated in `[P2-L3-507]`'s executable evidence; a one-line repair covers all 216 graph/index/fee cases without weakening corruption checks. **Verification:** independent JavaScript execution and Python structural/truth-table reconstruction agree exactly. **Publication status:** artifacts were committed at `ef3e013e962566bcdcd12a1e25633c4c829c7569`; tracker node `[P2-L5-441]` and the exact prewrite archive were committed and fully read back at `447fa729a9ff4be5bc67603a025153494033e07f`; affected IDs were read back in issue comment `6725654325`. **Precise remaining gap:** recover and authenticate the actual historical `R_mix341` RES-to-factor/LOCAL-CONVERT accepted-byte route, or prove it unavailable; then establish an all-rule asymptotic lower-bound transfer and noncircular same-calculus B3. `[P2-D1]`, `[P2-C3]`, `[P2-B1]`, `[P2-B2]` remain OPEN. **P versus NP OPEN.**
