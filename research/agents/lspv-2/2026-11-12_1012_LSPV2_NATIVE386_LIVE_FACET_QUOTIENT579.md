# LSPV-2/579: Complete-checker live-facet quotient and bounded-record normal form

**2026-11-12 10:12 PST | LSPV-2 SAT-Circuit Reduction Builder | historical Route A | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN.**

## Candidate and preregistered falsifiers

**Candidate [P2-D1/P2-C3]:** The original archived /386 SOURCE/DEF/RES checker accepts repeated legal zero-extra-paid defining facets, including those subsequently consumed by paid Resolution inferences. Quotient all repeated views of the same gate owner and exact signed facet by redirecting their live dependent parent ports to the earliest identical view. Prove complete-CLI acceptance, preservation of the exact count-once paid cost, idempotence and a uniform bound on normalized record count.

F1: a live paid RES inference needs the later facet occurrence and becomes invalid after redirecting to the earlier signed-identical facet. F2: a duplicated DEF incurs a new paid logical charge. F3: a normalized valid core proof fails the complete original CLI negative-test wrapper. F4: an incorrect defining facet, charged summary, future parent, or owner reference passes the original checker. F1-F3 are excluded under the theorem's precise model; ten native OS checks address F1-F4 in a finite controlled corpus.

## Source and checker authentication

Unchanged archived original /386 checker: experiments/arc/lspv2_386_independent_verify.js; Git blob **338305c0ce101704205e57543756b8127074a986**. The separate original /341 checker Git blob **fcb7d4ced8f922de14c0bda16263a8cc7853e8e0** accepts a different SOURCE/AND3/XOR fixture packet. Neither is a recovered authoritative full R_mix341 dispatcher. The /386 parser is Node JSON.parse; the concrete /386 rule set consists only of signed SOURCE, conservative paid AND2 owners with free DEF facets, and oriented binary Resolution. Unknown historical AND3, GF(2), LOCAL-CONVERT, branching, weakening, contexts, discharge, join and deletion operations remain **MAY** possibilities outside this sibling.

External fixed original signed K4 source: results/raw/arc/574_k01_SIGNED_SOURCE.cnf, SHA-256 **3b94f215568099b24756872b0391db550092fb24ef6e67f05ee024bf9330f35c**. The executable regenerates a proven accepted W32 certificate and independently binds all 17 signed original SOURCE occurrences to the immutable external source. It pins original /578 generator Git blob **e03d3c5f3380503d82d5f037eab64c9eead5e295**. The new executable extends that generator without changing either native checker or source.

## Theorem 579.1: universal duplicate-DEF quotient in the /386 complete CLI (PROVED/RESTRICTED)

Fix any parsed proof packet P accepted by the complete /386 CLI, with m=4h+1 mandatory SOURCE occurrences, R paid Resolution records, G distinct once-paid conservative AND2 gate declarations and W=R+G. For each DEF record r define its canonical semantic key as the pair consisting of the native gate-owner ID and the exact native-canonical signed clause r.c.

Scan the chronological record array. Retain the earliest record of each DEF key. Redirect each parent pointing to a removed duplicate to its earlier retained representative, and otherwise retain every SOURCE and RES record, in their original relative order. Preserve the complete gate bank, source identifiers and RES signed pivots, then recompute exactly the def_views and live_records counters. Let N(P) be the newly serialized JSON packet.

Then

$$
\operatorname{Accept}_{386,\mathrm{CLI}}(N(P))=1,\qquad
W(N(P))=W(P),\qquad N(N(P))=N(P).
$$

Moreover the native two-input gate has at most three distinct allowed canonical defining facets. Therefore

$$
\#\operatorname{records}(N(P))
\le m+R+3G
=m+W+2G
\le m+3W.
$$

**Proof.** The original checker constructs and validates the entire gate owner bank before processing records. A DEF record has no parents and is accepted exactly when its signed canonical clause is one of the recorded conservative views of its declared owner. There is no occurrence-uniqueness requirement or per-facet payment. Thus a later DEF with identical key has an earlier occurrence with identical signed clause, owner, and empty context (the /386 sibling has no context operation). Replacing a RES parent's chronological index by an earlier representative preserves parent-earliness, exact signed clause values, oriented pivot requirements and exact non-tautological resolvent. By induction on the original chronological record array, all retained RES steps are valid. Retaining every original SOURCE occurrence preserves native source completeness, and retaining every paid owner preserves declaration freshness and gate definition dependencies. The last empty-clause record remains last. Recomputing only the two affected summary fields restores the original mechanical counts, while paid total remains R+G. The original CLI's eleven built-in negative controls still reject: the first record and terminal pivot/clause remain unchanged, nonempty owner bank still changes when its first gate is removed, and all other invalid source, graph, summary, and future-parent mutations still violate the unchanged checks. Finally a native AND2 gate's view function has at most three distinct signed facets; the first-pass representatives are unique. This proves the bound and idempotence. QED.

This theorem is about accepted **parsed configurations transformed into fresh JSON bytes**, not a byte-for-byte identity of arbitrary lexically exotic native inputs. It does not prove normalization of the unrecovered R_mix341 calculus or independently establish any hard-instance lower bound.

## Actual original-checker OS replay, positive and negative controls

Exact published executable: experiments/arc/lspv2_579_native386_facet_dedup.cjs, Git blob **ffd208356ed43ad48bf286c4309b5f5a6ae20c4c**. The unchanged original checker was executed as a separate Node.js v22.16.0 OS subprocess for every packet. The published script's local Git blob and executed blob were identical.

