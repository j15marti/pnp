# CROSS-TRACK SYNTHESIS 64 | High-girth theta anti-pin theorem
**2026-11-18 07:31 PST** | New exact restricted theorem and executed hostile audit. **P versus NP OPEN.**

## Pre-search candidates (frozen locally before retrieval)
(1) Upgrade #63 relative pins to five-regular/girth-eight using source-derived replacement, not additive attachment; (2) price full contraction versus same-input UWI; (3) stress proof transport after gadget substitution; (4) demand an indispensable nonrelativizing WRAPPER hinge. Selected (1) after reading current outputs.

## Most recent specialist outputs actually read
- **Resource contraction TMR-1/091**, 06:55 PST, branch `tmr1-20261115-independent-lean060`, `research/agents/tmr-1/handoff.md`: full strict 3-distinct-literal parsimonious T5-to-CNF compiler; isolate normalization separately charges factor 5^i. Translation does NOT preserve original five-regular girth-eight promise.
- **Resource/time-space TMR-3/085**, branch `research/tmr3-t5-path-saturation085-20261118`, `main3_PNP_TIME_SPACE_TRADEOFFS.tex`: directed four-walk source-computable endpoint saturation and high-treewidth easy torus. Our new theorem adds arbitrary per-edge orientation and the high-girth theta pin barrier.
- **Nonrelativizing simulation LSPV-5 FACTOREDGATE1**, 07:06 PST, `research/main/2026-11-18_0706_MAIN_LSPV5_FACTOREDGATE1_CONDENSED.tex`, commit `5e0019e8`: syntactic reversible-conjugacy endpoint certificates are cheap on a recognized class; general semantic verification coNP-complete, nonrelativizing WRAPPER necessity open.
- **Universal obstruction TMR-2/084**, 06:12 PST, `research/agents/tmr-2/2026-11-18_0612_TMR2_T5_GIRTH_CYCLE_CERT084.md`: 170-vertex, five-regular, girth-eight source, short seven-node certified NO, and polynomial first cycle moment. Growing source-hard residual open.
- **Proof transport / cost-sound TMR-4/088**, 06:36 PST, branch `tmr4-20261118-0636-successor-frontier088`, `research/agents/tmr-4/handoff.md`: successor-triangle source recognizer gives width<=6 full-query OBDD even at high minimum frontier; NO arbitrary-decider-to-Resolution bridge.
Also searched project chat context, Library, Drive (no fresher substantive T5 report located), main/branches/PRs and primary CSP literature. No independently verifiable newer project chat was found.

## NEW THEOREM THETA-GIRTH8-ANTI-PIN64 (PROVED, restricted)
Fix T5: `R(a,b) iff (b-a) mod 5 in {1,3}`. A two-terminal *theta network* is a bipartite source made of >=1 internally vertex-disjoint oriented u-v paths, without extra arcs on their private vertices. Suppose every undirected cycle has length >=8. For **every** orientation of all arcs, the existential set of endpoint offsets `x_v-x_u mod 5` has size **at least two**. Thus no such gadget enforces any single exact relative color.

**Proof.** For a path of length L with q reversed arcs under traversal u-to-v, every allowed modular difference is `L+q+2b mod 5` for b=0,...,L, each attainable with positive multiplicity. Its support size is `min(L+1,5)`, since 2 is invertible mod5. Every L>=4 path has FULL support. If two internally disjoint paths both had length <=3, together they would form a cycle of length <=6, forbidden by girth>=8. Hence at most one short path restricts endpoints, and even its support size is >=2; all other path supports are full. Independent private internal vertices make combined support their intersection. QED.

**Scope restriction:** This rules out pure internally-disjoint path networks only, not branching/shared-interior gadgets, port replacement, or an all-gadgets high-girth pin. Separately, *adding* a gadget edge to a saturated degree-five original terminal cannot preserve degree five; genuine degree-balanced edge/vertex replacement is needed. #63 bipartite decision-to-witness theorem does not automatically extend to five-regular girth-eight source promises.

