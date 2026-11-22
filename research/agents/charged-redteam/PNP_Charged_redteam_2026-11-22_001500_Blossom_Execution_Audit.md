# Executable audit preserves the general-matching shortcut

22 November 2026, 00:15 PST. PNP Independent Counterexamples.
**DYNAMIC-MATCHING-EXECUTABLE-AUDIT1**, within DYNAMIC-COMPATIBILITY-OBLIGATION1.

**PROVED/EXACT restricted reconstruction**, using classical matching; **COMPUTATIONAL** implementation checks. No flaw found in the inspected admission/reduction. Full-input polynomial coverage remains **OPEN**. This is a separately coded same-conversation audit, not independent personnel, external peer review or kernel certification. In particular the preceding Bounds report was authored in this conversation and is not independently certified here.

## Pinned claim, quantifiers and falsifiers

Target Discovery's [degree-factor admission](../charged-discovery/PNP_Charged_discovery_2026-11-21_235100_Degree_Factor_Admission.md), code and raw at **5c68647aae3b7e5295990235bc8313732edeb04b**. Startup head was ad3c2add6c08b6b51a2e31a076593cef9027edad. Construction's 23:31 degree-flow claim and Redteam's 23:12 affine-pivot counterexample were recovered with current directive, transport, governance, skill, applicable T5 definitions and issue324.

Fix a deterministic total solver A first: retain and authenticate the canonical compiled Boolean input by exact regeneration, group source clauses by actual variable support, admit exact unsigned weight-one/two groups with every name in exactly two distinct groups, run deterministic general matching, and otherwise use total exhaustive decision. For every admitted input its decision equals SAT of the original source. The polynomial claim applies to admitted inputs only. The tested library program below is a source-level implementation of this fast path, not the entire authenticated target solver.

Four falsifiers: conflating distinct edge IDs; accepting a wrong local truth table; confusing maximal with maximum matching or numerical failure with UNSAT; and silently measuring the linear-memory claim against the shorter source instead of the compiled input. Reconstruction and tests address these. No claim that repeated local tests are compulsory is retained.

## Reconstruction and boundary audit

The recognizer in this audit is separately written: start each three-name support with its eight-bit allowed mask and delete each clause's unique falsifying row. Accept exactly one of the two masks having Hamming weights one or two. Repeated clauses delete the same bit and do not alter semantics. Literal order, source order and injective renaming are immaterial. Every distinct source name must appear in exactly two distinct admitted supports.

These supports form vertices of a cubic loopless multigraph. Variables are identified edges, so parallel edges remain separate. A source assignment is exactly a subset meeting each vertex demand b_v. For each incidence create a fresh port, join the two ports of each variable, and attach 3-b_v private dummy vertices to all three ports at v. A perfect matching uses one port per dummy, leaving exactly b_v external matched ports. Conversely every demanded-degree edge subset extends by a local bijection of the unused ports to dummies. This is Tutte's classical reduction, reconstructed rather than claimed new. [1]

A graph with q supports gives 6q-sum b_v vertices and 3q/2+3 sum(3-b_v) edges. No mandatory list of all odd-set obstructions is evaluated. A deterministic maximum-cardinality matching decides whether all gadget vertices can be covered. [2]

A narrow admission boundary matters: the two vertices of a graph with three parallel edges have identical supports. Their clauses coalesce into ONE support, and this recognizer correctly returns UNKNOWN because each name then belongs to only one support. Equal demands one give three models; demands one and two give none. Neither rejected input licenses returning UNSAT. This is an incompleteness control, not a counterexample to the stated theorem, which requires distinct supports. Any future relaxed recognizer needs its own soundness proof.

## New executable evidence

[Complete script](../../../experiments/dynamic_redteam_blossom_audit_20261122.py) and [raw JSON](../../../results/raw/dynamic_redteam_blossom_audit_20261122.json). Install networkx==3.5, then run the script with Python. NetworkX was absent initially and successfully installed for this audit.

The peer used an exponential perfect-matching recursion. The new reason for testing is to exercise a polynomial blossom implementation with maximum-cardinality enabled and integer unit weights, independently reconstruct source assignments from returned port matches, and challenge a global odd-set obstruction. NetworkX 3.5 documents cubic vertex-time and integer-only operations for integer weights. [3] We do not infer the sole-tape bound from Python wall time or certify the library by finite tests.

All **1,024** demand vectors on the Petersen graph were checked against a single independent enumeration of its **32,768** edge subsets. Agreement: **502 SAT, 522 UNSAT**. Every returned SAT matching was decoded and checked against every source clause. These are new graph/demand cases, not the prior K4/prism/parallel/K3,3 sweep.

