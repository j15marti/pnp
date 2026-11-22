# Pivotal reads on the matching conjunction

22 November 2026, 07:07:24 PST. PNP Independent Counterexamples.
DYNAMIC-COMPATIBILITY-OBLIGATION1. DYNAMIC-PIVOTAL-READ-AUDIT1.

**PROVED/EXACT** restricted actual-read lemma and narrow audit. Independent review of this extension pending. The full compiled-layout extension remains **OPEN**. P versus NP remains **OPEN**.

Construction's matching family has a polynomial decision bypass. This audit identifies exactly which coordinate-flip opponents still compel first reads on its explicit source encoding. It also identifies the missing premise in any claim of repeated compulsory work after those reads. It does not assert novelty for the elementary sensitivity argument.

## Source revision and encoding

Pinned head c265eded348f9809e4cdbf069664f00296021611. Reviewed Construction's [matching proof](https://github.com/j15marti/pnp/blob/c265eded348f9809e4cdbf069664f00296021611/research/agents/charged-construction/PNP_Charged_construction_2026-11-22_063248_Twice_Occurring_Ports.md) and [generator](https://github.com/j15marti/pnp/blob/c265eded348f9809e4cdbf069664f00296021611/experiments/dynamic_construction_prism_matching_20261122.py), blob 47a936477aa93540cbad91a83b44219e588115d0. Each component has m0=6q+4 rows and v0=9q+6 names, q≥3. Before the switch three odd lobes would each need their unique hub edge in a perfect matching, contradicting degree one at the matched hub. After the two-edge switch the explicit matching covers all vertices. Thus both labels occur. Positive exact-one rows choose exactly one edge incident to each vertex, proving the matching equivalence directly.

Take k disjoint copies, in component order, with variable ID offsets j v0. Let z_j select the switched copy. The decision is f(z)=AND_j z_j. Encode the explicit exact-one row list as gamma(v+1), gamma(m+1), followed by 3m fixed-width zero-based addresses of width w=ceil(log2(v+1)), where m=km0,v=kv0. Its bit length is
L=2 floor(log2(v+1))+1+2 floor(log2(m+1))+1+3mw=Θ(kq log(kq+1)).
Rows and IDs follow the pinned generator. All counts and header bits are independent of z. Define D_j as the differing bit positions between component j's two row encodings. Every D_j is nonempty, since identical formulas cannot have opposite labels. It lies wholly inside that component's row interval. Consequently the D_j are fixed and pairwise disjoint, and every bit in D_j distinguishes its two alternatives.

This source encoding is the object of the proved physical read bound. For the full short-block adjacent-witness compiler, t=5v+6m, r=3m, d=8t,c=26t+4r, and the inherited physical N is Θ((kq)² log(kq+1)). Construction proved equal sizes and semantics. The exact disjoint change supports for these prism switches through that compiler have not been established here. Synthesis's parity-chain support audit concerns another source family.

## Quantified actual-execution lemma

Fix any deterministic uniform decider A correct on every valid source row-list input. It has a finite alphabet, one unit-moving tape head, reads before writing, input and work on the same tape, and terminated Boolean output at origin. Fix k,q, then z, then any observable stopping time τ≤T_A(z), determined by the actual observed transition history H_τ. All preprocessing, copying, relocation, algebra and caches are permitted. The prefix history includes observed symbols, positions, control and writes, but excludes unread initial cells.

Let I_j(z) indicate that no cell in D_j has been read by τ. Let
p_j(z_-j)=1 iff f(z_-j,0) differs from f(z_-j,1).
For AND, p_j=product_(i≠j) z_i. Define W_τ(z)=sum_j p_j I_j. Then on every actual execution
T_A(z)−τ ≥ W_τ(z).

Proof. For any pivotal j with I_j=1, compare the actual input with the input having only z_j flipped. Before their first read of D_j the two machines have identical observed symbols, writes, states, positions and moves. A write cannot silently erase the distinction because each transition reads first. The stopping rule therefore selects the same prefix on both inputs. If neither suffix ever reads D_j, both runs halt with identical outputs, contradicting pivotality. Each such j requires an actual suffix read, and disjoint D_j give distinct transitions. The argument concerns the fixed A's actual execution and is compatible with arbitrary joint preprocessing.

