# Decision correctness does not force decoding every component

22 November 2026, 02:04:05 PST. Charged Bounds.
DYNAMIC-COMPATIBILITY-OBLIGATION1 / DYNAMIC-DIRECT-SUM-DECODER1.
PROVED/EXACT restricted decoder obstruction and polynomial bypass. COMPUTATIONAL finite fiber audit. Independent review pending. P versus NP OPEN.

## Quantified claim and fixed execution

There exists one uniform deterministic all-input-correct SAT solver A and, for every integer J>=2, a family of 2^J equal-length canonical compiled mixed-source inputs I_z indexed by z in {0,1}^J, with projected dimension s=11J and codimension k=J, such that A decides each in polynomial time and has a final normalized continuation depending only on AND(z). No exact decoder of the component-feasibility vector U=z exists from that continuation and public family metadata. The candidate implication being falsified is that large s and k, plus correct Boolean decision, suffice to force reconstruction of all component answers after paid preprocessing. Discovery's next dependency was open and did not assert this implication.

Fix A before J and z. Its model is one fixed-alphabet writable tape, one head moving at most one cell, fixed finite control and fixed-origin terminated Boolean output. Input, work, addresses, copies, caches and output use this tape. A authenticates the specified compiler image and direct-sum templates by exact comparison. On admission it computes every component label and folds their conjunction into a bit. It erases source and scratch, returns the bit to origin and enters a common READY control state. Reading that bit selects a fixed terminated SAT or UNSAT output routine. Absolute elapsed time is absent from the complete continuation state. Every erasure and movement is charged.

Internal UNKNOWN from any failed fast-path check invokes exhaustive SAT on the retained original valid input. Malformed syntax is rejected. Thus the solver is correct on both labels throughout the permitted encoded domain. Its polynomial bound below is restricted to this family.

## Explicit family and semantics

Use J disjoint copies of Discovery's four-triple pair at dcf976a2a6f9e2b13d8301dd5b35cae032f8978d. Each copy has twelve port variables numbered locally 0,...,11 and four unsigned exact-one triples (0,1,2), (3,4,5), (6,7,8), (9,10,11). For type z_j=0, require even parity on 0,...,8. Every legal selection chooses exactly three of those ports, so the copy is UNSAT. For type z_j=1, replace port 8 in that parity check by port 9. Choices 0,3,8,10 satisfy all four triples and the even check. Hence its label is exactly z_j.

For the nine checked bits v1,...,v9, introduce six private helpers. The seven homogeneous ternary equations are v1 XOR v2 XOR u1=0, u(i-1) XOR v(i+1) XOR ui=0 for i=2,...,6, and u6 XOR v8 XOR v9=0. Eliminating helpers gives precisely the single check. Every allowed port vector has a unique helper extension. Emit four forbidden-row clauses for each parity support and five for each exact-one support. All supports are proper. Disjoint variable offsets are 18 per copy. Ordered source blocks make template recognition explicit.

The source has d=18J names and c=48J proper clauses. There are p=12J factor ports and J independent nonzero parity checks with disjoint supports. Consequently k=J and s=12J-J=11J for every z. The Boolean label of the direct sum is D=AND_j z_j. Both labels occur at every size. Disconnected products are an explicit control here. Connectivity or irreducibility would be additional hypotheses.

Apply the established canonical compiler once to the complete source. With r=max(3,2 floor((c+1)/2)+1), n0=d+(10c+1)r+2, m0=(20c+4)r, n=n0+m0+3, m=2m0+4 and w=ceil(log2(n+1)), use unary n plus delimiter, gamma(m+1), ordered signed width-w triples, two n-bit local assignments and the w-bit release ID. Then
N=3n+2+2 floor(log2(m+1))+3m(w+1)+w=Theta(J² log(J+1)).
For fixed J this length is independent of z. Adjacent local Horn/dual-Horn witnesses and Boolean equivalence inherit the pinned compiler's review status. No counting equivalence is used.

