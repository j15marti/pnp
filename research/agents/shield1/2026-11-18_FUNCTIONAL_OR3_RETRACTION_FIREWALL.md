# SHIELD1 2026-11-18: Functional OR3 shield, counting and retraction firewall

**Status:** PROVED/EXACT for stated syntactic results (independent review pending), COMPUTATIONAL small-instance audit, arbitrary SAT-decider lower bound OPEN. P versus NP remains OPEN. This is additive SHIELD1 work; no active TMR-owned manuscript or retired tracker is altered.

## Earlier work and attribution

Reuses, without claiming originality, the proper OR3 gadget and proof translations in SHIELD1 OR3-PROJECTION-AUDIT1 (2026-10-15), SHIELD1 OR-BIDIRECTIONAL1 (2026-10-15), OR3-SYNCP1 (2026-10-16), and the three-variable seven-clause unique anchor already used in LSPV-4 PRIORITY-HORN-PARSIMONY67 (2026-10-24). The new scoped additions are a *two-way literal-retracting, selector-functional* shield, an exact counting equation, a constant-only projection impossibility, and an explicit nested-count failure.

## 1. Original shield, exact semantics and model counts

Let A(X),B(Y) be nonempty proper 3-CNFs on disjoint variable sets, q=m_A+m_B, and each A clause C=(a∨b∨c), B clause D=(d∨e∨f). Give each clause a private variable y_C or z_D and introduce selector s. Define

O(A,B)= AND_C [(s∨a∨y_C) AND (¬y_C∨b∨c)] AND_D [(¬s∨d∨z_D) AND (¬z_D∨e∨f)].

For any fixed source assignment (α,β):

  Exists (s,y,z) O(α,β,s,y,z)  iff  A(α) OR B(β).

The output is proper, clause-distinct, with exactly 2q clauses and v_A+v_B+q+1 variables. For exact model counts, interpret signed literal evaluations as bits and put t_C=b∨c, t_D=e∨f. Then the number of auxiliary extensions at fixed α,β is

  M_O(α,β) =
    PRODUCT_C(a_C+t_C) PRODUCT_D(1+t_D)
    + PRODUCT_C(1+t_C) PRODUCT_D(d_D+t_D).

**Proof.** At s=0 a left private pair has a+t possibilities for y; a right disabled pair has 1+t possibilities for z. At s=1 interchange sides. Private variables are independent. Summing the disjoint selector cases gives the formula. A branch has an extension iff its selected source is true.

## 2. Functional strict-3CNF OR shield

Introduce three globally fresh variables u,v,w. Let H(u,v,w) consist of the seven distinct proper 3-clauses that exclude each of the seven triples other than (1,1,1). Thus H has precisely one model. Define O*(A,B) by H and, for each A clause, four proper 3-clauses

  (s∨a∨y_C), (¬y_C∨b∨c),
  (¬y_C∨¬s∨¬u), (¬y_C∨¬a∨¬u),

and, for each B clause, four proper 3-clauses

  (¬s∨d∨z_D), (¬z_D∨e∨f),
  (¬z_D∨s∨¬u), (¬z_D∨¬d∨¬u).

**THEOREM (PROVED/EXACT).** O* has 4q+7 proper distinct clauses, v_A+v_B+q+4 variables, and for each fixed α,β:

  #AuxExt(O*,α,β) = 1[A(α)] + 1[B(β)].

Therefore #SAT(O*) = 2^(v_B) #SAT(A) + 2^(v_A) #SAT(B), and O* is SAT iff A OR B is SAT.

**Proof.** H fixes u=v=w=1. The first, third and fourth clauses of each left group enforce y_C iff (¬s AND ¬a); on the right they enforce z_D iff (s AND ¬d). Thus every source valuation plus s has exactly one assignment to all auxiliaries. With s=0 the second clause of each left group reduces to a∨b∨c, and all right groups are true. With s=1 interchange. All 3-variable supports are distinct within clauses; private y_C,z_D prevent repeated clauses, including when input source clauses repeat.

