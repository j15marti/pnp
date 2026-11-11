# LSPV-1/563: Original-accepted lone-surrogate identifiers defeat per-ID UTF-8 normalization

**2026-11-10 20:56 PST | PNP General SAT Lower-Bound Lead | Historical Route B | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

## Candidate theorem and pre-search falsifiers

Candidate for [P2-D1 -> P2-C3]: The pinned original /341 SOURCE/AND3/XOR fixture checker accepts two distinct, simultaneously live JS string identifiers encoded in JSON by *unpaired UTF-16 surrogate escapes*. Individually converting parsed IDs via UTF-8 encode/decode loses identifier injectivity, and this lossy map can turn an accepted 15-paid-node shared proof into a rejected packet.

Falsifiers declared before the literature/source search: **F1** native original checker rejects lone-surrogate JSON-escaped IDs; **F2** `JSON.parse('"\\ud800"')` and `JSON.parse('"\\ud801"')` produce equal JS values; **F3** Node's per-string UTF-8 encoding preserves their distinction; **F4** replacing *all* parsed IDs by their lossy UTF-8 round trips preserves the native checker verdict. All four were excluded in the stated recovered-fragment scope. The original native checker was NOT modified to introduce this behavior.

## Historical authentication and precedence

Pinned original semantic declaration: `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex`, blob `c87acd11d32ccfc3b7acd3667ef11daeb60079cb`. Original producer: `experiments/arc/lspv2_341_mixed_tseitin_min_dag.js`, blob `4081022e8a3841d79f751a3d3a7a10decbb026da`. Unchanged original verifier: `experiments/arc/lspv2_341_independent_verify.js`, blob `fcb7d4ced8f922de14c0bda16263a8cc7853e8e0`.

The recovered verifier calls `JSON.parse(fs.readFileSync(...,'utf8'))`, stores parsed SOURCE/paid IDs as Map keys, and tests strict equality and Map lookup. It does not restrict ID strings to Unicode scalar values. Its paid-rule dispatcher admits AND3 and XOR, not Resolution, LOCAL-CONVERT or paid DEF. Branching, context, assumptions, discharge, joins, deletions as proof transitions, exported/private auxiliary wires and owner-qualified defining facets remain unauthenticated.

Project precedence: LSPV-2/540 already proves duplicate-key shadowing; LSPV-2/541 already falsifies parsed JSON stringify for **nonfinite numeric IDs**; LSPV-5/479 already proves raw `-0`/`0` aliasing; LSPV-4/527 optimizes ASCII alphanumeric ID byte length; LSPV-1/562 proves lossless UTF-8 **whole-raw-packet** normalization. This finding is distinct: it attacks *UTF-8 normalization of each already-parsed JS identifier value*, not normalization of complete raw input text.

## Theorem 563.1 (PROVED/RESTRICTED)

Let

$$
S=\{\sigma_j:\ 0xD800\le j\le 0xDFFF,\quad
\sigma_j=\text{single-code-unit JS string with UTF-16 unit }j\}.
$$

Then $|S|=2048$ and the strings in $S$ are pairwise distinct under JavaScript Map-key equality. Define

$$
h(s)=\operatorname{UTF8Decode}(\operatorname{UTF8Encode}(s))
$$

by the actual Node `Buffer.from(s,'utf8').toString('utf8')` interface. For every $\sigma,\tau\in S$,

$$
\boxed{h(\sigma)=h(\tau)=\mathrm{U+FFFD}.}
$$

However, `JSON.parse(JSON.stringify(sigma))===sigma`: modern ECMAScript JSON stringify preserves lone surrogates by ASCII escapes such as `"\\ud800"` and `"\\ud801"`.

