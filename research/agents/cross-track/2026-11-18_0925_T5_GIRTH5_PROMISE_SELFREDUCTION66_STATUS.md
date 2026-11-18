# Cross-Track Synthesis 66 | Girth-five promise decision to original-input witness

**2026-11-18 09:25 PST. P versus NP OPEN.** New conditional theorem and promise-width corollary; no unrestricted lower bound. Independent mathematical review and native-TM microsteps open.

## Pre-search proposals (frozen before retrieval)
1. Attack the hard-count/easy-decision girth-eight family for invalid decision-cost inference.
2. Explore higher-girth pins beyond theta paths, without extrapolating theta impossibility.
3. Test fully charged same-input UWI and proof transport against promise-oracle composition.
4. Demand an indispensable nonrelativizing WRAPPER hinge; try source-aware and relativizing bypasses first.
The third candidate is the strongest closeable implication.

## Newest specialist research consulted
- **Resource contraction:** Newer [TMR-1/093 full-rank path-transfer theorem](https://github.com/j15marti/pnp/blob/tmr1-20261115-independent-lean060/research/agents/tmr-1/2026-11-18_0903_TMR1_T5_PATH_INVERSE093.md) proves det(M_path)=2^ell and rank five despite fully positive endpoint support for ell>=4, with a polynomial-time exact transfer algorithm. This eliminates exact-rank and positive-support proxies for unavoidable work. Predecessor [TMR-1/092 Fourier-flow exact count and poly(L) min(5^rho,2^(n-c)) upper bound](https://github.com/j15marti/pnp/blob/tmr1-20261115-independent-lean060/research/agents/tmr-1/2026-11-18_0759_TMR1_T5_FOURIER_FLOW_DUAL092.md); [TMR-3/086 affine/path source contraction](https://github.com/j15marti/pnp/blob/research/tmr3-t5-affine-core086-20261118/research/agents/tmr-3/2026-11-18_0722_TMR3_T5_IRREDUCIBLE_AFFINE_CORE086.md).
- **Nonrelativizing simulation:** [LSPV-5 FOLDPARITY1 typed semiconjugacy](https://github.com/j15marti/pnp/blob/main/research/main/2026-11-18_0811_MAIN_LSPV5_FOLDPARITY1_CONDENSED.tex); restricted endpoint proof, not unrestricted machine separation.
- **Universal obstruction:** [TMR-2/087 exact directed edge lift, girth five](https://github.com/j15marti/pnp/blob/main/research/agents/tmr-2/2026-11-18_0812_TMR2_T5_GIRTH5_BALANCED_GADGET087.md).
- **Proof transport:** [TMR-4/090 complete-query five-way OBDD/FBDD width-one versus at-least-five theorem](https://github.com/j15marti/pnp/blob/tmr4-20261118-0836-width-gap090/research/agents/tmr-4/2026-11-18_TMR4_T5_UNIFORM_WIDTH_GAP090.md), not a Resolution lower bound.
- Project chats/current history, recent [issue #3](https://github.com/j15marti/pnp/issues/3) handoffs, GitHub commits and file paths, Conversation/Library search and connected Google Drive searches were checked. No newer relevant 2026-11-18 T5 Drive report surfaced. Primary sources included Bang-Jensen-Hell-MacGillivray 1988, Barto-Kozik-Niven 2009, Dyer-Richerby 2013, Atserias-Dalmau 2008 and Kayll-Morris 2023. The latter abstract alone is insufficient for a polynomial-size uniform girth-eight reduction.

## Exact theorem, restricted/conditional
Fix R(a,b) = [(b-a) mod 5 is in {1,3}]. Let C5 denote all oriented simple digraphs of undirected girth >=5. **If an unrestricted all-input polynomial-time decider D5 exists for T5-homomorphism on C5, then unrestricted T5 ORIGINAL-input witness search is in FP.** This does *not* assert D5 exists.

**Edge compiler F:** replace every arc u->v of an oriented simple source with three internally disjoint paths, orientation words `--`, `---`, `---+` (minus = backward). Their five endpoint-difference cofactor vectors are (0,2,0,1,1), (3,1,1,3,0), (1,6,1,4,4). Product = (0,12,0,12,0)=12R, so
`#Hom(F(G),T5)=12^m #Hom(G,T5)`,
with n+6m vertices, 9m arcs, girth five for m>0. Immediate NO for loops or opposed arcs before compilation; remove duplicates.

**Relative-color pins:** G1(u,v;w) consists of u->v, u->w, w->v; existential w forces v-u=1 mod5. G3(u,v;w) consists of u->v, u->w, v->w; existential w forces v-u=3. Reversing terminals forces 4 and 2. A ZERO pin uses fresh q,w1,w2 and G1(u,q;w1) AND G1(v,q;w2), forcing v-u=0. Every pin adds <=3 vertices and <=6 arcs.

**Witness extractor:** initially test satisfiability via D5(F(G)). Gauge-fix one original root in each of c components to 0, then for each of n-c remaining original vertices try offsets 0,1,2,3 against its root, maintaining a satisfiable pin prefix; if all fail, offset 4 is necessary. Every augmented query is compiled by F into C5, even if its native pins introduced triangles. Before F reject local loops/opposed arcs; these cases are genuinely UNSAT. Verify the final coloring against all original arcs. At most 1+4(n-c) D5 calls. Max compiled query size n+6m+39(n-c) vertices and 9m+54(n-c) arcs, each O((n+m)log(n+m)) bits. All repeated parsing, query construction, recognition, workspace, failure branches, recursion and output charged; runtime <= poly(n+m)+(1+4(n-c))p(O((n+m)log(n+m))) when D5 uses polynomial p.

**Caveat:** This bypasses a native girth-five relative pinning gadget, but DOES NOT preserve five-regularity or girth eight. Those stronger promises remain open.

## Cross-track corollary
TMR-4/090 says for nonempty-arc T5 sources, optimum width for complete-query five-way deterministic OBDD/FBDD =1 if UNSAT and >=5 if SAT. F preserves SAT and maps to girth-five sources. Hence deciding whether optimum width <=4 on nonempty simple oriented girth-five sources is **coNP-complete**. A polynomial-time correct uniform factor-alpha<5 optimal-width compiler on this class would imply P=NP. This is *representation acquisition hardness*, not a general decision time lower bound or a Resolution-transport theorem.

## Executed adversarial checks
Independent standard-library Python audit: 2,689 assertions, zero failures; all 25 endpoint pairs for three path cofactors and the product; all 25 pairs for each of five exact relative pins; 160 original oriented sources, 565 compiled-girth-five oracle queries, peak 105 vertices and 144 arcs, original witness decisions verified against independent 5^n enumeration. Prototype oracle is explicitly exponential, not a claimed P decider. Three compiled graphs checked by independent expanded-source domain-propagation solver, including a 40-vertex, 54-arc UNSAT transitive K4 lift. All oriented simple n<=3 counting/girth identities verified.

Falsifiers: native pin girth fails but recompile repairs C5; high-girth8/five-regular promise does not follow; quotient recognition does not solve original NP-complete core; a same-input UWI must allow auxiliary compiled queries and use a common clock large enough for the chosen challenger; width-opt recognition is not arbitrary SAT-time hardness; WRAPPER is not needed by this entirely relativizing self-reduction.

## Explicit proof DAG
| Arrow | Status |
|---|---|
| General T5 Hom NP-complete | ESTABLISHED |
| F preserves SAT and exact count, girth=5 | PROVED RESTRICTED |
| Five exact relative pins | PROVED RESTRICTED |
| D5 in P -> unrestricted same-input T5 witness in FP | PROVED CONDITIONAL |
| Complete-query width gap + F -> girth-five width threshold coNP-complete | PROVED CONDITIONAL ON RESTRICTED WIDTH THEOREM |
| Hard exact counting -> hard SAT decisions on always-SAT girth-eight family | FALSIFIED |
| five-regular girth-eight decider-to-witness promise closure | OPEN |
| mandatory nonrelativizing WRAPPER hinge | OPEN |
| same-final-input common-clock universal UWI obstruction | OPEN |
| arbitrary decider-to-Resolution proof transport | OPEN |
| uniform superpolynomial T5 machine lower bound | OPEN |
| P versus NP | **OPEN** |

## Next four specialist assignments
- **Resource contraction, TMR-1/TMR-3:** Incorporate /093's invertible-but-easy path transfers; audit the source-authentic F compiler/recognizer and residual base-source after weighted/Fourier/affine compression, charging full access, generation, workspace and exact arithmetic.
- **Nonrelativizing simulation, LSPV-5:** Check relativization of this derived-query extractor and reject any WRAPPER step lacking a proven indispensable nonrelativizing operation. Stress-test hidden-cost tape certificates.
- **Universal obstruction, TMR-2:** Add the composed D5-extractor to all same-input common-clock UWI challengers; distinguish girth-five from five-regular girth-eight, and seek a valid stronger promise reduction if possible.
- **Proof transport, TMR-4:** Check the precise width acquisition corollary and work toward a checked proof-system-specific translation; never infer unrestricted Resolution or arbitrary-algorithm lower bounds.

Full local auditable report, script, results and frozen pre-search proposals are in the 2026-11-18_0925_T5_GIRTH5_PROMISE_SELFREDUCTION66_BUNDLE.zip reproducibility artifact. No specialist agent settings or files were changed. **P versus NP OPEN.**
