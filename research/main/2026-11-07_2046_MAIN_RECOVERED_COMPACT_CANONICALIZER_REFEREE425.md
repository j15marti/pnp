# LSPV-5/425 independent referee: compact canonical representatives for the recovered SOURCE/AND3/XOR checker

**Pacific timestamp:** 2026-11-07 20:46 PST  
**Role:** LSPV-5 independent red team, Route B primary  
**Tracker nodes:** `[P2-B2]`, `[P2-D1]`, `[P2-L1-466]`, `[P2-L5-409]`, `[P2-L5-414]`, `[P2-L5-415]`, `[P2-L5-416]`, `[P2-L5-417]`, `[P2-L5-419]`, `[P2-L5-420]`, new `[P2-L5-425]`  
**Status:** **PROVED-RESTRICTED** canonical compression theorem for one recovered parsed-object SOURCE/AND3/XOR checker; **COMPUTATIONAL** two-language replay; full historical $R_{\mathrm{mix341}}$ grammar, compact-witness premise, B2, B3 and P versus NP remain **OPEN**.

## IDEA: hypothesis and falsifiers stated before search

Initial hypothesis: a noncircular B3 bridge must supply an $R_{\mathrm{mix341}}$-native simulation of the canonical reject-trace proof system, and the current project had not isolated that factorization. Assumptions were the fixed historical calculus, a total polynomial SAT decider, original-source authentication and fully explicit proof bytes. The falsifiable prediction was that a same-$R$ polynomial generator or size simulation would be the missing premise.

Precise falsifiers:

1. a current tracker node already states the exact identity-system/same-$R$ factorization;
2. Cook--Reckhow yields polynomial bounds in every preselected fixed proof system, rather than in some polynomially bounded system;
3. an accepted recovered packet cannot be normalized to a compact representative without changing checker semantics; or
4. the recovered checker includes all historical RES, LOCAL-CONVERT, DEF, branch/discharge and provenance rules, making its canonicalization a full-calculus theorem.

Search immediately triggered falsifier 1: `[P2-L5-409]` already records that under SAT=P, B3 is equivalent to existential $W$-size simulation of the identity system by the same fixed $R$, while a uniform compiler is a stronger sufficient condition. Repeating that factorization would not be an advance. I therefore revised the target to the unresolved compact-witness sub-obligation in `[P2-L1-466]`: determine whether all accepted packets of the preserved recovered SOURCE/AND3/XOR checker have polynomial-size canonical representatives despite the accepted metadata, affine-mask and identifier aliases found in `[P2-L5-414/415/416/417/419]`.

## SEARCH: continuity, primary sources and repository deltas

The following current complete sources were read before iteration:

