# Joint preprocessing debit and its information ceiling

22 November 2026, 05:06:20 PST. PNP Lower Bound Connections.
**DYNAMIC-JOINT-PREPAYMENT-DECODER1**, within DYNAMIC-COMPATIBILITY-OBLIGATION1.
**PROVED/EXACT** for the conditional coding implication, its method ceiling and the counterexample below. **CONDITIONAL** for application to arbitrary SAT executions: compulsory decoders and their access restrictions remain unproved. Independent adversarial review is pending. P versus NP is **OPEN**.

The target is the earlier-decoder dependency returned by Accounting at 3154abb2c56b59d8f823ad10af8b27cc348db155. A shared preprocessing statistic can remove the same information from several marginal obligations. Subtracting its entropy only once from a sum of unconditioned marginal demands is invalid. The correct single-debit expression concerns the **joint** obligation, or its conditional chain. This repair has a ceiling: for source-determined obligations on fixed-length N-bit inputs it contributes at most N bits. Repeated physical transport requires additional justified locality, not additional copies of a semantic obligation.

## Exact conditional theorem

Fix a uniform deterministic decider A first, correct on every permitted encoded input. Fix N, a finite distribution X over permitted N-bit inputs, and a declared checkpoint rule 0≤τ(X)≤T_A(X). Let T_+=T_A−τ. The checkpoint can depend on the execution. It is not automatically public side information.

Let B be declared common side information, and let Z be a statistic retained at that checkpoint. Z need not be independent of B or of the source. It need not be the complete configuration. Let U=(U_1,...,U_J) be a fixed finite ordered list of source-defined random variables, chosen independently of a desired lower-bound conclusion. J and the conventions are known from B. Take B_j=(B,Z,U_1,...,U_(j−1)). No additional input-dependent metadata is silently supplied.

For each j assume all of the following on this one execution:

1. E_j(X) is a subset of actual suffix transitions τ+1,...,T_A. Every transition belongs to at most a deterministic ρ≥1 of the sets.
2. There is a binary record Π_j whose possible distinct strings are prefix-free conditional on each positive-probability value of B_j.
3. One fixed exact decoder satisfies H(U_j|B_j,Π_j)=0.
4. Pointwise |Π_j|≤b|E_j|+h_j, with b≥1 fixed and h_j≥0. Addresses, selectors, counts, variable-length fields, timing, basis metadata and any other annotations needed by that decoder are counted here or explicitly in B_j.

Then

E[T_+] ≥ max(0, (H(U|B,Z)−Σ_j E[h_j])/(bρ))
         = max(0, (H(U|B)−I(U;Z|B)−Σ_j E[h_j])/(bρ)).       (1)

In particular, replacing I(U;Z|B) by H(Z|B), or by the expected length of a conditional prefix code for Z, gives a possibly weaker valid bound. This is not an assertion that the physical cost of producing Z equals its entropy.

Proof: for each conditional code, Kraft's inequality and nonnegativity of relative entropy give H(Π_j|B_j)≤E|Π_j|. Explicitly, for a fixed side value, put q(p)=2^(−|p|)/K with K=Σ_p2^(−|p|)≤1. Then E|Π_j|−H(Π_j)=D(P||q)−log2 K≥0. Deterministic decoding gives H(U_j|B_j)≤H(Π_j|B_j). Summing, applying the conditional chain rule, and using the pointwise overlap bound gives

H(U|B,Z) ≤ Σ_j E|Π_j| ≤ b E[Σ_j |E_j|]+Σ_j E[h_j]
                           ≤ bρ E[T_+]+Σ_j E[h_j].

The mutual-information identity proves the second form. Empty records are legal only on conditional fibers where their prefix-free support is the singleton empty string.

The actual acquisition time is E[T_A]=E[τ]+E[T_+]. A separately proved prefix bound can be added because these intervals partition the same run. Prefix costs must not be taken from another input or another solver. If prefix and suffix code arguments charge overlapping events, their reuse must be audited before addition. The proof decoder need not run efficiently; neither its auxiliary computation nor Z becomes a free physical operation available to A.

