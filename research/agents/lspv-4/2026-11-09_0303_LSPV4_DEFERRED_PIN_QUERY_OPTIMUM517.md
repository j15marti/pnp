# LSPV-4/517 | Exact optimal delayed-negative tag queries on authenticated strict-3CNF Tseitin selectors

**2026-11-09 03:03 PST | LSPV-4, Route A | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN.**

**Nodes:** Material new evidence **[P2-L4-517]** refines **[P2-L4-516]** and the originating guarded selector **[P2-L2-516]**; prior affine-trie analysis **[P2-L2-515]** and source-authentication control **[P2-L4-515]** remain scoped. **[P2-A2]**, **[P2-A4]**, **[P2-A5]**, **[P2-D1]**, **[P2-C3]**, **[P2-B1]**, **[P2-B2]**, **[P1-01]**, **[P1-03]**, **[P1-04]** all remain OPEN. Historical R_mix341 rules and weights unchanged.

## IDEA -> SEARCH -> ITERATE, with predeclared falsifiers

**Hypothesis:** LSPV-4/516's sound grouped-pins policy performs $5q-5$ tag reads on $q=2^k$ descriptor-consistent variants, but reading all *four* negative tag signs **before advancing to the next group** is unnecessary for all-input soundness. Query one representative sign per group; as soon as any sign is positive output SAT; only after all representatives are negative read the remaining three signs per group before UNSAT. The precise summed tag-read minimum over all $q$ descriptor-consistent members, subject to correctness for *every* of the $2^{4k}$ mixed-sign template sources, should be $2q-2+3k$.

**Falsifiers, stated before checking:** (F1) Some mixed-sign four-facet pin makes SAT classification differ from OR of all sign-positivity bits. (F2) The delayed-query policy returns UNSAT without seeing all $4k$ negative signs, or returns SAT on an all-negative source. (F3) An alternative deterministic single-bit query order has lower summed read count on the $q=2^k$ consistent inputs, despite being correct on every accepted mixed-sign template. (F4) The strict-3 source encoding fails positional independence, proper ternary syntax, or original-source authentication assumptions.

**Search/continuity actually performed:** Read complete root proof1.txt at blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b and proof2.txt at research-stage blob f11e45dc179231729fbb54e9ff81bc017635af7a; issue #3 including latest five-role comments and the new knot/link handoff; governing 2026-11-02_1204 handoff, AGENTS.md, CODEX.md and .codex/skills/pnp-research/SKILL.md. Read role originals LSPV-2/516 (blob 409f49e5322efa71a178544548e04528938dd16e), LSPV-4/516 (blob 046320755c89dd3f863b7434c4be72a4f4bbcdf3), LSPV-4/516 five-role handoff (blob b3e53a2b4076645ac8b61dfad5252983f9967470), and executable experiments/arc/lspv4_516_trace_leaf_optimum_v8.js (blob f00465921f2d25a07f0f81081718c85139551a52). Read GROKPROOF/2026-11-08_1130_PROGRESS.md (blob 6942a99f176e996e9542f0386b7aa7fe2ce89e70) and research/agents/claude/world-ledger/README.md (blob de75a371ce3143a4495e6892df7fb04794a6b708). New knot/link topology note research/coordination/2026-11-09_KNOT_LINK_TOPOLOGY_SAT_FIVE_ROLE_HANDOFF.md (blob 0289edb73d1e38492f0693844667be59d4152785) is an additive candidate; no topology-to-FLMV simulation is assumed.

**External primary research and actual repository reads:** Fortnow–Lipton–van Melkebeek–Viglas (2005), JACM 52(6), DOI 10.1145/1101821.1101822, indexed-input machine and time-space lower bounds; Urquhart (1987), JACM 34(1), DOI 10.1145/7531.8928, exponential ordinary shared Resolution for expander-Tseitin; Bryant (1986), IEEE Trans. Computers 35(8), DOI 10.1109/TC.1986.1676819, DAG representation background. Actual GitHub pinned files reviewed: konard/p-vs-np README.md (blob 0e0ec77f83ad6eec1719a96066108b96ac1c2a95) and scripts/proof_status.json (blob 93b77ed3d8fe456f81c690035f45f07910a247f2); blkph0x/p-vs-np-proof-research METHOD_INDEX.md (blob 18d693ea71dfa433370eb7afbebc3106e32f03e5) and INDEPENDENT_AUDIT.md (blob b30515cced93d8911a6415555ee9ec1444502d93); MassimoLauria/cnfgen cnfgen/families/tseitin.py (blob 4bb5fd198fc4a698a5a207f67b36a9591b2a3bab); meelgroup/frat-xor README.md (blob 38a137bca4d4ab6443703d4c31fba5783021c581); openai/math CONTENTS.md (blob 7e1ed90ac5a666f1bbecb22027387c4ad79e9d03); berkeley-abc/abc README.md (blob 88a9d1a316dd9751acade746de315fd1e6e6c362). These are scope, formalization and shortcut controls, not proofs of the needed SAT contraction. Public web search was used; no separately authenticated Google-branded search, native FLMV interpreter, or historical R_mix341 checker was executed.

