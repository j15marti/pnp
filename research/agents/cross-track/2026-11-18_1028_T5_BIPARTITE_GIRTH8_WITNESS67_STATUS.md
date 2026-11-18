# CROSS-TRACK SYNTHESIS 67 | T5 BIPARTITE GIRTH-EIGHT WITNESS FIREWALL
**Time:** 2026-11-18 10:28 PST (America/Los_Angeles).
**Research classification:** exact finite-certificate theorem + elementary symbolic composition; conditional decision-to-search transition; no unrestricted complexity lower bound. **P versus NP OPEN.**

## Pre-search candidate order and evidence
Proposals were frozen **before** retrieving contemporary project data in local artifact `00_PRESEARCH_PROPOSALS.md`, SHA-256 `96c07a987cbd51634a0fdf6527696f146894350e6c773962eb4c3133e5f59131`. Four ideas: (1) girth/promise-preserving relative-color self-reduction, (2) counting vs decision counterexamples with charged source contraction, (3) proof-transport firewall, (4) same-final-input UWI and necessary nonrelativizing WRAPPER criterion.

**Newest substantive sources read (freshest available to this run):**
* Resource Contraction: **TMR-1/094 (10:03 PST)**, `research/agents/tmr-1/2026-11-18_1003_TMR1_T5_FULL_POLYMORPHISM_CLONE094.md`, branch `tmr1-20261115-independent-lean060`: every r-ary T5 polymorphism is a shifted coordinate projection, 5r total; NP-hardness corroborated, no algorithmic lower bound. **TMR-3/088 (09:27 PST)**, `research/agents/tmr-3/2026-11-18_0927_TMR3_T5_SIGNATURE_QUOTIENT088.md`, branch `research/tmr3-t5-signature-quotient088-20261118`: source-authenticated polynomial exact counting for all orientations of complete bipartite graphs using ≤45 support orbits; full-source checks and same-machine polynomial bounds; draft PR #290.
* Nonrelativizing Simulation: **LSPV-5 CRTOVERWRITE1 (09:06 PST)**, `research/main/2026-11-18_0906_MAIN_LSPV5_CRTOVERWRITE1_CONDENSED.tex` on main: restricted CRT last-writer certificate for a typed tape controller; hidden-read counterexample; general nonrelativizing endpoint certification and indispensable WRAPPER still open.
* Universal Obstruction: **TMR-2/088 (09:12 PST)**, `research/agents/tmr-2/2026-11-18_0912_TMR2_T5_GIRTH8_EQUALITY088.md` on main: fixed 65-vertex, 87-arc, girth-8 edge gadget with exact cofactor `142884 R` by critical-source complement equality.
* Proof Transport: **TMR-4/091 (09:36 PST)**, `research/agents/tmr-4/2026-11-18_TMR4_T5_CHAIN_HALFGRAPH091.md`, branch `tmr4-20261118-0936-chain-halfgraph091`: full source-derived 11-state five-way OBDD for forward-oriented chain graphs despite unbounded minimum frontier and high adjacency rank; not arbitrary-decider proof transport.

Cross-checked newest project issue #3 handoffs, newest commits, prior project chats, Files/Library search and Google Drive search. Drive results were older structural reports (mainly Sep/Oct), so no newer girth-eight theorem was inferred from them. Primary literature: Bang-Jensen, Hell, MacGillivray (1988) DOI 10.1137/0401029; Kun (2013) DOI 10.1007/s00493-013-2405-4; Baker, Gill, Solovay (1975) DOI 10.1137/0204037.

## New integrated theorem 67.1: **BIPARTITE** girth-eight exact compiler
Let `R(a,b)` mean `(b-a) mod 5` belongs to `{1,3}`. The TMR-2/088 fixed critical graph H has 33 vertices, 44 arcs, undirected girth 8, and is **bipartite** with 17/16 sides. Its critical edge is `0 -> 17`; deleting it gives P whose two terminals lie in opposite bipartition sides and are at undirected distance 7. Original-label exact pinned count is
`B_P(d)=(378,0,756,0,378)`.
Reverse every arc of a second copy of P, glue both copies only at terminals, and append an arc from terminal 17 to a new leaf. This gives a graph F with 65 vertices, 87 directed arcs, undirected girth exactly eight, terminal distance eight, and terminal cofactor
`K_F(a,b)=142884 R(a,b)`.
**NEW OBSERVATION:** F is itself bipartite, with 34/31 sides, and its *exposed terminals both belong to the same bipartition side* (the appended leaf is opposite to terminal 17, hence on the same side as terminal 0). This property was not asserted in the prior /088 handoff.

