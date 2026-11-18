# CROSS-TRACK T5-FIVEARC-OBSTRUCTION52 | 2026-11-17 20:29 PST

**Classification:** PROVED/EXACT restricted local-obstruction theorem and explicit ordinary Resolution certificate; finite independent audit passed. External mathematical review OPEN. **P versus NP OPEN.** The user has directed that research target T5-CSP itself, an NP-complete fixed-template problem, rather than repeatedly converting arbitrary SAT instances to T5.

## Four concrete integrations proposed before retrieval

1. Resource contraction + high-connectivity T5: attack the newest TMR-2 three-separator mixed YES/NO family with a no-advice **bounded-local-obstruction detector**, not only recognition of a special complete-bipartite family. Falsifier: YES member has an obstruction, or NO member lacks one.
2. Nonrelativizing simulation + same-source edit: add **one real original T5 arc** to a YES high-width three-connected family. Falsifier: the edit does not actually flip SAT, or the NO branch requires an unbounded source-dependent operation.
3. Universal obstruction + identical-source quantifiers: preserve one final satisfiable YES graph and a common clock, include a direct source-aware T5 coloring program as challenger. Reject swaps of the input between programs.
4. Proof transport + resource costs: extract an actual ordinary one-hot Resolution derivation directly from the bounded obstruction, check each inference, count source bytes, vertex names, adjacency, discovery, and certificate printing. Test whether a local proof blocks attempted unrestricted SAT-time inference.

## Newest substantive records checked

