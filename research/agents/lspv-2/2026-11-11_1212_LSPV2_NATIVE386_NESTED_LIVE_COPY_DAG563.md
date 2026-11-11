# LSPV-2/563: A terminal-live nested copy-definition chain in the original /386 checker

**2026-11-11 12:12 PST | SAT-Circuit Reduction Builder | historical Route A | PROVED/RESTRICTED construction and COMPUTATIONAL original-code replay | P versus NP OPEN**

## Candidate construction, falsifiers, and exact epistemic boundary

**One candidate:** From the byte-exact, original-/386-full-CLI-accepted signed K4 certificate of LSPV-2/562, insert a variable-length chain of paid conservative AND2 *copy gates* whose defining facets are consumed by an oriented Resolution detour. Make every inserted proof record, each new paid gate owner, and every shared intermediate parent part of the ancestor DAG of the final empty clause. The detour exactly recreates a genuine original SOURCE clause; reconnect one existing terminal-live parent to that new clause. For arbitrary nonnegative chain length k with safely representable fresh wire IDs, prove its native original-checker acceptance and exact paid cost.

**Falsifiers registered before execution:** F1: any signed parent port, pivot, derived clause or gate definition is not accepted by the unmodified original verifier; F2: a new owner or one of its defining facets is dead rather than an ancestor of the terminal contradiction; F3: the real checker rejects a valid chain because of unknown freshness, owner, record count or full-CLI mutation requirements; F4: malformed source/owner/port/parent/payment/terminal packets are nevertheless accepted. F1–F3 were excluded by an explicit signed induction, terminal ancestry traversal and original-checker replay; seven hostile F4 packets were all rejected. No full-historical-calculus falsifier has been excluded.

