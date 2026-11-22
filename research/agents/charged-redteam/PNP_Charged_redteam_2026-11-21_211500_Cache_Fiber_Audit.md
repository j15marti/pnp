# Which cached summaries preserve a compulsory block read?

21 November 2026, 21:15 PST, America/Los_Angeles. PNP Independent Counterexamples.

**DYNAMIC-CACHE-FIBER-AUDIT1. PROVED/EXACT restricted audit**, with the proofs below; **COMPUTATIONAL** finite evidence. This reconstructs Discovery's particular checkpoint claim at revision `60d2c55720b028466a7ef3095d3425a14e5851f2` [1]. It is an independently implemented reconstruction in the same continuing conversation, not external independent review. Further adversarial review is requested. No manuscript ownership is acquired.

Discovery's k-block read obligation is sound for its stated cache-free representation. It even survives a cached global permutation sign and holds on both decision labels. It does not survive arbitrary joint preprocessing: retaining the full composed permutation permits erasure of every intermediate table and decision without revisiting those blocks. The peer already excludes supplementary summaries from its positive corollary. Consequently this is a scope audit and a counterexample to an unrestricted extension, not a refutation of the peer's stated theorem. The generic certificate argument is established methodology, including repository predecessor TMR2-QUERY17 [3]; the new audit concerns reachable cached permutation configurations.

## Exact target, model and falsifiers

Use Construction's Boolean family [2], with r>=3, k>=1, L=2k, endpoints s=t=1, and explicit permutations A_i,B_i of [r]. Let G_i=B_i composed with A_i, V_0=1, V_i=G_i(V_{i-1}), and Y=[V_k=1]. Construction proves SAT iff Y=1 in both directions: exactly-one layer constraints force the path; the terminal pin accepts precisely the stated endpoint; a valid path extends through padding and compiler auxiliaries. This report uses that source projection with its internal review status and audits the subsequent representation, not a new count transformation. Symmetric strict C, ordered R and historical S/Q are not the predicates here.

Fix a deterministic total uniform solver before choosing parameters or distributions. Its machine has one writable tape, one head moving at most one cell per step, a fixed finite alphabet and finite control, no free clock or source oracle, and terminated Boolean output at the origin. All initial source cells, preprocessing, retained data and accesses are charged. A transition reads its scanned symbol before writing. No online schedule is imposed. Our lower statement quantifies over **every deterministic continuation correct on every reachable configuration of the specified READY domain**. It does not assert that every correct original-input solver reaches that domain. The bypass is one fixed globally correct solver with exact admission and an exhaustive fallback.

Four falsifiers are explicit:

1. The opposite-label modified table also changes the retained summary, invalidating the proposed single-block difference.
2. A claimed READY configuration is not reachable after the same authenticated preprocessing, or residual data, head position or timing distinguishes the purported fiber.
3. Whole-product preprocessing or a cached decision lets the continuation avoid the original blocks.
4. A claimed decoder reconstructs intermediate vertices from a suffix that depends only on their many-to-one product.

The sign-cache proof excludes (1) and (2) in its declared domain. Whole-product preprocessing realizes (3), and its fibers realize (4). These controls preserve both labels.

## One reachable-configuration criterion

For a fixed solver and a fixed checkpoint domain D, require the same head position and control on entry, the same publicly blank output area, and finite tape contents. Every C in D must actually be reachable from an admitted source; its label is the required decision of that source. A correct continuation makes the label well-defined. For opposite-label C,C' define Diff(C,C') as the tape positions at which their checkpoint symbols differ.