This common-side-information result does not authorize replacing the different B_j of an existing local-view argument by one global B without checking the resulting conditional entropies. Conversely, the original marginal-sum theorem remains valid with its original exact decoders, lengths and reuse. Equation (1) is a particular safe joint formulation, not a claim that every valid local lower bound must telescope.

## Method ceiling and the invalid stronger rule

If U is a deterministic function of X and B, then

H(U|B,Z) ≤ H(X|B) ≤ N.

Thus the positive numerical lower-bound certificate supplied by (1) alone is at most N/(bρ), and at most N under b,ρ≥1. The same is true if the preprocessing debit is replaced by the larger H(Z|B). This bounds this certificate, not the solver's runtime. A difficult decision function can have only one output bit and still be computationally difficult. Choosing Z to contain the source makes this conditional demand zero without constructing a fast algorithm.

This ceiling does not refute the project's quadratic crossing theorem. Separate physical cuts have distinct locally justified views, and the same source information can require transport across many separated cuts. Such demands are not the joint entropy of one globally informed decoder. The internally reviewed single-tape permutation control retains its matched quadratic-time and cubic-cumulative bounds. A new dynamic argument must prove its local views and subsequent necessary events after relocation.

The rejected stronger rule is
E[T_+] ≥ (Σ_j H(U_j|B)−H(Z|B)−Σ_j E[h_j])/(bρ)
under only the conditional decoders given B,Z. It drops correlations among obligations and fails even with a genuine decision bit, both labels, legal preprocessing and precisely identified suffix events. No peer is asserted to have claimed this stronger rule; it is the transfer hypothesis tested in this run.

## Concrete both-label execution

Use Construction's three-marked-column family at 009932ebaf093a18c19378261d0123f0c0c3297e [2]. For every odd t≥3 choose M uniformly from the three-element subsets of {0,...,t−1}. Independently choose either both words A^t or both words C^t with probability one half. The marker data occur explicitly in the authenticated input.

The AA relation on successive z bits is {(0,0),(1,1),(1,0)}. The all-zero closed walk satisfies every homogeneous marked parity check, so A^t/A^t is SAT for every M. The CC relation is {(0,1),(1,0)}. An odd number of flips cannot close, so C^t/C^t is UNSAT for every M. Let D be the SAT bit. Then M and D are independent and H(D)=1. This is a both-label distribution on formulas of the same compiled length, not an all-UNSAT promise.

Fix one full decider A* before t,M and the label choice. It authenticates the compiler image and marked family; on these two uniform word patterns it applies the proved scalar test. On other authenticated marked-family words it uses Construction's eight-bit relation evaluator. On valid nonmatches it decides exhaustively from the retained formula. Unknown admission is never reported as UNSAT. All parsing, failed recognition, exact regeneration, copying and motion are charged.

Before its final transition A* stores M in three increasing ell-bit fields, ell=ceil(log2 t), and D at the output origin with its framing already prepared. It places the head at origin in state READY. Define τ as this checkpoint. The next transition reads D and halts in the appropriate decision state, leaving the prepared output. Thus T_+=1. Z=M is a declared projection of the retained configuration, excluding D, the source and the clock; it is not a claim that these other data are physically absent.

For any public r≥1 take U_1=...=U_r=M and U_(r+1)=D, B=(t,r,A*,family,prior,READY convention). For j≤r, use E_j=empty and Π_j=empty. The decoder returns Z. For the final obligation, E_(r+1) is the single actual READY transition and Π_(r+1) its one-bit payload. Its identity is specified by the public state convention, not an input-dependent timestamp. The decoder returns this bit. Conditional codes are singleton empty strings or the two one-bit strings. Capacity b=1, overhead h_j=0, reuse ρ=1.

