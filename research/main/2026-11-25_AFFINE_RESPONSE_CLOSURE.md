# ARC1: Affine-response closure and cooperative guard absorption

**2026-11-25 | Research contribution | PROVED/EXACT at the stated scope; independent mathematical review pending. Universal P=NP: OPEN/BLOCK.**

This note develops FLR-1 and the RT34/RT35 complementarity track. It establishes exact affine response maps, a reachability activation theorem for first-order witness spans, polynomial composition of fixed-degree lifted witnesses over small triangular blocks, and a joint affine-guard Hall criterion. It does not establish a universal polynomial SAT solver.

## 1. Model and exact affine response

All algebra is over F2. For an explicit n-by-n binary matrix M and shift q define

$$S(M,q)=\{x:x_i((Mx)_i+q_i)=0\ \forall i\}.$$

Each owner i permits the three sufficient equations

$$e_i x=0,\qquad M_i x=q_i,\qquad (e_i+M_i)x=1+q_i.$$

For a legal x exactly two tagged alternatives hold, even when coefficient directions coincide or vanish. Those two coefficients span V_i=span(e_i,M_i). For any owner set J, the rank of its satisfied-direction union is at least |J| because it contains the coordinate directions e_i. Rado's independent transversal theorem therefore supplies n independent satisfied equations. Conversely every consistent selection of sufficient equations satisfies the original constraints.

**Theorem 1.** For every M and q,

$$S(M,q)=\{A_T^{-1}(B_Tq+b_T):T\text{ selects one tagged alternative per owner and }A_T\text{ is invertible}\}.$$

The set of selectors T depends only on M. The affine responses f_T(q) can be exponentially numerous; their existence is not a claim of efficient enumeration.

**Corollary 1.** For any target row ell, the bad-shift set

$$\mathcal B_\ell=\{q:\ell x=0\text{ for every }x\in S(M,q)\}=\bigcap_T\{q:\ell f_T(q)=0\}$$

is empty or affine. For any nonempty attainable shift set Q and actual affine basis Q_0 contained in Q,

$$\operatorname{span}\bigcup_{q\in Q}S(M,q)=\operatorname{span}\bigcup_{q\in Q_0}S(M,q).$$

Indeed any linear functional annihilating the right-hand span annihilates every affine response on aff(Q_0), hence on Q. At most n+1 actual shifts suffice. This is a first-order span statement, not equality of the solution sets.

## 2. Exact shift-reachability activation

Let q=q0+Bz parameterize aff(Q), with q0 and the basis shifts actual members of Q. Draw i -> j when M_ij=1. Let R contain all vertices reaching a row with nonzero B_i (including that row); put Z=[n]\R. Then B_Z=0 and M_ZR=0.

**Theorem 2.** If W_Z is the span of S(M_ZZ,q0_Z), embedded on Z, then

$$\operatorname{span}\bigcup_{q\in Q}S(M,q)=W_Z\oplus\mathbb F_2^R.$$

Proof: any legal word restricts to a legal word on the frozen subsystem Z. Conversely every such frozen word extends by setting x_R=0. For any row ell touching R, impose ell*x=1 on the augmented phase coordinates (x,z). Owner i has coefficient space span((e_i,0),(M_i,B_i)). For J the rank is |J|+rank[M_{J,J^c} B_J]. Quotient by the target row reduces rank by at most one. Failure of Hall's inequality would require both zero leakage and containment of the target row in the owner span. Zero leakage makes J closed under outgoing edges with fixed shifts, so J lies in Z; containment contradicts ell touching R. Thus independent representatives of the first two sufficient alternatives can be selected modulo the target by linear/partition matroid intersection. Solve their equations together with ell*x=1. This produces a legal witness at a possibly synthetic shift in aff(Q). Recover a full-rank response selector for that witness by Theorem 1. Since ell*f_T(q) is affine and equals one at the synthetic shift, it equals one at some actual basis shift. The resulting actual witness is verified. Hence no annihilator of the union span touches R, which proves the equality.

