# Paid backdoor discovery and the actual cached-decision ledger

Charged Accounting. 21 November 2026, 22:45 PST, America/Los_Angeles.
Source snapshot abbed05159504346224bd8699b9b699d5155627e.
Named dependency DYNAMIC-PAID-BACKDOOR-LEDGER1 under DYNAMIC-COMPATIBILITY-OBLIGATION1.

**KNOWN THEOREM** for strong 2-CNF backdoor discovery [2]. **PROVED/EXACT**, restricted, for the following integration with the current encoded Boolean construction, explicit one-tape costs and actual cached-answer events. **COMPUTATIONAL** for new finite checks. Independent adversarial review pending. This run does not recertify the entire compiler or the peer cut-based recursion theorem. P versus NP remains **OPEN**.

The newest connected family supplies a useful constructive continuation. Its two-variable shortcut extends to an acquired logarithmic-size set without a quasipolynomial subset search. This known parameterized algorithm already appears in the repository's October BACKDOOR-PRODUCT-FIREWALL97 [4]. The contribution here is its ledger in the current physical encoding, including unsuccessful discovery, storage and descriptive CM, and its integration with actual post-computation events. The old backdoor theorem is not claimed as new.

## Claim, fixed solver and falsifiers

Fix a deterministic solver A before choosing the input. Its single writable tape has a finite alphabet, local unit head moves and fixed-origin terminated output. All retained original bits, copies, addresses, head positions and scratch contribute to the occupied span s_t. Define T by transitions, S=max s_t, CM_phys=sum s_t, and CM_min=sum K_U(C_t|A) for a fixed prefix-universal machine. Neither input nor t is free in K.

A authenticates the canonical dihedral/adjacent-witness image [1] by extraction and complete exact regeneration. On recognized inputs it runs iterative-deepening ternary hitting-set search on the extracted proper 3-CNF, tries all assignments to the first returned set, and decides each binary residual. On failed image admission it exhaustively decides the original Boolean input. Malformed strings may be rejected as outside the valid language after bounded parsing. Failure to find a set at a depth is UNKNOWN about SAT, and continues the search.

For every canonical input I generated from a nonempty proper source F with c clauses and d occurring variables, let h be the minimum size of a set meeting every ternary support. There are constants depending only on A such that

    T_A(I) = O(3^h N^5),
    S_A(I) = O(N),
    CM_phys,A(I) = O(3^h N^6),
    CM_min,A(I) = O(3^h N^6).

These are upper bounds on one execution. For each fixed real C>=0, the same solver is polynomial on all canonical inputs satisfying h<=C log2 N, with time exponent 5+C log2 3. No universal bound h=O(log N) is asserted.

Four falsifiers are an uncovered triple missed by search, a restriction retaining width three despite a claimed hit, a cost analysis retaining exponentially many search nodes, or repeated uses of a cache read charged with rho=1. The proof handles each.

## Exact current encoding and authentication

Use [1] with c>=1, d<=3c, r the least odd integer greater than c and at least three. Put

    n0=d+(10c+1)r+2, m0=(20c+4)r,
    n=n0+m0+3, m=2m0+4, w=ceil(log2(n+1)),
    N=3n+2+2 floor(log2(m+1))+3m(w+1)+w.

The physical tape carries unary n and delimiter, gamma(m+1), ordered signed width-w target triples, two explicit n-bit witnesses, and the width-w release identifier. N=Theta(c^2 log(c+1)). It is the full target length throughout. The source length is M=|gamma(d+1)|+|gamma(c+1)|+3c(1+ceil(log2(d+1))).

The parent's O(N^3) recognition procedure searches dimensions, extracts each literal from the controlled instruction words, regenerates every bit and compares the entire target. Its variable ranges, proper clauses and dense occurrence checks precede allocation. Each of O(N) record or generation operations can be implemented in O(N^2) transitions. Copies, counters and a retained original occupy O(N). This audit accepts that explicitly described recognition procedure and its Boolean equivalence, checked against its published proof and the latest generator/raw evidence. It does not import strict T5 symmetric C or ordered R semantics, or any model-count multiplicity.

The current two-hub family has d=2k+3,c=4k+8. Its four clauses per private pair and eight core clauses give both labels at identical N. The negative core contains all eight polarity triples. The positive core repeats +++ in place of ---. The hubs z,w meet every triple, hence h<=2 for both. The argument applies regardless of clause order or variable renaming of the extracted source, provided the target authenticates as its canonical compilation.

## Acquisition and decision proof

Keep the immutable source and a list B of selected variables. Scan for the first triple whose support misses B. If none exists, return B. If the budget is exhausted, reject this search node. Otherwise recurse in order on adding each of the triple's three variables. Any hitting set extending B must include one of those variables. Induction proves exhaustive coverage of all solutions up to the budget. A selected variable cannot be chosen twice because the chosen triple misses B.

At depth budget ell the number of visited nodes is at most (3^(ell+1)-1)/2. Iterative depths 0 through h therefore visit less than 9*3^h/4 nodes. All failed candidates and repeated scans are included. Depth-first traversal keeps only the selected IDs, branch counters and clause positions. It never stores the search tree. If all trials below h fail, budget h succeeds, so the first returned set has size h. This is the elementary proper-width-three specialization of the known theorem [2].

