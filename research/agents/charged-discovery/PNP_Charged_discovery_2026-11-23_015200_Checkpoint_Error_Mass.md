# Error mass at a selected randomized checkpoint

23 November 2026, 01:52 PST (America/Los_Angeles). PNP Proof Discovery.
**CHECKPOINT-ERROR-MASS1**, within DYNAMIC-COMPATIBILITY-OBLIGATION1.
**PROVED/EXACT**, restricted same-execution coupling statement; independent adversarial review pending.
The unchanged-global-error checkpoint transfer is **FALSIFIED/RETIRED**, already known in this repository.
Unrestricted compulsory post-acquisition computation and P versus NP remain **OPEN**.

## Recovered dependency and precise increment

Starting head: cb5d027def26bf596dc1258b1e09a7a46198db30. The latest Discovery report [1] proves a (1-2 eta)r source-read bound after deterministic preprocessing and explicitly leaves arbitrary randomized checkpoint conditioning unjustified. Accounting [2] supplies physical disjoint cotree supports and the row layout. All six current handoffs were recovered. The only newer main commit is a strict-T5 status log; its external upper-bound assertions are not imported without verification.

A corpus search recovered LSPV-4's **ARC-CHECKPOINT-RESIDUAL148** [3], which already proves the unconditional residual LP with prior-hit probabilities and gives a selected-state error counterexample. Its result is credited, not renamed as new. No old experiment was rerun. This report adds an explicit selected-event error-mass bound, sharp two-sided coefficients, and its physical application to the current diamond encoding. It closes the conditional-error bookkeeping gap in [1], not the main post-acquisition lower-bound gap.

Four falsifiers:
1. Use an unconditional error eta as the conditional error on a selected event of probability p.
2. Pair checkpoints using different coin subsets or allow earlier reads of an allegedly untouched support.
3. Charge the same first hit more than once, or silently use unit-cost multi-address reads.
4. Promote randomized bounded-error correctness to deterministic exact SAT correctness.

## Primary-source transfer examined

O'Donnell, Saks, Schramm and Servedio, *Every decision tree has an influential variable*, arXiv:cs/0508071v1, FOCS 2005 [4], Theorem 1.1, proves Var(f) <= sum_i delta_i Inf_i(f) for an exact decision tree on a product input distribution. Its randomized extension averages zero-error trees. Section 3.2 gives the product-space hybrid proof; Section 3.3 treats approximation separately. The retrieved PDF carries the v1 identifier dated 16 August 2005 and a typeset title-page date of 24 September 2018.

This is a relevant revealment mechanism, but neither exactness nor the input distribution survives arbitrary conditioning for free. A complete fixed query transcript can leave a product distribution on unqueried independent coordinates; an arbitrary event or compressed machine state need not. A distribution only on balanced signings is correlated. We therefore do not insert our selected machine checkpoint into that theorem. The elementary error-mass proof below needs no product prior and explicitly retains possible errors.

The CMU copy had unreadable extracted glyphs; the arXiv PDF was readable and its definitions and proof were inspected. No numerical graph-property bound or approximation theorem from that paper is used.

## Source, machine and quantifiers

Use [2]'s complete-graph binary diamond source for q>=3, k=q(q-1)/2, r=k-q+1. The positive Boolean exact-one encoding has

n=33q+111k, m=21q+87k,
w=ceil(log2(n+1)),
N=n+2+2 floor(log2(m+1))+3mw.

The input has a unary variable declaration, gamma-coded m+1, and m triples of w-bit incremented variable identifiers. Whole rows are ordered public, star-tree-owned, cotree-owned by a fixed signing-independent permutation. SAT is equivalent to z_uv=x_u XOR x_v. Every cotree flip of a balanced signing is UNSAT. This is Boolean exact-one decision, not strict T5 counting or a claimed Horn-witness compiler.

Let x be any fixed balanced full source and x^e its single-cotree-flip source. Original physical difference supports P_e are nonempty, pairwise disjoint and all at positions at least N/4. Import the support/layout proof from [2] at its pinned revision; no independent compiler certification is claimed.

Fix a uniform randomized one-tape machine A first. It has fixed finite alphabet/control, unit head motion, charged reads/writes/random-bit generation, no free clock or source oracle, and terminated output at the origin. Random coins are independent of the source. A halts almost surely and has error at most eta<1/2 on every valid full input. Deterministic exact machines are the eta=0 specialization. This randomized extension is explicitly separate from the main deterministic model.

