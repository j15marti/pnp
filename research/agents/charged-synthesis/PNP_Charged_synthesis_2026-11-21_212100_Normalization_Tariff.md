# Normalization does not transfer a read lower bound for free

21 November 2026, 21:21 PST, America/Los_Angeles. PNP Charged Proof Synthesis.
Recovery revision: e78f80d84d240f624fa6193684022431b5ec5e27.

**DYNAMIC-NORMALIZATION-TARIFF1: PROVED/EXACT conditional transfer and restricted obstruction.** Existence of a useful universal normalizer remains OPEN. Independent adversarial review requested from Redteam and Accounting; this integration is not an additional independent certification of their results. No experiment was repeated. P versus NP remains OPEN.

## Selected implication

The strongest new local statement is Redteam's extension of Discovery: at the specified READY representation, even retaining permutation signs does not remove the need to read k table blocks. The first unresolved implication is whether this representation-specific necessity can constrain every original-input solver, perhaps by compiling that solver into the representation.

The correction proved here is quantitative. A normal-form compiler must have a paid overhead small enough relative to the lower demand. Polynomial equivalence alone does not transfer a fixed exponent. In the concrete route that reconstructs an original formula from the product tables, reconstruction itself must read all k blocks. Thus the k-read demand can be entirely met before the simulated solver begins. This is a negative transfer result, not a refutation of the valid k-read theorem.

## Model, lengths, quantifiers and falsifiers

Fix one total uniform deterministic Boolean solver A first, then fixed K>0 and a>=1, before choosing inputs. The physical model is the transport report's one writable tape, fixed finite alphabet/control, one local head, and terminated left-origin output. Source, retained copies, caches, addresses and all transformations are paid. No online schedule, free clock or external source exists.

For Construction's table-chain family, let r>=3,L=2k>=2, n0=(L+1)(2r-3)+2, m0=(L+1)(r²-2)+2Lr+8, n=n0+m0+3, m=2m0+4 and w=ceil(log2(n+1)). Keep the exact original encoded length

    N=3n+2+2 floor(log2(m+1))+3m(w+1)+w
     =Theta(kr² log(kr)).

The input includes ordered signed clauses, the unary variable declaration, gamma clause count, both local witnesses and release ID. SAT iff the composed maps send 1 to 1. This is Boolean decision, not symmetric C, ordered R, historical S/Q, or model counting.

The separate equality calibration has n=8r-1,m=10r and the same encoding grammar, hence N=Theta(r log r). These are different parameter regimes and different physical layouts. A lower bound on one is not added to the other.

Four falsifiers for a normalization transfer:
1. The compiled machine is outside the promised checkpoint class, for example because it retains an extra answer or product cache.
2. A normalization or reconstruction cost meets the whole lower demand before A executes.
3. A simulator has input-dependent overhead or changes length/model, but is treated as constant-factor.
4. Time simulation is used to claim physical or descriptive CM preservation without a separate resource comparison.

The concrete reconstruction realizes (2). The whole-product cache realizes (1) for an unconditional claim of checkpoint membership. Conditions (3) and (4) are explicit premises below, not assumed facts.

## Conditional transfer, with the tariff retained

Let X_N be a specified family of valid N-bit inputs. For every fixed A suppose a uniform wrapper W_A and a map x -> z(x) into the declared representation are supplied. Both labels must be preserved. For every x in X_N require:

* W_A on z(x) is a legal continuation in the representation class for which the lower theorem holds.
* The actual complete wrapper execution has a proved upper bound
  T_W(z(x)) <= q_A(N) + c_A T_A(x),
  where c_A>0 is independent of x,N. Every conversion, authentication, failed candidate, source read, reconstruction, simulation and output step belongs to this bound.
* On that same z(x), the proved representation demand is T_W(z(x)) >= d_A(x).

Then, pointwise,

    T_A(x) >= max(0,(d_A(x)-q_A(N))/c_A).

Proof: substitute the upper bound into the lower bound and rearrange, using nonnegativity of time. If the demand lower-bounds only a suffix of W, it still lower-bounds its total time, so the statement remains valid. No costs from unrelated runs are added. The comparison between two machines is justified solely by the explicit simulation inequality, not by calling them the same execution.

The demand and overhead must refer to the same x. If a theorem supplies only an average demand under one distribution, average the pointwise upper inequality under precisely that distribution. Do not subtract an overhead measured on a different input or distribution. Variable original lengths require E[N^a], not an unjustified power of a mean length.

For the proposed cap T_A(x)<=K N^a, a contradiction requires

    d_A(x) > q_A(N) + c_A K N^a.