## COMPUTATIONAL hostile audit
The stdlib Python source `audit_theta_pin64.py` checked:
- **510** orientation words across path lengths 1..8, 25 endpoint assignments each, matrix DP versus exact binomial expression;
- independent internal-color brute force for lengths <=4;
- **144,128** exhaustive ordered two-path, bipartite/girth>=8 networks with lengths <=8;
- **1,755** reproducibly sampled valid 3..5-path theta networks.
**311,657 assertions, zero failures.** Every theta support size was exactly `min(L_min+1,5)`, minimum support 2.

Independent `audit_graph_topology64.py` constructed four-edge subdivisions of `K_{k,k}`, k=3,4,5,6,8, with arbitrary oriented paths; checked every authentic source arc and witness, all degrees, and girth **16** by BFS. n=2k+3k^2, m=4k^2; source has a Kkk minor so treewidth>=k, yet polynomial original-source witness construction by exact length-four saturation. These are NOT five-regular: private vertices have degree 2. For k=8 the audit checked n=208, m=256, girth16. This independently agrees with /085's earlier high-width easy control; no novelty claimed for the general padding idea.

**Charged upper:** parsing and authenticating original graph, discovering private chains, confirming no extra edges, girth/degree inspection, five-bit support intersections and witness output all take polynomial explicit-source time and O(N) straightforward adjacency/work memory, with no free source discovery. Finite CPython runs are not native TM microstep proofs. Four-edge path deletion preserves SAT, **not exact #assignments**.

## Proof DAG (no promoted arrows)
| Arrow | Status |
|---|---|
| T5 fixed-target homomorphism NP-complete | ESTABLISHED [1] |
| Oriented path support `S_{L,q}`; all L>=4 paths saturated | PROVED exact |
| Bipartite girth>=8 theta can enforce a unique offset | FALSIFIED |
| All branching girth>=8 gadgets fail exact pinning | **OPEN**, NOT IMPLIED |
| Exact pinning preserved under five-regular girth>=8 source compiler | OPEN |
| Original-source T5 decision in P => witness in FP for unrestricted/bipartite class | CONDITIONAL, previously established via generated queries |
| High-width/high-girth alone => necessary superpoly time or Resolution | UNSUPPORTED |
| Encoding-specific CNF restriction => arbitrary-decider proof transport | OPEN |
| Indispensable nonrelativizing WRAPPER hinge | OPEN |
| Same-input/common-clock UWI defeats polynomial witness finders including derived queries | OPEN |
| General T5 superpolynomial lower bound, P!=NP | **OPEN** |

## Four next assignments
1. **Resource Contraction:** authenticate and eliminate all private length>=4 path chains in a fully priced source-to-residual compiler, charging failed recognition, generation, workspace, recursion and witness output; search nonneutral residuals.
2. **Nonrelativizing Simulation:** test WRAPPER necessity against factored source recognition and the exact path-support shortcut; distinguish syntactic certification from coNP semantic equivalence.
3. **Universal Obstruction:** seek genuinely branching/edge-replacement girth>=8 pin gadgets under five-regularity, test same original YES instance and common clock against all polynomial challengers; exclude fixed-core NO certificates.
4. **Proof Transport:** for any genuine replacement gadget prove canonical CNF clause/proof overhead rather than assuming arbitrary-decider-to-Resolution transfer. Red-team with /085 four-walk padding and /088 affine successor source compiler.

**Reproducibility:** full local bundle: `2026-11-18_0731_T5_GIRTH8_THETA_PIN_FIREWALL64_BUNDLE.zip` with PRESEARCH_PROPOSALS, both complete stdlib Python audits, raw JSON, full mathematical report, SHA256SUMS. No specialist schedules or other owners' manuscripts changed. Independent peer review open.

**Primary references:** [1] Bang-Jensen, Hell, MacGillivray (1988), DOI 10.1137/0401029; [2] Dalmau, Kolaitis, Vardi (2002), DOI 10.1007/3-540-46135-3_21; [3] Zhuk (2020), DOI 10.1145/3402029; [4] Baker, Gill, Solovay (1975), DOI 10.1137/0204037.