- **Resource/Information Necessity:** [TMR-2/074 three-separator orbit, 2026-11-17 19:12 PST](https://github.com/j15marti/pnp/blob/main/research/agents/tmr-2/2026-11-17_1912_TMR2_T5_THREE_SEPARATOR_ORBIT074.md). This family contains connected original-label CSPs based on b oriented K(h,h) blocks sharing s,t,u, exactly 3-vertex-connected base graphs with treewidth h. The recorded NO variant adds s->t, t->u, while the YES variant adds s->t, s->u. The newest relevant [TMR-4/062](https://github.com/j15marti/pnp/blob/main/research/agents/tmr-4/2026-11-15_2128_TMR4_LIVE_SHARED_CORE_EXTENSION062.md) and its handoff supply only a restricted fully charged compiler, not a lower bound on all T5 algorithms.
- **Nonrelativizing Simulation:** [TRACEAUDIT23](https://github.com/j15marti/pnp/blob/main/research/agents/nonrelativizing-simulation/2026-10-16_2223Z_TRACEAUDIT23_minimal.txt); newer [CLOCKMONOCHAIN26](https://github.com/j15marti/pnp/blob/main/research/agents/clock-gate/2026-11-17_CLOCKMONOCHAIN26.md) is a scoped restriction/fiber theorem, not a correctness-forced T5 WRAPPER.
- **Universal Obstruction:** [DIAGONALLIST34](https://github.com/j15marti/pnp/blob/main/research/agents/lspv-3/2026-10-17_0545_DIAGONALLIST34_NOTE.md), plus current project-chat same-final-input limitation. No all-program common-input UWI theorem was found.
- **Proof Transport:** [ALLFIELD-SHIELD-RETRACTION1](https://github.com/j15marti/pnp/blob/main/research/agents/proof/2026-10-16_2137_PROOF-TRANSPORT_ALLFIELD_SHIELD_RETRACTION1.md), [SEMDEG-FIREWALL1](https://github.com/j15marti/pnp/blob/main/research/agents/proof/2026-10-17_0145_PROOF-TRANSPORT_SEMDEG_FIREWALL1_HANDOFF.md), and immediate predecessor [T5-ROOTGAUGE-PC51](https://github.com/j15marti/pnp/blob/main/research/agents/cross-track/2026-11-17_1925_T5_ROOTGAUGE_PC51_STATUS.md). Their conditional or calculus-specific statements do not imply arbitrary SAT runtime bounds.
- Targeted Google Drive KRYLOVGUARD41, OBSERVERQUOTIENT41, historical WRAPPER reports and Library CIRCUITGUARD42 were inspected. Current GitHub commits also inspected. Primary literature: Bang-Jensen, Hell, MacGillivray (1988), DOI [10.1137/0401029](https://doi.org/10.1137/0401029); Fortnow, Lipton, van Melkebeek, Viglas (2005), DOI [10.1145/1101821.1101822](https://doi.org/10.1145/1101821.1101822); Cook and Reckhow (1979), DOI [10.2307/2273702](https://doi.org/10.2307/2273702).

## Main theorem: an edge-minimal four-vertex T5 NO obstruction

Let T5 be R(a,b)=1 iff (b-a) mod 5 belongs to {1,3}. On four original CSP vertices s,t,u,w, define the **five-arc DAG motif**:
[
s\to t,quad t\to u,quad s\to w,quad t\to w,quad u\to w.
]
**THEOREM:** This motif is UNSAT; removal of *any one* of its five arcs makes it SAT. Moreover, every larger T5 input graph containing this motif as a (not necessarily induced) subgraph is UNSAT.

**Symbolic proof:** All colors have exactly two distinct in-neighbor colors in T5. The path s->t->u forces colors of s,t,u to be pairwise distinct: adjacent ones must differ, and s=u would give a forbidden two-cycle in the target between the colors of s and t. The common sink w would require three different in-neighbor colors of its chosen color, impossible because the in-neighborhood has size two. Adding further arcs cannot restore a coloring. Minimality is witnessed by these color vectors [s,t,u,w], respectively after deleting s->t, t->u, s->w, t->w, u->w:
[
(0,0,3,1), (0,3,0,1), (0,1,4,2), (0,1,2,3), (0,3,1,1).
]
Each vector satisfies all four remaining genuine original arcs.

**Resolution transport, actual certificate:** The fixed direct five-color one-hot CNF of the five-arc graph has 20 Boolean rails, 119 axioms (four at-least-one clauses, 40 pairwise exclusivity clauses, 75 forbidden-arc clauses). A standalone deterministic DPLL-to-Resolution constructor produced a **100-inference ordinary Resolution refutation**, 219 total source-axiom-plus-derived lines, ending in the empty clause. A separate checker independently validated every parent index, unique complementary pivot and exact resolvent. For any larger graph containing the motif, all 119 axioms are literally present after renaming the four vertex indices, so the same 100 inference steps refute its one-hot encoding. This is actual bounded-subformula-to-Resolution transport; it is **not** arbitrary T5-decider-to-Resolution transport.

## Stronger one-edge status-changing control inside the newest TMR-2 family

For h>=4 and b>=2, let B(h,b) be TMR-2/074's b complete oriented bipartite K(h,h) blocks sharing three source-side vertices s,t,u. Each block has h-3 private source vertices and h private sinks, and every source in the block points to every sink.

Let Y(h,b) be B plus s->t and s->u. It is SAT: color (s,t,u)=(0,3,3), every private source 0 and every private sink 1. Now disclose and add the **single** additional original arc t->u, giving N+(h,b). The result is UNSAT: choose any one of the real sink vertices w. The five-arc motif is now a source subgraph. Both branches are directed acyclic, have large undirected connectivity/treewidth when h grows, and use actual five-symbol constraints. The NO branch has a constant-size semantic and Resolution certificate. The original equal-size TMR-2/074 NO variant (s->t,t->u) contains exactly the same obstruction.

This is a hostile falsification of the proposed implication:
> high 3-connectivity + unbounded treewidth + a genuine late SAT-status-changing edge => an inherently expensive NO decision.

A uniform, no-family-promise detector can parse an arbitrary explicitly listed T5 graph, build its adjacency table, enumerate all ordered distinct (s,t,u,w), and reject when the five arcs occur. This requires O(n^4) adjacency tests and ordinary polynomial total input-access/space cost; on a conservative bit-machine ledger, O((L+1)^6) time and O((L+1)^3) workspace suffice for reading/validation, adjacency creation, full motif search, and certificate serialization. On all other sources it must invoke a correct potentially exponential fallback. NO global polynomial T5 decider has been obtained.

## Executed independent audit

- Full five-color enumeration of the four-vertex obstruction (0 solutions), all 31 proper edge subsets (SAT), and explicit arc-deletion witnesses.
- Independent one-hot Resolution proof construction and complete proof-line checker: 119 genuine axioms, 100 derived resolvents, 219 total proof lines, 291 DPLL search nodes, final empty clause.
- 72 actual TMR-2-style sources h=4..9, b=2..5 with YES, original NO, and one-added-edge NO_PLUS; 228 seeded vertex-renaming controls; additional edges monotonicity; all expected answers, witnesses, and motif detection checked.
- **1,107 assertions, zero failures** in the final executed version. Standard-library CPython implementation. Results include the complete 219-line machine-checkable proof array.
- Executed source SHA-256: `a94d9b2d7304157a44ab6bd2be446a471e2f8f66df8c1f4388093fd8260cd2a7`.
- JSON result SHA-256: `ad3ff2ca1c4789b58b3ff1e2b2cdbc81c4a547b8a05a1e0a1843c74c63e7b2c5`.
- Local files: `t5_fivearc_obstruction52_audit.py` and `2026-11-17_T5_FIVEARC_OBSTRUCTION52_results.json`. Finite execution is not an independent external mathematical review.

## Updated proof DAG with strict status types

| Statement / arrow | Classification |
|---|---|
| T5-CSP is NP-complete | ESTABLISHED literature, fixed semicomplete target with multiple directed cycles |
| Fixed five-arc four-vertex DAG is minimal UNSAT | PROVED exact |
| Source graph containing that motif is UNSAT | PROVED exact |
| Direct five-color one-hot CNF has 100-inference Resolution refutation | PROVED exact, independent proof checker |
| TMR-2/074 NO and one-added-edge N+ contain that motif | PROVED exact |
| TMR-2/074 YES is genuinely SAT by explicit assignment | PROVED exact |
| High treewidth/3-connectivity + late edit forces hard T5 NO | FALSIFIED as a general inference by this family |
| Bounded local motif detector decides every T5 graph | FALSE; absence is inconclusive |
| Full-cost general T5 contractor including discovery, access, generation, workspace, recursion | OPEN |
| Status-changing WRAPPER forces a necessary nonrelativizing operation | OPEN; this instance is a countercontrol |
| One identical final SAT input and clock defeats all eligible witness algorithms | OPEN; direct YES witness is a challenger |
| Hard calculus certificates give lower bound on arbitrary T5 algorithms | OPEN; no general proof transport |
| Superpolynomial unrestricted worst-case time lower bound for T5-CSP | OPEN |
| P != NP | OPEN |

## Four specialist assignments

1. **Resource Contraction:** Integrate constant-motif detection *before* three-separator and tensor compilers. Charge source parsing, n^2 adjacency, all n^4 candidate quadruples, proof output and workspace. Next develop exact source-verified rules for locally obstruction-free, high-girth, 3-connected T5 cores; count generation/replay/recursion.
2. **Nonrelativizing Simulation:** Treat the YES-to-NO_PLUS single-arc disclosure as an adversarial nonrelativizing hinge control. Find a delayed SAT-status-changing edit that survives all bounded local obstructions, source-recognition, oracle replay, and direct evaluation. Any future proof must explain why SAT correctness forces acquisition of the delayed information.
3. **Universal Obstruction:** Preserve the same final YES source and one common clock for every eligible witness program. Include the explicit coloring above, and test whether claimed UWI restricts its program class or clock to exclude this perfectly valid uniform source recognizer. Do not infer a global UWI theorem from restricted family counterexamples.
4. **Proof Transport:** Independently audit the supplied 219-line certificate and prove a parameterized version of bounded-subformula Resolution embedding under arbitrary source renamings. For nonlocal UNSAT graphs, seek an *actual* transport theorem with explicit encoding/field/size charges, not a claim that all semantic algorithms emit a chosen calculus.

**Single highest-value next arrow:** move beyond *bounded-size UNSAT witnesses* and recognizably structured high-width T5 families, toward a direct T5-CSP theorem on high-girth, high-connectivity, locally k-consistent families that excludes cheap global source-recognition and semantic alternatives. No universal lower bound is yet established.

No agent schedules or prompts were modified.

READBACK_SENTINEL: T5_FIVEARC_OBSTRUCTION52_P_NP_OPEN
