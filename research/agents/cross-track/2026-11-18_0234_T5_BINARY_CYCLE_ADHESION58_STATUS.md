# CROSS-TRACK T5-BINARY-CYCLE-ADHESION58 | 2026-11-18 02:34 PST

**Scientific status: new restricted exact counterconstruction, finite independent audit, external review open. P versus NP remains OPEN.**

## Four pre-search candidates
Recorded before source retrieval in the reproducible conversation bundle (`presearch_2026-11-18_0221_PST.md`):
1. Resource Contraction + Proof Transport: require a genuine proof-system transport theorem, not a local-consistency heuristic.
2. UWI + T5 decision-to-witness: use one identical SAT input/common clock and permit the fully charged conditional <=5n-call witness extractor.
3. Nonrelativizing Simulation + WRAPPER: demand a logically indispensable nonrelativizing step after source-aware replay and complete machine/resource charging.
4. Fixed-T5 + variable alphabet: do not transfer an obstruction to a larger tournament without checking whether it becomes SAT.

**Selected repair/falsification:** Combine latest TMR-1/086 full-rank binary-cycle normal form with latest TMR-3/080 three-hub 125/25-state transfer and construct same-skeleton YES/NO instances with a polynomial source-aware algorithm.

## Latest substantive evidence read
- **Resource / machine model:** TMR-1/086 (01:59 PST), [binary-cycle theorem](https://github.com/j15marti/pnp/blob/tmr1-20261115-independent-lean060/research/agents/tmr-1/2026-11-18_0159_TMR1_T5_BINARY_CYCLE_NORMAL_FORM086.md). Exact equivalence between T5 homomorphisms and binary edge choices `b in {0,1}^m` satisfying `C(1+2b)=0 mod 5`; `rank_F5 C = rho=m-n+c`; spurious linear solution `b=2` makes unconstrained Gaussian relaxation vacuous.
- **Universal obstruction / necessary information:** TMR-2/079 (01:12 PST), [33-vertex girth-8 PC/SAC survivor with 73-node complete UNSAT refutation](https://github.com/j15marti/pnp/blob/main/research/agents/tmr-2/2026-11-18_0112_TMR2_T5_GIRTH8_EDGE_CRITICAL079.md). TMR-5/085 [separate PC3 false positive and anchored-PC3 shortcut](https://github.com/j15marti/pnp/blob/tmr5-20261116-0121-jmv-vector-chain063/research/agents/tmr-5/2026-11-18_0145_TMR5_PC3_SURVIVOR_085_ADDENDUM.md).
- **Resource contraction / time-space:** TMR-3/080 (01:21 PST), [draft PR #264](https://github.com/j15marti/pnp/pull/264). Source-verified three-hub clique adhesion; fully costed restricted `T=O((N+1)^16(1+3^(t+1)+5^(t+3)))`, `S_peak=O((N+1)^6)` bits. K5 triple-sink chain has `n=3+12r,m=30r,t=4`, exact 125-state count and correct twisted 25-state quotient.
- **Proof Transport / cost-sound representation:** TMR-4/084, [draft PR #265](https://github.com/j15marti/pnp/pull/265). Restricted 5-way to complete validity-preserving 3-bit **block-respecting** FBDD equivalence `S5 <= Sblock <= 6 S5`; arbitrary interleaved FBDDs, arbitrary machines and decider-to-Resolution remain OPEN.
- **Nonrelativizing simulation:** LSPV-5/CARRYDP1 (02:06 PST), [source-grounded carry-DP certificate](https://github.com/j15marti/pnp/blob/main/research/main/2026-11-18_0206_MAIN_LSPV5_CARRYDP1_CONDENSED.tex). Exact but restricted and relativizing, therefore not the necessary nonrelativizing hinge.
- Also checked current [issue #3 project-agent handoffs](https://github.com/j15marti/pnp/issues/3), past project chats and project Library files. Targeted Google Drive search found no newer substantive replacement for these reports; this is a retrieval limit, not a claim of completeness.
- Primary literature: [Bang-Jensen/Hell/MacGillivray 1988](https://doi.org/10.1137/0401029) for fixed-T5 NP-completeness; [Atserias/Dalmau 2008](https://doi.org/10.1016/j.jcss.2007.06.025) for width/pebble-game model; [Ben-Sasson/Wigderson 2001](https://doi.org/10.1145/375827.375835) for **Resolution-specific** size-width transport; [Barto/Kozik/Niven 2009](https://doi.org/10.1137/070708093) for smooth digraph CSP classification.

## Exact integrated theorem: full rank and 3-connectivity remain easy

Use genuine fixed T5 arcs `R(a,b) iff (b-a) mod 5 in {1,3}`. Construct an r-block bipartite oriented graph from three initial hubs `(a,b,c)`. At each block add two hubs `(d,e)`, then for every three-element subset I of five ordered hubs `(a,b,c,d,e)` add one private sink with three arcs from I's hubs to the sink. Expose `(c,d,e)` as next boundary.

For every r>=1: `n=3+12r`, `m=30r`, `c=1`, `rho=m-n+1=18r-2`. The undirected graph is 3-vertex-connected: deleting <=2 vertices preserves at least one of three shared hubs between consecutive blocks; every sink retains an adjacent hub; each pair of remaining hubs in any atom shares at least one of its three original common sinks. The minimum degree is three. The graph is a DAG.

**YES orientation:** all three hub-to-sink arcs in every triple. Setting every hub to 0 and every sink to 1 is a witness. For each triple of hubs, let `w(x,y,z)=#{q in Z5: R(x,q),R(y,q),R(z,q)}`. Let `W(a,b,c,d,e)` be the product over the ten triples of these w factors. A complete, exact 125-state transfer counts all original labelings:
`F0(a,b,c)=1`;
`F_{j+1}(c,d,e)=sum_{a,b in Z5} F_j(a,b,c)W(a,b,c,d,e)`;
`Z(Y_r)=sum_{a,b,c} F_r(a,b,c)`.
Simultaneous Z5 translation yields an independently checked 25-state quotient.

**NO orientation:** change exactly TWO arcs in the first atom, keeping every undirected edge and all subsequent atoms: reverse the arc connecting triple-(0,1,2)'s sink to hub 0 and reverse the arc connecting triple-(0,1,3)'s sink to hub 3. Both YES and NO are DAGs on the identical undirected, 3-connected skeleton. A finite first-block UNSAT certificate fixes hub a=0 using valid global Z5 translation and checks the other eight unchanged sinks. Adding the first changed sink leaves exactly four possible hub tuples:
`(0,3,3,0,0),(0,3,3,0,3),(0,3,3,3,0),(0,3,3,3,3)` (hub b=3).
Adding the second changed sink separately leaves exactly:
`(0,0,0,2,0),(0,0,0,2,2),(0,0,2,2,0),(0,0,2,2,2)` (hub b=0).
These supports are disjoint, so the first block and therefore every NO graph N_r are UNSAT.

The fundamental signed F5 cycle matrix has an identity block in the chord columns and full row rank `18r-2` for BOTH orientations. Hence arbitrarily high **independent binary-cycle rank + 3-connectivity + same-skeleton mixed SAT/UNSAT** do NOT force superpolynomial T5 decision computation. Exact count on the canonical YES family is polynomial in total serialized source size, and NO has a constant-size source-grounded rejection. Recognition reads, parses, checks and regenerates all canonical arcs in polynomial time, charging source access/generation/output/retention. Unsupported input requires correct exact fallback, not a false general polynomial solver.

## Falsifiers and independent execution
Standard-Python source in the conversation reproducibility bundle, no optional packages:
- Exact 125-state vs *independently indexed* 25-state recurrences agree for **all 81 lengths r=0..80**. Counts at r=1,2,4: **6,120; 5,976,840; 6,272,708,104,160**.
- r=80 has **963 vertices, 2400 arcs, cycle rank 1438, 242-digit exact positive count**.
- Explicit constructed F5 fundamental cycle matrices at r=1..4 have ranks **16,34,52,70**.
- Exhaustive 625 gauge-normalized first-atom tuples yield the disjoint 4-tuple supports above. The two-reversal NO examples tested at r=1,2,4,10 are DAGs; same undirected skeleton and connectivity after deleting any two vertices verified at r=1,2,4.
- Generic raw PC3 rejects the first-atom NO and does not reject the YES, a hostile check proving this is NOT a hard lower-bound instance.
- A **wrong** untwisted 25-state quotient at r=4 gives **6,274,952,108,160**, falsified against the correct **6,272,708,104,160**.
- Finite audit and independent review are distinct: zero test failures do not prove a universal computational lower bound.

## Proof DAG
| Load-bearing arrow | Status |
|---|---|
| Fixed-T5 CSP NP-complete | ESTABLISHED by 1988 theorem |
| T5 labels <-> restricted binary cycle equations; rank rho | PROVED exact, TMR-1/086 |
| Triple-sink 125-state/25-state exact count | PROVED restricted, reproduced |
| Two-edge-reversed same-skeleton DAG NO pair | PROVED restricted; 625-tuple source certificate |
| High rank+connectivity+mixed orientation => costly all-algorithm decision | **FALSIFIED** by source-aware algorithm |
| Full PC / singleton-AC persistence => large necessary work | **FALSIFIED** as proposed inference (TMR-2/079) |
| All-input fully charged contraction | OPEN |
| Indispensable nonrelativizing WRAPPER operation | OPEN |
| Same-input/common-clock bounded UWI against ALL admissible witness algorithms | OPEN |
| Arbitrary decider -> lower-bounded proof system transport | OPEN |
| Unrestricted superpolynomial T5 bound, P != NP | **OPEN** |

## Four next specialist assignments
1. **Resource Contraction:** run authenticated PC, modular-offset and separator quotients on binary-cycle representations; formulate a residual invariant that **cannot** be defeated by the 125-state family.
2. **Nonrelativizing Simulation:** explicitly attempt WRAPPER/replay bypass by canonical pair recognition and restricted carry-DP. Charge full generation, source probes, recurrence, live workspace and calls; show a correctness-*forced*, not merely implementation-specific hinge.
3. **Universal Obstruction:** one identical final satisfiable `Y_r`, common clock, bounded algorithm-description and time class; include hardcoded witness controls, the family recognizer and conditional <=5n-call T5 witness extraction. Keep `exists G forall A` distinct from `forall A exists G`.
4. **Proof Transport:** translate the actual TMR-2/079 **73-node** certified domain branching tree into a fully checked one-hot Resolution/RUP refutation with explicit inference and bit costs. Do not infer arbitrary-decider transport from proof-logging models.

**Highest-value unresolved implication:** unrestricted T5 necessary work after arbitrary indexed input access, polynomial source recognition, bounded-adhesion exact counting, PC/affine quotient and legal adaptive computation. **P versus NP remains OPEN.**

**Reproducibility:** local extended report, pre-search file, full executed Python audit and result JSON are bundled in the run's conversation artifacts. No claim that those additional files were uploaded to this GitHub path.
