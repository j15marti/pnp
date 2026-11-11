# LSPV-5/485: exact noninteger Resolution parents accepted throughout a binary64 rounding cell

**2026-11-11 04:21 PST | Independent Proof Red Team | historical Route B | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN.**

## IDEA: target and falsifiers

**Target claim.** The archived `/386` Resolution-parent check `Number.isInteger(p)` authenticates exact mathematical integer tokens. The attempted falsification replaces the first parent of record 22, whose canonical token is `16`, while holding the complete packet fixed.

Precommitted falsifiers were: (F1) exact decimal `16.000000000000001` rounds to parent 16 and is accepted; (F2) an infinite/parameterized neighborhood of exact nonintegers around 16 is accepted; (F3) decimals just outside the binary64 rounding cell reject; (F4) the lower and upper exact midpoint ties behave differently. F1 and F2 are confirmed. F3 is confirmed as a boundary control. F4 is refuted: both exact midpoint ties round to 16 and accept, as round-to-nearest-ties-to-even predicts.

## SEARCH and authentication

Read current `proof1.txt` (blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`), `proof2.txt` (pre-run blob `e7cb9e738ea31173766c553b2a5541e71df0c503`), issue #3, `AGENTS.md` (`4ae902888754d0b06ba4ce1aaeca0657a92b46a9`), `CODEX.md` (`754999f50de93cdb693ed37bc8110d31e9e698ef`) and `.codex/skills/pnp-research/SKILL.md` (`b8df83a7b0b1428f349b0e02ce1387d979e8db7f`). Re-read the current LSPV-5/484 handoff and actual LSPV-1/569, LSPV-2/554, LSPV-3/567, LSPV-4/540 and Claude world-ledger artifacts. Google Drive searches for `R_mix341 exact decimal Resolution parent` and `P2-D1 P2-C3 native calculus 485` returned no files. Current Grok/Claude material supplies no authenticated unified historical checker.

Primary sources: ECMAScript defines Number using IEEE 754 binary64 and chooses the closest representable value, with the tie behavior corresponding to roundTiesToEven: https://tc39.es/ecma262/2026/ . RFC 8259 permits JSON numbers with fractions and exponents but warns that implementation precision limits affect interoperability: https://datatracker.ietf.org/doc/rfc8259/ . These standards explain parsing; they do not prove anything about the lost historical calculus.

Change-aware required-repository review retained the pinned heads from the immediately preceding run: `konard/p-vs-np` `ecedd2b45f1c524d85c00b2da27a9c140025550c`, `blkph0x/p-vs-np-proof-research` `7dedc73f758dfbdc072e7aa29dfc08505761ebd5`, and `meelgroup/frat-xor` `18cd6bc17af10a9891c10a846ce966166f9fe0dc`. None supplies the `/386` JSON-decimal identity theorem or the complete R_mix341 dispatcher.

## ITERATE: exact rounding-cell lemma

At the exactly representable integer 16, the next binary64 number above is at distance $2^{-48}$, while the next number below is at distance $2^{-49}$. Therefore the round-to-nearest cell of 16 is

$$
\left[16-2^{-50},\;16+2^{-49}\right].
$$

The two exact decimal endpoints are

$$
15.99999999999999911182158029987476766109466552734375
$$

and

$$
16.0000000000000017763568394002504646778106689453125.
$$

The significand of 16 is even while each adjacent significand is odd, so both midpoint ties round to 16. Every exact decimal strictly inside this interval also rounds to 16. Consequently, the verifier first loses exact-decimal identity during JSON-to-Number conversion and then observes an integral Number.

## Unchanged-checker replay

Pinned verifier: `experiments/arc/lspv2_386_independent_verify.js`, Git blob `338305c0ce101704205e57543756b8127074a986`. Seed packet: `results/raw/arc/2026-11-10_2212_LSPV2_549_DUAL_NATIVE_POLYGLOT_PACKET.json`, Git blob `b9c1d306c300a3f1917ee01ecab16358ac77d4de`, SHA-256 `6272ffa2223cc426c2401d16d48919dcb5421a7e15490d97cc5cbc5f653b1527`.

Six exact noninteger spellings, including both exact midpoint ties, were parsed as Number 16 and accepted by an actual OS Node subprocess. Each retained the exact baseline summary: 50 paid nodes, one DEF owner, 49 RES nodes, 69 records, 17 SOURCE records, 4,492 assertion groups and all eleven bundled negative controls.

| Exact raw parent token | Parsed Number | Checker |
|---|---:|---:|
| `16.000000000000001` | 16 | ACCEPT |
| `16.0000000000000001` | 16 | ACCEPT |
| `1.6000000000000001e1` | 16 | ACCEPT |
| `15.9999999999999999` | 16 | ACCEPT |
| lower exact midpoint | 16 | ACCEPT |
| upper exact midpoint | 16 | ACCEPT |

Four outside-cell controls rejected. In particular, `16.000000000000004` parsed as the nonintegral next binary64 value, and the upper midpoint with its final digit increased by one did likewise. Symmetric lower controls rejected.

## Concrete/abstract consequence and scope

Let concrete parent identity retain `(raw UTF-8 span, exact JSON rational, parsed Number, resolved record)`. Any abstraction that keeps only `(parsed Number, resolved record)` merges all exact rationals in the cell above. That projection can describe operational checker behavior, but it cannot authenticate exact mathematical integrality or raw-byte identity. Because all six paths replay in the unchanged checker, CEGAR must retain them; they are genuine accepted paths, not abstraction artifacts.

A conservative repair lexes the JSON number, decides exact mathematical integrality and range before binary64 conversion, admits only canonical unsigned decimal integer syntax, and only then resolves the parent. This is a proposed repair, not historical authority.

This result is a **P2-D1 accepted-byte counterexample** and a **P2-C3 transformer obligation**. It does not change ancestry or logical cost and is not semantic unsoundness, a family lower bound, P2-B1, or a B2/B3 bridge. The archived `/386` checker still does not authenticate AND3, GF(2), LOCAL-CONVERT, branching, weakening, contexts, discharge, joins or the complete historical R_mix341 parser.

## Peer reconciliation and resource ledger

LSPV-1/569's finite bounded normal form is restricted to parsed `/386` mathematical configurations; raw decimal spellings remain infinite unless quotienting is explicitly proved. LSPV-2/554's gate-owner topological transport and LSPV-4/540's owner-incidence accounting are unaffected. LSPV-3/567 independently shows duplicate-member last-value shadowing; together, 567 and 485 require a raw-token layer before ordinary object/Number construction. The peer hosted-V8 claims were read at their stated scope but were not re-executed in this run; this run's 485 evidence used actual OS Node.

All-phase costs for 485: 11 checker subprocesses (one baseline, six acceptances and four controls), 7,549–7,584 input bytes for positive mutations, JSON parsing and the verifier's bundled hostile replays. Logical cost remains 50. Search, serialization, subprocess memory, evidence bytes and checker runtime are not logical work. No peak physical memory, span or machine-model conversion is inferred.

## Disposition

Material tracker delta: add `[P2-L5-485]` to `proof2.txt`. P2-D1, P2-C3 and P2-B1 remain OPEN. P2-B2/B3 remain separate and OPEN. P versus NP remains OPEN.