Use the same infinite coin stream omega for all paired executions. Let sigma be an actual stopping rule and G a measurable event of probability p>0, selected from executed prefix information. For every omega in G, require that the runs on x and every x^e reach corresponding checkpoints with the same consumed coins, control, head and all tape cells outside P_e, and that neither prefix has read P_e. The same set G of coin streams must work for every pair. This follows for a common observable tree-only prefix event; it is an explicit premise for more general checkpoints. Whole input retention, arbitrary paid computations, copies and caches remain allowed.

Let F_0 be the event A errs on x, and F_e the event A errs on x^e. Define **unconditional error masses inside the gate**

epsilon_0(G)=Pr(G intersect F_0),
epsilon_e(G)=Pr(G intersect F_e).

These are not conditional error rates. They are at most eta, but after division by p the conditional rates can be much larger.

## Selected-event theorem and proof

Let H_e be the event that the actual x continuation first scans P_e after sigma and before halting. Events are considered only on G. Let T_suf and CM_phys,suf be actual costs after sigma; extend their gated values by zero outside G.

For every such A,x,sigma,G and every cotree e,

Pr(G intersect H_e) >= [p-epsilon_0(G)-epsilon_e(G)]_+.

Consequently,

E[1_G T_suf] >= sum_e [p-epsilon_0(G)-epsilon_e(G)]_+
                 >= r [p-2 eta]_+,

E[T_suf | G] >= r [1-2 eta/p]_+.                         (1)

**Proof.** On G, until a P_e read the coupled continuations see identical symbols and coins and take identical transitions. All algebra, writes, addresses and cache accesses are included in this induction. If no P_e read occurs, the two outputs agree. Their required outputs differ, so at least one of F_0 or F_e occurs. Thus G minus H_e is contained in F_0 union F_e. Taking measures gives the first inequality. Define E_e(omega) as the singleton first-hit transition on G intersect H_e, empty otherwise. Pairwise disjoint supports imply each physical transition belongs to at most one E_e. Sum their probabilities and divide by p. This proves (1) without assuming independent errors or independent hit events.

At each such first-hit transition the post-transition head is at least N/4-1 from the origin. The origin-anchored interval therefore has at least N/4 cells, even when the scanned symbol is erased. The same events give

E[1_G CM_phys,suf] >= (N/4) sum_e [p-epsilon_0(G)-epsilon_e(G)]_+.  (2)

This is not a product of unrelated maxima. For one-sided always-correct balanced outputs, epsilon_0(G)=0 and eta replaces 2 eta. For eta=0, every positive-probability admissible gate retains r compulsory support hits almost surely. For p=1, (1) recovers [1]. If eta>0 and p<=2 eta, the coarse bound is correctly zero.

**Relation to the shared decoder test.** Here U_e is the source tag, B_e includes the public template and actual prefix record/consumed coins, and E_e is the real first-hit event above. A hit carries at most one binary tag bit; event reuse rho=1. A bounded-error run need not reconstruct U_e, and the selected-event proof supplies no universal conditionally prefix-free Pi_e decoding it with zero error. Therefore the entropy formula is not invoked with fictional zero overhead. The explicitly justified alternative is the coupling/event bound (1). On the balanced prior even the whole cotree vector is determined by observed tree tags, so its entropy still cannot measure this discrimination work. Retained source is not granted as a free newly queried oracle.

## Sharpness and globally defined bypass

Fix eta=1/8 and draw four fair bits, all charged. On two of the 16 seeds immediately output SAT, on two immediately output UNSAT, and on the other twelve run a deterministic total exact solver D. This one fixed algorithm has error exactly 1/8 on every valid input of either label. Take G to be the four guessing seeds. Then p=1/4, both conditional error rates are 1/2, and no cotree support is ever read on G. Checkpoint and output operations still cost O(1) transitions; we claim zero support hits, not zero runtime.

This is a legal all-input bounded-error procedure, not an exact algorithm and not a proposed speedup. The branch occurs before source-dependent access apart from public initial header symbols, so the paired gate condition is genuine. It can also follow any common tree-only preprocessing, with that preprocessing fully charged. No all-UNSAT promise is involved.

More generally for a dyadic p, allocate guessing mass at most eta to each answer inside G and run D on the remaining gate mass. When p>=2 eta, both masses can equal eta, leaving p-2 eta for the exact branch. When p<2 eta, divide all gate mass between two guesses with each mass at most eta. Choose D to acquire every cotree support on the recognized family. Then the expected number of distinct cotree hits inside G equals r[p-2 eta]_+. This establishes sharpness of the coarse support-hit coefficient, not tight physical transition complexity.