**ITERATE result:** The original LSPV-4/516 computation is SOUND but not optimal in *tag reads*. F1–F4 did not invalidate the corrected policy. The original phrase that all four negatives must be read "before advancing" is too strong; all negatives must be read **before issuing UNSAT**, not before moving to another group. This run supplies a global exact query-minimum theorem in the specified single-bit oracle model, not a general minimum runtime/space theorem.

## Exact theorem: aggregate tag-bit read optimum

Let $k\ge1$. On the fixed authenticated strict-three original-CNF source template from LSPV-2/516, each group $j$ has four independent literal-sign fields $z_{j,0},z_{j,1},z_{j,2},z_{j,3}$. For arbitrary mixed signs, satisfiability is exactly the OR of all $4k$ indicators of *positive* tag literals. Restrict the workload distribution to the $q=2^k$ descriptor-consistent inputs $z_{j,0}=\cdots=z_{j,3}=d_j$. A deterministic source-query policy may adaptively query one physical input bit per step, but it must classify **all** arbitrary mixed-sign template sources correctly, and cannot use an uncharged oracle that observes an unqueried source bit. Define $L(d)$ as the number of tag-sign bit observations before its final SAT/UNSAT decision, excluding invariant-source authentication and non-tag operations.

**PROVED/RESTRICTED (sharp minimum):**
$$
\boxed{\min_{\text{sound single-bit adaptive policies}}\sum_{d\in\{0,1\}^k} L(d)
= 2^{k+1}-2+3k=2q-2+3k.}
$$
The minimum counts tag queries from fresh independent starts on each original binary input; it is NOT a lower bound on shared multi-child algorithms, elapsed time, or arbitrary SAT decision machinery.

**Proof (lower bound).** On the all-negative input $d=0$, a correct policy must observe every one of the $4k$ tag positions: otherwise flipping one unqueried negative tag to positive makes a SAT original template with exactly the same observed input bits, giving an incorrect UNSAT decision. Take the zero-input execution and list the *first* observations of the $4k$ distinct tag positions in their execution order, omitting repeated queries and invariant-bit observations (whose cost can only increase work). Before the $t$th new tag query, suppose $r_t$ distinct tag groups have already had a query. Exactly $2^{k-r_t}$ descriptor-consistent sources agree with the zero-input transcript through that prefix. Each must incur the $t$th tag query. Therefore the aggregate reads are at least
$$
\sum_{t=1}^{4k}2^{k-r_t}.
$$
Each group has four required first-read events. To minimize this sum, an exchange argument moves the *first* read of any previously untouched group earlier than any extra read of a previously touched group. Such an exchange does not increase any prefix's number of untouched groups and strictly improves at least one intermediate term. Thus an optimal zero-path order queries one representative sign from each of the $k$ groups first and then all $3k$ remaining signs. Its total is
$$
\sum_{r=0}^{k-1}2^{k-r}+3k=2^{k+1}-2+3k.
$$

**Proof (attainment).** First inspect sign $z_{j,0}$ for $j=1,\ldots,k$ in order. Return SAT as soon as a positive is observed. If and only if all $k$ representatives are negative, inspect the other $3k$ signs (in any order), returning SAT on the first positive. Return UNSAT only after all are negative. This policy is correct on every one of the $2^{4k}$ accepted mixed-sign sources. On each descriptor-consistent positive source it halts on the first positive representative; only descriptor zero pays the additional $3k$ signs. This meets the lower bound. QED.

For comparison, LSPV-4/516's sound *group-complete-before-advancing* policy costs exactly $5q-5$ tag reads; a full scan costs $4kq$ tag reads. The improvement is
$$
(5q-5)-(2q-2+3k)=3(q-1-k),
$$
strictly positive for every $k\ge2$. At $k=10$, $q=1024$, the optimized policy uses **2,076** tag reads, the earlier sound policy **5,115**, and full scan **40,960**. The optimized policy retains exactly $k+1$ complete observed trace classes, consistent with the exact class optimum of [P2-L4-516], but materially reduces tag acquisition cost.

## Original-source family and hardness qualification

The source is the LSPV-2/516 original signed K4 Tseitin odd-charge core (6 edge variables, 16 proper 3-clauses), $k$ pinned controls using four ternaries per pin, a strict-three OR-chain, and split guarded proper-3 clauses. For $k\ge1$, the number of variables/clauses and exact physical binary packet length are
$$
n=19+6k,\qquad m=27+9k,\qquad w=\lceil\log_2(n+1)\rceil,
$$
$$
M=8+n+1+3m(w+1)+2=\Theta(k\log k).
$$
The packet has fixed 8-bit magic 10110110, unary $1^n0$ header, ordered unsigned variable IDs with sign bits, and terminal 01. The $4k$ tag signs occupy disjoint physical offsets. All fixed fields must be *source-authenticated without reading the tag signs during the shared phase*, or the observed-trace-class accounting changes; unlike the earlier faulty unordered-facet validator [P2-L4-515], every edge/ID/facet position is exact. A sound complete all-input decider must use a fully charged generic SAT fallback on malformed or off-template sources, with correctness on SAT/UNSAT/malformed. The fastpath is not a general SAT decider by itself.

