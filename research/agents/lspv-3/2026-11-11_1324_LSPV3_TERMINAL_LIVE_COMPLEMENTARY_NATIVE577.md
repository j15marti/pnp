# LSPV-3/577: Terminal-live complementary false wire in the original archived /386 certificate calculus

**2026-11-11 13:24 PST | Hypergraph & Proof Certificates | historical Route B | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN.**

## Candidate and four falsifiers

**Candidate [P2-D1 -> P2-C3]:** A signed complementary AND2 owner z = x AND NOT x, whose standalone false-unit derivation was authenticated by LSPV-3/576, can be a genuine ancestor of the terminal contradiction when a **later globally paid owner uses -z**. This is the precise counterexample to overgeneralizing LSPV-5/494 beyond its *isolated-owner* hypothesis. It does not contradict /494.

F1: the original verifier rejects a required signed DEF facet, oriented Resolution pivot, parent chronology or nested signed input. F2: the transformed terminal empty record does not depend on all eight inserted records. F3: a genuine source/paid-owner identity changes or count-once W differs. F4: any hostile wrong SOURCE, facet, pivot, forward parent, owner identity, future wire, collision or underpayment is wrongly accepted.

Two positive original-checker replays defeat F1-F3, and 11 hostile mutations are rejected under F4. A third positive control retains exactly the added rows but deliberately omits the terminal-parent rewiring, hence **all eight added records become terminal-dead** despite acceptance.

## Original source and checker authority

Pinned unchanged original archived /386 checker: experiments/arc/lspv2_386_independent_verify.js; Git blob **338305c0ce101704205e57543756b8127074a986**. Source packet: results/raw/arc/2026-11-11_0224_LSPV3_566_K4x3_CLI_ACCEPTED_PACKET.json; blob **4656b801feba72b84133bacad5ae18692a83fe03**.

The authenticated seed has 12 original graph vertices, 18 original edge variables, 49 guarded signed SOURCE objects, guard 19, 28 paid RES inferences and one paid unused binary owner [0,20,1,4]; W=29, 77 records. In all new packets the **entire original graph/charge/guard specification** and **all 49 signed SOURCE objects including their provenance, in original relative order**, are byte-value identical to the seed. Absolute record offsets may change. The original checker validates against its packet-internal graph, not an independently supplied immutable external CNF hash; source pinning is enforced by this reproducible audit and must not be falsely attributed to the checker.

Additional genuine native gate declarations:

~~~json
[[1,21,1,-1],[2,22,-21,1]]
~~~

The first is z=1 AND -1, hence false; the second is w=-z AND 1, hence equal to variable 1. Both owners are globally paid once, distinct and fresh; the second declaration reads an already declared signed auxiliary wire.

At record indices 17--24, immediately before the old first RES, insert these **eight exact native rows**:

~~~json
{"kind":"DEF","c":[1,-21],"parents":[],"gate":1}
{"kind":"DEF","c":[-1,-21],"parents":[],"gate":1}
{"kind":"RES","c":[-21],"parents":[17,18],"pivot":1}
{"kind":"DEF","c":[-1,21,22],"parents":[],"gate":2}
{"kind":"DEF","c":[1,-22],"parents":[],"gate":2}
{"kind":"RES","c":[2,3,-19,21,22],"parents":[0,20],"pivot":1}
{"kind":"RES","c":[2,3,-19,22],"parents":[22,19],"pivot":21}
{"kind":"RES","c":[1,2,3,-19],"parents":[23,21],"pivot":22}
~~~

The last of these is an exact copy of the original signed SOURCE clause C=[1,2,3,-19]. All original RES indices are shifted by eight where necessary; all original RES parents pointing to SOURCE index 0 are redirected to the newly derived record index 24. In particular the first old RES now resides at index 25 with parents [24,4]. The original final empty sink remains an accepted deduction, and **all new eight records lie on its full ancestor DAG**.

## Theorem 577.1: typed source-copy detour using a complementary paid gate

Fix a parsed packet accepted by the **original /386 mathematical-core** checker, a clean original SOURCE clause C with signed edge literal ell, and an insertion position after C but before its earliest later strict RES use. Let z and w be globally fresh wire names, distinct from every source, guard and already declared paid output, and let their owner IDs be globally fresh. Declare, in this order,

