# Sublinear testing does not replace exact source verification

23 November 2026, 00:54 PST (America/Los_Angeles). PNP Proof Discovery. **EXACT-TESTING-TRANSFER1**, within DYNAMIC-COMPATIBILITY-OBLIGATION1. **PROVED/EXACT** for the coupling lemma below; **FALSIFIED/RETIRED** for the proposed transfer of fixed-distance testing guarantees to exact decision on every source; **OPEN** for unrestricted post-acquisition computational necessity and P versus NP. Independent adversarial review pending.

## Target and recovered dependency

The strongest current concrete control is the diamond network solved by forest potentials. Accounting's newly completed source audit shows that a tree-only actual prefix on a balanced K_q source can predict every cotree tag under the balanced prior, while each tag remains compulsory for an exact both-label decider. This discovery run asks whether sublinear signed-graph testing supplies a legal faster verification step, or whether its lower-bound mechanisms transfer to the remaining offline task.

The answer is scoped: approximation with a distance promise gives useful partial tests, but supplies neither exact acceptance nor compulsory post-acquisition recomputation. A direct same-execution coupling bound quantifies what any bounded-error all-input verifier must still observe. It applies after paid deterministic preprocessing with an explicitly proved common prefix, and it permits unrestricted computation and caches.

The starting snapshot is Accounting commit 688e198257c63518f02f82d6f8ee347ba3e8a910. Governance, current continuation, transport model and matching upper bound/static ceiling, applicable T5 definitions, all six handoffs, latest Discovery original report and relevant Accounting/Synthesis original evidence were read. The earlier discovery result on persistent versus immutable substitutions remains intact. No online updates are supplied here.

## One primary result and its exact transfer boundary

Adriaens and Apers, *Testing properties of signed graphs*, arXiv:2102.07587v1 (15 February 2021), §§1 and 2.2 [1], gives a one-sided balance tester in the dense signed-adjacency query model. It accepts balanced graphs and rejects epsilon-far graphs with probability at least 2/3; intermediate inputs are unconstrained. Distance is normalized by q² edge modifications, permitting additions, deletions and sign switches.

Theorem 2 advertises a tilde-O(1/epsilon) query bound. The adjacent construction text samples tilde-O(1/epsilon) vertices and queries their entire induced subgraph. This run does not resolve that counting presentation or rely on its precise exponent. The verified promise/error contract is sufficient for the negative transfer. The explicit v1 PDF URL failed; the unversioned PDF was readable and the arXiv version history identifies v1.

A search for Nisan's 1991 *CREW PRAMs and Decision Trees* [2] recovered publisher metadata and abstract, but the PDF request redirected to the access page. Its full theorem hypotheses were unavailable, so no theorem from it is imported. The coupling proof below is provided in full, without a novelty claim.

For any balanced signing z of K_q, flip one cotree edge e. The resulting source is unbalanced and one sign switch restores it. Its distance is 1/q² under [1]'s convention. For any fixed positive epsilon and sufficiently large q, this input lies outside the rejection guarantee. Repetition does not repair a missing guarantee: a tester permitted to accept such a source with probability one remains permitted to do so on every repetition. Setting epsilon<=1/q² removes the advertised size-independent saving; independently, the following lower bound rules out an all-input sublinear verifier in this source-observation model. This is failure of a transfer, not failure of the published property tester.

## Source, machine and quantifiers

Use the explicit complete-graph binary diamond sources in the Accounting audit [3]. For q>=3, k=q(q-1)/2 and r=k-q+1, the star tree T has edges (0,v). Each base edge has private diamond fibers with identity/one fixed transposition tags. The positive Boolean exact-one encoding has

n=33q+111k, m=21q+87k,
w=ceil(log2(n+1)),
N=n+2+2 floor(log2(m+1))+3mw.

Source order is header, tag-independent rows, tree-owned rows, cotree-owned rows, with fixed canonical order inside each group. It is a permutation of whole triples independent of the signing. The SAT predicate is exactly the existence of potentials x satisfying z_uv=x_u XOR x_v. Thus N=Theta(q² log q), r=Theta(N/log N), and each one-cotree-flip neighbor is a legal equal-length opposite-label input. This is Boolean decision on exact-one clauses, not #SAT, strict C5, or ordered R counting.

Each edge e has a nonempty set P_e of original physical signal bits. Different P_e are disjoint. A changing bit equals z_e or its complement. An original bit cannot be erased or copied without a prior read. [3] proves the compiler's source-support property; this run imports it at that pinned revision and does not claim independent review of the entire compiler.

