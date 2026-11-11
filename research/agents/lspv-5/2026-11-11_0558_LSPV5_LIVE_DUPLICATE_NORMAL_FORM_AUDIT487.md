# LSPV-5/487: live repeated-facet normal-form audit under a binary64 parent alias

**2026-11-11 05:58 PST | Independent Proof Red Team | historical Route B | PROVED/RESTRICTED finite witness lemma + COMPUTATIONAL unchanged-checker replay | P versus NP OPEN**

## IDEA: target and falsifiers stated before search

**Target.** Attempt to falsify LSPV-1/569's restricted archived-`/386` normal-form step on the harder composition in which a repeated zero-charge DEF facet is actually referenced by a later paid Resolution node and that reference is written as a raw exact noninteger decimal accepted through binary64 rounding. The prediction was that deleting the duplicate, redirecting its consumer to the earlier identical facet, and reindexing every later parent would preserve complete original-checker acceptance and paid work.

Falsifiers:

1. deduplicating the referenced facet creates a future or dangling parent;
2. the retained earlier facet is not an admissible substitute for the live duplicate;
3. a raw numeric alias changes the logical minimum or prevents cost-preserving normalization;
4. the proposed normalization passes a reimplementation but fails the unchanged archived checker.

The unchecked delete in F1 and wrong-facet redirect in F2 both reject, as they should. The fully redirected normalization accepts and exactly recovers the original seed bytes after canonical serialization. F3 and F4 did not occur in this witness.

## SEARCH: source authentication and corpus reconciliation

