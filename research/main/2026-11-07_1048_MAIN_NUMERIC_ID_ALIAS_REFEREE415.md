# LSPV-5 Independent Red Team — Numeric-ID aliasing in the recovered `/341` checker

**Run:** LSPV-5/415  
**Pacific timestamp:** 2026-11-07 10:48 PST  
**Primary route:** Route B  
**Status:** **COMPUTATIONAL/PROVED-RESTRICTED parser counterexample**; `[P2-D1]`, `[P2-D3]`, all-mixed hardness, B3, and P versus NP remain **OPEN**.

## Result first

The recovered historical SOURCE/AND3/XOR checker parses its JSON packet with JavaScript `JSON.parse` and stores node identifiers in `Map` objects without first requiring a canonical identifier type. Distinct raw integer tokens outside JavaScript's safe-integer range can therefore denote the same parsed `Number`.

Two exact accepted examples are:

1. A source clause and its deletion witness use raw ID `9007199254740992`, while a proof parent uses raw ID `9007199254740993`.
2. A derived AND3 node uses raw ID `9007199254740992`, while its children refer to raw parent ID `9007199254740993`.

Both packets are accepted with the same 30,714-check stdout hash as the baseline because

$$
\operatorname{JSON.parse}(9007199254740992)
=
\operatorname{JSON.parse}(9007199254740993)
$$

as JavaScript `Number` values. Thus the accepted byte graph does **not** preserve textual integer equality of node identities. This is a concrete original-source/proof-provenance authentication defect in the recovered sublanguage.

It does **not** produce a satisfiable source accepted as UNSAT, shorten the 15-node logical proof, authenticate RES/LOCAL-CONVERT/DEF, prove an all-rule normalization, prove B3, or establish P versus NP.

## Tracker nodes reviewed

- `[P2-D1]` historical grammar and original-source-authenticated normalization — material evidence added: byte-level node identity is not canonical in the recovered SOURCE/AND3/XOR checker.
- `[P2-D3]` trusted-checker boundary — material evidence added: range projection from `[P2-L5-414]` is insufficient by itself; identifier type and canonical parsing are also required.
- `[P2-L5-415]` — new restricted accepted-byte counterexample and proposed repaired syntax.

`proof1.txt` and `proof2.txt` were both read completely before this experiment. Only the above `proof2.txt` nodes are materially affected.

## IDEA

### Initial hypothesis

Assume the recovered verifier treats parsed JSON values as node identities. Then a byte-distinct identifier alias should be accepted whenever two raw numeric tokens parse to the same JavaScript `Number`. A repair should require a canonical identifier domain before constructing any node map.

### Precise falsifiers stated before search

1. Every byte-distinct numeric alias is rejected by the recovered checker.
2. Every accepted alias normalizes uniquely without changing any source coordinate, parent edge, or paid node identity.
3. Signed or oversized identifiers cannot reach source or derived-parent lookup.
4. An independent raw-token implementation cannot reproduce an accepted collision.

## SEARCH

### Project continuity

Read at current or pinned versions:

- `proof1.txt`, complete blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`.
- `proof2.txt`, complete pre-experiment blob `daf0b1977dbfa833e3dec5bfbb024caa0c6cf308` (refetched again before tracker publication).
- Governing five-role handoff at historical commit `4e29ed7646f484707767acb6e63ec5f38afd98a8`, file blob `033b54…`.
- `AGENTS.md` blob `19656a…`, `CODEX.md` blob `754999…`, and `.codex/skills/pnp-research/SKILL.md` blob `b8df83…`.
- Recovered checker `experiments/arc/lspv2_341_independent_verify.js`, repository blob `fcb7d4ced8f922de14c0bda16263a8cc7853e8e0`; local SHA-256 `0a8167fc65f324860f60abd2a0e0176d0def968cb6ee7055b6aa1bfd43c255ae`.
- Historical packet `experiments/arc/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json`, repository blob `fe27fe…`; local SHA-256 `12d723c92c683ec1a59e17d95d0d47156babe7febe27b7432dc01279abcb8d95`.
- LSPV-1/482 report `research/agents/lspv-1/2026-11-07_1024_LSPV1_STRICT3_B1_B2_SEPARATION482.md`, blob `833923…`.
- LSPV-3/479 report `research/agents/lspv-3/2026-11-07_1024_LSPV3_DEF_OR_RES_CERTIFIED_GATE_PORT479.md`, blob `6b3bed…`.
- LSPV-4/475 report `research/agents/lspv-4/2026-11-07_LSPV4_SOURCE_INDEX_MEMOIZATION_PARETO475.md`, blob `ecfe66…`.
- Grok `GROKPROOF/2026-11-06_2316_PROGRESS.md`, blob `a20fb8…`.
- Claude `research/agents/claude/2026-10-28_0924_CLAUDE_WORLD-LEDGER-0001.tex`, blob `79e4d4…`.

The LSPV-1/482 and LSPV-3/479 advances remain restricted constructions. Neither supplies historical accepted bytes for the missing full grammar, so neither closes `[P2-D1]` or B3.

### External sources and repositories

- RFC 8259 states that integers in the inclusive range $[-(2^{53})+1,(2^{53})-1]$ are interoperable exactly; this is the relevant serialization boundary: <https://www.rfc-editor.org/rfc/rfc8259#section-6>.
- ECMAScript defines `Number.isSafeInteger` by exact integral representation and absence of another integer with the same `Number` value: <https://tc39.es/ecma262/multipage/numbers-and-dates.html#sec-number.issafeinteger>.
- FRAT-XOR uses an explicit positive-integer identifier format, illustrating that identifier syntax is part of a proof format rather than an incidental host-language detail: <https://github.com/meelgroup/frat-xor>.
- Required repository delta checks: `konard/p-vs-np` remained at `ecedd2b45…`; `blkph0x/p-vs-np-proof-research` remained at `7dedc73f…`. No theorem or implementation there supplied the missing historical `R_mix341` productions.
- Rotating corpus checks included `meelgroup/frat-xor`, `tanyongkiam/cake_lpr`, `peitl/short-proof`, `openai/math` at `4eaee875…`, and `anthropics/formal-math` at `16a5ce413…`. Targeted code search found no direct historical-341 parser implementation.

Google's branded interface was unavailable. Public web search and direct primary/official sources were used; no Google execution is claimed.

## ITERATE

### Exact experiment

The Python producer mutates the first fixture of the exact recovered packet, invokes the recovered checker, records packet/output hashes, and applies an independent proposed strict-string validation. The independent Node program reconstructs the colliding integer tokens **as raw JSON bytes** before invoking the checker, avoiding accidental pre-rounding by the producer.

| Case | Raw relationship | Historical checker |
|---|---|---:|
| Baseline | canonical string IDs | ACCEPT |
| Source positive collision | $2^{53}$ versus $2^{53}+1$ | ACCEPT |
| Source negative collision | $-2^{53}$ versus $-(2^{53}+1)$ | ACCEPT |
| Source large collision | $2^{60}$ versus $2^{60}+1$ | ACCEPT |
| Derived-node collision | $2^{53}$ versus $2^{53}+1$ | ACCEPT |
| Safe distinct control | $2^{53}-2$ versus $2^{53}-1$ | REJECT |
| Representable distinct control | $2^{53}$ versus $2^{53}+2$ | REJECT |
| `null` ID control | same `null` token | ACCEPT |
| Boolean ID control | same `true` token | ACCEPT |

All accepted variants produced stdout SHA-256 `af477923155e6e4340a643a4df5b437751b443f03993bbc04dbe73c8587bf7be`, identical to the reserialized baseline. The safe-range controls show that acceptance is caused by host-number aliasing, not by a verifier that ignores parent IDs.

### Restricted lemma

Let $B$ be a JSON byte string accepted by the recovered checker. Suppose a node definition contains an integer token $a$, a parent reference contains a different integer token $b$, and `JSON.parse(a) === JSON.parse(b)`. Because the checker inserts and retrieves identifiers with a JavaScript `Map` keyed by the parsed values, the parent reference resolves the node defined under $a$. Hence raw-token identity is not authenticated.

The witness $a=2^{53}$ and $b=2^{53}+1$ proves the premise.

### Revision and repair

The initial idea is confirmed, but the repaired claim must remain parser-specific. A sufficient repair for the recovered packet language is:

1. require every source ID, inference ID, deletion source ID, and parent reference to be a string;
2. require one canonical grammar, tested here as `^[A-Za-z][A-Za-z0-9_-]{0,63}$`;
3. require global uniqueness of source and inference IDs per fixture before any lookup;
4. reject non-string IDs rather than coercing or rounding them;
5. separately retain `[P2-L5-414]`'s affine-coordinate range projection.

The existing baseline passes this proposed validator; all eight mutated ID cases fail it. This is a **proposed repaired checker language**, not an assertion that the regex was part of historical `R_mix341`.

## Established-family and transfer ledger

| Family | Exact encoding / size | Established theorem and model | Known legal shortcut/control | Remaining Route-B transfer |
|---|---|---|---|---|
| Random strict 3-CNF (`[P2-F8]`) | Published fixed-density random 3-CNF; size linear in variable count | Exponential lower bound for ordinary Resolution under the paper's density/model assumptions | Branching, clause learning, ER, algebraic rules must be considered separately | No theorem over all historical mixed rules; exact family parameters/source remain ledger-controlled |
| Characteristic-3 strict 3-CNF (`[P2-F9]`, LSPV-1/482) | Peer report's published-family instantiation | Restricted B1/B2 separation in its stated construction/model | Identity/other proof systems and mixed rules remain controls | Does not imply same-calculus B3 or all-mixed hardness |
| Odd-charge cubic Tseitin strict 3-CNF | Four forbidden-pattern clauses per cubic vertex; $4h$ clauses and $3h/2$ edge variables | Ordinary Resolution lower bounds on appropriate expanders | Linear GF(2) elimination; `[P2-L5-410]` mixed semantic shortcut | Any mixed lower bound must survive affine, DEF/ER, Resolution, sharing, and exact parser/provenance rules |
| Pigeonhole principle | Standard PHP CNF, with an established ordinary Resolution lower bound | Haken-style Resolution hardness | Cook Extended Resolution is the mandatory upper-bound control | An equisatisfiable 3-CNF conversion alone does not preserve the needed lower bound |

Certified UNSAT, restricted proof-size hardness, and empirical solver difficulty remain distinct throughout.

## Resource and trust ledger

- **Logical distinct-node work:** unchanged at 15 inference nodes for the recovered fixture. No lower minimum was found.
- **Explicit packet evidence:** historical packet 197,514 bytes; compact reserialization 77,714 bytes baseline; source collision 77,750 bytes; derived collision 77,738 bytes.
- **Construction/search:** nine Python cases; nine independent Node assertions. Python checker invocations totaled approximately 1.7 seconds in the captured run, excluding report/publication.
- **Parsing/checking:** every accepted packet reran the recovered checker; no output was accepted on producer authority alone.
- **Storage/retrieval:** current GitHub blobs and full tracker contents were fetched; publication and final tracker readback are recorded separately.
- **Peak space:** not instrumented; no asymptotic same-machine claim is made.
- **Trust boundary:** this is the recovered SOURCE/AND3/XOR checker only. It remains unknown whether another historical parser imposed an external schema.

## Reproduction

```bash
python experiments/review/lspv5_415_numeric_id_alias_audit.py \
  --checker replay/413/lspv2_341_independent_verify.js \
  --packet replay/413/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json \
  --out results/raw/review/2026-11-07_1048_LSPV5_NUMERIC_ID_ALIAS415.json

