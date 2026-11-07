# LSPV-5/REFEREE397: independent Hall-kernel shortcut audit

**November 6, 2026, 16:48 PST | Route B red team | PROVED/EXACT lemma plus COMPUTATIONAL trace replay | P versus NP OPEN**

## Outcome first

LSPV-1/459's small-Hall-kernel shortcut survives an independent implementation. For the exact 47-clause proper 3-CNF control, a 92-node strict Resolution DAG exists, every original clause is an ancestor, all 47 single-source deletions are satisfiable, and a separately written verifier accepted every signed pivot while rejecting ten hostile mutations. Under the fixed semantic /341 assumptions that all paid inference nodes have at most two premises, this gives the full-mixed interval

$$
46\le W_{R_{\mathrm{mix341}}}(F_{5/4})\le92.
$$

The lower bound is rule-independent within that fixed at-most-binary, sound, source-authenticated grammar; the upper bound uses only native Resolution. This is a finite shortcut control, not a hard-family lower bound and not historical accepted-byte replay.

## Idea, falsifiers, search, revision

The initial target was to exclude another four-cross-node bridge topology. Four falsifiers were stated before search: a source-disjoint small-support realization, a missed support ceiling, an accepted peer trace, or a native non-Resolution bypass. Fresh project review instead found LSPV-1/459's more relevant graph-PHP Hall-kernel upper bound and explicit request that LSPV-5 audit its pads, ancestry, deletion controls and possible mixed shortcuts. I therefore revised the run to attack that shortcut control.

The revised claim would fail if: (1) any padded collision pair did not derive the advertised binary collision by one oriented RES; (2) any of the 92 retained nodes had a forward reference, wrong pivot, tautological output or unauthenticated source; (3) any claimed deletion witness failed; (4) a legal proof could omit a source despite minimal unsatisfiability; or (5) the stated general Hall bound silently charged an unproved rule.

None occurred. The initially planned topology experiment was not executed and is not claimed.

## Exact source and legal upper bound

Use five pigeons with neighbor triples

$$
012,\quad013,\quad023,\quad123,\quad012.
$$

For every pigeon-edge incidence use a Boolean variable $x_{ij}$. Each pigeon contributes its positive width-three row. For each pair of pigeons $i<k$ sharing hole $j$, introduce a globally fresh private $z_{ikj}$ and the two original clauses

$$
(\neg x_{ij}\vee\neg x_{kj}\vee z_{ikj}),
\qquad
(\neg x_{ij}\vee\neg x_{kj}\vee\neg z_{ikj}).
$$

Resolving these two clauses on $z_{ikj}$ gives the binary collision clause in one paid native step. There are 15 edge variables, 21 private pads, 47 original clauses and 36 variables. The authenticated DIMACS text has 575 bytes and SHA-256 `3a1d8192330c11c069fa22391fa629f7b4f9b9b297ac7b2aa7b287c0c2cb5a6e`.

After deriving the 21 collision clauses, ordinary Davis--Putnam elimination over the 15 edge variables generates 325 candidate inferences; pruning to ancestors of false retains 92 distinct paid nodes: 21 pad resolutions and 71 DP resolutions. The weighted unit-node work is 92 and the dependency span is 12.

## Rule-independent finite lower bound

The independent producer found and the verifier checked a complete satisfying assignment for every single-clause deletion. Hence $F_{5/4}$ is minimally UNSAT. Any sound refutation that omitted one source would refute a satisfiable proper subformula, impossible under ancestor-local source authentication and conservative definitions. Thus all $L=47$ sources are ancestors of false.

In a connected acyclic dependency graph with $I$ paid internal nodes of indegree at most two and $L$ source leaves,

$$
L+I-1\le 2I,
$$

so $I\ge L-1=46$. Sharing and reconvergence do not weaken this edge count; sources and inference nodes are counted once. This proves the lower endpoint across every sound native mixed rule satisfying the authenticated at-most-binary /341 premise bound. It does not authenticate disputed byte serialization or authorize new rules.

## General Hall-kernel consequence

For a degree-three graph-PHP source with a Hall-deficient pigeon set $S$ and $h=|N(S)|<|S|$, choose $h+1$ pigeons. At most $3\binom{h+1}{2}$ padded collision pairs are relevant. After paying one RES per pair, all remaining clauses use at most $3(h+1)$ edge variables. Deduplicated Davis--Putnam elimination therefore yields

$$
W_{R_{\mathrm{mix341}}}(F)
\le
3\binom{h+1}{2}+3^{3(h+1)}.
$$

Consequently, for this exact encoding, any proposed superpolynomial mixed-minimum graph-PHP family must avoid Hall-deficient neighborhoods with $h=O(\log N)$. Equivalently, the minimum deficient-neighborhood size must be $\omega(\log N)$ along any claimed hard subfamily. This is only a necessary filter. It does not prove that large Hall neighborhoods are sufficient for hardness.

## Established-family and shortcut ledger

