# TMR-5/072: independent C5-to-T5-to-CNF reproduction and polynomial-count high-treewidth reduction image

Date: 2026-11-17 13:52 PST. Owner: TMR-5 / PNP Machine Bottleneck Redteam.
Status: **PROVED/EXACT for the stated fixed-template combinatorial identities, external mathematical review OPEN**; independent finite implementations **COMPUTATIONAL**. This closes an independent-review dependency for TMR-1/071 but creates no unrestricted lower bound. P versus NP OPEN.

## Exact candidate, quantifiers, model and falsifiers

Candidate D5-T5-FOUR-ARC-INDEPENDENT: For every simple loopless undirected H=(V,F), with its complete unary-header, low-first-index binary encoding, let D(H) contain original V and two globally fresh vertices z_e,w_e for each e={u,v}, u<v, and arcs u->z_e->v->w_e->u. For Sigma=Z5, R(a,b) iff b-a mod5 in {1,3}, prove for every H

    #Hom(D(H),T5)=2^|F| #Hom(H,C5),

where undirected C5 adjacency is a difference of ±1 mod5. Independently verify its genuine source serialization, its direct T5-to-Boolean parsimonious width-at-most-three CNF compiler, and the precise decision (not 1-to-1 counting) reduction. New hostile control: the family H=K_{s,t}, s,t>=1, yields an explicit polynomial-time exact counter for a reduction-image family of unbounded treewidth and cycle rank.

Falsifiers identified before checking the original peer report and primary theorems: (1) an endpoint pair outside C5 adjacency admits a gadget extension; (2) an adjacent pair has a count other than two, or fresh auxiliaries collide; (3) source length, parsing, unique CNF extension or counting multiplicity changes under composition; (4) the apparent hard structural family lacks a charged compact direct counter.

## Full authenticated input-to-output chain

Source H uses unary 1^n0, 1^m0, and m strictly sorted distinct pairs 0<=u<v<n, each low-first of width w(n)=max(1,ceil(log2(max(2,n)))). Its exact length is L_H=n+m+2+2mw(n). Malformed inputs are INVALID, not NO. The source-aware constructor makes n_D=n+2m, m_D=4m; its complete directed edge source has L_D=n+6m+2+8mw(n+2m). For simple H, m<=n(n-1)/2 and w(n+2m)<=2w(n), giving L_D<=8L_H. Fresh vertex indices n+2e,n+2e+1 prevent aliasing, and graph edges are sorted before emission.

For any x,y in Z5, let t(d) be the number of z with R(x,z) and R(z,y) when d=y-x mod5. All four ordered increments are 1+1=2, 1+3=4, 3+1=4, 3+3=1 mod5; hence t(0..4)=(0,1,1,0,2). Two fresh, independent halves of one gadget have precisely t(d)t(-d), which is 2 for d=1 or d=4 and zero otherwise. Products over disjoint auxiliary pairs give the exact factor 2^m with no promised uncharged help. Restriction of an accepting D-labeling to old vertices is a C5-labeling; selecting one legal fresh assignment for each edge is a paid constructive extension. This proves a polynomial many-one reduction, not a parsimonious reduction.

The independent reverse CNF check follows TMR-1's explicit source model: for any directed G of n vertices and m arcs, five one-hot X_{i,a} plus three uniquely forced prefix-OR Y_{i,j} per vertex; 10 binary at-most-one clauses, nine width<=3 prefix equivalence clauses, and one final OR per vertex, plus the 15 forbidden directed-pair clauses per arc. Exactly q=8n Boolean variables and c=20n+15m clauses, width<=3. Every proper T5 labeling uniquely extends to Boolean auxiliaries; no incorrect one-hot pattern satisfies. Thus #SAT(F_G)=#Hom(G,T5), including loops, oppositely directed arcs, isolated vertices and empty instances. Composing with H gives q=8n+16m, c=20n+100m, and #SAT=2^m #C5Hom(H). Width-at-most-three is NOT silently called strict three-distinct-literal 3SAT; any further formal input normalizer is separately chargeable and remains OPEN for Anthropic-specific semantics.

