# LSPV-4/525: Paid sharing, XOR cancellation, and native resource firewall

**2026-11-10 13:36 PST | LSPV-4 Time-Space Resource Auditor | Route A label retained | PROVED/RESTRICTED and COMPUTATIONAL | P versus NP OPEN**

## IDEA, falsifiers, and precise scope

Candidate: an original-source-authenticated strict K4 Tseitin 3-CNF SOURCE/AND3/XOR refutation admits an arbitrarily long, nonminimal, **genuinely shared paid XOR proof DAG**. This tests whether component abstractions illegitimately charge a reused node twice, while distinguishing the limited original /341 fixture verifier from a separately specified semantic reference.

F1: typed, independently external-DIMACS-bound /539 checker rejects the sound XOR detour. F2: recovered original /341 verifier accepts the longer packet despite its hard-coded 4V-1 inference count. F3: first-creation costs, paid consumer surplus, or dependency depth disagree. F4: bad terminal RHS, changed original source, or missing parent is accepted by the typed reference. All four falsifiers were tested in the declared scope; none defeated the theorem.

## SEARCH and primary-source authentication

Read the **complete** current root proof1.txt (Git blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b), proof2.txt (at startup c3bde0f01a29b312a2395a7afc0f3534d76aba86, 917453 characters), issue #3, AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md, current role handoffs, LSPV-4/522-524, LSPV-2/538-540, LSPV-1/555, LSPV-3/549, LSPV-5/477, GROKPROOF/2026-11-10_1212_GROK_REVIEW.md and research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex. The Claude note uses a distinct sequential one-tape model.

Original project file blobs independently fetched:
- experiments/arc/lspv2_341_mixed_tseitin_min_dag.js: 4081022e8a3841d79f751a3d3a7a10decbb026da.
- experiments/arc/lspv2_341_independent_verify.js: fcb7d4ced8f922de14c0bda16263a8cc7853e8e0.
- experiments/arc/lspv2_539_strict_fragment_reference.cjs: fc91a6f33d0d010d6225365a3d9ce72a090af21f.

External repository checks: konard/p-vs-np scripts/proof_status.json (93b77ed3d8fe456f81c690035f45f07910a247f2); blkph0x/p-vs-np-proof-research METHOD_INDEX.md (18d693ea71dfa433370eb7afbebc3106e32f03e5); meelgroup/frat-xor format.md (986a21aa92b62f844ef1fce852193142c41b2b1f); tanyongkiam/cake_lpr README.md (e94f45e9aa000cd9ada12f4c771ac9daf28fe53c). These represent separate proof languages, not historical R_mix341 authority. Primary theory controls: Cook-Reckhow, J. Symbolic Logic 44 (1979) 36-50, DOI 10.2307/2273702; Cousot-Cousot, POPL 1977, DOI 10.1145/512950.512973; Blocki-Zhou, *On the Computational Complexity of Minimal Cumulative Cost Graph Pebbling*, arXiv:1609.04449.

## Theorem 525.1: exactly costed shared paid refutation family

Let F be the original signed strict proper odd-charge K4 Tseitin 3-CNF of 16 clauses and 6 variables, independently supplied as 163 ASCII DIMACS bytes. Let P0 be its source-bound typed 15-inference refutation with false affine terminal z0 = d14 (row 0=1). Let a=d12 be an earlier verified nonterminal affine row. For any integer k>=0, append fresh, **paid** binary-XOR inferences

$$
u_i=\operatorname{XOR}(z_{i-1},a),\qquad
z_i=\operatorname{XOR}(u_i,a),\qquad 1\le i\le k.
$$

All parents are previously defined and have distinct IDs; the new IDs are globally fresh. For each i, the GF(2) algebra gives z_i=z_(i-1)=0=1. All 16 original clauses remain in the final sink ancestry. This is a valid refutation in the separate typed, original-source-bound /539 SOURCE/AND3/XOR fragment for every k, **not** an authenticated historical full-calculus rule language.

The exact charges and structural parameters are

$$
m=16,\quad q_k=W_k=15+2k,\quad
R_k=30+4k,\quad S_k=2k,\quad
\deg^+(a)=1+2k,\quad D_k=6+2k.
$$

Here W counts each distinct first-created paid inference once at **fixed unit price**; R counts explicit premise-reference occurrences, not an invented native reference tariff; S is the total nonsink consumer surplus; and D is ideal parallel dependency span in unit-inference weights. The identity q-(m-1)=S holds exactly, as required by [P2-L4-524]. The first pair contributes two fresh paid nodes, two additional uses of the same paid anchor a, and two levels of dependency depth; induction gives all formulas.

The basic 15-node refutation already provides a cheaper legal OR alternative. Each original K4 clause is deletion-essential, so every sound original-source-explicit at-most-binary unit-paid refutation in the declared fragment must use all 16 clauses, giving the lower bound 15 and hence **exact restricted minimum 15**. Every k>0 packet is intentionally nonoptimal and cannot establish a lower bound against other legal proof choices.