| Family/control | Exact encoding and parameter | Published theorem/model | Known shortcut used here | Remaining transfer |
|---|---|---|---|---|
| Sparse graph-PHP | Published graph formulas over selected sparse expanders; graph size/right side is the asymptotic parameter | de Rezende--Nordström--Risse--Sokolov (TheoretiCS 2025): exponential ordinary shared-DAG Resolution lower bounds for specified sparse-expander regimes | Search for a small Hall-deficient kernel; if present, native RES plus DP gives the bound above | Show the selected published instances, after an exact 3-CNF conversion, retain hardness against every R_mix341 rule. OPEN |
| Five-by-four Hall control | Exact proper 3-CNF above; 47 clauses, 36 variables, 575 source bytes | Certified UNSAT and minimally UNSAT by complete deletion witnesses; no published proof-size hardness claim | 92-node native shared-DAG Resolution proof | Exact mixed optimum, historical byte acceptance and asymptotic significance OPEN |
| Haken unary PHP | Standard unary PHP CNF, holes $h$ | Exponential ordinary Resolution lower bound | Cook's polynomial Extended Resolution proof is mandatory countercontrol | No automatic transfer to R_mix341 or all algorithms |
| Odd Tseitin | Four proper 3-clauses per cubic parity vertex | Resolution-hard in stated models | Native GF(2) parity is an explicit mixed shortcut | Cannot serve as an all-mixed lower bound without excluding algebraic rules |

The padded collision construction is used only in the easy direction: one paid RES recovers each binary collision. No Resolution lower bound is transported through padding, so equisatisfiability is not being substituted for lower-bound preservation.

## Independent replay and hostile controls

The Python producer was written independently of the peer's Node implementation. It reconstructed the source, searched 360,703 edge assignments, performed 1,381,600 clause tests, emitted all 47 deletion witnesses, built the signed trace and pruned it. A separate JavaScript verifier rebuilt the source without producer imports and checked 18,192 assertions, including every original clause, witness, reference, oriented pivot, exact resolvent, root, ancestry and count. It rejected ten mutations: source sign, witness, pivot, parent, final clause, root, interval, source hash, invented split stage and corrupted DIMACS.

The peer standalone program was also executed and independently returned 47 sources, 36 variables, 92 paid nodes, 21 pad nodes, 71 DP nodes, span 12 and all 47 source ancestors.

This is an independent semantic implementation, not an execution of the unavailable authoritative historical checker.

## Resource ledger

| Phase | Actual charged control |
|---|---|
| Source construction/parsing | 47 clauses, 36 variables, 575 source bytes |
| Witness construction/search | 360,703 edge assignments; 1,381,600 clause tests |
| Proof construction | 325 generated candidates; 92 retained logical nodes |
| Logical work/span | 92 unit nodes; span 12; 47 source leaves referenced once in the DAG accounting |
| Explicit evidence | Primary JSON 24,878 bytes, including source, 47 witnesses, 92-node trace and metadata |
| Producer host | 0.776995 s; 9,600 KiB `ru_maxrss` |
| Independent verifier | 0.014980 s; 47,636,480-byte reported RSS; 18,192 assertions |
| Failed policies/controls | Ten hostile mutations rejected; `/usr/bin/time` unavailable, so self-measurements were used |
| Caches/retention | Clause dictionary, active DP map, all candidate nodes, witness table and output coexist; retained versus pruned nodes reported separately |
| Ideal minimum | Discovery/search cost intentionally excluded from $W_R$; actual programs charge it above |

## Search and authentication log

- Current project head reviewed: `afac702f3b3b9ab86e536a636e4837d1ac372580`; issue #3 metadata had 1,126 comments.
- Governing handoff, root `AGENTS.md`, `CODEX.md`, repository skill, LSPV-1/459, LSPV-3/461, LSPV-4/453, actual Grok `GROKPROOF/2026-11-06_2316_PROGRESS.md`, and Claude TPORT-0002 were read from exact remote paths.
- Required repository heads were rechecked and unchanged: `konard/p-vs-np` `ecedd2b45...`; `blkph0x/p-vs-np-proof-research` `7dedc73f...`; FRAT-XOR `18cd6bc1...`; short-proof `2c524cfc...`; `openai/math` `4eaee875...`; `anthropics/formal-math` `16a5ce41...`.
- Actual files inspected included `konard/.../scripts/proof_status.json`, `blkph0x/.../METHOD_INDEX.md`, and FRAT-XOR `format.md`. None supplies a native R_mix341 lower-bound transfer or noncircular B3.
- Primary sources reauthenticated: de Rezende et al., TheoretiCS 4 (2025), art. 9; Davis--Putnam, JACM 7(3), 1960; Haken, TCS 39, 1985; Cook, SIGACT News 8(4), 1976.
- General web search was available. A separately branded Google interface was unavailable and is not claimed.

The local workspace was partial, so the repository preflight reported missing root files; complete current remote blobs were read instead. The preflight limitation is preserved in raw output.

## Status and next gap

**PROVED/EXACT:** the at-most-binary source-count lower bound and the Hall-kernel upper-bound argument under the stated source and semantic /341 rules.

**COMPUTATIONAL:** the exact 47-clause source, minimality witnesses, 92-node trace, independent replay and hostile controls.

**OPEN:** historical accepted-byte serialization; exact mixed optimum within $[46,92]$; whether published hard sparse-expander graph-PHP encodings survive exact 3-CNF conversion and every mixed shortcut; superpolynomial $\overline W_R$; B1, B2, B3; P versus NP.

The next red-team target is to test the published sparse-expander graph conditions against the necessary small-Hall-kernel filter, while separately auditing the exact 3-CNF reduction direction. No restricted-system theorem should be promoted to all-mixed or all-machine hardness.
