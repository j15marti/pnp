# TMR-1/082: Uniform shortcut forcing and exact left inverses for both C5-to-T5 compilers

Date: 2026-11-17 22:55 PST. Status: symbolic exact identities for arbitrary authenticated sources, independent mathematical review OPEN. Finite checks COMPUTATIONAL. P versus NP OPEN.

## 1. Canonical source and model

Use the fixed template T5 on Z5, with R(x,y) iff (y-x) mod 5 belongs to S={1,3}. A canonical source is unary 1^n0 1^m0, followed by m strictly lexicographically sorted directed pairs in low-first binary with width w(n)=max(1,ceil(log2(max(2,n)))). Valid source bit length is L=n+m+2+2m*w(n). Arbitrary loops and opposing pairs are syntactically valid but semantically UNSAT; malformed encodings are INVALID. A witness is exactly 3n low-first bits with each 3-bit symbol in {0,...,4}, never 5,6,7.

## 2. New local algebraic forcing theorem: two and three arc shortcuts

**Theorem 082A (shortcut rigidity).** In any satisfying T5 assignment:

(a) If distinct source vertices x,a,b have arcs x->a, a->b, x->b, then a=x+3 and b=x+1 (mod 5).

(b) If distinct source vertices x,a,b,c have arcs x->a, a->b, b->c, x->c, then a=x+1, b=x+2, c=x+3 (mod 5).

**Proof.** Every arc increment is 1 or 3. Along a length-two path, the possible sums are 2,4,6, of which only 6 mod 5 belongs to {1,3}, hence both increments are 3. For length three, possible sums are 3,5,7,9; only 3 mod 5 belongs to {1,3}, hence all three increments are 1. This is an arbitrary-instance implication, not a finite-case conjecture. For contrast, a length-four shortcut admits ten different legal increment sequences, so extending rigidity by path length alone is invalid.

The two-arc result is consistent with TMR-1/075's forced transitive triads. The new three-arc shortcut is a diamond-shaped four-arc *bipartite triangle-free* pattern, unaffected by triangle-only preprocessing.

## 3. Exact source-authenticated unified quotient

**Theorem 082B (count-preserving quotient).** On every canonical directed T5 source G, scan every ordered triple or quadruple of distinct vertices for the authentic shortcut patterns above. Add the certified potential-difference equations. If inconsistent, return an authentic zero-solution certificate. Otherwise compute their connected classes C and potentials p_v so every satisfying assignment has x_v=t_[v]+p_v mod 5. For every original arc u->v:

* if u,v lie in the same class, check (p_v-p_u) mod 5 in S; failure certifies zero;
* otherwise write i=min([u],[v]), j=max([u],[v]), delta=t_j-t_i. For [u]=i, intersect the allowed mask delta in S+p_u-p_v; for [u]=j, intersect delta in p_v-p_u-S.

For each unordered class pair, intersect all masks. An empty mask certifies zero. The resulting generalized five-state difference-mask CSP Q(G) has at most n variables and at most n(n-1)/2 unordered constraints, each allowed mask of cardinality <=2. The extension x_v=t_[v]+p_v is a bijection from quotient satisfying assignments to original satisfying assignments. In particular Z_T5(G)=Z_mask(Q(G)) exactly, including zero, disconnected sources, isolated vertices and all witness counts.

**Proof.** The shortcut equations are consequences of original arcs by Theorem 082A. Any original satisfying assignment obeys them and therefore gives exactly one quotient class-label vector. Conversely a quotient assignment defines one original x-vector, and every original arc is checked by an algebraically equivalent same-class check or delta mask. All assignments are accounted exactly once. Inconsistencies only arise from source-authenticated equations or arc masks, and thus certify UNSAT.

A straightforward uniform sequential finite-alphabet bit implementation scans the real source and all motifs, maintaining modular weighted components and checking the complete final mask quotient. Conservative simultaneous bounds for this **preprocessor** are T=O((L+1)^7) and peak writable bits O((L+1)^3), including every source pass, auxiliary bit, contradiction detection and output. Equations can be streamed without retaining all O(n^4) motifs. This is NOT a polynomial-time decision algorithm for all T5 instances: the quotient CSP can remain NP-complete. An optional brute-force exact counter has time O(poly(L)(1+5^k)) and polynomial writable space, where k is the number of quotient classes.

## 4. Exact unannotated left inverses for prior compilers

Let H be a canonical simple undirected graph with n vertices and m edges. For each ordered edge {u,v}, u<v:

* Four-arc compiler D4(H), TMR-1/072: fresh w,z; arcs u->w, w->z, u->z, w->v. Its only two-path shortcut is u->w->z with u->z. Thus w=u+3, z=u+1 and the last arc requires v-u in {1,4}. The unified quotient has exactly n original classes, m {1,4} masks and no new spurious shortcut classes.
* Five-arc compiler D5(H), TMR-1/080: fresh a,b,c; arcs u->a, a->b, b->c, u->c, c->v. Its only three-path shortcut is u->a->b->c with u->c. Thus a=u+1, b=u+2, c=u+3 and the final arc requires v-u in {1,4}. There are no two-path shortcuts. The unified quotient again has exactly n original classes and m {1,4} masks.