The exact NP-complete classification is KNOWN from Hell--Nesetril's 1990 undirected H-colouring theorem (C5 is loopless and nonbipartite) plus this independently checked gadget, and separately from Bang-Jensen--Hell--MacGillivray's 1988 semicomplete target dichotomy. The polynomial reduction supplies no general SAT lower bound.

## New hostile control: polynomial-count image of K_{s,t}

For integers s,t>=1, let H=K_{s,t} with the left s vertices and right t vertices distinguished only by the authenticated canonical vertex order. The exact homomorphism count to undirected C5 is

    #Hom(K_{s,t},C5)=5(2^s+2^t-2).

Proof: Fix all s left labels. If they are all equal, there are five choices and each right vertex may choose either of two neighbors independently, giving 5*2^t. Otherwise, a nonempty common neighbor exists only if exactly two different left labels occur and are the two neighbors of one C5 vertex. The five possible unordered pairs are distance two, each with 2^s-2 surjective left sequences; their sole common neighbor forces every right label, yielding 5(2^s-2). All other left sequences have no common neighbor, since t>=1. Sum both disjoint cases.

Therefore the exact T5 count on the genuine four-arc reduction image is

    #Hom(D(K_{s,t}),T5) = 2^(st)*5*(2^s+2^t-2).

Its underlying undirected graph has n_D=s+t+2st vertices and m_D=4st edges, cycle rank r=m_D-n_D+1=2st-s-t+1. Contract each u-z_e-v path to recover K_{s,t} as a minor, so treewidth at least min(s,t). When s=t=k, both treewidth and cycle rank diverge, but a source-aware polynomial recognizer tries all candidate s,t with n_D=s+t+2st and m_D=4st, regenerates all exactly indexed gadget arcs, and compares complete authenticated records. It then writes 5*(2^s+2^t-2) shifted left by st bits. Only on a verified match does it output this exact count; other valid sources are OUTSIDE and are not misclassified as unsatisfiable. Unary/explicit source lengths satisfy n_D,m_D<=N, the integer output has O(st+s+t)=O(N) bits, and a conservative single-tape-model simulation of a locally headed multi-tape implementation has **same-run** T=O((N+1)^7), peak writable S=O((N+1)^3) for this recognizer, including parsing, candidate failures, index arithmetic, edge sorting/comparison, retained buffers, exact arithmetic and output. This is an UPPER bound on a restricted family. High treewidth, many cycle factors, many accepting witnesses, and hardness of other inputs cannot imply necessary work for this family. General-source fallback remains unrestricted/exponential.

Concrete exact counts for s=t=1,2,3,4 are 20, 480, 35840, 9830400. These are model-consistent exact integers, not evidence of a P-versus-NP lower bound.

## Independent executed evidence

Two different complete implementations were actually executed. **CPython 3.13** local independent source `tmr5_t5_chain072.py`, SHA256 `882194c19ec032d3a784b68830aeeda1be2b7515eb24db932ac3e465761bca6b`; immutable local JSON SHA256 `885d07b4b7fb61f58d6494599da1944795fb8f29ccbfb939680a71e3225d35c5`. It checked all 25 gadget endpoint pairs, all 76 simple graphs with n<=4 and low-first source roundtrips/bit blowup, 41,056 source labelings, 338,906 direct CNF model-vs-original-label checks on feasible complete sources, 11 full expanded T5 exhaustions, 16 K_{s,t} count cases with 1<=s,t<=4, and eight malformed-source rejections: zero failures. No random seed. Exact local files are bundled as `TMR5_072_independent_T5_chain.zip`, not asserted to be GitHub files.

An independently authored and actually run V8 implementation, revision `tmr5-t5-independent-v8-072-v1`, also checked 25 endpoint pairs, all 76 n<=4 graph families, 41,056 original labelings, and 16 exhaustive K_{s,t} cases: zero failures. This full stand-alone JavaScript source is published under `experiments/tmr/tmr5_t5_c5_independent072.js`; its immutable JSON under `results/raw/tmr/2026-11-17_1352_TMR5_T5_CHAIN072_V8_RAW.json`. GitHub file readback confirms source and raw blobs independently. Finite tests remain COMPUTATIONAL, while the universal formulas above have separate symbolic proofs. No native Turing-machine microcode or external independent referee has executed.

