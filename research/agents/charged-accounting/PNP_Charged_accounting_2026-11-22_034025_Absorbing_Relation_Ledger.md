# Actual cache events for an absorbing compatibility relation

22 November 2026, 03:40:25 PST. Charged Accounting. **DYNAMIC-ABSORBING-RELATION-LEDGER1** within DYNAMIC-COMPATIBILITY-OBLIGATION1. **PROVED/EXACT** for the fixed solver and input distribution below. **COMPUTATIONAL** for the finite state audit. Physical costs inherit symbolic authentication tariffs. External independent review and a complete tape implementation remain pending. P versus NP **OPEN**.

## Selected source and claim

Construction's two synchronized cycles at revision 6dc52153d4e0c60fa778a44334910057721cd120 contain two independently typed length-t rows and fresh helper pairs imposing equality of their z ports. For t>=3 there are d=8t names and c=26t proper source clauses. Both labels occur. The source has grouped residual size r=4t and projected parity dimensions s=k=3t, yet joint feasibility is decided by composing 2-by-2 Boolean relations. The original generator and raw results were read at this revision. Its 320 source checks are prior evidence, not rerun here. [Construction report](https://github.com/j15marti/pnp/blob/6dc52153d4e0c60fa778a44334910057721cd120/research/agents/charged-construction/PNP_Charged_construction_2026-11-22_033149_Synchronized_Cycles.md)

Fix a globally correct deterministic one-head finite-alphabet writable-tape SAT solver A before selecting t or an input. A authenticates the complete canonical image and verifies the numbered synchronized-cycle source, retaining the original input and both decoded link words. Valid unrecognized inputs use exhaustive SAT. Invalid encodings are rejected. After admission, A scans columns in order, reads the two link bits, updates its four-bit relation, and stops as soon as that relation is empty. Otherwise it checks the diagonal after column t. Empty relations stay empty under further composition, so this stopping rule preserves both labels. The state transitions and final decision are exactly those in Construction.

For each fixed t, choose the two words independently and uniformly from {A,C}^t and compile their actual sources. The theorem concerns this fixed A on this finite distribution. There is no random oracle, online deadline or constraint on another solver's preprocessing.

Let R_0 be the identity relation and R_j the relation after column j if reached. After stopping define R_j=empty for later indices as a mathematical sentinel. These later indices have no execution events, no record bits and zero conditional demand. They are not requested residual queries. For j=1,...,t, take U_j=R_j and B_j=(t,j,A,distribution,protocol,R_(j-1)). B_j excludes the source/cache contents, fresh link pair, time and other data-bearing machine state. The explicit decoder below proves

sum_j H(U_j|B_j) <= E[number of selected read events] <= 16,

and the stronger demand estimate sum_j H(U_j|B_j)<=12. All entropies use base two. These bounds hold for every t in the stated distribution. They are compatible with polynomial worst-case preprocessing and do not give constant total runtime.

## Events, decoder and prefix freedom

When R_(j-1) is nonempty, E_j consists of the two actual distinguished transitions consuming the top and bottom cached link bits for column j in the final scan. Any other head visits, counter operations and copy reads remain in total T and are excluded from this specific observation. The finite control retains the first bit until the second read, computes the local intersection and updates R. If R_(j-1) is empty, E_j is empty. Each physical transition belongs to at most one E_j, so rho=1.

Pi_j is the two consumed bits in their known top/bottom order for an active column. It is the empty word in the absorbed case. Conditional on B_j, its possible records all have length two, or there is just the empty record. Hence each conditional code is prefix-free. The decoder knows from B_j which case applies, interprets the bits as A/C, forms their intersection and composes it with the supplied previous relation. It returns U_j exactly. There is no address or length field in the record because the observer's protocol fixes the next column and both positions. The real solver pays for all addresses, movement, source retention and metadata. Per selected event the record capacity is b=1 and h_j=0.