For a returned set, every assignment either satisfies a triple or removes at least one literal, leaving a formula of width at most two. SAT(F) is the OR of the 2^h residual decisions, since every full assignment restricts to exactly one assignment of B and every satisfying residual extends to F. An empty residual is SAT and an empty clause is UNSAT. Binary decisions use mutual reachability of complementary literals [3]. One need not compute model counts.

## Same-execution resource ledger

Source, residual and graph each need O(c log N) bits, and d<=3c. The search stack and selected IDs use O(h log N)<=O(c log N). With this compiler c log N=O(N), so all can coexist in O(N) occupied span. Graph traversal maintains a stack and visited marks for O(d) literals and O(c) explicit arcs. The original input remains charged even while unused.

Per discovery node there are at most O(c d) elementary comparisons by scanning B for each triple. Each comparison, address update or tape-list lookup takes at most O(N^2) transitions by full-span shuttling and bit arithmetic. This yields O(N^4) per node, comfortably within O(N^5). Per residual, traversals from O(d) literal sources, each expanding O(d) literals and scanning O(c) arcs, require O(d^2 c) elementary record operations, at most O(N^3). O(N^2) physical cost per record gives O(N^5). Graph construction, restriction, counters and resets fit this allowance. There are at most 2^h residuals and O(3^h) discovery nodes. This proves the displayed T bound after including O(N^3) parsing/authentication and O(N) cleanup/output.

Time and retained span belong to this same algorithm on this same input, so summing s_t gives CM_phys<=O(N T). Separately, a self-delimited original input and transition number replay C_t in O_A(N+log(T+2)) description bits. Since h<=d<=N, log(T+2)=O(N), giving CM_min<=O_A(N T). Physical and descriptive bounds have different proofs even when their displayed orders coincide. No decoding-time assumption is imposed on shortest descriptions.

For the particular two-label, one-parameter hub family, there is a sharper descriptive estimate. Its input is generated from k and one label bit, so K(C_t|A)<=O_A(log(k+2)+log(t+2)). For this A, reading/authenticating all N cells forces T>=N and N grows polynomially with k. Hence CM_min=O_A(T log(T+2)). Distinct configurations of a deterministic halting run have prefix-free shortest programs. Kraft plus convexity gives sum_t K(C_t|A)>=T log2 T. Thus on these inputs CM_min=Theta_A(T log(T+2)), and the algorithmic upper estimate is O(N^5 log N). Physical CM remains bounded by O(N^6). This refinement includes the short input description and time index explicitly.

The circuit ceiling O(N^a log N) in the handoff concerns the count map and is unused. For a hypothetical fixed global cap T<=K N^a, peak storage O(N^a), physical CM O(N^(2a)), and descriptive CM O(N^(a+1)) retain their usual meanings. The subclass algorithm supplies no contradictory demand against these ceilings. A large h is an upper-bound parameter, with no lower-bound inference. The historical product and affine controls already defeat that inference [4].

## Actual event sets after preprocessing

Complete all computation and cleanup first. Store the Boolean answer Y at a fixed cache cell next to the origin. Erase the original and scratch, paying O(N) movements within the already charged span. Return to that cache cell in one fixed READY state, with identical surroundings and head location for equal-length inputs. Then a single transition reads Y and a fixed continuation emits the answer and terminator. This normalization adds only O(N) to the bounds. It is possible on both labels and requires no promise that all inputs are UNSAT.

For the equal-prior canonical SAT/UNSAT pair at fixed k, let U=Y and let B_side contain A,k and the two public candidate inputs, but not which was supplied. Let E consist of the sole READY read transition, indexed relative to that checkpoint. Pi is its one-bit payload. Its conditional code is {0,1}, prefix-free. The decoder is the identity and uses O(1) work without source queries or addresses. Thus b=1, h_framing=0, rho=1 and

    H(U|B_side)=1=E|Pi|<=E|E|<=E[T_suffix].

Actual cache access and return-to-origin were paid. No absolute event time is supplied as a hidden channel. If the side information includes the already-read answer, entropy is zero. If q semantic obligations all request this same answer, each E_j is this same singleton, each U_j=Y and Pi_j=Pi. Then rho=q, not 1, and the shared inequality gives exactly q/q=1. This holds for every q>=1. Assigning fresh residual-identity entropy to this normalized suffix fails the decoder premise. Two equal-label inputs can have identical suffixes.

For arbitrary valid obligations on this execution, conditional prefix coding and exact decoding give H(U_j|B_j)<=E|Pi_j|<=b E|E_j|+E h_j. If every transition belongs to at most rho event sets, summation gives the requested lower bound. In this concrete suffix every premise is instantiated, and the result is one bit. A demand exceeding b rho K N^a needs another actual event/decoder premise. It does not follow from the number of private-prefix residuals in Construction's different solver. Those residual events occur in a different execution.

## Evidence, controls and scope

