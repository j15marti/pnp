# CROSS-TRACK 59 | T5-FORK-STAR-DUAL-TRANSPORT
2026-11-18 03:21 PST (America/Los_Angeles). **P versus NP OPEN**. Restricted exact theorem, independent finite checks, external review pending. No other agent files or schedules modified.

## Pre-search hypotheses frozen
Before retrieval at 03:14 PST, proposed: (1) Resource Contraction × change to two-attackers-one-target ternary grammar; (2) UWI × same-input decision-to-witness; (3) Nonrelativizing Simulation × WRAPPER source-aware bypass; (4) Proof Transport × literal renaming between dual canonical encodings. Local frozen proposals and executable results appear in the conversation bundle, T5_FORK_STAR_DUAL_TRANSPORT59_BUNDLE.zip.

## Newest substantive source ledger
1. TMR-1/086, 01:59 PST, exact binary cycle-space T5 normal form, binary-domain requirement remains essential: https://github.com/j15marti/pnp/blob/tmr1-20261115-independent-lean060/research/agents/tmr-1/2026-11-18_0159_TMR1_T5_BINARY_CYCLE_NORMAL_FORM086.md
2. TMR-2/080, 02:15 PST, source-derived width-five exact bucket elimination on 33-vertex/44-edge critical NO/YES pair, 94,405 bucket tuples each, NO=0, YES=103936080: https://github.com/j15marti/pnp/blob/main/research/agents/tmr-2/2026-11-18_0215_TMR2_T5_BUCKET_WIDTH080.md
3. TMR-3/080, 01:21 PST, charge-complete restricted three-hub source-derived clique adhesion (125-entry, correct 25-state Z5 quotient); draft https://github.com/j15marti/pnp/pull/264
4. TMR-4/084, 02:36 PST, restricted one-to-six size transport between complete five-way FBDDs and fully block-respecting three-bit validity-sound Boolean FBDDs, not arbitrary decider-to-Resolution; draft https://github.com/j15marti/pnp/pull/265
5. Nonrelativizing route LSPV-5/CARRYDP1, 02:06 PST, exact *relativizing* source-grounded carry DP, not WRAPPER hinge: https://github.com/j15marti/pnp/blob/main/research/main/2026-11-18_0206_MAIN_LSPV5_CARRYDP1_CONDENSED.tex
6. Current project-chat user-directed ternary experiment; Google Drive/Library searches produced historical sources but no newer substantive T5 replacement. Accessible search is not exhaustive.
Primary literature: Bang-Jensen/Hell/MacGillivray 1988 fixed semicomplete-digraph H-colouring classification, https://doi.org/10.1137/0401029 ; bounded-treewidth CSP context Ganian et al IJCAI 2020 https://doi.org/10.24963/ijcai.2020/263 .

## EXACT theorem: duality, decision equivalence, and restricted proof transport
Set R(a,b)=1 iff (b-a) mod5 is in {1,3}. Old ternary A(x,y,z)=R(x,y)R(x,z), new ternary B(x,y,z)=R(x,z)R(y,z). For every assignment c and every triple:
  B(c_x,c_y,c_z)=A(-c_z,-c_x,-c_y).
Hence for every list I of B-tuples, let J contain A-tuples (z,x,y) for each (x,y,z) of I. Then B(I) is satisfiable iff A(J) is; exactly the same number of assignments satisfy both by global involution c->-c. Holds with repeated variables, duplicate constraints and isolates. Both directions compile in O(m log(n+2)) bit operations for explicit fixed-T5 triples plus validation, and witnesses in O(n) fixed-color operations.