Consequently H(U|B)=log2 binom(t,3)+1, I(U;Z|B)=log2 binom(t,3), and (1) gives exactly E[T_+]≥1. Repeating M produces no new events or required service. The invalid marginal rule instead gives 1+(r−1)log2 binom(t,3). At t=5,r=5 this is approximately 14.287712 bits against exactly one suffix transition. The contradiction is symbolic for all t≥5,r≥2.

The repeated M variables are not asserted to be compulsory decision-sensitive obligations. Their purpose is to falsify a proposed accounting inference. Only the final D decoder follows directly from this chosen decision protocol. Earlier input reads remain real and paid; this counterexample says nothing against a separately proved earlier local obligation. Giving the complete retained source to a decoder, or adding D to Z, makes the corresponding conditional demand vanish. Removing those data from side information without proving an actual sufficient transcript leaves the decoder premise open.

## Encoding and complete same-execution costs

Use the pinned ordered proper-3-CNF source and adjacent-witness compiler [2]. Source counts are d=8t, c=26t+4. Let
g=max(3,2 floor((c+1)/2)+1),
n0=d+(10c+1)g+2, m0=(20c+4)g,
n=n0+m0+3, m=2m0+4, w=ceil(log2(n+1)).
The full binary encoding has
N=3n+2+2 floor(log2(m+1))+3m(w+1)+w=Θ(t² log t).
It includes unary names, clause-count framing, signed literal addresses, both supplied witness strings and the release identifier. Boolean equivalence and physical compilation use the pinned compiler proof; semantic clause order does not impose a processing order.

The model is one deterministic finite-alphabet writable tape, one head moving at most one cell per primitive step. Charged span contains origin, head and all nonblank cells. All input, caches, address registers, copies and output share that tape.

| Work or resource | Charged bound and qualification |
|---|---|
| Generate source and compile image | Explicit polynomial construction, within inherited O(N³) single-tape tariff |
| Admission and failed candidates | Retain input; regenerate and compare every field, witnesses and release ID; O(N³) time, O(N) span |
| Word and marker extraction, scalar test, eight-bit fallback | Indexed operations, counters, marker normalization, address motion and buffers included in the same O(N³) tariff |
| Retention, relocation, caching and output | O(N) peak span; final READY preparation paid in prefix, one final transition in suffix |
| Full admitted-family execution | T=O(N³), S=O(N) |
| Physical cumulative storage | Σ s_k=O(N⁴) on this same run |
| Minimum-description cumulative storage | Independently, input and step index describe configuration in O(N+log(T+2)) bits, giving O(N⁴) |
| Arbitrary valid nonmatches | Failed recognition plus exhaustive fallback O(N³+2^n N³), O(N) span |

These are symbolic inherited implementation bounds, not measured native-machine timings. The final cache adds at most O(log t) bits and polynomial cursor work. The statistics supplied to a proof decoder do not waive their physical acquisition or retention. No free hashing or semantic merging is used.

For T≤K N^a with fixed a≥1, compare (1)'s numerator to bρ E[T_+] and hence to bρ K N^a. Its source-information ceiling cannot defeat any superlinear cap. The generic same-execution ceilings remain S=O(N^a), physical CM=O(N^(2a)), minimum-description CM=O(N^(a+1)), and count-map circuit size O(N^a log N). No exponent is excluded here; counting is separate from decision. No multiplication of unrelated time and space maxima is used.

## Falsifiers, evidence and status gates

Four concrete falsifiers are: retaining M but charging its marginal entropy r times with a single debit; omitting event-selection or basis metadata from the record; claiming a shared local-information restriction follows from an unrestricted offline tape; and interpreting the N-bit certificate ceiling as a polynomial algorithm. The construction and proof above resolve the first and delimit the others. The first genuinely open premise remains a noncircular, model-derived earlier decoder for every correct solver after paid joint preprocessing.

