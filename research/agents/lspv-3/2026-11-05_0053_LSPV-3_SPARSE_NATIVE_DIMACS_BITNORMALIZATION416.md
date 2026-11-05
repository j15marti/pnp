# LSPV-3/416: Large DIMACS indices defeat dense GF(2) bit accounting, not sparse proof normalization

**2026-11-05 00:53 PST. PNP Hypergraph & Proof Certificates.** IDEA → SEARCH → ITERATE. **PROVED/EXACT:** a literal fixed-R_mix341 source-authenticated AND3/XOR certificate family invalidates the assumption that the declared variable bound n0 is at most the ASCII DIMACS input bit length N. **PROVED/EXACT, restricted:** replacing declaration-sized dense GF(2) masks by sorted lists of referenced source/DEF indices provides polynomial-bit evidence for already-legal original-source-rooted abstract proofs under the strict root-only syntactic-support semantics. **COMPUTATIONAL:** two native test implementations plus two independently implemented conditional-grammar controls. **OPEN:** full original native exported-wire/DEF-facet grammar, evaluator-source retraction, B1, B2, B3, superpolynomial mixed-system minimum, P versus NP. External mathematical review pending.

**Numbering reconciliation:** An earlier LSPV-3/415 LOCAL root payload result (2026-11-05 00:24 PST) already appears in root main.tex. This later 00:53 PST independent sparse-index audit is labeled LSPV-3/416. Initial staging artifacts with suffix 415 were append-only and have not been overwritten; use this 416 report as canonical for the new result.

## IDEA and falsifiers, registered before search

The REFEREE349 typed normalizer assumed n0<=N for DIMACS. A decimal header can instead declare K=10^t variables in O(t) source bytes. Prediction: a row over x_K has at least K bits in a dense K-position representation, but its sparse singleton ID requires O(t) bits. Falsifiers were: (1) such a valid DIMACS source or AND3 is illegal; (2) an annotated GF(2) row is not globally exact; (3) a dense K-bit mask is polynomial in the input bits; (4) sparse XOR cannot preserve coefficient cancellation and source provenance.

## SEARCH and project reconciliation

First read Nov-2 12:04 five-role handoff at commit 4e29ed7646f484707767acb6e63ec5f38afd98a8, blob 033b54b87b7cbe94912af5cf67daa52859143a07; current issue #3 through its Nov-5 00:12 updates; AGENTS.md (19656af1), CODEX.md (754999f5), and .codex/skills/pnp-research/SKILL.md (b8df83a7). **Authoritative fixed rules:** research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex, blob c87acd11d32ccfc3b7acd3667ef11daeb60079cb. The original requires correct DIMACS header/terminators and a declared variable bound, free indexed source clauses, paid indegree<=2 RES, AND3 exact truth tables for <=3 original variables with globally exact optional GF(2) row, binary XOR, unary constant-support LOCAL-CONVERT, and globally fresh two-input DEF. It contains no n0<=N restriction or mandatory dense masks.

**Affected prior proof:** research/main/2026-11-04_1748_MAIN_NATIVE-ROOT-NORMALIZATION-TRACE-B3-FIREWALL-REFEREE349.md, blob 8cc0a99302c3106018bd41aee0278010e8716fae, explicitly writes n0<=N when bounding dense GF(2) rows. Its strict root-only source-authenticated framework is retained; the numeric step and its claimed uncharged input conversion are corrected, not a wholesale rejection. Read LSPV-3/414 (blob 4d5ab9400f28f638adc0c5b77a7b6a01bfbc16c6), LSPV-2/410 (19e272e0), LSPV-1/412 RUP handoff, LSPV-4/406 INDEX handoff (cc7f2c39), REFEREE355 and issue #3 REFEREE356. No existing paper in these reviewed records proved the same literal DIMACS-index correction. Other historical duplicates may exist, and novelty is not claimed.

Independent folders were located and read: GROKPROOF/2026-11-05_0718_PROGRESS.md; research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex (1f9fc727) and research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex (9a5b05d6). Their scoped time-space/portfolio results do not close native grammar or B3.

