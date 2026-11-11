# LSPV-5/483 independent red team: Resolution-parent negative-zero accepted-byte alias

**Pacific timestamp:** 2026-11-11 01:52 PST  
**Role:** LSPV-5 Independent Proof Red Team (historical Route B label preserved)  
**Status:** **COMPUTATIONAL accepted-byte counterexample** plus a **PROVED-RESTRICTED local repair lemma**. P versus NP remains **OPEN**.

## Outcome first

The unchanged archived `/386` verifier at Git blob `338305c0ce101704205e57543756b8127074a986` accepts two different raw JSON byte strings as the same Resolution parent reference: the baseline token `0` and the hostile token `-0`. The hostile packet is 7,534 bytes with SHA-256 `b7240d9b4be51a194d39f71696e12cca08664d339a58cbc44bd64bbddeb9d037`; the baseline is 7,533 bytes with SHA-256 `6272ffa2223cc426c2401d16d48919dcb5421a7e15490d97cc5cbc5f653b1527`. Both runs report exactly 50 paid nodes, 49 Resolution nodes, one DEF owner, 69 records, and 4,492 assertions.

This falsifies raw-token injectivity for an actual accepted Resolution-parent field and therefore blocks any P2-D1/P2-C3 argument that silently identifies accepted bytes after JSON parsing. It is **not** a semantic soundness failure, a cheap proof of a new formula, a proof-size lower bound, a B1 bridge, or a P-versus-NP result.

## IDEA: target and falsifiers stated before search

**Target claim.** In the archived `/386` accepted-byte language, the raw spelling of each Resolution parent denotes a unique prior record, so a source-authenticated abstraction may erase the spelling after parsing without a separate normalization theorem.

Precise falsifiers:

1. raw `-0` is accepted as parent `0`;
2. quoted `"0"` bypasses integer parent typing;
3. `-1` bypasses the prior-record bound;
4. an alias changes ancestry, sink reachability, or paid cost.

Falsifier 1 succeeded. Controls 2 and 3 were rejected. Falsifier 4 did not occur: ancestry, sink and cost were identical after the alias.

## SEARCH: authenticated inputs and external controls

I read the current `proof1.txt` (`96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`) and `proof2.txt` (pre-publication blob `8927e4ba0c54ba701ceac55e918203fcdf675e1a`), issue #3, `AGENTS.md` (`4ae902888754d0b06ba4ce1aaeca0657a92b46a9`), `CODEX.md` (`754999f50de93cdb693ed37bc8110d31e9e698ef`), the complete project research skill (`b8df83a7b0b1428f349b0e02ce1387d979e8db7f`), the current handoffs, and relevant LSPV/Grok/Claude artifacts including [P2-L2-549], [P2-L4-535], [P2-L4-536], [P2-L1-565] and [P2-L5-482].

The pinned packet is `results/raw/arc/2026-11-10_2212_LSPV2_549_DUAL_NATIVE_POLYGLOT_PACKET.json`, Git blob `b9c1d306c300a3f1917ee01ecab16358ac77d4de`, SHA-256 `6272ffa2223cc426c2401d16d48919dcb5421a7e15490d97cc5cbc5f653b1527`. The experiment invokes the original checker as an OS Node subprocess; it is not a reimplementation.

External controls:

- RFC 8259 permits an optional minus before the integer component of a JSON number; it does not assign application-level identity rules to numeric spellings: <https://www.rfc-editor.org/rfc/rfc8259>.
- ECMAScript `Number.isInteger` accepts integral Number values, while Number string conversion maps both positive and negative zero to `"0"`: <https://tc39.es/ecma262/multipage/numbers-and-dates.html#sec-number.isinteger> and <https://tc39.es/ecma262/multipage/abstract-operations.html#sec-tostring-applied-to-the-number-type>.
- RFC 8785 canonical JSON serialization emits negative zero as `0`, giving a relevant normalization control but not retroactively changing the accepted language: <https://www.rfc-editor.org/rfc/rfc8785>.
- FRAT-XOR instead specifies line IDs as distinct positive integers, illustrating that a proof format can choose a stricter identifier grammar: <https://github.com/meelgroup/frat-xor/blob/master/format.md>.
- Cook--Reckhow concerns relative proof-system efficiency and does not authenticate this parser or transfer a restricted verifier result to arbitrary computation: <https://www.cs.toronto.edu/~sacook/homepage/cook_reckhow.pdf>.
- Abstract Interpretation and Abstract Satisfaction supply approximation frameworks, not permission to quotient concrete accepted bytes without a soundness proof: <https://doi.org/10.1145/512950.512973> and <https://www.kroening.com/papers/popl2014.pdf>.

Targeted searches of `konard/p-vs-np` (observed head `ecedd2...`) and `blkph0x/p-vs-np-proof-research` (observed head `7dedc73...`) found proof-attempt/status material but no authenticated R_mix341 parser or theorem covering this alias. Google Drive searches for `R_mix341 native calculus accepted byte` and `P2-D1 P2-C3 proof2` returned no files. These negative searches are not mathematical evidence.

## ITERATE: authoritative replay

The mutation is confined to record 22, parent position 1:

```json
{"parents":[16,0]}
```

becomes

```json
{"parents":[16,-0]}
```

The replay matrix is:

| Packet | Raw parent | Accepted | Paid | RES | Assertions |
|---|---:|---:|---:|---:|---:|
| baseline | `0` | yes | 50 | 49 | 4,492 |
| hostile | `-0` | yes | 50 | 49 | 4,492 |
| type control | `"0"` | no | -- | -- | -- |
| bound control | `-1` | no | -- | -- | -- |
| canonicalized hostile | `0` | yes | 50 | 49 | 4,492 |

The experiment independently checks `Object.is(parsedParent, -0)`, then checks that JavaScript array lookup at that value returns exactly the record at index zero. The baseline and hostile verifier summaries agree on every recorded semantic and cost field: `paid`, `def`, `res`, `records`, `sources`, `sourceBits`, `oddModels`, `evenModels`, and `guardFalseModels`.

## Concrete/abstract semantics and polarity

For this fragment, a complete concrete checker state is

$$
c=(B,P,i,K,G,C,Q),
$$

where $B$ is the exact input byte string, $P$ is the parsed JSON value (including the negative-zero Number value), $i$ is the record cursor, $K$ is the indexed prior-record array, $G$ is the gate/source/provenance environment, $C$ is the paid cost ledger, and $Q$ contains the CLI summary and sink obligations. A concrete Resolution transition consumes the raw parent substrings in $B$, their parsed Numbers in $P$, and the referenced records in $K$.

The hostile run proves that the abstraction

$$
\alpha_{\rm parse}(B,P,i,K,G,C,Q)=(P,i,K,G,C,Q)
$$

is not injective on accepted concrete byte states. Its concretization contains at least both the baseline and hostile byte strings. This is harmless for a semantic theorem that explicitly quotients such spellings, but unsound for a theorem claiming exact source-byte authentication or unique raw ancestry unless the quotient and source-hash policy are separately proved.

A cost-sound negative-proof abstraction still needs all three obligations:

1. **step inclusion:** every accepted concrete step maps to an admissible abstract step;
2. **completion preservation:** every accepted concrete sink maps to an abstract completed refutation;
3. **resource polarity:** for every concrete refutation $P$, its image satisfies $\operatorname{cost}(P^\#)\leq\operatorname{cost}_R(P)$.

This counterexample attacks item 1 for any abstraction that authenticates raw bytes but omits the alias. It does not falsify item 3, because cost is unchanged.

## CEGAR verdict and restricted repair lemma

The hostile abstract path cannot be classified as spurious: the authoritative `/386` checker accepts its exact bytes. Refinement may distinguish `0` from `-0`, or a proved quotient may identify them; it may not delete the path merely because the intended grammar preferred `0`.

**PROVED-RESTRICTED local repair lemma.** For the finite positional-parent fragment checked here, define normalization only after parsing and validating that a parent is an integer in $[0,i)$. Serialize that integer in unique unsigned decimal notation. Then each validated positional parent has one normalized spelling, and both accepted spellings `0` and `-0` normalize to `0`. If raw-byte provenance is part of the theorem, reject any input whose parent token differs from its normalization. The experiment reserialized the hostile packet to 7,532 bytes, removed `-0`, and the original checker accepted it.

This lemma does not authenticate object keys, source hashes, other numeric fields, gate identifiers, lexical Unicode aliases, branching/context operations, or any unimplemented historical R_mix341 operation.

## Independent peer controls

I reran the available LSPV-1/2/3/4 artifacts:

- LSPV-1/563: 14 tests, 6,149 codec checks and 39,120 original assertions;
- LSPV-2/549: the dual packet remained accepted by both pinned native checkers, with non-composability controls still separating their rule languages;
- LSPV-3/560: 16 tests and 30,714 baseline checks; it remains a separate affine sublanguage, not full R_mix341;
- LSPV-4/535: all core/CLI, free-facet, paid-owner and negative firewall controls passed.

None of these controls rejects the new `/386` negative-zero parent alias, and none authenticates the complete historical calculus.

## Resource ledger

The hostile replay reads a 7,533-byte baseline packet and a 6,345-byte checker, materializes four packet variants one at a time in temporary directories, and executes five OS Node checker subprocesses (baseline, hostile, quoted-string, negative-one and canonicalized). Accepted baseline and hostile runs each execute 4,492 checker assertions. The hostile materialization is 7,534 bytes; its canonicalized serialization is 7,532 bytes. The audit code and raw-result files have SHA-256 values `673fb00f97f1fbbeb5ea38c80981a638135907650e52b9190be4c88a7c31ce84` and `cb1435e7869e9ea9b9a688955d1df947d5bb8f0d1d242784c9aa8ef70e7dc65f`.

Logical node cost, evidence bytes, parsing, construction, subprocess execution, temporary storage, report output, repository reads, tracker update and publication are kept separate. No logical proof-node count is converted into machine space. Peak live work space was not instrumented at the allocator level; the experiment therefore makes no numerical peak-space claim.

## Tracker status, publication scope and remaining gap

This run materially changes [P2-D1]: an additional accepted raw spelling exists in the actual `/386` Resolution parent field. [P2-C3], [P2-B1] and [P2-B2/B3] remain **OPEN**. The tracker delta is restricted to the new node [P2-L5-483].

The exact remaining gap is a complete, source-authenticated accepted-byte semantics for every historical R_mix341 transition, followed by a cost-sound abstraction covering every such concrete step and completed shared-DAG refutation. This local alias and repair do not supply that closure. P versus NP remains **OPEN**.

