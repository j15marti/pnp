# CROSS-TRACK T5-PC-MASK-FIREWALL57 | 2026-11-18 01:25 PST

**Status:** New restricted theorem, independently finite-audited. **P versus NP OPEN.** Full detailed report and executable audit are retained in current-run artifacts; no schedules or specialist settings changed.

## 1. Four mechanisms recorded before searching
Pre-search prescan file: `2026-11-18_0118_prescan_proposals.md`. Proposals were (1) challenge full-PC indiscernibility on high-girth critical T5; (2) same-final-input UWI against a hypothetical T5 decision-to-witness extractor; (3) require syntactic proof-system retraction and full charges; (4) distinguish genuine WRAPPER necessity from indexed source-read and template recognition. These were recorded before current-turn GitHub, Drive, Library and literature searches.

## 2. Current sources read
- **Resource contraction and information necessity:** TMR-2/078 (2026-11-18 00:07 PST), TMR-2/077 (2026-11-17 23:30 PST), TMR-4/062. TMR-2/078 proves an existential high-**undirected**-girth same-skeleton YES/NO pair surviving path consistency and singleton AC, but no explicit large NO graph, cost lower bound, or adaptive cofactor hardness.
- **Nonrelativizing simulation:** CLOCKADAPTIVEPOLY31 (2026-11-18 00:35 PST) and CLOCKMASKEDINVERSE22, plus TRACEAUDIT23. Sparse sections and hard inverse extraction do not establish a T5 WRAPPER necessity.
- **Universal obstruction:** DIAGONALLIST34 note and matching Google Drive handoff; publicly listed witness exclusions admit a same-input witness constructor.
- **Proof transport:** PROOF-TRANSPORT_ALLFIELD_SHIELD_RETRACTION1; exact all-field PC-degree transport is proven only for its stated shield/selector compiler. Prior T5 /50-/51 gadget retractions do not connect arbitrary deciders to refutations.
- **Project chats/files/Drive:** CROSS-TRACK /48-/56, T5 reports, the Google Drive MAIN shared proof state, library local proof-chain snippets. **Primary literature:** Bang-Jensen–Hell–MacGillivray (1988), Kozik (2021, 10.1137/18M117577X), Barto–Kozik bounded width, Ben-Sasson–Wigderson Resolution width, and Nešetřil–Zhu sparse incomparability.

## 3. Theorem 57A: PC-cardinality blindness does not mean equal PC masks
Fix the five-symbol loopless tournament `R(a,b) iff (b-a) mod 5 in {1,3}`. Let S=(V,E) be ANY finite undirected simple graph of girth >=7, with n vertices and m edges. For each edge orientation o, let P^o_uv be the actual fully closed ordinary complete binary (2,3)-path-consistency relation on ordered pair (u,v), including diagonal equality and inverse arcs.

The signed-shortest-path fixed-point lemma from TMR-2/077 yields for finite graph distance d:

`|P^o_uv|=5 min(d(u,v)+1,5)`; for disconnected distinct pairs the size is 25. All entries are nonempty. Thus the ordered n-by-n **cardinality array** C(o) is independent of o. For any random orientation O, `I(O;C(O))=0`. This statement is **only** for cardinalities, not actual masks.

The full 25-bit relation mask on an original source edge {u,v} is precisely R or its converse depending on direction. The two are disjoint ten-entry relations, so the original direction is read directly from that mask. Therefore the complete-PC mask encoding M(o) is injective in orientation and for any o,o' differing in t directed edges:

`Hamming(M(o),M(o')) >= 40t`.

Proof: the ordered pair (u,v) flips 20 membership bits when the edge reverses; (v,u) flips another 20, and edge-pair coordinates from distinct edges are disjoint. Nonedge mask changes add nonnegative differences. The 40t bound is exact when restricted to original edge pair coordinates.

## 4. Corollary 57B: identical local cardinalities, opposite SAT statuses
If S is bipartite, has girth >=7, and `2^m>5^n`, orient all edges left-to-right and label left vertices 0 and right vertices 1 to obtain SAT. Every T5 labeling induces **at most one** compatible orientation because T5 is a loopless tournament; hence at most `5^n` of `2^m` orientations are SAT, guaranteeing an UNSAT orientation on exactly the same S. Both pass full PC and have identical cardinality arrays. **No algorithm supplied only those cardinalities can solve all the orientations**, whereas the actual masks retain each source direction.

