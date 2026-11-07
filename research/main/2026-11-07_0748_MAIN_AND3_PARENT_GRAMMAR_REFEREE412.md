# LSPV-5/412 — `AND3` parent-grammar underdetermination audit

**2026-11-07 07:48 PST | Route B independent red team | PROVED/EXACT for specification nonuniqueness of the surviving `/341` prose and exhibited trace class; COMPUTATIONAL typed-trace controls; historical accepted-byte grammar OPEN. P versus NP OPEN.**

Tracked exact nodes: `[P2-D1]`, `[P2-L5-410]`, `[P2-L5-411]`, new `[P2-L5-412]`, and still-open `[P2-C3]`, `[P2-B1]`, `[P2-B2]`. Complete trackers were read before work: `proof1.txt` blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`; starting `proof2.txt` blob `af757c6238edcc9140eb4c183c5c7964302cdf3b`.

## Claim card and IDEA

- **Claim ID:** `[P2-L5-412]`, evidence for `[P2-D1]`.
- **Status before run:** historical `R_mix341` byte grammar OPEN; run 410's `RES → AND3` trace proved only in `/341` declared semantics.
- **Desired conclusion:** determine whether the surviving historical text and its exhibited original Tseitin proofs uniquely fix the serialized parent views admitted by `AND3`.
- **Quantifiers:** for every byte grammar satisfying a stated set of surviving syntactic/semantic facts, does the same split trace have the same acceptance value?
- **Input family:** established odd-charge cubic Tseitin proper 3-CNF and the exact split encoding from `[P2-L5-410]`; finite executable control is K4.
- **Model/resource:** acyclic source-authenticated typed proof DAG; every derived RES/AND3/GF2 node has unit weight; shared node charged once.
- **SAME_REALIZATION:** exact source clauses, exact node order, exact views, exact parent references and exact terminal affine contradiction.
- **Weakest material theorem:** two sound, complete, unit-weight typed realizations agree on every originally exhibited `/341` Tseitin proof but disagree on the run-410 split trace.

Initial hypothesis: the prose does not define the `condition` nonterminal or state whether a clause view produced by `RES` is a serialized `AND3` parent. Falsifiers registered before search were:

1. an authoritative parser/checker fixes the parent tags;
2. the historical text explicitly permits or excludes derived RES parents;
3. an authenticated historical byte trace contains such an edge;
4. either proposed audit grammar changes a historical weight or is semantically unsound.

None occurred. The run therefore proves only specification nonuniqueness; it does **not** choose a historical grammar.

## SEARCH: exact historical text and executable corpus

The governing source is `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex`, blob `c87acd11d32ccfc3b7acd3667ef11daeb60079cb`. Its complete rule paragraph says:

> **AND3:** from two conditions whose combined support has at most three original variables, derive their exact conjunction as an eight-bit truth-table factor.

It also fixes free original source clauses, unit cost for every derived node, at most two antecedent identifiers, ordinary RES completeness, binary GF(2) addition, and sound local semantic checks. It does **not** give a byte production for `condition`, a tag table, a reference grammar, or a clause-to-condition coercion. Its matching proof uses only source-clause and earlier-AND3 parents: three AND3 nodes combine four source clauses at each vertex. Its “fully labelled” executable and independent checker are described but no repository path, commit or accepted byte packet is cited in that report. Targeted current-tree searches for its reported assertion count, graph table, title and emitted trace text found the report but no authoritative historical parser or byte packet.

Relevant actual project artifacts read:

- LSPV-3/423, blob `49bf06ce...`, explicitly records that CANON2 is a **proposed** completion and its AND3 predicate accepts `clause`/`factor` views;
- proposed CANON2 implementation `experiments/arc/lspv5_361/rmix341_canon2_repair_referee361.py`, blob `7b6e8478...`, whose extensional view typing would accept a clause view produced by RES;
- LSPV-3/434, blob `b8028c05...`, and LSPV-5/373, which test semantic or CANON2R traces but retain the historical-byte caveat;
- current peers LSPV-1/477, blob `a7959a9d...`, and LSPV-3/475, blob `3a8da052...`; neither authenticates native historical bytes;
- actual Grok `GROKPROOF/2026-11-07_1220_PROGRESS.md`, blob `2c450bb3...`, and Claude world-ledger README/blob `de75a371...` plus `2026-10-28_1521_CLAUDE_ONETAPE-0001.tex`, blob `9a5b05d6...`; neither supplies the missing grammar.

Current issue #3 reported 1,209 comments. The governing November 2 handoff, `AGENTS.md`, `CODEX.md`, the complete research instructions, red-team mode and research protocol were read. Root `main.tex` again returned blob `68188a24badda635a5983fda1c381cdb694fd497` with zero readable bytes, so no root edit is safe.

Required change-aware repository review found no blob change from the preceding run:

- `konard/p-vs-np`: `scripts/proof_status.json` `93b77ed3...`, `proofs/complexity/README.md` `7ee9a11e...`;
- `blkph0x/p-vs-np-proof-research`: `METHOD_INDEX.md` `18d693ea...`, `REVIEW_ADDENDUM.md` `6a7cc2f8...`;
- `meelgroup/frat-xor/format.md` `986a21aa...`, `tanyongkiam/cake_lpr/README.md` `e94f45e9...`, `peitl/short-proof/README.md` `93d2090d...`, `marijnheule/drat-trim/README.md` `eb6ffcc4...`, `digama0/frat/README.md` `0864ba03...`;
- `openai/math/README.md` `cc5b0a03...`, `anthropics/formal-math/README.md` `1df53bfc...`.

These formats demonstrate why explicit ID namespaces and step productions matter, but none defines historical `R_mix341`. FRAT-XOR, for example, separately declares clause IDs and XOR IDs and gives explicit conversions. It is a distinct proof system, not historical authority. Primary literature review retained Urquhart/Ben-Sasson–Wigderson ordinary-Resolution hardness for expander Tseitin and Gocht–Nordström's separately typed proof logging for XOR reasoning. No theorem in those sources fills a project-specific byte grammar. A Google-branded interface was unavailable; authenticated GitHub and indexed primary-source searches were used.

## ITERATE: exact specification-nonuniqueness theorem

Let the **exhibited trace class** be the original `/341` odd-Tseitin proofs described in the historical report: every first local AND3 has two original source clauses, the third local AND3 has two earlier AND3 factors, and GF(2) nodes combine exact affine annotations.

Define two distinct audit grammars. They are proposed formalisms, not renamed historical rules.

1. **EXTENSIONAL.** A reference resolves to a semantic `clause`, `factor` or `affine` view. AND3 accepts any earlier `clause` or `factor` view. Therefore a derived RES clause is a condition.
2. **TAGGED.** AND3 accepts a source-clause view or an earlier AND3-factor view, but not a clause whose producer tag is RES. Ordinary RES remains unrestricted and complete, so this is still a complete refutation system; it is simply a narrower typed realization of the undefined `condition` nonterminal.

Both grammars:

- use the identical free source axioms and exact source SHA-256;
- use the identical RES, truth-table conjunction and GF(2) semantics;
- have acyclic earlier-parent references;
- charge every derived node exactly one;
- reject forged truth tables, affine annotations, pivots and terminal rows;
- are sound, and are complete because they retain ordinary Resolution.

### Theorem 412.1 — surviving `/341` prose does not determine the split trace

**PROVED/EXACT.** The surviving `/341` rule paragraph plus its exhibited trace class does not uniquely determine whether an AND3 record may name a RES-produced clause view.

**Proof.** Every exhibited original cubic-Tseitin proof uses only source-clause and AND3-factor parents. Hence EXTENSIONAL and TAGGED accept the same proof, with exactly $3h+(h-1)=4h-1$ paid nodes and the same truth tables and affine rows.

For the exact split formula of `[P2-L5-410]`, each original clause is first reconstructed by one correctly oriented RES. The immediately following local AND3 names those derived clause views. EXTENSIONAL accepts them. TAGGED rejects the first one solely because its producer tag is RES. Both outcomes are compatible with every exhibited original trace and every fixed weight; the difference lies exactly in the missing parent nonterminal. Therefore the prose and exhibited traces do not determine acceptance of the split byte sequence. ∎

The theorem is about a missing specification field. It does not prove that TAGGED is the intended historical semantic scope, that EXTENSIONAL is historically accepted, or that the actual historical parser existed in either form. An authoritative conclusion needs the original parser/format or an explicit historical rule stating the coercion.

## Exact established-family ledger

| Family | Exact encoding and size | Published/model-specific result | Legal shortcut control | Remaining transfer |
|---|---|---|---|---|
| Cubic-expander odd Tseitin $F_h$ | One edge variable; four proper signed ternary clauses per cubic vertex. $3h/2$ variables, $4h$ clauses, indexed length $\Theta(h\log h)$. | Exponential unrestricted ordinary shared-DAG Resolution size on suitable expanders; characteristic-dependent PC lower bounds. These are restricted proof systems. | Exhibited `/341` AND3/GF(2) proof has $4h-1$ declared-semantic nodes. | Historical bytes and full mixed lower bound OPEN. |
| Exact split $S(F_h)$ | Replace $C_i=(\ell_1\lor\ell_2\lor\ell_3)$ by $(\ell_1\lor\ell_2\lor a_i)$ and $(\ell_1\lor\ell_3\lor\neg a_i)$, private fresh $a_i$. $11h/2$ variables, $8h$ proper ternary clauses, same asymptotic indexed length. | `[P2-B17]`/`[P2-L5-411]` transfer ordinary Resolution hardness; `[P2-B18]` transfers ordinary PC degree. | `[P2-L5-410]` gives an $8h-1$ declared-semantic RES/AND3/GF(2) proof. | The `RES → AND3` serialized parent permission is not fixed by surviving prose. |
| K4 odd/even controls | Base: 6 variables, 16 clauses; split odd: 22 variables, 32 clauses. | Enumeration certifies 0 odd models and 8 even models; no finite graph is an asymptotic hardness certificate. | Base proof 15 nodes; split EXTENSIONAL trace 31 nodes. | Computational validation only. |

Certified UNSAT, proof-size hardness and empirical solver difficulty remain distinct. No empirical solver claim is used.

## Independent executable audit and hostile controls

The Python implementation constructs exact source-authenticated K4 packets and both typed grammars. The independently authored Node implementation reconstructs the source and trace without importing Python code or data.

| Check | Python | Independent Node |
|---|---:|---:|
| Odd/even base models | 0 / 8 | 0 / 8 |
| Original base proof | both accept, 15 nodes | both accept, 15 nodes |
| Split proof | EXTENSIONAL accepts, 31; TAGGED rejects | same |
| Exact local truth/affine rows checked | 128 per accepted proof | independently replayed |
| Hostile mutations rejected | 9 | 8 |

Mutations cover source hash, malformed original clause, wrong RES pivot/orientation, forward reference, very large unsafe identifier, false factor row, false affine annotation, false GF(2) sum and an unknown semantic-oracle rule. A repeated-parent AND3 idempotence control passed. No DEF occurs in this fragment, so repeated/tautological DEF facets were not silently inferred or tested as native. The even-charge terminal was rejected because it is not $0=1$.

Artifacts and hashes:

- `experiments/review/lspv5_412_and3_parent_underdetermination.py`, SHA-256 `b072e4b867548b49721969c552c4678fe2050b2939e34a9dc3d14c8ac998d6ac`;
- `experiments/review/verify_lspv5_412_and3_parent_underdetermination.mjs`, SHA-256 `d7abb3e1b8c7f9a0814250d4326c95dbe61bb31827114c8c41ed6d057ee62311`;
- `results/raw/review/2026-11-07_0748_LSPV5_AND3_PARENT_UNDERDETERMINATION412.json`.

The Python canonical base/split packets are 2,971/5,538 bytes with SHA-256 `70021a03...`/`5e513aa2...`. Host wall time was 0.007731 seconds and peak RSS 10,368 KiB. These measurements include source construction, parsing, hashing, truth-table checks, mutation copying, verification and output in that implementation. They are not historical-checker execution, proof-search cost, native TM cost, or an FLMV time/space bound. Ideal logical work remains 15/31 distinct unit-paid nodes; encoded bits and physical validation are separately reported.

## Cross-domain and barrier audit

Typed proof formats are analogous to typed intermediate representations: a semantic object may exist without a legal serialized coercion between producer and consumer tags. This is an **ANALOGY/CANDIDATE** only. The exact theorem comes from the two formal grammars above, not from compiler theory.

Relativization and algebraic-oracle replacement do not repair a missing byte production: even a semantic oracle saying that the RES clause is a valid condition does not show the historical parser accepts its reference. Conversely, this specification result says nothing about arbitrary SAT algorithms or lower bounds. Extensions, Gaussian elimination and every legal mixed shortcut remain admitted in the global minimum.

## Status, tracker effect and next gap

**Actual advance:** `[P2-D1]` is narrowed: the decisive missing object is now an explicit `condition`/parent-view nonterminal or an authenticated record exercising `RES → AND3`. The original `/341` text and its source-only Tseitin traces cannot decide that edge. New node `[P2-L5-412]` records this exact result.

**Not advanced:** `[P2-C3]` full rule-by-rule normalization, `[P2-B1]` all-mixed superpolynomial minimum and `[P2-B2]` noncircular same-calculus B3 remain OPEN. `[P2-L5-410]` remains an EXTENSIONAL declared-semantic upper bound, not a historical byte certificate. The established ordinary-Resolution and ordinary-PC lower bounds remain restricted-system results.

**Next exact target:** locate or reconstruct from an authenticated historical artifact the serialized `condition` production and view coercions; then run one complete source-exact split-Tseitin record whose immediate AND3 parent is a RES node. If no such artifact exists, the fixed calculus must remain underspecified rather than silently choosing CANON2, TAGGED or another completion. P versus NP remains OPEN.

## Primary references

1. Urquhart, A., “Hard Examples for Resolution,” *JACM* 34(1), 1987, DOI `10.1145/7531.8928`.
2. Ben-Sasson, E. and Wigderson, A., “Short Proofs Are Narrow,” *JACM* 48(2), 2001, DOI `10.1145/375827.375835`.
3. Gocht, S. and Nordström, J., “Certifying Parity Reasoning Efficiently Using Pseudo-Boolean Proofs,” AAAI 2021, DOI `10.1609/aaai.v35i5.16494`.
4. `meelgroup/frat-xor/format.md`, blob `986a21aa...`, distinct explicit XLRUP/FRAT-XOR syntax.
