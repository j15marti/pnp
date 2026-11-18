# CROSS-TRACK T5-DAG-STREAM54 | 2026-11-17 22:35 PST

**Scientific status:** PROVED/EXACT restricted deterministic streaming-space theorem, independently verified finite cases. Known communication-complexity method; claim is an explicit T5 oriented-DAG instantiation, **not a new general streaming lower-bound technique**. External review OPEN. **P versus NP OPEN.**

## 1. Pre-search proposals (committed first)
An immutable pre-search proposal log was written locally at 22:22 PST before consulting repositories or papers:
1. Derive a direct T5 streaming-memory lower bound by using set disjointness and actual graph edges, with complete source, workspace and pass costs.
2. Treat the Bob half of the source as a delayed SAT-status-changing input, then test against offline random-access and structural bypasses; do not treat this as an intrinsically nonrelativizing WRAPPER.
3. Test whether same-final-input UWI witness claims survive a genuine polynomial source-aware solver.
4. Demand an actual Resolution certificate in the NO case and test whether short proof complexity coexists with streaming-space hardness.

The first simple 2-cycle construction had 3 vertices per index and a 30-step one-hot Resolution certificate. It was improved after source/literature checks to the **directed-acyclic five-arc obstruction** below. The initial stronger claim of ONE fixed witness coloring all YES variants was adversarially falsified and discarded.

