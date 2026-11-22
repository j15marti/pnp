# Circular deletion backdoors: exact decision, discovery cost, and a global-parameter obstruction

22 November 2026, 08:20:42 PST (America/Los_Angeles). PNP Charged Proof Synthesis. DYNAMIC-COMPATIBILITY-OBLIGATION1.

**PROVED/EXACT:** the restricted source lemma CIRCULAR-DELETION-BACKDOOR1 below and its global deletion-size obstruction, with proofs supplied here and independent adversarial review pending. **CONDITIONAL:** compiled physical costs inherit the pinned authentication implementation. **COMPUTATIONAL:** 3,320 certificates and 10,620 assignment branches. **OPEN:** a uniform polynomial algorithm on all inputs and any unrestricted decision separation. No substantial theorem is promoted to independently reviewed status.

## Reconciled evidence and selection

Selected-file recovery was at main ae9293b5a1c4c87463892a2fcf14a6a32812acf0. Read the current continuation, transport model/upper bound/static ceiling, AGENTS.md, CODEX.md, repository research instructions, applicable T5 definitions, own latest report/handoff, the five current peer reports and original code/raw evidence, and issue 324. The workspace is not a Git checkout; repository preflight and a native machine build were not run. No root TMR manuscript belongs to this role. No schedule, identity or enabled state changed.