**AUTHORITY:** The only executable source-authenticated checker used is the unchanged archived sibling \`experiments/arc/lspv2_386_independent_verify.js\`, Git blob \`338305c0ce101704205e57543756b8127074a986\`, SHA-256 \`22d12f665fecede1a047ea20c0c2d3f245c7195ce5df44f342891198ea04a113\`. It checks its in-band signed cubic-Tseitin SOURCE occurrences, strictly oriented RES, paid conservative AND2 definitions, and free defining facets. Its complete CLI additionally applies 11 built-in mutations. It does **not** authenticate the historical full \`R_mix341\`, AND3, GF(2), LOCAL-CONVERT, private/exported wires, branch contexts, weakening, discharge, joins, deletions or their fixed rule weights. The independently published *reference constructor* below is **not an authoritative checker**.

## Exact starting source, typed configuration, and theorem

The baseline original-CLI-accepted source packet is
\`results/raw/arc/2026-11-11_1112_LSPV2_562_ACCEPTED_CONE_W29.json\`,
Git blob \`318c52d99977ea4e91bc8554051138a700c1dc94\`: 17 original signed SOURCE occurrences, 28 paid oriented Resolution inferences, one paid AND2 owner \`[0,8,1,4]\`, no defining facets, 45 records, logical \`W=29\`. The target original SOURCE occurrence (record 7) is the exact signed clause

$$
S = [-1,-4,-5,-7].
$$

For each integer $k \ge 0$ whose new wire IDs fit the checker's safe-integer namespace, append $k$ globally distinct AND2 owner declarations

$$
D_j=[j,\,8+j,\,7+j,\,7+j],
\qquad 1\le j\le k.
$$

Owner $D_j$ declares the *fresh* output $z_{8+j}$ from the same previously declared input $z_{7+j}$ twice, so as a Boolean function $z_{8+j}=z_{7+j}$. No owner, inference or wire is free merely because the semantics is an identity. For each new owner, use both signed defining facets

$$
[7+j,-(8+j)] \quad\text{and}\quad [8+j,-(7+j)].
$$

The existing original paid owner 0 supplies \`[1,-8]\` and \`[8,-1,-4]\`. These are two of its genuine defining facets, and require zero additional inference cost after the owner charge.

Construct the oriented RES chain by first resolving \`[1,-8]\` against $S$ on pivot $1$. This gives
\`[-4,-5,-7,-8]\`. For $j=1,\ldots,k$ use the forward facet to replace the current negative wire by negative $z_{8+j}$, resolving with pivot $-(7+j)$. For $j=k,\ldots,1$, use the backward facet and oriented pivot $-(8+j)$ to return to negative $z_8$. Resolve against \`[8,-1,-4]\` on pivot $-8$; the result is **exactly** $S$, with all signed literals and no tautology or weakening.

Keep all 17 SOURCE occurrences unchanged and ahead of the new records. Insert \`2+2k\` genuine DEF facet records and \`2+2k\` genuine paid RES records after them. Shift all later original derived-record indices by $\delta(k)=4+4k$ and redirect one old terminal-live parent formerly referencing SOURCE record 7 to the new copy of $S$. The original 28 RES records remain distinct and otherwise unchanged. All new facets and all new RES records become terminal ancestors. All new paid owner outputs are used by those terminal-live DEF facets.

**Theorem 563.1, restricted to the unchanged original archived /386 full checker.** The described packet $P_k$ is accepted by that complete checker for every valid safe-integer $k\ge0$. Its exact checker's logical-work tariff and proof-row counts are

$$
\boxed{
W_{386}(P_k)=31+3k,\qquad
R_{386}(P_k)=49+4k,\qquad
N_{\rm RES}(P_k)=30+2k,
}
$$

$$
N_{\rm paid\ owner}(P_k)=1+k,\qquad
N_{\rm free\ DEF\ facet}(P_k)=2+2k.
$$

The cost is the number of distinct paid Resolution *occurrences* plus the number of distinct paid owner IDs, once each; SOURCE and already-owned defining facets cost zero additional work. The end-to-end paid-RES dependency span for the constructed packets is $9+2k$, a distinct measure from work, evidence bytes, construction time and peak memory.

**Proof.** The original K4 SOURCE and 28 old RES records already satisfy the original checker. The original owner 0's two stated facet clauses are exactly members of \`views(8,1,4)\`. Each newly declared copy owner has a fresh output; its input is either original output 8 or the immediately previous newly defined output. Its two stated clauses are members of \`views(z,z_{prev},z_{prev})\` after canonical literal sorting and duplicate removal. The first new RES follows from $1$ against $-1$ in $S$, yielding the signed clause above. Inductively the forward RES on $-z_{prev}$ and its opposite $+z_{prev}$ preserves all other signed literals and advances exactly one negative wire; the backward RES reverses this using the second definitional facet. The final RES on $-8$ against $+8$ in the exit facet restores $-1$ and $-4$, exactly $S$; no new opposite pair appears. Thus every inserted RES has exactly two earlier valid parents and the exact checker-normalized signed resolvent. Reindexing all later parents preserves their original proof values. Replacing a single old terminal-live SOURCE parent by the new equal signed clause preserves the old RES check at that node and inductively all descendants. The 17 immutable SOURCE occurrences and final empty clause remain. The full CLI requirements, including an Array record container, nonempty owner declarations, and terminal-pivot negative test, remain satisfied. The new records are on the terminal ancestor path by construction. The summary counts follow by adding $k$ paid owners, $2+2k$ free facets and $2+2k$ paid RES records to the W29 seed. QED.

**Restricted inverse.** On the explicitly constructed family, erase only the inserted facets and $2+2k$ RES records, undo the index shift and restore the one replaced SOURCE-7 parent. The exact W29 original full-CLI-accepted seed is recovered, showing the detour is not an unavoidable computational resource. It is a *positive legality/realisability control* and a warning against treating semantically trivial gate identities as forbidden; not a lower-bound candidate. This inverse is not a general full-calculus normalization and assumes no context or mixed-rule parent side conditions.

## Original-code computational verification and raw evidence

In hosted V8, the original unmodified \`checkProof\` body and complete original command-line test loop were evaluated with temporary I/O adapters (the SHA field emitted by the temporary \`crypto\` adapter is *not* a real digest). Exact Git blob values were independently retrieved from GitHub; the original mathematical rule dispatcher and all 11 built-in hostile mutations were not rewritten. This was **not** a native operating-system Node.js subprocess run. The published Node.js subprocess replayer is syntax-checked but not separately executed end-to-end this run.

| k | Paid W | SOURCE | RES | Paid owners | Free DEF facets | Records | UTF-8 bytes | RES span | Original-CLI assertions |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 31 | 17 | 30 | 1 | 2 | 49 | 3,089 | 9 | 3,454 |
| 1 | 34 | 17 | 32 | 2 | 4 | 53 | 3,319 | 11 | 3,577 |
| 2 | 37 | 17 | 34 | 3 | 6 | 57 | 3,554 | 13 | 3,849 |
| 4 | 43 | 17 | 38 | 5 | 10 | 65 | 4,037 | 17 | 4,393 |
| 8 | 55 | 17 | 46 | 9 | 18 | 81 | 5,001 | 25 | 5,481 |

All five positives were accepted, including all 55 original built-in corruption controls, with **20,754 positive-case original-checker assertions**. Seven explicitly constructed additional $k=2$ hostiles were rejected: wrong original signed source, undefined facet owner, forward parent, incorrect copy facet, undercharged cost, missing paid owner declaration, and false terminal clause. This is a finite computational cross-check of the symbolic theorem, not an asymptotic empirical cost law.

**Executable reference generator + OS replay:** \`experiments/arc/lspv2_563_native386_nested_copy_replay.cjs\`, Git blob \`2560f2b9f1502e7dd232a45439744eb1975fca15\`. It SHA-pins original seed/checker, deterministically regenerates $k=0,1,2,4,8$, verifies committed bytes for $k=1,2,4$, invokes the unchanged original checker as a Node.js subprocess, then runs the seven negative controls. It has passed syntax validation but not complete OS execution in this run.

**Exact byte-exact accepted packets:** \`results/raw/arc/2026-11-11_1212_LSPV2_563_ACCEPTED_NESTED_COPY_K1.json\` (blob \`f0b0ab006c16b176e9c962443e4a6d76e5d00155\`), \`results/raw/arc/2026-11-11_1212_LSPV2_563_ACCEPTED_NESTED_COPY_K2.json\` (blob \`798acc52de1819af71ab09d22011a2459d13344f\`), and \`results/raw/arc/2026-11-11_1212_LSPV2_563_ACCEPTED_NESTED_COPY_K4.json\` (blob \`90749002238e0508913efacbfd810b36e63149e7\`).

**Machine-readable hosted-V8 original-checker raw result:** \`results/raw/arc/2026-11-11_1212_LSPV2_563_NESTED_COPY_HOSTED_V8_RAW.json\`. No random seed: the construction is deterministic.

## Concrete-to-abstract relevance, CEGAR, and mandatory shortcuts

For the *authenticated /386 sublanguage only*, take a concrete state
$C=(b,P,s,i,D,G,K,E,H,W,g)$ holding exact input byte sequence $b$ and Node decoder/parser result $P$, an independent-source binding field $s$ if supplied, current record index $i$, globally paid owner IDs $D$, fresh wire declarations $G$, signed clause history $K$, oriented parent-port edges $E$, paid node occurrence/DAG ledger $H$, accumulated logical work $W$, and full-CLI goal predicates $g$. The restricted abstraction $\alpha(C)$ retains source occurrence identities and digests, owner/wire dependencies and freshness, chronological oriented parent-port clause values, paid owner and RES occurrence identities, and the terminal/full-CLI acceptance predicates. Its $\gamma$ consists of **all byte-level configurations that parse and validate to those observations**. Each *existing authenticated* concrete transition is represented by an abstract transition with the same cost, which is no greater than the concrete cost, and every /386 completion remains represented. In particular each copy-owner step is paid once, both facets are free only after their owner exists, and both forward/backward RES steps are separately paid. This provides a direct local simulation invariant for this restricted construction.

A cheaper semantic label quotient that discards contexts, declaration chronology, paid identities or assumed source binding may spuriously elide or mischarge the chain. Replaying candidate shortcuts against the original checker distinguishes realizable early-clause reuse (genuine) from invalid future-wire reuse (spurious); any CEGAR restriction must be justified separately by a *new* soundness proof. The natural zero-detour normalization for these particular packets is genuine, so an abstraction minimizing over proof choice must keep it as an option and may not infer an inflated work lower bound from the deliberately longer path.

**Crucially**, there is no authenticated full concrete state or complete $\alpha,\gamma$ for the historical \`R_mix341\`. Any unverified AND3, GF(2), LOCAL-CONVERT, exported/private wire, split, weakening, discharge, join or delete operation remains an unknown *MAY* transition conservatively overapproximated at a cost no greater than its authenticated tariff, never silently assigned impossible. The full cross-rule RES-to-AND3 and DEF-to-LOCAL-CONVERT port grammar remains absent. No claim of full-calculus CEGAR soundness, P2-B1 lower bound, or noncircular SAT-in-P bridge B3 is made.

## Corpus and literature reconciliation

**CORPUS REVIEWED:** Both root trackers \`proof1.txt\` and \`proof2.txt\`, issue #3 and latest relevant comments, \`AGENTS.md\`, \`CODEX.md\`, \`.codex/skills/pnp-research/SKILL.md\`, full repository tree (16,509 entries), original /386 checker, original /341 fixture research, current peer LSPV-1/579, LSPV-3/575, LSPV-4/548 and LSPV-5/493, LSPV-2/539–562 including the actual 540–549 raw-byte/syntax investigations, and newest coordinated handoffs. Historical low-level native parser reports were compared with original code. The prior /553, /554, /555, /560–562 constructions establish individual zero-paid facets, topological owner declaration, a single connected DEF/RES splice and paid-RES value merging. This new finite chain combines *arbitrary-depth transitive owner dependencies* with *terminal-live use of both copy facets and every newly charged owner*. No full historical checker was discovered in the searched repository.

**Precedence and contradiction audit:** LSPV-1/579 improves a **different fixed original signed bridge source** to W61; it neither competes with nor supplies lower bounds for this K4 chain. LSPV-5/493 found that the exact published LSPV-3/575 runner exits nonzero after performing tests due to a summary field typo; that runner is not used here. The recent original-/386 proof normalizers emphasize legitimate low-work alternatives and CLI-specific owner requirements; our construction leaves the baseline cheaper alternative intact. Nothing changes root proof-chain obligations.

**Primary literature and reference formats:** Cook–Reckhow (1979), *The Relative Efficiency of Propositional Proof Systems*, JSL, DOI 10.2307/2273702, defines general proof-system verification without authenticating a particular project's grammar. Cousot–Cousot (1977), POPL, DOI 10.1145/512950.512973, supplies the abstract simulation framework, not an SAT lower bound. Baek–Carneiro–Heule, *A Flexible Proof Format for SAT Solver-Elaborator Communication*, arXiv:2109.09665, and the original [FRAT-XOR format](https://github.com/meelgroup/frat-xor/blob/main/format.md) demonstrate genuinely separate proof serialization and XOR interfaces, not R_mix341 interoperability. CEGAR planning/reference formalisms do not authorize deleting unverified mixed operations.

**WHAT CHANGED:** Added a source-pinned, active nested-copy full-CLI-accepted sublanguage control, proved restricted transformer/ledger formulas, new accepted-byte packets and a reproducible reference Node OS-runner. **ADOPTED:** /562 authoritative sibling checker, immutable SOURCE occurrences, once-paid owner identity, signed parent ports. **REJECTED:** treating semantically redundant definitions as free to construct, assuming an equal-clause quotient preserves mixed-rule contexts. **RETIRED:** no historical rule or tracker node. No all-input theorem or algorithmic lower bound.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** P2-D1, P2-C3, P2-B1 and separate P2-B2/B3 remain OPEN. P1-01/P1-03/P1-04 remain OPEN. No scheduled identity, historical weight, title, timezone, scientific label or ownership boundary is changed.

**Next decisive acquisition:** Obtain an authoritative single historical original parser/dispatcher and a source-bound, truly cross-rule RES-to-AND3 or DEF-to-LOCAL-CONVERT accepted packet. Test at least two corrupt typed-port/context variants against that checker before extending full cost-sound alpha/gamma.

**P versus NP remains OPEN.**
