# Accounting for shared prefix information in the connected exact-one family

22 November 2026, 08:44 PST. PNP Charged Accounting. DYNAMIC-COMPATIBILITY-OBLIGATION1. Named lemma ARTICULATION-PREFIX-LEDGER1.

**PROVED/EXACT** restricted actual-scan decoder, bounded reuse comparison and normalized-suffix counterexample. **CONDITIONAL** polynomial compiled tariff inherits authentication. **COMPUTATIONAL** finite entropy and event-membership audit. Independent adversarial review pending. P versus NP remains OPEN.

## Fixed machine, inputs and claim

Pin Construction at [dec4350c30459630faa060ddf3ddfba91c66507d](https://github.com/j15marti/pnp/blob/dec4350c30459630faa060ddf3ddfba91c66507d/research/agents/charged-construction/PNP_Charged_construction_2026-11-22_083034_Articulation_Compatibility.md), including its generator, raw evidence and issue 324 comment 7082160553. A source has q Latin blocks, q switch bits Z, true endpoint gadgets, v=8q+7 variables and m=9q+6 positive exact-one triples. Identity blocks preserve a port bit and switched blocks implement R={00,01,10}. R squared is full. The decision D is SAT iff sum Z differs from one. This preserves both labels. Prior Construction tests are retained without rerunning them.

Fix one deterministic finite-alphabet single-tape solver A before q or the input. It validates the complete compiled formula using the published inverse/regeneration guard. On recovered canonical sources it tests membership in the generator family, parses q from the counts, checks each of the two local block templates with canonical names and checks both endpoint gadgets. This takes polynomial work with exact comparisons. Each block has seven private names under either template, so two alternatives can be checked independently without a 2^q search. Outside this family A may use the earlier guarded decomposition and otherwise exhaustive SAT on the original.

For the canonical family, A writes the recovered Z in a fixed q-cell area, with q and its location determined by the common encoding length. It then erases the original input, parsing buffers and authentication state, keeping only Z and public q, length and layout metadata. This normalization is paid and may follow polynomial work. A scans Z in order, maintains count min(2,sum Z), and optionally retains its prior states in a q-cell history area. All cells outside these areas have prescribed values. At completion A writes D at the origin, clears Z and history and returns to READY at the origin. The declared model has no free clock. Initialization, erasure, return travel and all retained span are charged.

For every q>=1 take a uniform J in {0,1,...,q}. Let Z=0^q for J=0, and let Z have its sole one at position J otherwise. This distribution includes SAT and UNSAT. Define U_j to be the scanned prefix state after bit j, encoded as 0 before the switch and 1 after it on this prior. It is precisely the left-to-right port domain, respectively {1} or {0}, ignoring the right endpoint until termination. The complete vector U determines J, so H(U)=log2(q+1).

The claim is an exact decoder ledger for this fixed machine's real scan, together with a counterexample to making the entire prefix vector a compulsory post-cache obligation of every decision solver. The decoder does not require arbitrary SAT machines to execute these scan states.

## Decoder, addresses, framing and reuse

At checkpoint j immediately before the designated SCAN transition, put the unread Z cells j through q in the hidden region. B_j contains public A,q,layout,prior and the complete current configuration outside that region, including the known earlier Z cells, retained history, state and head location. The preparation above ensures that outside information is exactly a deterministic function of public metadata and prior prefix bits, and conversely the retained history determines those bits on this prior. No sampled source or answer is retained outside that region. Head position and address are public functions of q and j at the SCAN checkpoints. Elapsed time is unavailable to the machine and excluded from B_j.

E_j contains the one actual transition reading Z_j in state SCAN, at its prescribed cell. Pi_j is that binary payload, even if it is conditionally deterministic. Decoder computes U_j from the last prefix state and Pi_j. The alphabet at a SCAN cell has two legal values. Codewords have length one for every fixed B_j, so they are conditionally prefix-free. Capacity b=1, framing h_j=0, and rho=1 because the designated transitions are distinct. Public event identity and length avoid a missing address or termination code. Physical counter manipulation, history storage, crossing moves and framing initialization still cost transitions.

For a direct entropy calculation, if no earlier one occurred, the remaining possible J values number q-j+2. The chance that the new bit is one is 1/(q-j+2). Otherwise the new U_j is already determined. Hence

H(U_j | B_j) = ((q-j+2)/(q+1)) h2(1/(q-j+2)).

Summing j=1 through q telescopes by the entropy chain rule to log2(q+1). Therefore the actual-event theorem gives

E[T] >= sum_j H(U_j|B_j)/(b rho) = log2(q+1).

The scanner in fact executes q designated reads. The entropy bound is consistent with that exact event count. Its scope is this specified scan and observation interface. Earlier preparation has already paid to discover and copy Z. The bound supplies no second compulsory acquisition theorem for arbitrary solvers.

For comparison take only public q and protocol as each B'_j. Record the entire actual scan prefix Pi'_j=Z_1...Z_j with E'_j={e_1,...,e_j}. Each record has publicly known length j, h'_j=0 and b=1. Then H(U_j|B'_j)=h2(j/(q+1)), but event e_1 occurs in all q records, so rho=q. The valid inequality is E[T]>=sum_j h2(j/(q+1))/q. Charging this numerator with rho=1 is false accounting for those event sets. Pairing just e_j with public-only side information generally fails decoding because a zero bit does not distinguish a switch already seen from one still ahead. These two ledgers show concretely how causal side information and event reuse must be coordinated.

If B_j includes the complete configuration, including unread Z, all conditional demands vanish. The hidden-region restriction is explicit and follows the declared observer and fixed machine scan. It is not a universal inability of the machine to access retained information. Every stored bit remains charged in the resource ledger.

## What survives after caching

At final READY, all q single-switch inputs have identical full configurations and suffixes. Their message profiles are different. Thus for q>=2 no decoder using only public parameters and the complete normalized suffix can recover U on all these inputs. Under the both-label prior,

H(U|D) = q/(q+1) log2(q),
H(D) = h2(1/(q+1)).

This is an exact failure of the proposed post-cache profile decoder. To avoid an all-UNSAT correctness loophole, A is globally correct by its authenticated fast path and exhaustive fallback, and the prior also contains a SAT input. The indistinguishable UNSAT fiber alone is enough to defeat profile reconstruction. A one-read final-decision ledger with U=D, Pi=D, b=1,h=0,rho=1 is valid. Repeating that same read across virtual subtree obligations raises reuse accordingly.

This strengthens the prior [anchor-fiber accounting](PNP_Charged_accounting_2026-11-22_074600_Anchor_Decoder.md) by giving a growing connected-family profile, its exact causal entropy sum and actual event memberships. It does not infer P=NP from the failed lower-bound decoder.

## Same-execution resource audit

Use Construction's physical encoding. Set t=5v+6m=94q+71, r=3m=27q+18, d=8t, c=26t+4r, g=max(3,2 floor((c+1)/2)+1), n0=d+(10c+1)g+2, m0=(20c+4)g, n=n0+m0+3, M=2m0+4, w=ceil(log2(n+1)). Unary n, gamma(M+1), M signed triples, two n-bit witness strings and the release ID give

N=3n+2+2 floor(log2(M+1))+3M(w+1)+w=Theta(q^2 log(q+1)).

No compressed parameter hides a truth table. The source has O(q log(q+1)) bits. Complete compiler emission has the inherited O(N^3) budget, while physical input inversion/regeneration/authentication has inherited O(N^4) time and O(N) span. These implementation premises are carried explicitly and were not kernel-verified or simulated natively here.

| Stage | Same-execution charge |
|---|---|
| Parsing, metadata, source retention, failed template candidates, exact authentication | O(N^4) time and O(N) span under the published tariff |
| Canonical source guard, discovering Z, two templates per block, copies and address arithmetic | Polynomial scans bounded by O(N^4), O(N) span |
| Clear original and temporary state, initialize fixed Z/history areas and public counters | O(N^2) conservative time, O(N) span including cleared/visited area |
| Actual q reads, history writes, counter changes, relocation between areas | O(q N^2) conservative time, O(N) span, included in O(N^4) |
| Final cache, erasure, output and origin return | O(N^2) conservative time, O(N) span |
| Admitted total | T=O(N^4), S=O(N), CM_phys=O(N^5) |
| Description cost | Independently C_t is reconstructible from original input and t in O(N+log T) bits, yielding CM_min=O(N^5) |
| Failed guard | UNKNOWN and exact fallback, potentially O(N^4+2^n N^3) time with O(N) span |

Erasure does not refund already visited storage or prior cumulative cost. The entropy records are analysis objects. A's history area is physically present and paid, but no exponentially large collection of records is stored. Input authentication and copies occur before the declared scan and are not free side channels into its decoder.

Construction's broader decomposition cost is compatible with a sum over local assignments. If terminal piece sizes are at most 9+floor(log2(s+1)), there are at most m nonempty pieces and at most 512(s+1)m local assignments. Only two feasibility bits per separator are stored. Large circular pieces receive unary domains and need at most two parent-bit tests. This accounting does not establish acquisition or local feasibility for correlated two-variable separators. The implemented Construction checker enumerates every local piece and lacks the production guard for large pieces. Its finite evidence validates the tested small sources, while the symbolic large-piece tariff depends on the specified circular routine.

For a fixed cap T<=K N^a with a>=1, S=O(N^a), physical CM=O(N^(2a)), minimum-description CM=O(N^(a+1)), and the separate count-map circuit ceiling is O(N^a log N). Here log(q+1)=O(log N), far below b rho K N^a. No exponent is excluded. The internally reviewed transport calibration keeps its quadratic-time/cubic-cumulative match and Dh<=N^2/8, Dh^2<=N^3/27 static ceiling.

Four falsifiers are a retained sampled copy outside the hidden region, missing address/length data, reused prefix events falsely assigned rho=1, and a decoder that attempts to recover the profile from the final answer. The normalized scan layout, fixed frame, membership count and q-input collision address them respectively. DISJ and equality sanity PASS as scope checks. Simultaneous DTISP PASS for the conditional same-run upper ledger. Configuration counting PASS as an upper description. No nonrelativizing step or circuit lower bound is proposed. Affine, complement, private-leaf, forced-domain, relocation and shared-cache controls remain legal. The target is Boolean decision with strict T5 counting kept separate.

## Reproduction and fresh sources

[Code](../../../experiments/dynamic_accounting_articulation_20261122.py) and [raw](../../../results/raw/dynamic_accounting_articulation_20261122.json) enumerate the q+1 prior inputs for every q from 1 through 32, totaling 560 inputs. They verify identity decoding, joint-profile injectivity, conditional entropy sums, exact event reuse and normalized decision fibers. At q=32, joint and causal entropy are log2(33)=5.044394119 bits, marginal sum is 23.757241213 bits, rho for nested prefixes is 32, and hidden profile entropy after D is 4.848484848 bits. These finite checks use floating logs only for numerical identities and do not validate physical tape timing. The symbolic entropy proof supplies the asymptotic result. Run Python 3 with standard library only. No random seed.

Fresh query “Shannon 1948 mathematical theory communication conditional entropy chain rule noiseless coding theorem pdf” led to the primary [1948 paper](https://people.math.harvard.edu/~ctm/home/text/others/shannon/entropy/entropy.pdf), especially entropy conditioning and equivocation. Its probability identities justify the displayed chain decomposition. No compulsory SAT execution premise follows from source coding.

Fresh GitHub queries were org:ORG "conditional entropy" "prefix" across anthropics, openai, xai-org, google, google-research and google-deepmind. Results were respectively 0,32,0,1,0,0, with Google Research successfully retried after a transient 429. The Google hit was uncertainty-baselines/baselines/t5/data/metrics.py at search-result blob 04360d2cb7a4c750f6c5a0905804a5b41e88bb9c, a prediction metric rather than a machine event theorem. It was not imported.

One promising official result was read at OpenAI commit 4eaee87548250b2682affda7d05d947c05554bae, [08-prefix.tex](https://github.com/openai/math/blob/4eaee87548250b2682affda7d05d947c05554bae/preprints/Conditional-information-under-deterministic-coordinate-sweeps-September-26-2026/build/sections/08-prefix.tex), blob 67cc581bb6e494ce297208d08ede531a3c547bd2. Its signed-mass contraction assumes fresh independent switches in repeated prescribed coordinate sweeps and an invariant boundary law. Its list-entropy application conditions on paths. Offline SAT correctness supplies neither those random dynamics nor mandatory sweeps. No theorem from that manuscript is imported. The ordinary entropy chain calculation here is proved directly. No external code or proof kernel was executed.

Official ownership was checked using domain-verified [Anthropic](https://github.com/anthropics) and [OpenAI](https://github.com/openai), [xAI's corporate repository link](https://x.ai/news/grok-os), [Google's organization policy](https://opensource.google/documentation/reference/github/where), [Google Research resources](https://research.google/resources/) and [DeepMind's official project](https://deepmind.google/science/alphafold/). Search scope is bounded to this decoder dependency. Zero hits do not establish absence of other relevant work.

State recovery used connected files at dec4350c30459630faa060ddf3ddfba91c66507d, current governance, dynamic continuation, transport model and upper ceiling, T5 resource definitions and bounded-reuse lemma, owned latest report/handoff, peer handoffs, and Construction's original code/raw. No full local checkout, preflight, compiled-image or native tape build was available. No peer file or historical manuscript is changed.

**One next dependency to Bounds and Synthesis.** Prove a later actual observation requirement that holds for every fixed correct solver after its chosen paid preprocessing and caches, with side information and disjoint event sets justified for that execution. This report supplies one fixed scanner's exact ledger and the normalized profile-decoder counterexample. Redteam receives the q>=2 identical-suffix fiber and the hidden-region invariant to attack. Construction receives the supported additive upper costs and the production-guard distinction. Independent review requested.
