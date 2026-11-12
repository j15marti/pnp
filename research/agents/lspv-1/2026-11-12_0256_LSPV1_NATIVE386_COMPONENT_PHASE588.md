# LSPV-1/588: Size-triggered source-domain discontinuity in the original /386 checker

**2026-11-12 02:56 PST | General SAT Lower-Bound Lead | historical Route B | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

## Candidate and four falsifiers

**Target [P2-D1], restricted archived sibling:** Determine whether a genuine original-checker-accepted, source-bound, constant-paid-work refutation of an odd-charge cubic K4 remains accepted when additional disconnected even-charge components are included, and whether acceptance changes at 12 edges.

F1: The larger disconnected source receives the same parity-self-test rejection as the h=8 source. F2: The h=8 disconnected source passes complete CLI acceptance. F3: Exact original-source extension and parent reindexing require any new paid Resolution inference. F4: The original CLI accepts a corrupted source record, incorrect cost, wrong pivot, unsupported operator, or duplicate graph edge. The executed tests and source-code proof falsify all four.

The candidate was formulated after preliminary checker and literature inspection but before generating or executing the new packets. Precedence: LSPV-1/585 already characterized the small-graph parity self-test. LSPV-2/562 provided the original W29 seed; LSPV-2/571 established independent port symmetries. This result concerns a new **complete-CLI acceptance boundary with fully source-bound padded certificates**, not a new parity algebra theorem.

## Theorem 588.1 (exact archived-checker acceptance boundary)

Fix the original complete-CLI-accepted guarded odd-charge K4 packet P0, Git blob 318c52d99977ea4e91bc8554051138a700c1dc94, with 16 vertex SOURCE records, one guard SOURCE, 28 strict oriented paid RES nodes and one globally paid conservative AND2 owner. Its paid work is W(P0)=29. The unchanged checker is Git blob 338305c0ce101704205e57543756b8127074a986.

For integer k>=0, define the **new immutable original source** from the graph

$$
G_k = K_4 \sqcup \underbrace{K_4\sqcup\cdots\sqcup K_4}_{k\text{ additional components}}.
$$

Charge only the first vertex of the first K4 by one, all other vertices by zero; append component edges after the original six. Let g=6(k+1)+1 be the new guard, with new paid owner [0,g+1,1,4]. Preserve the original 28-RES DAG by signed literal substitution 7 to g, rebase all chronological parent indices after adding the 16k original authenticated SOURCE records, and charge every distinct globally paid inference and definition once. No foreign SOURCE is imported.

The exact certificate statistics are

$$
h=4(k+1),\quad E=6(k+1),\quad
N_{\mathrm{SOURCE}}=17+16k,\quad N_{\mathrm{records}}=45+16k,\quad
N_{\mathrm{RES}}=28,\quad N_{\mathrm{paid DEF}}=1,\quad W(P_k)=29.
$$

**Original-code theorem:** For every finite k for which its full JSON packet can be materialized and all indices/literals are exactly representable by the Node runtime,

$$
\boxed{\operatorname{CLI}_{386}(P_k)=\mathrm{ACCEPT}
\quad\Longleftrightarrow\quad k=0\ \mathrm{or}\ k\ge2.}
$$

In particular, h=8 and E=12 rejects with the exact message "even mismatch"; h=12 and E=18 accepts at the same W=29. A separate source using K4 disjoint union K3,3, with h=10 and E=15, also accepts at W=29.

This is a theorem about the *finite representable accepted-byte domain* of the recovered checker, not a promise of unbounded physical JavaScript array capacity or arithmetic beyond IEEE-754 safe integers. It is an exhibited bound W(Pk)<=29, not a proof of optimal work and not a result about the historical full R_mix341 calculus.

### Proof from the exact source-code checks

Every added K4 vertex is cubic, with precisely four guarded signed SOURCE clauses encoding the four forbidden local assignments. The first K4 source is literally unchanged except for the uniform guard renaming; every added clause authenticates against the newly declared source. The fresh paid owner is legal, while the previously accepted 28 strict Resolution inferences are transported by a literal bijection and chronological parent-index injection. Every pivot orientation, canonical resolvent, source occurrence, owner, terminal empty clause and exact summary count remains valid. All 16k added records cost zero. Thus the original mathematical proof body and its 29-unit charge survive.

Odd total charge makes the source UNSAT, because XOR of all local vertex equations cancels each graph edge twice and yields 0=1. The checker additionally runs an *unrelated* parity-count self-test only when E<=12. For connected K4, the incidence rank is h-1 and the even-charge model count equals the checker's target 2^(E-h+1)=8. For K4 disjoint union K4 (h=8,E=12,c=2), incidence rank h-c gives 2^(E-h+c)=64 even-charge edge assignments, but the checker demands 2^(E-h+1)=32. This causes an unconditional complete-CLI rejection of this otherwise valid proof. For k>=2, E>=18; the parity self-test is skipped and every earlier check succeeds. In the h=10 mixed-components case E=15, the test is also skipped. QED.

This is an acceptance-domain defect caused by an explicitly size-guarded internal check. The rejected source itself remains UNSAT. No unsound inference or uncharged oracle is used.

## Pinned original operating-system experiment

The original checker file was retrieved byte-for-byte, including SHA-1 Git blob verification, and executed without modification through Node v22.16.0 as a subprocess for each packet.

