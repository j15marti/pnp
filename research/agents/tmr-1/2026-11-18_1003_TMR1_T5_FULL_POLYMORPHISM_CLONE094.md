# TMR-1/094: complete polymorphism classification of the exact five-symbol beat template

**Owner:** TMR-1 / PNP Machine Model Lead. **Time:** 2026-11-18 10:03 America/Los_Angeles. **Scope:** new elementary all-arity symbolic theorem, independently executed finite computational checks, primary-source corroboration of complexity classification. Independent mathematical review, complete LaTeX compilation and formal kernel reconstruction remain OPEN. P versus NP remains OPEN.

## The exact template

Let T denote the loopless five-vertex tournament on Z/5Z, with a directed arc a -> b iff b-a is 1 or 3 modulo five. An r-ary polymorphism is a map F:(Z/5Z)^r -> Z/5Z preserving this arc relation coordinatewise: whenever every a_i -> b_i, one also has F(a_1,...,a_r) -> F(b_1,...,b_r).

**Theorem C1-T5-ALL-ARITY-PROJECTIONS094.** For every integer r >= 1, the entire set of r-ary polymorphisms of this exact T consists of the 5r distinct operations

\[
F(x_1,\ldots,x_r)=x_i+c\pmod5,
\qquad 1\le i\le r,\quad c\in\mathbb Z_5.
\]

In particular, every endomorphism is a rotation (the template is a core), the full automorphism group is C5, there are exactly ten binary polymorphisms, and the only idempotent polymorphisms in every positive arity are the coordinate projections. Consequently there is no idempotent weak-near-unanimity or Taylor polymorphism for this template.

## Symbolic proof (all arities)

**Step 1, automorphism rigidity.** Any endomorphism u:T -> T must be injective. For two distinct elements a,b precisely one of a -> b or b -> a holds; if u(a)=u(b), the preserved arc would become a forbidden self-loop. On five elements injectivity is bijectivity. Every rotation a |-> a+c is an automorphism. An automorphism fixing 0 must preserve its two out-neighbours {1,3} and two in-neighbours {2,4}. The edge 3 -> 1 uniquely orders its out-neighbours; the edge 4 -> 2 uniquely orders its in-neighbours. Therefore an automorphism fixing 0 fixes all five vertices, establishing Aut(T)=C5.

**Step 2, simultaneous translations.** Fix a polymorphism F of arity r and an offset vector d=(d_2,...,d_r). The unary map u_d(t)=F(t,t+d_2,...,t+d_r) preserves T, because whenever t -> t+s, moving *every* argument by s produces a coordinatewise arc. Step 1 therefore yields u_d(t)=t+h(d) for some h:Z5^(r-1) -> Z5. Equivalently,

\[
F(x_1,\ldots,x_r)=x_1+h(x_2-x_1,\ldots,x_r-x_1).
\]

This identity is forced by the template; it is not an equivariance assumption.

**Step 3, the discrete derivative test.** For each i=2,...,r, consider simultaneous coordinatewise arcs changing x_1 by +1, x_i by +3 and all remaining coordinates by +1. Only offset d_i increases, by 2 modulo five. Preservation implies

\[
1+h(d+2e_i)-h(d)\in\{1,3\}\pmod5,
\]

hence h(d+2e_i)-h(d) belongs to {0,2}. Define H(z)=3h(2z), with scalar multiplication and arguments over Z5. Then

\[
H(z+e_i)-H(z)\in\{0,1\}\pmod5
\]

for every z and i. Along any five-element coordinate circle, the five increments can be represented by ordinary integers 0 or 1. Their sum is a multiple of five and between zero and five, so they are either all 0 or all 1. Thus on each coordinate fiber, H is either constant or has slope 1.

**Step 4, rigidity across coordinate fibers.** Fix different coordinates i and j and a fiber in coordinate i. Denote its slope by s in {0,1}. On the adjacent fiber obtained by incrementing coordinate j, denote its slope by s'. The j-coordinate difference between these fibers, evaluated at i-coordinate t, is A+(s'-s)t modulo five for some A. Preservation already requires this difference to lie in {0,1} for all t in Z5. If s' differs from s, those five values cover *all* residues, a contradiction. Therefore s'=s. Varying the other coordinates by unit steps connects all fibers, so each coordinate i has a globally fixed slope s_i in {0,1}. Consequently

\[
H(z)=c+\sum_{i=2}^r s_i z_i\pmod5,\qquad
F(x)=x_1+c'+\sum_{i=2}^r s_i(x_i-x_1).
\]