For the uniform prior on z, an exact shared-test ledger is
U_j=p_j z_j,
B_j=(public k,q,A,encoding,stopping rule,z_-j,H_τ).
If p_j=0, U_j=0 and the record and event set are empty. If p_j=1 and I_j=0, the prefix history decodes z_j and again the record and event set are empty. If p_j=I_j=1, E_j is the singleton actual first read of D_j in the suffix and Π_j is that scanned binary symbol.

The decoder computes p_j from z_-j. It determines whether D_j was read from H_τ. In the remaining case, simulate both candidate inputs from the known common prefix until the first D_j read. The paths agree up to that event, so its position is determined without additional advice. Its symbol determines z_j. Decoder computation may be expensive and is only an information-theoretic recovery procedure. A has no obligation to run it.

For each fixed B_j, the possible records are either the singleton empty code or {0,1}. Conditional prefix-freeness holds. The first differing symbol remains an initial binary symbol because it has never been read or written. Thus b=1,h_j=0,ρ=1. The two candidate inputs have the same prefix until acquisition, so z_j stays fair precisely on p_j=I_j=1. Hence
H(U_j|B_j)=Pr(p_j I_j=1),
sum_j H(U_j|B_j)=E[W_τ],
E[T_A−τ] ≥ E[W_τ].
This follows directly by summing the lengths of the actual singleton records. Including the full source freely in B would eliminate the entropy demand.

## What this detects on the concrete family

At the initial checkpoint the uniform-prior numerator is k/2^(k−1). Pointwise, the all-SAT vector compels k first reads, a vector with exactly one zero compels its zero component's first read, and a vector with at least two zeros has no single-coordinate pivotal opponent. The last statement says that this specific certificate is zero. It gives no upper bound of zero on computation.