**General indexed-web queries:** "Cook Reckhow 1979 relative efficiency propositional proof systems polynomial bounded iff NP coNP full paper", "Haken 1985 intractability resolution pigeonhole exponential proof", "knowledge compilation bounded support variable relevance Boolean circuit coNP complete", "proof complexity semantic substitution circuit equivalence coNP complete extended resolution certificates", "Raz Tzameret 2008 resolution over linear equations proof system PDF", "Cook 1976 short proof pigeon hole using extended resolution original paper PDF". Read Cook author bibliography https://www.cs.toronto.edu/~sacook/, Cook–Reckhow publisher abstract and ECCC Raz–Tzameret TR07-078 research record. Where full texts were unavailable no full-paper claim was made. **Direct Google-branded search unavailable**; these were general indexed-web queries only. Haken's 2^{Omega(h)} bound concerns ordinary shared-DAG Resolution on explicitly indexed unary PHP_(h+1)^h (standard encoding Theta(h^3 log h) bits). Cook's 1976 polynomial Extended Resolution PHP proofs and the parity shortcut on Tseitin are mandatory controls. Neither theorem is an all-algorithm lower bound.

Authenticated github.com/openai code-search queries: ExecCNFNodeSearchCosts, ImplementationCertificates, CookLevin, LRAT proof checker, support essential input circuit. Read full openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean (blob 1ced21f44ad49370d1b812e862c03c3a91d7f836) and RuntimeAssembly.lean (41df76f44884b50cca30460fa2d23bc3bf0848a0). They handle charged machine executions and explicitly retain open implementation obligations, not a same-R proof compiler.

## ITERATE 1: legal three-node source certificate and exact optimum

For every integer t>=2 set K=10^t and use the following **fully materialized decimal** DIMACS, where every occurrence of K prints its decimal numeral:

    p cnf K 4
    K 0
    -K 0
    K 1 0
    -K 1 0

Write X=x_K and Y=x_1. The formula comprises (X), (not X), (X or Y), (not X or Y). All literals have indices within the declared bound; x_K is genuinely used. N(t)=Theta(t) bits.

Two paid AND3 nodes have original-variable combined support {x_1,x_K} of size two: AND3(source1,source3) computes X and has a globally exact GF(2) annotation x_K=1; AND3(source2,source4) computes not X and has row x_K=0. One paid XOR adds the two rows, cancelling x_K and obtaining 0=1. The original-source-rooted typed DAG has q=3 unit-cost nodes, and its source and sparse proof evidence have O(t) bits. Two dense arrays indexed 1..K would each need at least K=10^t=2^{Omega(N)} physical bits. This is a falsifier of dense-mask bit accounting, not of mathematical proof correctness or sparse evidence.

**Crucial shortest-proof control:** ordinary native RES directly resolves source1 and source2 to empty in **one** node. No source clause is empty, hence a zero-node contradiction does not exist and W_R(F_t)=1. The three-node construction is a valid nonminimal upper trace deliberately exposing annotated GF(2) behavior. Flipping the second unit to (X) produces a matched SAT source with model X=Y=1; original UNSAT has no model. Neither family supplies superpolynomial hardness.

## ITERATE 2: corrected polynomial-bit normalization, scoped

Let F be a valid explicit N-bit DIMACS and pi an already **legal, original-source-authenticated** q-node derivation in the strict root-only interpretation of the unchanged R_mix341. Assume every AND3/LOCAL public support is constant-sized, syntactically authenticated original variables, LOCAL internal gates are private terms, fresh public variables have their own paid DEF owners, and all represented rule outputs are finite explicit clauses, rows or fixed-support root tables. Then the **same abstract DAG** has a typed sparse representation of size polynomial in N+q, irrespective of the magnitude of the header's declared K. This does not authorize new operations or a DEF-facet selector.

Proof: each old literal index <=K has O(N) binary bits because K is decimal-printed in the N-bit source. Fresh paid DEF index K+i has O(N+log(q+2)) bits. The initial source contains at most L<=N distinct literal IDs. Each of q charged DEF/local nodes can introduce only constant-many newly referenced IDs; RES and XOR combine existing finite supports. Thus the total set of referenced identifiers has M=O(N+q) elements, even if K is exponential in N. Encode clauses and GF(2) coefficient sets as sorted lists of signed/unsigned IDs, affine RHS as one bit, AND3/LOCAL roots as constant-support truth tables, DEF as fresh output, ordered input references and a 16-table gate tag, and DAG edges as source or earlier paid-node IDs. A coarse total length is N+O(q M (N+log(q+2)) + q*2^{c_R}) bits, where c_R is the fixed original-support constant. GF(2) XOR is symmetric difference of ID sets, including same-input cancellation. The original node sequence, source labels and q are unchanged.

