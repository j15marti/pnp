# T5-TWO-ATTRIBUTE-BALANCED60 | 2026-11-18
**P versus NP is OPEN.** Restricted mathematical results and reproducible finite audit; no unrestricted computational lower bound.

## Model
Letters and colors each form the regular 5-tournament R(a,b) iff (b-a)%5 in {1,3}. A point is (letter,color). Define strict discordance D((a,c),(b,d)) iff a!=b,c!=d and [R(a,b) XOR R(c,d)]. Define permissive winning-XOR W((a,c),(b,d))=R(a,b) XOR R(c,d), allowing one tied attribute. Define the balanced ternary fork B(x,y,z)=D(x,y) & D(x,z) & [R(letter(x),letter(y)) XOR R(letter(x),letter(z))], so the center wins by letter against precisely one opponent and by color against the other.

## Theorem 1 (pairwise-XOR collapse)
Both the strict pairwise D-fork and permissive W-fork CSPs are decision-equivalent to ordinary graph 5-coloring. D's target graph is undirected, 8-regular, with 25 vertices/100 edges: project a D-solution to letters; lift each proper coloring by t -> (t,-t). W's target digraph has outdegree 12: project using h(a,c)=c-a mod5; the same anti-diagonal embedding lifts every proper 5-coloring. Source edge orientations do not change YES/NO answers for either binary model.

## Theorem 2 (balanced ternary reduction)
B on 25 states is satisfiable iff its letter projection T(a,b,c)=[R(a,b)&R(c,a)] OR [R(b,a)&R(a,c)] is satisfiable. Projection is immediate; the inverse lift sets every vertex's color to minus its letter. The 25-state dimension therefore does not raise decision complexity beyond the five-state balanced relation.

## Theorem 3 (direct NP-completeness)
T(a,b,c)&T(b,a,c)&T(c,a,b) holds exactly when a,b,c induce a directed 3-cycle in T5. Every ordered pair a!=b lies in a directed 3-cycle because T5 is regular: if a beats b and b's two out-neighbors did not beat a, a would defeat >=3 vertices, impossible. Thus existentially quantifying c in the triple gadget defines a!=b. Replace every edge of an arbitrary graph with a fresh c and three T constraints. This gives a linear-size reduction from graph 5-colorability; the five-state and two-attribute balanced CSPs are NP-complete.

## Theorem 4 (parity-only firewall)
The five distinct-variable balanced constraints (0,1,2),(0,1,3),(1,0,2),(1,2,3),(2,0,3) are consistent as abstract edge-sign parity equations but UNSAT over T5. If 0 beats1, 3 must beat three other vertices; if 1 beats0, 3 must lose to three others; T5 has outdegree/indegree exactly two.

## Audit (deterministic seed 20261118)
- 10,771 assertions passed, 0 failures.
- Target strict degree 8, permissive outdegree 12.
- Of 25^3 ordered triples: strict pairwise fork admits 1600; permissive fork 3600; balanced fork 800. Balanced five-letter relation admits 40 of 5^3 triples.
- Exhaustive 4,096 subsets of 12 centered triples on four variables: old two-wins language 107 SAT, new balanced language 1696 SAT, 1,621 differing SAT outcomes. 32 balanced UNSAT instances pass abstract orientation-parity consistency; smallest such uses 5 constraints.
- Three-center cycle gadget tested over all 125 color triples; 210 graph coloring instances/gadgets tested with proper witness extraction.

## Proof DAG
PROVED: Pairwise-XOR collapses to 5-coloring; balanced 25-state projection/lift; direct balanced NP-completeness; parity-consistent four-vertex UNSAT example.
OPEN: arbitrary-algorithm T5 superpolynomial time lower bound, fully charged hereditary contraction, mandatory nonrelativizing WRAPPER, same-final-input UWI, universal arbitrary-decider proof transport, P vs NP.

## Next specialists
Resource Contraction: measure balanced hypergraph elimination after eliminating redundant color dimension; charge all parsing, state, recursion and output.
Nonrelativizing Simulation: attempt cross-attribute constraints that break the anti-diagonal global lift and test against semantic shortcuts/oracle replay.
Universal Obstruction: compare the identical final balanced instance and common clock against source-aware 5-state witness recovery.
Proof Transport: develop a checked encoding-specific map for the three-center cycle gadget; do not infer algorithmic lower bounds.

## Sources
Hell & Nesetril, On the complexity of H-coloring, JCTB 1990 DOI 10.1016/0095-8956(90)90132-J.
Bang-Jensen, Hell & MacGillivray, The complexity of colouring by semicomplete digraphs, SIDMA 1988 DOI 10.1137/0401029.
VERIFICATION_SENTINEL_T5_TWO_ATTRIBUTE_BALANCED60