## Theorem 525.2: explicit cost partition and overcharging counterexample

Allocate all 15 original paid records to the core component and precisely the 2k fresh paid records to the detour component. The repeated references to a incur no second **inference-creation charge**. Hence

$$
W_{\rm core}+W_{\rm detour}=15+2k=W(P_k).
$$

A purported cost-sound abstraction that charges each of the additional 2k anchor references as a second paid **creation** instead obtains 15+4k, strictly **above** the concrete 15+2k for k>0. This violates the required abstract-path cost <= concrete cost. Any actually authenticated reference/application tariff must be charged separately in BOTH concrete and abstract ledgers. This family is a concrete counterexample to double-charging, rather than a completed proof of P2-C3.

There are no branch contexts or discharged hypotheses in this particular example. Native CASE, WEAKEN, DISCHARGE, JOIN, DEF/facets, LOCAL-CONVERT, RES and private/exported wires remain **UNAUTHENTICATED**. They cannot be forbidden to protect a conjectured lower bound.

## ITERATE: original-function replay and independent restricted checker

The pinned **original** /341 producer and checker bodies were executed in isolated V8, adapting only file/stdout access. The separately defined typed /539 checker was executed with a separate exact original DIMACS source. The temporary SHA256 digest adapter for /539 was a stub: it **does not** constitute a source SHA256 result. The reported Git blob IDs come from independent repository reads.

| k | Paid W | References R | Span D | Reuse surplus S | Fanout(a) | Packet JSON bytes | Typed /539 | Recovered /341 |
|---:|---:|---:|---:|---:|---:|---:|---|---|
| 0 | 15 | 30 | 6 | 0 | 1 | 3563 | ACCEPT | ACCEPT |
| 1 | 17 | 34 | 8 | 2 | 3 | 3754 | ACCEPT | REJECT |
| 2 | 19 | 38 | 10 | 4 | 5 | 3945 | ACCEPT | REJECT |
| 4 | 23 | 46 | 14 | 8 | 9 | 4327 | ACCEPT | REJECT |
| 8 | 31 | 62 | 22 | 16 | 17 | 5091 | ACCEPT | REJECT |
| 16 | 47 | 94 | 38 | 32 | 33 | 6619 | ACCEPT | REJECT |

The recovered checker explicitly rejects all k>0 packets at its hardwired 4V-1 proof-candidate-length check. Its REJECT does not prove the valid typed derivation is illegal in intended historical R_mix341; rather the two **accepted languages differ**. All five wrong-terminal-RHS mutations were rejected by the typed reference, and the published audit also includes an altered-external-source and a missing-parent hostile control. Original V8 harness: 35 checked conditions. The newly published standalone Node audit is source pinned and syntax inspectable but **was not run as a local Node OS process in this isolated V8 execution**.

## Resource ledger and physical firewall

| Part | Fixed logical charge in declared reference | Evidence / sequential time / span / retention / physical space |
|---|---|---|
| Original SOURCE | 0 paid inferences | 163 external signed DIMACS bytes, finite input parsing/source matching, source reads and indices; cannot be treated as zero physical memory. |
| Original K4 AND3 | 12 distinct paid, one unit each | Two parent IDs and support/truth table or checked affine alias; local eight-case truth-table checking, parent retrieval and working arrays. Original checker has known accepted type-coercion defects [P2-L2-538], excluded only in the separate typed reference. |
| GF(2) / XOR | 3+2k distinct paid, unit each | Two explicit references, mask and RHS, source-bound row semantics; actual parse, BigInt XOR and mask bit lengths; logical span D=6+2k, NOT verified physical parallel time. |
| Shared a=d12 | one paid creation **total** | Additional 2k reference occurrences consume actual evidence bytes and lookup/retention time; do NOT manufacture unit-priced native reference tariffs. |
| Proof output and memory | not measured by W | JSON packet 3563..6619 bytes plus 163-byte source. For arbitrary k decimal IDs give O(k log(k+2)) evidence bits. The fixed printed topological order with immediate last-use release has **5 live derived values** for the tested k, but the original JavaScript checker retains a materialized input/Map, and physical peak is larger. No unrestricted live-value optimum claimed. |
| Alternatives, search, failure and recomputation | not counted in W | Real construction, acquisition, failed strategies, persistence, source authentication, cache, retrieval, duplicate parse, index/head movement, recomputation and readback require their own serial-time/all-phase writable-space ledger. |
| Other historical native operations | UNKNOWN | Cannot determine their accepted bytes, weights, zero-cost closure behavior, context scope or memory effects from this fragment. Include all as MAY until authenticated, including cheap XOR and paid extension shortcuts. |