With q_A(N)<=Q_A N^d, a sufficient power-law demand is omega(N^max(a,d)); at equality of exponents constants matter. A nonlinear simulation envelope g_A(N,T_A(x)) replaces c_A T_A(x) when necessary, and the cap test becomes d_A(x)>q_A(N)+g_A(N,K N^a). A polynomial-time normalizer of unspecified degree is therefore insufficient to preserve a fixed cap. These elementary inequalities are a proved conditional implication; they do not prove the existence of any useful W, q or large d.

An analogous transfer for either CM convention requires its OWN pointwise inequality CM_W<=q_CM+c_CM CM_A. A time bound alone supplies no such inequality. Long-lived copied input may enlarge physical CM, while self-contained descriptions are a different measure. The report does not infer a CM lower bound on A from W by multiplying independent peak-space and time quantities.

## Concrete failure of a reconstruct-then-simulate repair

For the peer permutation subfamily, G_i=B_i composed with A_i. READY_sign contains the explicit k products and global sign, with fixed other state. Redteam proves that every correct continuation must read k blocks: change one G_i using an even three-cycle sending its current path image to an image that flips the endpoint label. The cache stays unchanged, and both configurations are reachable by A_i=id,B_i=G_i. This works on both SAT and UNSAT states for r>=3.

Consider the natural attempt to make arbitrary A obey this normal form: from READY_sign, regenerate the exact canonical Boolean input x(G) using A_i=id,B_i=G_i, then run A on x(G). The source generator is injective in G: the transition literal identifiers expose every table entry in fixed positions. Therefore ANY deterministic exact regenerator must inspect an original symbol in every product block before completing the output. If it failed on block i, choose a different same-parity permutation there, for example an even three-cycle modification. The sign cache and all other cells agree, so unread-input coupling would produce identical regenerated formulas, although their transition literals differ. This is impossible. There are k disjoint blocks, hence reconstruction alone takes at least k transitions.

Consequently any valid q covering this reconstruction has q>=k on these inputs (or at least supremum q>=k when stated uniformly). Substituting the available demand d=k gives no positive lower bound on A from the displayed transfer. This does not show that every conceivable compiler is expensive; it falsifies THIS proposed repair and identifies the exact quantitative requirement on a different compiler.

The regenerator is not an operation required of the original solver. Redteam's actual full-product solver computes P=G_k...G_1, erases the factors, and answers from P(1). Its suffix is O(r log(r+1)) independently of k. Thus a proof cannot require regeneration just because the proof prefers the READY_sign representation. The actual prefix is paid; no claim is made that the complete original run is constant-time.

## Reconciled dependency graph and status

| Source revision and role | Established scoped statement | Open or rejected implication |
|---|---|---|
| 400ea6f3890fa613d51bf5f4f7b7e80d7f615e75, Construction | Proper Boolean table-chain formula, both-label endpoint equivalence; exact n,m,N; authenticated polynomial fast path | This forced-path family as a superpolynomial hardness candidate is FALSIFIED/RETIRED |
| 5fef2167d60d2ca34bbfa32f3211f5224e1a2380, Bounds | Nested globally fresh information totals at most N; Boolean cleanup preserves polynomial time exponent under its alphabet convention | Repeated global entropy amplification fails; compulsory local views remain OPEN |
| a5ab8fd7d60ecebce8b8ba77c3651da9da853142, Accounting | Actual suffix crossings, terminated state codes, exact decoder from full-string injection, true checkpoint reuse | Resetting an exhausted potential or treating overlapping suffixes as disjoint fails |
| 60d2c55720b028466a7ef3095d3425a14e5851f2, Discovery | Pair products erase odd-layer information; k block reads on its cache-free SAT checkpoint | Online prefix-query service does not transfer to the offline endpoint task |
| e78f80d84d240f624fa6193684022431b5ec5e27, Redteam | Both-label sign-cache k reads; full-product cache bypass; intermediate-path decoder fails | Universal checkpoint membership fails; no claim that the peer's qualified theorem was false |
| 790875f74755a178e8ad810b67ebd603c10f6e89, prior Synthesis | Reachable opposite-label splices suffice for suffix crossing injection | Valid raw-input hybrids do not imply reachable processed-state hybrids |

All statements retain their published review status. Bounds reports internal adversarial review; the newer role reports request review, not external certification. The transport/prepayment baseline has internal review only. This synthesis does not promote inherited results merely because they agree.

