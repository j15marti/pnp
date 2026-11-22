# Accumulated decoder history and repeated obligations

22 November 2026, 09:05 PST. PNP Lower Bound Connections. DYNAMIC-COMPATIBILITY-OBLIGATION1. Named lemma ACCUMULATED-DECODER-HISTORY1. PROVED/EXACT conditional accounting theorem and concrete scan instantiation. COMPUTATIONAL finite audit. Independent review pending. P versus NP OPEN.

The new step strengthens the selected-anchor decoder and Accounting's articulation ledger. It identifies the precise information term that a proposed recurrence must supply when later decoders discard earlier observations. The term measures omitted information. It does not, by itself, measure physical erasure or compulsory recomputation.

## Quantifiers and model

Fix any total correct deterministic solver A before choosing a distribution on permitted N-bit inputs X. The physical model is the repository's one writable finite-alphabet tape, read-before-write unit-speed head, input/work/output charged, and terminated Boolean output at the origin. Fix a finite number J of obligations. Padding inactive stages with a constant is allowed only with stage selection and activity information accounted. Each U_j is a deterministic finite-valued function of X, specified independently of the desired lower bound. Let B_0 be initial decoder side information.

For each j, let V_j=(B_0,Pi_1,...,Pi_(j-1)) be the accumulated analytical record. Let B_j=f_j(V_j) be the actual side information supplied to decoder j, for a fixed public f_j. Additional source-dependent metadata must be put into an explicitly accounted earlier record before being included in V_j. Adaptive task identities and stopping indices are subject to this rule. This theorem does not assert that every checkpoint view is a function of earlier charged records. That is a premise to check on an application.

Require an actual decoder U_j=d_j(B_j,Pi_j). For every value of B_j, the possible Pi_j form a prefix-free code. On the same execution specify actual transition sets E_j, fixed capacity b>0, and nonnegative charged framing lengths h_j such that |Pi_j|<=b|E_j|+h_j. Every transition occurs in at most rho sets, rho>=1. These are the shared compulsory-work premises, not consequences of the entropy calculation.

Define the omitted-information term
delta_j=I(U_j;V_j | B_j).
Then

sum_j H(U_j|B_j)
= sum_j H(U_j|V_j) + sum_j delta_j
<= H(U_1,...,U_J|B_0) + sum_j delta_j
<= H(X|B_0) + sum_j delta_j
<= N + sum_j delta_j.

When all U_j are the same Boolean decision D, replace N by H(D|B_0)<=1. In particular, if B_j retains all V_j, the decision can contribute at most one bit in total. For j>1 it contributes zero once the first valid record decoded D.

Proof. Since B_j is a function of V_j, the conditional mutual information identity gives the equality. Earlier decoded U_i are functions of V_j by induction, because both their side information and records are recoverable there. Hence H(U_j|V_j)<=H(U_j|B_0,U_1,...,U_(j-1)). Summation is the entropy chain rule. The obligations are deterministic functions of X, giving the next bound. The repeated-D case follows from its joint vector entropy. Every variable here has finite support at fixed N, since A halts on the finite input set. No efficiency of the analytical decoder is required.

Independently, prefix-free coding gives
H(U_j|B_j)<=H(Pi_j|B_j)<=E|Pi_j|.
For completeness, conditional Kraft weights 2^(-length) sum to at most one. Normalizing those weights and applying nonnegativity of relative entropy gives entropy no larger than expected code length, for each B_j fiber. Sum and use sum_j |E_j|<=rho T pointwise to obtain

E[T] >= (sum_j H(U_j|B_j) - sum_j E[h_j])/(b rho).

The two inequalities together show the first open premise for a superpolynomial demand based on these successive decoders. Large repeated demand beyond N requires a large omitted-information sum as well as legal event membership and reuse. Establishing delta_j alone supplies no necessity for a future read. Omitting a retained cache from a decoder is an analytical restriction requiring its own machine-locality justification.

A complete source supplied in B_0 makes every U_j entropy zero. A complete correct configuration makes the future decision entropy zero even when computing that decision is difficult. This theorem respects both obstructions. Local crossing decoders may have nonnested views with large delta_j, so their repeated transport costs remain possible. Their physical locality proof is essential.

## Concrete Construction instantiation

Use Construction's 08:30 articulation family at dec4350c30459630faa060ddf3ddfba91c66507d, recovered through main 8039783927a4d7f5358874d0c35c2e81b4e206c2. Its q switches give positive exact-one sources with v=8q+7,m=9q+6. A switch block has port relation R={00,01,10}, a nonswitch block equality, and both end ports are pinned true. R squared is full. Therefore SAT iff the switch count differs from one. This is both-label decision.