For previously audited symplectic W(3,4) incidence skeleton, `n=170`, `m=425`, girth 8, and `170 log2(5)-425=-30.272223869...`. This audit does NOT construct or certify a particular 170-vertex UNSAT orientation, nor assert an efficient source-family generator.

Hostile bypass: given two uniformly polynomial-time constructible authentic YES/NO templates as a *promise*, a complete canonical input comparison decides the two-template promise in time polynomial in source bit length, charging template generation, reading, workspace, and output. If NO templates require nonuniform advice, this is only a P/poly promise shortcut, not a claim of a global polynomial T5 solver.

## 5. Independent computational audit
Executed CPython3 stdlib `t5_mask_firewall57_audit.py`. Exhausted all 128 orientations of C7 and 256 of C8; additionally 64 sampled C9 and 32 sampled C10 orientations, 480 total. Computed complete PC via independent bit-mask composition, checked signed shortest-path kernels on all ordered pairs, verified exact cardinality totals **665, 960, 1305, 1700** (respectively), orientation injectivity of full masks, and independently checked SAT of all tested oriented cycles via exact transfer-matrix counting. Tested 800 randomly selected distinct-orientation pairs for the `>=40t` full-mask bound and equality `40t` on the edge-pair slots.

Small authentic K(2,4) control: exact source-label enumerations gave NO=0, left-to-right YES=90; full canonical source comparison and corrupted-string controls passed. This six-vertex seed has girth 4 and is NOT a high-girth test.

**37,969 assertions, zero failures**, runtime ~1.05 seconds. All finite checks are COMPUTATIONAL, not asymptotic solver lower bounds. Independent external math review pending.

## 6. Proof DAG
| Arrow | Status |
|---|---|
| Fixed T5 homomorphism CSP NP-complete | ESTABLISHED literature |
| Girth>=7 full PC signed-path cardinality invariant | IMPORTED restricted theorem TMR-2/077; independent cycle checks |
| Full PC masks recover every original orientation bit; `>=40t` separation | **PROVED EXACT this run** |
| Full PC cardinality array independent of orientation | **PROVED integrated corollary** |
| Bipartite S with `2^m>5^n` gives same-skeleton SAT/UNSAT but same cardinalities | **PROVED** conditional on skeleton S |
| Cardinality-only decider on such orientations | **FALSIFIED** |
| Full PC masks identical for different orientations | **FALSIFIED** |
| Two-template uniform promise recognizer | PROVED scoped upper bound |
| Full-source unrestricted T5 superpolynomial necessity | OPEN |
| Nonrelativizing WRAPPER indispensability | OPEN |
| Same-final-input all-eligible-program UWI | OPEN |
| All-decider-to-PC/Resolution proof transport | OPEN |
| Universal fully charged contraction / DTISP contradiction | OPEN |
| `P != NP` | **OPEN** |

## 7. Next four specialist assignments
1. **Resource Contraction:** Build one independently certified explicit W(3,4) NO orientation and same-skeleton YES. Compare FULL masks, cofactor tables, OBDD/FBDD, and authentic source-aware shortcuts, charging construction, parsing, space, address operations, recursion, proof verification and output.
2. **Nonrelativizing Simulation:** Test whether any status-changing T5 WRAPPER operation is required after full indexed input access, direct arc inspection and hypothetical polynomial T5 decision. Treat mere hidden orientation as ordinary source information.
3. **Universal Obstruction:** Fix one identical final SAT graph, common clock, exact program class. Include full-source recognition and conditional T5 pinning-based decision-to-witness search as challenger; forbid input-per-program switching.
4. **Proof Transport:** Find an actual explicit large NO T5 graph and establish any Resolution/PC hardness with complete encoding and inference-by-inference transport. Do not promote proof-calculus hardness to arbitrary decision-time hardness without a separate theorem.

**One highest-value remaining arrow:** identify representation-independent obligatory superpolynomial work on ordinary complete-source random-access T5 inputs, not mere PC cardinality collapse. Full masks retain all source orientations, so local-cardinality blindness cannot be used as a general necessity argument.

**Artifacts:** Local detailed report `2026-11-18_0125_T5_PC_MASK_FIREWALL57_REPORT.md`, script `t5_mask_firewall57_audit.py`, JSON `2026-11-18_0118_T5_PC_MASK_FIREWALL57_results.json`, and immutable prescan proposals file.