Let Q(C) be the set of positions whose checkpoint symbols are observed by the continuation on C before those symbols are overwritten. Then

    Q(C) intersects Diff(C,C') for every opposite-label C' in D.

**Proof.** If no differing original symbol is observed, couple the two continuations. Until their first differing read, control and head agree, so every write, move and decision agrees. A first visit to a differing cell reads it before any overwrite and is exactly the forbidden differing observation. Cells written earlier have identical new symbols in both runs. Thus no first disagreement can occur, and both runs halt with the same decision, contrary to correctness. This is an actual-execution argument, not a requirement to compute a hypothetical residual query.

If each C has k opposite-label alternatives differing only in pairwise disjoint physical blocks, the first differing observations supply k distinct actual transitions. Therefore T_suffix(C)>=k. Arbitrary further copying, relocation, adaptive order, sharing and recomputation after C are permitted by the coupling. The substantial premise is the existence of those **reachable alternatives preserving everything outside the chosen block**, including cached summaries. Restricting D to all-UNSAT states would leave no such alternative and no bound.

## Positive audit: a global sign cache preserves the alternatives

Define READY_sign to contain the ordered G_i tables in k fixed disjoint blocks, the dimensions, and the bit

    Z = product_i sgn(G_i).

All other cells are blank or fixed for these dimensions; head and control are fixed. Recognition, pair composition, sign calculation, copying and erasing are paid in the prefix. No prefix duration is made available at READY. Every product list is reachable: choose A_i=id and B_i=G_i, generate the original legal input, and run this same normalization. This proves reachability rather than assuming arbitrary checkpoint splicing.

Fix any product list and any block i. Write v=V_{i-1}, u=G_i(v), and Q=G_k composed with ... composed with G_{i+1}, with identity for an empty suffix. If Y=1, choose any u'!=u. If Y=0, choose u'=Q^{-1}(1), which is unequal to u. Choose a third element different from u,u', possible because r>=3. There is a three-cycle c sending u to u'. It is even. Replace only G_i by c composed with G_i. The new endpoint is Q(u'), so its decision is opposite to Y; all table signs, hence Z, are unchanged. The altered state is reachable by the preceding factorization. Outside block i nothing changes.

The criterion proves **T_suffix>=k on every SAT and every UNSAT READY_sign configuration**, for every correct continuation on this domain. This strengthens the peer's cache-free SAT corollary in a precisely limited direction. Even retaining the entire vector of table signs would preserve this particular argument. The statement fails at r=2: the sign of the full product already determines its action on 1. That excluded-dimension control is executed below.

For each input and i, choose the lexicographically first three-cycle in this proof that flips its label. E_i is the singleton containing the first actual transition observing a differing checkpoint symbol relative to that alternative. These are genuine events; distinct i have disjoint E_i, so their reuse is one. This counts one necessary read per block, not entropy of an independent answer per block. The identity of an event, if transmitted as a separately selected record, would itself require paid address/time framing. No such free record is used in the coupling proof.

## Negative audit: full product is enough, without an answer-only cache

Let P=G_k composed with ... composed with G_1. A fixed solver can compute P as an explicit r-entry table, retain it, and erase G_1,...,G_k and all original source/work data. Put a self-delimiting r header and P at the origin, other dimension information afterwards, clear the output slot and return to a fixed READY_product control. No answer bit need be computed or stored during this normalization. From this state a continuation reads P(1), compares it with 1 and emits Y. Scanning the whole r-entry table and returning to the origin gives the safe bound O(r log(r+1)) suffix time, independent of k. For fixed r=3 this is O(1), despite unbounded k and growing original input length.

This is not free preprocessing. The end-to-end polynomial charges are below. It directly defeats an attempted assertion that the syntactic k stages force k *additional* reads after any paid preprocessing. Unlike an all-UNSAT promise, the retained product ranges over both decisions. Unlike merely retaining the decision, it supports every start/end query on the composition. If all G_i were also retained, changing one G_i would generally change the P cache; an opposite-label perturbation cannot preserve P, so the disjoint-support proof still fails.

For independently uniform G_i, each P has exactly (r!)^(k-1) preimages: choose G_1,...,G_{k-1} freely and determine G_k uniquely. For k>=2 the intermediate vector W=(V_1,...,V_{k-1}) is uniform on [r]^(k-1) conditional on P. Indeed each desired vertex at stage i<k leaves (r-1)! choices for G_i, and G_k is then forced. Thus

    H(W | P) = (k-1) log2 r.

The entire READY_product suffix is a deterministic function of P and public dimensions. Consequently even all suffix events and the full checkpoint do not decode W; the residual conditional entropy is unchanged. This is not a demand that the solver compute W. It is the reason that proposing W as a compulsory decoded target is invalid on this legal run. The peer's odd-factor-vertex obstruction is credited, not retested; this test concerns the additional collapse of the product-list checkpoint itself.

An answer-cache implementation is an even smaller control: compute Y once in the prefix, retain it next to the fixed output area, and use O(1) suffix transitions. It was already identified by Construction and Discovery. We do not claim that control as a new result.

## Actual decoder and entropy ledger

There is an actual decoder for the decision, with a much smaller demand than the fictitious vector of intermediate services. For either normalized solver take one obligation U_1=Y. Let B_1 include the fixed solver, public dimensions, fixed starting head/control, and optionally Z in the sign-cache version. It excludes all table contents. The public output area is initially blank. Let E_1 contain every suffix transition through output and halt. Encode each scanned tape symbol using b=ceil(log2(|Gamma|+1)) bits, with a reserved END code after halt. Pi_1 is this read-symbol sequence plus END, h_1=b, and rho=1. Fixed-width symbols and a unique END make the actual records conditionally prefix-free.

The decoder simulates the fixed transition function from the known control and head using successive recorded read symbols. It recovers the writes, real unit head moves, absolute addresses relative to the known origin, and output. It consults no source oracle or virtual residual service. Previously written and public cells can be checked for consistency. Address strings are not transmitted separately because the fixed machine's moves determine them from the record; if that model premise is removed, the record must change. An explicit simulation with finite dictionaries and binary addresses has a conservative polynomial cost in |Pi_1|+|B_1|; it is a proof decoder, not uncharged work imposed on the solver. All solver-side movements and address manipulation remain actual transitions in E_1.

Conditional source coding and exact decoding give

    H(Y | B_1) <= H(Pi_1 | B_1) <= b E[T_suffix] + b,
    E[T_suffix] >= (H(Y | B_1) - b)/b.

For uniform permutation tables, even conditioned on Z, Y is Bernoulli(1/r). Each parity coset acts transitively on [r] for r>=3, so conditioning on a parity leaves the relevant image uniform. Hence the entropy here is only h_2(1/r)<=1. With this framing the numerical bound is vacuous. The k-read bound comes instead from the proved disjoint opposite-label perturbations, not from k independent output obligations. Giving the whole configuration as B_1 makes the entropy zero. For W at READY_product, the required decoder does not exist. Reusing one suffix record for k proposed obligations would have rho=k, not one. These distinctions prevent a formal entropy inequality from claiming compulsory work that the execution does not perform.

## Encoding, full cost ledger and cap comparison

Keep exactly Construction's source and physical input length [2]. With L=2k,

    n0=(L+1)(2r-3)+2,       m0=(L+1)(r^2-2)+2Lr+8,
    n=n0+m0+3,             m=2m0+4,
    w=ceil(log2(n+1)),
    N=3n+2+2 floor(log2(m+1))+3m(w+1)+w
      = Theta(kr^2 log(kr)).

This serializes unary n, gamma(m+1), ordered signed literal identifiers, two n-bit local witnesses and the release-variable ID. All 2k source permutation tables are explicit. No truth table of exponentially many paths is hidden in k. The transformed READY representation is work data, not a redefinition of input length N.

One fixed total solver first parses and authenticates the complete canonical formula, witnesses and metadata by exact regeneration. Enumerate bounded candidate parameters, charge rejected candidates, validate permutations by pairwise entry comparisons, and accept only exact byte equality. Failure is UNKNOWN from the recognizer followed by correct exhaustive Boolean fallback on the retained source, never inferred UNSAT. Successful recognition then performs pair composition and the selected cache transformation. Product composition uses O(kr) indexed table lookups/writes; global sign by inversion counts uses O(kr^2) field comparisons. Indices, counters and entries have O(log N) bits and are stored and accessed on the same tape.

| Component on a recognized run | Conservative paid bound |
|---|---|
| Parsing, all parameter trials, failed candidates, exact regeneration and comparisons | O(N^4) single-tape steps |
| Validate tables, compose pairs/full product, calculate sign, retain buffers | Fits O(N^4), O(N) occupied/visited span |
| Copy to canonical offsets, erase source and scratch tracks, normalize head/control | Fits O(N^4); no free reset |
| Sign-cache continuation | At least k reads; an explicit path evaluator fits O(N^4) |
| Full-product continuation | O(r log(r+1)) steps, independent of k |
| Original input, tables, copies, cache, address bits, output | O(N) peak span on this same run |
| Physical CM, sum of actual charged storage over transitions | O(N^5) end to end |
| Input-charged minimum-description CM | Separately O(N^5) end to end |

To justify the loose envelope, use O(N) parameter candidates and at most O(N) bounded field operations per candidate, implementing each in O(N^2) sole-tape steps with sweeps and elementary bounded arithmetic. Successful pairwise permutation checks and sign calculations take O(kr^2)=O(N) field operations; composition takes fewer. Input, extracted representation, regenerated candidate, temporary product buffers and counters occupy O(N) bits with constant tracks. Invalid headers are bounded against available length before allocation. An N-bit source, fixed solver and self-delimiting time index describe each deterministic configuration in O(N+log(T+2)) bits, giving the separate descriptive upper bound. These are implementation envelopes, not measured physical-TM runtimes.

Erasing the source does not license dropping the input charge. In particular we may safely charge O(N r log(r+1)) to either cumulative convention for the short product suffix; we do not claim constant CM when r is fixed and original N grows. The same-execution upper bounds include discovery, all actual accesses, sharing, conversion, adaptive rejection/fallback dispatch and output. The fallback is total, but no global polynomial bound is claimed outside the recognized family.

For any separately fixed cap T_A<=K N^a, a>=1, the comparison ceilings remain S=O(N^a), physical CM=O(N^(2a)), and minimum-description CM=O(N^(a+1)). Our k-read floor is below N and does not defeat any of these polynomial exponents. A hypothetical entropy demand would need to exceed b rho K N^a after subtracting framing on the same run. The O(N^a log N) count-map circuit ceiling is not a decision theorem and is unused here. The different separated map-equality family retains its internally reviewed matching O(N^2) time/O(N^3) cumulative calibration and static-method ceilings; nothing here resets or adds its potential to another execution's costs.

## Reproducible evidence, controls and source search

Run `python experiments/dynamic_redteam_cache_fibers_20261121.py`. [Code](../../../experiments/dynamic_redteam_cache_fibers_20261121.py) and [raw evidence](../../../results/raw/dynamic_redteam_cache_fibers_20261121.json) exhaust all 36 product lists at r=3,k=2. They have 12 SAT and 24 UNSAT labels. All 96 enumerated label-flipping three-cycle changes preserve the global sign and alter one block. For each configuration the minimum whole-table certificate given sign is two; given the answer cache it is zero. Counting the cache as a queried coordinate gives minima two and one, respectively. Whole-table queries are stronger than single-cell reads, and the tests are not machine timing measurements.

The six full-product fibers each have six members and a constant decision label. Each of the three intermediate vertices occurs twice in every fiber. The excluded r=2,k=1 control has zero table queries given sign, confirming the necessity of r>=3. Exact source parameters at the tested size are n0=17,m0=67,n=87,m=138,w=7,N=3596. This calculation preserves the peer's encoding; the old 1,296 source-factorization/CNF-admission experiment was not rerun. The generator projection and asymptotic proofs above are separate from these finite checkpoint tests. The experiment was extended once to test the full-product bypass after the task moved to the Redteam audit; no unchanged completed experiment was rerun as a claimed advance.

Code SHA256: `32828b06df864ddac06346ef8833b3a984ab5ca9cf9fb7eea603c376603bf7ab`.
Raw SHA256: `9cc9c23074531a9fddde7a01d853295eec215876637580a871581f0c574cce7d`.

DISJ/equality sanity PASS at restricted scope: perturbations have opposite labels, not merely distinct descriptions. Simultaneous DTISP PASS for the single displayed recognized execution. Deterministic-configuration gate PASS as a coupling argument, not a state-count runtime bound. Relativization, Natural Proofs and algebrization supply no barrier bypass; unrestricted transfer remains OPEN. Relocation and shared global algebra are the bypass. Complementing the decision preserves the perturbation argument. Renaming changes physical offsets and must be paid/authenticated, not assumed to preserve admission. Forced-domain/path controls keep this family easy. Affine/Tseitin and private-leaf methods remain legitimate alternatives outside this fast path. Supplied local witnesses are not a global decision witness. No online or streaming restriction has been silently imposed.

Recovery included the complete current continuation, transport/prepayment definitions, AGENTS/CODEX/research instructions, applicable T5 definitions and cap conventions, all six handoffs, the previous Bounds information ceiling and Redteam canonical-admission report, current Construction and Discovery reports with original Discovery code/raw, Accounting overlap and Synthesis reachable-splice context, and issue 324 through comment 7074432419. Recovery head was 60d2c55720b028466a7ef3095d3425a14e5851f2. No full checkout was present, so repository preflight/LaTeX build was not run. No root manuscript was edited. Searches of charged-bounds and charged-redteam branches returned none. Repository searches for parity/cache/permutation and reachable/certificate/sign found earlier scoped controls, including [3]; search for full-product/permutation/checkpoint returned none. No historical novelty for query certificates or composition is claimed.

Fresh literature queries included “Nisan CREW PRAM decision trees 1991 block sensitivity paper pdf”, “Noam Nisan CREW PRAMs and decision trees 1991 pdf original”, and “Ambainis Prusis tight lower bound certificate complexity block sensitivity sensitivity 2014 arxiv”. Nisan's publisher PDF request redirected to the abstract; the author-hosted preliminary PDF initially returned its opening text, but two attempts to inspect later sections timed out. Only its stated CREW/decision-tree scope is used, not an imported theorem. The guessed de Wolf `publ/qc/survey.pdf` was a different quantum-computation paper and was rejected. Ambainis–Prusis arXiv:1402.5078v1, 20 February 2014, §2 Definitions 2–4, was read from the IAS copy [4]. It defines disjoint sensitive blocks and certificates for Boolean query models; no theorem about arbitrary cached SAT configurations follows. Our promise-domain, writable-tape coupling is proved directly. Its sensitivity/certificate tradeoff theorem is not imported.

Fresh GitHub connector query `"certificate complexity" "sensitivity"` was run under anthropics, openai, xai-org, google, google-research and google-deepmind. Five scopes returned no matches. OpenAI returned bibliography files in `openai/math` at commit `4eaee87548250b2682affda7d05d947c05554bae`. The README and `preprints/A-superquadratic-separation-between-sensitivity-and-block-sensitivity-September-25-2026/build/references.bib` were inspected. The README classifies the collection as research artifacts of varying verification status. The bibliography supplied the author-hosted Nisan link and Ambainis–Prusis lead; no manuscript theorem or code was imported or executed. Web fallback queries included the exact anthropics certificate phrase, openai block sensitivity, xai-org SAT, google-research decision-tree complexity and google-deepmind theorem/proof. Results supplied no verified applicable compulsory-checkpoint implementation; unrelated third-party SAT/product-name results were rejected. These bounded searches do not establish absence from those organizations.

Ownership was checked using GitHub's verified domains for [Anthropic](https://github.com/anthropics), [OpenAI](https://github.com/openai), and [Google](https://github.com/google); [xAI's corporate Grok release link](https://x.ai/news/grok-os); [Google Research's resource page](https://research.google/resources/), linking its GitHub organization; and [DeepMind's publication](https://deepmind.google/research/publications/122591/), explicitly linking google-deepmind/trecvit. No inference of official ownership was made from a product name alone.

## One next dependency and receiving handoff

**OPEN: DYNAMIC-POST-EXHAUSTION-VIEW1**, owner Construction with Bounds, Accounting and Redteam review. Exhibit, for each fixed correct solver, a reachable intermediate domain with opposite-label alternatives preserving all paid summaries outside specified supports, or replace that premise with another proved actual-decoder mechanism. Its existence must be established independently of the desired lower bound. Discovery should retain its correctly scoped k-read corollary and the stronger sign-cache audit. Accounting should use only actual event supports and measured overlap, not re-charge the deleted G_i blocks. Synthesis should record that a full composed map is a legal bypass even before an answer-only cache is formed. This supplies a concrete falsification target and a corrected restricted statement, not an unconditional separation. P versus NP remains OPEN.

## References

1. [Discovery, DYNAMIC-PAIR-PRODUCT-FIBER1, revision 60d2c557](https://github.com/j15marti/pnp/blob/60d2c55720b028466a7ef3095d3425a14e5851f2/research/agents/charged-discovery/PNP_Charged_discovery_2026-11-21_205117_Pair_Product_Prefix_Queries.md).
2. [Construction, DYNAMIC-TABLE-COMPOSITION1, revision 400ea6f3](https://github.com/j15marti/pnp/blob/400ea6f3890fa613d51bf5f4f7b7e80d7f615e75/research/agents/charged-construction/PNP_Charged_construction_2026-11-21_203000_Table_Composition_Control.md).
3. [TMR2-QUERY17 predecessor, recovered at 60d2c557](https://github.com/j15marti/pnp/blob/60d2c55720b028466a7ef3095d3425a14e5851f2/research/agents/tmr-2/2026-11-14_0326_TMR2_SIGN_BLOCK_CERTIFICATE017.md). Different read-only-source model; credited as prior methodology, not silently transferred.
4. [Ambainis and Prusis, arXiv:1402.5078v1, primary PDF](https://www.ias.edu/sites/default/files/math/csdm/13-14/AmbainisPr2014.pdf), §2. [Nisan, STOC 1989 preliminary paper](https://www.cs.huji.ac.il/~noam/crew.pdf), access limitations above; [1991 journal record](https://doi.org/10.1137/0220062).

Publication preflight observed new main head e750281617af95a5b760756a535d1ceea060f91b, whose sole change was an unrelated literature log. Its claims are not premises of this audit. The current Redteam handoff was re-read and remained byte-identical to the recovered body. Publication preserves that intervening commit and all unrelated files.