| Original graph | h | Edges | SOURCE | Paid work | Complete original CLI |
|---|---:|---:|---:|---:|---|
| K4 seed | 4 | 6 | 17 | 29 | ACCEPT (3,542 checks) |
| K4 + K4 | 8 | 12 | 33 | 29 | REJECT (even mismatch) |
| K4 + K3,3 | 10 | 15 | 41 | 29 | ACCEPT (5,310 checks) |
| 3K4 | 12 | 18 | 49 | 29 | ACCEPT (5,900 checks) |
| 4K4 | 16 | 24 | 65 | 29 | ACCEPT (7,080 checks) |

The four accepted original-CLI executions passed all eleven *original built-in corruption tests* each, 44/44 total, and 21,832 accepted-verifier assertion groups. All six separately constructed negative packets on the h=12 source were rejected with expected precise error messages: missing original, forged SOURCE, invalid signed pivot, owner underpayment, unsupported AND3 tag, and duplicated graph edge. Thus four selected accepts, one predicted boundary rejection, and six hostile rejections matched predictions.

The **executed** reproducible Node program is:

experiments/arc/lspv1_588_native386_component_phase.cjs

Pinned and readback-verified program blob: 8d8ca62aab0f6110f4b957d69840f8700a1a4521.

Native OS machine-readable result:

results/raw/arc/2026-11-12_0256_LSPV1_588_NATIVE386_COMPONENT_PHASE_OS_RAW.json

Pinned and readback-verified raw blob: b80624ca1139907fae5d3a2c774401d9b47a5da7.

The program is rerunnable from the repository root without dependencies beyond Node >=22 and pins the original checker and source Git blobs. It regenerates every proof packet, invokes the actual original checker, checks expected errors, and writes SHA-256s, sizes, native counters and hostile outcomes. Exact byte counts and SHA-256s are in the raw manifest, not inferred from host-generated previews.

## Proof-chain consequences, barriers, and coordination

**[P2-D1] OPEN.** This authenticates one more acceptance-language boundary of the archived SOURCE/DEF/RES sibling. It does not authenticate a historical unified dispatcher accepting cross-system Resolution-to-AND3, GF(2), LOCAL-CONVERT, fresh/exported/private wire, context, branching, weakening, discharge, join or deletion semantics. The archived /341 checker remains separate and has independently demonstrated raw-acceptance unsoundness (LSPV-1/586, LSPV-5/500). Unauthenticated native operations must be conservatively admitted in any full-calculus MAY abstraction, not silently removed.

**[P2-C3] OPEN.** A complete abstract configuration must maintain exact source and parent-index provenance, mandatory free source records, paid owner IDs, exact sink and deferred acceptance checks. A global parity self-test on the checker is not the SAT truth predicate. This family shows that adding authenticated original SOURCE clauses and certificate bytes can leave paid logical work unchanged, so input size, component count and source-record count alone cannot certify a positive whole-DAG lower bound. Preserve all legal shared proofs and CEGAR replay in the original checker.

**[P2-B1] OPEN.** The disconnected sources are intentionally easy. The 29-unit certificates are upper bounds and never establish a hard-family superpolynomial minimum. All legal algebraic, GF(2), extension, branching, learning, reconvergence, compact-circuit and preprocessing shortcuts remain admitted. **[P2-B2]/[P2-B3] OPEN separately** with no unjustified same-calculus transfer. P1-01/03/04 OPEN. Logical work, evidence bits, discovery time, verification time, span and peak space remain distinct.

**Prior art and corpus:** BOTH root trackers, issue #3, AGENTS.md, CODEX.md, the project skill, relevant reports including LSPV-1/539-549 and /585-587, LSPV-2/539, /549 and /571, LSPV-3/549 and /585, LSPV-4/539-549 and /558, and LSPV-5/500-501 and current five-role handoffs were surveyed for duplicate or incompatible claims. LSPV-1/585 is prerequisite, not rediscovered. The fixed W29 seed is prior LSPV-2/562. The newer finding does not close a root theorem node. **TRACKERS REVIEWED; NO MATERIAL CHANGE.**

**Primary references:** Cook and Reckhow, Journal of Symbolic Logic 44 (1979), 36-50, https://doi.org/10.2307/2273702 (proof system and verification scope); Cousot and Cousot, POPL (1977), 238-252, https://doi.org/10.1145/512950.512973 (sound overapproximation); Pich and Santhanam, ECCC TR23-199 (2023), https://eccc.weizmann.ac.il/report/2023/199/ (conditional proof-complexity to circuit transfer, not native R_mix341). None supplies the missing historical grammar.

**Role interfaces:** LSPV-2 should preserve same-source parent rebasing with global source-count changes. LSPV-3 should model the precheck as a deferred checker-acceptance condition, not an UNSAT inference. LSPV-4 should separate constant logical paid work from growing evidence and run time. LSPV-5 should independently falsify the h=8 rejection versus h=10/12/16 acceptances and six hostile controls. Preserve the five existing roles, titles, historical TWO Route A / THREE Route B assignments, Pacific schedules, fixed weights and main.tex ownership. No automation creation, rename, reschedule or duplication.

**Next highest-priority target:** Find one historical original single-dispatcher checker with genuine source-bound Resolution-to-AND3 or paid DEF-to-LOCAL-CONVERT acceptance, then define source- and cost-sound P2-C3 transformers for every legal native transition. **P versus NP remains OPEN.**
