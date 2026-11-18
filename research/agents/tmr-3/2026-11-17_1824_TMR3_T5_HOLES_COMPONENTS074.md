# TMR-3/074: component-local missing-triple signature with full-support holes

Date: 2026-11-17 18:24 PST, America/Los_Angeles.
Owner: TMR-3 / PNP Time-Space Tradeoffs.
Status: PROVED/EXACT for the explicitly stated restricted class by symbolic argument below; independent mathematical review OPEN. Finite reference audit COMPUTATIONAL. P versus NP OPEN.

## Candidate, quantifiers, falsifiers

C3-T5-HOLES-WITHOUT-UNIVERSAL-HUB-QUOTIENT074. For every integer k>=6 and every missing-triple set F subset binom([k],3) of size d<k-2, form the original directed graph I(k,F) containing k hubs and a distinct private sink for every triple S not in F, with arcs i->L_S for all i in S. The missing-triple support is allowed to cover ALL k hubs. The input is the actual full binary digraph, not an encoded hypergraph oracle. Define the missing-triple primal graph with edges between every pair appearing in one missing triple; let kappa be its maximum connected component size, including isolated hubs. One deterministic source-authenticated exact counter computes all original homomorphisms to the fixed T5 tournament in time O((N+1)^12(1+2^kappa)) and simultaneous writable space O((N+1)^4) bits on recognized instances, where N is binary input length. If recognition fails, the same program's exact forest-enumeration fallback takes O((N+1)^12(1+2^(n-c))) time and the same polynomial writable space; malformed inputs reject.

Falsifiers: F1 a valid 3-color hub assignment when d<k-2; F2 an incompatible two-color palette with all present leaves satisfiable; F3 a monochromatic deleted sink weighted incorrectly or double-counted pair; F4 an uncharged decomposition/table size or any nonfamily source accepted into the shortcut. The symbolic proof addresses all four.

## Rigidity beyond the old s<k premise

Let Out(a)={a+1,a+3} (mod 5). One private sink receiving three hub colors has 2 choices when monochromatic, 1 when the distinct colors form one of the five compatible unordered pairs {a,a+2}, and 0 otherwise.

If a hub labeling uses at least three different colors, partition its nonempty color classes into three nonempty groups of sizes a,b,c with a+b+c=k. Every choice of one hub from each group has three different actual colors, so its triple MUST be missing. Thus d>=abc>=k-2 (for positive a,b,c, using abc >= a+b+c-2). This contradicts d<k-2. Consequently every valid hub labeling uses <=2 colors.

If two different colors occur, with class sizes p and k-p, the number of mixed triples is p(k-p)(k-2)/2 >= (k-1)(k-2)/2 > d. Thus some present triple contains both colors, so its sink forces the pair to be compatible, i.e. have difference ±2 modulo 5. This proves the five-palette completeness, WITHOUT any uncovered hub.

The threshold is sharp as a general sufficient guarantee: for k>=4 put colors (2,3,0,0,...,0) on the hubs and delete exactly the k-2 triples {0,1,j}, 2<=j<k. Every remaining private sink sees either one color or one of the compatible pairs {0,2}, {0,3}; the three-color hub assignment extends. Therefore the theorem cannot simply assert universal rigidity at d=k-2.

## Exact component-signature theorem

Let M_F(a) be the number of missing triples monochromatic under a binary hub assignment a in {0,1}^k. Let p(a) be its number of ones and define exact nonnegative integer coefficients
  A_{p,j}=#{a in {0,1}^k: p(a)=p, M_F(a)=j}.
For the original directed graph, where m=binom(k,3)-d leaves actually exist,
  Z(I(k,F)) = 5*2^m + 5*sum_{p=1}^{k-1} sum_{j=0}^d
                      A_{p,j} 2^{binom(p,3)+binom(k-p,3)-j}.          (1)

