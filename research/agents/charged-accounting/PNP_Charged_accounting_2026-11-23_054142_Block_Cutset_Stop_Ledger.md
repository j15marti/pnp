# Block cutsets and a stopped conjunction ledger

23 November 2026, 05:41:42 PST. PNP Charged Accounting.
BLOCK-CUTSET-STOP1 within DYNAMIC-COMPATIBILITY-OBLIGATION1.
PROVED/EXACT for the specified deterministic decision implementation and source prior. Independent review pending. P versus NP OPEN.

The new result is an accounting refinement of Discovery's [cutset algorithm](../charged-discovery/PNP_Charged_discovery_2026-11-23_044849_Cutset_Decision_Transfer.md). The existing [block-local hub theorem](../../main/block_orbit_20261122/Block_Local_Hub_Theorem.md) already proves the articulation composition principle. This report applies that principle to the new cutset parameter, then proves the exact entropy of an actual stopped aggregation record. It makes no novelty claim for block decomposition or cutset conditioning.

Fix a single uniform deterministic decider A for valid positive Boolean exact-one triple lists. Use the sole finite-alphabet read/write tape, unit head speed, input-inclusive live span and origin-terminated output of the transport report. For every authenticated triangle bundle with finite simple quotient Q, obtain the matching signs and gains by the paid recognizer and affine conversion. Inconsistent signs give UNSAT. Consistent signs give x_u−x_v≠g_uv over F3. No externally imposed clause-processing order, locality, graph-evaluation schedule or free source access is assumed.

The four falsifiers are conflicting articulation values despite feasible blocks, multiplying independent cutset search spaces, decoding unread verdicts from a stopped record, and claiming that a cheap suffix makes preprocessing free. The following composition proof, sum bound, transcript fibers and full ledger address them.

## Composition and the upper bound

For each nontrivial block B, including bridges, run Discovery's deterministic spanning-forest endpoint rule inside B. Let its computed cutset size be s_B. Isolated vertices require no search. Within a feasible gain block, adding a common residue to all x_v preserves every difference. Therefore any chosen value at a single articulation can be attained. Root the block-cut forest and successively translate a feasible coloring of each child block to match its parent at the unique shared articulation. No other already-colored vertex is shared. This proves global feasibility if and only if every block is feasible. It also proves that a block's feasible boundary domain is all three values, or empty. Unary pins or multi-vertex separators would require different boundary records.

Define W(Q)=1+sum_B 3^{s_B}. A authenticates the original source once, computes the block decomposition and solves each block using the exact cutset algorithm. It can stop at a failed block, or compute all block verdicts for the explicit suffix experiment below. The admitted same-run bounds are

    T=O(W(Q) N^7),     S=O(N²),
    CM_phys=O(W(Q) N^9),     CM_min=O(W(Q) N^8).

There are at most k nontrivial blocks. Every quotient edge belongs to exactly one block and total vertex occurrences across blocks are O(q+k). Thus the topology, local assignments, offsets and table references can be stored within the inherited O(N²) span, and one workspace is recycled. The factor is a sum. Cartesian products of choices in distinct blocks are unnecessary for the Boolean conjunction.

The source counts remain n=33q+9k, m=21q+9k and N=n+2+2 floor(log2(m+1))+3m ceil(log2(n+1)). All declaration and row bits are charged. Recognition, failed patterns, discovery of blocks, sign/gain conversion, copies, source retention, reverse labels, queues, table allocation, resetting, addresses, caches, return to origin and output are included. A DFS decomposition or polynomial repeated connectivity scans fits the prior O(N^4) indexed-bit budget; conservative O(N³) sweeps simulate its accesses. Each cutset branch fits that budget. Since W≤1+k3^q, log W=O(N), deterministic source-and-time replay yields the stated minimum-description bound. Off-family inputs use the original exact enumeration, with O(2^n N^7) time and the corresponding exponential cumulative bounds. This remains a uniform globally correct algorithm. The theorem gives no polynomial all-input cap.

If every computed s_B≤d log2(N+2) for fixed d, then W=O(N^{1+d log2 3}), so admitted total work is polynomial even when the sum of the cutsets is linear in N/log N. This extends the parameter accounting; the previous global-cutset bound remains a correct upper bound.

## Connected source family with independent block verdicts

