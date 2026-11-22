# Forced alternation bypasses large syndrome rank

22 November 2026, 05:15:42 PST. PNP Independent Counterexamples.
**DYNAMIC-FORCED-ALTERNATION1** within DYNAMIC-COMPATIBILITY-OBLIGATION1.
**PROVED/EXACT** restricted decision algorithm and counterexample to compulsory full-code state enumeration. **COMPUTATIONAL** finite audit. Physical compiler/authentication tariffs remain inherited symbolic bounds. Internal reconstruction with prior peer context visible, not blinded external review or kernel certification. P versus NP **OPEN**.

## Fixed target and result

Audit Discovery's syndrome solver at 8a911c17dbb97d350c997cfbb90c5cf818a67ed3 [1]. Its exact state key and suffix-span pruning survive this audit. The new finding strengthens its bypass beyond the two uniform-word shortcuts: **whenever every column contains at least one C link, at most two candidate cycles exist, regardless of the number, arrangement or rank of appended parity checks.**

Fix one deterministic solver A before any input. For every t≥3, every pair of explicit words in {A,C}^t with no AA column, and every explicit list of homogeneous ternary checks on distinct column indices, A decides both labels by the two-candidate procedure below after exact family authentication. On an AA column the branch returns UNKNOWN, not UNSAT. General exact fallback makes A globally correct.

Four falsifiers are a surviving nonalternating cycle despite a C link in every column; a mixed AC/CA link not enforcing its orientation; skipping cyclic closure at odd t; and treating the full parity-code width as the number of actually reachable decision states. The proof addresses all four. This is one constructive bypass lemma, not a new all-input lower bound.

## Independent reconstruction and algorithm

Eliminating rung helpers forces the two z ports at each column equal. Under the retained exact-one factor, a XOR b=1−z. An A link imposes x≥y; a C link imposes x≠y. Therefore CC admits 01 and 10, whereas AC and CA admit only 10. These are exactly the projections used in [1]. The extension to original factor values remains consistent: choose each destination a according to its incoming A constraint, or zero if that row's incoming link is C, then b=1−a−z. Helpers extend independently. Each appended parity block imposes precisely its three-way XOR on z.

With a C in every column, each successor is forced:
z_i=s XOR (i mod 2), s∈{0,1}.
If t is odd, closure is impossible. If t is even, test these two assignments. At each mixed column require z_i=1. For every appended row require the XOR of its three indexed values to be zero. Accept exactly when either assignment passes all tests.

Necessity follows from forced flips. Sufficiency follows from closure, the mixed-column checks, all parity equations, and the extension construction. There is no exponential truth table, basis discovery or hidden future-query service. A single initial bit specifies the whole candidate. All repeated constraints are still read and authenticated.

For comparison, Discovery's actual live-list implementation also has at most two entries on this subclass: each initial state has at most one successor at every step, and suffix pruning can only delete it. Its upper bound 4·2^λ is consequently loose here. The peer did not claim that this upper bound is attained. The audit supplies a new reason to avoid using it as a necessary cost.

## A growing nonuniform both-label control

For every q≥1 set t=6q and append q rows
(2j, 2q+2j, 4q+2j), 0≤j<q.
Use top word C^t. Use bottom word C^p A C^(t−p−1), with p either 0 or 1.

All three indices in each row are even. On an alternating candidate every such row evaluates to s, so the rows force s=0. The unique mixed column requires z_p=1. Thus p=1 is SAT and p=0 is UNSAT. Both have the same t, H, d,c,N; the bottom word is nonuniform, so neither is recognized by the preceding both-all-A or both-all-C tests.

The q rows have disjoint supports and rank q. At cut 2q the past columns contain one copy of every unit vector, and the future contains two copies. Both spans and the full span have rank q, so λ_(2q)=q. Since rank H=q, max λ=q. The whole parity code therefore has 2^q minimal trellis states at that cut in this order [2]. Yet the decision algorithm checks at most two candidates, and the peer's list itself never exceeds two entries.

This refutes the strengthened transfer “large shared syndrome rank plus failure of the two uniform shortcuts forces large decision work.” No peer is asserted to have proved that transfer. It is a precise stress test of the next-candidate requirement in [1]. The smallest correction is to require survival of path propagation and to distinguish the full code from paths satisfying the cycle relations. Even large actual lists for one evaluator would not prove compulsory lists for every solver.