node experiments/review/verify_lspv5_415_numeric_id_alias.mjs \
  replay/413/lspv2_341_independent_verify.js \
  replay/413/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json
```

Observed:

- Python: 9 cases, 7 accepted as predicted; PASS.
- Independent Node: 9 assertions; PASS.
- Producer SHA-256: `9b838576bbe4cd6d2747d7bd11d8b5ef2ac63eb34da4eef59eb41f968c314662`.
- Independent verifier SHA-256: `cefba0e3d605686e16f7af10ab4d88652cd6f121e9ef835f35ed194b3a645ef0`.
- Raw results SHA-256: `73756d52b018f50e775981f241aad44e072a92fdf3a85c18585246f2c9e6ccca`.

## Publication safeguard and precise remaining gap

Root `main.tex` was fetched but exposed an empty payload (current blob `68188a24badda635a5983fda1c381cdb694fd497`), so it was not edited: full outside-marker byte preservation could not be verified.

The precise remaining gap is still a complete historically authorized parser and native simulation for Resolution, `RES → AND3`, LOCAL-CONVERT, DEF/extension, branching, scope discharge, and all exact weights, now additionally requiring canonical node identity and affine-coordinate domains. After that, Route B still needs a superpolynomial lower bound surviving **every** legal mixed shortcut and a noncircular same-calculus B3 bridge. P versus NP remains **OPEN**.
