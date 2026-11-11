# LSPV-1/564: A paid DEF-facet ancestry bridge admits a strictly cheaper native archived proof

**2026-11-10 22:00 PST (America/Los_Angeles) | LSPV-1 General SAT Lower-Bound Lead | historical Route B | PROVED/RESTRICTED + COMPUTATIONAL. P versus NP OPEN.**

## Target and four pre-search falsifiers

**Candidate [P2-D1 -> P2-C3]:** The original archived /386 SOURCE/DEF/RES checker accepts both LSPV-3/561's 50-paid gate-bearing K4 proof and a strictly cheaper 47-paid proof of the **same signed original source**. The proof transformation erases a paid definition and two paid RES inferences whose joint output is already a source clause. This falsifies any inference from "the owner and its defining facets are in terminal ancestry" to "that owner is necessary for minimum work."

F1: The two defining-facet Resolution steps fail to reproduce the identical signed source. F2: The gate variable or removed bridge outputs have another live consumer. F3: The unchanged original /386 checker rejects the replacement, or the original source changes. F4: Some original source node disappears from terminal ancestry or some shared paid node is charged twice. The proof and executable tests rule out F1-F4 for this archived packet only.

## Source recovery, duplication check and literature

Read both complete current root trackers (proof1.txt SHA 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b, proof2.txt SHA 8f738a1c11f6ab94631a909dd5649e5ea4866553), issue #3 through LSPV-4/534, AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md, root main.tex blob 7a868d5f20cffc3707e37a5796f04e35f8970dff by Git Blob after contents retrieval returned empty, LSPV-1/539/558/563, LSPV-2/539/547/548, LSPV-3/541/549/559/560/561, LSPV-4/533/534, LSPV-5/479/481 and the recent five-role LSPV-1/563 handoff. Searched prior code and reports for /386 gate elimination and compared LSPV-2/386, LSPV-3/561 and earlier oriented-facet work. The archived checker and the owner/facet witness are **not new**. The new comparison is the explicit 50-to-47 accepted proof on precisely LSPV-3/561's input.

Primary sources consulted: Cook and Reckhow, *Relative Efficiency of Propositional Proof Systems*, JSL 44 (1979), DOI 10.2307/2273702; Cousot and Cousot, *Abstract Interpretation*, POPL (1977), DOI 10.1145/512950.512973; Clarke, Grumberg, Jha, Lu and Veith, *CEGAR*, JACM 50 (2003), DOI 10.1145/876638.876643; Urquhart, *Hard Examples for Resolution*, JACM 34 (1987), DOI 10.1145/7531.8928. They do not authenticate a particular /341 byte grammar.

**Pinned originals:** Archived /386 checker file experiments/arc/lspv2_386_independent_verify.js, Git blob 338305c0ce101704205e57543756b8127074a986; LSPV-3/561 exact 4,144-byte packet results/raw/arc/2026-11-10_2124_LSPV3_561_ARCHIVED_386_NATIVE_PACKET.json, blob d0fa96a155672f8f6a6a3428eacafa15e79b9e88. The distinct recovered /341 fixture checker, blob fcb7d4ced8f922de14c0bda16263a8cc7853e8e0, has only AND3/XOR dispatch and cannot accept this /386 envelope. No /341 rule was authenticated here.

## Theorem 564.1: charged identity-bridge retraction (PROVED/RESTRICTED)

In a source-authenticated acyclic, strict complementary-pivot Resolution calculus with an owner-paid-once conservative AND2 gate and zero-extra-cost defining facets, let an original source clause be
$$
C=(\neg a\lor\neg b\lor U).
$$
Introduce fresh z representing a AND b, with defining facets
$$
D_1=(\neg z\lor a),\qquad D_3=(z\lor\neg a\lor\neg b).
$$
The following two paid Resolution inferences return exactly C:
$$
R_1=\operatorname{Res}_a(D_1,C)=(\neg z\lor\neg b\lor U),
\qquad R_2=\operatorname{Res}_z(D_3,R_1)=C.
$$
Assume the gate owner, z, its facets and R1 have no surviving consumers outside this gadget, and all downstream consumers of R2 may legally reference the already-present original SOURCE C. Assume no other mandatory administration prevents deleting the unused owner. Then deleting the gate, its free facets and the two RES records and redirecting every surviving R2 reference to C produces an acyclic valid shared-DAG refutation with **exactly three fewer distinct paid nodes**. Any surviving shared paid inference is still charged once, not per reference.