Dependency structure: authenticated family -> actual reachable view -> correctness-derived distinguishability -> actual decoder or alternative read argument -> capacity and bounded reuse -> same-run demand -> fixed-cap comparison. The first unresolved edge remains universal existence of a useful view. The attempted alternate edge, arbitrary solver -> normal-form wrapper -> original-solver lower bound, additionally requires the quantitative tariff theorem above. The existing k-read demand does not pay that tariff.

## Same-execution ledger and decoding gates

On the recognized table-family solver, parsing, exact regeneration, candidate discovery/rejection, table validation, pair/full composition, copies, relocation, deletion, retained addresses, sharing, recomputation and output have the peer's conservative T=O(N^4), peak span O(N), physical CM=O(N^5), and descriptive CM=O(N^5), separately. The simpler Construction evaluator has O(N^3) time and O(N^4) cumulative envelopes. These are different algorithms, not costs to add together. Original N remains charged even when a later representation is small.

For any fixed cap T<=K N^a, a>=1, local motion gives S=O(N^a); sum of actual physical span gives CM_phys=O(N^(2a)); source-plus-time replay gives CM_min=O(N^(a+1)). The count-map simulation size O(N^a log N) applies to the specified count transducer and supplies no Boolean decision lower bound here.

The calibrated equality family still supplies Omega(N²) time and Omega(N³) CM in the stated one-tape model, with matching polynomial upper bounds. Time and descriptive CM exclude only a<2; physical CM alone excludes only a<3/2. The static expressions remain bounded by N²/8 and N³/27. The new k-read statement with k<=N excludes no fixed a>=1.

For the accounting route specify U_j, all side information B_j, actual E_j, and conditionally prefix-free Pi_j with an actual decoder and |Pi_j|<=b|E_j|+h_j. The maximum number of memberships of any transition is rho. Only then does

    sum_j H(U_j|B_j) - sum_j E[h_j] <= b rho E[T]

follow by conditional coding and summing actual event memberships. Selecting a cut, checkpoint, address or obligation using source-dependent information requires its own accounted header/conditioning. Decoder simulation is mathematical proof work, not a service imposed on the solver.

At Redteam's normalized decision checkpoint, one valid target is U=Y, with B consisting of solver, dimensions and fixed head/control, optionally the sign, but not tables. Pi records scanned symbols and END, b=ceil(log2(|Gamma|+1)), h=b, E all suffix transitions, rho=1. Replaying the fixed transition function reconstructs addresses and output. H(Y|B)<=1, so this framing gives no positive large entropy bound. Giving full configuration makes entropy zero. Intermediate vertices after full-product normalization are NOT decodable, despite their residual uncertainty. For Accounting's fixed cuts U is the diagonal permutation, B includes the consumed crossing prefix, Pi is remaining states plus END, and reuse across checkpoints counts all suffix memberships. These are different valid or invalid decoders, not interchangeable demands.

DISJ/equality sanity PASS at scoped levels. Simultaneous DTISP PASS only with the stated per-run partitions and explicit simulation comparisons. Deterministic configurations are used through exact coupling/injections, not state-count lower bounds. Relativization, algebrization and Natural Proofs supply no unrestricted barrier bypass. Affine/Tseitin, forced-domain, complement, renaming, private-leaf, shared-computation and decision-witness controls remain legal; neither a prescribed graph nor witness construction is made mandatory.

## Fresh searches and evidence recovery

Read current governance/research instructions, the continuation and transport, prepayment, applicable T5 definitions, six handoffs, prior Synthesis report and current peer reports at the recovered revision. Inspected Redteam's original executable and raw product fibers: 36 configurations, 96 witnesses, six product fibers with constant labels. These are prior COMPUTATIONAL evidence, not a new execution or proof of asymptotics. No code experiment is necessary for the algebraic transfer and injective regeneration proof. No full checkout, preflight or LaTeX build was available. No historical manuscript or peer handoff is changed.

Fresh repository query: '"normalization" "tariff"'. It returned earlier restricted leaf-core/operational-rule tariffs, not a universal compiler; no such result is imported. Branch search charged-synthesis returned none. Issue 324 was read through Redteam comment 7074663435.

Fresh primary query: 'Hennie Stearns 1966 two tape simulation multitape Turing machines T log T pdf'. Read the original JACM paper's model, abstract and Theorem 1, pp. 533 and 541: its constructive simulation uses two tapes and O(T log T) time with machine-dependent constants. This is a warning against silently assuming constant-factor simulation, not a theorem imported into the one-tape checkpoint class. It says nothing about compulsory SAT stages or CM preservation. Primary PDF: https://www.cs.toronto.edu/tss/files/papers/HennieStearns66.pdf . Our tariff implication is proved directly, without using an external hardness assumption.

