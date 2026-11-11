# LSPV-5/482: Prototype-sensitive accepted identifiers falsify ordinary-object namespace transport

**2026-11-10 22:48 PST | PNP Independent Proof Red Team | historical Route B | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

## Result first

The unchanged pinned recovered `/341` SOURCE/AND3/XOR checker accepts one odd-K4 certificate after seven live SOURCE/paid identifiers and every corresponding reference are renamed to:

`__proto__`, `constructor`, `toString`, `hasOwnProperty`, `valueOf`, `isPrototypeOf`, and `__defineGetter__`.

The accepted UTF-8 JSON packet is 3,665 bytes, has SHA-256 `cd7606fd35ef7c9402a5feb45831889a529e95add015e88d94fec8c6289470f3`, completes 1,401 checker assertion groups, and retains 15 paid nodes. Independent exhaustive evaluation finds zero satisfying assignments among all $2^6=64$ assignments to the 16-clause source.

The original checker is **not** unsound on this test: it correctly implements its identifier namespace with ECMAScript `Map`. The counterexample instead falsifies a plausible P2-C3 transformer or independent checker reimplementation that replaces `Map` with an ordinary `{}` property dictionary. With the common duplicate test `dict[id] !== undefined`, the ordinary object rejects the accepted certificate at the first `__proto__` SOURCE record because the inherited accessor is already visible. With unchecked `dict[id]=value`, assigning an object-valued `__proto__` changes the dictionary prototype and creates no own `__proto__` entry.

A repair control using `Object.create(null)` plus `Object.prototype.hasOwnProperty.call` accepts the hostile identifier sequence, as does `Map`. This proves a namespace-level repair lemma, not complete historical-calculus closure.

## IDEA -> SEARCH -> ITERATE

### Initial idea and precise falsifiers

**Target claim:** once raw-byte decoding is fixed, the recovered checker's parsed identifier namespace can be transported to any ordinary string-key dictionary without changing accepted completed refutations or count-once cost.

Exact falsifiers stated before searching:

1. a checker-accepted live identifier equal to an inherited `Object.prototype` property;
2. a concrete accepted packet rejected by the proposed dictionary duplicate/parent tests;
3. unchecked `__proto__` assignment changing the namespace prototype rather than creating an own proof-node entry;
4. a repair control showing that the failure is representation-specific rather than a semantic property of the certificate.

All four tests resolved against the initial transport claim.

### Search and evidence that changed the claim

ECMAScript specifies `Map` as a keyed collection whose keys are distinguished by SameValueZero. The `Object.prototype.__proto__` name is instead an inherited accessor with a setter that can change an object's prototype. OWASP's prototype-pollution guidance independently recommends `Map`/`Set`, or `Object.create(null)` when an object dictionary is required. These are exact JavaScript namespace facts; they are not proof-complexity lower bounds.

Primary/authoritative starting points:

- ECMAScript 2026, Map objects and SameValueZero: <https://tc39.es/ecma262/2026/multipage/keyed-collections.html> and <https://tc39.es/ecma262/2026/multipage/abstract-operations.html>.
- ECMAScript `Object.prototype.__proto__`: <https://tc39.es/ecma262/2026/multipage/fundamental-objects.html>.
- OWASP Prototype Pollution Prevention: <https://cheatsheetseries.owasp.org/cheatsheets/Prototype_Pollution_Prevention_Cheat_Sheet.html>.
- Cousot and Cousot, *Abstract Interpretation* (POPL 1977): <https://www.di.ens.fr/~cousot/COUSOTpapers/POPL77.shtml>.
- D'Silva, Haller and Kroening, *Abstract Conflict Driven Learning* and *Abstract Satisfaction*: <https://www.kroening.com/publications/view-publications-dhk2013-popl.html> and <https://www.kroening.com/publications/view-publications-dhk2014-popl.html>.

Required-repository change-aware review:

- `konard/p-vs-np/README.md`, blob `0e0ec77f83ad6eec1719a96066108b96ac1c2a95`: explicitly limits its checked inclusion result to its finite-machine model and leaves NP subset P open.
- `blkph0x/p-vs-np-proof-research/README.md`, blob `f397a7747eaca82df3d754d0a4b4bab1fe10f814`: explicitly describes bounded/promised algorithms and scoped obstructions, not a P-versus-NP solution.
- `meelgroup/frat-xor/README.md`, blob `38a137bca4d4ab6443703d4c31fba5783021c581`: identifies a separate FRAT-XOR to XLRUP elaboration/checking pipeline, not the historical `/341` language.
- `tanyongkiam/cake_lpr/README.md`, blob `e94f45e9aa000cd9ada12f4c771ac9daf28fe53c`: announces a final 1 November 2026 release and a coming successor; its checker contract is separate from `/341`.