Take b copies of K4 sharing a single common vertex 0 and otherwise disjoint. Orient each edge by increasing local vertex labels and put the three common-vertex edges first in each block's order. The block cutsets have size two, the global selected endpoints have size 2b, and r=k-q+1=3b. The dimensions are

    q=3b+1, k=6b, n=153b+33, m=117b+21,
    W=1+9b, N=Theta(b log(b+2)).

For each block independently choose one of two actual rotation-label patterns. With all gains zero, K4 is UNSAT. With only the edge from the common vertex to its first private vertex having gain 1, it is SAT: assign residues 0,0,1,2 in that order. Each block has a freely selectable root color by translation. The matching p(i)=i+g is always even. Hence every vector D of b block verdicts is realized by a genuine encoded source of identical dimensions, and the whole source is SAT exactly when every D_i=1. Take the uniform prior over these 2^b sources. This is randomness in the input only. Both labels occur.

The sum bound gives polynomial total decision work on this connected family. The global factor 3^{2b} is an avoidable upper-bound factor, not a lower bound. The construction illustrates a resource comparison on the same encoding.

## Actual events, prefix-free records and missing obligations

Define A's selected branch to compute all block verdicts first and prepare a compact cache. A pays to relocate the b verdict bits into cells 1,...,b, marks cell 0 as the output origin, writes a sentinel at b+1, and removes other input and work. The head starts at cell 1 in fixed SCAN control. This cleanup is a chosen program phase, with its complete polynomial cost included above. It is not required of arbitrary solvers.

A scans the cache until the first zero, or until all b bits have been read and the sentinel is reached. It remembers the verdict in finite control, returns to the marked origin and outputs the answer and terminator. Bits are left intact, including unread bits. Let L be the number of verdict cells read. Define U as the stopped word D_1...D_L. B contains A, b, the public quotient, the two block patterns, the uniform prior and the canonical layout, but no selected input or cache content. E contains precisely those L actual cache-bit reads. It excludes the return scans and sentinel test. Pi is the chronological read word. The decoder returns Pi.

For fixed b, the possible words are 0,10,...,1^{b-1}0,1^b. No word is a proper prefix of another, so framing overhead h=0. Each actual charged transition reads one Boolean symbol, giving capacity b_event=1 and reuse rho=1. (The symbol b_event distinguishes capacity from the number b of blocks.) Each word w has probability 2^{-|w|}, with 2^{b-|w|} compatible full verdict vectors. Therefore

    H(U|B)=E[L]=sum_{i=1}^b 2^{-(i-1)}
                 =2−2^{1-b}.

This proves the requested event inequality E[T]≥H(U|B)/(b_event rho) on this execution. No free stopping index is supplied. The prefix code determines its own end from the first zero or the known maximum length. Repeatedly indexing this same record j times requires rho=j.

The full vector D has entropy b, but

    H(D|U,B)=b−E[L].

For b>1, the record 0 is compatible with 2^{b-1} inputs. Thus it cannot decode D. The return movement can reveal only the already observed positions and control and never scans the unread suffix. Earlier acquisition may have exposed D, and the retained cache still stores it. Neither is freely included in Pi. A full-configuration decoder would receive that information explicitly and its conditional entropy would change accordingly.

The suffix costs T_suffix=Theta(L+1), physical span Theta(b+1), and CM_phys,suffix=Theta((b+1)(L+1)), because all cache bits remain. Thus expected suffix time is Theta(1) but expected physical cumulative cost is Theta(b+1). Its worst-case time is Theta(b+1), with quadratic worst-case suffix cumulative cost. These statements use the same execution and its retained storage. They do not erase the polynomial acquisition cost.

One can instead form a running AND while computing block verdicts and immediately cache the final decision. This removes the separate cache scan entirely. Hence neither reconstruction of all D nor even this stopped-word obligation is compulsory for every correct solver. A universal claim still needs an independently justified decoder after arbitrary paid joint preprocessing.

## Caps, controls and finite evidence

For T≤KN^a, a≥1, the stopped-record demand is below two bits, while even the full b-bit cache is O(N). No polynomial exponent is excluded. General ceilings stay S=O(N^a), physical CM O(N^(2a)), minimum-description CM O(N^(a+1)), and separate count-map circuit size O(N^a log N). The internally reviewed single-tape map/permutation transport theorem retains its tight quadratic-time/cubic-cumulative calibration and Dh≤N²/8, Dh²≤N³/27 static ceilings. Boolean source feasibility remains separate from counting.