Fresh GitHub query '"preprocessing" "time-space" "lower bound"' covered anthropics, openai, xai-org, google, google-research and google-deepmind. Google initially returned 429 and returned no matches on the single retry. Four other scopes had no matches. OpenAI returned the computation-reduction section at openai/math commit 4eaee87548250b2682affda7d05d947c05554bae, path preprints/Unconditional-time-lower-bounds-for-Weisfeiler-Leman-equivalence-September-25-2026/build/sections/03-circuits.tex. Its inspected statement uses graph order O(m^6), padding n>=m^20 and O(n^4) multitape construction. These are a different problem, model and length transformation, so its claimed lower-bound consequences are not imported. No kernel or repository code was executed. This source was a lead about explicit overhead accounting only.

Web fallback grouped the same six github.com scopes with preprocessing/time-space or preprocessing/lower-bound. It returned an OpenAI subset-sum introduction, Google OR-Tools parameter/schema files, tabular-ML clipping and unrelated third-party results, with no verified compiler for this target. No commit is asserted for uninspected snippets. No claim of exhaustive absence is made.

Ownership was checked freshly through verified domains on https://github.com/anthropics and https://github.com/openai, https://x.ai/news/grok-os linking xai-org/grok, https://opensource.google/documentation/reference/github/where naming google, https://research.google/resources/ linking Google Research GitHub, and https://deepmind.google/research/publications/122591/ linking google-deepmind/trecvit. Product names alone were not accepted. The separate recent Grok literature log is not a theorem premise of this synthesis.

## One next lemma and receiving assignments

**DYNAMIC-LOW-OVERHEAD-VIEW1, owner Bounds with Construction.** For one independently defined candidate demand, supply either actual original-run views or a uniform wrapper with a proved pointwise overhead/simulation bound and a demand exceeding q_A(N)+c_A K N^a on some same-length inputs. Do not define the demand as optimal remaining runtime. Actual-view existence, the wrapper and a useful quantitative gap are OPEN.

Construction: provide a compact both-label family with shared choices, exact original encoding and admission costs. Bounds: state the quantifier order and prove a positive gap after the tariff. Accounting: audit event membership, decoder framing, reuse, and separate CM simulation inequalities. Discovery: attack the candidate with global algebra and alternate representations, retaining efficient caches. Redteam: independently audit the injective-regeneration argument and seek a lower-overhead wrapper or cached bypass. Synthesis: keep the universal-view and positive-gap edges explicitly open. These are receiving dependencies in this owned handoff and issue 324, not modifications of another role's files.

No new unrestricted exponent is excluded. A polynomial counting result would still require a separate justified decision connection. P versus NP remains OPEN.

## Pinned project sources

- [Construction](https://github.com/j15marti/pnp/blob/400ea6f3890fa613d51bf5f4f7b7e80d7f615e75/research/agents/charged-construction/PNP_Charged_construction_2026-11-21_203000_Table_Composition_Control.md)
- [Bounds](https://github.com/j15marti/pnp/blob/5fef2167d60d2ca34bbfa32f3211f5224e1a2380/research/agents/charged-bounds/PNP_Charged_bounds_2026-11-21_200818_Dynamic_Fresh_Information_Ceiling.md)
- [Accounting](https://github.com/j15marti/pnp/blob/a5ab8fd7d60ecebce8b8ba77c3651da9da853142/research/agents/charged-accounting/PNP_Charged_accounting_2026-11-21_204600_Checkpoint_Overlap.md)
- [Discovery](https://github.com/j15marti/pnp/blob/60d2c55720b028466a7ef3095d3425a14e5851f2/research/agents/charged-discovery/PNP_Charged_discovery_2026-11-21_205117_Pair_Product_Prefix_Queries.md)
- [Redteam](https://github.com/j15marti/pnp/blob/e78f80d84d240f624fa6193684022431b5ec5e27/research/agents/charged-redteam/PNP_Charged_redteam_2026-11-21_211500_Cache_Fiber_Audit.md)
- [Prior Synthesis](https://github.com/j15marti/pnp/blob/790875f74755a178e8ad810b67ebd603c10f6e89/research/agents/charged-synthesis/PNP_Charged_synthesis_2026-11-21_202200_Reachable_Checkpoint_Splice.md)
- [Prepayment and all-checkpoint potential](https://github.com/j15marti/pnp/blob/7ad8794c9a6df14d47c85f9ba4efdc76518c46e5/research/main/Charged_UNSAT_Preprocessing_Tradeoff_2026-11-21.md).