Fix the authenticated scanner from Accounting f0d3a02a3f10a2aed4c7ec1525d0d80a92abe411. After full family authentication succeeds, normalize by clearing the original, scratch copies and input-dependent control state, leaving a q-cell switch vector, public q and a zero saturated counter. No fallback is needed after successful authentication; failed guards keep the original for fallback. In the scan erase each consumed vector bit after updating the counter. At each SCAN checkpoint all cells outside the unread vector are public functions of q,j and the counter, including origin output cells, head, phase state and addresses. The model exposes no external clock. This is a deliberate fixed legal scanner with paid erasure and scans, so the decoder's hidden-region restriction follows from its complete visible configuration. Let X=Z be uniform over all 2^q switch strings for the source-level calculation (the general bound uses the physical N-bit image). U_j=min(2,sum_(i<=j) Z_i), the prefix relation state encoded as 0,1,2. This definition is independent of any runtime claim.

For its actual upward scan set B_j=(q,j,U_(j-1),public SCAN protocol), Pi_j=Z_j and E_j={the one transition reading normalized cell j}. Known layout and SCAN state determine the addressed cell and fixed one-bit framing. The counter update decodes U_j. Thus b=1,h_j=0,rho=1. Earlier records determine the counter and j. Take V_j to contain the entire prior bit prefix. Given the counter, older prefix details have no further information about U_j, so delta_j=0. The joint entropy of the whole saturated-counter profile is the total fresh demand, at most q. The scanner pays all normalization and movement before and between these events.

If B_j is reduced to public q,j, a valid record is the complete prefix Z_1...Z_j. Its E_j consists of the first j actual reads and rho=q. Then delta_j=H(U_j)-H(U_j|Z_<j). The excess marginal demand is exactly the sum of these deltas. A proposed one-bit record with this restricted view is invalid: at j=2, prefixes 00 and 10 have the same current bit and different U_2. This gives a specific failure of the decoder premise rather than a presumed work lower bound.

For repeated final decisions, first computing D and then using the same READY read in J records gives rho=J and no amplification. If a particular machine really performs J new reads, rho=1 is possible, but correctness does not compel that machine design. After paying the scan, a globally correct scanner can output its cached D and halt. All valid nonfamily inputs are handled by exact fallback. No virtual prefix service is required of another correct solver.

## Costs and cap comparison

In the compiled family, inherited parameters are t=5v+6m, r=3m,d=8t,c=26t+4r,g=max(3,2 floor((c+1)/2)+1), n0=d+(10c+1)g+2,m0=(20c+4)g,n=n0+m0+3,M=2m0+4,w=ceil(log2(n+1)). The physical field order is unary n with delimiter, gamma(M+1), M signed fixed-width triples, two n-bit witness vectors and a w-bit release ID. Thus N=3n+2+2 floor(log2(M+1))+3M(w+1)+w=Theta(q^2 log(q+1)).

The family scanner inherits symbolic T=O(N^4), peak physical span S=O(N), and CM_phys=O(N^5) after parsing, authentication by inversion/regeneration/comparison, failed candidates, original retention, vector copies, counters, source/name/address scans, initialization, sharing, cleanup and origin output. Input-plus-step replay independently gives CM_min=O(N^5). These compiled tariffs are CONDITIONAL on the prior authentication implementation and were not newly simulated. They are bounds for one admitted execution. Nonfamily fallback O(2^n N^3+N^4) can be exponential. The analytical V_j is not an extra physical tape and its storage is never added to S.

Under T<=K N^a, a>=1, the standard ceilings are S=O(N^a), CM_phys=O(N^(2a)), CM_min=O(N^(a+1)), and the separate count-map circuit ceiling O(N^a log N). The shared numerator must exceed b rho K N^a to contradict this cap. With delta=0 it is at most N, or one for repeated D. This calculation alone cannot exclude all fixed exponents. Physical distance/retention theorems may provide distinct certificates, with overlap checked. The internally reviewed permutation control retains its single-tape quadratic-time/cubic-cumulative match and static Dh<=N²/8,Dh²<=N³/27.

Discovery's two-variable star extension at 80397839 encodes graph 3-colorability, with constant NAND leaf tables and variable endpoints. Its hardness result leaves compulsory U_j and their decoder views OPEN. The current theorem applies to any such proposed decoder sequence. A valid general polynomial join algorithm would still imply P=NP. Neither the entropy ceiling nor the scanner provides that algorithm.

## Falsifiers and verification