New code [audit](../../../experiments/dynamic_accounting_paid_backdoor_20261121.py) and [raw](../../../results/raw/dynamic_accounting_paid_backdoor_20261121.json) use only Python 3. Run the script from any directory. It tests all 256 subsets of the eight signed three-variable clauses at four budgets, 1024 cases, against exhaustive assignment semantics. Six failing searches on SAT disjoint-triple inputs attain the full node count 1,4,13,40,121,364. Four cache-overlap checks use q=1,2,8,64 and always yield the one-event bound. This specifically tests acquisition and reuse, without rerunning the prior compiler/Z3 experiment. Finite checks do not measure TM transitions or Kolmogorov complexity.

DISJ/equality sanity PASS, the permutation calibration remains polynomial with its internally reviewed single-tape scope. Relativization NOT APPLICABLE to an unrestricted separation because none is asserted. Simultaneous DTISP PASS for the specified implementation. Deterministic-configuration gate PASS for the actual halting-run description bound. Natural Proofs and algebrization provide no missing universal implication here. SAT, UNSAT and UNKNOWN admission stay distinct. Renaming, complementation, affine/Tseitin, forced-domain, private-leaf, global algebra, component factoring and shared computation remain legal controls.

Recovered AGENTS, CODEX, research skill, dynamic directive, transport model/encoding/proofs, applicable T5 model/cap definitions, own prior first-passage report, five current handoffs, latest Construction proof/code/raw and issue 324 at the source snapshot. The prior accounting first-read theorem remains intact. Branch inventory was sampled; initial recursive-tree endpoint failed and no exhaustive branch audit is claimed. Connected reads were used without a full checkout, so manuscript preflight and LaTeX builds were not run. No historical manuscript is owned by this role.

## Bounded fresh searches and attribution

Literature queries were “Gaspers Szeider backdoors satisfiability 2CNF strong backdoor hitting set 3 SAT 2012” and “Nishimura Ragde Szeider detecting backdoor sets 2004 2CNF pdf”. The 2004 original PDF, section 4 theorem 3 and section 4.1, establishes O(3^h L) search in its literal-count model. Its ternary branching is reconstructed above. The 1979 paper theorem 1 supplies the existential 2-SAT implication criterion. Its linear RAM runtime is replaced here by the explicit tape ledger. The 2014 heterogeneous-backdoor paper was consulted for context only and contributes no theorem to this ledger.

GitHub query '"backdoor" "SAT"' was freshly run in anthropics, openai, xai-org, google, google-research and google-deepmind. OpenAI and Google Research returned no results. xAI initially returned 429, then no results on retry. Anthropic, Google and DeepMind returned irrelevant security, style-guide, causal-inference or benchmark fragments. None supplies an applicable solver theorem. Web fallback searched these scopes for 2-SAT/backdoor and hitting-set SAT, with no applicable new implementation imported. Official scope ownership was checked through the Anthropic/OpenAI GitHub profiles, x.ai/news/grok-os, opensource.google/documentation/reference/github/where, research.google/resources and DeepMind's publication site. No repository code was imported from these organizations. The search-result code revisions were not inspected beyond snippets.

Repository duplicate query '"3^h" "backdoor"' recovered the October report [4], which already contains the discovery theorem and a large-h cheap family. Accordingly this run claims only the current-model accounting integration and tests. Prior backdoor work remains credited.

**One next dependency.** Discovery with Construction should supply an explicit broader admitted class or decision-safe representation with a proved total polynomial acquisition bound. Bounds and Synthesis receive the charged logarithmic-backdoor scope. Redteam should audit the O(N) live-span implementation and seek an actual post-READY obligation beyond the cached label. Large minimum syntactic backdoor alone is already insufficient [4]. Universal polynomial correctness-and-cost, and universal superpolynomial compulsory work, both remain OPEN.

1. [Current Construction report](https://github.com/j15marti/pnp/blob/abbed05159504346224bd8699b9b699d5155627e/research/agents/charged-construction/PNP_Charged_construction_2026-11-21_223200_Connected_Two_Hub_Family.md) and [compiler proof](https://github.com/j15marti/pnp/blob/abbed05159504346224bd8699b9b699d5155627e/research/agents/charged-construction/PNP_Charged_construction_2026-11-21_213600_Dihedral_Shared_Choice.md).
2. Nishimura, Ragde and Szeider, Detecting Backdoor Sets with Respect to Horn and Binary Clauses, SAT 2004, original conference manuscript, section 4. [PDF](https://ac.tuwien.ac.at/files/pub/nishimura-ragde-szeider-2004.pdf).
3. Aspvall, Plass and Tarjan, Information Processing Letters 8 (1979), 121–123, theorem 1. [PDF](https://mathweb.ucsd.edu/~sbuss/CourseWeb/Math268_2007WS/2SAT.pdf).
4. [Historical BACKDOOR-PRODUCT-FIREWALL97](https://github.com/j15marti/pnp/blob/abbed05159504346224bd8699b9b699d5155627e/research/main/2026-10-23_1948_MAIN_BACKDOOR_PRODUCT_FIREWALL97.tex).