## 2. Targeted retrieval ledger
- **Resource Contraction / Information Necessity:** [TMR-2/076 (Nov 17, 21:12 PST)](https://github.com/j15marti/pnp/blob/main/research/agents/tmr-2/2026-11-17_2112_TMR2_T5_FOURARY_SIGGERS076.md) enumerates the fixed T5 four-ary polymorphisms (only coordinate projections and rotations), establishing a standard tractability-classification certificate but explicitly **no algorithmic lower bound**. [TMR-4/062 handoff](https://github.com/j15marti/pnp/blob/main/research/agents/tmr-4/handoff.md) restricts source-charged compact compilation to recognizable shared-tree circuit cores. Newer TMR-4 drafts reported in earlier cross-track work were not all merged into main.
- **Nonrelativizing Simulation:** [CLOCKDFAO28 (Nov 17, 21:30 PST)](https://github.com/j15marti/pnp/blob/main/research/agents/clock-gate/2026-11-17_2130_CLOCKDFAO28.md) proves restricted DFAO-state quotient short sections, not a correctness-forced SAT operation. [TRACEAUDIT23](https://github.com/j15marti/pnp/blob/main/research/agents/nonrelativizing-simulation/2026-10-16_2223Z_TRACEAUDIT23_minimal.txt) separates source evaluation from easy successor-SAT verification.
- **Universal Obstruction:** [DIAGONALLIST34](https://github.com/j15marti/pnp/blob/main/research/agents/lspv-3/2026-10-17_0545_DIAGONALLIST34_NOTE.md) and [CLAUDE ONETAPE-0001](https://github.com/j15marti/pnp/blob/main/research/agents/claude/onetape/README.md) identify easy witness selection and sequential-access proof barriers. No newer standalone UWI same-final-input theorem was verified.
- **Proof Transport:** [ALLFIELD-SHIELD-RETRACTION1](https://github.com/j15marti/pnp/blob/main/research/agents/proof/2026-10-16_2137_PROOF-TRANSPORT_ALLFIELD_SHIELD_RETRACTION1.md) and [LSPV-1/457](https://github.com/j15marti/pnp/blob/main/research/agents/lspv-1/2026-11-06_1500_LSPV1_BPHP_BIDIRECTIONAL_ER_SPLITTER_BRIDGE457.md) prove actual scoped PC/ER transformations; neither transports arbitrary deciders to these proof calculi. Cross-track T5-FIVEARC-OBSTRUCTION52 supplies the original four-vertex motif and a checked 100-step Resolution certificate. T5-ANCHOR-WITNESS53 gives conditional same-template decision-to-witness extraction.
- **Project chats/files:** recent project status and local prior reports 47–53, plus Library PNP_Hostage_Review_and_Agent_Restart_2026-11-17 and PNP_Best_Proof_Chain_Draft_2026-11-17.
- **Google Drive:** [STREAM-INDEX18 (Oct 21)](https://docs.google.com/document/d/1hVfCnj-FofOIe1Iz6Q39I3LuLw34sS6CuVcjuPg8tpU/edit) gives a different restricted one-pass INDEX/no-forgetting obstruction, and continuity/outage log was reviewed.
- **Primary literature:** Bang-Jensen, Hell & MacGillivray 1988 DOI 10.1137/0401029; Roughgarden *Communication Complexity (for Algorithm Designers)* arXiv:1509.06257; Sherstov *Thirty-Five Years of Set Disjointness* (2014); Sharma & Velusamy ESA 2026 DOI 10.4230/LIPIcs.ESA.2026.131; Brakensiek, Putterman, Sharma & Velusamy arXiv:2610.07455 *Cores Characterize the One-Pass Streaming Complexity of CSPs* (Oct 5, 2026). The latter results establish a much broader framework and preclude a generic novelty claim here.

## 3. Exact five-symbol construction and theorem

The fixed tournament is T5 on Z_5 with R(x,y)=1 iff (y−x mod 5) is 1 or 3.

For each i in [m], create SIX distinct vertices (s_i,t_i,u_i,w_i,a_i,b_i). Add the THREE fixed edges
s_i→t_i, t_i→u_i, u_i→w_i.
Alice's m-bit string A chooses one additional edge at each i:
A_i=1: s_i→w_i; A_i=0: s_i→a_i.
Bob's m-bit string B chooses one additional edge:
B_i=1: t_i→w_i; B_i=0: b_i→t_i.

These 5m edges on 6m vertices constitute a genuine unweighted T5 input graph. Each source has a *fixed, input-independent* integer header and exactly 5m equal-width **pure edge-pair records** with no A/B/C labels or separate Boolean fields, streamed as the common 3m-edge scaffold, all m Alice edges, then all m Bob edges. There are no artificial Boolean constraints, extra target relations, loops, antiparallel pairs, or duplicated edges. Every graph is an **oriented DAG** under the per-gadget topological order b,s,t,u,w,a.

**Local exact counts**, independently determined by checking all 5^6 assignments:
A_i B_i = 00: 160 T5 colorings; 01: 100; 10: 50; 11: ZERO.
When both bits are one, the actual five-arc core
s→t, t→u, u→w, s→w, t→w
is UNSAT. To see it directly, the edges s→w,t→w,u→w require 3 distinct incoming colors for w, because the path s→t→u cannot have any repeated color in a loopless tournament. But every T5 color has exactly TWO in-neighbors. Removing either selected edge leaves a satisfying assignment; the two dummy leaf alternatives cannot obstruct satisfying extension.

Consequently, for any A,B,
  G(A,B)→T5 iff A∩B=empty,
and
  #Hom(G(A,B),T5)=160^{N00} 100^{N01} 50^{N10} (zero if N11>0).
The 6m-vertex original-source graph is always a DAG, yet its exact streamed decision encodes m-bit set disjointness.

### One-pass lower bound
Let a deterministic, **one-way, insertion-order** T5 stream decider read all 5m edges and decide SAT, with uniform program, shared fixed header, no rereads, and all writable/index/control state counted in S bits. After Alice's block, the streaming configuration must distinguish all 2^m possible A. Given A≠A', choose j where they differ and finish with Bob's singleton B=e_j; one continuation is SAT and the other UNSAT. Since the input head is at the SAME fixed boundary and all previously read input is unavailable, equal complete states would contradict correctness. Thus there must be ≥2^m distinct boundary states: S≥m−O(1) bits, or Ω(L/log L) for L=Θ(m log m) input bits. The O(m)-bit remembered-A vector gives a matching upper bound up to model constants. The prefix-state lower bound is representation-independent **within the sequential one-way model**.

### Deterministic p-pass lower bound
If the algorithm may make p sequential full passes over the fixed split source and retain S bits between blocks/passes, Alice and Bob can simulate it with at most 2p−1 alternating S-bit state messages: Alice→Bob once per pass and Bob→Alice on all but the final pass. The classical deterministic DISJ communication lower bound D(DISJ_m)≥m (proved by 2^m fooling set {(A,complement A)}) gives
  (2p−1)(S+O(1))≥m.
Hence S=Ω(m/p). For p *complete* passes, T≥pL, so the worst-case cost of this specified scan model obeys
  T·S=Ω(mL)=Ω(L²/log L)
in the customary fixed-program asymptotic regime, with O(1) finite control. (If using a variable number of passes or a nonstandard machine, restate and charge that model first.)

**This is a direct T5 restricted machine lower bound, NOT a P!=NP theorem.** In particular, the explicit source family has an O(m)-bit single-pass solver, and an offline indexed-input parser can compare Alice and Bob's record i with only O(log m) workspace. The lower bound vanishes when the machine can reread or randomly access prior source records without charge.

## 4. Hostile controls and proof systems
1. A constant-memory one-pass decoder is refuted by prefix indistinguishability, even if it recognizes the exact source grammar. A source recognizer cannot recover unavailable Alice bits from Bob's suffix.
2. A two-sided delayed edit genuinely changes SAT status but is NOT a logically necessary *nonrelativizing* WRAPPER hinge. The derived memory bound is the standard, relativizing streaming/communication method. Allowing random access defeats the asserted necessity.
3. On an identical final SAT graph, a source-aware **polynomial-time** witness finder reads both blocks and uses a precomputed valid 6-color tuple for each of 00/01/10. The proposed stronger hypothesis that ONE fixed tuple works for all three YES patterns is false: the union contains the UNSAT five-arc core. Do not swap “same final input” for different hard inputs; UWI remains OPEN.
4. On any NO instance, the four-vertex five-arc core has a **constant-size ordinary one-hot Resolution refutation**. We reconstructed the exact standard one-hot CNF: 20 Boolean variables, 119 source axioms; the independently checked DPLL-to-Resolution conversion produces 100 genuine Resolution inferences and the empty clause. This is a **scoped original-CNF proof**, not a general decision-to-proof transport. Short certificates coexist with the one-pass space bound.
5. No uncharged guest calls, cache, source parsing, generation, address index, recursion, work tapes, communication, or output. Upper algorithm uses paid bitset. Multi-pass protocol transmits every writable-state bit. No claim that output-counting rank or proof width forces arbitrary SAT runtime.

## 5. Executed audit
Reproducible CPython standard library script: `t5_dag_stream54_audit.py`. Deterministic seed 202611172229. All 87,380 complete (A,B) input pairs for m=1..8 checked, 9,840 YES and 77,540 NO; all local exact 5^6 counts independently enumerated; all 2^m prefix signatures checked for m<=10, i.e. 2^10 distinct states at the largest tested m. The five-arc core and each single-edge deletion were tested. Ordinary Resolution proof independently reconstructed, 100 inferences, 119 original CNF axioms, 291 recursive DPLL visits. 84 additional seeded fixed-length DAG/source/renaming controls, exact edge-only source parsing and 84 malformed-header rejection controls, plus 5-ary relation controls.
**265,751 assertions, ZERO unexpected failures.**
The finite test is a check of construction and certificate, not a proof of the asymptotic communication bound, whose separate fooling-set/prefix-distinguishability proof is above. External peer review OPEN.

## 6. Explicit proof DAG
| Arrow | Classification |
|---|---|
| T5-CSP NP-complete | ESTABLISHED literature (Bang-Jensen et al. 1988) |
| Fixed-length authentic 6m-vertex DAG family G(A,B) | PROVED construction |
| G(A,B) SAT iff DISJ(A,B) | PROVED exact |
| 160/100/50/0 local counting and product formula | PROVED exact |
| All 2^m prefixes must have distinct one-pass states | PROVED in the specified streaming model |
| Deterministic p-pass space Ω(m/p), T*S Ω(L²/log L) for p complete scans | PROVED under explicit model |
| 100-step one-hot Resolution certificate for 11 core | PROVED restricted |
| Streaming space LB implies lower bound on indexed-readonly Turing machines | **FALSIFIED** by O(log m)-workspace random-access solver on this family |
| Delayed Bob stream requires nonrelativizing WRAPPER | **FALSIFIED** as a general implication here |
| One common YES witness for all three possible 00/01/10 inputs | **FALSIFIED** |
| Same-final-instance UWI beating every eligible program | OPEN |
| General decider-to-proof-system transport | OPEN |
| Universal fully charged T5 time lower bound and P≠NP | OPEN |

## 7. Next assignments for four specialists
- **Resource Contraction:** Formalize the p-pass to indexed-random-access boundary with exact bit-access and head-movement charges. Seek a lower bound for actual general T5 instances after allowing random access, not simply against an artificially sequential interface.
- **Nonrelativizing Simulation:** Identify an edit whose SAT-status effect survives *any* available source-indexing/replay shortcut; prove the effect is required by SAT correctness, or falsify the proposed WRAPPER. Do not call the standard communication bound nonrelativizing.
- **Universal Obstruction:** Fix one final satisfiable T5 source, one common clock, and a declared program class. Include the actual O(m)-memory one-pass and O(log m)-workspace offline witness extractors. Test same-input quantifiers, not a per-program varying graph.
- **Proof Transport:** Independently replay the exact 119-axiom/100-inference certificate, then investigate whether an explicit proof transformation exists on high-girth locally consistent T5 NO cores. Short local refutations do NOT imply uniform T5 proof-size upper bounds.

**Single highest-value missing implication:** a fully costed lower bound that cannot be evaded by arbitrary *indexed* input access or by a source-aware polynomial-time T5 decider. Avoid further NP-completeness reductions from SAT unless quantitatively essential. No schedule changed. P≠NP OPEN.

### References
1. Bang-Jensen, Hell, MacGillivray, SIAM J. Discrete Math. 1(3) (1988) 281–298, https://doi.org/10.1137/0401029
2. Roughgarden, *Communication Complexity (for Algorithm Designers)* (2015), https://arxiv.org/abs/1509.06257
3. Sherstov, *Thirty-Five Years of Set Disjointness* (2014), https://web.cs.ucla.edu/~sherstov/pdf/mfcs-disjointness.pdf
4. Sharma, Velusamy, *Characterizing Streaming Decidability of CSPs via Non-Redundancy*, ESA 2026, https://doi.org/10.4230/LIPIcs.ESA.2026.131
5. Brakensiek, Putterman, Sharma, Velusamy, *Cores Characterize the One-Pass Streaming Complexity of CSPs* (Oct 2026), https://arxiv.org/abs/2610.07455
