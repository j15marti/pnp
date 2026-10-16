# PROOF-TRANSPORT: ALLFIELD-SHIELD-RETRACTION1
Date: 2026-10-16 21:37 Asia/Seoul. Status: restricted PC/PCR theorem, finite symbolic audit PASSED; external review pending; P versus NP OPEN.

## Pre-search proposals
ONE-BRANCH-SHIELD-PC; COMPILER-RETRACTION; CERTIFICATE-NO-FORCING; SPREAD-LIFT-ACCOUNTING. Then searched project chats/files, GitHub, Google Drive and primary literature. Full local report and executable audit are retained in the research package.

## Closed proof interface
For arbitrary proper 3-CNFs A,B on disjoint variable sets, let O(A,B) be the actual proper OR3 shield, and T the actual 72m-variable/96m-clause exact-(2,2) selector compiler (not the 24v/32v balanced occurrence compiler). Write J=T(O(A,B)), q=m_A+m_B. It has exactly 144q variables and 192q clauses.

THEOREM (any field K): From any degree-D ordinary PC or PCR refutation of J, derive an ordinary PC refutation of A in degree <= max(D,3). Hence if A and B are UNSAT, deg_PC,K(J)>=deg_PC,K(A) and deg_PCR,K(J)>=deg_PC,K(A).

Proof: Set OR-selector s=0, A-split witness y_C=not(a), B-split z_C=0 and all B variables 0. Each A pair maps to an A clause plus a Boolean axiom consequence; B pairs vanish. Retract T by setting its own selector t=0, first witness u_C=not(first literal), second witness v_C=0, clone variables equal to their parent, and all 15-variable Q gadget variables to zero. Every final target variable maps to 0,1,x,or 1-x; every target clause maps to a source A axiom or a Boolean consequence of degree <=3. Each target Boolean axiom maps to a source Boolean consequence of degree <=2. For a source PC line P, multiplying by a target variable projected to 1-x is simulated as P-xP using one ordinary variable multiplication and one linear combination; degrees do not rise. PCR complementary rails map to 1-rho(x). Same *complete original target realization* is used for all steps, with no oracle and no uncharged preprocessing.

## Quantitative all-field benchmark
Take a 6-regular graph G with h vertices for which the Conneryd/de Rezende/Nordstrom/Pang/Risse all-field 3-colouring PC-degree theorem holds. Standard Boolean 3-colouring has h ternary and 12h binary clauses. Properize each binary D as (D or z_D) and (D or not z_D), giving A_G with 25h proper 3-clauses and 15h variables. Project z_D=0; the adapter (1-a)(1-b)(1-c)=-(a+b+c-1)+ab+ac+bc-abc costs degree <=3. Let B0 be the eight-clause unsatisfiable 3-variable full signed cube. Then J_G=T(O(A_G,B0)) has N=3600h+1152 variables and M=4800h+1536 clauses. All-field PC/PCR degree is Omega(h); expanded-monomial PC/PCR size is 2^Omega(h)=2^Omega(N) by the established size-degree theorem. Indexed binary input length L=Theta(h log h), giving 2^Omega(L/log L). This is explicit certificate hardness, NOT unrestricted runtime hardness.

## Adversarial correction
A linewise O(S) expanded-monomial projection under this signed selector map is FALSE. A single target monomial y_1...y_k can map to product_i(1-x_i), with 2^k expanded monomials. Realized k=2,4,8 inside the actual compiler: 1->4,16,256. Degree remains <=k. Thus degree hardness is transported directly; size hardness must be inferred from the *target's own* PC/PCR size-degree theorem, not a claimed O(S) literal projection.

## Independent audit and scope
A clean integer-polynomial implementation reconstructed the full shield, doubled signed occurrence list, all clone cycles, exact Q gadget and 72m/96m counts. It checked 20,544 target clause projections and 15,408 Boolean-axiom projections, including a 10,368-variable K4-colouring compiled target; only two surviving source axiom images per A clause. 428 random ordinary-PC inference commutations, 32 exhaustive small-case canonical assignment extensions and 1,834 colour-adapter modular evaluations in characteristics 2,3,5,7,11 passed. Corrupting the shield selector produced invalid source clauses in all four cases. All symbolic identities were checked over Z, thus are characteristic independent.
Code SHA256: 2439a3378f3d8a5b153f1997163563f17a136939170d303e3d58c9ffed216705
JSON SHA256: 82f5f656a115a2dd93757d6d69baa126df4cc35b30673c0fd4e6c9462e561521

## Interfaces not promoted
CP22LIFT1 and OR3-SYNCP1 are syntactic integer Cutting Planes with coefficient/rounding charges, not PC or SAT runtime. Historical C and universal U regularizers differ from selector T. GF(2) short proofs of shielded cubic Tseitin persist, but do not undermine hard non-affine graph colouring. SoS over reals is distinct. RUP-only logged solvers permit Resolution extraction but arbitrary RAT/DRAT or parity solvers do not. ROUNDINGSQUEEZE5 requires a binary triangle DAG and one same saved row for all outputs. Polynomial gadget indexed search has a polynomial communication upper ceiling. A hypothetical global P-time SAT decider need not emit any fixed calculus: its own verifier can check a zero-bit UNSAT certificate by running the decider. NO unrestricted decider-to-proof bridge, and P vs NP remains OPEN.

References: Conneryd et al., Graph Colouring Is Hard on Average for Polynomial Calculus and Nullstellensatz (FOCS 2023; arXiv:2503.17022); Impagliazzo-Pudlak-Sgall, Computational Complexity 1999; Miksa-Nordstrom, CCC 2015; internal PC22_ALLFIELD1/CP22LIFT1/OR3-SYNCP1/PC-SHIELD-ESCAPE6/RS5REVIEW1.

Handoff: rigorous next scope is charged explicit certificate-emitting algebraic solvers. Check algorithm-to-PC materialization and break it with alternate representations. Do not infer arbitrary polynomial-time SAT lower bounds.