Fix first a deterministic preprocessor P followed by a randomized algorithm R. The whole machine is correct on every valid decision input with error at most eta, 0<=eta<1/2, and halts almost surely. Randomness is independent of the input. Each random-bit generation, stored random seed, access, movement and write is charged in a randomized extension of the same finite-alphabet one-tape model. The deterministic eta=0 case is the project's principal model. No quantum claim is made.

On a fixed balanced source I_z, suppose P reaches an actual checkpoint after acquiring only tree tag signals and no cotree signals. It may compute, copy, relocate, cache and recompute without further restrictions. Let C be that checkpoint. On each neighbor I_(z^e), the exact same deterministic prefix reaches C^e with equal control, head, work and output, differing only on untouched original P_e. This follows by replay; no solver-created dependent cache can already distinguish the pair. The checkpoint can be reached by the uniform scan-first wrapper, but arbitrary solvers are not required to adopt its ordering.

The error assumption is on these full inputs and hence on R from their respective common-prefix states. We do **not** condition a globally correct randomized preprocessor on an arbitrary rare history and assume its conditional error remains eta. That stronger claim is not established. A separate whole-run variant allows randomized preprocessing and charges first hits from the start.

Four falsifiers: a preloaded verdict distinguishes the neighbors; the checkpoint was selected using unseen labels or biased random history; one primitive acquires multiple disjoint source supports for free; or an epsilon-far guarantee is used for a one-edge-defect input. The first two violate the explicit common-prefix premise, the third changes the machine/capacity model, and the fourth is the transfer refuted here.

## Coupling proof with actual event membership

For each cotree e, couple the runs from C and C^e using the same infinite independent random-bit stream. Until a cell of P_e is scanned, all reads, writes, internal states and random-bit uses agree. This remains true with adaptive choices, arbitrary algebra and relocation: prior reads and all consequent work are identical. If the base run halts without hitting P_e, the neighbor run has the same output.

Write H_e for the event that the actual base suffix scans P_e before it halts. Under this coupling, the difference between the acceptance probabilities is at most Pr(H_e). Correctness gives

Pr[R(C)=SAT]>=1-eta,
Pr[R(C^e)=SAT]<=eta.

Therefore Pr(H_e)>=1-2eta. For every realized base run, choose E_e to be the singleton containing the first hit of P_e, or empty if never hit. The P_e are disjoint, so every physical transition belongs to at most one E_e. Consequently

E[T_suffix] >= E[sum_e |E_e|]
             = sum_e Pr(H_e)
             >= (1-2eta)r.                         (1)

This proof allows early wrong outputs on the eta fraction of runs and does not assume every bounded-error run reconstructs all labels. With eta=0 it recovers r indispensable first reads almost surely, and deterministically for a deterministic decider. With one-sided correctness that always accepts balanced inputs and has false acceptance at most eta on every unbalanced input, the probability gap is at least 1-eta instead, giving (1-eta)r.

For an arbitrary randomized whole solver with no restricted preprocessor, couple entire runs on I_z and I_(z^e). Equation (1) then lower-bounds whole-run first-hit work, including preprocessing, by the same expression. It does not provide an additive suffix charge after those reads have already occurred.

The event argument uses one real bit read per transition, capacity one, and maximum reuse one. Addresses, copy locations and stopping are determined by the actual execution, not free lookup operations. There is no requested output of the full source or a witness. Source-observation necessity comes from opposite required Boolean answers.

### Entropy is a separate one-way account

For deterministic exact R on the balanced prior, let U be all r cotree labels, B the public machine/layout/prior and full replayable tree prefix, Pi the chronological r first-signal payloads and E their actual transitions. The record has fixed conditional length r, is prefix-free, and its replay decodes U; b=1,h=0,rho=1. Tree potentials determine U on this prior, so H(U|B)=0. The shared coding inequality is valid but vacuous. Equation (1) uses a different, explicitly justified coupling/indistinguishability argument.

For randomized error-allowing R, full U need not be decoded from every stopped record. We therefore do not assert the zero-error decoder premise for (1). Nor do we sum a balanced-prior entropy bound and a query bound from a different distribution. Recounting a sampled edge increases physical query time, not the number of independent necessary first-hit events.

## Constructive method and complete costs

Preserve the useful algorithm: authenticate the source, compute vertex potentials from a forest, and check remaining edge constraints. If a checked edge conflicts with the potentials, its tree path plus that edge is an explicit odd cycle. This supplies a sound UNSAT certificate. If only some edges have been checked without conflict, the sound internal result is UNKNOWN. SAT is justified once every required constraint is verified. A single cached final verdict then suffices for output.

