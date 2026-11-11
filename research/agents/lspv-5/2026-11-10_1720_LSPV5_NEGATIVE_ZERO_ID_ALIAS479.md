# LSPV-5/479 — negative-zero paid-ID alias defeats raw-byte identity and strict-fragment coverage

**2026-11-10 17:20 PST | Independent Proof Red Team | historical Route B | COMPUTATIONAL accepted-byte counterexample + PROVED/RESTRICTED ECMAScript semantic fact. P versus NP remains OPEN.**

## Target, exact claim, and falsifiers

Target claim tested: **the LSPV-2/542 source-occurrence transporter, together with the strict LSPV-2/539 typed reference, is sufficient to preserve authenticated source multiplicity and paid-node identity for every byte packet accepted by the recovered /341 checker.**

Quantified falsification result:

$$
\exists P\;\bigl(\mathrm{Accept}_{341}(P)\land
\neg\mathrm{Accept}_{539}(P)\land
\mathrm{rawId}(P)=-0\land\mathrm{rawRef}(P)=0\bigr).
$$

The four pre-search falsifiers were:

1. duplicate source occurrences collapse under the transport map;
2. raw numeric aliases such as \`-0\`/\`0\` merge distinct paid nodes;
3. a source/proof identifier crosses the reference checker's type boundary;
4. canonicalization changes accepted-byte cost or verdict.

Falsifier 2 succeeds. Falsifier 3 explains why the strict repair rejects it. The occurrence-bucket construction survived direct canonical/permuted K4 replay; no duplicate-collapse counterexample was found.

## IDEA -> SEARCH -> ITERATE

### IDEA

Replay the exact 542 transporter and then attack the remaining paid-identity layer, without changing the independently supplied source or any logical rule.

### SEARCH and authentication

Current repository head inspected: commit \`1a6015e518e849eef53b8b55b94cf11fe64cd052\`. Both root trackers were read in full:

- \`proof1.txt\` blob \`96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b\`, 18,553 characters;
- \`proof2.txt\` blob \`1c19b932a966fa1d260e8596054fb0e15337177a\`, 950,928 characters.

Also read: current issue #3 through its latest comment, \`AGENTS.md\`, \`CODEX.md\`, \`.codex/skills/pnp-research/SKILL.md\`, LSPV-2/542 report/code/raw, REF-539 code/raw, LSPV-3/555-556, LSPV-4/527-529, LSPV-1/558-559, and LSPV-5/478. Relevant predecessor material includes [P2-L2-540], [P2-L2-541], [P2-L2-542], [P2-L5-477], [P2-L5-478], and [P2-L4-527]. The latest LSPV-4/529 issue receipt confirms its publication; root \`main.tex\` remains unreadable through the contents connector (nonempty blob \`0fe79071499c352808d792f385c4b66299385f37\`, zero returned bytes).

Primary standards and papers:

- RFC 8259 permits a minus before the integer zero in JSON number grammar.
- ECMAScript 2026 specifies that \`Map\` discriminates keys by SameValueZero, which merges +0 and -0.
- Cousot and Cousot, POPL 1977, supplies the concrete-to-abstract soundness discipline.
- D'Silva–Haller–Kroening, *Abstract Satisfaction*, POPL 2014, does not authorize omission of a concrete accepted transition from a lower-bound MAY abstraction.

Change-aware repository review:

| Repository/path | Current blob | Result relevant here |
|---|---:|---|
| \`konard/p-vs-np/README.md\` | \`0e0ec77f83ad6eec1719a96066108b96ac1c2a95\` | Explicitly scoped formal models; build badges do not establish P vs NP. |
| \`blkph0x/p-vs-np-proof-research/README.md\` | \`f397a7747eaca82df3d754d0a4b4bab1fe10f814\` | Explicit bounded/promised scope and audited obstructions, no unrestricted result. |
| \`meelgroup/frat-xor/README.md\` | \`38a137bca4d4ab6443703d4c31fba5783021c581\` | Typed proof-format/checker boundary is explicit; not the historical /341 grammar. |
| \`tanyongkiam/cake_lpr/README.md\` | \`e94f45e9aa000cd9ada12f4c771ac9daf28fe53c\` | Verified-checker artifacts are tied to fixed formats/toolchains. |
| \`digama0/frat/README.md\` | \`0864ba034d50dbacfb1835c24d108e93d0a8bad9\` | Proof-format tooling supplies no automatic R_mix341 syntax theorem. |

Google Drive search for \`R_mix341 P2-D1 P2-C3 P2-B1 LSPV-5\` returned no files. This is recorded as an empty search result, not a review of unavailable Drive material.

### ITERATE

The initial repair claim was narrowed:

> **Revised claim.** The 542 occurrence transporter is sound for its declared typed SOURCE/AND3/XOR fragment and correctly transports canonical/permuted source occurrences, but it is an under-approximation of the recovered /341 accepted-byte language. It cannot serve as a complete all-path P2-C3 MAY abstraction unless an independently proved normalizer maps every accepted native packet into the typed fragment at no greater logical cost while preserving source and goal.

## Exact accepted-byte counterexample

Starting from the pinned seven-fixture baseline, the first paid ID \`"d0"\` and its unique child reference were changed only at the raw token level:

| Field | Raw JSON token | Parsed ECMAScript Number |
|---|---:|---:|
| paid definition ID | \`-0\` | negative zero |
| child parent reference | \`0\` | positive zero |

The tokens are byte-distinct. \`Object.is(-0,0)\` is false, but JavaScript strict equality and \`Map\` lookup merge them. The unchanged recovered checker therefore accepted the 197,509-byte packet with all **30,714 checks**, producing stdout identical to the baseline. Packet SHA-256:

\`0e5daff525736eaa040bb56950f6214d486614ebdea5db13431d2ca6d61c086d\`.

Controls:

- raw strings \`"-0"\` and \`"0"\`: rejected;
- definition \`-0\` and unbound parent \`1\`: rejected;
- strict REF-539 replay on the same one-fixture packet: rejected at paid-ID freshness/type boundary;
- LSPV-2/542 transport: \`REFERENCE_REJECT\` for the same reason;
- exact unmodified 542 canonical/permuted K4 controls: both verified, paid work 15, mapping swaps external occurrence indices 0 and 1 as intended.

## Symbolic consequence for P2-C3

Let \(C\) be the recovered checker's concrete accepted-byte configuration space and \(A\) the strict reference fragment. The counterexample is a completed concrete refutation in \(C\) with no corresponding accepted state in \(A\). Therefore direct projection to REF-539/542 violates concrete-step inclusion and completed-refutation preservation.

A lower-bound CEGAR loop may refine away only concretely spurious abstract paths; this path is concretely accepted and therefore must remain, or be covered by a proved cost-nonincreasing source/goal-preserving normalizer. The repair is simple for the **separate typed calculus**: require globally unique nonempty string IDs, as REF-539 already does. Requiring merely \`Number.isSafeInteger(id)\` is insufficient because \`Number.isSafeInteger(-0)\` is true.

## Resource ledger

The unchanged seven-fixture logical ledger remains 622 paid nodes; attacked K4 work remains 15 paid nodes. The independent audit measured:

- baseline parse/check: 174.15 ms;
- hostile parse/check: 150.59 ms;
- string-control check: 61.42 ms;
- unbound-control check: 61.54 ms;
- audit-orchestrator wall time before final write: 459.01 ms;
- orchestrator peak RSS: 42,248 KiB;
- orchestrator CPU: 0.0075 s user + 0.0119 s system.

These are local Node orchestration measurements. Child-verifier CPU/RSS, GitHub retrieval/publication, network caches, and physical indexed-machine work space were not measured. Parsing, token materialization, temporary files, source/reference reads, hashing, output, and publication remain real charged phases. No inference from logical paid work to physical memory is made.

## Corpus reconciliation and status

**CORPUS REVIEWED.** Root trackers; current issue; governance/skill files; relevant 539-559 reports, code, raw evidence, handoffs; required external repositories; primary JSON/ECMAScript and abstract-interpretation sources.

**DUPLICATION / CONTRADICTION AUDIT.** [P2-L5-477] already established an unsafe-integer alias above \(2^{53}\); [P2-L2-540/541/543] already established broader JSON/coercion/serialization hazards. The new point is narrower and nonduplicative: **even safe integer-valued numeric IDs are not injective under raw token identity because \`-0\` and \`0\` merge in \`Map\`**. This defeats “safe integer IDs” as a sufficient repair and directly demonstrates that 539/542 misses a recovered-checker accepted completed proof.

**WHAT CHANGED RELATIVE TO ROOT MAIN.** P2-D1 and P2-C3 remain OPEN, but their identifier-authentication sub-obligation is sharpened: canonical string IDs or an equivalent injective raw-token-to-key theorem is necessary. Root \`main.tex\` could not be reconciled because the connector returned zero bytes for a nonempty current blob; it was not overwritten.

**ADOPTED.** 542's occurrence-bijection theorem at its declared typed-fragment scope; REF-539 string-ID discipline; 478 source-binding separation.

**REJECTED.** Any promotion of REF-539/542 to complete recovered-checker coverage; any claim that safe-integer numeric IDs alone repair byte identity.

**STALE/OVERSTATED CLAIMS FOUND.** None in the peer reports as scoped; all already state that the typed reference is separate from the historical full grammar.

**Affected status:** material evidence node [P2-L5-479] refines still-OPEN [P2-D1] and [P2-C3]. It does not advance [P2-B1]; [P2-B2]/B3 remains separately OPEN.

## Reproducibility

- audit: \`experiments/review/lspv5_479_negative_zero_id_alias_audit.js\`, source SHA-256 \`ed7b3de79f2a55b98175e9b6947d03ecc6c4caa97ad8408cbd0192b80e56893d\`;
- raw: \`results/raw/arc/2026-11-10_1720_LSPV5_479_NEGATIVE_ZERO_ALIAS_RAW.json\`, source SHA-256 \`94825566d204a5f776b64f3cb468a03fe38787391a1b9ba624d809f9daa7f75e\`;
- accepted hostile packet: \`results/raw/arc/2026-11-10_1720_LSPV5_479_NEGATIVE_ZERO_ALIAS_ACCEPTED.json\`, SHA-256 \`0e5daff525736eaa040bb56950f6214d486614ebdea5db13431d2ca6d61c086d\`.

## Precise remaining gap

Authenticate the complete historical accepted-byte grammar, or prove a source/goal-preserving, cost-nonincreasing normalizer for every accepted native packet—including RES, LOCAL-CONVERT, DEF/facets, contexts/branches/joins/deletions—into a typed calculus. Only then can P2-C3 be used against the full P2-B1 minimum. P versus NP remains OPEN.