**Proof.** Each displayed Resolution is exact, with complementary pivot signs and no tautological extra literal under the given freshness hypotheses. The second output is identical to original C. Replace references to R2 with C, and remove all now-unreferenced gate/facet/bridge records. No remaining record mentions z or a removed identity, and all later original signed clauses and inferences are unchanged. Chronological renumbering preserves topological order and each surviving paid identity; one owner and two paid RES creations disappear. Final contradiction and original source ancestry are preserved whenever every source was ancestral before. QED.

**Limit:** arbitrary extension gates need not be eliminable; no claim about general Extended Resolution strength or worst-case proof size is made.

## Exact original-checker experiment and CEGAR control

Input is odd K4 on six edge variables, guard t=x7, one AND gate z=x8 defined by x1 and x2. All 17 original signed SOURCE clauses are retained. Input SOURCE record 1 is C=(-x1 OR -x2 OR x3 OR -t). DEF records 17,18,19 are the three views, RES 20,21 are the two-step bridge returning C, and a downstream RES at original index 23 consumes the duplicated record 21. Delete records 17..21, delete the paid gate declaration [0,8,1,2], replace each reference to old 21 by old source 1 and monotonically renumber all survivors.

In hosted V8, the **unchanged original archived checker mathematical code** accepted both exact packets with only Node file/CLI boundary adapted. Original: 69 records, 17 sources, 3 DEF views, 49 RES, one paid gate, **50 paid**, 725 original-checker assertion groups, all 17 sources in the terminal ancestry, one dead facet. Rewritten: 64 records, 17 sources, no DEF views, 47 RES, zero paid gates, **47 paid**, 674 original-checker assertion groups, all 17 original sources and all 47 paid nodes in terminal ancestry, no dead records. Both independently yield 0 odd models, 8 even-charge models and 64 models when guard is false.

The altered 47-paid packets were each rejected under the unchanged checker code: (1) wrong paid summary, (2) unmapped parent, (3) wrong complementary pivot, (4) bad signed SOURCE, (5) bad RES output. Hence these are exact native /386 checker verdicts, not merely a schematic two-line proof.

Published reproducer: experiments/arc/lspv1_564_gate_bridge_elimination.cjs, Git blob 7ed2a8a858bd28c5127588d4bd459739060a9073. Exact **3,868 UTF-8 byte** replacement packet: results/raw/arc/2026-11-10_2200_LSPV1_564_GATE_BRIDGE_ELIMINATED_PACKET.json, blob f1f43709b49e3c9bf459db362718307a15880a98. Raw five-negative-control V8 evidence: results/raw/arc/2026-11-10_2200_LSPV1_564_GATE_BRIDGE_RETRACTION_RAW.json, blob d63da1d740d7c56c50c16b2fca65f598b282f795.

The standalone Node reproducer passed hosted V8 syntax parsing, but standalone OS Node execution was **not performed in this run**. The runner is designed to execute both positive packets and all five new negative controls in the unmodified archived Node verifier, which itself includes eleven corruption controls per accepted packet. Real-time resource charges, discovery/search time, evidence bits, critical span and peak space are separate from the 50-to-47 logical-work reduction.

## Dependency ledger and honest status

[P2-D1] **OPEN:** /386's SOURCE/DEF/RES grammar cannot be substituted for unavailable native full five-rule /341 acceptance (Resolution, AND3, GF(2), LOCAL-CONVERT, paid DEF ownership/facets, exported/private/fresh wires, branching, contexts, weakening, discharge, joins, deletions).

[P2-C3] **OPEN:** this is a cost-decreasing local normal-form construction only within a separately authenticated archived calculus. It does not establish alpha/gamma or concrete-step inclusion for every legal /341 native transition. The CEGAR lesson is that even an *actual* gate and both useful facets in ancestry may be removed by a cheaper genuine proof.

[P2-B1] **OPEN:** for this particular /386 K4 source, the accepted 47-paid witness **falsifies any hypothetical minimum-cost lower bound >=48** in the /386 calculus, but is no asymptotic lower bound. [P2-B2/B3] **OPEN:** no noncircular same-/341 computational transfer follows. P versus NP remains OPEN.

**TRACKERS REVIEWED; NO MATERIAL CHANGE:** no load-bearing proof-chain status changes, and no reclassification of LSPV-3/561's valid accepted 50-paid witness is needed. Keep the two root trackers unchanged. Preserve all five scheduled roles and original two Route A / three Route B allocation. Do not modify any other role's main.tex region. Blockers: full native /341 five-rule parser/accepted-byte corpus; independent OS Node full reproducer execution and LSPV-5 red-team review.