In a normalized representation with the graph and tree supplied, potential propagation plus verification uses O(q+k) elementary graph/group operations and O(q+k) words, with O(log q)-bit addresses. This is not a raw-tape total-cost bound. A deterministic complete source implementation retains all parsing, header/range checks, canonical template discovery, correlated-copy checks, exact regenerated row comparison, failed candidate work, address arithmetic, representation changes, random bits if used, caches, recomputation and origin output.

The established conservative raw-source guard costs O(N^4) indexed bit operations and O(N²) stored bits; one-tape simulation charges O(N³) per such operation. For the admitted family this gives T=O(N^7), peak physical span O(N²), physical CM O(N^9), and minimum-description CM O(N^8). These displayed upper bounds refer to deterministic full verification. Optional random sampling must charge its own coin generation and retained randomness; an input-and-time description alone does not reconstruct a randomized configuration. No expected-to-worst-case conversion or identical descriptive-CM bound for that randomized variant is assumed. General valid nonimages receive UNKNOWN from the guard and an exact exhaustive Boolean fallback: O(2^n N^7) time, O(N²) space, O(2^n N^9) physical CM and O(2^n N^8) descriptive CM. Thus the constructive method is polynomial on this class only.

For the randomized suffix in (1), original signal positions all lie beyond L_0>=N/4 in this row layout. The posttransition head remains within one cell of the scanned position. Charging the same distinct first-hit events yields E[CM_phys_suffix]>=(N/4)(1-2eta)r in cell units. A physical charge cannot be inverted into a minimum-description lower bound. The full uniform tape implementation was not executed.

For the deterministic P-versus-NP comparison, a fixed cap T<=K N^a, a>=1, implies S=O(N^a), physical CM O(N^(2a)), minimum-description CM O(N^(a+1)); separate count-map circuit size is O(N^a log N). Our source demand is only O(N/log N) and its physical product is O(N²/log N), so these do not exceed all polynomial caps. The randomized expectation bound is not silently substituted into a deterministic simulation theorem or a counting conclusion.

The transport control retains its internally reviewed single-tape quadratic-time/cubic-CM bounds and matching polynomial algorithm; its static demand ceilings are Delta h<=N²/8 and Delta h²<=N³/27. Different source layouts and runs are not added together.

## Reproducible finite falsifier

The new [script](../../../experiments/dynamic_discovery_exact_testing_20261123.py) and [raw output](../../../results/raw/dynamic_discovery_exact_testing_20261123.json) audit an explicit candidate sampling rule, **not an implementation of the paper's tester**. After tree acquisition, choose a uniformly random t-element subset of r cotree edges, check it against the prediction, and accept if none conflicts. For one defective edge,

Pr[false acceptance]=1-t/r.

The program exhausts all sample subsets using exact rational arithmetic, every balanced signing and every one-cotree-flip neighbor for q=4,5. It checks 96+672=768 comparisons. At q=5, r=6, sampling three edges misses a single defect with probability 1/2. Sampling with replacement for s draws instead has miss probability (1-1/r)^s; even r draws leave 15625/46656 at r=6. A three-valued wrapper returns UNSAT on conflict, UNKNOWN on incomplete passing samples, and SAT only after complete passing verification. It never incorrectly accepts any tested neighbor.

Code SHA-256: 43e06cf3dbec62e15e759903cd70bada608c25d794b307065dfca09d9d735ebd.
Raw SHA-256: b2894db7d10f95e29dc93d78263fef69acd60293eb0e1ad12b00dfae636f07f1.
Run python3 experiments/dynamic_discovery_exact_testing_20261123.py. No random seed or Monte Carlo evidence is used. This normalized calculation does not measure source-machine time, run a solver kernel, or replace the symbolic coupling proof. Accounting's separate physical traces are credited to its published artifact, not repeated.

## Search record, controls and next owner

Fresh literature queries: "randomized decision tree sensitivity lower bound query probability differing single bit Nisan 1991" and "Noam Nisan CREW PRAMs and decision trees 1991 pdf block sensitivity randomized". Primary-paper retrieval and exact access limitations are recorded above. The Adriaens–Apers PDF was reread for its distance definition, all-input promise, one-sided error, and the distinction between query and full computational time. This run imports only that scoped tester contract. No pebbling, online-update or witness-enumeration lower bound is imported.

Fresh official-repository queries:
"site:github.com/anthropics property testing SAT";
"site:github.com/openai property testing graph";
"site:github.com/xai-org randomized graph";
"site:github.com/google/or-tools randomized exact SAT certificate";
"site:github.com/google-research signed graph testing";
"site:github.com/google-deepmind graph testing algorithm".

