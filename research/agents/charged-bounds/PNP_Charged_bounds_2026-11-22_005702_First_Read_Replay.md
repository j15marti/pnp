# First-read replay gives an actual decoder and a linear acquisition ceiling

22 November 2026, 00:57:02 PST. Charged Bounds.
**DYNAMIC-FIRST-READ-REPLAY1**, within DYNAMIC-COMPATIBILITY-OBLIGATION1.
Recovery e9ad51427d7ba24508085ed2c31e1fa29c0c503b.
**PROVED/EXACT restricted decoder lemma. Independent review pending. P versus NP OPEN.**

Accounting asked for an earlier-event decoder with explicit selection metadata. A full replay from the initial state supplies such a decoder for the Boolean output, with no address annotation. The entire record contains at most N original bits. Applying this particular mechanism repeatedly therefore requires a new locality or recomputation premise. No unrestricted runtime bound follows from this ceiling on its record.

## Quantifiers, initial state and events

Fix any deterministic finite-alphabet one-writable-tape machine A, with one head moving at most one cell per transition, before the input distribution. Its control and initial head are public. Binary input I occupies the public cells 0,...,N-1; every other cell is blank, with any end convention fixed publicly. All work, copies, addresses and output occupy this same tape. Every transition reads its current cell before writing. Output starts at the fixed origin and includes a terminator.

Fix N and any finite distribution supported on valid length-N inputs on which A halts with a correct Boolean SAT decision. Let U=D(I). Let B contain A,N, the initial layout and the distribution, but not the sampled input. This permits distributions with both labels. The source code of A is fixed advice of constant length.

E(I) is the set of actual transition indices at which the head first scans a cell in the original interval [0,N-1]. Pi(I) lists, in increasing transition order, the bit read at those transitions. A first-scanned original cell still holds its input bit: an earlier overwrite would itself have required a prior scan. Original cells count only once, even when reused as work or output later. Thus |Pi|=|E|<=min(N,T).

Three falsifiers are a write preceding the cell's purported first read, an unknown initial scratch/configuration supplied to the decoder, and selective omission of a first read while still claiming deterministic replay. The first contradicts the declared transition model. The latter two are excluded premises, and become real obstructions when one tries to restart the argument after preprocessing.

## Actual decoder and conditional prefix freedom

The following external proof decoder is fully specified. It does not run on A's tape.

    initialize simulated control/head to A's initial values
    initialize a map of scanned cells as empty
    while simulated A has not halted:
        let i be the simulated head position
        if i is absent from the map:
            if 0 <= i < N:
                consume the next bit of Pi and place it at i
            else:
                place blank at i
        perform A's transition using that cell's simulated symbol
        update that cell, control and head in the simulation
    return the simulated Boolean output

On a valid transcript, induction over transitions proves that the simulated control, head and every scanned cell agree with the actual execution. When the next previously unscanned input cell is encountered, the record supplies its original value. Every other required value was initialized publicly or written during the identical prefix. Consequently the decoder halts and returns U. It reconstructs all selected event indices and cell addresses from the preceding record bits and fixed dynamics, with no free absolute clock.

For a fixed B, suppose a valid transcript p is a proper prefix of another valid transcript pq. Up to the halt associated with p, the decoder follows the identical transitions on either record and consumes exactly p. It then halts on both, so pq cannot be the record of a longer actual execution with those same read answers. This contradiction proves conditional prefix freedom, including the possible singleton empty word. The decoder uses halting as its terminator; no physical input length field is omitted because N is fixed in B. For variable-N distributions, condition on N or encode it separately.

Set b=1, h_1=0, rho=1. The exact decoder gives
     
    H(D|B) <= H(Pi|B) <= E|Pi| = E|E| <= E T.

This is the requested shared inequality with one obligation. General sets satisfying exact decoding and length |Pi_j|<=b|E_j|+h_j can be summed only after proving pointwise reuse at most rho. Decoder reconstruction of addresses makes the present zero framing valid. An arbitrary selected subsequence need not have this property.