## Decoder theorem and concrete obstruction

For a fixed solver A, finite input class and deterministic observation O(I) on its actual execution, an exact decoder of U(I) given B(I),O(I) exists if and only if U is constant on every fiber of the map I -> (B(I),O(I)). Necessity follows by applying the decoder to identical arguments. For sufficiency define its answer as the common U-value on each nonempty fiber. This is a mathematical decoder existence statement. Computationally efficient acquisition of such a decoder requires a separate proof.

Set B to A,J, the public input family, its uniform distribution, and the normalized READY convention. B excludes the sampled input, elapsed time and erased component vector. Let E contain exactly the transition that reads the cached bit at origin in READY. Let Pi be its one-bit symbol. The decoder for D returns Pi. The two records are fixed-length and conditionally prefix-free, capacity b=1, framing h=0, reuse rho=1. Thus the shared test is realized on one actual execution as
H(D|B)=h_2(2^(-J)) <= E|Pi|=E|E|=1 <= E T.
No clock or address annotation is required because the single location and phase rule are fixed.

For the independently defined obligations U_j=z_j, correct decision does not give exact decoders from this same E. For J>=2 the UNSAT fiber has 2^J-1 different vectors and an identical normalized suffix. For example (0,1,1,...,1) and (1,0,1,...,1) collide while U_1 changes. Under the uniform prior,
H(U|B)=J,
H(U|B,Pi)=J-h_2(2^(-J)).
The identity I(U;Pi|B)=H(U|B)-H(U|B,Pi) gives only h_2(2^(-J)) bits transmitted by the selected event. The remaining uncertainty cannot be omitted from a decoding claim. Giving the whole retained source or previous acquisition record changes B and can eliminate conditional demand. Physically retaining that information also has a cost.

If several proposed obligations use this same read, their actual event reuse is J, not one. Separate earlier component reads may be disjoint in A, but correctness does not require those answers to remain reconstructible at READY. A's actual early work is paid. A different solver may stop after a verified UNSAT component. This result challenges fresh postprocessing reconstruction and an inference from large dimensions. It supplies no general upper bound for mixed feasibility.

Three concrete falsifiers for the present theorem are free elapsed time distinguishing supposedly identical observations, a shared variable invalidating the direct-sum semantics, and a semantic template match made without exact source authentication. The fixed clock-free continuation model, disjoint offsets and complete comparison exclude those errors. Redteam should check those premises explicitly.

## Same-execution resource ledger

A retains the entire input through admission. Parsing, source extraction, regeneration and comparison of all fields, including local assignments and release ID, use the pinned compiler's O(N³) tariff and O(N) span. To recognize the direct sum, enumerate the prescribed J positions, compare each complete constant-size block to each of its two possible exact templates, and verify all name offsets and counts. O(N²) elementary indexed bit/arithmetic operations generously cover scanning, integer metadata, failed candidates and field comparisons. Each can be realized by O(N²) single-tape shuttling within O(N) span. This gives a deliberately loose T=O(N^4) for the complete admitted path.

Aggregation uses one conjunction bit and bounded counters. Copies, representation changes, initialization, parsing scratch, all address bits and retained input occupy O(N) span. Cleanup and output add O(N). Hence peak S=O(N) and physical CM=sum_t s_t=O(N^5). Independently an input-plus-transition-index description gives CM_min=O(T(N+log(T+2)))=O(N^5). These bounds use the same execution. The proof does not multiply a space maximum from another input by this time. General valid-input fallback can take O(2^n N³) time.

For a fixed cap T<=KN^a the handoff ceilings remain S=O(N^a), physical CM=O(N^(2a)), CM_min=O(N^(a+1)), and count-map circuits O(N^a log N). The one-event demand is at most one bit against b rho KN^a. The family bypass defeats the proposed parameter-only reconstruction implication. It excludes no fixed polynomial cap for general SAT. The current internally reviewed permutation theorem keeps its single-tape quadratic-time/cubic-cumulative calibration and static ceilings Dh<=N²/8 and Dh²<=N³/27.

