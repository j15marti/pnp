# LSPV-2/573: Native /386 paid-owner defining-facet CEGAR discriminator

**2026-11-12 04:12 PST | SAT-Circuit Reduction Builder | historical Route A | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

## Candidate construction and four falsifiers

**Candidate 573.1:** Two independently source-bound checker-accepted proofs have identical signed clause records, chronological RES DAG, paid work, source and even the same paid owner ID/output, yet admit different zero-extra-paid DEF-facet transitions. Therefore an abstraction that erases the owner-defining operands cannot decide exact next-step legality; its MAY paths require CEGAR refinement on owner/facet provenance.

F1: changing unused owner inputs invalidates the native base refutation. F2: both owner variants admit the same candidate facet. F3: the two apparently different owner banks are distinguished by the proposed coarse alpha. F4: a foreign owner, wrong facet, underpayment or forward parent escapes unchanged original-checker rejection. The exact original-OS experiment contradicts F1, F2, F3 and F4 for the stated packets.

## Original authority, scope and reproducibility

The unchanged, archived /386 implementation is **experiments/arc/lspv2_386_independent_verify.js**, pinned original Git blob **338305c0ce101704205e57543756b8127074a986**, SHA-256 **22d12f665fecede1a047ea20c0c2d3f245c7195ce5df44f342891198ea04a113**. This code independently verifies the restricted signed SOURCE, unit-paid conservative AND2 gate owner, zero-additional-paid DEF facet, strict signed binary RES language. Its own complete CLI performs eleven corruption tests. It is **not** a checker for the complete historical R_mix341 system.

The prior accepted W29 guarded K4 base packet is **results/raw/arc/2026-11-11_1112_LSPV2_562_ACCEPTED_CONE_W29.json** (original Git blob 318c52d99977ea4e91bc8554051138a700c1dc94). The separately supplied, exactly ordered 17-clause original-source file is **results/raw/arc/2026-11-11_0812_LSPV2_559_EXTERNAL_K4_SIGNED_SOURCE.cnf** (original Git blob e8bc4300f1f4518cb447edaf3f699bcee4839803; SHA-256 3b94f215568099b24756872b0391db550092fb24ef6e67f05ee024bf9330f35c). The executable checks every parsed signed SOURCE record against every external original clause in order. In both branches the external source is fixed, not rewritten by the certificate.

This is a new **transition-discriminability** test, not a new claim that native /386 validates a mixed RES-to-AND3 record. LSPV-2/553 already established free facet prefix insertions, /565 and /570 addressed stepwise restricted alpha and source-bound CEGAR, and /572 proved gate-owner topological presentation invariance. LSPV-1/566 treated record-DAG reordering, and LSPV-2/539, /547, /549 established the distinct checker grammars and a noncomposition firewall. This report specializes the **necessary defining-bank information** for exact CEGAR transitions, with two counterposed native accepts on the same projected state.

## Exact theorem 573.1: the defining-bank information is indispensable for exact transition recognition

Use a fixed source and its W29 original certificate. Give the checker one paid owner with ID 0 and output wire 8, choosing two legal definitions:

$$
D_A=(0,8,1,4),\qquad D_B=(0,8,2,5).
$$

All original SOURCE records and all 28 signed RES records are byte-identical in A and B. Neither proof record uses wire 8; the owner is paid once in both. Both are accepted full refutations at logical work W=29.

Consider an abstract state projection alpha0 which retains the external source bytes, source occurrences, every previously available signed clause, record kind/parent/index graph, declared paid owner ID and output, the number of owners and the paid cost, but forgets **the defining input operands** of owner 0. Then

$$
\alpha_0(C_A)=\alpha_0(C_B).
$$

For the insertion of a free defining facet of owner 0, the pinned original rule builds the exact canonical facets of z=a AND b:

$$
\{-z,a\},\qquad\{-z,b\},\qquad\{z,-a,-b\}.
$$

Thus the canonical clause [1,-8] is admitted from A and rejected from B; conversely [2,-8] is admitted from B and rejected from A. The complete original command-line checker validates these differences. Both inserts occur immediately before the first SOURCE record, with all subsequent RES parent indices incremented by one. Both legal insertions preserve the final empty RES clause and the exact W29 paid cost.

**Proof of non-exactness:** If a single-valued abstract exact legality predicate depends only on alpha0(C) and the proposed facet, it returns the same verdict for C_A and C_B because their alpha0 states coincide. The native legality relation gives opposite verdicts for [1,-8], a contradiction. Consequently no such predicate can be both sound and complete for these two concrete states. An overapproximating MAY abstract transformer remains sound only by retaining both transitions, admitting spurious paths for one of the concrete histories. A refinement retaining the owner-defining facet relation, or equivalent provenance sufficient to distinguish it, separates the two cases. QED, for this pinned restricted calculus.

**Important direction of the theorem:** This is a counterexample to an *exact* clause-only/owner-ID-only transition representation, not a counterexample to sound MAY overapproximation. Cost-sound negative-resource abstract interpretation may retain the spurious zero-charge edge and subsequently refine it; it may never delete the authentic cross-owner facet shortcut.

The one-owner bank is paid once independently of how many genuine facets are mentioned. The record's zero additional logical charge does **not** mean zero certificate bytes, parser/verifier work, critical span or physical memory. These are distinct ledgers.

## Actually executed original Node.js OS tests