For a simple oriented source G with n vertices and m arcs, replace every arc by a private copy of F, identifying its exposed terminals with the source endpoints. In a canonical encoding, sort undirected edges, map the lower endpoint to terminal 0 and the higher to terminal 64, and reverse *all gadget arcs* when the original edge points in the reverse direction. Since reversed gadget transfer is `142884 R(b,a)`, this preserves original constraints and exactly the same labeled underlying undirected skeleton under edge reversals.

**Theorem:** The compiler `C_8(G)` has exactly `n+63m` vertices, `87m` arcs; if m>0 it has undirected girth exactly eight; **it is always bipartite regardless of whether G is bipartite**, because all original vertices can lie in one global bipartition class and every gadget places both exposed terminals in that class. Furthermore,
`Z(C_8(G))=142884^m Z(G)`
and `SAT(C_8(G)) iff SAT(G)`. For m=0 the output has no cycles and is trivially bipartite and SAT. Loops/antiparallel arcs in arbitrary input are rejected as immediate NO before compilation, duplicates deduplicated; a fixed compiled NO instance can be used if a total many-one reduction is required. Acyclicity, 5-regularity, high minimum degree and general source complexity are **not** preserved.

This is an explicit linear-size, count-preserving reduction from unrestricted T5 to **bipartite, undirected-girth-at-least-eight oriented T5**, strengthening the girth-eight statement in /088. The latter is NP-complete by the known fixed-T5 NP-completeness theorem; neither large girth nor bipartiteness by itself gives an unrestricted time lower bound. Kun's earlier large-girth CSP reductions establish related general complexity equivalence, and this is a concrete specialized compiler.

## New integrated theorem 67.2: promise DECISION implies original-input WITNESS
Assume a uniform deterministic polynomial-time decider `D_8` for bipartite girth-at-least-eight T5 instances, including arbitrary orientations. For an arbitrary original simple oriented G with n vertices, m arcs and c weak components, choose a root in each component and normalize each root color to 0 using the Z5 rotations. For every other vertex, adaptively test relative differences 0,1,2,3 via exact ordinary-T5 gadgets: difference 1 is
`R(r,v) & R(r,w) & R(w,v)`; difference 3 is `R(r,v) & R(r,w) & R(v,w)`; reversing terminals yields 4 or 2, and difference 0 identifies source vertices. Use D_8 only after compiling each augmented query via `C_8`. If all four tests fail, difference 4 is forced. Retain satisfiable prefixes, output colors of the **identical original G**, then explicitly verify all its arcs. Each augmented graph before compilation has at most `n+(n-c)` vertices and `m+3(n-c)` arcs. Each compiled query has at most
`n+63m+190(n-c)` vertices and `87m+261(n-c)` arcs.
The number of decision calls is at most `1+4(n-c)`.

This gives
`BIPARTITE-GIRTH8-T5-DECISION in P => UNRESTRICTED-T5-WITNESS in FP`,
with all source reading, actual graph generation, addressing, materialization, malformed-source guards, each repeated D_8 call, bookkeeping, recursion/stack, workspace, and witness verification charged on one uniform sequential implementation. The claim is **conditional** and relativizes. In particular it is not a nonrelativizing WRAPPER hinge or a computational lower bound.

## Independent hostile finite audit
A separately written standard-library Python verifier did not import TMR-2's code. It checks the authenticated original 33/44 source SHA-256
`0d82de7d49547e71bc2959c6c1760633fd4dfd935ef33769ad9ddb38916efbac`,
and independently performs exact factor/bucket elimination on original T5 labels (no precomputed B/K arrays used to obtain cofactor results). It reproduced:
* P source girth eight, terminal distance seven, width upper six, exact B `(378,0,756,0,378)`, 703,325 factor-value visits over five terminal pins.
* Edge gadget 65 vertices, 87 arcs, undirected girth eight, terminal distance eight, 34/31 bipartition, exact K `(0,142884,0,142884,0)`, width upper six, 1,545,925 factor-value visits over five pins.
* Opposite orientations of the five-edge four-variable test source have source solution counts 0 and 5, identical undirected compiled skeleton and compiled counts 0 and `297774841883278683354117120`.
* Five independent explicitly materialized nontrivial compiled graphs (up to 384 vertices and 522 arcs) have **bipartite** undirected-girth-eight skeletons, even when source graph contains an odd cycle. All 25 terminal pairs satisfy the cofactor, and all 4 relative-pin gadget truth tables pass.
* Constant 63-vertex and 87-arc expansion, and the reported sequential-query size inequalities hold exactly. No failed assertions.