The numerical packet-size increments happen to be 191 bytes per pair for the tested two-digit identifiers. They are not claimed constant for unbounded k. Identifier size and UTF-8/JSON lexical alias risks [P2-L5-477], [P2-L2-540] remain material. High-width sparse GF(2) rows, extension variables, branch joins, and retention/recomputation tradeoffs remain explicit unresolved falsifiers for full R_mix341.

## Status and publication

**Actual advance:** a parametrically proved, genuinely shared paid-XOR proof family, a count-once cost partition with explicit overcharge falsifier, independently original-source-bound finite replay, and a differential proof that the recovered /341 hardwired fixture language is stricter than this separately authenticated sound typed fragment. Unlike LSPV-4/523-524's tree-only original fixtures and LSPV-2/539's safe **unused** extra paid node, this control has genuine paid reconvergence in the **sink ancestry**.

**Affected evidence node:** [P2-L4-525], supporting still OPEN [P2-D3], [P2-D1], [P2-C3] and [P2-B1]. No historical rule or weight is changed. [P2-B2]/B3 remain separate and OPEN.

**Artifacts:** experiments/arc/lspv4_525_native_shared_xor_audit.cjs; results/raw/arc/2026-11-10_LSPV4_525_NATIVE_SHARED_XOR_RAW.json; research/coordination/2026-11-10_LSPV4_NATIVE_SHARED_XOR_FIVE_ROLE_HANDOFF525.md.

**Verification:** original-function V8 differential and negative controls; published executable not OS-executed in this run. **Publication:** role-owned report/code/raw created; tracker and issue updates must be current-SHA, merge-safe and fully read back. **Remaining gap:** authenticate the actual all-rule historical byte parser [P2-D1], prove every-rule cost-sound concrete-inclusive abstraction [P2-C3], then establish all-legal-proof lower bounds [P2-B1], with B3 separate. P versus NP OPEN.


### Theorem 525.3: exact joint fanout times identifier-length evidence floor (PROVED/RESTRICTED)

For any k>=1 and integer L>=3, rename the existing paid anchor ID d12 (three ASCII characters) to a globally fresh, JSON-safe ASCII string consisting of L copies of the letter L, replacing **all** its parent occurrences, with no other proof alteration. The separate typed /539 checker still accepts, and the source/semantic graph, distinct-node logical weight $W=15+2k$, fanout, span and proof conclusion are unchanged.

The ID appears exactly once at its definition and $1+2k$ times as a reference, for $2k+2$ occurrences. Because all identifiers are encoded as unescaped ASCII JSON strings and their quotation/syntax is unchanged, the exact increase in serialized certificate bytes is

$$
\boxed{\Delta B(k,L)=(2k+2)(L-3).}
$$

This is a **cross-term** in fanout and physical identifier length. Counting a referenced lemma once in $W_R$ is correct, but does not make its repeated **byte-string occurrences** free to emit, parse, compare or retrieve.

| Detour pairs k | New anchor-ID length L | Paid W | Extra JSON bytes | Total packet bytes | /539 reference |
|---:|---:|---:|---:|---:|---|
| 1 | 128 | 17 | 500 | 4254 | ACCEPT |
| 1 | 512 | 17 | 2036 | 5790 | ACCEPT |
| 1 | 2048 | 17 | 8180 | 11934 | ACCEPT |
| 1 | 8192 | 17 | 32756 | 36510 | ACCEPT |
| 16 | 128 | 47 | 4250 | 10869 | ACCEPT |
| 16 | 512 | 47 | 17306 | 23925 | ACCEPT |
| 16 | 2048 | 47 | 69530 | 76149 | ACCEPT |
| 16 | 8192 | 47 | 278426 | 285045 | ACCEPT |

This proves a representation-specific explicit-byte lower bound of $\Omega(kL)$ for these particular certificates, **not** a lower bound on the shortest encoding, cheapest semantically equivalent proof, or any SAT algorithm. Compact canonical IDs or a different proof DAG can avoid the overhead; the original k=0 15-step proof remains a valid cheaper option.

The **published GitHub audit file** (blob 388996bfdec25bfd1d349903ce462c86f58c3b83) was subsequently executed inside V8 with mock Node file/VM/crypto/Buffer adapters, and passed **84 assertions** covering six unrenamed cases, eight long-ID cases, original checker rejection, and source/parent/terminal corruption. This is **not** an OS-level Node execution. Cryptographic adapters were stubs; GitHub blob SHAs were checked independently using actual repository fetch results. Its raw file, blob 7bedec99de08a2460cca6fec285a5c74d1d9821a, contains the exact byte ledger.

The additional theorem is the new physical resource advance beyond the earlier count-once logical work identity. For full R_mix341, reference tariffs and any compact reference addressing scheme must be authenticated before promoting the $\Omega(kL)$ cost to a rule-system-wide statement.