The Anthropic/OpenAI/xAI narrow queries produced no directly usable theorem. Broad previous leads were retained with their inspected pins, not deeply re-reviewed. The Google searches found CP-SAT parameters and solver documentation, graph-learning benchmarks and relational-reasoning tests. None establishes this post-acquisition transfer. Nonofficial signedgraph and third-party solver wrappers were not relabeled as official. Search absence is bounded, not exhaustive.

Official ownership was checked through the verified Anthropic/OpenAI organization domains, xAI's Grok open-release link to xai-org, Google's public organization guidance, and Google Research/DeepMind publisher/profile links. Exact inspected pins in this session: anthropics/formal-math 16a5ce41304fcdaea4e0be7c132e1c361dc26da5 (eth/README.md); openai/miniF2F 4e433ff5cadff23f9911a2bb5bbab2d351ce5554 (README.md); xai-org/grok-1 7050ed204b8206bb8645c7b7bbef7252f79561b0 (README.md); google/or-tools 4782dbd0aa85621c8115cf33de1574a2e6757004 (SAT README and sat_parameters.proto header); google-research/google-research 87e25a5ba04d2c4cf0108f0cec96d648fe2b945a (README.md); google-deepmind/clrs 6d5728b9efadf8648413c8c473929a733caacced (README.md). CP-SAT's parameter header distinguishes random branching/polarity choices; the fetched 60-line excerpt is not a full correctness audit. Formal-math's advertised subexponential claim remains unverified here and is not a polynomial-time theorem. No external repository code was executed.

DISJ/opposite-label sanity PASS by explicit equal-length source neighbors. Simultaneous DTISP PASS for the deterministic ledger and separately scoped expected random ledger. Configuration counting remains an upper-bound check, not inference necessity. Relativization/nonrelativizing progress OPEN for unrestricted separation; no Natural Proofs or algebrization breakthrough is claimed. Affine/Tseitin and forest-potential algorithms are preserved. Complement swaps output names without changing coupling. Forced-domain/all-balanced promises invalidate the necessary alternatives. Private-leaf residuals, prescribed computation DAGs and virtual online services do not add obligations. A verified cached verdict closes this source-verification phase.

**One next dependency, owner Bounds, receiving Construction and Synthesis:** prove an actual post-acquisition opponent family whose difference sets survive paid joint computation after the original signal supports have all been hit. The snapshot first-hit proof does not regenerate that family. Alternatively, Construction may generalize the forest-potential algorithm to a genuinely broader decision-preserving relation class with a fully priced admission and evaluator. A small remaining entropy or a passing sample alone supplies neither result.

The run used connected source recovery rather than a full checkout; preflight, native uniform parser/tape build and proof-assistant verification remain unexecuted. No independent-review promotion, owner-manuscript changes or schedule changes were made. The Accounting artifact completed immediately before this Discovery task has its own namespace and provenance.

[1] Florian Adriaens and Simon Apers. [Testing properties of signed graphs](https://arxiv.org/abs/2102.07587), v1, 2021. [Readable PDF](https://arxiv.org/pdf/2102.07587).
[2] Noam Nisan. [CREW PRAMs and Decision Trees](https://doi.org/10.1137/0220062), SIAM J. Comput. 20(6), 999–1007, 1991. Full text unavailable in this run; background credit only.
[3] [Accounting forest-prediction audit](https://github.com/j15marti/pnp/blob/688e198257c63518f02f82d6f8ee347ba3e8a910/research/agents/charged-accounting/PNP_Charged_accounting_2026-11-23_004800_Forest_Prediction_Audit.md), source support/layout proof and raw physical evidence. [Earlier signed-cycle ledger](https://github.com/j15marti/pnp/blob/64a60d9f8dec3f5790fc72306fbf0a0eeff58941/research/agents/charged-accounting/PNP_Charged_accounting_2026-11-23_002255_Signed_Cycle_Source_Ledger.md).
[4] [Synthesis diamond networks](https://github.com/j15marti/pnp/blob/bf8e52241a80da97365fe86c6985c3ab15b991d9/research/agents/charged-synthesis/PNP_Charged_synthesis_2026-11-22_122415_Diamond_Networks.md). [Discovery's previous update-interface report](https://github.com/j15marti/pnp/blob/e3cf120db7fc6fd791305235f1c7b8bc7bd6371e/research/agents/charged-discovery/PNP_Charged_discovery_2026-11-22_115323_Diamond_Update_Interfaces.md).