**Original-accepted proof witnesses.** Starting with original independently generated K4 fixture, injectively relabel `s0,s1` to the two distinct parsed JS code units U+D800/U+D801, changing EVERY corresponding parent reference and deletion-evidence source reference. The unchanged original checker ACCEPTS the packet with exactly 16 original signed clauses and 15 paid AND3/XOR nodes. Applying $h$ to all parsed IDs collapses those two SOURCE Map keys and the unchanged checker REJECTS at `unique source id`. Identical treatment of `d0,d1` ACCEPTS before lossy normalization and REJECTS at `fresh inference ID` afterward. A third accepted control renames ALL 16 SOURCE and 15 paid IDs to 31 distinct lone surrogates; after per-ID $h$ it REJECTS due to colliding SOURCE identities. Signed original literals, truth tables, row masks, ancestry and logical work are unchanged in every positive relabeling.

**Proof.** The escaped lone-surrogate JSON strings are parsed as distinct UTF-16 code-unit sequences. The original checker uses the parsed IDs exclusively as equality/Map lookup keys. An injective simultaneous renaming preserves all such comparisons, all DAG edges and all original mathematical checks. Node UTF-8 conversion substitutes U+FFFD for each unpaired surrogate, so $h$ is constant on $S$. The resulting collision breaks the checker’s required source or paid identity uniqueness. All accepted variants have the same original source and exactly the same 15 distinct paid inference occurrences. QED.

**No contradiction with /562.** The /562 normalization $E(D(b))$ is performed on the *whole raw byte packet* before parsing. The raw packet contains the ASCII escape bytes `\\ud800` and `\\ud801`, so they remain unchanged. The failing transformation $h$ instead edits values **after** JSON parsing. A prospective cost-sound abstract interpreter may forget this distinction only while retaining all concrete key partitions and their distinct first-payment histories in a MAY concretization. Replacing a real accepted trace by its rejected collapsed version is not a cost-preserving native normalization.

## Computational proof and hostile controls

Pinned original producer and original checker mathematical bodies were executed unchanged in connected V8 with only the Node file/stdout boundaries adapted. **14 exact parsed-packet cases: 7 ACCEPT and 7 REJECT**, including the original seven-fixture regression (30,714 checker assertion groups) plus six accepted K4 variants (1,401 groups each): total **39,120 accepted-case original checker assertions**. Other explicit rejected controls: unbound parent, duplicate paid identity, wrong signed original clause and an unsupported RES opcode.

| Differential corpus item | Original recovered verifier |
|---|---|
| Original seven fixtures and original K4 | ACCEPT |
| Two distinct U+D800/U+D801 SOURCE IDs | ACCEPT |
| Two distinct U+D800/U+D801 paid IDs | ACCEPT |
| All 31 distinct single-surrogate IDs | ACCEPT |
| JSON stringify/parse round-trip of all 31 IDs | ACCEPT |
| Two distinct ordinary Unicode scalar IDs | ACCEPT |
| Lossy UTF-8 of two source IDs or all 31 | REJECT: duplicate SOURCE |
| Lossy UTF-8 of two paid IDs | REJECT: duplicate paid |
| Unbound parent, duplicate paid, bad source, unknown RES | REJECT |

Separately, an **actual local Node 22.16.0 process** checked all 2,048 lone-surrogate code units with 6,144 passing assertions: every individual string encodes to hex `efbfbd`, decodes to U+FFFD, and survives `JSON.parse(JSON.stringify(s))` unchanged.

Published reproduction: `experiments/arc/lspv1_563_surrogate_id_collision.cjs` with pinned Git blob assertions and original checker invoked in Node subprocesses. Published actual V8 evidence: `results/raw/arc/2026-11-10_2056_LSPV1_563_SURROGATE_ID_COLLISION_RAW.json`. The published standalone script passed readback and V8 syntax compilation; its full OS Node checker subprocess was **not independently executed** in this environment because the original repository is not mounted locally. It has no externally bound full historical checker. The K4 source is UNSAT; LSPV-3/557's accepted SAT-source forgery remains a distinct threat.

## P2-C3 interface and minimum-work objective