The decoder can take T simulated transitions and use a representation of the whole scanned area. No efficient inverse or short computation is asserted. The proof record is not assumed physically stored by A. Charging its decoding as additional mandatory work for A would be a different claim.

## Concrete integration with the gate-cycle candidate

Construction's authenticated scalar cycle solver is fixed before k,p,q. For every even k>=6 its source constraints have one shared gate g. In gate branch zero, marked vertices 0,p require adjacent bits to sum to zero; branch one uses 0,q; every unmarked vertex requires sum one. Propagation toggles between marks, proving branch feasibility p mod 2 and q mod 2. The Boolean decision is their OR.

Use the exact same canonical input as Construction at 3757eba. With c=4k+4,d=k+1,r=c+1,
     
    n0=d+(10c+1)r+2, m0=(20c+4)r,
    n=n0+m0+3, m=2m0+4, w=ceil(log2(n+1)),
    N=3n+2+2 floor(log2(m+1))+3m(w+1)+w.

Unary n and delimiter, gamma(m+1), ordered signed width-w triples, two explicit n-bit assignments and a w-bit release identifier give N=Theta(k² log k). The compiler has inherited Boolean equivalence and adjacent local Horn/dual-Horn witnesses. Its physical layout is not the permutation control layout.

Fix a uniform distribution over p,q independently in {1,2}. For ANY correct A, the lemma decodes D from its actual whole-run first-read record, giving H(D)=2-(3/4)log2(3) bits. It does not assert that this record decodes the two branch bits. In particular correctness constrains leaves only by D.

For the specific scalar solver that authenticates every bit by a full input scan, its first-read record does determine the entire input. An external decoder can replay the scan, reconstruct the original array, extract the canonical source and compute its first-branch bit V=p mod 2. Thus epsilon=H(V|B,Pi)=0 for that particular solver, and E T>=H(V)=1. The same E was already charged during authentication. It is not a new event set in a later phase. This solves the earlier-decoder request in a restricted way and identifies exactly what fails in a proposed repeated-work use.

At the cleaned READY checkpoint, p,q=(1,2),(2,1) have the same SAT cache and opposite V. There the suffix cannot decode V. If the restart decoder receives all of the retained original input freely, V has zero conditional entropy. If it receives an unknown tape configuration, the initial-state replay induction fails at its first unknown read. These cases agree with Accounting's branch-equivocation debit and Bounds' prior endpoint debit.

For all inputs, |E|<=N. The exact single-record entropy demand cannot exceed E|E|<=N. This does not bound A's total time by N: all intermediate computation and head travel remain charged. The crossing-sequence method can count repeated transport across distinct boundaries and has a different polynomial ceiling. The current first-read lemma alone cannot establish recurrent demands beyond initial acquisition.

## Full resource audit and upper bounds

Every actual transition of A, including parsing, authentication, discovery, failed candidates, copying, relocation, representation changes, adaptive switching, algebra, cache use, recomputation, address maintenance and output, counts in T. E selects a subset of those transitions; it does not discount the others. Physical span s_t includes the original input while retained and every nonblank cell, head and origin. CM_phys=sum s_t. CM_min=sum K(C_t|A), with input and t unavailable for free.

For the fixed cycle scalar solver, reuse the explicit exact authentication and mark enumeration costs from Construction and Accounting. Authentication costs O(N³); O(k²) candidate pairs each compare O(k) source records; each physical record operation costs at most O(N²). Current records, retained input and counters fit O(N) span. Cleanup erases through a high-water delimiter and returns to the origin, adding O(N). Thus T=O(N³+k³N²)=O(N^(7/2)), S=O(N), CM_phys=O(N^(9/2)). Separately the concise k,p,q generator plus t gives CM_min=O(T log N) on this family. Malformed admission is rejected after bounded validation; valid nonmembers get exhaustive SAT fallback, preserving global correctness without a global polynomial guarantee. Reduction production, if performed separately, costs O(N³), O(N) span under the inherited compiler.

The replay decoder imposes no additional resources on this execution. An actual logger would require its own writes and address bookkeeping; no such logger is silently inserted. Copies of Pi as an external mathematical record do not create new A events. All costs above refer to one solver, encoding and execution.

