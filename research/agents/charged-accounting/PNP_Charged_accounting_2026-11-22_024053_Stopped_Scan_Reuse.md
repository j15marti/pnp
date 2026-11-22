# Actual-event accounting for the mixed-cycle stopped scan

22 November 2026, 02:40:53 PST. Charged Accounting. **DYNAMIC-STOPPED-SCAN-REUSE1**, within DYNAMIC-COMPATIBILITY-OBLIGATION1. PROVED/EXACT for the fixed solver and distribution below. COMPUTATIONAL exact finite audit. External independent review pending. P versus NP OPEN.

The mixed-cycle scalar decision admits a concrete variable-length observation record. Its prefix records overlap on actual physical reads, making maximum reuse essential. This run instantiates the entropy inequality exactly and preserves the paid polynomial upper bound. Its first unresolved transfer is the claim that any richer obligation must occur on every correct solver's execution.

## Source revision, fixed solver and model

The candidate is Construction at 4d5d4f24b1cc4d6a86a5560f78c79af9b2ce213d. Each t>=3 cycle has factor ports (a_i,b_i,z_i), exact-one factors, and checks a_i XOR b_i XOR u_(i+1)=0. Link C uses z_(i+1) and link A uses a_(i+1). The source contains d=3t variables and c=9t clauses. Construction proves SAT iff t is even or an A occurs. Both labels occur for odd t at the same length. All variables are factor ports, one component survives the specified leaf rule, and independent b_i pivots yield s=2t,k=t. [Original report and evidence](https://github.com/j15marti/pnp/blob/4d5d4f24b1cc4d6a86a5560f78c79af9b2ce213d/research/agents/charged-construction/PNP_Charged_construction_2026-11-22_023500_Mixed_Cycle_Residual.md).

Fix a total deterministic finite-alphabet, one-head, one-writable-tape SAT machine A_scan before any input. Its admission procedure parses and authenticates the complete canonical compiled source, verifies all exact-one and parity blocks, and writes the recognized link word into a contiguous t-cell cache using C=0,A=1. The source image and all scratch remain charged. It completes admission before using this cache. Unknown valid inputs invoke exhaustive decision on the retained original formula. Malformed inputs are rejected under the input-language convention. A_scan is a specified variant of Construction's solver. Construction also permits accumulating OR during admission, which avoids this later scan.

For even t the admitted path outputs SAT. For odd t, A_scan moves to the cache start and reads it left to right, halting the scan at the first 1 or the public end position t. It stores the resulting OR bit, returns to the fixed output origin and emits the terminated decision. Internal counter, movement and output transitions are charged. The event set below selects only the distinguished transition at which each new cache bit is first consumed by this final scan. An implementation may have extra head visits during counter updates, which remain part of T. They supply no extra event in the selected set.

For each fixed odd t, take the uniform distribution over all 2^t link words and their deterministic compiled images. The solver is the same for every t. Let B contain t, the public generator, uniform prior, machine and scan-entry protocol. B excludes the sampled input, retained cache, state containing its values and absolute timing. This is explicitly a theorem about this observer of this machine. The observer restriction supplies no universal locality principle for arbitrary SAT algorithms.

## Decoder, framing, capacity and reuse

Let M be the first position with value 1, capped at t when no earlier 1 occurs. Let e_i denote the actual bit-consumption transition for cache cell i, which exists precisely when i<=M. Let Pi be the string of symbols consumed at e_1,...,e_M, and U=Pi. The observation is a subsequence of this actual execution. Its identity decoder uses B to know the cap t and returns the observed word. Allowed records are 0^(m-1)1 for 1<=m<=t and 0^t. They form a prefix-free set. The terminating 1 or the known length t supplies framing, so h=0. No event addresses or timestamps are encoded for the decoder because order and the next cache cell are fixed by the machine and public protocol. The machine still pays to locate and traverse these cells.

Each selected transition reads one binary cache symbol. Thus the record capacity is b=1 for this defined observation channel, even though the machine has other fixed-alphabet symbols and internal control. This does not assert that an arbitrary transition with disclosed timing or state conveys only one bit. For the single record, E={e_1,...,e_M}, rho=1, and |Pi|=|E|=M.

Under the uniform word distribution, every legal record x has probability 2^(-|x|). This holds for both length-t terminal records. Consequently

H(U|B)=sum_x Pr(x)|x|=E[M]=sum_(i=1)^t Pr(M>=i)=sum_(i=1)^t 2^(-(i-1))=2-2^(1-t).

The claimed inequality is therefore instantiated with equality at the record length, giving E[T]>=H(U|B)=2-2^(1-t). Full admission, initialization, movement and output remain in T. This lower bound concerns the chosen scan and does not claim that the total expected computation takes constant time.

Now define, for every j=1,...,t, U_j to be the prefix of U of length min(j,M), Pi_j=U_j, and E_j={e_i:1<=i<=min(j,M)}. Take B_j=B with public index j. The decoder is again identity. The allowed words terminate at their first 1 or reach length j. Hence conditional prefix freedom holds, h_j=0 and H(U_j|B_j)=E[min(j,M)]=2-2^(1-j).

These obligations are defined from the input word and the public stopping rule. They are all recoverable from actual selected events. Correctness does not require the machine to output them separately. In fact it need never materialize them as separate objects.

Every e_i belongs to E_j exactly for j>=i. Its multiplicity is t-i+1. The first event always exists and belongs to all t records, so rho=t exactly, on every execution. Pointwise,

sum_j |Pi_j|=sum_(i=1)^M(t-i+1)<=t M<=t T.

Taking expectations and using the exact prefix entropies yields

sum_j H(U_j|B_j)=2t-2+2^(1-t),

E[T]>=(2t-2+2^(1-t))/t.

The reused-record bound tends to 2. The single-record bound is stronger for finite t. Setting rho=1 for these overlapping E_j would incorrectly count the first physical read t times. The corrected computation needs no multiplication of unrelated maxima.

After the decision is cached, a separate READY read with U=D and the same public background gives a one-bit prefix-free record with b=1,h=0,rho=1. Its entropy on this distribution is h_2(2^-t), since only the all-C word is UNSAT. It can be charged as a distinct actual transition if that transition is explicitly present. Conditioning on the retained answer gives zero answer entropy. Free access to the retained source also determines the entire stopped record. The larger stopped record is optional solver work, while Construction's admission-time OR supplies an even shorter continuation.

## Same-execution physical ledger

Use the existing adjacent-witness compiler without reordering its layout. With c=9t,d=3t, set r=max(3,2 floor((c+1)/2)+1), n0=d+(10c+1)r+2, m0=(20c+4)r, n=n0+m0+3, m=2m0+4 and l=ceil(log2(n+1)). Unary n and delimiter, gamma(m+1), ordered signed literal triples, the two n-bit witnesses and the l-bit release ID occupy exactly

N=3n+2+2 floor(log2(m+1))+3m(l+1)+l=Theta(t² log t).

Construction's authenticated source recovery is charged O(N³) time and O(N) span. Regeneration compares every field and tries the two link types at each position. Writing t recognized bits and keeping a valid-admission flag costs polynomial time within this tariff, including exact indexes, failed candidates and length metadata. No equality hash is used as a semantic certificate. Initialization and retained copies occupy O(N) cells.

The added cache scan uses at most t distinguished reads, O(t log(t+1)) logical counter/bit operations and O(N) total live span, including source, cache, address scratch and output. The conservative indexed single-tape tariff O(N²) per bit operation covers travel, temporary unary address marks and counter work. Because t log(t+1)=O(N), its added time is O(N³). Cache placement, moving to its start, resetting its scan counter, clearing scratch and returning to output fit the same bound. The method chooses a single authenticated path and pays for every failed recognition attempt before fallback.

Thus the admitted path has T=O(N³), S=O(N), and physical CM=sum_tau S_tau=O(N⁴) on that execution. Independently, the fixed deterministic machine, original input and step counter describe a configuration with O(N+log(T+2)) bits, giving minimum-description CM=O(N⁴). These are separate conventions with coinciding upper exponents. Unknown valid inputs use the inherited exhaustive fallback with O(2^n N³) time and O(N) span. All-input correctness is retained, while the polynomial guarantee is restricted to authenticated cycles.

The full T<=K N^a comparison keeps S=O(N^a), physical CM=O(N^(2a)), description CM=O(N^(a+1)), and count-map circuit size O(N^a log N). Our observation demand, after rho, stays below 2. Even its uncorrected O(t) value is below a large enough fixed polynomial cap. The permutation transport control retains internally reviewed single-tape scope, quadratic-time/cubic-cumulative calibration and its static-method ceiling. No strict T5 counting result is asserted.

Three falsifiers are an undisclosed timing or address channel in Pi, reuse rho=1 despite overlapping prefixes, and treating the cached word as free decoder side information while retaining positive conditional entropy. The explicit decoder, multiplicities and B exclusions resolve these for A_scan. The first open general premise is a model-enforced observer and compulsory obligation for every fixed correct solver after its own permitted preprocessing.

## Evidence and fresh searches

The [audit program](../../../experiments/dynamic_accounting_stopped_scan_20261122.py) exhaustively enumerates all link words at t=3,5,7,9,11, for 2728 total inputs. It checks actual read indices, exact event multiplicities, prefix freedom, Kraft equality and all entropy/expected-length identities using rational arithmetic. The [raw output](../../../results/raw/dynamic_accounting_stopped_scan_20261122.json) records exact fractions. This is a new accounting test of the stopped record and overlap, rather than a rerun of Construction's 248 semantic cases. It validates a finite operational scan specification. The compiled single-tape machine, full-checkout preflight, LaTeX and theorem-prover kernel were not executed. Machine-cost exponents are symbolic. Original Construction code/data and our prior Gray ledger were recovered at 4d5d4f24b1cc4d6a86a5560f78c79af9b2ce213d.

Fresh literature query was “Shannon 1948 mathematical theory communication noiseless coding theorem pdf prefix codes entropy.” Read the corrected reprint of Shannon, Bell System Technical Journal 27 (1948), 379–423 and 623–656, section 9 Theorem 9 and the binary coding example in section 10. Its theorem concerns communication rates for a specified source and channel. It does not supply a compulsory SAT observation channel. The finite dyadic-code identities above are proved directly, which avoids importing asymptotic rate hypotheses into a single execution. [Primary paper](https://people.math.harvard.edu/~ctm/home/text/others/shannon/entropy/entropy.pdf).

Fresh official GitHub code searches used “prefix-free” and “entropy” together in anthropics, openai, xai-org, google, google-research and google-deepmind. Five organizations returned no hits. Google first returned HTTP429 and then returned no hits on one retry. OpenAI returned a draft excerpt about conditional Gaussian-observation coding at revision 4eaee87548250b2682affda7d05d947c05554bae. Its full hypotheses were not verified and no theorem from that draft is imported. [Search hit](https://github.com/openai/math/blob/4eaee87548250b2682affda7d05d947c05554bae/preprints/Localization-costs-and-information-growth-for-exact-Gaussian-observations-September-27-2026/build/sections/drafts/replica-localization/predecessor-span.tex).

Ownership was checked through [Anthropic](https://github.com/anthropics), [OpenAI](https://github.com/openai), [xAI's official release](https://x.ai/news/grok-os), [Google's ownership guidance](https://opensource.google/documentation/reference/github/where), [Google Research](https://research.google/resources/) and [DeepMind](https://github.com/google-deepmind). Bounded search absence is not a repository-wide theorem. Mandatory model, coordination, governance and T5 definitions were recovered through GitHub. Publication is confined to Accounting's namespace, script and raw evidence.

DISJ/equality sanity passes as a retained control. Simultaneous DTISP uses one specified execution. The deterministic-configuration bound is an upper description bound. Relativization, Natural Proofs and algebrization supply no unrestricted promotion here. Affine/Tseitin, complement, private-leaf, forced-domain and cached-decision controls remain admissible.

**One next dependency to Bounds and Synthesis.** Identify an actual local observation after full preprocessing for which correctness forces more than the cached answer, and prove its source/state exclusions plus event multiplicity on every relevant solver. Redteam receives the concrete target of an admission-time OR that removes this optional stopped scan. Discovery receives the source-channel mismatch, while Construction's small-separator direction remains a constructive alternative. P versus NP OPEN.