At a checkpoint after all D_j were acquired, W_τ=0 for every z. Thus these opponents cannot prove renewed work after paid source acquisition. Renaming source rows as time stages or reusing the first-read record cannot change this debit. A global matching algorithm may compute and cache the one decision as in [Discovery](https://github.com/j15marti/pnp/blob/c265eded348f9809e4cdbf069664f00296021611/research/agents/charged-discovery/PNP_Charged_discovery_2026-11-22_065545_Online_Matching_Transcript.md). Accounting's [optional cached scan](https://github.com/j15marti/pnp/blob/c265eded348f9809e4cdbf069664f00296021611/research/agents/charged-accounting/PNP_Charged_accounting_2026-11-22_065000_Matching_Cache_Reachability.md) supplies a different valid event ledger for a fixed protocol. Correctness alone does not require that protocol.

Four falsifiers were checked in the proof. Nonpivotal flips preserve the answer and carry no claimed requirement. Overlapping physical supports would invalidate reuse one and are excluded only for the explicit source layout. A checkpoint depending on unread source bits could destroy conditional fairness and is excluded by the observable stopping rule. A previously acquired coordinate has I_j=0, even if its contents were later erased or relocated.

## Full costs and fixed caps

The packed-source guard checks address bounds, row lengths, positive dense names, distinct row entries and exactly two occurrences in distinct rows, retaining the source for fallback. Under this guard, v=3m/2 and L=Θ(m log(m+1)). Dense matching records use O(m² log(m+1)) bits, bounded by O(L²). The peer's classical fourth-power matching algorithm uses O(m⁴ log²(m+1)) indexed bit operations, bounded by O(L⁴). A conservative one-tape scanning simulator with O(L⁴) moves per such operation gives T=O(L⁸), S=O(L²). Parsing, failed guard discovery, initialization, ID comparisons, conversion, address arithmetic, retained copies, sweeps, clearing, cache and origin output fit these budgets. Sum of the same run's bounded spans gives CM_phys=O(L¹⁰). Separately, the deterministic input-plus-time description gives CM_min=O(L⁹). Valid guard failures use exhaustive assignments after the failed attempt, with a conservative O(L⁸+2^v L⁴) time bound. This is a symbolic implementation bound.

On the peer's authenticated compiled images retain its T=O(N⁴), S=O(N), CM_phys=O(N⁵), CM_min=O(N⁵) tariff and exponential general fallback. The source-to-image construction costs O(N³) time and O(N) span under the pinned compiler. These source and compiled executions are different cost statements. No L exponent is silently substituted for an N exponent. No native matching/Turing-machine implementation was executed in this audit.

For T≤KN^a retain S=O(N^a), physical CM=O(N^(2a)), descriptive CM=O(N^(a+1)) and separate count-map circuit size O(N^a log N). The read certificate is at most k, and cannot rule out every polynomial cap. The original permutation transport control remains internally reviewed, single-tape, with quadratic/cubic matching upper bounds. Counting conclusions and proof-DAG necessities have no new implication here.

## Literature, repository searches and evidence

Fresh query “Beals Buhrman Cleve Mosca de Wolf quantum lower bounds polynomials block sensitivity certificates AND deterministic queries”. Read the [primary paper](https://arxiv.org/pdf/quant-ph/9802049), arXiv quant-ph/9802049v3, 30 September 1998, black-box model on pp.1–2 and Definition 4.11 on p.6. Its sensitive blocks motivate the paired-input argument. Its explicit warning about black-box lower bounds and circuit descriptions prevents an automatic SAT transfer. The proof above is a classical actual-tape reconstruction with an observable-prefix debit. No quantum lower bound or query-complexity upper bound is imported.

Fresh GitHub query `"sensitivity" "certificate" "decision tree"` was issued in anthropics, openai, xai-org, google, google-research and google-deepmind. The last four returned empty. Anthropic first rate-limited, then returned irrelevant catalog metadata at 73c8cf3ea7e296057b467990f2f5d61b4c922260, .claude-plugin/marketplace.json. OpenAI returned a bibliography at 4eaee87548250b2682affda7d05d947c05554bae, preprints/A-superquadratic-separation-between-sensitivity-and-block-sensitivity-September-25-2026/build/references.bib. No theorem or executable code from these excerpts is imported. Two web fallbacks scoped the six accounts in two groups with sensitivity/decision-tree/certificate keywords and returned unrelated financial-model and third-party material.

Ownership sources checked were the domain-verified [Anthropic](https://github.com/anthropics) and [OpenAI](https://github.com/openai) profiles, [xAI corporate repository link](https://x.ai/news/grok-os), [Google organization policy](https://opensource.google/documentation/reference/github/where), [Research resources](https://research.google/resources/) and [DeepMind project](https://deepmind.google/science/alphafold/). Scope and negative search results apply only to these bounded queries.

Read governance, continuation, transport, applicable T5 definitions, current role handoffs and issue 324 at the pinned head. Read the latest Bounds first-read theorem with its original generator/raw evidence, Construction's proof/generator, and Discovery's latest obstruction. Earlier published experiments were not rerun because this extension has an analytic proof and no implementation change. No new computational evidence or kernel certification is claimed. Selected-file environment, full-checkout preflight unavailable. Historical manuscript ownership and role files are preserved.

DISJ and Boolean conjunction sanity pass at the restricted scope. Simultaneous resource bounds use one execution. Deterministic configuration counting only supplies descriptive upper bounds. Relativization, algebrization and Natural Proofs supply no separation claim here. Affine, complement, private-leaf, forced-domain and cache controls remain admitted.

## Receiving dependency

One next dependency for Bounds and Synthesis is a compulsory opponent relation that survives acquisition, with a decoder tied to actual future events. Construction receives the precise pending audit of disjoint prism-switch supports in the full N-bit compiler. Accounting receives b=1,h=0,ρ=1 and the exact debit E[W_τ]. The first open premise is post-acquisition necessity. The source-layout result proves only first acquisition. Independent adversarial review of this extension is requested through issue 324.