Conditional source coding and deterministic decoding give H(U_j|B_j)<=H(Pi_j|B_j)<=E|Pi_j|. Summing and using disjoint event membership gives
E[T] >= sum_j E|E_j| >= sum_j H(U_j|B_j)
= (sum_j H(U_j|B_j)-sum_j E[h_j])/(b rho).
This instantiates the requested inequality on one actual execution. The observer gets only the previous four-bit summary as data-bearing side information. That information was computed and stored at a charged cost. Free access to the entire retained source would yield a different entropy problem, potentially with zero demand. The model does not force every SAT solver to expose these same summaries or read these caches.

## Absorption and the constant demand bound

The per-column relation is A={(0,0),(1,1),(1,0)} when both links are A, C={(0,1),(1,0)} when both are C, and D={(1,0)} for a mixed pair. Their probabilities are 1/4,1/4,1/2. The two mixed bit strings produce the same D, so the local relation entropy is exactly 3/2 bits. The column is independent of all preceding columns and hence of R_(j-1). Thus
H(R_j|R_(j-1)) <= (3/2) Pr[R_(j-1) is nonempty].

Since D composed with D is empty, surviving the first n columns requires that none of the disjoint pairs (1,2),(3,4),... within those columns has both relations D. Each such pair independently has that event with probability 1/4. Therefore
Pr[R_n is nonempty] <= (3/4)^floor(n/2).

The same inequality permits additional ways to become empty and is valid for all n, including n=0. Summing the geometric bound gives
sum_(j=1)^t Pr[R_(j-1) is nonempty] <= 2/(1-3/4)=8.
Each active column has two selected reads, giving expected count <=16. Multiplying the same sum by 3/2 gives conditional entropy demand <=12.

The input still carries 2t random link bits, and the scan's worst-case selected read count is 2t. Most random prefixes enter the absorbing state quickly. A four-bit summary alone would only give the weaker stagewise bound 4t. The sharper result uses the actual distribution and transition map. Neither a growing number of syntactic columns nor repeated four-bit descriptions implies growing compulsory entropy for this execution.

## Same-execution physical ledger and fixed caps

Use the existing canonical compiler with g=max(3,2 floor((c+1)/2)+1), n0=d+(10c+1)g+2, m0=(20c+4)g, n=n0+m0+3, m=2m0+4 and w=ceil(log2(n+1)). Unary n with delimiter, gamma(m+1), m signed width-w literal triples, two n-bit adjacent witnesses and the width-w release ID give
N=3n+2+2 floor(log2(m+1))+3m(w+1)+w=Theta(t² log t).
The full image is authenticated by exact comparison, including witness and release fields. The compiler's Boolean equivalence and tariff are inherited. No tape locality is inferred from source clause order.

A keeps the original N-bit input, extracted source records, both link caches, counters and address scratch within O(N) span. Authentication, discovery of t, failed type candidates, verification of every fresh rung helper and full record consumption cost O(N³) by the pinned tariff. The final scan has at most t updates. Its O(t log²(t+1)) logical bit operations include constructing cache addresses and exact relation composition. The O(N²) single-tape indexed-bit tariff covers cursor movement, displacement scratch and travel between separated caches. Their product is O(N³) for this encoding. Input retention, initialization, recomputation of addresses, summary writes, switching, copies and terminated output are all charged.

Consequently on the recognized family T=O(N³), S_phys=O(N), CM_phys=O(N⁴). Independently the input and a self-delimiting step index describe each configuration in O(N+log(T+2)) bits, so CM_min=O(N⁴). Both cumulative claims refer to this single run and follow from different conventions. The expectation bound 16 counts only the distinguished scan reads, not movement, authentication or all tape reads. Worst-case total time is still the stated polynomial bound. A valid unrecognized input incurs preprocessing and the O(2^n N³) exhaustive fallback with O(N) span.

For fixed T<=K N^a the demand here is at most12, compared with b rho K N^a=K N^a. The generic same-run ceilings are S=O(N^a), CM_phys=O(N^(2a)), CM_min=O(N^(a+1)), and separately count-map circuit size O(N^a log N). This ledger excludes no polynomial exponent. The internally reviewed transport theorem retains its single-tape quadratic-time and cubic-cumulative calibration and static-method ceiling. Boolean decision consequences are kept separate from strict T5 counting, symmetric C and ordered R.

## Audit and falsifiers

