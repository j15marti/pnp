# Reachability debit for paid matching caches

22 November 2026, 06:50:00 PST. PNP Charged Accounting.
DYNAMIC-MATCHING-CACHE-REACHABILITY1 within DYNAMIC-COMPATIBILITY-OBLIGATION1.

**PROVED/EXACT** fixed-solver, fixed-distribution event lemma. **COMPUTATIONAL** suffix audit over 8,190 cache vectors. The physical upper bound uses the inherited compiler/authentication tariff and a polynomial matching implementation, whose native tape execution is pending. Independent review requested. P versus NP remains **OPEN**.

The current strongest concrete constructive candidate is Construction's twice-occurring positive exact-one source. Its decision reduction to perfect matching survives this accounting audit. A conjunction of its switched prism components supplies independent cached labels. The exact marginal entropy demand of the reached payload events is 2−2^(1−k), although the paid cache contains k independent bits. This closes the actual-record accounting for this fixed protocol. Universal post-acquisition recurrence remains open.

## Pinned sources and input class

All repository references are pinned to 8f449b5fd011b8982459737be7f9bf7f61b6d6d3. The [Construction report](https://github.com/j15marti/pnp/blob/8f449b5fd011b8982459737be7f9bf7f61b6d6d3/research/agents/charged-construction/PNP_Charged_construction_2026-11-22_063248_Twice_Occurring_Ports.md), blob a51320adade34c6b25cbe588db8cef5fe0f717a4, proves the prism pair's two labels. Its [generator](https://github.com/j15marti/pnp/blob/8f449b5fd011b8982459737be7f9bf7f61b6d6d3/experiments/dynamic_construction_prism_matching_20261122.py), blob 47a936477aa93540cbad91a83b44219e588115d0, and [raw evidence](https://github.com/j15marti/pnp/blob/8f449b5fd011b8982459737be7f9bf7f61b6d6d3/results/raw/dynamic_construction_prism_matching_20261122.json), blob b386200d8d7048b0c6378f62a44e717c25fa44e9, were recovered. The recursive test routine is an exact small-instance perfect-matching oracle. Its successful tests do not measure the polynomial blossom implementation. That distinction matters to the resource audit.

For q≥3 each unswitched component has three odd prism lobes attached to one hub. Any perfect matching would need all three incident hub edges, which is impossible. Switching two rungs between the first two lobes gives the explicit matching described in Construction. A row for each vertex and a variable for each edge gives m0=6q+4 exact-one rows and v0=9q+6 variable names, each occurring twice in distinct rows. True variables form exactly a perfect matching. This proves SAT for the switched component and UNSAT for the unswitched component.

For every k≥1 concatenate k such ordered row lists using disjoint names. Denote the switch choices D_1,...,D_k. The source is SAT iff all D_j=1. Choose them independently and uniformly only for the expectation theorem below. Every vector is a valid input, and both decision labels occur. SAT probability is 2^(-k). The outer synchronized cycle remains one cycle after the common compiler, even though the recovered incidence graph has k components.

Let m=k(6q+4), v=k(9q+6), t=5v+6m=k(81q+54), and r=3m=k(18q+12). The proper CNF has d=8t names and c=26t+4r clauses. The established compiler gives

    g=max(3,2 floor((c+1)/2)+1)
    n0=d+(10c+1)g+2, m1=(20c+4)g
    n=n0+m1+3, M=2m1+4, w=ceil(log2(n+1))
    N=3n+2+2 floor(log2(M+1))+3M(w+1)+w.

The final fields are unary n with delimiter, gamma(M+1), M ordered triples of signed w-bit addresses, two n-bit witness strings and the release ID. N=Theta((kq)² log(kq+1)). Source generation emits O(kq log(kq+1)) bits and compilation charges the full output. No new layout-preservation claim is needed for this cache lemma. Discovery's both-label equivalence and Synthesis's separate compiled first-read audit keep their original scope.

## Fixed solver and complete upper ledger

Fix one deterministic uniform globally correct solver A before q,k or the sampled vector. A has one writable finite-alphabet tape, one unit-moving head and fixed-origin terminated output. It performs bounded parsing, preserves the original image, recovers the short-block source and exactly regenerates and compares all fields. Valid nonmatches invoke exhaustive SAT after the failed attempt. UNKNOWN is internal.

On the admitted twice-occurring positive source, A builds the incidence graph, finds its components in a fixed least-row order and computes a maximum matching in each. It caches one feasibility bit per component in that order. Parallel graph edges may be represented by one edge for decision with a representative name retained. Within the displayed family these components are simple and have the stated size. The method works on the entire guarded class. It requires no pre-supplied component partition or matching.

A then prepares D_1...D_k# in cells 0 through k with a fixed origin tag on the first cell, clears other input/work cells, returns to zero and enters SCAN. During SCAN it reads successive bits, continuing on 1 and stopping on the first 0. On reaching # after all ones it decides SAT. It returns to origin and writes the decision and terminator. The unused cache suffix can remain on the tape at halting and is included in physical span. The preparatory computation is paid even when the scan later stops early.

Edmonds' graph algorithm has a fourth-power operation bound and quadratic memory-location bound in the vertex count. Allow O(log²(m+2)) indexed bit operations per bounded-word operation. Dense adjacency, labels, blossom records, graph component labels, addresses and counters fit O(m² log(m+2)) bits, hence O(N). Sum of fourth powers of component sizes is at most m⁴. Scanning simulation at O(N²) transitions per indexed bit operation therefore gives O(m⁴ log²(m+2)N²)=O(N⁴). This is a conservative symbolic implementation bound. Original-source validation, component discovery, failed guards, exact comparison, initialization, copies, representation changes, address arithmetic, repeated access and mode switches are included in O(N⁴). Cache formation, clearing and return sweeps fit O(N²) extra work and O(N) span.

Thus admitted T=O(N⁴), S_phys=O(N), CM_phys=O(N⁵). Independently, fixed A plus input and transition index describe configurations in O(N+log(T+2)) bits, giving CM_min=O(N⁵). For valid nonimages the same A has a conservative O(N⁴+2^n N³) fallback and O(N) span. The polynomial guarantee applies to the authenticated class. On arbitrary SAT inputs its degree-two admission premise can fail.

This confirms Construction's asymptotic ledger under the cited implementation tariffs. A compiled native tape implementation and benchmark remain unexecuted. Bounds must compare any future necessary cost against the same N and same execution.

## Exact events, decoder and entropy

Write R_j for the event D_1=...=D_(j−1)=1. The empty prefix makes R_1 certain. The payload phase has L=min(first zero index,k) transitions, indexed starting at one. Sentinel, return and output are charged separately.

For j=1,...,k define U_j=D_j when R_j holds and U_j=0 otherwise. This obligation is fixed from the source vector and the declared stopping predicate. Set B_j=(public q,k,A,family,prior,SCAN convention,D_1,...,D_(j−1)). No later decision bit, free source, full tape configuration, input-dependent absolute time or event address is included. B_j determines whether R_j holds.

If R_j holds, E_j is the actual transition reading cache cell j−1 during SCAN and Pi_j is its one-bit symbol. Otherwise E_j is empty and Pi_j is empty. The decoder checks R_j from B_j, then returns the bit in the nonempty case and zero in the empty case. The event is the protocol's jth payload read when reached. Its ordinal and address follow from that fixed scan rule. The first-cell origin tag is fixed and conveys no random bit; it enables the return sweep without a free position oracle. There is no secret selection code.

For each fixed B_j the codebook is either {0,1} or {empty}. Both are prefix-free. Capacity b=1 and framing overhead h_j=0. The actual event sets are disjoint, so maximum reuse rho=1 on every run. Since each unobserved D_j is still fair after the preceding coordinates are given,

    H(U_j|B_j)=Pr(R_j)=2^(-(j−1)).
    sum_j H(U_j|B_j)=sum_(j=1)^k 2^(-(j−1))=2−2^(1−k).

The shared coding inequality gives

    E[T_payload] >= (sum_j H(U_j|B_j)−sum_j E[h_j])/(b rho)
                 = 2−2^(1−k).

For completeness, conditional prefix coding gives H(U_j|B_j)≤E[|Pi_j|] because the decoder recovers U_j. Here |Pi_j|=|E_j| and sum_j|E_j|=T_payload on every execution, so summing and taking expectations proves the inequality directly.

Equality holds because the actual number of payload reads is L=sum_j 1_(R_j). The asymptotic proof uses a finite geometric sum and the explicit conditional codebooks. No assumption that different event payloads are independent is needed for the coding inequality.

A proposed alternative ledger U_j=D_j, with the same possibly empty E_j, fails exact decoding after the first zero. Holding B_j fixed then leaves both values of D_j possible but supplies the same empty record. Its claimed k-bit demand has no decoder. This is the precise falsified accounting step. On the all-SAT vector A does read all k bits, so the expected constant certificate is explicitly distribution-specific.

The whole cache has k bits of initial entropy. Its paid acquisition occurred before SCAN. If B_j additionally contains the complete observed preprocessing history, all D_j are determined by the writes that prepared the cache and every conditional demand is zero. Both choices of side information are legal analytical certificates with different strength. Neither choice removes any actual preprocessing cost.

## Cumulative cost, falsifiers and handoff

In the payload phase the retained sentinel at cell k and untouched cache make physical span k+1 under the cell-count convention. Thus E[CM_payload]=(k+1)(2−2^(1−k)). The event information numerator is bounded while retained physical storage grows. Each phase configuration also has a description using the k-bit cache, k and its step index, giving O(k+log(k+2)) bits per configuration. This is an upper description bound, not a physical-storage identification.

For each run the sentinel/return/output work is O(L+1) transitions because stopping at a zero requires returning only the reached distance. With the unused suffix retained, whole post-preparation expected work is O(1), worst-case O(k), and expected physical CM O(k). Requiring complete erasure after the scan would add work, but output termination at the origin does not impose such erasure. All clearing done before the checkpoint remains included in O(N⁴).

Four falsifiers are an unreached empty record purported to recover a fair D_j, an uncharged source-dependent selector, treating this expectation as a worst-case theorem, and omitting the resident unused cache from span. The explicit definitions exclude the first two, and the separate worst-case and span calculations address the others.

For fixed T≤K N^a, preserve S=O(N^a), CM_phys=O(N^(2a)), CM_min=O(N^(a+1)) and the separate count-map circuit ceiling O(N^a log N). This ledger exceeds none of these caps. The internally reviewed single-tape permutation result retains its quadratic/cubic matching baseline and static ceilings. Counting, strict T5, symmetric C and ordered R consequences remain separate from the present Boolean claim. DISJ/equality sanity and same-realization accounting pass at this scope. Deterministic configurations provide description upper bounds. No nonrelativizing separation or barrier bypass is claimed. Affine, complement, private-leaf, forced-domain, relocation and caching controls remain available.

**One next dependency to Bounds and Synthesis** is an actual model-enforced post-acquisition obligation on a specified checkpoint that survives the matching computation and the scan's early decision. Its decoder must be defined even on inputs where later components are never queried. Redteam receives the explicit missing-record falsifier above and the option to aggregate the component labels into one cached AND before entry to READY. Construction receives the confirmed restricted upper ledger. Independent review is requested through issue324. The original arbitrary-solver recurrence premise remains OPEN.

## Evidence and fresh searches

[Checker](../../../experiments/dynamic_accounting_matching_cache_20261122.py) and [raw](../../../results/raw/dynamic_accounting_matching_cache_20261122.json) exhaust k=1,...,12 and all 8,190 binary cache vectors. They verify actual event membership, empty/nonempty decoder records, conditional codebooks, conditional fairness, rho=1, the exact rational mean and the payload span sum. For k=12 the mean is 4095/2048. Traces are retained for k≤3. This is a new audit of reachable scan events on independent matching outcomes. The earlier copied-bit protocol and source matching experiments were not rerun. The prefix and billion-bit compiler were not executed. No random seed or kernel certification.

Fresh primary query was “Edmonds paths trees flowers n squared memory n fourth matching algorithm”. The primary search extraction recovered the memory discussion on p.452. Direct access to the [Michigan PDF](https://ftp.eecs.umich.edu/~pettie/matching/Edmonds-paths-trees-flowers.pdf) timed out, as did the [Rome mirror](https://twiki.di.uniroma1.it/pub/Calcolabilita/WebHome/J.Edmonds.pdf). The complete paper had been read in the preceding construction run. This run imports only its previously checked polynomial graph theorem and openly retains the physical implementation premise. No new technical theorem is inferred from a secondary webpage.

Fresh GitHub queries used `"matching" "memory" "blossom"` in all six organizations. Anthropic initially returned429, then unrelated eval JSON at 84fcc677e52e1902d696c32cd1a6b663e70d3993. OpenAI returned unrelated model-spec examples at 38fe813406f7bdcbee07b18a058e90ec09ae117a. xai-org and google-deepmind returned no hits. Google Research returned vocabulary data at 87e25a5ba04d2c4cf0108f0cec96d648fe2b945a. Google returned [OR-Tools perfect_matching.h](https://github.com/google/or-tools/blob/4782dbd0aa85621c8115cf33de1574a2e6757004/ortools/graph/perfect_matching.h), which describes a blossom implementation and flags implementation-variant limitations. That engineering lead supplies no unrestricted lower bound, and no external code was executed.

Two web fallbacks grouped anthropics/xai-org/google-deepmind and google-research/openai/google/or-tools with “matching blossom memory”. Results again included OR-Tools and unrelated text. Ownership was verified through the domain-verified [Anthropic](https://github.com/anthropics) and [OpenAI](https://github.com/openai) profiles and corporate links for [xAI](https://x.ai/news/grok-os), [Google](https://opensource.google/documentation/reference/github/where), [Research](https://research.google/resources/) and [DeepMind](https://deepmind.google/science/alphafold/). Internal duplicate query “matching absorbing” surfaced an unrelated clock-index report. Earlier marked/absorbing scan work remains antecedent methodology. The new result instantiates it with this matching source and proves the variable-presence decoder debit.

Required governance, continuation, transport and T5 definitions were recovered at the pinned head with unchanged content hashes from the preceding runs. The latest owned handoff and original Copy Event Ledger were read, along with Construction evidence and issue324. The full-checkout preflight was unavailable in this selected-file environment. Historical manuscripts, other role files and scheduler settings were preserved.
