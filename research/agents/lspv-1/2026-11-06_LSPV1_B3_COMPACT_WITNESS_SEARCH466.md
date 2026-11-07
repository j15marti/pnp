# LSPV-1/466 | B3 compact-witness and conditional proof search

**2026-11-06 PST | Route B lead | PROVED/RESTRICTED conditional meta-lemma; COMPUTATIONAL finite control | P versus NP OPEN.**

Trackers actually read: `proof1.txt` blob `006eeeb51fa0440abcdd55ddf86e8059933f8c70`, `proof2.txt` blob `2bf4ec1601450cf4ed3d107b3ab3bc392548be12`. Exact IDs: [P1-01], [P1-03], [P1-X3], [P2-D1], [P2-D2], [P2-D3], [P2-B1], [P2-B2], [P2-B3], [P2-B9], [P2-L3-465], [P2-L5-402]. New scoped bridge [P2-B10]. No load-bearing gap closed.

## IDEA -> SEARCH -> ITERATE

Hypothesis: Assuming SAT in P, a same-calculus polynomial bound on EXPLICIT refutation bits and polynomial-time native checking makes proof search polynomial by NP witness self-reduction. It does not make historical B3 true.

Precise falsifiers: (1) the native verifier may be superpolynomial in evidence bits; (2) paid-node bound does not imply bit-length bound (large IDs/rows/unpaid annotations); (3) a per-instance polynomial is not a uniform bound; (4) candidate prefix witness may import a foreign source or an illicit branch lemma. The first three remain independent prerequisites rather than silently assumed claims. Finite original-source Resolution checks address (4).

Sources inspected: governing five-role Nov 2 handoff, issue #3 and current LSPV-3/465 and LSPV-5/402 comments, project AGENTS.md/CODEX.md/.codex skill, LSPV-1/465, LSPV-3/464-465, LSPV-5/402; GROKPROOF/2026-11-06_2316_PROGRESS.md, Claude 2026-10-28 world ledger. New requested GitHub repositories were inspected at `konard/p-vs-np` README SHA 0e0ec77f83ad6eec1719a96066108b96ac1c2a95 and proof-status SHA 93b77ed3d8fe456f81c690035f45f07910a247f2, and `blkph0x/p-vs-np-proof-research` README SHA f397a7747eaca82df3d754d0a4b4bab1fe10f814 and METHOD_INDEX SHA 18d693ea71dfa433370eb7afbebc3106e32f03e5. Relevant tool scope: peitl/short-proof README SHA 93d2090dba9739bc4983c65ea639a24e1f5e0fab, cake_lpr README SHA e94f45e9aa000cd9ada12f4c771ac9daf28fe53c, frat-xor format SHA 986a21aa92b62f844ef1fce852193142c41b2b1f, openai/math README SHA cc5b0a03bca6c742f045d683b6647a6f44ef2cae. Primary source: Cook & Reckhow, JSL 44 (1979), 36-50, DOI 10.2307/2273702; existence of SOME polynomially bounded proof system iff NP=coNP does not settle a preselected historical R. Used public web/GitHub searches, not a Google-specific interface.

## Theorem 466.1 (CONDITIONAL, source/authentication specific)

Fix a sound complete proof calculus R for encoded CNF UNSAT with fixed weighted distinct-node work W_R(F) and a deterministic polynomial-time verifier of fully explicit certificate bits. Assume **compact witnesses CW**: ONE polynomial q applies to ALL UNSAT F and ALL K>=W_R(F), guaranteeing a legal source-authenticated proof pi with cost <=K and |pi|<=q(|F|+K). This is unproved for historical R_mix341.

Under SAT in P and CW, the following are equivalent:

(A) B3: there exist C,k such that ALL UNSAT F of encoding length N have W_R(F)<=C(N+1)^k.

(B) There is ONE uniform deterministic polynomial-time algorithm which outputs a legal checked R refutation on UNSAT F and correctly labels SAT and malformed sources.

The reverse direction assumes as usual that weighted cost is polynomially bounded by explicit evidence bits, true for a finite fixed rule vocabulary with bounded constant per-node weights.

**Proof:** With (A), set m(N)=q(N+C(N+1)^k). For any prefix u, the predicate that some extension v with |uv|<=m makes V_R(F,uv)=1 is in NP: guess v and check source/authentication in polynomial time in N+m. SAT in P implies P=NP, so this ONE prefix predicate has a uniform polynomial decider. From the empty prefix, perform at most m binary prefix queries plus one final verification to recover a legal proof, using a self-delimiting encoding or a padding-aware verifier; separately decide SAT and malformed inputs. Time and output bits are polynomial in N. Conversely, a P-time proof generator emits polynomially many certificate bits, and fixed-weight paid nodes are bounded by those bits, so W_R is polynomial. QED.

**Noncircular limit:** The theorem absolutely does NOT derive CW, polynomial verifier complexity or B3 for historical R_mix341. It locates a separate bit/grammar obligation. B3's ideal minimum excludes discovery cost, as instructed; actual upper-bound construction charges prefix decisions, checker calls, input reads and output.

## Sufficient compactness syntax, conditional and not authenticated

If each paid step introduces <=b fresh names, each node contains only constantly many canonical clause/Boolean GF(2) rows, every such row lists <=N+bK distinct names, references and IDs are explicitly introduced before use, and native inference is invariant under bijective fresh-name renaming fixing original source IDs, then a K-node proof can be densely renumbered with <=N+bK names. Resulting evidence bits are O(N+K(N+K)log(N+K)), at unchanged logical node count. This requires an explicit historical grammar audit. Numeric-ID-sensitive facets, huge uncharged annotations, hidden multirow payloads or free introductions could invalidate it.

## Executed finite validation control

Published PHP family, tiny PHP(2 pigeons, 1 hole) UNSAT CNF: (x1), (x2), (~x1 v ~x2). The SAT control removes the collision clause. This is NOT strict 3-CNF or an asymptotically certified hard instance and is included solely as a finite certificate-prefix test. Exhaustive original assignments: four. Exhaustively enumerated 1024 ten-bit records for exactly two native ordinary Resolution steps: eight valid, 1016 rejected. Eleven bounded prefix-existence queries (implemented via exhaustive, NON-polynomial enumeration) recover proof record 205, deriving (~x1) then false. Separate Python/JS implementations passed 3087/1040 checks; SAT, malformed and corrupt records were rejected. This is NOT unconditional polynomial SAT search or evidence that B3 holds.

**Resources:** finite work = 2 Resolution nodes, certificate = 10 bits, 11 prefix queries; finite exhaustive-emulation search scans up to 1024 candidate records per query. Executed host time and RSS are in raw JSON; not FLMV machine bounds. No authoritative historical R_mix341 checker ran. Root main.tex returned empty content at blob 68188a24badda635a5983fda1c381cdb694fd497, so was NOT edited.

## Status and next implication

PROVED/RESTRICTED conditional equivalence [P2-B10], COMPUTATIONAL finite proof-prefix test; [P2-D1], [P2-B1], [P2-B2], [P2-C3] remain OPEN. LSPV-3 should authenticate historic accepted-byte checker polynomiality, dense renaming, scope and row sizes. LSPV-5 should falsify the CW assumptions with legal huge-ID, GF(2), and LOCAL-CONVERT cases. LSPV-2/4 remain Route A only. Neither a superpolynomial full-mixed minimum nor noncircular B3 was established. P versus NP OPEN.
