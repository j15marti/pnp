# Correlated values and physical event reuse are different quantities

22 November 2026, 05:41:00 PST. PNP Charged Accounting.
**DYNAMIC-COPY-EVENT-LEDGER1: PROVED/EXACT** for two fixed solver protocols on Construction's monotone-tail family. **COMPUTATIONAL** suffix audit. Internal review with peer context visible; independent adversarial review pending. P versus NP **OPEN**.

## Target and exact conclusion

Fix the solver before the input distribution. For each q≥1, sample equiprobably F(q,0) and F(q,1) from Construction at 89d89578d1fe09b0dabd62e9966499bacbb19cb5 [1]. Their Boolean decisions D are respectively 0 and 1. All resource statements below use the same single-tape execution and full input length N.

The named question is whether repeated, perfectly correlated obligation values automatically force a large event-reuse factor. They do not. Reuse counts membership of physical transitions, not equality of the values they carry. Conversely, statistical correlation does not authorize fictitious additional read events. We instantiate both cases, preserving Bounds' distinction between joint information and locally recorded transport [2].

For one fixed correct solver A_copy we obtain actual disjoint sets E_j, U_j=D, B_j=B, fixed-length one-bit records, b=1,h_j=0,rho=1, and
E[T_phase] ≥ sum_j H(U_j|B)=q.
The joint entropy H(U_1,...,U_q|B) is only 1. For a second fixed correct solver A_cache on exactly the same inputs, all q proposed records can instead refer to its one actual cache read, so rho=q and the same formula gives only 1. Both are polynomial-time on this family. Neither implementation is compulsory for other correct solvers.

Four falsifiers: assigning rho=1 to q aliases of one transition; assigning rho=q merely because q disjoint reads have equal payloads; replacing marginal demand by joint entropy while claiming the same certificate; and assigning a physical storage lower bound to shortest descriptions of a repeated-bit tape. The explicit constructions settle each at its declared scope.

## Source semantics and encoding

Construction uses t=8q columns, top C^(6q)A^(2q), bottom differing at one prefix column p where C becomes A, and q parity rows (2j,2q+2j,4q+2j). Rungs identify the two z ports. CC forces a flip, mixed AC/CA forces 1→0, and AA imposes a nonincreasing pair. The even prefix returns to its initial bit s. The AA tail has endpoints s,s, so all its bits equal s. The parity rows force s=0. Thus SAT iff p is odd, including our two equiprobable labels. This is decision equivalence, not exact counting.

The source counts are d=64q,c=212q. With the pinned compiler:
g=max(3,2 floor((c+1)/2)+1);
n0=d+(10c+1)g+2; m0=(20c+4)g;
n=n0+m0+3; m=2m0+4; w=ceil(log2(n+1)).
The entire encoded length is
N=3n+2+2 floor(log2(m+1))+3m(w+1)+w=Theta(q² log(q+1)).
Unary declaration, gamma clause count, signed addresses, both supplied local witnesses and release ID are included. Proper width three and adjacent local Horn/dual-Horn witnesses come from the inherited compiler. No physical column adjacency or processing order is assumed.

Both algorithms authenticate the exact canonical image and all fields, checking cheap length constraints before loops. They recognize this family and compute D=p mod2. A valid nonmatch uses exhaustive decision on the retained input; internal UNKNOWN is not UNSAT. Source recovery, comparisons, failed candidates, switching, addresses, copying, discovery and output remain charged. This supplies global correctness, not a global polynomial bound.

## Two actual protocols

The model is a deterministic fixed finite-alphabet machine with one writable tape, one head and unit moves. Span includes origin, head and nonblank support. All input, metadata, caches and work are on that tape.

A_copy, after paid admission and decision, creates q copies of D in cells 0,...,q−1 and a nonblank sentinel # in cell q. It erases the rest of its former input and work, returns to cell0 and enters SCAN. The exact checkpoint therefore contains D^q# and fixed control, with no free external source. Constructing this state, including the q counter and its eventual deletion, is paid. It can be performed by bounded sweeps in O(N²) additional transitions and O(N) span because q≤N.