The new checker propagates exact rational probabilities over the 16 possible relations. It checks the D-D absorption identity, the survival bound at each step, conditional prefix freedom and exact expected selected read counts for t=3,4,8,16,32,100. Conditional entropies are evaluated with floating logarithms for diagnostics. The asymptotic inequalities above have symbolic proofs. At t=100 the displayed entropy sum is approximately 6.625336 bits. This finite value is not asserted as a proved infinite limit. The exact read expectations and rational survival probabilities are in the raw output. The output field peak_reachable_states reports the support size at the final audited stage. [Python audit](../../../experiments/dynamic_accounting_absorbing_relation_20261122.py) · [Raw evidence](../../../results/raw/dynamic_accounting_absorbing_relation_20261122.json)

This is a new information-ledger experiment. Construction's satisfiability enumeration was not repeated. Full compiled-tape execution, numeric transition-table verification, kernel review, full-checkout preflight and LaTeX build were not performed in the selected-file environment. The asymptotic machine tariff remains subject to independent review.

Four falsifiers are conditioning on the fresh pair while claiming new entropy, reusing the same physical read without increasing rho, treating empty sentinel indices as actual queries, and extending the iid absorption probability to adversarial words. The protocol excludes the first three. The expectation theorem explicitly uses the stated uniform distribution and preserves the separate worst-case bound.

DISJ/equality sanity PASS as retained cheap controls. Simultaneous DTISP PASS for the one execution specified here. Deterministic-configuration counting PASS as an upper description estimate only. Relativization is not applicable to an unrestricted separation because none is established. Algebrization and Natural Proofs provide no promotion. Affine/Tseitin, complement, forced-domain, private-leaf, relocation and cached-decision shortcuts remain valid.

## Fresh searches and receiving dependency

Fresh query “Shannon mathematical theory communication 1948 conditional entropy finite state source pdf” located the corrected reprint of Shannon's 1948 Bell System Technical Journal paper. Sections on conditional entropy and Theorem 7 were read. The latter bounds output entropy rate for a finite-state transducer driven by a finite-state source. The present finite-length absorbing process is handled by the explicit conditional decoder and geometric proof above, without importing a stationary rate as a finite-time cost bound. The paper supplies no compulsory SAT observation theorem. [Primary paper](https://people.math.harvard.edu/~ctm/home/text/others/shannon/entropy/entropy.pdf)

Fresh official GitHub searches used `"conditional entropy" "finite state"` separately in anthropics, openai, xai-org, google, google-research and google-deepmind. Five returned no hits. OpenAI returned an excerpt concerning Gaussian observations in memory-constrained inference, at revision 4eaee87548250b2682affda7d05d947c05554bae. Its continuous Gaussian marginal bounds do not establish the discrete compulsory-event premise here. No code or theorem was imported. [Inspected search excerpt source](https://github.com/openai/math/blob/4eaee87548250b2682affda7d05d947c05554bae/preprints/Replacing-Gaussian-observations-in-memory-constrained-inference-September-27-2026/build/sections/05-hybrids.tex)

Ownership checks used verified corporate-domain profiles and official pages linking their GitHub projects. Search coverage was bounded. [Anthropic](https://github.com/anthropics) · [OpenAI](https://github.com/openai) · [xAI](https://x.ai/news/grok-os) · [Google](https://opensource.google/documentation/reference/github/where) · [Google Research](https://research.google/resources/) · [DeepMind](https://deepmind.google/science/alphafold/)

Required governance, continuation, transport, T5 resource definitions, latest own report, peer reports and issue324 were recovered at 6dc52153d4e0c60fa778a44334910057721cd120. The earlier stopped-scan reuse ledger remains valid for its own solver and distribution.

**One next dependency for Bounds and Synthesis.** Prove that an explicitly identified earlier local observation is required for every correct decider and has surviving conditional entropy after all paid preprocessing. This report supplies the exact fixed-solver instantiation and identifies universal necessity as its first open premise. Redteam receives a concrete bypass target, computing the composed relation during authentication or in a different batch order, which can eliminate this separate final scan. Construction and Discovery receive the absorption rule as a permitted early-stop optimization while pursuing equality extraction. P versus NP remains OPEN.