The repository-wide exact search for `__proto__ constructor SOURCE identifier Map` found no prior project result. Google Drive searches for `R_mix341`, `P2-D1 native calculus`, and `LSPV-5 prototype checker` returned zero files. No Drive evidence was silently substituted.

### Revised claim

**PROVED/RESTRICTED namespace theorem:** for the pinned recovered `/341` K4 SOURCE/AND3/XOR fixture, the original `Map` namespace accepts the prototype-sensitive packet. The ordinary-object transformer defined below is not language preserving. A null-prototype own-property dictionary simulates this finite namespace trace exactly, but no claim is made yet about the complete parser, all accepted packets, raw token identity, external source authentication, or all historical rules.

## Exact concrete and abstract configurations

For the restricted checker, take a concrete configuration

$$
C=(b,J,i,M,S,P,W,q),
$$

where $b$ is the complete raw packet byte string; $J$ is the decoded and parsed JSON object; $i$ is the current record index/phase; $M$ is the ECMAScript `Map` from parsed identifiers to live SOURCE or paid records; $S$ is the authenticated-in-this-packet source-record sequence; $P$ is the processed paid proof prefix; $W$ is the count of distinct paid proof records; and $q$ is the current checker control state. Terminal acceptance additionally requires all original `/341` fixture checks and the contradiction row.

The relevant concrete transitions are:

- `SOURCE(k,r)`: require `!M.has(k)`, then `M.set(k,r)`;
- paid `AND3/XOR(k,p_1,p_2,r)`: require `!M.has(k)` and `M.has(p_1),M.has(p_2)`, check the rule semantics, then `M.set(k,r)` and increment $W$ once;
- deletion/witness lookup: retrieve the same parsed identifier class from $M$ and check the witness;
- terminal: check the final affine contradiction and summary.

The rejected candidate abstraction/transport uses an ordinary object $O=\{\}$ and

$$
\alpha_{\rm obj}(M)[k]=M(k),\qquad
\mathsf{present}_{\rm obj}(k)\equiv O[k]\ne\texttt{undefined}.
$$

No sound concretization $\gamma_{\rm obj}$ makes this a step simulation over all accepted string identifiers: for $k=\texttt{"__proto__"}$, `present` is true before insertion because the accessor is inherited. Thus the concrete SOURCE step is admissible while its purported abstract successor is absent. Completed-refutation preservation fails immediately. If insertion is attempted without an own-key test, assigning an object value to `__proto__` changes the prototype and does not create the intended own entry.

The repaired namespace candidate is a null-prototype dictionary $O_0=\texttt{Object.create(null)}$ with

$$
\mathsf{present}_0(k)\equiv
\texttt{Object.prototype.hasOwnProperty.call}(O_0,k).
$$

For a finite sequence of pairwise-distinct JavaScript string keys, $\alpha_0$ copies every `Map` entry to an own property of $O_0$, and $\gamma_0$ reconstructs the `Map` from those own entries. Induction on insertions/lookups proves namespace-trace equivalence for that sequence. The executed hostile trace is an independent control of this lemma.

This is not yet a complete abstract interpretation of $R_{\mathrm{mix341}}$: it omits decoder states, numeric and `undefined` keys, raw lexical aliases, external source hashes, RES, DEF/facets, LOCAL-CONVERT, branch contexts/discharge/joins, weakening, deletion policy, and any cross-rule ownership semantics.

## Sound resource polarity and CEGAR consequence

For a lower-bound-safe MAY abstraction, every legal concrete completed refutation $P$ must map to an admissible abstract completed refutation $P^\#$ with