**Bit-time distinction:** polynomial *existence* of normalized evidence, and polynomial checking given normalized finite evidence, do not imply that converting an arbitrary supplied E-bit giant proof payload costs poly(N+q) time. An ordinary fully reading compiler is bounded in terms of E+N+q and must charge every bit read, allocation, intermediate expansion and all-phase peak space. In particular allocating K dense bits and freeing them counts in rho. This is the precise corrected reading of REFEREE349, not a general evaluator-to-F compiler.

## ITERATE 3: conditional semantic-support hostile control

To distinguish syntactic support from a forbidden semantic oracle, use the fixed SAT source F=(y) and (y or u). Its paid AND3 factor A=y. Given arbitrary CNF G(x), the explicit hypothetical LOCAL circuit condition C_G = y OR (G(x) AND z1 AND z2 AND z3 AND z4) is always implied by A. If G UNSAT its essential support is only {y}; if G SAT every zi is essential, hence support >3. Checking "essential support <=3" is coNP-complete even with this trivial anchored source and implication. The complement has four input-flip witnesses. **This construction is NOT a legal LOCAL-CONVERT under the native syntactic <=3-support interpretation.** It is a countercontrol only against granting an uncharged semantic essential-support checker under a broader hypothetical circuit grammar. Native fixed-rule validity cannot be inferred from this conditional reduction.

## Verification and cost status

Native Python producer high_dimacs_sparse415.py passed 94 assertions on t=2,4,8,16,32,64,128,256,512,1024; independent JS BigInt checker verify_sparse_native415.mjs passed 114 checks, with four malformed-DIMACS rejections, Boolean local truth-table checks, GF(2) mask cancellation, both SAT and UNSAT source controls and explicit sparse byte comparison. Raw SHA256: 180694f31119fc1727ce7156a44bbb65a741278c782ad81b7250da3ed426d692. Neither allocated K bits or enumerated 2^K assignments. Two further independent implementations of the *conditional* support control tested 256 small G (95 SAT, 161 UNSAT): Python 107,907 checks, JS 66,850; raw SHA256 07f1bebac3abb31ec886e08a32360fb0f9802bd11b4b807f83bc6b9980806c2e. Finite checks are COMPUTATIONAL; the all-t indexing result and restricted sparse-proof existence statement have direct proofs above. Independent specialist review pending. All host work, proof bits, output and verification time are separate from paid logical q; no FLMV exponent is asserted.

## B3 and remaining precise barriers

B3 is SAT in P ⇒ for the SAME preselected R_mix341, exists C,k forall N: Wbar_Rmix341(N)<=C(N+1)^k. Neither a polynomial-bit encoding of an *existing* proof nor a rejecting trace establishes the existence of polynomial-q proofs from original F. LSPV-1/412's valid RUP-to-native-RES translation assumes a solver already prints RUP logs, which does not follow from SAT in P. Cook–Reckhow's consequence for SOME proof system is not B3 for THIS system. B1, B2, B3 and P!=NP remain OPEN.

**Next obligation:** audit real native paid-DEF facet selectors, original support authentication and global GF(2) row ownership for each legal consumer, replacing dense K-bit masks by sparse referenced IDs in any charged normalizer. Then establish a genuinely source-retracting polynomial same-R translation or a legal counterexample, and separately close or refute B3 without assuming polynomial native certificates or correctness reflection.

## References

[1] Haken A (1985), The Intractability of Resolution, Theoretical Computer Science 39:297–308.
[2] Cook SA (1976), A Short Proof of the Pigeon Hole Principle Using Extended Resolution, SIGACT News 8(4):28–32.
[3] Cook SA, Reckhow RA (1979), The Relative Efficiency of Propositional Proof Systems, Journal of Symbolic Logic 44(1):36–50.
[4] Raz R, Tzameret I (2008), Resolution over Linear Equations and Multilinear Proofs, Annals of Pure and Applied Logic 155:194–224.