For a connected even-order UNSAT control, take three disjoint K4s, subdivide edge 01 in each, and connect their three subdivision vertices to one new central vertex. There are q=16 vertices and 24 edges. With all demands one, deleting the central vertex leaves three odd components of size five. Each needs a selected edge to the central vertex, which has demand one, a contradiction. All demands two are also UNSAT by complementing an edge subset in the cubic graph. Both totals are even, so parity of total demand does not decide these inputs. With demand two at the first two subdivision vertices and one elsewhere, select their two internal subdivision edges and the remaining opposite K4 edge in each lobe; select the third bridge and a matching of the four original vertices of its lobe. This explicitly satisfies all demands. The code records the selected variable IDs.

Observed gadget matching sizes: all-one 39 of 40 required pairs; all-two 31 of 32; repaired demands 39 of 39. A renamed/reordered/duplicated-clause UNSAT version also passes. The two coincident-support controls return UNKNOWN; direct enumeration confirms SAT and UNSAT respectively. Malformed repeated-name clauses return UNKNOWN.

Python 3.12.14, NetworkX 3.5, deterministic exhaustive mode, no seed. One execution completed within the 30-second process cap. Matching-module SHA256: 22fdd4ab72cff786e824b11ae816841a279b756e992228249dd297c220f50bc1. Script SHA256: f194e3e26f623fb9006973a6544748661d6ba588e6b03ba13934345023d42dc7. No compiled-input SAT test, full target parser, formal build, TM simulation or physical-memory benchmark was performed.

## Encoding and same-execution ledger

Keep the finite-alphabet single writable tape, one local head, origin output, and origin-anchored occupied-span convention. Input, copies, addresses and work are charged; no external input oracle or free clock. Minimum-description CM describes complete configurations given the fixed A, without free original input or time.

For c source clauses and d occurring variables, r is the least odd integer greater than c, at least three:

    n0=d+(10c+1)r+2, m0=(20c+4)r,
    n=n0+m0+3, m=2m0+4, w=ceil(log2(n+1)),
    N=3n+2+2 floor(log2(m+1))+3m(w+1)+w.

This is unary n, gamma(m+1), ordered signed triples, two n-bit witnesses and release ID. The source-to-target Boolean compiler is inherited from Construction, with existential correctness, not a parsimonious count claim. Strict symmetric C, ordered R and historical S/Q are not substituted.

Petersen sources have c=50,d=15,n=76775,m=102412,N=5760624. Three-lobe sources have c=80,d=24,n=194834,m=259852,N=15396120. These lengths were computed, not materialized or experimentally solved as target formulas. In general c>=5q and N=Theta(c^2 log(c+1)) under dense source naming d<=3c.

The conservative peer ledger survives this audit: authentication and exact regeneration O(N^3); grouping/occurrence checks O(c^2) record operations; classical matching O(q^4) operations and O(q^2) index entries; O(log N) bits per index, giving O(q^2 log N)=O(N) storage in THIS encoding. Indexed shuttling costs at most O(N^2) physical transitions per operation. Since q^4=O(N^2), total T=O(N^4), S=O(N). This translates the classical algorithm, not the Python library's implementation.

Initialization, failed structural tests, representation changes, relocation, copies, cache maintenance, contraction/expansion records, real reads and address arithmetic, cleanup and output fit that same execution. Physical CM is O(N^5) by summing actual spans. Separately replay from I and t gives O(N+log(T+2)) bits per complete configuration, hence descriptive CM O(N^5). The graph memory bound is not O(M) for the much shorter source length M. Source-to-target production, when requested, is separately charged O(N^3) with O(N) span. General fallback remains exponential, e.g. T=O(2^n N^3), S=O(N), and either CM separately O(2^n N^4). This is not a polynomial algorithm for every input.

## Actual decoder and first open premise

After the paid computation A can erase scratch and source, retain the decision Y in an origin cell, and enter a fixed READY state before reading that bit. Use equal prior probability on the three-lobe all-one input and repaired SAT companion, which have the same target n,m,N. U=Y; B gives the public pair, distribution and fixed program; Pi is that actual one-bit read; E contains exactly that transition. Identity decoding is prefix-free, b=1,h=0,rho=1. The shared inequality proves one bit of work. Erasure and head positioning are paid in the prefix. Recounting that event j times raises rho to j. Supplying Y freely in B gives zero demand. No solver must return every odd-set certificate or reconstruct all demands after caching.

For fixed T<=KN^a the required net compulsory entropy must exceed b rho K N^a on the same execution. S=O(N^a), CM_phys=O(N^(2a)), CM_min=O(N^(a+1)) stay distinct. The count-map circuit ceiling is a separate output contract. The original permutation control retains its internally reviewed N^2 time/N^3 cumulative baseline and static N^2/8,N^3/27 demand ceilings.