The old first two clauses remain an actual subset of O*. Hence every *forward* general-Resolution upper refutation bound for O continues to hold for O*, even though O* has stronger auxiliary constraints.

## 3. Exact two-way proof retractions and bounds

On O and O*, define:
  rho_A: s=0, y_C=¬a_C, z_D=0;
  rho_B: s=1, y_C=0, z_D=¬d_D.

On O* also fix u=v=w=1. Both leave all source X,Y variables unchanged. Every input clause maps either to a source clause of the selected leaf or to a Boolean tautology. The nontrivial image of each selected source group is exactly its original 3-clause. These are **literal/constant substitutions**, NOT 0/1 restrictions.

For UNSAT A,B, general Resolution substitution closure implies:

  max(I(A),I(B)) <= I(O*) <= I(A)+I(B)+q+1
  max(W(A),W(B)) <= W(O*) <= max(W(A),W(B))+1,

where I is minimum genuine inference count and W is minimum possible refutation width. The upper proofs use only old groups in O*. Earlier SHIELD1 PC/SoS-degree and CP lower transports continue with their own assumptions, not as a statement about all proof systems. In particular, arbitrary regular-Resolution size and explicit-monomial PC size are NOT transferred without a separate closure theorem. General proof lower bounds on one common OR instance combine by MAX across leaves, never automatically by SUM.

## 4. NEW strict-width constant-restriction firewall

**THEOREM (PROVED/EXACT, exact syntactic scope).** Suppose A(X) and B(Y) have at least one proper 3-literal clause each and X∩Y is empty. There is no proper 3-CNF F(X,Y,Z) admitting two *auxiliary-only Boolean constant restrictions* r_A,r_B such that, after dropping true clauses but keeping the remaining literal clauses as written, F|r_A is exactly A and F|r_B is exactly B.

**Proof.** Select a 3-literal clause C of A. Under r_A it must arise from an original clause C' of width at most three. Deleting literals cannot create three source literals, so C'=C and contains no auxiliary variable. An auxiliary-only restriction r_B cannot affect C. Thus C survives as a non-tautological X-clause in F|r_B, which cannot equal B(Y). Contradiction.

**Limitations:** This no-go is for clause-by-clause exact retractions, not arbitrary semantic equisatisfiability, additional source pinning, width-4 clauses, or proof transformations involving derivations. It establishes why claiming the SHIELD1 maps are mere constant restrictions is unsound. Buss and Yolcu (arXiv:2402.15871) show general regular Resolution is not substitution closed, so the distinction matters.

## 5. Selector parsimony and nested composition barrier

If a source assignment satisfies both A and B, any shield preserving the two distinct selector branches has at least two auxiliary extensions, one with s=0 and one with s=1. Hence a two-branch retracting shield cannot be globally *parsimonious for Boolean OR* even if it has exactly one extension for each active branch. This is a direct two-selector-value argument.

Let Ψ=O*(O*(F1,F2),O*(F3,F4)). Put q_L=m1+m2, q_R=m3+m4, Q=q_L+q_R. Then Ψ has exactly 16Q+63 clauses and sum_i v_i+5Q+26 variables. For any fixed assignment to ALL four source-leaf variables, write b_i=1[Fi is true]. The exact number of auxiliary extensions is

  #AuxExt(Ψ) = 2^(q_R+4)(b1+b2) + 2^(q_L+4)(b3+b4).

**Proof.** With root selector left, its new functional aux have one extension for each satisfying assignment to the left child's q_L+4 internal variables. The entire right child's q_R+4 internal variables are unrestrained because its clauses are inactive at the root. Thus the left contribution is (b1+b2)2^(q_R+4); swap sides for the other branch.