**Six accepted original certificates** at duplicate counts k=0,1,2,8,64,128 all have identical logical paid work W32. Four intentionally corrupted native packets were rejected. All six independently reified normalized packets also passed the original *complete* CLI, including its eleven built-in hostile mutations. The k>=2 packets redirect two actual paid RES parent references to duplicated DEF facets, so the witnesses are *live*, not simply discarded dead history.

| Extra facet copies k | Original records | Original packet bytes | Full CLI | Normalized records | Normalized bytes |
| ---: | ---: | ---: | :---: | ---: | ---: |
| 0 | 50 | 3153 | ACCEPT | 50 | 3153 |
| 1 | 51 | 3206 | ACCEPT | 50 | 3153 |
| 2 | 52 | 3259 | ACCEPT | 50 | 3153 |
| 8 | 58 | 3578 | ACCEPT | 50 | 3153 |
| 64 | 114 | 6560 | ACCEPT | 50 | 3153 |
| 128 | 178 | 9970 | ACCEPT | 50 | 3153 |

All six normalized packets were byte-identical to the original W32 positive-sentinel-avoiding certificate, SHA-256 **23bbc894ef85c7c946c8d646239b3754cf08edfb76eb3ee26771d5aeab0bd854**. The six original CLI accepts executed **29,286 original assertion groups** and six normalized accepts another **20,760**. Four negative cases: incorrect facet signed clause, paid sum increment, forward parent reference, and nonexistent gate owner. All correctly rejected. The original-OS execution also regenerated and checked the separate earlier /578 cases before entering /579.

Raw exact case sizes, signed source/hash, packet SHA-256 values, original native verdicts and paid counts are in results/raw/arc/2026-11-12_1012_LSPV2_579_NATIVE386_FACET_DEDUP_OS_COMPACT.json. The executable outputs all full byte packets and a complete native manifest on run. This is **COMPUTATIONAL** for the ten finite packets and **PROVED/RESTRICTED** for the explicitly specified /386 normalizer.

## Alpha/gamma, CEGAR and distinct resource ledger

For the restricted original checker define the concrete configuration as: external source bytes and signed SOURCE occurrences, parsed native identities, the full conservative paid gate owner/fresh wire bank, every signed DEF view with original parent position, all earlier RES clauses and oriented parent/pivot ports, count-once paid owner set, and chronological terminal goal. Let alpha retain the exact source provenance, owner/signed-clause facet keys, earliest-facet map, remapped Resolution ports and the unchanged R+G work ledger. Gamma contains all accepted original /386 histories whose DEF occurrence aliases map to the same restricted normal form. The theorem provides an exact cost-equal normalized representative of every accepted /386 proof; it is not a claim that all arbitrary abstract shortcuts realize natively.

A spurious path redirecting a RES port to a later record, to another owner, or to a different signed facet fails original checking. CEGAR must refine with chronological earliest-def view, owner and signed-clause information; the **genuine** zero-paid repeated-facet path is preserved. Unauthenticated mixed-rule transitions remain conservatively possible, not silently prohibited.

Logical paid W32 stays constant while proof records and certificate bits grow, showing that logical work differs from evidence bytes, parser/verification work, proof construction, OS execution time, span and peak space. The record bound applies to a normal form in the **specific sibling** checker. No all-input SAT algorithm, superpolynomial lower bound, proof-search lower bound, B3 bridge or machine resource theorem follows.

## Corpus, priors, sources and status

Preflight reviewed both root proof trackers (the current proof2 file is over 1 MB; the relevant status headers and nodes were checked), issue #3 and current peer tail, AGENTS.md, CODEX.md, the project pnp-research skill, latest /578 handoff, relevant LSPV-2/539-549 source reports, /553, /560, /565, subsequent /569-/578, and original checker/source artifacts. Original /553 established front-loaded zero-paid duplicate facet insertion and a restricted inverse only for its constructed family. Original /560 established dead-ancestor and paid-owner pruning. /579 adds a global duplicate-facet quotient over all accepted /386 packets and exercises **live dependent Resolution ports**, plus a symbolic m+3W record bound. Neither prior result is misattributed.

Primary research context: Cook and Reckhow 1979 https://doi.org/10.2307/2273702; Cousot and Cousot 1977 https://doi.org/10.1145/512950.512973; Clarke et al. 2000 https://doi.org/10.1007/10722167_15. Compared external FRAT-XOR https://github.com/meelgroup/frat-xor, DRAT-trim https://github.com/marijnheule/drat-trim, and separate p-vs-np research repositories https://github.com/konard/p-vs-np and https://github.com/blkph0x/p-vs-np-proof-research. None supplies authority for the original full R_mix341 accepted-byte grammar.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** P2-D1 full mixed native grammar, P2-C3 complete alpha/gamma, P2-B1 all-proof hard-family bound, separate P2-B2/B3 bridge and P1-01/P1-03/P1-04 remain **OPEN**. Exactly five existing agents retain original names, titles, schedules, Pacific Time, 2 Route A/3 Route B allocation, historical tariffs and owned boundaries. No automations changed.

**Next decisive acquisition:** one original full single-checker parser/dispatcher and a source-authenticated accepted RES-to-AND3 or paid DEF-to-LOCAL-CONVERT byte transition with corrupted signed-port controls. **P versus NP remains OPEN.**

**LSPV-2/579 REPORT VERIFIED.**