SCAN reads each 0/1 cell, remembers the last bit in finite control and moves right one cell; on # it changes state. This is one fixed transition rule, independent of q. The payload phase has q transitions, followed by one sentinel transition. A return sweep then clears copies and sentinel and writes the terminated decision at origin in O(q) transitions. There is no uncharged q-dependent machine program.

Take B=(q,source pair,prior,A_copy,SCAN convention), excluding D, sampled input and input-dependent elapsed time. For j=1,...,q let E_j be the jth payload transition after entry to SCAN, U_j=D, and Pi_j the symbol it reads. B and j specify this ordinal event; no absolute timestamp or input-dependent address is supplied. The decoder returns its one-bit record. For fixed B, possible records are {0,1}, which is prefix-free. Capacity b=1 counts binary payload only. Length is known, h_j=0. The sets are pairwise disjoint, rho=1. Each marginal entropy is exactly one bit and T_phase=q, giving the claimed bound with equality.

No independence assumption enters the inequality: individually H(U_j|B)≤E|Pi_j|, then sum lengths and apply event overlap. The elementary prefix-code bound follows from Kraft and nonnegative relative entropy. Correlation matters if we change to a joint decoder: conditioning each later U_j on its predecessors yields entropy sequence 1,0,...,0. Conditioning on retained Z=D yields all zeros. These are valid weaker certificates for the same physical run, not reductions in its actual work.

A_cache instead prepares a single D at origin with output framing and reads it once in READY before terminating. For q repeated obligations U_j=D and E_j={that same READY transition}, Pi_j=D, b=1,h_j=0, the true rho is q. The marginal numerator q divided by rho gives1. Under the predecessor-conditioned joint formulation the numerator is1. Omitting this actual reuse gives the false inequality1≥q for q>1.

This comparison does not discard valid repeated-transport lower bounds. It shows why a theorem about all correct SAT solvers must prove the repeated events unavoidable. The copied scan is deliberately optional work. A_cache is a concrete bypass of the assertion that every solver on F(q,p) must perform q decision-payload reads after acquiring D.

## Same-execution resource ledger

| Resource | A_copy on admitted family | A_cache on admitted family |
|---|---|---|
| Parsing, source authentication, exact regeneration, discovery, failed tests | Inherited O(N³) time,O(N) span | Same |
| Cache formation, input clearing and repositioning | O(N²) additional, O(N) span | O(N²) additional, O(N) span |
| Post-preparation read/output work | O(q), all moves and sentinel included | O(1) after framing |
| Whole-run time and peak physical storage | O(N³),O(N) | O(N³),O(N) |
| Whole-run physical cumulative cost | O(N⁴) | O(N⁴) |
| Whole-run minimum-description cumulative cost | O(N⁴), separately by input/time replay | O(N⁴), separately |
| Valid nonimage fallback | O(N³+2^n N³),O(N) span | Same |

All inherited bounds are symbolic compiler/simulation tariffs, not measured full-machine executions. The suffix implementation does not eliminate prior authentication costs.

There is a sharper physical/description distinction after A_copy's checkpoint. During each of its q payload reads the nonblank sentinel at q makes the span exactly q+1 under the stated cell-count convention. Thus payload CM_phys=q(q+1). Yet the complete checkpoint and any phase configuration have a description consisting of q,D,the transition index and a fixed interpreter, of O(log(q+2)) bits. Therefore CM_min over that phase is O(q log(q+2)); it is not forced to equal the quadratic physical cost. Constants encode the fixed machine and conventions. The shortest description is not a free working representation provided to the solver. A_cache's cleaned suffix is constant size and time.

For T≤K N^a, keep the generic ceilings S=O(N^a), CM_phys=O(N^(2a)), CM_min=O(N^(a+1)), and separate count-map circuits O(N^a log N). q=O(sqrt(N)) here, so even A_copy's q-bit marginal certificate excludes no polynomial cap with a≥1. The internally reviewed single-tape transport control retains its quadratic/cubic baseline and static ceilings Delta h≤N²/8, Delta h²≤N³/27. The joint N-bit method ceiling is not a ceiling on all physically local transport certificates or on runtime.

## Evidence, gates and receiving dependency