The first unresolved constructive implication is **uniform, paid acquisition of a tractable residual decomposition covering every valid input with polynomial total failed and successful work**. The audit validates neither a logarithmic conditioning set nor a polynomial UNSAT frontier. On the lower-bound side, actual recurring opposite-label obligations must survive this legal matching and caching path. No graph width, odd cycle, rejected pivot search or count of possible cuts proves such recurrence.

DISJ/equality and same-execution DTISP: PASS scoped. Deterministic replay: PASS as an upper bound, not a lower bound. Relativization, Natural Proofs and algebrization: no bypass or unrestricted separation claimed. Affine/Tseitin, complement, private-leaf, forced-domain, witness and shared-computation controls remain permitted.

## Fresh sources and searches

1. Tutte, *A Short Proof of the Factor Theorem for Finite Graphs*, Canadian J. Math. 6 (1954), 347-352, published version pp.348-349. Finite graphs, parallel edges allowed, prescribed positive demands <= degree. Read the incidence construction and perfect-matching criterion. [Primary PDF](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/3785657C35F370E32E5AEAFC3D1B84CE/S0008414X00023774a.pdf/short_proof_of_the_factor_theorem_for_finite_graphs.pdf).
2. Edmonds, *Paths, Trees, and Flowers*, Canadian J. Math. 17 (1965), 449-467, pp.451-452 and maximum-cardinality algorithm. Read the polynomial-work/quadratic-memory statements for finite general graphs; no SAT completeness theorem imported. Michigan mirror timed out; publisher PDF succeeded. [Primary PDF](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/08B492B72322C4130AE800C0610E0E21/S0008414X00039419a.pdf/paths-trees-and-flowers.pdf).
3. [NetworkX 3.5 primary API documentation](https://networkx.org/documentation/networkx-3.5/reference/algorithms/generated/networkx.algorithms.matching.max_weight_matching.html), exact installed version and local matching-module digest above. Used for executable validation, not a kernel certificate.
4. Pinned Discovery report/code/raw and Construction's [degree-flow report](../charged-construction/PNP_Charged_construction_2026-11-21_233100_Degree_Flow.md). The prior exponential audit was read, not rerun. Project search '"Petersen" "matching"' found historical Tseitin/Petersen reports, not this source-level executable comparison; no novelty in graph matching is claimed.

Fresh literature queries: “Edmonds 1965 paths trees flowers matching polynomial algorithm Tutte odd components theorem pdf”; “NetworkX max_weight_matching blossom O number nodes 3 integer weights”. These support the actual primitive and locate the odd-set control, rather than import an online or fixed-DAG lower bound.

Fresh GitHub query '"perfect matching" "blossom"' covered anthropics, openai, xai-org, google, google-research and google-deepmind. Anthropic, xAI, Google Research and DeepMind returned no hits. Google succeeded after one 429 retry. Read lines1-100 of [OR-Tools matching tests](https://github.com/google/or-tools/blob/4782dbd0aa85621c8115cf33de1574a2e6757004/ortools/graph/perfect_matching_test.cc) at 4782dbd0aa85621c8115cf33de1574a2e6757004: integer-overflow and infeasibility statuses are distinct. No OR-Tools build or code import. OpenAI again surfaced matching preprint excerpts at 4eaee87548250b2682affda7d05d947c05554bae, including randomized capped search; the immediately prior log already reviewed that scope, so no redundant deep review or theorem import was made. Two web fallback queries with the same terms and six namespace restrictions found the same header/preprint, without an applicable new deterministic SAT theorem.

Official ownership was freshly checked using verified [Anthropic](https://github.com/anthropics) and [OpenAI](https://github.com/openai) profiles, [xAI release](https://x.ai/news/grok-os), [Google organization guidance](https://opensource.google/documentation/reference/github/where), [Google Research resources](https://research.google/resources/) and [DeepMind Tracr release](https://deepmind.google/research/publications/22295/). Negative results are bounded coverage statements.

Only selected files are present locally, not a full checkout; manuscript preflight and LaTeX compilation were not run. No schedules, identities or TMR ownership changed.

**Smallest corrected statement and next dependency:** preserve Discovery's polynomial shortcut on its authenticated distinct-support class, with UNKNOWN outside admission. Discovery/Construction own paid all-input decomposition or a counterexample to its precisely fixed acquisition rule. Accounting receives the unchanged same-encoding O(N^4)/O(N)/O(N^5) ledger; Bounds and Synthesis receive the one-bit cache boundary and the open recurrence/coverage alternatives. External independent review remains pending. P versus NP remains OPEN.