DISJ/full-state sanity PASS within scope. Simultaneous DTISP PASS as same-execution upper accounting. Deterministic configuration gate PASS through replay. Relativization, algebrization and Natural Proofs are not separation mechanisms used here. Affine translation, sharing, source relocation, caching, complement and recomputation remain legal. The articulation argument uses unpinned single-vertex interfaces; forced-domain and two-variable interfaces are explicit falsification controls for extending it.

[Code](../../../experiments/dynamic_accounting_block_stop_20261123.py) and [raw](../../../results/raw/dynamic_accounting_block_stop_20261123.json). Run python experiments/dynamic_accounting_block_stop_20261123.py. The new exact rational audit checks all 2,046 block-label vectors for b=1,...,10, prefix freedom, Kraft equality, verdict preservation, fiber sizes, expected length and the entropy formula. It exercises the new stopped conjunction record. It does not rerun Discovery's forest solver tests or claim to instantiate a native tape. Source semantics and block composition are proved above using the existing compiler and original reports. Parser, full-checkout preflight, native tape and formal-kernel checks were not run; state was recovered through connected reads.

Next dependency for Bounds and Synthesis: identify a compulsory distinction inside an irreducible block that survives paid cutset conditioning and direct verdict aggregation. Redteam receives the proposed full-vector decoder from the stopped word as a concrete counterexample target. Discovery receives the sum-over-blocks cost refinement. General P versus NP remains OPEN.

## Recovery and bounded searches

Recovered at e949c765d87f2ae141d1b6e21c7b4bfa50ee443f. Read the operating guides, research skill, current dynamic directive, transport model/encoding and static ceiling, applicable T5 definitions, all six handoffs, latest Accounting normalization and Discovery cutset reports, original block-local hub theorem and latest issue 324 entries. The earlier block theorem already contains the structural composition result and sum accounting for its hub parameter. This report specializes the newer cutset procedure and adds the exact stopped record, without claiming the old decomposition as new.

Fresh literature query “Dechter Pearl constraint satisfaction biconnected components cycle cutset 1987” found Network-based heuristics for constraint-satisfaction problems, Artificial Intelligence 34 (1987). Its author PDF had no readable text in this session; a screenshot request did not provide inspectable page content. The directly readable primary IJCAI 1985 paper, The Anatomy of Easy Problems: A Constraint-Satisfaction Formulation, Theorem 3 and final cutset discussion, verifies tree processing and the domain-size-to-cutset-size factor used in the inherited algorithm. The block gluing and entropy proofs are given here. [Primary 1985 paper](https://ijcai.org/proceedings/1985/0217.pdf), [1987 author PDF](https://ics.uci.edu/~dechter/publications/r3.pdf).

Fresh GitHub queries org:ORG "biconnected" "constraint" returned counts anthropics 1, openai 0, xai-org 0, google 1, google-research 0, google-deepmind 1. Google initially rate-limited and succeeded on retry. The Anthropic result was mockturtle/lib/nauty/testg.c and DeepMind's was open_spiel/games/hive/hive_board.h; these were search leads only. The Google source was inspected at commit 1fc9e44a77e27b5c293b859a26dc3180fec45fb1. Its cp_model_solver_helpers.cc decomposes an LP constraint-variable graph into connected components and leaves biconnected processing as a TODO. It supplies no proof of the gain-block theorem. [Pinned code](https://github.com/google/or-tools/blob/1fc9e44a77e27b5c293b859a26dc3180fec45fb1/ortools/sat/cp_model_solver_helpers.cc).

Supplemental web searches combined those six official organization site filters with “biconnected” and “constraint”. Ownership was checked through organization pages and vendor links: [Anthropic](https://github.com/anthropics), [OpenAI](https://github.com/openai), [xAI release](https://x.ai/news/grok-os), [Google organization guidance](https://opensource.google/documentation/reference/github/where), [Google Research](https://github.com/google-research), [Google DeepMind](https://github.com/google-deepmind). No external solver is imported as an asymptotic lower bound. Manuscript ownership and scientific scopes remain those in the recovered directive.