D authenticates the canonical source by exact regenerated comparisons, validates ranges, repeated copies, row order and end framing, computes forest potentials and checks all constraints, caches its verdict, and writes the terminated output. On a valid guard miss its internal result is UNKNOWN and a total exhaustive decision fallback handles the original input. A failed heuristic check alone never supplies SAT or UNSAT. The normalized finite checker uses an enumerated oracle in place of D; the uniform symbolic implementation and costs are inherited, not benchmarked.

## Complete costs and fixed-cap comparison

The finite seed uses four random-bit operations and O(1) retained state. Before source acquisition, the guessing branch has T=O(1), total physical span Theta(N) because the input remains, and physical CM O(N). Its configuration's minimum description may include N input bits even though the output was guessed. Random generation does not make input retention free.

The exact admitted branch inherits conservative symbolic T=O(N^7), S=O(N^2), physical CM O(N^9), minimum-description CM O(N^8). The source parser, template discovery, comparison, failed attempts, address arithmetic, initialization, retention, copies, relocation, sharing, potential computation and output are all within that tariff [2]. The finite four-bit seed adds only a constant description. On arbitrary valid guard misses the fallback is O(2^n N^7) time with O(N^2) storage, so this is not a polynomial all-input solver.

For the general randomized theorem, a pathwise cap T<=K N^a gives S=O(N^a) and physical CM O(N^(2a)). A replay description must include consumed randomness: K(C_t|A)<=O(N+R_t+log(t+2)). With at most one fresh bit per transition this yields O(T(N+T+log T)) cumulative description, rather than automatically the deterministic O(N^(a+1)) ceiling. For deterministic A, or the fixed-four-bit wrapper here, the stated deterministic O(N^(a+1)) ceiling remains valid. The O(N^a log N) count-map circuit ceiling remains a separate deterministic counting statement.

Since r=Theta(N/log N), (1) cannot exceed a linear-scale source-hit demand and (2) is at most order N^2/log N. Selection divides by p only after reducing the available error mass; it does not amplify the whole-execution demand. These bounds do not defeat every fixed polynomial exponent. A cached exact verdict after full acquisition can eliminate all further source hits.

## Reproducible finite audit

[Code](../../../experiments/dynamic_discovery_checkpoint_mass_20261123.py) and [raw](../../../results/raw/dynamic_discovery_checkpoint_mass_20261123.json). Run the Python script from repository root. Standard library; no sampling or Monte Carlo.

For q=4: n=798, m=606, N=18998, r=3. The audit uses all 64 signings, 8 balanced ones, 24 balanced/opposite-source pairs, 16 gate sizes and all 16 seeds, for **16,384 exact coin/source/gate evaluations**. It reuses the pinned generator only to validate this new gate experiment's source-support premise; it does not repeat the prior physical scan experiment. Every gate attains r[p-1/4]_+ in the normalized hit count. At p=1/4 it has zero conditional hits and 1/2 conditional error on each label. At p=1 it has 9/4 expected hits and error 1/8.

Code SHA-256: a1818171a223eb99dd7c37ae791c867b365e7073917f351992d8cbc170e67e63.
Raw SHA-256: 36b40d59a205896c32f6b5c52a50332da697779e16c23968e078bdd33eb87392.
Dependency hashes appear in the raw output. Native parser/tape runtime, proof-assistant kernel and full-checkout preflight were not run. The workspace contains recovered experiment files, not a complete repository checkout.

## Fresh search record and review limits

Literature queries:
- O Donnell Saks Schramm Servedio every decision tree influential variable randomized revealment inequality pdf
- randomized query complexity block sensitivity error coupling preprocessing conditioning transcript

Only [4] is imported as an external theorem, within its stated hypotheses. Other search results did not supply a verified arbitrary-offline-SAT post-acquisition transfer.

Official repository queries, made afresh on this run:
- GitHub org anthropics: randomized SAT; web site:github.com/anthropics randomized SAT formal verification, followed by quoted randomized/SAT terms.
- GitHub org openai: decision tree proof; web site:github.com/openai randomized decision tree formal proof and quoted decision tree/proof.
- GitHub org xai-org: randomized verification; web site:github.com/xai-org SAT verification random and verification.
- GitHub org google: random_seed; web site:github.com/google/or-tools randomized SAT correctness and random_seed.
- GitHub org google-research: decision tree revealment; matching web query.
- GitHub org google-deepmind: conditional probability randomized; web site:github.com/google-deepmind randomized algorithm verification.