For a fixed T<=KN^a, retain S=O(N^a), CM_phys=O(N^(2a)), CM_min=O(N^(a+1)), and O(N^a log N) for the separate count-map circuit. A demand contradicts the cap only after exceeding b rho KN^a on that execution. Excluding one exponent does not exclude all polynomial exponents. The internally reviewed permutation transport control retains its single-tape quadratic-time/cubic-CM matching bounds and static ceilings Dh<=N²/8, Dh²<=N³/27. Counting claims are not imported into this Boolean result.

## Sources, recovery and bounded searches

[Own prior finite-phase endpoint proof](PNP_Charged_bounds_2026-11-22_000500_Phase_Endpoint_Debit.md), [Accounting's exact uncertainty ledger](../charged-accounting/PNP_Charged_accounting_2026-11-22_004337_Branch_Equivocation.md), [Construction's family](../charged-construction/PNP_Charged_construction_2026-11-22_003353_Factor_Backdoor_Acquisition.md), and [Discovery's affine control](../charged-discovery/PNP_Charged_discovery_2026-11-22_004633_Affine_Parameter_Control.md) were recovered at the snapshot. Construction and Accounting original code/raw were read, including the complete candidate generator and four-case suffix evidence. This is a symbolic decoder proof; no previous experiment was rerun, and no finite experiment or formal kernel verification is claimed.

Fresh primary query “decision tree deterministic query algorithm transcript prefix free entropy expected query complexity primary paper” led to Andrew Drucker, The Complexity of Joint Computation, MIT doctoral thesis, September 2012, section 2.1.1, pp.59-60. It defines binary decision-tree transitions and their leaf outputs. The deterministic query representation is the classical framework used here. The writable-tape replay lemma above proves its particular event correspondence. Direct-product conclusions in that thesis require their own multi-output/query hypotheses and are not imported into one Boolean decision. [Author-hosted primary text](https://people.csail.mit.edu/andyd/Drucker_PhD_thesis.pdf).

Fresh GitHub query '"decision tree" "query complexity"' covered anthropics, openai, xai-org, google, google-research and google-deepmind. Four scopes returned no hits. Anthropic/FlashProve returned Compile/Batch/Life.lean at 9e2bdd8ff5bf9c62f18263d7dac189b0400b260c, an excerpt describing adversary/session loads. OpenAI/math returned references.bib for a query-complexity preprint at 4eaee87548250b2682affda7d05d947c05554bae. These excerpts provide neither a compiled proof of this lemma nor a SAT model transfer. No code or theorem imported from them. Official scope provenance is the previously verified Anthropic/OpenAI profiles, x.ai/news/grok-os, Google's official organization guidance, Google Research resources and Google DeepMind profile. These bounded queries do not establish absence of relevant work.

The directive, transport, governance and repository research skill plus applicable T5 definitions were recovered again for this run. Their exact model and same-execution ceilings are used above. Selected files are available locally, not a complete checkout; full-checkout preflight and LaTeX compilation were not run. This owned Bounds note updates no historical TMR manuscript.

DISJ/equality sanity PASS for the stated input acquisition claim. Simultaneous DTISP PASS. Deterministic replay PASS as a decoder argument and an upper-description mechanism, without a configuration-count runtime lower bound. Relativization remains OPEN for unrestricted promotion; arbitrary input-dependent oracle replies are outside this decoder's bit supply. No Natural Proofs or algebrization bypass is asserted. Affine/Tseitin, complements, private leaves, forced domains, decision witnesses, caching and relocation remain allowed.

**One next dependency, Accounting with Bounds.** Supply a model-enforced later local interface whose starting state is reconstructible from already charged records and whose new exact decoder has positive conditional demand after endpoint/uncertainty debits. Its actual events must include more than repeated counting of original first scans. Redteam receives restart configurations and omitted-record selection as the concrete falsifiers. Synthesis receives the linear first-acquisition ceiling; Construction/Discovery retain their polynomial algebraic shortcuts. P versus NP OPEN.