Four concrete falsifiers delimit the theorem/application. Supply B_j with a new source-dependent address or query for free, so it is not f_j(V_j). Omit an already retained counter and still claim a one-symbol decoder. Reuse the same READY transition while declaring rho=1. Treat J different queries on J inputs as stages of one execution. The first falls outside the conditional theorem and the other three invalidate claimed physical applications.

The new checker exhausts every switch string for q=1,...,8, 510 inputs. It verifies saturated updates, zero delta for a retained counter, the entropy identity under omitted prefixes and the prefix reuse count. At q=8, fresh demand is 3.921875 bits, marginal demand 7.016693783510265, and omitted information 3.094818783510265. This is a new all-switch prior and a new information-loss identity, rather than a rerun of Accounting's zero-or-one-switch experiment. Symbolic proof establishes the general result. No native tape simulation or kernel proof was executed.

[Checker](../../../experiments/dynamic_bounds_history_20261122.py) and [evidence excerpt](../../../results/raw/dynamic_bounds_history_20261122.json).

DISJ sanity PASS at conditional scope, with no hidden communication restriction imported. Simultaneous DTISP PASS for the stated scanner execution. Deterministic configuration counting PASS as an upper-bound check. Relativization, algebrization and Natural Proofs supply no unrestricted conclusion here. Affine/Tseitin, complement, forced-domain, private-leaf, relocation and sharing controls remain compatible with arbitrary preprocessing and fallback.

## Fresh sources and recovery

Shannon, A Mathematical Theory of Communication, Bell System Technical Journal 27 (1948), corrected reprint, section 6 properties 5–6, gives the discrete conditional chain rule and reduction of entropy by conditioning. The theorem above is a direct finite-variable derivation with additional decoder hypotheses proved explicitly. Query used “Shannon 1948 mathematical theory communication conditional entropy chain rule pdf”. [Primary text](https://people.math.harvard.edu/~ctm/home/text/others/shannon/entropy/entropy.pdf).

Each official organization anthropics, openai, xai-org, google, google-research and google-deepmind was freshly searched for the exact pair “conditional entropy” “transcript”. Five returned zero hits. OpenAI returned three files in openai/math at 4eaee87548250b2682affda7d05d947c05554bae. Read the Gaussian-observation introduction at preprints/Localization-costs-and-information-growth-for-exact-Gaussian-observations-September-27-2026/build/sections/00-introduction.tex. Its claimed learner tradeoff assumes independent Gaussian observations, finite memory and signal accuracy, with retained stopping information. Offline SAT has no mandatory new independent observations or accuracy task. No theorem from that manuscript is imported and no build was run. The matrix-multiplication hit was outside this target. [Inspected revision](https://github.com/openai/math/blob/4eaee87548250b2682affda7d05d947c05554bae/preprints/Localization-costs-and-information-growth-for-exact-Gaussian-observations-September-27-2026/build/sections/00-introduction.tex).

Two web fallback queries grouped the first three org domains with “conditional entropy transcript” and the last three with “information complexity transcript”. They surfaced third-party material, with no additional official result adopted. Ownership verified through domain-verified [Anthropic](https://github.com/anthropics) and [OpenAI](https://github.com/openai), corporate [xAI release](https://x.ai/news/grok-os), [Google policy](https://opensource.google/documentation/reference/github/where), [Google Research](https://research.google/resources/) and [DeepMind](https://deepmind.google/science/alphafold/). External repository results are clues subject to exact hypotheses and review.

Recovered AGENTS.md, CODEX.md, the repository skill and active governance, dynamic directive, transport model/matching upper/static ceiling, T5 definitions and entropy/accounting sections, current Bounds report and five peer handoffs, Construction and Accounting originals with code/raw, and latest issue324 comments. Repository search for “forgetting” “entropy” found historical source-query controls and T5's full-state obstruction. The present addition is the explicit delta identity for sequential decoded obligations. Selected-file connected recovery was used because there is no local checkout. Preflight and full-tree survey were not completed; the recursive tree endpoint returned no structured body. No manuscript ownership inferred.

## One next dependency

Accounting should instantiate delta_j and the actual future E_j on a proposed second compulsory phase after arbitrary paid joint preprocessing, and prove why the fixed solver cannot retain a sufficient summary instead. Redteam receives the j=2 prefix collision and repeated-READY reuse tests. Synthesis receives the N+sum(delta) ceiling and the stronger one-bit ceiling for repeated decisions. Construction receives preservation of the saturated-counter bypass. Any unrestricted recurrence remains OPEN pending the locality and compulsory-event premises.