[Finite checker](../../../experiments/dynamic_bounds_joint_prepayment_20261122.py) and [raw evidence](../../../results/raw/dynamic_bounds_joint_prepayment_20261122.json) enumerate all marker sets and both uniform word labels for t=3,5,7,9: 260 input samples, with r=1,2,5. Independent z-walk enumeration checks the restricted labels. Exact fibers contain one SAT and one UNSAT input per marker set. Every conditional record decodes, and the charged suffix payload is exactly one bit. Entropies use floating logarithms as diagnostics; the all-t proof uses exact cardinalities. No seed, native tape simulation, integrated compiler run or kernel certification is claimed. The new experiment tests joint versus marginal prepayment, not the completed absorbing-scan experiment.

DISJ/equality sanity PASS as retained polynomial controls. Simultaneous DTISP PASS for the stated symbolic execution. Deterministic-configuration counting is used only for the upper description bound. Relativization, algebrization and Natural Proofs yield no separation step. Affine/Tseitin, complement, private-leaf, forced-domain, decision-witness, relocation and shared-computation bypasses remain legal. This report does not transfer strict T5 counting, symmetric C or ordered R results.

## Fresh sources and bounded search record

[1] C. E. Shannon, *A Mathematical Theory of Communication*, corrected reprint of Bell System Technical Journal 27 (1948), section 6, pages 11–12 of the PDF. Fresh query: “Shannon 1948 mathematical theory communication conditional entropy joint entropy pdf”. Read the finite discrete joint/conditional entropy identities and subadditivity. Only those finite identities are imported; the conditional prefix-code inequality is proved above. No stationary-source or online theorem is transferred to offline SAT. [Primary text](https://people.math.harvard.edu/~ctm/home/text/others/shannon/entropy/entropy.pdf).

[2] [Construction, 009932eb](https://github.com/j15marti/pnp/blob/009932ebaf093a18c19378261d0123f0c0c3297e/research/agents/charged-construction/PNP_Charged_construction_2026-11-22_043212_Three_Marked_Columns.md). Report and original generator/raw recovered. Both-label semantics, exact counts, canonical image authentication and eight-bit solver. The source file's decide routine was inspected; this run uses independent z-cycle enumeration only for its uniform-word control.

[3] [Accounting, 3154abb2](https://github.com/j15marti/pnp/blob/3154abb2c56b59d8f823ad10af8b27cc348db155/research/agents/charged-accounting/PNP_Charged_accounting_2026-11-22_043943_Marked_Absorption.md). Its one-time marker record and conditional summary chain are preserved. The present result does not invalidate its ledger.

[4] [Discovery, 8a911c17](https://github.com/j15marti/pnp/blob/8a911c17dbb97d350c997cfbb90c5cf818a67ed3/research/agents/charged-discovery/PNP_Charged_discovery_2026-11-22_045216_Syndrome_Trellis.md). Report, code and raw recovered. Its paid syndrome solver is constructive on bounded rank; its H=[I I I] control rejects compulsory full-code trellis inference. No general polynomial-rank guarantee is inferred.

[5] [Prior Bounds event-selector theorem](PNP_Charged_bounds_2026-11-22_035605_Event_Selection_Decoder.md). Selector/framing charges remain mandatory. The new lemma additionally conditions on shared preprocessing and prior obligation values.

[6] R. Clifford, M. Jalsenius and B. Sach, *Cell-Probe Lower Bounds for Bit Stream Computation*, ESA 2016, article31, DOI10.4230/LIPIcs.ESA.2016.31. Fresh obstruction query: “Clifford Jalsenius Sach 2016 bit stream computation information transfer conditional entropy known outside interval online lower bounds”. Rechecked the primary model and introduction: each arriving symbol requires an answer before the next symbol is processed; the argument reconstructs past updates from required interval outputs and audits probe overlap. These required online outputs are absent from offline SAT. This supplies a concrete reason not to treat syntactic stages as repeated obligations. The prior selector report already reviews its detailed address/content decoder; that deep review was not repeated. [Primary paper](https://drops.dagstuhl.de/storage/00lipics/lipics-vol057-esa2016/LIPIcs.ESA.2016.31/LIPIcs.ESA.2016.31.pdf).

Fresh connected GitHub searches used `"conditional entropy" "mutual information"` separately in anthropics, openai, xai-org, google, google-research and google-deepmind. Anthropic, xAI and DeepMind had no hits. Google first returned HTTP429, then no hits on one retry. OpenAI returned elementary information-theory definitions and a quantum-entropy excerpt; Google Research returned n-gram entropy reporting. None supplies the missing compulsory decoder. Inspected search-excerpt revisions:
- openai/math 4eaee87548250b2682affda7d05d947c05554bae, `preprints/Bounded-Step-Walks-on-Gaussian-Primes-September-26-2026/build/preliminaries.tex` and `preprints/A-two-dimensional-area-law-from-a-global-spectral-gap-September-24-2026/build/sections/01-preliminaries.tex`.
- google-research/google-research 87e25a5ba04d2c4cf0108f0cec96d648fe2b945a, `homophonous_logography/entropic/ngramcrossentropy-main.cc`.

[OpenAI classical excerpt](https://github.com/openai/math/blob/4eaee87548250b2682affda7d05d947c05554bae/preprints/Bounded-Step-Walks-on-Gaussian-Primes-September-26-2026/build/preliminaries.tex) · [OpenAI quantum excerpt](https://github.com/openai/math/blob/4eaee87548250b2682affda7d05d947c05554bae/preprints/A-two-dimensional-area-law-from-a-global-spectral-gap-September-24-2026/build/sections/01-preliminaries.tex) · [Google Research excerpt](https://github.com/google-research/google-research/blob/87e25a5ba04d2c4cf0108f0cec96d648fe2b945a/homophonous_logography/entropic/ngramcrossentropy-main.cc).

These were excerpt inspections, not full-paper validation, theorem imports or external code execution. Web fallback queried the first three organization paths with `"conditional entropy" preprocessing`, and the Google/Research/DeepMind paths with `"conditional entropy" caching`. It surfaced OpenAI Fourier entropy foundations and Google Research compressive visual representations, plus differently owned repositories. None justified a SAT execution restriction; no additional code was imported. A preliminary query using conditional-mutual-information/entropy/preprocessing also ran, but its displayed results were truncated, so no findings are attributed to it.

Official ownership was verified via domain-verified [Anthropic](https://github.com/anthropics) and [OpenAI](https://github.com/openai) profiles, [xAI's link to xai-org/grok](https://x.ai/news/grok-os), [Google's organization policy](https://opensource.google/documentation/reference/github/where), [Google Research's GitHub link](https://research.google/resources/) and [DeepMind's link to google-deepmind/alphafold3](https://deepmind.google/science/alphafold/).

Mandatory governance, continuation, transport, applicable T5 resource definitions, owned handoff, relevant peer reports and issue324 were recovered at 8a911c17dbb97d350c997cfbb90c5cf818a67ed3. Repository duplicate query `"preprocessing" "joint entropy"` found the earlier restart/replay audit, which cites the same elementary entropy identity but studies a different execution. A charged-branch search returned no branches. The environment has selected files rather than a complete checkout; full-checkout preflight, LaTeX build and integrated tape checks were not run. No historical TMR manuscript ownership or agent settings were changed.

**One next dependency, to Accounting and Synthesis:** exhibit a model-enforced local decoder for an earlier event on the next candidate, with retained-source and basis access accounted for, whose demand survives paid preprocessing without treating a globally conditioned joint entropy as replenished information. Redteam receives the one-transition marked-family execution as the explicit falsification target for a marginal single-debit claim. Construction and Discovery retain their verified restricted algorithms. Any substantial all-solver transfer requires independent adversarial review.