Local reproducibility paths: `/mnt/data/pnp_cross_track/run67/audit_girth8_selfreduction67.py`, `AUDIT_RESULTS.json`, `00_PRESEARCH_PROPOSALS.md`.
SHA256 audit script `ae9e9c123ea3196f54e27249dc5676e678cc820f8f0e26c9e6fb0cb54c251290`; raw result `e28b87c929e20f01f9be125dcdc1924e0c4a3033220c701a62a2f679f3003e60`.

## Explicit proof DAG
| Arrow | Status | Scope |
|---|---|---|
| Fixed T5 CSP NP-complete | ESTABLISHED, published | Bang-Jensen et al. |
| TMR-2/088 exact critical-source cofactor B and edge cofactor K | Independent finite-exact verification completed | Fixed gadget |
| **Unrestricted T5 -> bipartite girth>=8 T5 with exact count factor** | **PROVED symbolically conditional on verified fixed-gadget certificate** | Linear-size, fully explicit |
| **Polynomial bipartite girth>=8 T5 decision -> polynomial original T5 witness** | **PROVED conditional implication** | Correct common-input reduction and cost ledger |
| Self-reduction excludes all polynomial witness algorithms on one original G | OPEN; previous no-query versions insufficient | Include all legal derived queries |
| Girth-eight compiler preserves 5-regular degree promise | FALSE for this gadget (degrees 1,2,3,4; source terminals degree-dependent) | No five-regular result |
| High frontier/row diversity/rank => costly arbitrary computation | FALSIFIED as inference | TMR-3/088, TMR-4/091 provide easy controls |
| WRAPPER supplies necessary nonrelativizing step | OPEN | Ordinary self-reduction uses none |
| Specific Resolution proof-system lower bound transports to arbitrary T5 deciders | OPEN | No actual arbitrary-decider-to-Resolution theorem |
| Superpolynomial unrestricted T5 decision lower bound | OPEN | Every alternative source-aware solver remains admissible |
| P versus NP | **OPEN** | No load-bearing separation arrow |

## Next specialist assignments
1. **Resource Contraction (TMR-1/TMR-3):** Independently check bipartite-preservation and extension cofactor; implement a source-authenticated compiler recognition/contraction for the explicit 63-private-vertex grammar. Charge generator, full canonical source scan, numeric coefficient, intermediate workspace, recursion and witness lifting. Test easy source quotients before hardness claims.
2. **Nonrelativizing Simulation (LSPV-5):** Treat `D_8` as a hypothetical oracle and run the exact same-input witness algorithm with fully paid derived queries; show that any proposed WRAPPER hinge is genuinely outside relativizing self-reducibility. CRTOVERWRITE1's hidden-read falsifier remains an upper-bound limitation, not a lower-bound proof.
3. **Universal Obstruction (TMR-2):** Seek mixed SAT/UNSAT sources **not cheaply recognizable as fixed-gadget compilations** and retain the stronger five-regular girth-eight requirement separately. Quantify over every eligible uniform polynomial witness finder on one final G with one common clock, including `Witness^{D_8}`.
4. **Proof Transport (TMR-4):** Produce a checked encoding-specific proof map for the 65-variable edge substitution, with explicit clause/width/length costs and source-aware recognition, or a concrete falsifier. Do not infer arbitrary-decider lower bounds from OBDD or Resolution lower bounds.

## Scientific scope
The high-value single arrow closed here is **promise-preserving self-reducibility for bipartite girth eight**, not P!=NP. The 65-vertex fixed gadget is relatively large but uniform and constant size. Counting preservation and bipartiteness do not imply intrinsic algorithmic difficulty; a canonical source compiler can be recognized and reversed, and alternate polynomial shortcuts must be allowed. Independent external proof review, physical microstep implementation and proof-kernel formalization are still open. No peer agent schedules, root proof trackers or other research files were changed.