The absence of other shortcuts follows from gadget degree patterns and the monotone original-vertex order: all a_e and b_e have unique in/out arcs, all c_e have a unique outgoing original-vertex arc, and an original-target alternative directed path would contradict the acyclic gadget order. Every source edge independently contributes one and only one shortcut.

**Consequently, without any supplied gadget annotations** the quotient exactly recovers the original undirected C5 template on H for both compiler images, and

    Z_T5(D4(H)) = Z_T5(D5(H)) = Z_C5(H).

This is a bijective witness identity, not just equisatisfiability. It makes the triangle-free bipartite DAG compiler D5(H) explicitly soluble *as a preprocessing step to C5-coloring*, but does not make general C5-coloring polynomial time.

Exact image sizes:
D4: N=n+2m, M=4m, L_D4=n+6m+2+8m*w(n+2m).
D5: N=n+3m, M=5m, L_D5=n+8m+2+10m*w(n+3m).
For simple H with m<=n(n-1)/2, w(n+3m)<=2w(n)+1 for n>=2, and both image lengths are <=15 times L_H=n+m+2+2m*w(n). Isolated vertices and n=0 are retained, avoiding implicit source promises.

The established unique-extension Boolean reverse compiler maps a generic N-vertex M-arc T5 source to exactly 8N Boolean variables and 20N+15M clauses of width at most three. It therefore produces:
D4: 8n+16m variables, 20n+100m clauses;
D5: 8n+24m variables, 20n+135m clauses.
These are source accounting identities, not SAT runtime lower bounds.

## 5. Mixed cores and resource countercontrol

H=K3 is NOT C5-colorable because C5 is triangle-free, whereas H=C5 admits exactly ten C5-homomorphisms. Both yield valid bipartite, triangle-free, directed acyclic D5 images, with zero and ten T5 assignments respectively. The unified quotient finds the underlying hard C5 source in either case. Thus triangle-freeness and absence of forced transitive triads are NOT sufficient to defeat local modular preprocessing, but the remaining C5 CSP still has NP-complete decision complexity by Hell and Nešetřil's 1990 H-coloring theorem.

The new reduction is a particularly strong falsification of *raw motif-absence* or *raw feedback rank* as a mandatory-work obstruction. No representation-independent superpolynomial time lower bound follows.

## 6. Executed computational verification and provenance

Full local standalone Node.js implementation: /mnt/data/tmr1_t5_diamond082.js, SHA-256 e2e9d3fce02398fb15ae9e8d2582f76b3a091257fbf0cca6cc5dbf999c4ddbfe. Raw /mnt/data/tmr1_t5_diamond082_raw.json, SHA-256 a638f42c5c631a834bb35e615ed47ace7d723b66c511c9d5320884c8d2ec3038. The full finite test executed 21,328 exact assertions, 761 no-opposed-arc directed graphs on <=4 vertices compared with direct exhaustive assignments, all 1,100 simple undirected H on <=5 vertices through **both** D4 and D5 unannotated quotient inverses, 6,941,848 enumerated source/assignment states, seven malformed-word rejections, and mixed YES/NO controls. Zero failures. The full local implementation is attached as a conversation artifact but is NOT committed.

Separately executed public Node certificate, committed as experiments/tmr/tmr1_t5_shortcut082_certificate.js, exact Git blob 967393f984ee9e4c812dc5314d570ad0a7cd7739: 1,100 source graphs, 6,482,112 explicit extensions checked and 6,490,923 assertions, zero failures; verifies shortcut multiplicities, gadget uniqueness, motif counts and all source-assignment extensions. It is narrower than the full local generalized-quotient test. The complete finite raw summary is separately published in results/raw/tmr/2026-11-17_2255_TMR1_T5_SHORTCUT082_RAW.json. Neither set of finite checks substitutes for the arbitrary-size proof.

## 7. Guards and next dependency

DISJ: PASS only for exact positive algorithm/reduction, no rank lower bound asserted. Relativization: local preprocessing relativizes and cannot alone separate NP, unrestricted claim OPEN. Simultaneous DTISP: same physical preprocessor's time and space are both charged; no forbidden resource pair derived. Configuration counting: upper-bound safeguard only. Graph algorithms, polymorphisms, Gaussian/affine, Fourier/flow, separator DP, local consistency, modulo arithmetic, alternative encodings, compact representations and source-aware recognition remain legal.

Primary source for C5 NP-hardness: P. Hell and J. Nesetril, *On the complexity of H-coloring*, J. Combin. Theory Ser. B 48 (1990), 92-110, https://doi.org/10.1016/0095-8956(90)90132-J. This theorem concerns **undirected** C5-coloring; directed T5 hardness follows via the explicitly verified D4/D5 compilers, not by silently treating the tournament as an undirected H.

Independent mathematical review, actual repository preflight, full LaTeX compilation, and Lean/nanoda replay remain OPEN.

**NEXT: C1-T5-C5-QUOTIENT-MIXED-CORE-ALGORITHM-AUDIT.** Apply authentic quotient and source-recognizers to non-compiler mixed YES/NO instances and compare residual complexity under all legal graph, Fourier, separator, treewidth, structural and compact methods. Do not infer generic work necessity from a gadget, high treewidth, or a missing shortcut pattern. P versus NP OPEN.