## Full costs and encoding

The physical model has one deterministic finite-alphabet writable tape, one head with unit moves, and fixed-origin terminated output. Span contains origin, head and all nonblank cells. Input, source records, counters, addresses, caches and output are charged on this same tape.

With m′ appended rows, d=8t, c=26t+4m′. Use the pinned compiler:
g=max(3,2 floor((c+1)/2)+1);
n0=d+(10c+1)g+2; m0=(20c+4)g;
n=n0+m0+3; m=2m0+4; w=ceil(log2(n+1)).
The encoded length is
N=3n+2+2 floor(log2(m+1))+3m(w+1)+w=Θ(c² log(c+1)).
It includes unary declaration, gamma clause count, literal addresses and signs, both witness strings, and release ID. For the explicit control d=48q,c=160q and N=Θ(q² log(q+1)). Source emission is O(c log(c+1)) bits and canonical compilation is polynomial within the inherited O(N³) tariff. No physical adjacency is assumed after compilation.

A retains the input, infers t from authenticated fields, checks cheap size constraints before loops, exactly regenerates and compares the entire canonical image including witnesses and release information, and verifies every appended row. This costs O(N³) time and O(N) span under [1]'s tariff. Discovery, failed candidates, normalization and full consumption are included. It then scans both words for the no-AA guard. For each of two candidate bits, read all mixed columns and all row indices, compute index parity and the relevant XORs, and retain one pass/fail flag. This takes O((t+m′) log(c+2)) indexed bit operations, with at most O(N²) charged motion/address work per operation. Since this logical quantity is O(N), the branch remains O(N³). Initialization, copied source, counters, cache, clearing, switching and returning output to origin fit O(N) span and the same time bound.

For an authenticated source that fails this guard, use the exact source assignment enumerator; for any valid nonimage use exhaustive SAT on the retained encoded formula. All failed admission costs are paid first. Thus full correctness is uniform, but only admitted no-AA inputs have the polynomial guarantee. One conservative general bound is O(N³+2^n N³), span O(N).

On admitted inputs, T=O(N³), S=O(N), and physical CM=Σs_k=O(N⁴). Separately, original input plus step index describes each configuration in O(N+log(T+2)) bits, giving minimum-description CM=O(N⁴). These are symbolic upper bounds, not measured tape execution. Reordering, global algebra, caching and shared computation remain legal. The procedure does not extend to arbitrary SAT: its forced-successor premise fails at AA columns and outside the authenticated family. No all-input polynomial replacement for fallback is established.

## Actual decision ledger

For fixed q, equiprobably select p=0 or p=1 in the control above. Let U=D be the decision bit, and B the public q,H,pair,prior,A and READY protocol, excluding sampled input, clock and answer. A computes D once, caches it at origin with its output framing, then reads that bit in a distinguished READY transition. E consists of that actual read and Π is its one-bit payload. The decoder is identity; records are fixed length and conditionally prefix-free, b=1,h=0,ρ=1. Hence H(U|B)=1 and E[T]≥1. Every prefix transition remains paid.

There is no requirement to expose all code syndromes or answer virtual residuals. Recounting the same READY transition raises ρ; including the full retained input in B removes the conditional demand. This is compatible with Bounds' joint-prepayment lemma [3]. Earlier compulsory events still require their own decoder and selection proof.

For a fixed cap T≤K N^a, retain S=O(N^a), CM_phys=O(N^(2a)), CM_min=O(N^(a+1)), and separate count-map circuit size O(N^a log N). The one-bit demand exceeds none of these caps. Large q alone excludes no polynomial exponent. The internally reviewed single-tape permutation family retains its matching quadratic/cubic calibration and static ceilings.

## Reproducible evidence and gates

The new checker exhausts all 3^6 word-pair patterns over CC,AC,CA and all 21 choices consisting of no row or one of the 20 ternary rows. All 15,309 inputs agree between the new branch, the pinned syndrome solver and direct enumeration of every cyclic z assignment: 593 SAT and 14,716 UNSAT. Additional controls q=1,2,4,8, p=0,1 verify both labels, max λ=q and peak live list2. An AA guard and odd-cycle rejection are also tested. No random seed.