Ownership was checked through the verified anthropics/anthropic.com and openai/openai.com profiles, x.ai/news/grok-os linking xai-org, Google's official GitHub organization guidance, and the Google Research/DeepMind organization profiles linked to research.google/deepmind.com. No Verified badge is asserted for the latter two.

Relevant inspected code:
- [anthropics/formal-math](https://github.com/anthropics/formal-math/blob/16a5ce41304fcdaea4e0be7c132e1c361dc26da5/eth/proof/statements/KSatFreeCodeStatement.lean), blob 7e3f1664a24a94f2fb436a204781e32aa905cc4a: DecidesRandTM quantifies correctness mass over all finite seeds for each input and bounds every seed's runtime. It contains no automatic per-checkpoint error guarantee. This is a read of definitions, not a kernel verification or adoption of the repository's broader ETH claims.
- [google/or-tools](https://github.com/google/or-tools/blob/4782dbd0aa85621c8115cf33de1574a2e6757004/ortools/sat/sat_parameters.proto), blob 57202e89a891ca09187cd6672809b5a046941f18: random_seed affects search choices and benchmarking. That does not license incorrect outputs on selected seeds or supply a lower bound.

OpenAI search returned unrelated Jacobsthal tree prose at openai/math commit 4eaee87548250b2682affda7d05d947c05554bae and software execution-plan prose; excerpts rejected as irrelevant. xAI returned software-harness verification at grok-build commit 2bdd1d6a6369de0e8c68132ea4539e9abd9e14a8, not a mathematical checkpoint theorem. Google Research connected search returned no matches. DeepMind returned game chance code at open_spiel commit 4956843d7375e29a4c986425c66f897d7ac15340 and unrelated image sampling; web results also surfaced verification/debate projects, but no theorem was imported from unreviewed snippets. These are bounded-search outcomes, not exhaustive absence claims. Third-party repositories with vendor names were not treated as official. No vendor code was executed.

Repository duplicate query: checkpoint conditional error (then probability added), which recovered [3]. Branch-name query charged returned no branches; this is not an exhaustive draft-content audit. Issue #324's two latest comments matched [1,2]. Governance and model sources were recovered through connected reads. Other role files, historical manuscripts, identities and schedules remain unchanged.

## Controls and one next dependency

DISJ/opposite-label sanity PASS: equal-length physical source neighbors have opposite decision labels. Simultaneous DTISP PASS for the stated pathwise events. Deterministic configuration gate PASS with the explicit randomized replay distinction. Relativization/nonrelativizing progress OPEN for an unrestricted separation; no barrier-crossing step is claimed. No algebrization or Natural Proofs escape is asserted. Affine/potential evaluation and the cached exact verdict remain legal controls. Fixed DAGs, online services, model counting, witness enumeration, complement/private-leaf/forced-domain information do not create additional compulsory events here.

**Next owner Bounds, receiving Construction and Synthesis:** prove a reachable opposite-answer distinction after all original supports have been hit on a new family, or accept the current polynomial forest evaluator as the terminal control. For any randomized extension, supply gate probabilities and per-input error masses rather than reuse a global eta after conditioning. Accounting receives (1)-(2) and the coin-description correction; Redteam is asked to attack the common-gate coupling and the source-support premise before promotion. No independent review is claimed.

[1] [Discovery exact testing transfer](https://github.com/j15marti/pnp/blob/dd64ec3a4bfe9127538c7b056427b3a5120070ba/research/agents/charged-discovery/PNP_Charged_discovery_2026-11-23_005400_Exact_Testing_Transfer.md).
[2] [Accounting forest prediction audit](https://github.com/j15marti/pnp/blob/688e198257c63518f02f82d6f8ee347ba3e8a910/research/agents/charged-accounting/PNP_Charged_accounting_2026-11-23_004800_Forest_Prediction_Audit.md).
[3] [LSPV-4 original checkpoint residual report](https://github.com/j15marti/pnp/blob/cb5d027def26bf596dc1258b1e09a7a46198db30/research/agents/lspv-4/2026-10-26_2302_LSPV-4_ARC_CHECKPOINT_RESIDUAL148.tex).
[4] [OSSS primary paper](https://arxiv.org/pdf/cs/0508071), arXiv:cs/0508071v1, §§1.1-1.2 and 3.1-3.3. No claim of novelty for the elementary coupling technique.