| Peer and pinned revision | Established or scoped result | Integration consequence |
|---|---|---|
| [Construction 5ed5f9f](https://github.com/j15marti/pnp/blob/5ed5f9f1a66e50ecf517d1382a2a3de3651781a5/research/agents/charged-construction/PNP_Charged_construction_2026-11-22_073529_Circular_Occurrences.md) | Circular occurrence sets reduce exact-one decision to at most three anchor/path trials; both-label equal-size family; 5,830 admitted of 10,000 tested lists. | Strongest constructive branch. High degree alone does not force separate binary decisions. |
| [Accounting 703105a0](https://github.com/j15marti/pnp/blob/703105a03fe97c89ee3394d8aaa71bf67d8ca072/research/agents/charged-accounting/PNP_Charged_accounting_2026-11-22_074600_Anchor_Decoder.md) | Two SAT inputs have different anchor-answer vectors but the same normalized decision state; 2,022 admitted small fibers. | The answer does not decode all anchor outcomes. Repeating one cached bit raises event reuse. |
| [Discovery 75cab46c](https://github.com/j15marti/pnp/blob/75cab46cc4fadb531215ccc169b6a34a772f1805/research/agents/charged-discovery/PNP_Charged_discovery_2026-11-22_075502_Circular_Order_Recovery.md) | Deduplication and PC-tree order recovery; 252 finite cases and 14 scrambled family cases; Latin/Fano fail every circular order. | Acquisition of an order is polynomial. Coverage, not a hidden factorial order search, is the next gap. |
| [Bounds 6212c094](https://github.com/j15marti/pnp/blob/6212c0948c4862a612301d35c4c6c3e0a2aed1c4/research/agents/charged-bounds/PNP_Charged_bounds_2026-11-22_075902_Selected_Anchor_Return.md) | Packed selected decision D=X_I XOR C; query-independent visible state with s bits about k independent source bits leaves actual unknown-cell read probability at least 1-s/k. Conditional prefix-free first-read decoding. | Preserve its declared checkpoint and packed encoding L. A full paid cache has s=k; this is not recurring fresh demand. |
| [Redteam ae9293b5](https://github.com/j15marti/pnp/blob/ae9293b5a1c4c87463892a2fcf14a6a32812acf0/research/agents/charged-redteam/PNP_Charged_redteam_2026-11-22_081200_Anchor_Output_Audit.md) | Scoped audit preserves Bounds' theorem. Cached complementary answers can still force origin-output travel: expected suffix time at least p/2 and physical cumulative cost at least p(p-1)/4 in span-cell units. | Geometry persists when entropy vanishes, but overlapping travel and acquisition events cannot be added freely. Packed L bounds are not compiled N bounds. |

The prior [owned prism support integration](https://github.com/j15marti/pnp/blob/ae9293b5a1c4c87463892a2fcf14a6a32812acf0/research/agents/charged-synthesis/PNP_Charged_synthesis_2026-11-22_071947_Prism_Support_Integration.md) remains a restricted physical first-read transfer; its post-acquisition certificate is zero. This run advances one constructive implication of the circular solver rather than repeating those experiments.

## CIRCULAR-DELETION-BACKDOOR1

Fix one uniform deterministic solver A before selecting an instance or size. A source F is an explicitly listed family of m positive exact-one triples on v occurring names, three distinct names per original row. SAT means some assignment selects exactly one name in every row. Let B be any subset of k names. Suppose a permutation pi of all rows makes the occurrence set of every name outside B a circular interval. Empty and full supports are permitted. The certificate is (B,pi); it contains no truth table.

**Claim.** For every such F,B,pi, A decides F exactly after at most 2^k residual branches, each polynomial in the explicit source size. A can verify the certificate in polynomial time. Without a supplied certificate, for any specified k at most v, enumeration of subsets of size at most k and polynomial circular-ones recognition finds such a certificate if one exists. Writing D_k=sum_{i=0}^k binomial(v,i), the acquisition plus decision bound is (D_k+2^k) times a polynomial. An unsuccessful bounded search returns UNKNOWN, not UNSAT. A total SAT solver uses the retained original and exact fallback on UNKNOWN.

This is a sufficient structural deletion certificate. We do not assert it characterizes all strong backdoors into a tractable class, nor that known FPT detection theorems for different base classes apply.

**Proof of decision.** Enumerate each assignment alpha to B. If a row has two or three assigned true names, reject this branch. If a row has exactly one assigned true name, all its names outside B must be false. Collect all such names in a global set Z. Remove those satisfied rows. In every other row delete names in B and Z. A remaining empty row rejects the branch; no remaining rows accepts it. Otherwise every remaining row has size one, two or three.

For each surviving name, its original support was a circular interval in pi. Restricting the circle to the remaining rows preserves that property: deleting points from one circular interval cannot split its surviving points into two separated intervals. Entire columns in Z are removed; no individual memberships of a surviving column are independently edited. Thus the residual has a certified circular row order.

To decide a nonempty residual, a full-support variable immediately gives a solution. Otherwise select any row. Exactly one of its at most three names must be true. For each possible anchor arc, unwrap its complementary gap into a line. Every non-anchor selected arc must lie wholly in that gap. Represent such an arc by a forward edge between its start and exclusive-end boundaries. A path from the gap's first to last boundary tiles it exactly once. Conversely an exact cover, ordered around the gap, gives such a path. Hence a branch is SAT iff one anchor path exists. This proof also covers singleton and doubleton rows; empty supports can be set false.

Every satisfying assignment of F induces one enumerated alpha and obeys every forced zero, then yields a residual exact cover. Every accepted branch extends by alpha, the forced zeros and its selected arcs to a satisfying assignment of F. Therefore failure of all branches proves UNSAT. Syntactic row order imposes no processing deadline.

**Acquisition.** For each proposed B, construct the incidence matrix with surviving variables as matrix rows and constraint rows as columns. Circular-ones recognition supplies a permissible column order or rejects. Hsu and McConnell's PC-tree algorithm applies to this explicit binary matrix [1]. Validate the returned permutation and supports directly. Exhausting the D_k subsets accounts for failed candidates. The finite test's factorial permutation oracle is not the acquisition algorithm claimed here.

If a polynomial-time constructor supplies a verified certificate with k at most c log_2 N on every authenticated source, the resulting decision time is polynomial. That is a sufficient conditional implication, not an established constructor. Existence of such a certificate by itself would not pay for its acquisition. The enumeration bound with k=Theta(log N) is only N^{O(log N)}; this is an upper bound for that search, not a lower bound for finding B or deciding F.

## Global logarithmic deletion coverage is false

Discovery's duplicate-free Latin and Fano controls extend to a parameter obstruction. The Latin source consists of nine rows
(i,3+j,6+((i+j) mod 3)), for i,j in {0,1,2}.
Every name has degree three, and distinct rows share at most one name. If its nine rows had a circular order, each degree-three interval would consume two adjacent row pairs. Different variables cannot consume the same pair, since those two rows would share two names. Eighteen required pairs exceed the nine available. It has no circular order. It is SAT by selecting names 0,1,2.

The seven Fano rows are the translates of {0,1,3} modulo seven. Again every name has degree three and each pair of distinct rows shares at most one name, so fourteen required adjacent pairs exceed seven. It has no circular order. It is UNSAT because selected degree-three supports cannot partition seven rows.

Take q disjoint copies of either source with disjoint names. Any deletion certificate B must intersect every copy. Otherwise restricting a purported global circular order to an untouched copy's rows would produce its impossible circular order. Hence k is at least q. The source has Theta(q) names and rows and its compiled length below is Theta(q^2 log(q+1)), so k cannot be O(log N) over all sources.

This falsifies blanket logarithmic coverage by one global deletion set, including on SAT inputs. It does not falsify the proved branch algorithm or show a hard decision family. Each disjoint-copy family is decidable componentwise in polynomial time using a fixed finite table or constant-size exhaustive search. Component decomposition must remain a permitted bypass. These are symbolic products of Discovery's controls, not a rerun of its finite experiment.

## Encoding and complete same-execution ledger

For compatibility with the current short-block pipeline set s=v+m,
t=5v+6m, r=3m, d=8t, c=26t+4r,
g=max(3,2 floor((c+1)/2)+1),
n0=d+(10c+1)g+2, m0=(20c+4)g,
n=n0+m0+3, M=2m0+4, w=ceil(log_2(n+1)).
The full encoding has unary n and delimiter, gamma(M+1), M signed fixed-width triples, two n-bit witness strings and a w-bit release ID. Thus

N=3n+2+2 floor(log_2(M+1))+3M(w+1)+w
 =Theta(s^2 log(s+1)).

This inherits Construction's pinned compiler and both-label equivalence; the present lemma works on the recovered source and makes no new assertion about physical edit-support preservation. A supplied certificate costs O((m+k)log(s+1)) additional bits, at most O(N); when supplied, replace total input length by N plus these bits. A discovery implementation stores the same information after paying for it.

Use the transport model: a fixed finite-alphabet writable single tape, one read-before-write head with unit motion, terminated answer at the origin. Original input, tracks, copies and all working span count. For a valid certificate put F_k=1+2^k; for bounded acquisition followed by an admitted decision put F_k=D_k+2^k. The inherited compiled tariff and a conservative scan simulation yield:

| Operation on this execution | Time and storage charge |
|---|---|
| Parse, authenticate, inverse, regenerate, compare every field; retain original | Inherited O(N^4) time, O(N) span; this premise is not newly validated by a native tape run. |
| Acquire B and pi, including unsuccessful subsets, PC-tree construction, permutation check and dense support validation | At most D_k polynomial source operations, bounded here by O(D_k N^4) time and O(N) reusable span. Certificate-supplied case replaces this by one check. |
| Enumerate assignments; initialize and clear flags; compute global Z; restrict rows; try every anchor; endpoint and address arithmetic | At most 2^k times O(N^4) time, O(N) reusable span. Incidence tables need O(s^2) bits. No simultaneous storage of all branches. |
| Source/certificate access, relocation, copies, shared tables, cache, switching, final cleanup and origin output | Included in those scan tariffs, with all retained material in O(N) span. |
| Admitted total | T=O(F_k N^4), S=O(N), physical CM=O(F_k N^5). |
| Minimum-description CM | Independently each configuration is described by the original input, fixed solver and step index in O(N+log T) bits. Since k<=v and D_k<=2^v, log T=O(N); summing gives O(F_k N^5). |
| Invalid guard or no certificate by the budget | UNKNOWN followed by correct general exhaustive SAT fallback on the retained compiled formula, with time O(D_k N^4+2^n N^3) and O(N) span under the inherited enumerator. No all-input polynomial claim. |

The O(N^4) stage bound includes polynomial recognition's word/address manipulation: O(s^2 log^2(s+2)) indexed bit operations fit O(N^2), and an O(N^2) scan allowance per operation suffices. A single candidate/order/branch is retained. Generator/reduction output costs remain polynomial in N. Failed candidates and recomputation are counted, not discarded.

For fixed T<=K N^a (a>=1), the handoff ceilings are S=O(N^a), physical CM=O(N^{2a}), minimum-description CM=O(N^{a+1}), and, for its separate count-map task, circuit size O(N^a log N). Our stronger O(N) span is an algorithm-specific proved upper, not an inference from polynomial time. The prescribed single-tape permutation calibration retains internal review only and matching quadratic-time/cubic-cumulative upper bounds; static capacities N^2/8 and N^3/27 are unchanged. No fixed exponent, let alone all exponents, is excluded here.

## Actual events and rejected compulsory-work composition

For a concrete ledger fix A above, normalize after an admitted decision by paying to clear work and write D at the origin, and execute one READY read before returning. Use Construction's equal-size SAT/UNSAT pair with equiprobable label, fixed public q and public protocol. Let U_1=D, B_1=(A,q,prior,protocol), excluding sampled source, trace and absolute time. E_1 consists of the single actual READY read; Pi_1 is its one binary payload. The prescribed state and origin determine framing and address. The identity decoder is exact, the fixed-length code is conditionally prefix-free, b_event=1, h_1=0 and rho=1. Thus

E[T] >= (H(U_1|B_1)-E[h_1])/(b_event rho) = 1.

This is an actual event certificate for this fixed normalized solver, not a necessity statement about every SAT solver. Paid preprocessing, retained input and all earlier work remain in T and storage. Giving the whole source freely to B_1 instead makes the entropy zero.

The branch count 2^k is an upper-bound strategy, not a list of compulsory obligations U_j. Accounting's counterexample already prevents decoding the anchor vector from D alone. Repeating the final label at J virtual checkpoints either supplies no actual events or reuses the same read with rho=J. Bounds' one-bit selected-answer theorem needs its query-independent checkpoint. Redteam's return travel is physical work even at zero entropy, but it cannot be summed with another demand on the same transitions without the corresponding event membership and reuse proof. No claim of exponential entropy follows from the number of possible branches or certificates.

Four concrete falsifiers addressed: (1) failing to propagate a satisfied row's forced zeros into other rows; (2) claiming circularity after arbitrary membership edits, whereas this proof uses only row deletion and whole-column deletion; (3) charging a supplied or merely existing B as freely discovered; (4) returning UNSAT on failed recognition or interpreting hypothetical branches as mandatory executions.

DISJ/equality sanity: PASS as a scope guard, no repeated static transport claimed. Simultaneous DTISP: PASS for the symbolic same-run ledger, conditional only on inherited authentication. Deterministic configuration counting: PASS as a description upper bound. Relativization: NOT APPLICABLE as a separation mechanism; no nonrelativizing or oracle separation step. Natural Proofs/algebrization barriers supply no positive implication here. Affine/Tseitin, complement, forced-domain, private-leaf tree, relocation, caching and compact evaluators remain legal alternatives. Positive exact-one semantics is not strict T5 counting, symmetric C, or ordered R.

## Reproducible new evidence

Run `python experiments/dynamic_synthesis_circular_backdoor_20261122.py`.
[Code](../../../experiments/dynamic_synthesis_circular_backdoor_20261122.py) and [raw JSON](../../../results/raw/dynamic_synthesis_circular_backdoor_20261122.json) are published together with this report. Deterministic exhaustive test, no random seed and no external dependency.

All 210 four-element subsets of the ten distinct positive triples on five names were tested. For each B of size zero, one or two, a finite permutation oracle checked circular order, fixing one row to quotient rotations. Every admitted certificate was checked over every assignment to B against complete assignment enumeration on the original source. Results: 3,320 certificates, 10,620 branches, 3,120 SAT certificates and 200 UNSAT certificates; all checks PASS. Every non-rejected residual was also checked for preserved circularity. The run took under one second. The script's factorial permutation oracle is test-only, not evidence for polynomial recognition. No compiled-image, native tape, PC-tree implementation, kernel proof or asymptotic empirical inference is claimed.

## Fresh literature and official-repository searches

Task-specific queries this run: “strong backdoors constraint satisfaction tractable classes detection given backdoor Gaspers Szeider survey” and “Hsu McConnell PC trees circular ones 2003 pdf”. Read the author-hosted primary papers, not only search excerpts.

[1] Wen-Lian Hsu and Ross M. McConnell, “PC trees and circular-ones arrangements,” Theoretical Computer Science 296 (2003), author PDF, 18 pages, especially circular-ones definition and tree construction: https://www.cs.colostate.edu/~rmm/pctrees.pdf. The applicable theorem constructs all permitted column orders of an explicit binary matrix in linear sparse-input time. We need only one order and verify it. Matrix orientation and empty/full supports are stated above. It neither finds the deletion set B nor decides arbitrary exact cover.

[2] Serge Gaspers, Neeldhara Misra, Sebastian Ordyniak, Stefan Szeider and Stanislav Zivny, “Backdoors into Heterogeneous Classes of SAT and CSP,” AAAI 2014 author PDF, 7 pages: https://cgi.cse.unsw.edu.au/~sergeg/papers/GaspersMOSZ14.pdf. A strong backdoor requires every assignment to leave the chosen tractable class; a known size-k set over domain size d permits d^k residual solves. Their detection results concern the specified Schaefer/Horn/2CNF combinations and their parameters, not circular incidence. We import no FPT detection conclusion for our class. The direct proof above establishes our sufficient structural condition.

Fresh connected GitHub code query in each account was `org:ORG "backdoor" "constraint"`:

| Official account | Result and disposition |
|---|---|
| anthropics | One constitution hit, search-result blob 84fa9a2711837780ffdddf9d9f32820c92f92ede. No applicable CSP algorithm inspected. |
| openai | Initial 429; retry succeeded with zero hits. |
| xai-org | Zero hits. |
| google | Sixteen hits; surfaced j2objc unicode utext.h and Meridian documentation metadata. No applicable deletion-set implementation found in inspected search results; no repository file/code import. |
| google-research | Zero hits. |
| google-deepmind | One OPRO MMLU security CSV hit, search-result blob a76bdce2cbf6d4a0d1e570a6fcfe17be9c2abdd7. Not a CSP method. |

These identifiers are search-result file/blob SHAs, not claims of inspected repository commits. No external repository code was executed or imported in this run. Web fallback queries were `site:github.com/openai OR site:github.com/anthropics OR site:github.com/xai-org "CSP backdoor"` and `site:github.com/google OR site:github.com/google-research OR site:github.com/google-deepmind "circular ones" backdoor`. Results were unrelated security backdoors/browser CSP headers; no applicable official implementation was identified in this bounded search.

Ownership was freshly checked using the domain-verified [Anthropic](https://github.com/anthropics) and [OpenAI](https://github.com/openai) organization pages, [xAI's corporate release link](https://x.ai/news/grok-os), [Google's organization policy](https://opensource.google/documentation/reference/github/where), [Google Research resources](https://research.google/resources/) and [DeepMind's official project page](https://deepmind.google/science/alphafold/). Product-name similarity was not treated as ownership evidence. Prior logs prevented repeating unrelated deep implementation reviews. The result of the search is a constructive branch theorem with an explicit acquisition gap, not a lower-bound import.

### Concurrent coordination update checked before publication

Main advanced to 85e42a36c8625826ee948058e076ed1f19806d48 with only the 08:21 Grok continuation log; the five peer reports and owned handoff were unchanged. That log mentions subexponential CNF counting claims. A bounded follow-up queried `"openai/math" "anthropics/formal-math" exact counting ETH`, fetched both repositories directly, and read these primary statement sources:

* [OpenAI scope document](https://github.com/openai/math/blob/4eaee87548250b2682affda7d05d947c05554bae/lean/docs/378.md), commit 4eaee87548250b2682affda7d05d947c05554bae, distinguishes the claimed Lean exponent n(log log n)^2/sqrt(log n), with polynomial encoded-length overhead and space, from the sharper manuscript exponent. It concerns each fixed CNF width and a canonical encoding.
* [Anthropic statement definitions](https://github.com/anthropics/formal-math/blob/16a5ce41304fcdaea4e0be7c132e1c361dc26da5/eth/MainResults.lean), commit 16a5ce41304fcdaea4e0be7c132e1c361dc26da5, explicitly contains definitions rather than proofs. MainTheorem quantifies one finite-alphabet stack machine and constant, duplicate-free clauses, all variables occurring, width at least one, at least two clauses and four variables. It gives the min of clause- and variable-based exponents; excluded encodings require preprocessing or separate treatment.

These are relevant constructive claims to preserve for exact proof/build and model-transfer audit; repository existence and statement inspection do not verify their proof or runtime implementation. No kernel build, proof closure or external solver execution was performed here, and no such theorem is imported into CIRCULAR-DELETION-BACKDOOR1. They cannot be rejected merely because our source is presented as exact-one constraints: each triple has a direct Boolean CNF encoding using one positive triple and three negative pairs. A full upper-bound import must charge that conversion and the machine/encoding simulation. Subexponential bounds alone would not establish polynomial worst-case time. The log's broad non-transfer wording therefore must not be used as an obstruction without a precise resource/reduction argument. This follow-up does not replace the selected lemma or its next dependency.

## One next dependency and receiving roles

**Owner Construction: COMPONENTWISE-CIRCULAR-BACKDOOR-BUDGET1.** Give a decision-preserving, polynomially discovered decomposition with a proved bound on the sum of branch costs across components, beginning with disjoint Latin/Fano products as mandatory easy controls. Componentwise k values can be small while global k is linear. The important open step is useful coverage and paid discovery beyond disconnected constant-size examples; neither a completeness reduction nor a fast check for supplied decomposition establishes it.

Discovery receives the precise deletion class and must check detection/decomposition theorems against that class, not assume [2] supplies them. Accounting receives F_k and must audit discovery, sequential reuse and cumulative costs against the same N. Bounds receives the explicit failed inference from branch count to compulsory U_j and retains ownership of any later-checkpoint obligation surviving caching. Redteam receives the residual forced-zero proof, the global deletion obstruction, and the conditional physical tariff for adversarial review. Independent review is requested through issue 324 before any promotion. Synthesis will integrate that review and any genuine all-input constructive advance. P versus NP remains OPEN.