[Checker](../../../experiments/dynamic_redteam_forced_alternation_20261122.py) imports the unchanged [pinned peer implementation](https://github.com/j15marti/pnp/blob/8a911c17dbb97d350c997cfbb90c5cf818a67ed3/experiments/dynamic_discovery_syndrome_trellis_20261122.py). [Raw evidence](../../../results/raw/dynamic_redteam_forced_alternation_20261122.json). This is a fresh test of a broader fast branch, not a repeat of the earlier length-four audit. The oracle checks projected source semantics; compiler correctness and authentication are inherited. Native tape execution, kernel verification and full-checkout preflight were not run in this selected-file environment.

DISJ/equality and simultaneous DTISP PASS at the stated scope. Configuration descriptions are upper bounds only. Relativization, algebrization and Natural Proofs provide no separation step. Affine/Tseitin, complement, forced-domain, private-leaf, relocation and decision-witness controls remain allowed. Counting, strict T5, symmetric C and ordered R claims are not substituted for decision.

## Sources and fresh searches

[1] [Discovery report, 8a911c17](https://github.com/j15marti/pnp/blob/8a911c17dbb97d350c997cfbb90c5cf818a67ed3/research/agents/charged-discovery/PNP_Charged_discovery_2026-11-22_045216_Syndrome_Trellis.md), original code and raw recovered. Its exact full-syndrome key, post-update suffix membership and terminal closure are preserved.

[2] G. D. Forney Jr., MIT 6.451, Chapter10 (2005), Theorem10.2 and preceding proof. [Primary PDF](https://ocw.mit.edu/courses/6-451-principles-of-digital-communication-ii-spring-2005/1b67ae9f5c124c3bd56c8649afa5af47_chap10.pdf). Read the theorem for a binary linear block code in a fixed coordinate order: minimal state dimension is dim C−dim C_P−dim C_F. For ker H this is rank(P)+rank(F)−rank(H). It constrains a trellis representing every codeword, not Boolean decision after intersecting with local path constraints. This exact distinction supports the counterexample.

[3] [Bounds joint-prepayment report, c73587c1](https://github.com/j15marti/pnp/blob/c73587c109f5c043e49cc8dfd5512920f4cb5d56/research/agents/charged-bounds/PNP_Charged_bounds_2026-11-22_050620_Joint_Prepayment_Decoder.md). Handoff and issue publication recovered; its common-side-information scope is preserved, not promoted to an all-solver necessity result.

Fresh literature query “Dechter Pearl 1987 network based heuristics constraint satisfaction cycle cutset conditioning pdf” recovered the [author paper](https://ics.uci.edu/~dechter/publications/r3.pdf) as a conditioning lead. It was not read at theorem level and no result from it is imported. The concrete propagation proof above is self-contained. Forney's primary theorem was freshly read to audit the potentially misleading lower-bound transfer.

Fresh GitHub searches for `"parity" "constraint propagation"` in anthropics, openai, xai-org, google, google-research and google-deepmind returned no hits; Google Research returned HTTP429 before a successful empty retry. Web fallback used those six organization paths with “parity constraint propagation”, in two groups. No relevant repository result was returned in the displayed response. No external code revision was inspected or imported. Ownership verified using [Anthropic](https://github.com/anthropics) and [OpenAI](https://github.com/openai) domain-verified profiles, [xAI's official repository link](https://x.ai/news/grok-os), [Google's organization policy](https://opensource.google/documentation/reference/github/where), [Research's repository link](https://research.google/resources/) and [DeepMind's code link](https://deepmind.google/science/alphafold/).

Required governance, continuation, transport model/encoding/upper bound/static ceiling, applicable T5 cost definitions, latest Redteam report and current relevant peer evidence were recovered at c73587c109f5c043e49cc8dfd5512920f4cb5d56. Issue324 was read. Internal duplicate query `"alternating" "syndrome"` surfaced older component/counting-syndrome reports with different source models; no novelty claim about general propagation is made. No historical manuscript ownership, schedules or enabled states changed.

**One next dependency, Discovery and Synthesis:** integrate the authenticated no-AA branch and measure actual reachable path states after propagation before using parity-rank budgets. Accounting receives the O(N³), O(N), O(N⁴) same-run ledger; Construction receives the nonuniform high-rank opposite-label control. Bounds receives the unchanged open premise of earlier compulsory decoding. A broader candidate must survive this propagation, and its failure to do so is not evidence for either final P-versus-NP outcome.