I read complete current `proof1.txt`, Git blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`, and complete current prepublication `proof2.txt`, blob `7db80e8b55a7f5c348fbb2ed8decd3ceaa2657f3`; current coordination issue #3; `AGENTS.md`; `CODEX.md` blob `754999f50de93cdb693ed37bc8110d31e9e698ef`; and `.codex/skills/pnp-research/SKILL.md` blob `b8df83a7b0b1428f349b0e02ce1387d979e8db7f`. Google Drive search for `R_mix341 normal form repeated DEF facet Resolution parent` returned no result.

Material peer sources actually read include LSPV-1/569's bounded normal form, LSPV-1/571's exact archived-CLI characterization, LSPV-2/555's live DEF-to-RES splice, LSPV-2/556's real OS replay, LSPV-3/569's component-syndrome source quotient, LSPV-4/541's canonical-byte rescan theorem, LSPV-5/485--486, Grok `GROKPROOF/2026-11-11_0620_PROGRESS.md` blob `fd5754e590a16d21c698836fd995144a65a91391`, and Claude world-ledger blob `79e4d4e7e0e3edff3aba8610852c45534bdde128`. Relevant 539--549 results remain restricted reference or sibling-checker results, not authentication of one all-rule native dispatcher.

The exact unchanged executable is `experiments/arc/lspv2_386_independent_verify.js`, Git blob **`338305c0ce101704205e57543756b8127074a986`**. The exact source-bound seed is `results/raw/arc/2026-11-10_2124_LSPV3_561_ARCHIVED_386_NATIVE_PACKET.json`, blob **`d0fa96a155672f8f6a6a3428eacafa15e79b9e88`**. It contains 17 SOURCE records, three free DEF facets for one paid owner, 49 paid RES records, 69 total records, and $W=50$.

Primary sources checked were Cook--Reckhow (1979) for proof-system-specific cost, Cousot--Cousot (1977) for sound abstraction, and Clarke--Grumberg--Jha--Lu--Veith (2000) for concrete counterexample replay in CEGAR. The required repository review found no matching historical grammar in `konard/p-vs-np`; `blkph0x/p-vs-np-proof-research` keeps source/replay limitations explicit; DRAT-trim documents format-specific deletion behavior; FRAT/FRAT-XOR use separately typed proof formats; and current `openai/math` contains formal SAT machinery but no authority for this archived language. The FRAT-XOR code-search query was rate-limited once; previously pinned head `18cd6bc17af10a9891c10a846ce966166f9fe0dc` and its unique-ID behavior remain only a comparison. `openai/math`, `anthropics/formal-math`, CakeLPR and DRAT do not supply the missing R_mix341 checker.

**Duplication/contradiction audit.** LSPV-4/541 already showed that unreferenced repeated facets do not raise logical work, and LSPV-2/555 showed a different genuine live facet/RES detour. LSPV-1/569 proved the parsed-object duplicate-facet normal form. LSPV-5/485 proved accepted exact noninteger parent aliases. The new increment is the first direct composition of an **actively referenced repeated facet** with an accepted noncanonical parent lexeme, followed by exact inverse normalization through the original full CLI. This validates rather than supersedes those prior results.

## ITERATE: exact hostile packet and repaired normal form

In the seed, record 17 is the true facet

$$
D=(x_1\lor\neg z_8),
$$

and record 20 uses it as a parent of strict Resolution:

$$
D,\; (\neg x_1\lor\neg x_2\lor x_3\lor\neg g_7)
\;\vdash\;
(\neg x_2\lor x_3\lor\neg g_7\lor\neg z_8).
$$

The hostile positive packet inserts an identical owner/facet occurrence at new record 20, shifts all old records and parent indices at least 20 by one, and makes the shifted paid child at record 21 reference the duplicate. A second positive packet writes that live parent as the exact decimal token `20.000000000000001`. ECMAScript binary64 conversion maps that exact lexeme to Number 20, so the original integer/chronology checks accept it. The immediately separated token `20.000000000000004` parses as a noninteger and rejects.

Define the witness normalizer $q$ as follows: parse the accepted raw bytes; delete duplicate record 20; redirect every parent 20 to retained record 17; decrement every parent greater than 20; and recompute only `def_views` and `live_records`. Then

$$
q(P_{\rm alias})=P_{\rm seed}
$$

as exact parsed JSON, and canonical LF serialization has the seed's exact SHA-256 and Git blob. Paid owner and RES counts are unchanged, hence

$$
W(q(P_{\rm alias}))=W(P_{\rm alias})=50.
$$

This is a **PROVED/RESTRICTED lemma for this explicit witness**, by direct inspection of the transformation and exact equality to the authenticated seed. It independently validates one live instance of LSPV-1/569. It is not a new proof of the universal /569 theorem and not a full R_mix341 normal form.

## Original-checker results and hostile controls

The runner executed the unmodified archived source in actual Linux OS Node v24.22.1 subprocesses. A telemetry wrapper changed only `process.argv` presentation and registered an exit-time resource report; the checker source and every proof check remained byte-identical.

| Case | Bytes | Result | $W$ | Records | Original assertions | Child peak RSS KiB |
|---|---:|:---:|---:|---:|---:|---:|
| authenticated seed | 4,144 | ACCEPT | 50 | 69 | 4,492 | 41,404 |
| live exact duplicate | 4,192 | ACCEPT | 50 | 70 | 4,534 | 41,400 |
| live decimal alias | 4,208 | ACCEPT | 50 | 70 | 4,534 | 41,272 |
| normalized alias | 4,144 | ACCEPT | 50 | 69 | 4,492 | 41,404 |
| delete without redirect | 4,144 | REJECT | n/a | n/a | n/a | 38,520 |
| redirect to wrong facet | 4,144 | REJECT | n/a | n/a | n/a | 38,588 |
| alias outside rounding cell | 4,208 | REJECT | n/a | n/a | n/a | 38,460 |

All four positives also passed the original CLI's eleven synthetic negative checks: **44 built-in hostile checks and 18,052 assertion groups** in total. The accepted decimal-alias packet has SHA-256 **`7b004589433d188a46efe579aa643977c97ed43fbfdb2ef5ef89a939df7aa62e`** and Git blob **`42c2ea5fa274b77ea513814c4a4d45b26a49f089`**. Normalization returns SHA-256 **`2259e61a1e0e1a80f3be29490199af9a7c7f5382ecaf151b0a924d47c738ebff`**, Git blob **`d0fa96a155672f8f6a6a3428eacafa15e79b9e88`**.

The unchecked delete is rejected because its first shifted child points to itself/future index 20. The wrong redirect is rejected because facet 18 lacks the required positive pivot literal. These controls show why a semantic duplicate test alone is insufficient: parent redirection and chronology are proof obligations.

## Concrete/abstract configurations, polarity and CEGAR

For this archived checker only, a complete concrete scan configuration is

$$
C=(b,i,s,G,O,K,S,n_{src},n_{def},n_{res},w),
$$

where $b$ is the raw byte string, $i$ the current record index, $s$ the fixed internal source specification, $G$ the declared owner/output-wire map, $O$ the source-occurrence ledger, $K$ the chronological clause array, $S$ the seen-source set, the $n$ values are counters, and $w$ is charged owners plus charged RES occurrences. Parser state and raw token spans are part of a genuinely complete byte-level configuration; omitting them would erase the 485 alias phenomenon.

For the tested quotient, the abstract state is

$$
A=(s,G,O,\widehat K,\widehat E,w),
$$

where identical `(owner, facet clause)` records are represented once and every RES hyperedge points to that retained representative. The abstraction $\alpha$ first applies the historical JSON decoder, then the proved duplicate/facet redirection on this image. Its concretization $\gamma(A)$ is the set of raw byte strings whose historical parse and redirection produce $A$; it therefore contains both exact-integer and binary64-alias spellings. On the witness:

$$
\alpha(P_{\rm alias})=P_{\rm seed},\qquad
W^\#(\alpha(P_{\rm alias}))=50\le W(P_{\rm alias})=50.
$$

Completed-refutation preservation is not inferred from configuration cardinality: it is established here because the normalized object is exactly the already accepted seed and the original checker is rerun. No memory bound is inferred from the number of abstract configurations, and no proof-DAG work is reinterpreted as machine memory.

**CEGAR polarity.** The live duplicate and decimal alias are genuine concrete paths, so a refinement that deletes them is unsound for overapproximating the historical accepted-byte language. The outside-cell alias, unchecked delete and wrong-facet redirect are concretely rejected and may be excluded by refinements recording exact decoder value, chronology and owner/facet identity. This is the permitted direction: replay first, refine only proved-spurious paths.

The full-cost negative-proof transfer still requires, for every legal full-calculus refutation $P$, an admissible abstract refutation $P^\#$ with `cost(P#) <= cost(P)`. This run establishes that inequality only for the displayed witness pair. It does not cover AND3, GF(2), LOCAL-CONVERT, branching, contexts, discharge, joins, weakening, deletion, exported/private wires, ER/PHP or Tseitin shortcuts.

## All-phase resource ledger and model firewalls

- **Logical work:** 1 paid owner + 49 distinct RES nodes = 50 before and after normalization. The repeated facet costs zero only because that is the authenticated `/386` tariff.
- **Explicit evidence:** 4,208 bytes for the hostile alias; 4,144 bytes after normalization. Evidence size is not logical work.
- **Construction/search:** deterministic one-pass splice plus parent rewrite over 69 records; no claim that an optimal proof can be found this way in general.
- **Parsing/source/head reads:** JSON parse, internal source reconstruction, owner checks and all 17 SOURCE occurrences are charged by the actual checker run; repository/API retrieval is external research overhead, not proof work.
- **Verification:** positive subprocess wall times were approximately 59--80 ms in this run. These are environment-specific measurements, not asymptotic machine bounds.
- **Peak physical space:** measured child-process high-water RSS was 41,272--41,404 KiB on positives. This includes Node, parser, full materialized packet, checker tables, 64-row source control, output and telemetry. It is not a lower bound and not the logarithmic-workspace alternative of LSPV-4/541.
- **Retrieval/recomputation:** the original implementation retains arrays/maps; an alternative rescan verifier may trade polynomial time for lower work space. Neither implementation proves a proof-search space bound.
- **Failed policies:** delete-without-redirect, wrong-facet redirection and outside-cell alias all reject. No discovery cost is charged into the retrospective proof minimum.

No configuration-count-to-memory, proof-DAG-work-to-memory, or finite-byte-to-asymptotic-exponent inference is made. The `/386` checker is a sibling fragment, not the exact unified random-access FLMV machine or a SAT decider.

## Status, trackers, manuscript and next target

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** This run independently validates the existing restricted parsed-object normal form and the already tracked binary64 alias phenomenon; it does not change any root dependency or evidence status. Exact relevant tracker IDs remain `[P2-D1]`, `[P2-C3]`, `[P2-B1]`, separate `[P2-B2]`/B3, `[P2-L5-485]` and `[P2-L5-486]`. P2-D1, P2-C3, P2-B1 and P2-B2/B3 remain OPEN.

Root `main.tex` currently reports blob `5c117868624d40e93251b35934453eba6a746cb3`, but the connected full-file read returned **zero content bytes**. Therefore an exact LSPV-5-region replacement with outside-byte preservation was not safe and `main.tex` was not modified. A role-owned insertion fallback accompanies this report; this is a publication blocker, not mathematical evidence.

**What changed relative to root main:** one composed finite validation is now available; no executive theorem or tracker status changes. **Adopted:** /569 duplicate-facet redirection, /485 decoder quotient and /541 work/evidence separation. **Rejected:** deleting duplicates without a total parent map, redirecting merely by gate owner, and excluding accepted numeric aliases as CEGAR-spurious. **Retired:** nothing.

**Next decisive falsifier:** run the universal /569 normalizer on a packet where a retained facet is used by multiple reconvergent RES children and a nested renamed output wire is also a live pivot; then compare mathematical-core and exact full-CLI acceptance. In parallel, the load-bearing P2-D1 target remains one externally source-bound, genuinely heterogeneous certificate accepted by one authoritative historical checker with RES plus AND3/GF(2)/LOCAL-CONVERT and two wrong-port rejects.

No role, identity, title, schedule, timezone, historical rule/weight, ownership boundary, or two Route A/three Route B label changed. **P versus NP remains OPEN.**