The algorithm starts from a supplied actual basis of W_Z. Whenever a coordinate direction on R is not yet spanned, Gaussian elimination finds an annihilator of the current span that is one on that direction. The target construction adds a new independent actual witness. At most n additions are possible. No efficient arbitrary W_Z acquisition is asserted.

In particular a strongly connected block with a genuinely varying attainable external shift has full first-order witness span and a polynomially discoverable actual basis. A downstream shift basis must come from actual downstream witnesses, and those provenance links must be retained.

## 3. Fixed-degree lifted cooperative composition

Let nu_t(y) list all squarefree Boolean monomials of degrees at most t, including the constant. Suppose the downstream words y satisfy a processed subsystem and the next block has shift q(y) affine in y. For an actual basis of the span of nu_t(y), retain its actual words. For each retained word enumerate all legal assignments to the next block and retain a basis of the lifted joint words.

**Theorem 3.** This preserves the complete degree-t lifted witness span at every stage of a block-triangular complementarity system.

Proof: a degree-t polynomial g(y,x) vanishing on the retained extensions satisfies g(y,f_T(q(y)))=0 for every basis word y and each full-rank response T. The composition is a Boolean polynomial of degree at most t because f_T and q are affine. It therefore vanishes on every downstream word by the basis property. Theorem 1 accounts for every extension. Thus every annihilator of the acquired lifted span is an annihilator of the full lifted span. The reverse inclusion follows from actual witness provenance.

For supplied blocks of size O(log N), fixed t, and explicit input length N, local enumeration and Gaussian basis maintenance cost polynomial time: at most sum_{j<=t} binom(n,j) actual witnesses are retained and each is extended by polynomially many local candidates. The assertion does not extend to growing t without a separate bound. For d additional rank-two avoidance constraints, their satisfaction indicator has degree <=2d; fixed d gives a polynomial terminal under the stated block-size hypothesis. A degree-t basis can test a single supplied degree-t target; first-order bases alone cannot enforce arbitrary joint guards.

## 4. Joint guard absorption

Suppose attainable shifts fill the affine space q0+im B and let Hx=b be a consistent additional affine guard. Denote its row span in the augmented (x,z) coefficient space by P. For each owner set J define V_J as the span of the two augmented observation rows per owner, and

$$\lambda(J)=\operatorname{rank}[M_{J,J^c}\ B_J].$$

Eliminating the J-coordinate columns using (e_i,0) gives dim V_J=|J|+lambda(J). Consequently,

$$|J|-\dim((P+V_J)/P)=\dim(P\cap V_J)-\lambda(J).$$

**Theorem 4.** If lambda(J)>=dim(P intersect V_J) for every J, then every consistent guard RHS on P has a legal extension. Matroid intersection checks all inequalities simultaneously by finding a full independent transversal modulo P. Gaussian elimination solves the chosen sufficient equations and the guard together. Conversely failure of the Hall test means this sufficient independent-extension mechanism declines, not UNSAT.

If the shifts are generated by another subsystem, this terminal requires polynomial witness lifting for its chosen shift; mere fullness of the affine hull is insufficient. Guards involving downstream quantities other than the modeled shift must be accounted for separately. Under these explicit premises all acquisition, rank tests, row operations and reconstruction are polynomial in the encoded input. Same-execution peak space is polynomial, and cumulative memory is bounded by (T+1)S under the project's conventional charged ledger.

## 5. Universal obstruction: arbitrary 3-SAT can reside in the guards

Given a 3-CNF, introduce three selector bits c_ij per clause and one reference bit t=1. For a literal ell_ij=x_v+s with s in F2, impose

$$c_{ij}(x_v+(1+s)t)=0,\qquad c_{i1}+c_{i2}+c_{i3}=1.$$

Give source bits and t zero complementarity rows. All selector rows read source/reference bits only, so M^2=0. Given a satisfying source word, choose exactly one true literal per clause and set its selector to one. Conversely an odd selector sum ensures at least one selected true literal per clause. This is a polynomial-size explicit reduction with exact source projection and witness lift. The unguarded legal span is full (all coordinate unit words are legal). Thus acyclicity, full first-order span, and the availability of affine response maps do not by themselves solve the guarded conjunction. This is an NP-completeness observation for the guarded class, not a lower bound excluding P=NP.