Proof: The five monochrome hub labellings each have exactly 2^m full sink extensions. Every nonmonochrome compatible two-color labeling has a UNIQUE unordered palette {a,a+2}, among five palettes. For a fixed palette and binary assignment, each present monochromatic triple independently contributes two sink choices, and every present mixed triple contributes one. Of all binom(p,3)+binom(k-p,3) monochromatic triples, exactly j have been deleted. Thus the full multiplicity is the power in (1). Each original full coloring is counted exactly once. All exponents are nonnegative because they count actual present monochromatic triples.

Build the missing-triple primal graph and its connected components C_1,...,C_t using paid graph operations. Each deleted triple lies wholly in exactly one C_i. On each C_i enumerate the actual 2^|C_i| binary assignments and create the bivariate coefficient table
  P_i(z,u)=sum_{a_i in {0,1}^{C_i}} z^{#ones(a_i)} u^{#missing_mono(a_i)}.
For isolated vertices the polynomial is 1+z. Since original binary hub choices on different components are independent and the missing-triple monochrome count is additive,
  prod_i P_i(z,u) = sum_{p,j} A_{p,j} z^p u^j.                    (2)
Multiply coefficient tables with exact integer convolution while storing one rolling global table; do not materialize 2^k assignments. Each table has at most (k+1)(d+1) entries, and each coefficient is <=2^k. Component enumeration takes sum_i 2^|C_i| <= k 2^kappa binary masks. Polynomial-time table convolution and final (1) therefore give O(poly(N) (1+2^kappa)) time and polynomial simultaneous workspace. This closes the named missing-support-all-hubs dependency in the small-d, small-missing-component regime. It does NOT claim a general polynomial algorithm when kappa=Theta(k) or d>=k-2.

In particular, if k=3r, r>=2, and F consists of r pairwise disjoint missing triples covering all hubs, then s=|union F|=k, d=r<k-2, kappa=3. The previous /073 algorithm requiring s<k cannot apply, but (1)-(2) run in polynomial bit time and space. Explicit local polynomial for each 3-hub hole:
  P_i(z,u) = u + 3z + 3z^2 + u z^3.
So the entire coefficient array is extracted from P_i(z,u)^r. This is a nontrivial connected source-to-output family with arbitrarily many holes and no untouched universal hub.

## Source authentication, exact resource partitions and fallback

Canonical binary original input: unary n, delimiter, unary m_arcs, delimiter, and m_arcs low-bit-first fixed-width original arc endpoint pairs. Invalid delimiter, length, bit or endpoint means REJECT; duplicate arcs are normalized. Self-loops and opposite directed arcs make count zero, correctly. The actual deterministic machine first stores or scans the complete source and derives all adjacency and indegree/outdegree records. Hub candidates are precisely vertices of indegree zero and positive outdegree; sink candidates have outdegree zero and three distinct incoming hub neighbors. Require these classes to exhaust original vertices, require unique parent-triple per sink, and enumerate all binom(k,3) candidate triples to discover F, d and the d<k-2 condition. No family oracle, artificial leaf values, or preloaded decomposition exists. On any failed recognition, use the already proved source-authenticated /068 spanning-forest binary difference enumerator, checking all non-tree arcs and multiplying rooted count by 5^c. This is an all-input complete output algorithm.

Phase A parsing, normalization, source-head seeks and candidate discovery: T_A=O((N+1)^8); live S_A=O((N+1)^4) bits. Phase B missing-triple primal components and masks: at most k 2^kappa masks; charge per mask all triple checks, addresses, locally headed seeks, counting and table updates with O((N+1)^8) bit work. Phase C rolling exact coefficient convolution: at most polynomially many (k+1)(d+1) states and pairs, each retaining O(N) bits; conservative T_C=O((N+1)^10), S_C=O((N+1)^4). Phase D formula (1) and output: at most (k+1)(d+1) terms, full exact nonnegative exponent, 0<=Z<=5^n so O(N) output and scratch bits, conservative T_D=O((N+1)^10). On one and the same sequential, locally headed, finite-alphabet execution phases do not overlap; peak live workspace includes source, matrix, components, currently enumerated masks, previous/new coefficient tables, all arithmetic, heads and output. Thus T_rec=O((N+1)^12(1+2^kappa)), S_peak=O((N+1)^4). Source recognition failure followed by forest fallback is included in T_other=O((N+1)^12(1+2^(n-c))) and matched space. No constant-time random-access/BigInt machine is assumed.

This is a conservative polynomial envelope, not a native microcode trace; no claimed time lower bound, Tree Evaluation speedup, physical checkpoint-space bound, or general SAT transfer follows. Signed-3SAT-to-T5 reductions of peer agents require their precise original-graph blowups to transfer exponents; the semicomplete-digraph NP-completeness dichotomy alone does not supply them.

## Reproducible finite audit and limitations

Local CPython 3 stdlib source revision tmr3-t5-holes-components074-v1, seed 202611171824, source SHA256 e1df53336bdf4b07a9478c00fae3913700b0a717af09b38fd2786959351a2632. Two identical successful audits, raw SHA256 de470668e0b34e095e90f0815a19baf2e4306b265dd6bfd193e1000f1b379f73: 150 checks, 0 failures, 42 randomized k=6,7 reference cases compared with independent 5^k original hub-color enumeration and independent 2^k palette enumeration; all-support disjoint holes k=6,9,12,15,30, each kappa=3; malformed and graph fallback controls; k=4,d=2 three-color sharpness witness. Largest k=30 graph has 4080 original vertices, 12150 arcs, and exact answer of 1220 decimal digits. Exact source and raw JSON were produced locally. An initial *test harness* attempted an unnecessary 2^30 independent crosscheck and timed out; the corrected final audit restricts that comparison to k<=15 and both completed successful runs matched byte-for-byte. That harness timeout is not a T5 solver theorem failure.

Finite comparisons are COMPUTATIONAL and do not verify the infinite-family theorem. Full native deterministic machine microcode, repository preflight without local checkout, independent external mathematics review, and full LaTeX compilation have NOT been executed. Independent mathematical review remains OPEN.

## Mandatory gates and scientific controls

DISJ sanity PASS restricted: no static-rank-to-work inference and no necessity claim. Relativization NOT APPLICABLE WITH REASON: a positive concrete restricted algorithm, not a separation; unrestricted NP claims and BGS/algebrization/Natural Proofs remain OPEN. Simultaneous DTISP PASS restricted for the complete same-machine upper ledger and full output; no forbidden-region or unrestricted lower bound. Deterministic configuration counting PASS upper-bound consistency only; never a work lower bound or randomized/quantum claim.

All Horn/dual-Horn, 2-SAT, affine/Gaussian, treewidth, equality, autarky, products, padding/auxiliary, selector/unique-solution, module, twin, degree-two, component, caching/recomputation and exact-source compact shortcuts remain legal. No generic representation necessity follows from large cycle rank, core, frontier, tensor rank or eigenvalue. Historical /341 FAIL as full UNSAT authority; /386 RESTRICTED. P versus NP OPEN.

## Original reference and next dependency

Bang-Jensen, Hell and MacGillivray (1988), "The Complexity of Colouring by Semicomplete Digraphs", SIAM J Discrete Math 1(3):281-298, DOI: 10.1137/0401029, classification of semicomplete fixed-template homomorphism, not quantitative reduction size.

ONE next load-bearing lemma: C3-T5-RAINBOW-EDGESET-SIGNATURE. Extend the exact signature beyond d<k-2 by keeping a charged finite-state representation of surviving 3+ color hub assignments when missing triples constitute every rainbow triple of a hub coloring. Specify treewidth/connected-component parameters and source-discovered decomposition, or give a concrete counterexample demonstrating why no such bound transfers.
