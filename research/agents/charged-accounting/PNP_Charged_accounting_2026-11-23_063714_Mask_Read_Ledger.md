# Actual mask reads after paid context acquisition

23 November 2026, 06:37:14 PST. PNP Charged Accounting.
MASK-READ-LEDGER1 within DYNAMIC-COMPATIBILITY-OBLIGATION1.
PROVED/EXACT for a fixed deterministic implementation and specified input distributions. Independent review pending. P versus NP OPEN.

This audits Discovery's two-terminal context family at a730a66bc77840872a46de977316c00e3eab4020 [1]. Its all-context message count is correct under the stated one-way contract. The present advance gives an actual tape-event ledger for one supplied context, an exact conditional entropy calculation, and a paid ordering improvement. The prior block-stop calculation [2] treated independent fair verdict bits. Here the events test individual support bits, with a second stopping rule within each piece and context-dependent success probabilities.

For every m≥1 and fixed context C=(C_1,...,C_m) with C_i a nonempty subset of {0,1,2}, choose A_i independently and uniformly among all eight subsets. This is a distribution over authentic, equally sized source instances using [1]'s fixed mask certificates. Fix one uniform deterministic solver before selecting m,C,A. It authenticates the encoded family, obtains the actual masks, then evaluates the Boolean decision AND_i[A_i intersect C_i is nonempty]. It remains correct on every admitted mask pair. A failed family guard invokes exhaustive decision on the original valid input. Contexts with an empty coordinate are handled by immediate rejection after authentication.

The exact target is

    H(U | B) = E[Q] = 2 sum_(i=1)^m product_(j=1)^i p_j,
    p_j = 1 − 2^(−|C_j|),

for the selected transcript U and side information B defined below. Since p_j≤7/8, E[Q]≤14(1−(7/8)^m)<14. This expectation is over the stated source prior. Worst-case Q is at most 3m. The missing universal premise is that any such transcript must occur on every correct offline execution.

Four falsifiers are a read word failing to determine its own stopping point, a reread or framing field omitted from capacity, an unpaid physical address or retained source, and treating a change in evaluation order as a free speedup. The decoder, event selection, complete cost ledger and paid rearrangement address these separately.

## Input and model

Use the transport report's deterministic sole finite-alphabet read/write tape, unit head speed, origin output and input-inclusive physical span. All input, metadata, work and caches occupy that tape. No free input head, retained-source oracle or clock is supplied. Cumulative physical memory is the sum of physical spans on that execution; minimum-description cumulative memory sums descriptions of complete configurations.

Discovery's graph has q=10m quotient vertices and k=22m−2 quotient edges. Four gain diamonds share each terminal pair, and neutral two-edge paths join neighboring terminal vertices. It is biconnected. A gain diamond's allowed terminal differences give a three-bit mask. Distinct interiors permit intersection of these masks, and every neutral path can be completed after fixing its endpoints. Thus its decision is the conjunction above, on both labels. Its triangle expansion and positive Boolean exact-one star encoding give n=528m−18 variables and R=408m−18 rows. With w=ceil(log2(n+1)), encoded length is

    N=n+2+2 floor(log2(R+1))+3Rw=Theta(m log(m+2)).

The unary header, gamma row-count field and every literal identifier are included. This report inherits the proved source equivalence from [1]; it audits its normalized decision phase, without rerunning the graph generator or treating exact-one rows as ordinary OR clauses. This is Boolean decision, with no strict T5 counting consequence.

## Fixed execution and actual events

After paid parsing and authentication, the solver writes a consecutive cache of fixed-width blocks, each containing C_i's three bits and A_i's three bits with fixed separators. A sentinel follows the last block. It erases the other source and work regions, returns to the cache origin and enters a fixed SCAN state. This phase, including cache construction and cleanup, is charged. The full original source can instead be retained within the whole-run upper bounds below.

Within block i, in increasing bit position d, examine A_i[d] only if C_i[d]=1. The first tested one proves this block feasible and advances to block i+1. If all |C_i| tested bits are zero, reject. On completion of all blocks, accept. The solver returns to the output origin and writes the verdict and terminator. Only a constant number of tape positions and finite-control steps per block is needed apart from the initial construction. Reading C_i and travelling across untested A bits are real charged transitions.