The original archived checker ran unchanged in Node v22.16.0 subprocesses. The independent signed-source binding was checked before generation. Four accepts and six rejections matched the predeclared expectations, with **13,334 original assertion groups over the four accepts**, including 44 built-in corruption checks.

| Byte-exact construction | Verdict | Work | Bytes |
|---|---:|---:|---:|
| Base A, owner AND(1,4) | ACCEPT | 29 | 2866 |
| Base B, owner AND(2,5) | ACCEPT | 29 | 2866 |
| Free facet [1,-8] with A | ACCEPT | 29 | 2916 |
| Free facet [1,-8] with B | REJECT: not true gate view | 29 (declared) | 2916 |
| Free facet [2,-8] with B | ACCEPT | 29 | 2916 |
| Free facet [2,-8] with A | REJECT: not true gate view | 29 (declared) | 2916 |
| Foreign owner reference | REJECT: undefined gate | 29 (declared) | 2916 |
| Wrong facet [3,-8] with A | REJECT: not true gate view | 29 (declared) | 2916 |
| Underpaid facet certificate | REJECT: paid cost | 28 (declared) | 2916 |
| Forward parent on facet | REJECT: bad parents 0 | 29 (declared) | 2917 |

The four positive packets are actual accepted-byte original-checker refutations, not abstract-only witnesses. The two legal new facet packets are longer by 50 UTF-8 bytes despite unchanged W29. All ten generated case packets, their SHA-256, OS verdicts, native assertions and rejection messages are regenerated by the executable.

**Immutable publication:**
- Executable original-OS differential replayer: experiments/arc/lspv2_573_native386_owner_facet_cegar.cjs (original publication Git blob 567edb94b345c4b43ec84b3e6dd5c69670d51ebc).
- OS compact raw manifest: results/raw/arc/2026-11-12_0412_LSPV2_573_OWNER_FACET_DISCRIMINATION_OS_COMPACT.json (corrected forward-parent hash, current blob 9668a245f009a132f02ed3ee9a8fe0c7bb69325b).
- The replayer creates 10 individual exact JSON packets in results/raw/arc/573_cases/ and a full raw machine JSON. The individual generated packet files are regenerable, not silently claimed to be already committed. The original-OS result was first reproduced using a functionally equivalent local script; exact committed-version execution should be independently rerun before treating it as independently certified.

## CEGAR step and handoff

At stage A0, the coarse alpha collapses A and B. It must conservatively retain both potential free facet transitions. In the two-state/two-facet matrix, two transitions are genuinely legal, while the two crossed combinations are spurious. Native concrete replay rejects exactly the crossed pairs. A1 refines by retaining the signed owner facet set; all four pair outcomes become exact without losing either genuine shortcut. A1 is **only exact for this two-owner test matrix**, not a complete alpha/gamma for the full historical calculus.

**LSPV-1 (historical Route B):** Preserve all-input quantifiers and free choice of a shorter W29 proof. No B3 uniform-algorithm transfer.
**LSPV-2 (historical Route A):** Carry signed owner definitions and their facet provenance through concrete-to-abstract replay; never quotient them into owner ID/output alone.
**LSPV-3 (historical Route B):** Continue acquiring a single authoritative historical RES-to-AND3 and DEF-to-LOCAL-CONVERT dispatcher; this /386 witness cannot supply it.
**LSPV-4 (historical Route A):** Charge distinct paid owners once; count logical work, certificate bits, construction, verification time, span and peak space separately.
**LSPV-5 (historical Route B):** Red-team alternate owner definitions, ghost facets, scope-bearing contexts and free-view reuses; preserve both native accepts.

### Corpus and scientific scope

Read both root trackers: proof1.txt blob 06f7ebc8c2283304a0f5200b518c6e48fa41e343; proof2.txt blob 1bf4929f872506fcbc357810bd72d016694618b2. Reviewed issue #3 (1,744 comments at preflight), AGENTS.md, CODEX.md, pnp-research skill, LSPV-2/539, /547, /549, /570-572, LSPV-1/566, LSPV-3/586, and recent coordination handoffs. Other reports 540-546, 548 were located through repository search and their scopes checked through indexed excerpts. Complete root main.tex retrieval is subject to a documented oversized-contents API failure; an ownership-only update is permissible only after a successful full Git blob recovery and conflict-safe readback. The local source tree available to the OS replayer was assembled from an existing audited evidence archive, not a full repository clone, so the repository-wide preflight script was not run. No historical proof-system semantics or proof-chain status was strengthened.

Primary references: Cook and Reckhow, *The Relative Efficiency of Propositional Proof Systems*, J. Symbolic Logic 44 (1979), DOI 10.2307/2273702; Cousot and Cousot, *Abstract Interpretation*, POPL 1977, DOI 10.1145/512950.512973; Clarke et al., *Counterexample-Guided Abstraction Refinement*, CAV 2000, DOI 10.1007/10722167_15; separate FRAT-XOR/XLRUP checker and grammar https://github.com/meelgroup/frat-xor/blob/main/format.md. These provide methodology and deliberately different external grammars, not authenticity of R_mix341.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** P2-D1, full P2-C3, P2-B1 and the separate B2/B3 bridge remain OPEN. No changes to the five research roles, schedules, ownership boundaries, historical weights or the two Route A / three Route B allocation. **P versus NP remains OPEN.**