- `proof1.txt`, blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b` (18,553 bytes), and `proof2.txt`, search-time blob `70acb43e2f3fc4b5b7bfceae588a04e81a3e4c5a` (317,971 bytes). Exact prewrite/postwrite blobs are recorded in the publication receipt.
- Governing historical handoff `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md` at commit `4e29ed7646f484707767acb6e63ec5f38afd98a8`, blob `033b54b87b7cbe94912af5cf67daa52859143a07`.
- Current issue #3 through page 13, including LSPV-1/494, LSPV-2/483, LSPV-3/489 and LSPV-4/485; `AGENTS.md` blob `19656af1...`, `CODEX.md` blob `754999f5...`, and `.codex/skills/pnp-research/SKILL.md` blob `b8df83a7...`.
- Actual peer files: LSPV-1/494 blob `406e9748...`, LSPV-3/489 blob `a5b7461a...`, Grok `GROKPROOF/2026-11-08_0320_PROGRESS.md` blob `72edb314...`, and Claude `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex` blob `9a5b05d6...`.
- Exact prior bridges: LSPV-1/466 blob `f4a12eae...` and LSPV-5/409 blob `0b2e41a...`. `[P2-L1-466]` makes compact witness length an explicit premise; `[P2-L5-409]` already gives the identity-system factorization.

Primary-source scope checks:

- Cook and Reckhow, *The Relative Efficiency of Propositional Proof Systems* (JSL 1979): existence of **some** polynomially bounded propositional proof system is equivalent to NP=coNP; a p-simulation transfers bounds in its stated direction. It does not make every fixed system polynomially bounded.
- Shuo Pang, *A Degree--Size Relation for Resolution over Polynomials*, arXiv:2610.00837: exponential DAG size for fixed restricted $\operatorname{Res}(\operatorname{PC}_r/\mathbb F_p)$ parameters on constant-width CNFs under the stated degree hypothesis. It does not cover the recovered checker or the full mixed calculus.
- Urquhart's expander/Tseitin resolution lower bound was retained as a mandatory ordinary-Resolution control. Algebraic parity reasoning remains a legal shortcut control in a stronger mixed system.

Required repository review and exact versions:

- `konard/p-vs-np` stayed at `ecedd2b45...`; `scripts/proof_status.json`, blob `93b77ed...`, inventories formal claims/assumptions but contains no historical-$R_{\mathrm{mix341}}$ compiler.
- `blkph0x/p-vs-np-proof-research` stayed at `7dedc73...`; `METHOD_INDEX.md`, blob `18d693...`, marks finite/certificate results at their scoped status and supplies no arbitrary-CNF compactness theorem.
- `meelgroup/frat-xor` stayed at `18cd6bc...`; `format.md`, blob `986a21...`, provides an XOR-aware certificate format/checker target, not a same-$R$ B3 theorem.
- `tanyongkiam/cake_lpr` stayed at `033aad53...`; `README.md`, blob `e94f45...`, documents a verified LPR checker and its trust boundary, not this historical grammar.
- `cslib-community/complexitylib` was at `bbfd3506...`; the initially guessed path was unavailable, then the actual `Complexity/Computability/Complexity/CookLevin/Completeness.lean`, blob `ffe13da6...`, was read. It proves SAT NP-hard/complete and UNSAT coNP-complete in its formal setting; it does not produce same-$R$ proofs.
- `openai/math` was at `4eaee875...`; `Final.lean`, blob `a69635a...`, exposes its axioms and an external subexponential theorem, with no applicable compact canonicalizer.
- `uds-psl/cook-levin` main-branch fetch failed and is recorded as unavailable, not silently counted as reviewed.

Actual targeted queries included `Cook Reckhow polynomially bounded proof system NP coNP original paper`, `Urquhart Tseitin exponential resolution lower bound`, `Res(PC) degree size Pang`, `compact proof witness fixed checker`, and repository/path searches for proof-status, checker formats, Cook--Levin completeness and same-system simulations. A separate Google-branded interface was unavailable; indexed research search plus direct primary files and GitHub repositories were used. No repository title, build badge or formalization was treated as proof.

## Established-family ledger

| Field | Exact record |
|---|---|
| Family | Pang $F(n,3,8n)$ duplicate-free hard subsequence, retained from `[P2-L5-423/424]`; Tseitin contradictions on bounded-degree expanders are the ordinary-Resolution parity control. |
| Exact 3-CNF | Pang: a set of $8n$ strict clauses, each using three distinct variables with one of eight polarity patterns. The recovered finite packet instead encodes graph/Tseitin controls through SOURCE/AND3/XOR data; it is not asserted to be Pang's family or a hardness encoding. |
| Size parameter | Pang uses $n$ variables and $8n$ clauses, with the inspected explicit binary bound $L\le192n^2+129n+2$. The recovered fixtures use graph vertices $V$, edges $E$, and record count $W=4V-1$. |
| Theorem/source | Pang Theorem 7.2(a), arXiv:2610.00837, gives a.a.s. $\exp(\Omega_{p,r}(n))$ size in fixed restricted $\operatorname{Res}(\operatorname{PC}_r/\mathbb F_p)$. Urquhart gives exponential ordinary-Resolution lower bounds for suitable Tseitin formulas. |
| Model/rules | Syntactic shared proof DAG in the named restricted system; neither theorem is all-algorithm hardness or automatically a lower bound for historical $R_{\mathrm{mix341}}$. |
| Known methods | Shared DAGs, branching, learned clauses, extension variables and GF(2) parity reasoning must remain legal controls when native or simulated. The present canonicalizer preserves the recovered checker's actual SOURCE/AND3/XOR dependency graph and does not exclude shortcuts. |
| Remaining transfer | Prove an all-native-rule lower bound or source-authenticated polynomial retraction for the fixed historical mixed calculus. Equisatisfiability and a compact representative in a strict sublanguage are insufficient. |

Certified UNSAT, certified proof-size hardness and empirical solver difficulty remain distinct. This run proves no new family lower bound.

## ITERATE: recovered-sublanguage canonical compression

### Recovered checker scope

The executable target is the preserved independent checker
`replay/413/lspv2_341_independent_verify.js`, SHA-256
`0a8167fc65f324860f60abd2a0e0176d0def968cb6ee7055b6aa1bfd43c255ae`,
on packet `replay/413/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json`, SHA-256
`12d723c92c683ec1a59e17d95d0d47156babe7febe27b7432dc01279abcb8d95`.
This is an independent recovered semantic checker, not the authoritative historical raw-byte parser.

### Theorem 425.1 (canonical representative, restricted)

For every parsed packet accepted by this fixed recovered SOURCE/AND3/XOR checker, there exists an accepted canonical packet with:

1. dense string source IDs `s0,s1,...` and derived IDs `d0,d1,...`, preserving source order and derived topological order;
2. every parent and deletion reference rewritten to those IDs;
3. every affine integer mask $m$ replaced by $P_E(m)=m\mathbin{\&}(2^E-1)$;
4. only checker-read fields retained; and
5. bit length $O\!\left(\sum V(E+W+1)\right)$ over fixtures/claims, where accepted recovered records assert $W=4V-1$, hence a polynomial $O(\sum V^2)$ bound.

This proves existence and an effective canonicalizer for the parsed-object sublanguage. It does not assert that every historical proof, every CNF, or every $R_{\mathrm{mix341}}$ rule has such a packet.

### Proof

**IDs.** The checker creates JavaScript `Map` entries from the parsed ID values and looks up parents/deletion witnesses by the same parsed values. Traverse accepted sources and derived records in their already verified order, assign dense string IDs, and consistently rewrite every checked reference. Equality and lookup outcomes are unchanged; strings avoid the numeric and lexical alias surfaces audited in `[P2-L5-415/416]`.

**Affine rows.** The checker observes only the low $E$ coordinates. Projection satisfies

$$P_E(a\oplus b)=P_E(a)\oplus P_E(b).$$

For SOURCE and AND3 rows, every tested coordinate and truth-table condition is preserved. For XOR records, projected parent XOR equals the projected child. The sink equation is likewise preserved. Thus high ghost bits from `[P2-L5-414]` can be removed without changing acceptance.

**Fields and order.** Remove metadata never read by the checker, retain all required graph, clause, support/table, charge, sink and deletion-witness data, and preserve checked array order. This removes the unbounded ignored-metadata channel from `[P2-L5-419]`. It does not authenticate raw source bytes or repair duplicate-member ambiguity before `JSON.parse`; duplicate members already have last-wins parsed semantics.

**Size.** Dense IDs need $O(\log V)$ bits each. The graph/source portion is polynomial. There are $W$ records whose retained affine rows have $E$ bits, plus retained tables/supports and references polynomial in $V,E,W$. The recovered deletion list has $4V$ witnesses, each with an $E$-bit row. A conservative aggregate is $O(V(E+W+1))$ bits per fixture/claim, and the accepted invariant $W=4V-1$ makes it $O(V^2+VE)$.

### Executed adversarial replay

The Node producer made 31 checks. Six accepted encodings all normalized to exactly 71,853 bytes with SHA-256 `1637821fc706fd80abcaf70cbd458d1ad648bcf1576e1eed564b519bb62aba25` and remained accepted:

| Variant | Input bytes | Canonical bytes |
|---|---:|---:|
| baseline | 197,514 | 71,853 |
| ignored metadata | 3,251,118 | 71,853 |
| paired affine ghost bit 8192 | 81,808 | 71,853 |
| unsafe numeric ID alias | 77,749 | 71,853 |
| safe lexical ID alias | 77,708 | 71,853 |
| duplicate JSON member, last wins | 77,734 | 71,853 |

Four corruptions (`sink_rhs`, `bad_literal`, `bad_table`, `missing_parent`) were rejected both before and after/during normalization. Seven finite fixtures from $V=4$ through $V=32$ satisfied explicit conservative size bounds. An independent Python reconstruction made 14 additional checks and reproduced the exact canonical byte count and SHA-256.

### Independent challenge and scope firewall

This result partially discharges only the compact-bit objection for packets already accepted by this recovered sublanguage. It does **not** discharge `[P2-L1-466]`'s full compact-witness premise because:

- the checker is not complete for arbitrary binary-encoded CNFs;
- RES, LOCAL-CONVERT, DEF, case split, assumption discharge and general branching/reconvergence are absent;
- source identity is checked only according to this recovered packet model, not an authenticated external historical byte stream;
- duplicate raw JSON members remain last-wins at `JSON.parse`, so raw provenance is not canonical before parsing; and
- canonicalizing an existing proof neither constructs a proof nor bounds the minimum for every input.

Accordingly the theorem does not imply B1, B2 or B3. Cook--Reckhow cannot fill the gap for this preselected system. The free optimal-choice minimum, known shortcut proofs, DAG sharing and distinct-node accounting are unchanged.

## Resource ledger

- **Logical nodes/weights:** unchanged. Canonicalization renames nodes and projects checker-unobserved bits; it adds no rule, split, weakening or discharge and does not revise historical weights.
- **Evidence bits:** producer program, independent Python reconstruction and 3,409-byte raw summary. The baseline is 197,514 bytes; the canonical parsed-object serialization is 71,853 bytes; the metadata stress input is 3,251,118 bytes.
- **Construction/search:** canonicalization scans sources, records and checked fields and rewrites retained masks/references. Discovery, failed searches, repository reads, parsing, hashing, output and verification are ordinary host work and are not smuggled into the ideal proof minimum.
- **Parsing/authentication:** theorem begins after JSON parsing. Raw duplicate-member parsing and authoritative historical source authentication remain outside scope.
- **Sharing/retrieval:** topological dependency edges and shared parent IDs are preserved; a shared subproof remains one node. No branch-local conclusion is moved across contexts because this recovered schema has no branch contexts.
- **Work/span/space:** scripts report logical/serialized size only, not a parallel span theorem or realizable historical-machine schedule. Retention versus recomputation was not optimized. No FLMV same-machine, exponent or peak-space claim is made.

## Tracker decision, advance and remaining gap

Material evidence affects `[P2-D1]` and `[P2-B2]` through the compact-witness premise in `[P2-L1-466]`; add `[P2-L5-425]`. The node must explicitly preserve the recovered-sublanguage restriction and reference the alias/metadata audits. `[P2-B1]`, `[P2-B2]`, `[P2-D1]`, `[P2-C3]` and historical-$R_{\mathrm{mix341}}$ B3 remain **OPEN**. `proof1.txt` has no material change.

**Actual advance:** a proof and effective construction showing that every accepted parsed packet of the recovered SOURCE/AND3/XOR checker has a deterministic polynomial-size canonical representative; six alias/metadata encodings collapse to one accepted byte string.  
**Verification:** 31 Node checks plus 14 independent Python checks; exact cross-language 71,853-byte/SHA agreement; four corruptions rejected.  
**Publication status:** report, programs, raw result and handoff prepared for a leased current-head commit; the receipt records final SHAs and full readback.  
**Precise remaining gap:** extend compactness, source authentication and native simulation to the exact full historical grammar for every CNF, or exhibit a legal counterexample; separately prove an all-rule lower bound and a noncircular same-calculus B3.  
**P versus NP remains OPEN.**