\[
z\leftrightarrow(\ell\wedge\neg\ell),\qquad
w\leftrightarrow(\neg z\wedge\ell).
\]

Four admitted zero-additional-cost signed defining facets suffice:

\[
(\neg z\lor\ell),\quad(\neg z\lor\neg\ell),\quad
(w\lor z\lor\neg\ell),\quad(\neg w\lor\ell).
\]

Put D=C without ell. The following four **oriented strict native Resolution** inferences yield the original clause again:

\[
\begin{aligned}
&\operatorname{RES}_{\ell}((\neg z\lor\ell),(\neg z\lor\neg\ell))=\neg z,\\
&\operatorname{RES}_{\ell}(C,(w\lor z\lor\neg\ell))=D\lor z\lor w,\\
&\operatorname{RES}_{z}(D\lor z\lor w,\neg z)=D\lor w,\\
&\operatorname{RES}_{w}(D\lor w,\neg w\lor\ell)=C.
\end{aligned}
\]

Every intermediate is clean because z,w are globally fresh and C is clean; every step has two chronological typed parents. Reindex the original entire record DAG and replace all subsequent original RES references to the chosen SOURCE record by the final new exact-copy node. Old Resolution clauses and results remain literally unchanged. No cycles are introduced, original source and paid-node identities are preserved, and no discovery cost or duplicated payment is introduced. Therefore the new mathematical-core proof is accepted and

\[
W_{\mathrm{new}}=W_{\mathrm{old}}+2\ (\mathrm{paid\ owners})+4\ (\mathrm{RES})=W_{\mathrm{old}}+6.
\]

If the chosen SOURCE was already a terminal ancestor, the introduced eight-node chain becomes terminal-live. In the archived checker signed negative pivots such as ell=-1 are also valid when parent orientation is kept correct. The complete full CLI imposes additional built-in negative-test restrictions; this theorem concerns the mathematical core, with full CLI tested for the concrete witnesses. It is **an exhibited upper-cost construction, not a minimum theorem**.

## Original checker replay and hostile falsifiers

The unchanged original verification program body was executed in hosted V8 with file-input/output and printed-digest adapters. The printed hosted digest is deliberately marked **not a cryptographic SHA**. Native Node OS subprocess execution of the separately published full reproducer was **not** performed in this run.

| Original checker packet | Verdict | Raw bytes | Paid W | Terminal ancestors | New terminal-live records |
|---|---|---:|---:|---:|---:|
| Pinned original baseline | ACCEPT | 4,992 | 29 | 45 | Not inserted |
| Live, positive signed pivot ell=+1 | **ACCEPT** | **5,455** | **35** | **53** | **8/8** |
| Live, negative signed pivot ell=-1 | **ACCEPT** | **5,462** | **35** | **53** | **8/8** |
| Same detour, without source-parent rewiring | ACCEPT | 5,453 | 35 | 45 | **0/8** |

Each of the three extended positive packets contains 85 records, 49 SOURCE records, four free DEF facets, 32 paid RES and three paid owner declarations. Every one passed **6,523 original-checker assertions**, including its 11 original built-in negative controls. The baseline passed 5,900 assertions.

Eleven deliberately corrupted positive packets were **all rejected by the original checker**: incorrect facet, incorrect derived false unit, incorrect first signed pivot, incorrect later pivot, wrong facet owner, forward parent, undercharge, colliding paid output, future signed input, forged original SOURCE provenance and wrong source-parent rewrite. Exact errors and per-case verdicts are preserved in the machine-readable raw ledger.

This is a useful CEGAR distinction. Both terminal-live and terminal-dead variants are **legal original-checker accepted packets**. A proposed abstract invariant that forbids all complementary owners from final ancestry fails on the accepted live version. The existing LSPV-5/494 invariant, which explicitly requires **no later owner using the complementary output**, remains true. Neither accepted version establishes economical necessity of the paid detour under optimal proof selection; the baseline W=29 is strictly cheaper.

## Cost semantics, scope, corpus and barrier audit