Let E be exactly the transitions executed in designated TEST control states that examine a selected A bit. These transition identifiers are a subset of the actual trace, with no multiplicities. Let Q=|E|. Let U be their chronological binary read word and let Pi=U. Side information B contains the fixed solver, m, C, cache geometry, prior and public source templates, with no A, selected source, or complete configuration.

A decoder simulates just the block and bit-index control from C. Each successive bit of Pi either finds a witness for a block or exhausts its selected bits and rejects. It stops when the solver would reject or finish the last block. Thus every possible complete word is a leaf of this fixed decision tree. No complete word is a proper prefix of another. Addresses and stopping length follow from C and the word; they are not an extra hidden channel. Every TEST transition contributes one bit, so capacity b=1, framing overhead h=0, and maximum reuse rho=1. Real address discovery and storage are charged by the implementation, even though the decoder is allowed the fixed C in its side information.

Each leaf word w fixes exactly |w| distinct coordinates of the uniformly random 3m-bit A. All remaining bits are arbitrary and cannot alter the path. Its fiber therefore has size 2^(3m−|w|) and its probability is 2^(−|w|). It follows directly that

    H(U|B)=sum_w Pr(w)|w|=E[Q],
    H(A|U,B)=3m−E[Q].

The actual-event theorem consequently gives E[T]≥E[Q]=(H(U|B)−E[h])/(b rho). No entropy theorem about hypothetical residual answers is used. Defining multiple copies of this obligation over the same TEST transitions requires raising rho accordingly.

Conditional on reaching block i, the selected bits remain fresh fair bits. Expected tests in it are sum_(r=0)^(|C_i|−1) 2^(−r)=2p_i. Its success probability is p_i. Earlier blocks use disjoint A coordinates, so its reach probability is product_(j<i)p_j. Summing gives the claimed formula. For all C_i full, it is exactly 14(1−(7/8)^m).

The scalar verdict has entropy h_2(product_i p_i), at most one bit. Giving the decoder a complete retained A cache makes H(A|B,A)=0. Neither statement measures the cost already spent acquiring or computing that cache. For nonempty C and m≥1 both verdicts occur under this prior. There is no all-UNSAT promise.

## Paid ordering improvement and physical costs

Among fixed permutations that fully process one piece before starting another with this within-piece procedure, placing smaller |C_i| first minimizes expected TEST reads. For adjacent success probabilities p,q the contribution conditional on reaching them is 2p+2pq in one order and 2q+2pq in the other. Later reach probability pq is the same. Exchanging an inversion decreases expectation by 2(p−q). Repeated exchanges establish the claim. This is optimality within that specified evaluation class only. It does not claim optimality among arbitrary adaptive solvers or minimum total tape time.

The solver can discover the ordering and relocate complete paired blocks into three buckets using paid scans. This uses O(m) constant-width cache cells and at most a conservative O(N^4) indexed-bit work allowance already used for source authentication. Decoder side information now includes the context-determined ordering. Source-independent randomness is unnecessary. Context-dependent acquisition cannot be omitted when comparing the original and reordered implementations.

If J is the number of blocks visited, then J≤Q≤3J for nonempty C. The scan, return and output take Theta(J+1) transitions. The unmodified cache and end marker occupy span Theta(m+1) throughout this suffix. Consequently

    T_suffix=Theta(Q+1),
    CM_phys,suffix=Theta((m+1)(Q+1)).

Hence expected suffix time is bounded by an absolute constant and expected physical CM is Theta(m+1); worst-case suffix time and CM are O(m) and O(m²). These are same-execution statements. Removing only entropy does not automatically remove physical span.

The complete admitted procedure retains the published conservative tariff: O(N^4) indexed bit work over O(N²) span, simulated by O(N³) charged tape sweeps per indexed bit instruction. This covers parsing, exact duplicate/missing-row checks, graph and mask discovery, failed candidates, addresses, copies, orientation conversion, cache initialization, bucket rearrangement if used, cleanup, return and output. Thus

    T=O(N^7), S=O(N²), CM_phys=O(N^9), CM_min=O(N^8).

Describing a deterministic configuration by input and time costs O(N+log T+log N) bits. That proves the descriptive bound without multiplying unrelated extrema. The fallback for valid off-family sources is O(2^n N^7) time, O(N²) span, O(2^n N^9) physical and O(2^n N^8) descriptive cumulative cost. Invalid encodings are rejected during parsing under the encoding contract. This is a globally correct exact algorithm with a restricted polynomial fast path. No polynomial bound for arbitrary SAT follows.