The four-facet pin has $g_j=1$ feasible iff ANY of its four guard signs are positive, and $g_j=0$ feasible iff ANY are negative; for $g=\bigvee g_j$, all original odd-Tseitin clauses can be satisfied when $g=1$, while $g=0$ forces the UNSAT core. Consequently, SAT iff at least one positive tag is exact for *all* accepted mixed-sign patterns.

This finite K4 family is a correctness/optimizer falsifier, NOT a certified asymptotically hard 3-SAT family. Urquhart expander-Tseitin formulas have published exponential *ordinary Resolution* lower bounds on appropriate graphs, but no lower-bound preservation through this guarded selector or historical fixed mixed R_mix341 is proved. Strong legal shortcut controls include XOR/Gaussian elimination, native source recognition, extension variables, branch DAG sharing and direct OR evaluation.

## Independent computational controls

Published reproducible JavaScript verifier: experiments/arc/lspv4_517_delayed_pin_readoff_optimal.js, full executable run in V8 via the GitHub connector. It constructs exact original proper-3CNF K4 selectors for k=1..10, checks 2046 descriptor-consistent source instances with four disjoint independently verified sign offsets per descriptor coordinate, tests 16 entire four-facet pin sign patterns under both guard values, and exhaustively checks all $2^{4k}$ arbitrary mixed-sign template cases for k=1,2,3 (4368 total). A separate dynamic-programming optimizer minimizes all legal zero-path tag-observation schedules for k=1..6 (up to 15,625 distinct states); each exact optimum equals the formula. Published V8 result: **8,538 assertion groups PASS**.

Independently implemented Python: /mnt/data/lspv4_517_independent.py and /mnt/data/lspv4_517_python_raw.json, bundled in the run's reproducibility ZIP. This independently regenerates the original 3-CNF sources, source lengths and SHA-256 baseline fingerprints, verifies all k=1..10 read totals/class counts and all 4368 mixed-sign patterns, and independently dynamic-programs 15,625 states at k=6. Python **8,616 assertion groups PASS**. The two independent implementations agree on the precise optimum at each k, including 2,076 at k=10. Neither implementation executes an actual native FLMV indexed-tape machine or historical R_mix341 accepted-byte checker. Finite controls are COMPUTATIONAL; the all-k theorem is supplied by the exchange argument, not extrapolated from test data.

## Resource and transfer firewall

The exact result charges ONLY tag-bit observations on a per-child, fresh-start, deterministic *query* model. In a real native FLMV simulation independently handling all q original encodings, source authentication of the other $M-4k$ fields may cost $\Theta(qM)$ input operations; indexed jumps require constructing, writing/erasing and reading INDEX bits and physical head movement; all certificate or child representation bits, descriptor generation, virtual transducer effects, output, fallback guest simulation, cache lookup, delayed reads, failed policies, replay and recomputation must be charged. Storing the entire precomputed original source in WORK has high-water $\Omega(M)$, even if subsequently cleared; the hosted verifiers do store it. An on-demand indexed generator is a separate construction, not implicitly zero-cost.

The optimized per-input tag-query span is at most $4k$, with $k$ only on SAT inputs; aggregate optimized query work $2q-2+3k$ if independently run over all $q$. The exact minimum here is **neither** the minimum over all shared physical computation DAGs **nor** native elapsed time or WORK space. A common structural source authenticator, the $O(qM)$ cost of explicitly outputting all children, and the all-input generic SAT fallback can dominate. No polynomial all-input FLMV contraction, no same-machine recursive applicability, and no source-independent rank bound follows. Proposed Route A recurrence
$$
t'\le \max(11/10,3/5+t/2),\qquad s'\le\max(1/2,s/2)
$$
remains OPEN at **[P2-A2] [P2-A4] [P2-A5]**. Cross-route **[P2-B1] [P2-B2]** and historical grammar **[P2-D1]** remain OPEN.

**Result:** exact all-k optimal query work in a specified sound single-bit policy model and a precise correction to [P2-L4-516]'s query scheduling assertion. **No P versus NP resolution.**

## Sources

1. L. Fortnow, R. J. Lipton, D. van Melkebeek, A. Viglas, "Time-Space Lower Bounds for Satisfiability", *JACM* 52(6), 835-865 (2005), DOI 10.1145/1101821.1101822. https://lance.fortnow.com/papers/files/tst.pdf
2. A. Urquhart, "Hard Examples for Resolution", *JACM* 34(1), 209-219 (1987), DOI 10.1145/7531.8928.
3. R. E. Bryant, "Graph-Based Algorithms for Boolean Function Manipulation", *IEEE Trans. Computers* 35(8), 677-691 (1986), DOI 10.1109/TC.1986.1676819.
4. Internal source family and first sound scan: research/agents/lspv-2/2026-11-09_0214_LSPV2_SEMANTIC_AFFINE_RANK516.md and research/agents/lspv-4/2026-11-09_0236_LSPV4_SEMANTIC_TRACE_LEAF_OPTIMUM516.md.