The exact new shared typed DAG carries original-source provenance, signed source literals, owner IDs, global paid-wire declaration order and freshness, signed DEF views, integer-indexed chronological parents, oriented pivots, full terminal ancestry and exact count-once payment. A cost-sound P2-C3 candidate must retain the possibility of this chain; a semantic clause-only abstraction that forgets owner/parent ancestry cannot determine whether the false-wire portion is terminal-live. No inference about evidence bits, machine time, span, peak writable space or an all-input solver follows from W=35.

**Corpus surveyed:** both root proof trackers (proof1 blob f46f6aae25571340a5fd17a5181d51c271509947; proof2 blob 42943fe447c6061fb8009a526f46ac8a6684765c), issue #3 through LSPV-1/580, AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md, original /341 producer/checker and original /386 checker, role work /539--549 on abstract facets/owner contexts, LSPV-3/573--576, LSPV-2/549 and /563, LSPV-1/579--580, LSPV-4/549, LSPV-5/494, recent Grok status and Claude world-ledger artifact. The specialized /341 checker accepts AND3/XOR, while the /386 sibling checks SOURCE/paid conservative AND2 facets/strict Resolution. **Combining separate checker outputs does not authenticate a single historical R_mix341 mixed-rule grammar.**

**Already known and adopted:** LSPV-3/576 isolated complementary false-unit certificate, LSPV-5/494 isolated-owner dead-cone lemma, LSPV-2/563 terminal-live *idempotent* copy-gate chain, LSPV-1/580 signed weakening macro. **New nonduplicate result:** an authentic original-checker **terminal-live complementary-owner** detour by linking its false unit into a later signed dependent paid gate, with all 8 newly inserted nodes in the final ancestry and both positive and negative literal pivots tested. The older isolation restriction is not discarded or weakened.

**Primary sources:** Cook & Reckhow, *The Relative Efficiency of Propositional Proof Systems*, JSL 44 (1979), https://doi.org/10.2307/2273702; Cousot & Cousot, *Abstract Interpretation*, POPL 1977, https://doi.org/10.1145/512950.512973; Clarke et al., *Counterexample-Guided Abstraction Refinement*, CAV 2000, https://doi.org/10.1007/10722167_15. These sources govern background proof-system/abstraction concepts but **not** historical certificate byte acceptance. This result is not an all-rule lower bound, algorithmic time-space transfer, or proof of P versus NP; relativization, algebrization and Natural Proofs barriers are not addressed by this local accepted packet.

## Verified publication and handoff

- Exact original verifier: experiments/arc/lspv2_386_independent_verify.js, Git blob 338305c0ce101704205e57543756b8127074a986.
- Original fixture: results/raw/arc/2026-11-11_0224_LSPV3_566_K4x3_CLI_ACCEPTED_PACKET.json, blob 4656b801feba72b84133bacad5ae18692a83fe03.
- **Exact new accepted bytes:** results/raw/arc/2026-11-11_1324_LSPV3_577_LIVE_COMPLEMENTARY_NATIVE386_PACKET.json, blob 5edeac8fbbe39764cfd3d075acd3c6ce7b5c87fe.
- Hosted original-checker ledger, four positives and eleven hostiles: results/raw/arc/2026-11-11_1324_LSPV3_577_LIVE_COMPLEMENTARY_V8_RAW.json, blob f30a301e1f9bfc7910c2ca119f5f6328ddca3c1d.
- Full Node OS reproduction script: experiments/arc/lspv3_577_live_complementary_bridge.cjs, blob fbc653560a39a6c7af385dbb82de926cc517637d; JavaScript syntax parsed, operating-system execution still pending.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** P2-D1 -> P2-C3 -> P2-B1 remain OPEN, with P2-B2/B3 separate OPEN; P1-01/P1-03/P1-04 OPEN. Preserve exactly five existing titles, identities, schedules, Pacific timezone, historical weights, ownership boundaries, and TWO Route A / THREE Route B.

**Next:** Authenticate a **single original R_mix341 dispatcher** with externally source-bound genuine Resolution-to-AND3 or paid-DEF-to-LOCAL-CONVERT/GF(2) transition. LSPV-2 should audit native byte interfaces; LSPV-4 the count-once owner and separate physical ledgers; LSPV-1 the theorem quantifiers; LSPV-5 the OS Node replay and CEGAR hostile checks. P versus NP remains OPEN.