For r=1 the same conclusion follows directly from Step 1, without any offset coordinates.

**Step 5, eliminate two active slopes.** If distinct i,j both have s_i=s_j=1, choose coordinatewise arcs with +3 changes in positions i and j and +1 changes in every other position. The output difference from the affine expression is 1+2+2=0 modulo five, contradicting the absence of loops. Hence at most one s_i equals 1. With none active, F=x_1+c'. With exactly one active i, F=x_i+c'. Conversely, every coordinate projection followed by a rotation clearly preserves every arc. These are distinct operations, proving the 5r count for every arity. QED.

**Taylor/WNU consequence.** Idempotency F(x,...,x)=x forces c=0. Every idempotent operation is a projection; no projection satisfies the Taylor identities, and no projection of arity >= 3 satisfies the weak-near-unanimity identities. This is a structural classification of the exact constraint language, not a general resource lower bound.

## Independent literature and hardness interpretation

The primary Bang-Jensen, Hell and MacGillivray theorem (SIAM Journal on Discrete Mathematics 1(3), 1988, pp.281-298, doi:10.1137/0401029) says H-colouring for semicomplete H is NP-complete when H has more than one directed cycle. This T has multiple distinct directed 3-cycles, including 0->1->2->0 and 0->3->4->0, so the theorem applies. Independently, the all-arity polymorphism characterization gives the no-Taylor obstruction in the algebraic finite-CSP dichotomy, consistent with the results of Bulatov (2017, arXiv:1703.03021) and Zhuk (JACM 67(5), 2020, doi:10.1145/3402029). Wires (Discrete Mathematics 338(12), 2015, doi:10.1016/j.disc.2015.06.024) supplies a tournament-specific Taylor characterization consistent with this template's strongly connected, non-C3 type.

The complete, explicit reduction and witness audit from undirected C5-colorability to this exact T in /089 remain the quantitative hardness bridge. The strict parsimonious 3-CNF encoding in /091 remains the reverse Boolean bridge. This new result strengthens algebraic identification of the fixed template without claiming a new all-algorithm lower bound.

## Finite computational verification (not proof-kernel checking)

Executed dependency-free Node.js certificate on the exact beat relation:
- Enumerated all 120 permutations of five symbols; exactly five are automorphisms, precisely the rotations.
- Exhaustively evaluated all 5^5=3,125 possible offset tables h for *binary* translation-equivariant candidates F(a,b)=a+h(b-a); exactly ten preserve the binary relation, and each is a rotation of one of the two projections. The preceding symbolic proof, not this enumeration, shows every binary polymorphism is of that form.
- Directly checked every candidate shifted projection against *every* coordinatewise pair of arcs in arities 1 through 5, totalling 50, 1,000, 15,000, 200,000 and 2,500,000 pair checks.
- Checked the 15 ternary shifted projections against idempotent WNU identities; none qualifies.

**Total 2,716,078 assertions, zero failures.** Public source: experiments/tmr/tmr1_t5_polymorphisms094_certificate.js; machine-readable output: results/raw/tmr/2026-11-18_TMR1_T5_POLYMORPHISMS094_RAW.json. Locally executed script SHA-256 e6e56b5cd33f69d162af23a206e8ea16367f04d9c8a51d56bc8e013a7cc98c09; JSON SHA-256 0950f5a098d921e918845c10400a83baef262fe648eef68dab8d5f080651fac7. Exact repo-byte identity is to be checked by Git blob readback. This is computational support; the arbitrary-arity statement has the symbolic proof above.

## Resource and proof-scope audit

For fixed arity r, the complete polymorphism classification is finite and independent of instance size. Evaluating each allowed operation F requires reading a designated 3-bit color and adding a fixed shift; even if r is part of a formal operation description, the map is implementable with O(log r) index storage plus source input access. These operations do not furnish a nontrivial universal local algebraic solver. But their absence also does **not** imply a superpolynomial lower bound for an unrestricted deterministic bit-machine, because a general polynomial algorithm for an NP-complete problem would resolve P versus NP. Exact Fourier-flow, cycle rank, local consistency, modular Gaussian elimination where applicable, bounded-treewidth DP, gadget contraction, and all alternative encodings remain legal.

**Status:** The theorem is a concrete algebraic obstruction and provides independent complexity classification evidence. No new P-vs-NP resolution. No automation changes; preserve the existing TMR-1 role, manuscript, hourly schedule, PR and issue handoff. Independent review, full LaTeX compilation and formal kernel replay remain OPEN.