Under canonical one-hot color CNF (exactly one 5-color atom per vertex, plus the 15 forbidden color pairs per directed arc), variable permutation X_{v,a}->X_{v,-a} maps CNF(A(J)) exactly onto CNF(B(I), clause-by-clause. It maps each Resolution inference to a Resolution inference of identical width and length. This is an actual restricted proof-transport theorem. It DOES NOT map arbitrary machine deciders to Resolution, Polynomial Calculus, or FBDDs. Proof-file read/write and indexing work are at most linear in encoded proof size up to O(log(n+p)) bit addressing; the CNF builder produces O(n+m) clauses and O((n+m)log(n+m)) encoded bits.

For each original loop-free T5 arc u->v, introduce fresh w_e and replace edge by one distinct-variable tuple A(u,v,w_e) or B(u,w_e,v). Every valid edge admits exactly two extensions w_e; every invalid edge admits zero. Thus #ternary=2^m #T5 on the n original variables and m fresh auxiliaries. For loops, reject in O(m) and emit a constant-size UNSAT ternary gadget. T5 digraph SAT reduces in linear-size, fully source-generated form to either restricted (three distinct variable indices) ternary language; both are NP-complete by the known T5 classification. This is NOT parsimonious counting without the 2^m factor.

## Hostile falsification on the SAME ordered tuples
Use three distinct unordered triple supports on four original vertices:
 (0,1,2), (0,3,1), (0,2,3).
Old A yields only the star 0->1,0->2,0->3. Exactly 5*2^3=40 satisfying colorings, witness (0,1,1,1).
New B yields the same star plus 1->2->3->1. The T5 out-neighborhood of any color contains only two colors and is transitive; a directed triangle requires three distinct colors. Therefore B is UNSAT. Neither graph has an antiparallel edge; the new B graph has a genuine directed triangle, so NO directed-acyclicity claim. Constant-size source-aware W4 detection rejects this family, not a superpolynomial lower bound.
Small easier controls: (0,1,2),(0,2,1) produces A=20,B=0; distinct-support (0,1,2),(1,0,3) produces A=0,B=30 (opposite-arc shortcut).

The new B target elimination has matrix K_{ab}=sum_z R(a,z)R(b,z), where K rows are [2,0,1,1,0]; [0,2,0,1,1]; [1,0,2,0,1]; [1,1,0,2,0]; [0,1,1,0,2]. Exact det(K)=4 and full rank 5. TMR-3 three-parent sink w(a,b,c) is expressible as two B tuples sharing one target; a full-rank matrix alone does not imply costly unrestricted computation.

## Actual reproducible audit
Executed standalone CPython stdlib implementation with zero failed assertions:
- 15,000 pointwise all-color anti-isomorphism checks for 24 distinct ordered 4-variable triples;
- 25 independent original arc/helper assignment cases, verifying exactly 2 extensions per valid edge;
- 300 independently generated randomized B->A one-hot CNF set bijections, 44,120 B-clauses cumulatively;
- all distinct unordered triple-support four-variable source families with NO antiparallel arcs in either language: k=1: 24 checked, 0 SAT differences; k=2: 132 checked, 0 SAT differences; k=3: 168 checked, 16 SAT differences; minimum example reported;
- exact integer Bareiss determinant(K)=4.
Results contain explicit witnesses, exact counts and enumeration bounds. No empirical runtime lower bound inferred.

## Proof DAG, status
ESTABLISHED by literature: T5 H-colouring NP-complete.
PROVED exact: source-to-source A/B antiduality, assignment count bijection; distinct-helper T5->A/B edge encoding with 2^m extension factor; one-hot Resolution clause/literal renaming; W4 same-ordered-triples falsifier and common-target full-rank transfer.
KNOWN restricted: TMR-2 width-five 33-vertex upper algorithm, TMR-3 125/25 interface upper, TMR-4 block-respecting FBDD bound.
CONDITIONAL: any polynomial A/B decision procedure yields polynomial T5 decision, and with complete T5 decision-to-witness self-reduction (including actual query costs) polynomial T5 witnesses on the same final source input.
FALSIFIED: the same ordered tuple list has invariant SAT answer when A is replaced by B; local W4 or a matrix-rank gap proves unrestricted hard computation.
OPEN: UWI with single identical final input and common clock against all polynomial challengers; indispensable nonrelativizing WRAPPER hinge; arbitrary-decider-to-proof transport; representation-independent T5 time-space lower bound; P versus NP.

## Next specialist assignments
Resource Contraction: normalize both ternary grammars and source-derived common-target factors before any complexity claim; charge parse/access, generation, memo, exact large integers and recursion; challenge with W4 and bounded-adhesion upper bounds.
Nonrelativizing Simulation: test proposed hinge against direct O(m log n) role permutation and global color inversion. No hidden nonrelativizing operation here; find a genuinely unavoidable one or keep arrow OPEN.
Universal Obstruction: one identical final SAT T5 input and clock, challenger includes hypothetical polynomial A/B decider reduced to fully charged T5 witness extractor; do not use four-vertex NO as universal witness obstacle.
Proof Transport: formal checker for the canonical one-hot Resolution clause renaming; do not extrapolate to arbitrary deciders or FBDD interleaving. Check effect of fresh helper nodes on PC width and derivation accounting.

No specialist schedule, root proof tracker or peer manuscript changed. P versus NP OPEN.
