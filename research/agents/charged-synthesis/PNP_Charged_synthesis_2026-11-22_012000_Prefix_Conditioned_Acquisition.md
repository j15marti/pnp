# Prefix-conditioned acquisition and the remaining dynamic dependency

22 November 2026, 01:20 PST. PNP Charged Proof Synthesis.
**DYNAMIC-PREFIX-CONDITIONED-INNOVATION1**, within DYNAMIC-COMPATIBILITY-OBLIGATION1.
Recovery revision e76095277d6469b50f3ba3bf0830cebf9f8f91aa.
**PROVED/EXACT restricted information ceiling, conditional on the explicitly stated decoders. Independent adversarial review requested, pending. P versus NP OPEN.**

The strongest current concrete candidate is Construction's authenticated gate-cycle/factor pipeline, enlarged by Discovery's verified affine alternative. Its compulsory-work implication remains unproved. This note closes one narrower integration question: splitting Bounds' initial acquisition into successive replayable stages cannot generate more than N bits of new conditional demand in total. It does not bound the time needed to process those bits.

## Five-peer reconciliation at exact revisions

| Role and source | Retained result | Rejected or unresolved implication |
|---|---|---|
| [Construction 00:33, 3757eba](https://github.com/j15marti/pnp/blob/3757eba746904cbe2983b6cbdda9f8a3bf9b0f07/research/agents/charged-construction/PNP_Charged_construction_2026-11-22_003353_Factor_Backdoor_Acquisition.md) | Local sufficient certificate of size h is found with failed search included; admitted solver O(3^h N^5), span O(N). Cycle is SAT iff p or q is odd. | Uniform logarithmic h is false even for easy positive disjoint clauses. This is an upper bound, not compulsory execution. |
| [Accounting 00:43, 4ed0e24](https://github.com/j15marti/pnp/blob/4ed0e245baadd5e7a41a82d979fa77056e8428dd/research/agents/charged-accounting/PNP_Charged_accounting_2026-11-22_004337_Branch_Equivocation.md) | Actual-record demand subtracts residual uncertainty epsilon, framing and event reuse. Cycle's two branch bits lose (3/4)log2(3) bits after OR. | Exact recovery of branch information does not follow from a correct final label. |
| [Discovery 00:46, e9ad514](https://github.com/j15marti/pnp/blob/e9ad51427d7ba24508085ed2c31e1fa29c0c503b/research/agents/charged-discovery/PNP_Charged_discovery_2026-11-22_004633_Affine_Parameter_Control.md) | Dense parity sources have h=d but a paid polynomial Gaussian solver handles both labels, T=O(N^(7/2)). | Large factor parameter does not force exponential work. Connected affine/factor mixtures have no solver proof yet. |
| [Bounds 00:57, 12da5f0](https://github.com/j15marti/pnp/blob/12da5f0cf86d3b5d0c1e808f7a1adeee6eab472d/research/agents/charged-bounds/PNP_Charged_bounds_2026-11-22_005702_First_Read_Replay.md) | Known-start replay reconstructs addresses/times from globally first-scanned original bits; conditional prefix freedom, at most N bits. | Unknown later starting scratch is excluded. One acquisition record is not a repeated transport theorem. |
| [Redteam 01:15, e760952](https://github.com/j15marti/pnp/blob/e76095277d6469b50f3ba3bf0830cebf9f8f91aa/research/agents/charged-redteam/PNP_Charged_redteam_2026-11-22_011502_Restart_Replay_Audit.md) | Explicit read/write/erasure trace reproduces initial replay and the charged cache-read repair. | Opposite labels have identical empty late records if only globally new original reads count. No defect alleged in Bounds' excluded case. |

Original Construction generator/raw, Discovery elimination/raw, Accounting's exact derivation and Redteam transition code/raw were recovered. Own preceding residual-factor report was read fully. Its acquisition handoff is now answered only for Construction's specified local certificate. The broader all-input coverage question is still open. Same-conversation peer reports and finite tests do not constitute external independent certification.

## One quantified lemma

Fix a deterministic finite-alphabet single writable-tape machine A before choosing N or a finite distribution mu over valid length-N binary SAT encodings on which A halts correctly. The input occupies cells 0 through N-1, other cells are blank, initial control/head are public, and each transition reads before writing and moves at most one cell. Copies, source, addresses, work and terminated fixed-origin output share that tape. No online restriction is imposed.

Let B specify A,N,mu and the public initial layout. Let E be the actual transition indices at which A first scans an original input cell. Let Pi list the original bits read, in execution order. No input-dependent advice, start-state annotation, source array or absolute clock is added to B. Bounds' initial replay reconstructs the scanned configuration and event addresses, and halting makes the support of Pi prefix-free. In particular |Pi|=|E|<=N.

Fix a finite number s of phase slots and stopping rules before sampling I. Each boundary must be recognizable by the replay decoder from B and the bits consumed so far, with no future lookahead or hidden checkpoint annotation. The last slot ends at halt; unused slots after halt are publicly padded by empty records. Let Z_j be the consecutive block of Pi consumed in slot j and E_j the corresponding original-first-scan transitions. Zero-bit segments are allowed only when their end is reconstructible without another unknown input bit. Thus the E_j are disjoint, cover E, and the tuple (Z_1,...,Z_s) is reconstructible from Pi and B.

For each j fix an obligation U_j=f_j(I), independently of a desired resource lower bound. Assume an actual decoder d_j with

    d_j(B,Z_1,...,Z_j)=U_j

on every input in the support. This is a hypothesis to prove for a proposed obligation; Boolean decision correctness does not provide arbitrary f_j. Put B_j=(B,Z_1,...,Z_(j-1)) and Pi_j=Z_j. Then

    sum_j H(U_j | B_j)
       <= H(Pi | B)
       <= min(H(I | B), E|Pi|)
       <= N.

Moreover each Z_j is conditionally prefix-free given B_j, with b=1,h_j=0,rho=1, and these same actual events establish

    E[T] >= sum_j H(U_j | B_j).

The final inequality is useful only up to the stated acquisition ceiling. It is not an O(N) upper bound on T.

### Proof

Given a prior record prefix, deterministic replay reaches the same boundary configuration on every compatible input. Within the next slot it supplies known or previously written symbols directly and requests one new bit exactly at an original first scan. If one valid slot record were a proper prefix of another, the replay would encounter the public ending predicate after consuming the shorter word on both executions, contradicting the longer word's being a record of that slot. If no bit is needed, the empty word is the only possible word conditional on that prefix. This proves conditional prefix freedom without a length or address channel.

The exact decoder makes H(U_j|B_j,Z_j)=0. Therefore

    H(U_j|B_j)=I(U_j;Z_j|B_j)<=H(Z_j|B_j).

Summing and applying the finite Shannon chain rule yields H(Z_1,...,Z_s|B). Concatenation recovers Pi, while public replay reconstructs the boundaries, so this equals H(Pi|B). Pi is a deterministic function of I, giving the H(I|B) ceiling. Its prefix-free support gives H(Pi|B)<=E|Pi|. Finally, conditional coding in each slot gives H(U_j|B_j)<=E|Z_j|=E|E_j|; disjointness gives sum |E_j|=|E|<=T. This proves all displayed statements.

No proof logger is inserted into A. The external decoder may take the entire runtime to replay; no efficient compression, inverse or access primitive is asserted. If boundaries require input-dependent metadata not reconstructed by replay, it must be included and charged. The zero-framing lemma then no longer applies verbatim.

### Four falsifiers and precise scope

1. An input-dependent boundary or slot count conveys extra information not present in Pi. Require the public stopping rules above or pay for the metadata.
2. Marginal H(U_j|B) is summed while previous record information is silently available. Those are different side-information conventions; conditional innovation cannot be replaced by repeated marginal demand.
3. A local observer is granted the entire prior transcript although the intended locality model forbids it. Our lemma concerns a global replay decoder. It does not establish that every physical local decoder has this side information.
4. Events from different runs or repeated copies of the same acquisition are treated as disjoint. Our E_j partition one execution. Any reuse elsewhere needs its actual rho.

Thus this result does NOT refute repeated transport lower bounds, even for a short input. A local observer may repeatedly lack information that a global observer already knows. Proving and charging that locality is exactly the missing dynamic implication. Full-state entropy and unrestricted offline algorithms remain allowed.

## Concrete family, ledger and cap comparison

The selected cycle has k cyclic names plus gate g, even k>=6, marks 0,p in gate zero and 0,q in gate one. Forced zero degrees and alternating degree-one constraints give branch bits p mod2 and q mod2. This source derivation covers both SAT and UNSAT. It is not strict counting.

For the same canonical compiler let c=4k+4,d=k+1,r=c+1,
n0=d+(10c+1)r+2, m0=(20c+4)r, n=n0+m0+3, m=2m0+4,
w=ceil(log2(n+1)), and

    N=3n+2+2 floor(log2(m+1))+3m(w+1)+w=Theta(k² log k).

Unary n and delimiter, gamma(m+1), signed width-w triples, two n-bit adjacent local assignments and the w-bit release ID comprise the physical input. Compiler equivalence and local witness properties retain their existing internal-review status. The physical cut layout of the permutation control is not transferred through this compiler.

Fix A_cycle as the exact regeneration recognizer, exhaustive mark-pair search and scalar parity solver with correct exhaustive fallback. Its initial authentication scans every original bit. Choose p,q independently uniformly in {1,2}. After that acquisition prefix, both branch bits and D are functions of the reconstructed input, so every subsequent obligation among them has H(U_j|B_j)=0 in this global decoder convention. Across the entire record H(I|B)<=2. Four repeated claims of new branch information cannot turn this distribution into more than two bits of conditional acquisition demand.

If the decoder instead omits the prior record, Redteam's late globally-new-read record is empty and cannot recover opposite labels. A genuine cache-read event gives one bit at most, with Pi=D,b=1,h=0,rho=1. Repeatedly reusing that transition raises rho. These cases are alternatives with different declared B_j, not additive costs.

| Cost on the same A_cycle execution | Bound and qualification |
|---|---|
| Parse dimensions, extract/regenerate, authenticate all fields, reject failed source candidates | O(N³) time, O(N) span |
| Exhaustive mark discovery and failed pairs | O(k²) pairs times O(k) comparisons |
| Physical reads/writes, address bits, copies, comparisons, counters and representation changes | O(N²) transitions per comparison, retained input included |
| Parity evaluation, decision cache, high-water cleanup, relocation to origin, terminated output | O(N) additional time, O(N) maximum span |
| Complete recognized path | T=O(N³+k³N²)=O(N^(7/2)); S=O(N) |
| Physical cumulative cost | CM_phys=sum_t s_t=O(N^(9/2)) |
| Minimum-description cost | k,p,q and time replay separately give CM_min=O(T log N) |
| Failed recognition outside this family | Exact exhaustive fallback, potentially O(2^n N³); UNKNOWN is internal admission failure |
| Target production, if separately requested | Inherited O(N³) time, O(N) span |

These are symbolic implementation bounds, not fresh TM measurements. The proof decoder's scratch is not free physical scratch for A. Existing affine and matching upper bounds remain available as alternative fixed solver branches; no time from one input is multiplied by storage from another. Sequential search may reuse graphs, rows and caches, with all initialization and failed work paid.

Under a fixed cap T<=K N^a, use S=O(N^a), CM_phys=O(N^(2a)), CM_min=O(N^(a+1)) and the distinct count-map circuit ceiling O(N^a log N). For general exact decoders of records bounded by b|E_j|+h_j with overlap rho, the cap is contradicted only if the net sum of demands exceeds b rho K N^a. For inexact records, Accounting's epsilon_j=H(U_j|B_j,Pi_j) must also be subtracted. The present restricted acquisition numerator is <=N and supplies no all-exponent exclusion. No lower bound on either CM follows simply by multiplying this information demand by an unrelated peak.

The static permutation family remains an internally reviewed single-tape calibration with matching quadratic time and cubic cumulative cost; Dh<=N²/8 and Dh²<=N³/27. It is not the current dynamic construction. A counting separation alone would not settle decision P versus NP.

## Fresh searches, evidence and gates

Fresh primary queries were “conditional mutual information chain rule adaptive transcript entropy deterministic query complexity primary paper” and “Shannon 1948 conditional entropy chain rule successive choices”. Shannon's corrected 1948 BSTJ reprint, section6, finite joint/conditional identity, was checked in the [MIT primary-paper copy](https://web.mit.edu/6.441/spring05/reading/shannon1948.pdf). This is the classical identity used in the proof, not a novelty claim or imported runtime theorem. A promising [randomized query-composition paper](https://toc.cs.uchicago.edu/articles/v019a009/v019a009.pdf) failed retrieval with HTTP502; no theorem from it is imported.

Fresh GitHub query `"conditional entropy" "chain rule"` covered anthropics, openai, xai-org, google, google-research and google-deepmind. Five scopes returned no hits, xAI after one429 retry. OpenAI/math returned [06-tilted-arrays.tex at 4eaee87548250b2682affda7d05d947c05554bae](https://github.com/openai/math/blob/4eaee87548250b2682affda7d05d947c05554bae/preprints/Compatibility-entropy-and-the-spectrum-of-a-Thorp-sweep-September-26-2026/build/sections/06-tilted-arrays.tex), a search excerpt using conditional entropy for column reveals in a Thorp-sweep preprint. It supplies no compulsory SAT interface or verified source-code theorem; no deep review or import. Official scopes were checked via [Anthropic](https://github.com/anthropics), [OpenAI](https://github.com/openai), [xAI](https://x.ai/news/grok-os), [Google guidance](https://opensource.google/documentation/reference/github/where), [Google Research](https://research.google/resources/), and [DeepMind](https://github.com/google-deepmind). Bounded no-hit results do not prove absence of relevant work.

Current directive, transport and applicable T5 definitions were recovered at this snapshot; AGENTS, CODEX and repository research skill were read in this continuation. Own prior report and the five peer sources above were read, with original code/raw where relevant. Branch-name search “charged” returned no branches, not a proof that no other drafts exist. Issue324 supplied the current receiving dependencies.

No experiment was rerun: the new result is symbolic chain-rule composition. Redteam's new four-case transition raw and Construction/Discovery finite evidence retain their stated limits. A selected-file workspace is available, not a complete checkout; full repository preflight, LaTeX compilation and formal-kernel builds were not run. Only the Synthesis report and own handoff are changed by this integration.

DISJ/equality sanity PASS for the scoped ceiling, with transport explicitly preserved. Simultaneous DTISP PASS for the one-run ledger. Deterministic-configuration gate PASS as replay/description only, never a runtime lower bound. Relativization OPEN for unrestricted promotion; an oracle's unknown replies would require additional records. No Natural Proofs or algebrization bypass is claimed. Affine/Tseitin, complement, private-leaf, forced-domain, decision-witness, global preprocessing and relocation controls remain permitted.

## One next mathematical task and receiving dependencies

**DYNAMIC-LOCAL-RECURRENCE-AFTER-ACQUISITION1**, owner Bounds with Accounting: specify a model-enforced local interface whose decoder lacks information despite paid joint preprocessing, whose initial local state/endpoint is charged, and whose positive net demand is carried by actual later events with bounded reuse. Require this uniformly for each fixed correct solver under the proposed cap, not merely for a prescribed computation. A rigorous negative result is equally acceptable.

Redteam receives the explicit falsification target: erase to a scalar cache, or relocate the needed information before the proposed phase. Construction receives the constraint that clause/gate stages cannot define execution phases by fiat. Discovery receives the search for a primary theorem with exactly the offline preprocessing and local-state hypotheses. Synthesis retains the constructive alternative task of paid coverage by affine/factor methods, without claiming their connected conjunction tractable. Independent adversarial review of the new restricted lemma is requested before any promotion. Neither direction of P versus NP is resolved.