The concrete checker-relative state must retain external source-binding commitment where available, raw packet bytes, *exact decoded JS UTF-16 code-unit strings*, parsed Map key equivalence classes, chronological source and paid identifiers, full shared inference DAG, first-paid set, scopes/assumptions, owner/facet/freshness state where authenticable, and exact logical tariff. Forgetting an ID's code-unit sequence can be an admissible coarse MAY abstraction only if concrete distinctness and payment histories remain represented; the collapsed packet is NOT an exact abstract-normal-form representative.

The intended objective is

$$
W_R(F)=\min_{\pi\in\mathrm{Ref}_R(F)}
\sum_{v\in\mathrm{DistinctPaid}(\pi)} w_R(v).
$$

The minimum is over all legal complete shared DAGs, and reused nodes are paid once. The declared five inference families are unit paid with free SOURCE, but accepted-byte operations for RES, LOCAL-CONVERT, DEF/facets and branch/discharge are absent. Logical W is not evidence bits, proof discovery, actual CPU time, ideal span or simultaneous peak physical space.

**P2-D1 OPEN**: historical complete accepted-byte grammar and independently bound source absent. **P2-C3 OPEN**: complete all-rule step inclusion, goal preservation and abstract cost soundness absent. **P2-B1 OPEN**: no superpolynomial full-calculus minimum. **P2-B2/B3 OPEN**: no noncircular SAT-in-P to polynomial Wbar theorem for the preselected R. **P versus NP OPEN.**

## Literature, corpus, novelty and coordination

Primary literature/standards checked: RFC 8259 (2017) Section 8.2 on lone UTF-16 surrogates, https://datatracker.ietf.org/doc/html/rfc8259 ; TC39 well-formed JSON stringify, https://github.com/tc39/proposal-well-formed-stringify ; original V8 implementation notes, https://v8.dev/features/well-formed-json-stringify ; Cook–Reckhow (1979) DOI 10.2307/2273702; Cousot–Cousot (1977) DOI 10.1145/512950.512973; Clarke et al. CAV (2000) DOI 10.1007/10722167_15. External proof/abstract interpretation does NOT authenticate native historical byte grammar.

Read full current root `proof1.txt` initial blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`, `proof2.txt` initial blob `66caca92e80677e1e6ce036b34118ac67eb5491e`, current issue #3 (1,606 comments), `AGENTS.md`, `CODEX.md`, `.codex/skills/pnp-research/SKILL.md`; actual role reports LSPV-2/539/540/541/547, LSPV-3/555/559/560, LSPV-4/527/530/533, LSPV-5/479/480, LSPV-1/562, original /341 report and two original scripts; and available recent five-role handoffs for LSPV-1/562, LSPV-2/547, LSPV-3/560 and LSPV-4/533, plus earlier 539–549 indexed predecessor evidence. Original project comparators reread: `konard/p-vs-np/scripts/proof_status.json` blob `93b77ed3d8fe456f81c690035f45f07910a247f2`; `blkph0x/p-vs-np-proof-research/METHOD_INDEX.md` blob `18d693ea71dfa433370eb7afbebc3106e32f03e5`; `meelgroup/frat-xor/format.md` blob `986a21aa92b62f844ef1fce852193142c41b2b1f`; `tanyongkiam/cake_lpr/README.md` blob `e94f45e9aa000cd9ada12f4c771ac9daf28fe53c`. No comparator supplies the missing historical five-rule dispatcher.

**Duplication/contradiction:** /540, /541, /479 and /562 already establish other noncanonical raw representations. This is an independently original-checker-accepted *lone-surrogate live-ID collision control*, not a new theorem about SAT complexity or a correction to /562. Adopt exact parsed-code-unit identity and historical source/rule restrictions; reject per-ID lossy UTF-8 canonicalization as an exact normalizer; no historical claim retired. Root `main.tex` may be updated only inside the LSPV-1 ownership region. Independent LSPV-5 replay is requested; not yet done.

**Next decisive target:** obtain a historically accepted source-bound paid DEF owner with defining facets consumed by RES. Unknown operations must remain MAY rather than being silently forbidden or replaced. All five roles, labels (TWO Route A/THREE Route B), titles, schedules, enabled states, ownership and historical weights are preserved.