A second legal implementation calculates the running conjunction during mask discovery and stores only its final verdict before output. It omits every TEST event of the selected scan. Therefore the above transcript demand is implementation-specific. The unconditional necessity of this or a stronger event set after paid joint preprocessing remains OPEN.

Under fixed T≤KN^a, a≥1, the demand here is below 14 bits in expectation. It cannot exclude a fixed polynomial cap. The handoff ceilings remain S=O(N^a), physical CM O(N^(2a)), descriptive CM O(N^(a+1)), and the separate count-map simulation size O(N^a log N). The internally reviewed single-tape permutation control retains its quadratic-time/cubic-cumulative calibration and static ceiling. This report creates no unrestricted lower-bound transfer.

## Checks and receiving dependency

COMPUTATIONAL evidence in [checker](../../../experiments/dynamic_accounting_mask_reads_20261123.py) and [raw output](../../../results/raw/dynamic_accounting_mask_reads_20261123.json). Exhaustion covers all 399 nonempty contexts of lengths one through three and all 178,808 pairs with first-half masks. It verifies Boolean decisions, prefix freedom, Kraft equality, exact fiber cardinalities and expected read counts. All 243 five-piece cardinality profiles also pass comparison against every distinct permutation. These tests concern the new bit-level scan and ordering claim. They do not repeat the predecessor's graph-coloring checks. The symbolic argument supplies general quantifiers.

The workspace lacks a full checkout. Native bitstream parser, native tape, formal-kernel proof and repository preflight were not executed. State was recovered through connected reads. No TMR manuscript ownership is assumed. DISJ/full-state sanity PASS within the declared interface. Same-execution DTISP and deterministic replay gates PASS as upper accounting. Relativization, algebrization and Natural Proofs provide no separation mechanism here; unrestricted transfer remains OPEN. Caching, relocation, affine translation, complement, private-leaf source semantics and forced-domain controls retain their earlier scopes.

Next owner Bounds, receiving Synthesis: derive compulsory event membership for an obligation surviving arbitrary paid mask acquisition and running conjunction. Redteam receives the explicit claim to falsify, that the suffix transcript decodes all 3m mask bits; its exact residual entropy above disproves it for this implementation. Discovery receives the context-dependent event tariff and the ordering improvement.

## Sources and fresh searches

Recovered head a730a66bc77840872a46de977316c00e3eab4020, all six handoffs, operating guides, research skill, dynamic directive, transport model and applicable T5 definitions, latest Accounting and Discovery reports, and issue 324. Earlier report status and original source scope are retained.

1. [Discovery, two-terminal context rows](../charged-discovery/PNP_Charged_discovery_2026-11-23_055153_Two_Terminal_Context_Rows.md), pinned in the recovered head. The 7^m+1 statement concerns every future context with source inaccessible.
2. [Accounting, block cutset stopped ledger](PNP_Charged_accounting_2026-11-23_054142_Block_Cutset_Stop_Ledger.md), same head. Its one-level fair-verdict scan is the predecessor, with a different prior and event set.
3. Shannon, A Mathematical Theory of Communication, Bell System Technical Journal 27 (1948), corrected reprint, §9 Theorem 9 and §10. Fresh query “Shannon 1948 mathematical theory communication noiseless coding prefix code entropy original paper pdf”. Inspected the noiseless source entropy/channel capacity hypotheses and the example of a deterministic computable source. This supplies entropy context; the finite prefix and fiber argument is proved directly above. [Primary paper](https://people.math.harvard.edu/~ctm/home/text/others/shannon/entropy/entropy.pdf).

Fresh GitHub searches used the exact conjunction “short circuit” “entropy” within anthropics, openai, xai-org, google, google-research and google-deepmind. All returned zero except Google, whose digitalbuildings YAML described electrical short circuits and thermodynamic entropy. That result is irrelevant and rejected without importing code. DeepMind was rate-limited once and returned zero on retry. No external implementation or repository commit was inspected. Official ownership was checked via [Anthropic](https://github.com/anthropics), [OpenAI](https://github.com/openai), [xAI's release link](https://x.ai/news/grok-os), [Google's organization guidance](https://opensource.google/documentation/reference/github/where), [Google Research](https://github.com/google-research), and [Google DeepMind](https://github.com/google-deepmind). These bounded searches found no applicable compulsory-execution theorem.
