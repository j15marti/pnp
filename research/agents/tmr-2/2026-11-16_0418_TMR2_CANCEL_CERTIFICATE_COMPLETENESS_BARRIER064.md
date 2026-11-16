# TMR-2/064: cancellation-aware source certificate and the coNP completeness barrier

Date: 2026-11-16, America/Los_Angeles, approximately 04:18 PST. Owner: TMR-2 / PNP Information Necessity, Track A. Authority: research/coordination/2026-11-15_END_TO_END_AGENT_MANUSCRIPTS.md. Scientific status: **PROVED/EXACT RESTRICTED** for the fully specified algorithm and **KNOWN-COMPLEXITY-BASED PROVED/EXACT** for the elementary coNP-completeness argument below. External independent mathematical review **OPEN**; finite tests **COMPUTATIONAL**. **P versus NP OPEN**.

## Candidate, quantifiers, falsifiers, and integration

Named dependency: **D2-CERTIFIED-DEGREE-COMPRESSION**, continuing /063. Candidate: for *every fully authenticated* \`p d2poly\` circuit source using genuine \`I,N,A,O,P\` gates (no early \`E/X\` gates, hence constructed bilinear dimension \(d=0\)), construct a deterministic, polynomial-cost, *sound but incomplete* cancellation certificate. This must accept some sources with intermediate syntactic degree \(>2\) when their source-produced root polynomial is certified quadratic, and return the exact number of accepting **original** input assignments. Reject high-degree sources as **OUTSIDE THE CERTIFIED CLASS**, not UNSAT. Complementary impossibility target: deciding actual ANF degree \(\le 2\) for unrestricted Boolean DAGs is coNP-complete, including this gate vocabulary, so no universal efficient complete semantic certificate follows without an NP-level breakthrough.

Four pre-search falsifiers: (1) XOR cancellation or interning changes pointwise output or loses original-input multiplicities; (2) high-degree gate expansion or unbounded re-materialization violates the same-machine resource ledger; (3) a surviving atom of claimed degree two still depends on an uncharged high-degree atom; (4) the degree-hardness reduction or the eight-evaluation third-derivative certificate fails. Source comparison included the complete owned /063 paper and original /063 report, executable and raw data, TMR-4/066 draft and TMR-5 latest issue #3 reports, and the primary algebraic-degree references listed below. A local checkout was absent; preflight was not run.

Pipeline, with explicit all-length semantics:
canonical ASCII source bytes and complete authentication -> source DAG topological order and input-coverage proof -> normalized parity-vectors and hash-consed AND atoms with paid attempted contractions -> live-atom marking and sufficient degree certificate -> packed quadratic polynomial for the *actual output* -> exact integer quadratic Gauss elimination -> \(\#\mathrm{ONE}\), SAT=(count>0), and output. Every step is uniform and source-derived. If malformed, reject as malformed; if authentically outside the certificate, return OUTSIDE, without a SAT/UNSAT assertion. No semantic oracle, truth-table advice, or equivalence test is used.

## Exact source grammar

Use the authentic /063 ASCII grammar \`p d2poly n a b g root\` with \(n=a+b,\ a,b\ge1,\ n\le2g\), precisely \(g\) id-labelled records in arbitrary textual order, one trailing LF, safe canonical decimal numbers and exactly one root. All original \`I\` inputs and all source records must be reachable by DFS, and the dependency DAG must be acyclic. In this *restricted subgrammar*, \`I id j\` reads original \(z_j\), \`N id u\` is NOT, and \`A,O,P id u v\` are AND, OR, XOR. There are no \`E\` or \`X\` early gates, so this is the \(d=0\) subcase of the previously authenticated source language. Syntactically noncanonical sources are INVALID; unsupported authentic extensions are OUTSIDE the local grammar. Source cost \(N\) is the entire encoded byte length, not just the number of gates.

## Theorem 14: polynomial-time constructive sound certificate

Work in \(\mathcal R_n=\mathbb F_2[z_0,\ldots,z_{n-1}]/(z_i^2-z_i)\).
After authentication, map each genuine source gate \(t\) to a parity vector \(V_t\) over one constant coordinate and canonical *atom identities*. The atoms are the distinct original-input leaves \(I(j)\) and any newly created canonical AND-of-parity-vectors \(\mathsf A(U,V)\). A parity vector represents the XOR of the indicated atoms. Each stored atom has exactly one identity, but every actual source gate is parsed and accounted for even when later canceled. In particular, different source gates that construct the **same ordered-canonical operand pair** share an atom; the operands themselves are full parity vectors, not truth tables.

Construct \(\operatorname{AND}(U,V)\) with the following exact Boolean identities:
\[
0\land U=0,\quad 1\land U=U,\quad
U\land U=U,\quad U\land(1\oplus U)=0.
\]
For all remaining inputs, order the operand vectors, look up their pair in the paid atom dictionary, and create one AND atom if absent. Gate transitions are
\[
V_I=[I(j)],\quad V_N=1\oplus V_u,\quad
V_P=V_u\oplus V_v,\quad V_A=\operatorname{AND}(V_u,V_v),
\]
\[
V_O=V_u\oplus V_v\oplus\operatorname{AND}(V_u,V_v).
\]
These formulas use **integer bitmaps with XOR**, not an uncharged canonical Boolean-function oracle. The dictionary may be implemented by deterministic list scan rather than expected-time hashing.

Assign degree 1 to raw \(I(j)\). Assign each AND atom the clamped value
\(\min(3,\deg U+\deg V)\), where \(\deg U\) is the maximum certified degree of its live atom coordinates, with constant degree zero. The output degree is computed from \(V_{\mathrm{root}}\), not from the maximum syntactic degree of all original gates. If the output certified degree \(\le2\), recursively mark only the atom dependencies present in its vector. Every marked atom has degree \(\le2\). Substitute the authentic input monomials into the **retained normalized atom graph**, evaluating AND via idempotent polynomial multiplication and XOR by coefficient parity. A polynomial degree-\(\le2\) coefficient vector of \(1+n+\binom n2\) bits suffices per live atom. This produces \(p(z)\in\mathcal R_n\) satisfying \(C(z)=p(z)\) for every original assignment by induction on authentic gates and retained atoms.

Set \(H(p)=\sum_z(-1)^{p(z)}\). Repeatedly select a quadratic pair \(z_i z_j\) and write
\(p=z_i z_j+z_i A(t)+z_j B(t)+R(t)\). The elementary exact identity
\[
\sum_{z_i,z_j}(-1)^p=2(-1)^{R(t)+A(t)B(t)}
\]
eliminates two variables, preserving quadratic degree. For the residual affine expression the signed sum is zero if a nonzero linear term remains, otherwise a signed power of two. Finally
\[
\boxed{\#C=(2^n-H(p))/2}
\]
is the exact count over the \(n\) **original input identities**. Eliminated gates or irrelevant variables do not change the input measure or create auxiliary multiplicities. SAT is YES exactly when this integer is positive.

**Correctness:** each local rewrite is an identity on \(\{0,1\}\); interned atoms have equal **formal expressions**, not guessed equal functions. Therefore every source gate, including high-degree gates later canceled, preserves its pointwise value. Marked atoms are topologically earlier than their consumers; their certified degrees bound their Boolean quotient polynomial degrees. Neither a false low-degree certificate nor a free oracle is introduced. The quadratic Gauss identity proves the output. A rejected certificate is not a lower bound on another algorithm and is not evidence of UNSAT.

**Cost partition and SAME execution:** \(g\le N,\ n\le2g\). There are at most \(n+g\) atom identities (indeed at most one new atom per original leaf or AND/OR gate), and at most \(g\) source parity vectors. All are bitmaps of \(O(g+n)\) bits; the pair keys and full original source/addresses, topological data, failed dictionary comparisons, and the retained normalized graph cost \(O(N^2)\) bits. At most \(g\) simultaneously stored quadratic vectors of \(O(n^2)\) bits use \(O(N^3)\) bits total. The character elimination uses an additional \(O(n^2)\) bits; signed count and intermediate coefficients have \(O(n)\) bit length; output uses \(O(n)\) bits. No exponential-size table, formula unrolling, or preloaded source objects are retained. The **one** locally headed deterministic multitape realization performs \(O(N)\) source reads plus polynomial validation, \(O(g)\) atom creations with up to \(O(g)\) dictionary probes each, \(O(N)\)-bit key comparisons, \(O(g)\) live-polynomial evaluations on \(O(n^2)\)-bit coefficient vectors, at most \(n/2\) quadratic eliminations and exact bit arithmetic. A deliberately loose bound covering local tape seeks/copies, lookup failures, all buffers and output is
\[
\boxed{T(N)=O(N^{12}),\quad S_{\rm peak}(N)=O(N^3)}
\]
for authentic sources accepted by the certificate; validity and OUTSIDE detection are polynomial too. The physical bit-machine is analytical, **not** an executed microtrace. A single execution underlies both upper bounds, and no parallel-network span is substituted for total work.

## Theorem 15: unrestricted degree-\(\le2\) certification barrier

Let \(\mathrm{DEG2}=\{\langle C\rangle:C\text{ is a well-formed Boolean circuit and }\deg_{\mathbb F_2}(C)\le2\}\), where the degree is that of its **unique square-free ANF**, not the syntactic gate-degree bound. Then **DEG2 is coNP-complete** under ordinary polynomial-time many-one reductions. The statement already holds for authentic gate DAGs built from input, AND, OR, NOT (and optionally XOR), with no early bilinear interface.

Membership: \(\deg C>2\) iff there exist three distinct original input coordinates \(i,j,k\) and a context assignment \(y\) to the other coordinates for which
\[
\Delta_i\Delta_j\Delta_k C(y)
=\bigoplus_{\epsilon\in\{0,1\}^3}
 C(y\oplus\epsilon_i e_i\oplus\epsilon_j e_j\oplus\epsilon_k e_k)=1.
\]
A nondeterministic certificate specifies \(i,j,k,y\); verify it by **eight** circuit evaluations. This follows by taking derivatives of the unique square-free ANF: a third derivative is nonzero iff some monomial has support containing that triple. Hence the complement of DEG2 is in NP.

Hardness: for any 3CNF \(\varphi(x)\), construct its actual polynomial-size shared Boolean evaluator \(G_\varphi(x)\), introduce three **fresh** original input bits \(u,v,w\), and output
\(C_\varphi(x,u,v,w)=G_\varphi(x)\land u\land v\land w\).
If \(\varphi\) is unsatisfiable, \(C_\varphi=0\), hence degree zero. If satisfiable, the exact derivative \(\Delta_u\Delta_v\Delta_w C_\varphi(x)=G_\varphi(x)\) is nonzero, hence degree \(\ge3\). The construction is polynomial, root-reachable and source-authentic, with no oracle; any unused named SAT inputs may be removed before emitting the source, and the source can use \(a+b=n,\ n\le2g\). Thus 3UNSAT reduces to DEG2 and DEG2 is coNP-hard. These are unconditional *complexity classifications*, not a proof that P differs from NP. A polynomial-time **complete** DEG2 recognizer for every such input would imply P=NP. This barrier explains the need for a **sound incomplete** certificate and invalidates any claim that structural cancellation alone solves unrestricted SAT.

## Executed reproducibility and hostile controls

Exact executable revision \`TMR2_CANCEL_CERT064_v1\`; deterministic xorshift seed **20261116**; code \`experiments/tmr/tmr2_cancel_degree_e2e064.js\`; raw \`results/raw/tmr/2026-11-16_0418_TMR2_CANCEL_CERT064_NODE_RAW.json\`. A hosted V8 run actually executed the complete self-contained source and returned **85 accepted cases**, **84 independent exhaustive original-assignment comparisons**, **2 rejection controls**, **85 quadratic character calls**, **zero final failures**. Exact output includes 6-input shared-cancellation count 16, eight-input separately constructed identical high-cubic count 64, mixed high-OR cancellation count 96, 64-input/193-gate cancellation count \(2^{62}\), and a contradictory source with count zero and certified degree zero. The 64-input source has 128 constructed atoms but only three live atoms, without expanding the high-degree structure. The two initial in-memory harness drafts failed on an overly high-degree *test expectation* and a generated-source input-coverage mistake; those harness mistakes were fixed before the final published run and are not mathematical counterexamples. No claim is made that every arbitrary cancelled Boolean circuit is recognized, and the finite code only exercises the \(d=0\) case.

DISJ sanity: **PASS restricted**. DISJ4, \(\bigwedge_i(\neg x_i\lor\neg y_i)\), is cheap 2CNF with \(3^4=81\) satisfying assignments, but its general raw-only conjunction lies outside the present low-degree certificate. OUTSIDE is not UNSAT or a lower-bound witness. Relativization: **PASS local** algebraic upper construction, **OPEN** unrestricted NP transfer (BGS, algebrization and Natural Proofs remain relevant). Simultaneous DTISP: **PASS restricted** for the one explicit implementation and **OPEN** for any all-machine resource necessity. Deterministic configuration counting: **PASS as upper-bound safeguard only**, \(T\le2^{O(S+\log N)}\) for fixed deterministic halting machines with the stated heads, no work lower bound or randomized/quantum claim. Horn, affine/Gaussian, 2SAT, bounded treewidth, equality, autarky, products, padding, auxiliary encodings, unique-selector, unique-solution rank one and compact alternative circuits are all legal; these were **not exhaustively tested in /064**. Integer Fourier versus characteristic-two rank and randomized isolation do not appear as free steps. /341 FAIL full UNSAT, /386 RESTRICTED.

## TMR-4 handoff and one next dependency

**D2-CANCEL-NORMALFORM-TRACE** is the execution-sensitive invariant: authentic source bytes and all gate IDs/wires -> parsed predecessor/cycle/coverage state -> each gate's parity bitmap and every actual AND attempt -> canonical ordered operand key, cache hit/miss, idempotence/complement/constant contraction -> retained atom graph, source-preserving semantic identity and clamped degree -> live mark and retained quadratic coefficient vectors -> exact pair elimination state -> integer H, normalization, original count/output. Allowed charged transitions: READ_SOURCE, VALIDATE, DFS, XOR_BITMAP, AND_LOOKUP_HIT/MISS, CREATE_ATOM, CONSTANT/IDEMPOTENT/COMPLEMENT, PRUNE_AFTER_CERT, COEFFICIENT_BUILD, COEFFICIENT_MULTIPLY, QUADRATIC_PAIR, AFFINE_RESIDUAL, EXACT_COUNT, STORE/EVICT/RECOMPUTE/SWITCH and WRITE_OUTPUT. Share each actual object once, count distinct cache copies and physical head seeks, and retain legal alternate representations. This is a sufficiency/correctness invariant for the constructed evaluator, not an arbitrary-machine lower bound.

**ONE NEXT DEPENDENCY D2-CANCEL-CERT-SPECTRAL-COMPOSITION (OPEN):** extend this paid cancellation-aware normalization from the \(d=0\) original-input subgrammar to the full authenticated /063 \`E/X\` early-bilinear source, preserving actual \(\mathbb F_2\) source-discovered basis/masks and the \(O(4^d\operatorname{poly}(N))\) exact counting bound on the newly recognized class. No global degree decision or automatic SAT hardness claim.

Sources: (1) TMR-2/063, original \`research/agents/tmr-2/2026-11-16_0105_TMR2_RELATIVE_DEGREE2_SHARED_DAG063.md\`, executable and raw pinned by blob in manuscript; (2) Ryan O'Donnell, *Analysis of Boolean Functions*, 2014, corrected arXiv:2105.10386 (Boolean polynomial foundations), https://arxiv.org/abs/2105.10386 ; (3) Ana Salagean and Percy Reyes-Paredes, *Probabilistic estimation of the algebraic degree of Boolean functions*, 2023, https://arxiv.org/abs/2306.12196 (higher-order derivative and ANF testing context). CoNP-completeness proof above is given self-contained, rather than improperly ascribed to a cited theorem. No repository checkout/preflight, pdflatex, physical-TM instruction replay or external independent mathematical review was performed. P versus NP remains OPEN.