In particular four single-clause leaves and exactly one satisfied leaf already give 64 extensions. Local one-branch functional uniqueness does NOT compose into portfolio-wide uniqueness.

## 6. Exact encoding and boundary of hardness transfer

For canonical dense source variable identifiers, use gamma-encoded positive counts and signed literals of width 1+ceil(log2(v+1)). Original O has bit size

  |gamma(v+1)| + |gamma(2q+1)| + 6q(1+ceil(log2(v+1))),
  v=v_A+v_B+q+1.

Functional O* has bit size

  |gamma(v*+1)| + |gamma(4q+8)| + 3(4q+7)(1+ceil(log2(v*+1))),
  v*=v_A+v_B+q+4.

If all declared source variables actually occur, v_A+v_B<=3q, and both bit lengths are Θ(q log(q+2)). Dense canonical input parsing and emission use O(q+v_A+v_B) word actions and Θ(output bits) emitted bits; sparse labels, arbitrary identifier canonicalization, sequential bit-machine head movement, and any source authentication require their actual additional costs.

For any proof system P with proved source-preserving literal-substitution translator g_P, the valid inheritance statement for an OR portfolio Ψ is

  size_P(Fi) <= g_P(size_P(Ψ), |Ψ|),

for every leaf i, *on this one actual Ψ*. This is NOT a lower bound on an arbitrary SAT decider's runtime on Ψ.

**Strongest OPEN bridge:** Show a same-input, globally valid, fully charged transport from arbitrary polynomial SAT-decision traces to a specified lower-bounded proof system, surviving unrestricted algorithms and alternative representations. A correct global decider may recognize canonical OR shields whose leaves are cubic Tseitin parity formulas, solve each leaf by Gaussian elimination, and fall back to exhaustive search on all unrecognized inputs. This is polynomial on those shield instances despite inherited exponential general-Resolution hardness. It refutes any unconditional polynomial trace-to-Resolution translator, not P=NP. No P-vs-NP separation is obtained.

**Mandatory gates:** DISJ PASS for exact existential OR; relativization OPEN for all-decider bridge; simultaneous DTISP and deterministic configuration counting NOT APPLICABLE for finite gadget proof and OPEN for arbitrary-machine consequences.

## 7. Reproduction and reference record

Local independently executed standard-library Python enumerator tested three signed source-pairs q=2,3,4, all 64 fixed source assignments for each (192 total), exhaustive original and anchored functional auxiliary assignments, source-level OR, counting identities, properness, and both exact retractions. It also ruled out all eight auxiliary-only constant assignments for recovering either single-clause source exactly. 774 assertion-counted checks, no failures. Original total model counts (280,380,576); functional (112,104,96). Script SHA256 0946ce63c06f5e7b52fe56126eb63b6e5649435e011b03dd9cb8236ad57c8f68. JSON SHA256 32b8e54c02c4fce8cf548840ba171d101e3766328257d8ff75d3b3cecf3eec95. These are finite computational corroboration; the proof claims above are symbolic. No native TMR preflight or compilation was claimed.

**Next load-bearing target:** arbitrary-decider-to-specific-proof-system same-instance transport or a rigorous barrier ruling out a clearly defined class of such transports.

### Relevant primary literature
1. Ben-Sasson and Wigderson, *Short Proofs Are Narrow: Resolution Made Simple*, JACM 48 (2001): https://eccc.weizmann.ac.il/eccc-reports/1999/TR99-022/
2. Filmus, Hrubes and Lauria, *Semantic Versus Syntactic Cutting Planes*, STACS 2016: https://doi.org/10.4230/LIPIcs.STACS.2016.35
3. Buss and Yolcu, *Regular resolution effectively simulates resolution*, arXiv:2402.15871: https://arxiv.org/abs/2402.15871
4. Cook and Reckhow, *The Relative Efficiency of Propositional Proof Systems*, JSL 44 (1979): https://doi.org/10.2307/2273702