[Checker](../../../experiments/dynamic_accounting_copy_events_20261122.py) and [raw](../../../results/raw/dynamic_accounting_copy_events_20261122.json) cover q=1,...,32 and both D values, 64 exact suffix traces. They check event membership, decoder bits, addresses, phase length, copied rho1, aliased rhoq, and exact payload CM=q(q+1). Entropy values are exact from two equiprobable outcomes, without floating logs. Small traces are retained verbatim. This is new suffix-event evidence; the previously completed source-semantic experiments were not repeated. The Python dictionary represents the literal suffix transition relation; Python runtime is not a tape cost. No prefix, compiled-image, full-tape or kernel execution is claimed.

Original Construction code and raw evidence, Bounds' theorem, the prior Accounting report and handoffs, required governance/model/definitions and issue324 were recovered at 89d89578. The prior marked-absorption result remains fixed-solver/iid-scoped and is not transferred to these adversarial words. No full-checkout preflight was possible in the selected-file workspace. Historical manuscripts, roles and schedules are unchanged.

DISJ/equality and simultaneous DTISP: PASS at the stated scope. Deterministic configurations: PASS only as an upper-description argument. Relativization/algebrization/Natural Proofs: no barrier bypass or unrestricted separation asserted. Relocation, affine/Tseitin, complement, forced-domain, private-leaf, cached-decision and shared-computation controls remain permitted. Strict T5 counting, symmetric C and ordered R are not substituted for decision.

**ONE next dependency to Bounds/Synthesis:** prove a model-enforced reason that distinct post-preprocessing decision-sensitive read events must occur for every fixed correct solver, including their selectable records and reuse, or exhibit another legal bypass. Neither correlated payloads nor a large copied representation supplies that premise. Redteam receives the direct A_cache bypass of obligatory A_copy scans; Construction/Discovery retain the restricted polynomial solver and can pursue paid contraction without this artificial copying.

## Fresh literature and official repositories

[1] [Construction, 89d89578](https://github.com/j15marti/pnp/blob/89d89578d1fe09b0dabd62e9966499bacbb19cb5/research/agents/charged-construction/PNP_Charged_construction_2026-11-22_053032_Monotone_Tail.md), original generator and raw recovered. The physical encoding and authentication tariff remain inherited.

[2] [Bounds, c73587c1](https://github.com/j15marti/pnp/blob/c73587c109f5c043e49cc8dfd5512920f4cb5d56/research/agents/charged-bounds/PNP_Charged_bounds_2026-11-22_050620_Joint_Prepayment_Decoder.md), explicitly preserving the original marginal theorem as well as the joint chain theorem. This report instantiates that distinction, not a correction to its stated theorem.

[3] C. E. Shannon, *A Mathematical Theory of Communication*, corrected 1948 reprint, section6, pp.11–12, [primary text](https://people.math.harvard.edu/~ctm/home/text/others/shannon/entropy/entropy.pdf). Fresh query “Shannon 1948 mathematical theory communication noiseless coding entropy pdf”; read joint subadditivity, conditional entropy and chain identity. Imported only finite discrete identities. No stationary-source, asymptotic channel or online-output hypothesis is applied to SAT. Prefix coding is justified separately above.

Fresh GitHub searches for `"repeated reads" "entropy"` in anthropics, openai, xai-org, google, google-research and google-deepmind returned no hits. Web fallback searched the first three and the latter three organization paths with “entropy information transfer memory”. Results included [OpenAI Gaussian memory-constrained inference](https://github.com/openai/math/tree/main/preprints/Replacing-Gaussian-observations-in-memory-constrained-inference-September-27-2026) and [DeepMind policy entropy documentation](https://github.com/google-deepmind/trfl/blob/master/docs/trfl.md). These are unrelated to compulsory SAT reads; no theorem or code was imported and no external repository commit was inspected. No access failure occurred in these searches.

Ownership references rechecked: [Anthropic](https://github.com/anthropics), [OpenAI](https://github.com/openai), [xAI's corporate GitHub link](https://x.ai/news/grok-os), [Google organization policy](https://opensource.google/documentation/reference/github/where), [Google Research resources](https://research.google/resources/), [DeepMind code links](https://deepmind.google/science/alphafold/). Internal duplicate query `"correlated" "reuse" "copies"` surfaced older fusion-tariff material with different finite transition systems; no claim of novelty for the general counting principle. Charged branch search was empty. Search scope was bounded to the current event-ledger premise.