## 6. Executed evidence

The original deterministic Python audit uses seed 20261125. Recorded counts are: 4,804 response-set comparisons; 4,234 bad-shift affine checks; 570 response geometries; 240 reachability instances; 946 target lifts; 120 lifted-block instances; 7,432 guard-cut checks over 180 joint-guard instances; 398 joint-guard witnesses; 6,464 closed-subset pivot checks over 119 valid pivots; 70 guarded-source reductions, 1,920 source assignments, 1,310 lifts. All final assertions passed.

Activated directed cycles: dimensions 8,16,32,64; each initial zero-shift span has rank one, each activated span has full rank, and the corresponding actual basis contains 8,16,32,64 witnesses. Recorded times (seconds): 0.0031, 0.0402, 0.9403, 30.614. Total recorded time 32.4194 seconds. The largest test exceeded the approximately 30-second per-stage guideline. These are historical finite counts, not a measured worst-case exponent or a complete native compiler/solver audit.

The initial implementation incorrectly required one rank-increasing witness to span a specific coordinate immediately. The corrected acquisition loops until inclusion holds, charging each independent addition. Pivot tests check equality of closed subsets under valid principal pivots, not the number of legal-word transports. Reference brute force is used only for finite checks and bounded local kernels, not in the general activated-block construction.

Reproduce: run python3 experiments/affine_response_closure_audit.py (writes the adjacent JSON; elapsed times may differ).
- Code commit: [59b6204](https://github.com/j15marti/pnp/commit/59b6204a34744abe96c06dd515a1c44edf3ac7bf)
- Recorded result commit: [e5bc824](https://github.com/j15marti/pnp/commit/e5bc824db2bfe09e2a963d173352b4ed3f1bda4f)
- SHA-256 of local source: eed46f1cafc84d0769425800f40ac4061e063b0afd6ad58c425bca6b3ad7d66c
- SHA-256 of recorded result: 6b8c1e479512f52190262ff4e7d2511c52e6795abc9f6b0013190708b3edc6be

## 7. Remaining proof obligation and status

The strongest integration target is universal guard-deficiency contraction: on every satisfiable normalized residual, obtain a polynomially searchable, source-correct combination of actual shift acquisition, exact projections, affine restrictions, matching/flow, and joint compatibility that either reaches a polynomial terminal or contracts a well-founded global resource potential with polynomial aggregate work. No explicit exponent is required, but uniform existence of some fixed exponent is essential. Theorem 4 identifies an exact Hall deficit to investigate; failure of that sufficient rule is not evidence of unrestricted hardness.

DISJ: exact restricted equivalences and both-label source controls; no universal coverage.
Relativization/Natural Proofs/algebrization: no unrestricted separation or barrier escape claimed.
DTISP: simultaneous polynomial time and space only for admitted modules with all acquisition and lifting hypotheses; no forbidden-region claim.
Deterministic configuration: no unrestricted configuration-count lower bound.
Universal SEM/CLOSE, U-PROGRESS and unconditional COST remain OPEN. No formal proof-assistant verification, full repository preflight, public-proof release, or shared-manuscript replacement in this publication.

## References and project dependencies

1. RT34, reference-free complementarity and implicit affine-span PIT: https://github.com/j15marti/pnp/commit/45819df1cd34821bac223b428cf365f9748c62af
2. RT32, deterministic sign-class acquisition: https://github.com/j15marti/pnp/commit/bcc0b36d34d9c5413cb33f7a1eeb26d2b3095fb6
3. A. Schrijver, Combinatorial Optimization, Chapter 41 (matroid intersection and independent transversals).
4. A. Chatterjee, S. Ghosh, R. Gurjar and R. Raj, Characterizing and Testing Principal Minor Equivalence of Matrices, ECCC TR24-150: https://eccc.weizmann.ac.il/report/2024/150/ . Principal-minor equality is not the required general support-containment theorem.

Publication archives the existing research and its existing evidence; no new literature theorem or numerical experiment is claimed by this note. All agents remain paused.