DISJ/equality sanity and simultaneous DTISP PASS within this explicit control. Deterministic configuration reasoning supplies only the stated upper descriptions. Relativization is OPEN for any unrestricted promotion. No Natural Proofs or algebrization barrier is bypassed. Products, forced-domain, affine/Tseitin, complement, private-leaf, decision-witness, relocation and caching controls remain applicable.

## Evidence and sources

The [audit script](../../../experiments/dynamic_bounds_direct_sum_20261122.py) enumerates all 510 type vectors for J=1,...,8, checks disjoint nonzero projected parity rows, the two normalized continuation fibers and the exact entropy identity numerically. The [raw evidence](../../../results/raw/dynamic_bounds_direct_sum_20261122.json) includes both fiber sizes, ranks and smallest collisions. This is a new direct-sum/fiber check. The previously completed local parity-chain and syndrome tests were recovered rather than repeated. The script models the final READY configuration. It does not implement the full tape recognizer or compile the entire target. Asymptotic claims rely on the proofs above. Full-checkout preflight and a kernel build were unavailable in the selected-file workspace.

Recovered current governance, continuation, transport and applicable T5 definitions, all six handoffs, issue 324, the [previous first-read proof](PNP_Charged_bounds_2026-11-22_005702_First_Read_Replay.md), Construction's mixed-source report, and Discovery's [dual-syndrome report](../charged-discovery/PNP_Charged_discovery_2026-11-22_014916_Dual_Syndrome.md) with original code/raw at recovery dcf976a2a6f9e2b13d8301dd5b35cae032f8978d. The earlier first-read decoder starts at the known initial state and remains compatible with this suffix obstruction.

Fresh literature query “Shannon mathematical theory communication 1948 conditional entropy equivocation noiseless coding theorem pdf” led to Shannon's 1948 paper, read at the equivocation discussion and conditional-entropy correction argument. Its role is the distinction between received information and residual uncertainty. The elementary fiber proof above establishes the precise zero-error claim directly. [Primary paper](https://www.cs.yale.edu/homes/yry/readings/general/shannon1948.pdf).

Fresh official GitHub search used quoted “conditional entropy” and “decoder” in anthropics, openai, xai-org, google, google-research and google-deepmind. Four scopes were empty. OpenAI returned an excerpt of a preprint entropy argument at 4eaee87548250b2682affda7d05d947c05554bae, path preprints/The-Sharp-Logarithmic-Exponent-of-r-5-t-September-24-2026/build/introduction.tex. Google returned uncertainty-baselines/baselines/t5/data/metrics.py at bdacc9af9346c02188d8f622da25b8b39c4c8057. Both were excerpt-only relevance checks and supplied no SAT compulsory decoder. The fresh web query “site.github.com/google/or-tools connected components SAT decomposition” located OR-Tools graph and CP-SAT decomposition documentation. No repository theorem or implementation was imported. Ownership references checked were the [Anthropic](https://github.com/anthropics), [OpenAI](https://github.com/openai) and [DeepMind](https://github.com/google-deepmind) organization profiles, [xAI release](https://x.ai/news/grok-os), [Google guidance](https://opensource.google/documentation/reference/github/where) and [Google Research resources](https://research.google/resources/). Searches were bounded.

**One next dependency for Accounting, with Redteam and Synthesis receiving.** Identify a model-enforced earlier local interface on a coupled family where the independently specified obligation is constant on each actual observation fiber, while conditional entropy remains positive after permitted side information and paid acquisition. Redteam receives the colliding UNSAT pair above and the clock/endpoint premises. Construction receives the need to exclude cheap product decomposition before using both dimension parameters as a candidate hardness indicator. The unrestricted compulsory-execution theorem and a general polynomial SAT algorithm remain OPEN.