$$
\operatorname{cost}^{\#}(P^{\#})\le \operatorname{cost}_{R}(P).
$$

The ordinary-object transformer fails before cost comparison because it omits a legal concrete accepted path. It is therefore an underapproximation at this point and cannot support a P2-C3 minimum lower bound. Abstract satisfaction must interpret `present(k)` as membership/own-entry existence, not arbitrary prototype-chain property lookup.

CEGAR cannot call the hostile path spurious: it was replayed in the authoritative recovered checker. The valid refinement is to repair the abstract domain/transformer so it includes the path. Deleting the path would reverse the required coverage polarity.

The repaired null-prototype trace preserves the same 15 paid logical nodes in this finite case, so its abstract logical cost is equal here. This does **not** prove a real-time or live-peak-space bound. Dictionary allocation, UTF-8 decoding, JSON parsing, hashing/comparison, proof-record storage, retrieval/recomputation, subprocess buffers, raw output, and publication all remain separate physical costs. Configuration cardinality is not memory, and proof-DAG work is not memory.

## Executed certificate and controls

Pinned Git blobs:

- producer: `4081022e8a3841d79f751a3d3a7a10decbb026da`;
- checker: `fcb7d4ced8f922de14c0bda16263a8cc7853e8e0`.

Node v24.22.1 OS-subprocess results:

| Case | Bytes | SHA-256 | Native checker | Namespace control |
|---|---:|---|---|---|
| Baseline K4 | 3,518 | `fd6c0b89...09a19` | accept, 1,401 | Map/object accept |
| Prototype-sensitive IDs | 3,665 | `cd7606fd...470f3` | accept, 1,401 | Map accepts; `{}` rejects |
| Dangling original-name parent | 3,658 | `6c885ef8...dc951` | reject: missing antecedent | expected |
| Duplicate `__proto__` SOURCE ID | 3,663 | `46ee637a...45a27c` | reject: unique source ID | expected |
| Null-prototype repair | same parsed hostile trace | n/a | n/a | accepts |
| Unchecked `__proto__` assignment | local object | n/a | n/a | prototype changes; no own key |

The accepted hostile packet is embedded losslessly as base64 in the raw JSON. The K4 source is a finite Tseitin/affine control, not an asymptotic hard-family result. Exhaustive source evaluation is independent of checker acceptance and gives 0/64 models.

## Independent peer review performed this run

- **LSPV-1/563:** the published original-checker reproducer reran successfully: 14 differential tests, seven accepts/seven rejects, 39,120 original assertion groups, and 6,149 codec checks. This confirms its restricted lone-surrogate counterexample, not all-rule closure.
- **LSPV-2/549:** after fetching the pinned `/386` checker and exact packets, the native OS Node runner passed. One 7,533-byte polyglot is independently accepted by `/341` at 15 paid nodes/1,401 checks and by `/386` at 50 paid units/4,492 checks; one-sided mutations show noncomposition. This is not one mixed proof.
- **LSPV-3/560:** the typed restricted-sub-language runner passed 16 tests and the seven-fixture 30,714-check baseline. It remains a strict sound subset, not a MAY abstraction of every accepted byte string.
- **LSPV-4/535 predecessor:** the native runner passed 12 padded positive cases, its negative controls, and the 47-core/47-CLI/48-CLI differential. This verifies the predecessor write's executable scope. It does not authenticate a joint historical dispatcher.

The first attempted reruns of /549 and /535 failed only because this scratch mirror lacked `lspv2_386_independent_verify.js` and exact packet files. After fetching their pinned blobs into the expected paths, both native runners passed. This was an environment-completeness failure, not a scientific counterexample.

## Corpus reconciliation

**CORPUS REVIEWED.** Root `proof1.txt` blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`; root `proof2.txt` blob `6f67f45292072d832143b187b433c0dbd64be47f`; `AGENTS.md` blob `4ae902888754d0b06ba4ce1aaeca0657a92b46a9`; `CODEX.md` blob `754999f50de93cdb693ed37bc8110d31e9e698ef`; repository skill blob `b8df83a7b0b1428f349b0e02ce1387d979e8db7f`; issue #3 metadata/body (1,616 comments, updated 2026-11-11T06:51:22Z); root `main.tex` blob `bd4895c53e7f787eefb633bf1c6d9903ec52c1a5`; LSPV-5/481 handoff blob `16f3297517af2c20b623a91f83e4c4b775681cd3`; current LSPV-1/563, LSPV-2/549, LSPV-3/560 and LSPV-4/535 reports/code; GROKPROOF `2026-11-06_2316_PROGRESS.md` blob `a20fb8b3640d7574faf238a4a83a021bb0984808`; Claude world-ledger report blob `79e4d4e7e0e3edff3aba8610852c45534bdde128`; required external repositories listed above. The issue-comments bulk connector returned `Transport closed`; current issue metadata/body was read, and the exact new issue comment will be read back directly after publication.

The local preflight script correctly reported that the scratch mirror lacks root `main.tex`, `AGENTS.md`, `CODEX.md`, and the complete skill file. Those authoritative files were instead read from current GitHub blobs; this limitation is disclosed rather than treated as a complete checkout.

**DUPLICATION / CONTRADICTION AUDIT.** Prior /477, /479, /481, /540, /541, /545, /546 and /563 concern numeric, signed-zero, UTF-8, BOM, undefined-terminal or surrogate equivalence. None found by exact project search addresses inherited JavaScript object names. /560 is intentionally a strict canonical-string subset and therefore excludes this packet; it is not contradicted. /562's whole-packet UTF-8 result is also not contradicted. /549 and /535 concern independent `/341` and `/386` checker composition/cost, not namespace transport.

**WHAT CHANGED RELATIVE TO ROOT MAIN.** A new restricted P2-C3 transport failure is added: parsed string identity alone is insufficient unless the implementation preserves `Map`/own-key membership semantics. No original checker soundness theorem, proof-weight lower bound, or B1/B2/B3 implication changed.

**ADOPTED / REJECTED / RETIRED PRIOR COMPONENTS.** Adopt the exact pinned `/341` `Map` semantics, /481's requirement to preserve complete accepted paths, and /560's distinction between a strict sound subset and an all-accepted MAY abstraction. Reject ordinary inherited object dictionaries as exact namespace implementations. Retain null-prototype own-key dictionaries as a candidate namespace repair only. No historical component is retired.

**STALE OR OVERSTATED CLAIMS FOUND.** Any current or future claim that arbitrary JavaScript string dictionaries are interchangeable for proof identifiers is overstated. No such exact claim was located in the current tracker, so this is a preventive counterexample rather than a correction to a named theorem.

## All-phase resource ledger

- logical work: 15 distinct paid nodes, unchanged by renaming;
- explicit accepted evidence: 3,665 UTF-8 JSON bytes; 4,888 base64 characters embedded in raw output;
- construction: one producer run plus deterministic seven-ID rewrite;
- parsing/checking: four OS Node checker subprocesses; accepted cases each completed 1,401 assertion groups;
- independent semantic check: all 64 source assignments;
- negative controls: one dangling parent, one duplicate source, ordinary-object rejection, unchecked-prototype mutation;
- repair control: null-prototype dictionary with own-property membership;
- peer execution: /563, /549, /560 and /535 runners as recorded above;
- source/head/index reads: GitHub blobs, issue metadata, required repository README blobs, primary-web sources, and empty Drive searches;
- output/publication: report, executable, raw JSON, handoff, tracker delta, LSPV-5 `main.tex` region, issue comment, and exact readbacks;
- caches/retrieval/recomputation: Node buffers and temporary packet files were used and removed; no physical peak-RAM measurement was made;
- runtime: the published /482 runner completed in under one second in this environment, but this finite wall time is not an asymptotic theorem;
- failed policy: ordinary `{}` membership; failed initial peer reruns due to absent pinned `/386` files in the scratch mirror.

No inference from packet count, configuration count, logical DAG work, or serialized bytes to RAM space is made.

## Tracker/status impact

This is a material new P2-C3 transformer counterexample and warrants `[P2-L5-482]` in `proof2.txt`. It does not change `proof1.txt`.

- **Family failure:** none; the finite K4 source remains UNSAT.
- **P2-D1:** still OPEN; only the recovered `/341` fragment is exercised.
- **P2-C3:** still OPEN; ordinary-object namespace transport is falsified, and the null-prototype repair is namespace-only.
- **P2-B1:** still OPEN; no all-input normalization/transfer theorem follows.
- **P2-B2/B3:** separate and OPEN.
- **P versus NP:** OPEN.

## Artifacts and next target

- executable: `experiments/review/lspv5_482_prototype_key_namespace_audit.js`;
- raw evidence: `results/raw/arc/2026-11-10_2248_LSPV5_482_PROTOTYPE_KEY_NAMESPACE_RAW.json`;
- five-role handoff: `research/coordination/2026-11-10_2248_LSPV5_PROTOTYPE_KEY_NAMESPACE482_FIVE_ROLE_HANDOFF.md`.

**Next decisive target:** run the same prototype-sensitive identifier matrix against an authoritative source-bound `/386` DEF-owner/facet-to-RES certificate, then determine whether its identifier namespace and CLI/core wrapper use `Map`, an own-key dictionary, or property-chain lookup. A separate common JSON envelope is not cross-rule authentication.

Exactly five role identities/titles/schedules/timezone, two Route A/three Route B labels, enabled states, historical rules/weights, and ownership boundaries are unchanged. No agents or automations were created, renamed, rescheduled, duplicated, enabled, or disabled.

**LSPV-5/482 VERIFIED REPORT; P versus NP OPEN.**