## Mandatory gates and full-program synthesis

DISJ sanity: **PASS restricted**. The explicit K_{s,t} control has highly connected structure and exponentially many labels, but a source-authenticating exact polynomial counter; no source-split rank or prescribed representation lower bound is transported to arbitrary machines. Relativization: **PASS for the combinatorial gadget**, while any nonrelativizing P!=NP claim is OPEN; BGS/algebrization/Natural Proofs barriers are unaddressed. Simultaneous DTISP: **PASS for the specified recognizer/compiler UPPER bounds on one actual model**, not a forbidden deterministic lower resource pair. Deterministic configuration counting: **PASS as an upper-bound consistency check only**, not a proof of necessary computation. Affine/Fourier, cycle-space, treewidth DP, local consistency, products, selectors, normalization, unique solutions, padding, sharing, caching and adaptive FBDD remain legal alternatives. Prior /341 FAIL as logical UNSAT authority, /386 RESTRICTED.

Ranked pipeline arrows after this audit:
1. TMR-1 / exact C5->T5 four-arc -> parsimonious width<=3 Boolean CNF: **independently PROVED/EXACT**, supported by two finite reproductions. The upstream explicit authenticated 3SAT->C5 gadget source-size/witness interface is still **OPEN**; NP-hardness itself is KNOWN from the primary dichotomy.
2. TMR-2 / source-aware cofactor and constant-successor recognizers: **PROVED/EXACT restricted**; general representation-independent time necessity **OPEN**. The unbounded decimal-header exact-output claim is **FALSIFIED and repaired on main**.
3. TMR-3 / signed forest cycles, Fourier, degree-two elimination: **PROVED/EXACT restricted**, all-input forbidden DTISP or polynomial decider **OPEN**.
4. TMR-4 / authenticated MDD, block OBDD, adaptive FBDD and CNF: **PROVED/EXACT upper constructions**, representation-width-to-any-machine resource lower bound **OPEN**. A particular fixed order is never made compulsory.

A 3SAT->T5 polynomial reduction permits the logical implication that a polynomial-time solver for ALL T5 inputs would decide 3SAT in polynomial time. It does not turn an exponential witness/OBDD lower bound for a chosen encoding into a superpolynomial lower bound against every Boolean-SAT decider. P versus NP remains OPEN.

## One highest-value next dependency

Independently produce, authenticate and exhaustively verify a complete direct 3SAT->undirected C5-colouring gadget and charged source-bit/witness mapping, then compose with the now independently verified four-arc/Boolean-CNF interfaces. Do not promote a local gadget PASS or structural rank to an all-machine SAT lower bound. No peer manuscript, retired tracker, workflow or agent schedule change is authorized.

## Primary sources and reviewed role evidence

Hell, P., Nesetril, J. (1990), *On the Complexity of H-Coloring*, JCTB 48:92-110, DOI 10.1016/0095-8956(90)90132-J.

Bang-Jensen, J., Hell, P., MacGillivray, G. (1988), *The Complexity of Colouring by Semicomplete Digraphs*, SIAM J. Discrete Math. 1(3):281-298, DOI 10.1137/0401029.

TMR-1/071 authentic direct gadget report, `research/agents/tmr-1/2026-11-17_1317_TMR1_T5_C5_GADGET_AND_PARSIMONIOUS_3CNF071.md`, draft PR #197; TMR-2/068 source repair merged to main; TMR-3/069 degree-two weighted elimination draft PR #226; TMR-4/071 adaptive FBDD draft PR #227; TMR-5/071 high-girth/path-consistency report in draft PR #209.

Preflight not run: there is no local full repo checkout and local GitHub DNS is unavailable; full LaTeX compilation and formal kernel were not executed. OWN main5 manuscript reconciliation and role-owned handoff are recorded separately after source SHA recovery and readback. No external mathematical peer review is claimed.
