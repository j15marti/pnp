# Zero entropy does not discharge exact verification

23 November 2026, 00:48 PST, America/Los_Angeles. PNP Charged Accounting. Named lemma **FOREST-PREDICTION-AUDIT1**, under DYNAMIC-COMPATIBILITY-OBLIGATION1. **PROVED/EXACT**, restricted source and deterministic machine as specified below. Finite evidence **COMPUTATIONAL**. Independent adversarial review pending. P versus NP **OPEN**.

The new contribution is an explicit row layout and actual checkpoint at which a growing number of indispensable source reads has zero conditional Shannon entropy under the analyzed input distribution. This is a strict limitation of treating entropy as a complete remaining-work measure. It does not refute the valid one-way entropy inequality, or the already proved signed-cycle certificate theorem. The previous single-cycle last-bit observation is amplified to a complete-graph cotree, with the physical layout rederived.

## Statement, quantifiers and falsifiers

Fix any uniform deterministic machine A correct on both labels for every valid positive Boolean exact-one triple input. It has one integer-indexed writable finite-alphabet tape, one unit-speed read-before-write head, fixed control, and terminated Boolean output at origin. All initial input, copied data, work, addresses and caches share this tape. There is no free original-source oracle or clock.

For each q>=3, use the binary-label diamond construction over K_q. Write k=q(q-1)/2 and fix the star spanning tree T={(0,v):1<=v<q}. Let I_z denote the explicit source for any z in {0,1}^k, with the reordered layout below. Fix a balanced z, meaning z_uv=x_u XOR x_v for vertex potentials. At any actual execution prefix sigma of A that has observed exactly the tree's tag signals and none of the cotree's signals, A must subsequently acquire all

r=k-q+1=(q-1)(q-2)/2

cotree tags. A may have used arbitrary paid computation, relocation, sharing and caches before sigma. The prefix condition concerns actual observations, not a demand that every solver use this schedule. More generally, every still-unobserved nonbridge must be read at any balanced prefix, by the predecessor theorem [1].

Under the uniform distribution on the 2^(q-1) balanced inputs, a replayable such prefix B determines every remaining tag. Thus H(U|B)=0 for U the cotree label vector, while T_A(I_z)-sigma>=r. A uniform scan-first algorithm reaches such a prefix on this layout; it can then finish via a fully paid polynomial guard and forest solver, with a total correct fallback outside the guard.

Four concrete falsifiers:
1. A row permutation depends on z or mixes tag owners in a field.
2. The purported prefix has already read a cotree signal, including incidental head transit.
3. A balanced-only correctness promise is silently substituted for both-label correctness.
4. A computed prediction is substituted for authenticated evidence, or a source read is charged again at every cycle.

The construction and proofs below exclude these cases. Once a correct full verdict has actually been computed and cached, no new source-read obligation is asserted.

## Source semantics and physical layout

At the pinned predecessor revision [1,2], each base edge u<v has private fibers a=q+2j,b=a+1. The five fiber matchings are identity on ua,ub,ab and the same identity/transposition tag on va,vb. Every fiber is a triangle. The diamond forces terminal color bijections f_v=f_u composed with p_uv. Consequently the binary-tag source is SAT exactly when z is a vertex-potential gradient. A sign flip on any K_q edge changes a balanced signing to an unbalanced one: that edge lies on a cycle whose parity changes. These are legal opposite-label inputs of equal length.

The star compiler gives h=3(q+2k) coloring vertices and the exact ledger

n=33q+111k, m=21q+87k,
w=ceil(log2(n+1)),
N=n+2+2 floor(log2(m+1))+3mw.

The stream consists of unary n followed by 0, gamma(m+1), and m rows of three incremented dense variable IDs, each of width w. It is positive Boolean exact-one, not strict C5/T5 counting and not a claim of adjacent Horn witnesses.

In the canonical order, the first 4h rows are independent of all tags. Every varying row has exactly one tag owner: the sorted expanded-edge slot and private ID are independent of z, and its varying destination field depends on one original edge only. The predecessor proves this from disjoint destination-fiber intervals [1]. For binary tags, every changing bit is z_e or its complement.

Apply the following **fixed row permutation**: first all tag-independent rows, then all rows owned by tree edges, then all rows owned by cotree edges, preserving canonical order inside each group. Membership is determined solely by q and the canonical edge slots. The zero-tag source and each of its k single-tag variants suffice to compute it. No truth table over 2^k signings is needed. The checker uses precisely those k+1 generators, not exponential source material. It then applies the same permutation to every signing.

Whole triples move intact, including their private IDs; declarations, clause multiset, n,m,N and semantics are unchanged. Every tag support P_e is nonempty and disjoint from the other supports. All tree supports precede all cotree supports. Each complete input remains an ordinary explicit exact-one instance. The parser may not trust the purported layout without authentication.

The compiler can emit and compare these k+1 explicit strings sequentially, retain an O(N)-entry owner/permutation table, and permute rows by direct scans. This is polynomial work in N, with O(N^2) bits a conservative storage allowance. The observed finite code is a generator audit, not a measured uniform Turing-machine compiler.

A one-tape scan-first wrapper can parse n,m and compute the public row boundary using counters and repeated computation in an already visited header area or on negative tape coordinates. It then scans only through the tree block, retaining the original source. Work-area visits never cross a cotree cell. On a family input, sigma is the transition immediately before the first cotree row. The wrapper need not announce SAT, authenticate the unseen suffix, or assume balance at this point. It subsequently completes the guard and exact decision. This shows the checkpoint is reachable uniformly; it is not forced on other algorithms.

## Actual events, decoder and opposite-label witnesses

For each e, let tau_e be the first transition scanning any original address in P_e. Before tau_e no cell in P_e can have been overwritten: writing requires reading. Any copying, caching or combining of a tag therefore includes its first signal acquisition. Every actual prefix can be replayed from public A,q,layout and its chronological first-signal payloads. The simulator resolves all same-owner source copies after receiving that payload and honors all subsequent writes and movements. This determines addresses and the full created work state. Unseen original cells remain unresolved and accessible only through real future reads.

Fix a balanced z and a cotree e unobserved at sigma. Let z^(e) flip only e. The two executions have the same prefix, including control, head, output cells, all work and every cache. Their remaining tape differences are precisely P_e, still original. Their required answers differ. If the actual continuation on z never scans P_e, the two continuations stay identical through termination, a contradiction. The sets P_e are disjoint. Assign weight one to each reachable opposite-answer difference set. Each transition can first hit at most one set, giving the justified alternative to an entropy lower bound:

T_A(I_z)-sigma >= sum_e 1 = r.

This is an explicit instantiation of the project's reachable-state hitting/packing theorem [3], with all opponents reachable at the **same** prefix time and every paid cache preserved. No virtual residual service or fixed inference graph is required. The packing potential counts unhit sets; its per-transition decrease is at most one. It reaches zero before accepting.

For the shared entropy ledger, take U=z restricted to E(K_q)\T; B=(fixed A,q,layout,balanced prior,adapted stop rule,complete prefix signal record); Pi is the chronological first cotree raw-bit record; E={tau_e:e outside T}. Under this prior every execution is accepting and must read all cotree tags, so Pi has exactly r bits. Replay identifies the owners, orientations, addresses and writes. Pi decodes U. For each fixed B the records have fixed length r, hence are prefix-free. Effective b=1, framing overhead h=0, maximum reuse rho=1. No timing or address fields are omitted from the decoder, since replay supplies them.

Fix x_0=0. Tree observations give x_v=z_0v, hence z_uv=z_0u XOR z_0v. Therefore U is already determined by B and H(U|B)=0. The entropy formula correctly yields only E[T-sigma]>=0. It cannot be reversed to infer a zero suffix cost. The alternative pointwise packing bound gives r on that same run. The solver's correctness domain still includes every unbalanced neighbor, even though the chosen probability distribution does not.

A uniform all-signings prior leaves r independent bits conditional on the same tree observations. That is a different distribution; it must not be silently substituted into the balanced expectation. A rejecting execution need not read every cotree edge. A cached full verdict after all needed acquisition can defeat all renewed source demands. No recurrence of r after such a checkpoint is proved.

## Same-execution cost ledger and cap comparison

Let L_0 be the header plus all tag-independent rows. At least the original 4h fixed rows lie there, so L_0>=header+12hw. Since 4h/m=(12q+24k)/(21q+87k)>=8/29, L_0>=N/4. Every cotree first-read event occurs at original position at least L_0. After the read-before-move transition the head remains at least L_0-1, even with erasure. With origin-anchored span charged after each transition,

CM_phys^(>sigma) >= sum_(e outside T) s_(tau_e) >= rN/4

in cell units. This charges distinct actual events, not a product of unrelated time and space maxima. Other physical transitions are additional. It is not a minimum-description lower bound.

In fact every balanced source can be generated from q and q-1 potential bits. For any fixed A, a self-delimited encoding of those data and t reconstructs its complete C_t. Hence

K(C_t|A) <= O(q+log(t+2)),

with generator and interpreter constants fixed. The time index and potentials are explicitly paid description bits, not free side information. Under polynomial time this is O(q+log N), despite the large physical span. No large minimum-description charge follows from the zero-entropy suffix.

A correct all-input solver admits this row-permuted class by the existing graph-star/diamond guard, regenerated exact row comparison and end framing. It does not use hash equality. An alternative direct K_q guard derives q=(87n-111m)/540 and k=(33m-21n)/540, validates integral ranges and k=q(q-1)/2, computes the fixed templates, checks all repeated tag copies, IDs, rows and end framing, and then checks all gradient constraints. Bounds are checked against actual available source length before allocation. On a valid guard miss the internal result is UNKNOWN and the retained original goes to exhaustive assignment decision. Invalid syntax is rejected by the declared parser, not treated as a mathematical UNSAT instance.

The previously established conservative admitted tariff remains valid with the extra polynomial row permutation: O(N^4) indexed bit work and O(N^2) stored bits, each access conservatively simulated by O(N^3) unit transitions. It covers parsing, baseline/single-toggle template discovery, row ordering, failed checks, address arithmetic, source retention, copies, work-area initialization, forest potentials, sharing, cache formation and terminated origin output. Thus T=O(N^7), S=O(N^2), CM_phys=O(N^9). CM_min=O(N^8) generally on admitted inputs, and O(N^7(q+log N)) on balanced ones by the shorter source description. These are symbolic upper bounds, not tight runtime claims. The complete fallback takes at most O(2^n N^7) time with the same O(N^2) storage allowance; it is not a polynomial guarantee on arbitrary inputs.

For fixed T<=K N^a, a>=1, retain S=O(N^a), CM_phys=O(N^(2a)), CM_min=O(N^(a+1)); count-map size O(N^a log N) is a separate counting simulation. Here r=Theta(q^2)=Theta(N/log N), and rN=Theta(N^2/log N). These demands fit the corresponding ceilings even at a=1. Zero entropy does not exclude a cap; the additional hitting bound does not exclude every polynomial exponent. Neither a general polynomial solver nor a separation follows.

## Finite evidence and limitations

[Checker](../../../experiments/dynamic_accounting_forest_prediction_20261123.py), [raw evidence](../../../results/raw/dynamic_accounting_forest_prediction_20261123.json). Run python3 experiments/dynamic_accounting_forest_prediction_20261123.py from repository root. No random seed is used.

| q | n | m | N | Valid scan traces | Balanced inputs | Compulsory cotree reads | Conditional entropy |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 | 432 | 324 | 9198 | 8 | 4 | 1 | 0 |
| 4 | 798 | 606 | 18998 | 64 | 8 | 3 | 0 |
| 5 | 1275 | 975 | 33470 | 112 | 16 | 6 | 0 |

The first two sizes exhaust all signings. At q=5 the suite covers every balanced signing and all its one-cotree-flip neighbors. Total: 184 valid physical scan traces and exact payload replays, 124 opposite-label neighbor checks, 28 singleton balanced conditional fibers, and 12 damaged-input guard misses. Every row permutation preserves the full clause multiset; every generated source matches its predicted disjoint-support superposition. The q=4 checkpoint is cell 17918; the three sample chord first reads occur at transitions 17935,18296,18470. Its full finite guard uses 37999 transitions, peak span 19000 cells and physical CM 721943002. The cached READY suffix uses three transitions including output; it makes no fresh source acquisition.

The finite fixture's counters, known-label map and lookup verdict abbreviate a finite transition table separately compiled for each tested q. These numbers are physical scan measurements for those finite machines, not a scalable O(N) algorithm. The symbolic uniform guard and its polynomial one-tape simulation were not executed. Source generators and oracle work are test-harness costs, not silently charged as constant-time uniform machine work. The checker was rerun only to restore dependency files byte-for-byte before recording their hashes; this did not introduce a second scientific experiment.

Checker SHA-256: 4038508c11143fa4a10724140d2def0d9b6f32186af128366627ed31b1badb75.
Raw SHA-256: 8040fd5c6057d327367bf2e5e4ac06347fc61a5e40ee11b2ff5328d4bd9aed61.
Dependency SHA-256 values are embedded in the raw file and match the pinned repository bytes.

No full checkout was available for preflight, and no proof-assistant kernel or general native tape parser ran. Connected reads recovered governance, the continuation/model/ceiling definitions, all six handoffs, the original Accounting and Synthesis evidence, and the relevant source/neighbor reports at 64a60d9f8dec3f5790fc72306fbf0a0eeff58941. The recursive tree request yielded no usable content; only the first 100 branch names were recovered, so no exhaustive draft-branch audit is claimed. Owner manuscripts and schedules are unchanged.

## Controls and receiving dependency

DISJ and opposite-label sanity PASS: each flipped edge gives an equal-length permitted source with opposite answer. Simultaneous DTISP PASS in the stated model: all events are on one execution. Configuration-counting PASS as an upper-description check; it supplies no runtime lower bound. Relativization/nonrelativizing progress OPEN for an unrestricted separation: no barrier-crossing step is claimed. Natural Proofs/algebrization are not invoked as positive tools.

Affine/Tseitin, complement and scalar caching remain controls. Forests have no cotree and no balance obstruction. Fixed labels or an all-balanced promise destroy the required opposite-label inputs. Private-leaf entropy, forced-domain syntax, prescribed witness DAGs and repeated cycle descriptions provide no extra charges. Unlike the permutation transport family, this row layout has its own physical proof. Its costs are not added to costs from other inputs.

**Next owner Bounds, copied to Synthesis:** maintain the pair (conditional entropy, reachable opposite-answer packing), rather than identify either with total residual runtime. The first open premise is a family in which an independently established computational obligation survives after all original-source difference sets have been hit. This example supplies no such post-acquisition recurrence.

**Redteam target:** try a reachable balanced prefix with exactly the tree signals acquired but a cache that distinguishes an unobserved cotree flip. Either exhibit a hidden earlier signal access or falsify the disjoint-support replay proof. A verified full-verdict cache after the chord checks remains a legal bypass and should not be challenged as an error.

## Literature and official-repository search record

The fresh literature query was "graph property testing signed graph balance query complexity spanning tree certificates parity constraints". It located Florian Adriaens and Simon Apers, *Testing properties of signed graphs*, arXiv:2102.07587v1, 15 February 2021, [primary PDF](https://arxiv.org/pdf/2102.07587), read at §§1.1 and 2.2. Its balance tester distinguishes balance from epsilon-far inputs in signed graph query models with permitted error; it does not certify every one-edge defect. The gradient characterization matches our control. No sublinear exact solver is imported. The theorem above is proved directly from legal neighboring sources. The discovery handoff should audit this exact-versus-testing transfer.

Fresh owner-scoped searches used:
- site:github.com/anthropics SAT certificate formal verification
- site:github.com/openai decision tree query complexity theorem proving
- site:github.com/xai-org SAT solver formal verification, then site:github.com/xai-org "graph" "proof"
- site:github.com/google/or-tools parity constraints graph SAT
- site:github.com/google-research signed graph balance, then site:github.com/google-research/google-research "signed" "graph"
- site:github.com/google-deepmind graph algorithm CLRS

Ownership checks used the verified [Anthropic](https://github.com/anthropics) and [OpenAI](https://github.com/openai) profiles; the [xAI release](https://x.ai/news/grok-os) links xai-org; [Google's organization guidance](https://opensource.google/documentation/reference/github/where), [Google Research resources](https://research.google/resources/), and the owner profiles/linked publisher domains identify the Google namespaces. Google Research and DeepMind profiles did not display a Verified badge in the retrieved text; publisher identity was checked through their linked domains and project references rather than claiming such a badge.

| Inspected repository file | Commit | Exact relevance |
|---|---|---|
| anthropics/formal-math, eth/README.md | 16a5ce41304fcdaea4e0be7c132e1c361dc26da5 | Advertises a subexponential counting/decision result. Its proof/kernel was not rebuilt and its claim is not imported. That advertised bound alone is not polynomial. Same pin as prior search, so no redundant deep review. |
| openai/miniF2F, README.md | 4e433ff5cadff23f9911a2bb5bbab2d351ce5554 | Formal theorem benchmark, no applicable exact-event theorem in inspected file. Search also surfaced math preprints, not audited or imported here. |
| xai-org/grok-1, README.md | 7050ed204b8206bb8645c7b7bbef7252f79561b0 | Model inference code. No relevant certificate/verification algorithm found in the bounded search. Unrelated "proof" hits were rejected. |
| google/or-tools, ortools/sat/README.md | 4782dbd0aa85621c8115cf33de1574a2e6757004 | Describes SAT, XOR and other constraint propagators, useful algorithmic controls; no uniform polynomial SAT or arbitrary-solver lower bound follows. |
| google-research/google-research, README.md | 87e25a5ba04d2c4cf0108f0cec96d648fe2b945a | Project collection; graph-learning search hits did not establish exact source-verification guarantees. |
| google-deepmind/clrs, README.md | 6d5728b9efadf8648413c8c473929a733caacced | Selected algorithm traces cannot prescribe an arbitrary decider's execution. |

These were bounded searches, not exhaustive absence claims. No vendor code was executed or used as a mathematical proof.

[1] [Accounting signed-cycle source ledger](https://github.com/j15marti/pnp/blob/64a60d9f8dec3f5790fc72306fbf0a0eeff58941/research/agents/charged-accounting/PNP_Charged_accounting_2026-11-23_002255_Signed_Cycle_Source_Ledger.md), plus its exact executable evidence. This predecessor already proves mandatory nonbridge reads and the single-cycle last-bit phenomenon.
[2] [Synthesis diamond networks](https://github.com/j15marti/pnp/blob/bf8e52241a80da97365fe86c6985c3ab15b991d9/research/agents/charged-synthesis/PNP_Charged_synthesis_2026-11-22_122415_Diamond_Networks.md). Source generator blobs c55318ded56c5c13a4352b05570302e945d3d000 and de5421f5fa9954cd9c1ca2043962a4c8c8f4a351.
[3] [Reachable-state local obligations](https://github.com/j15marti/pnp/blob/64a60d9f8dec3f5790fc72306fbf0a0eeff58941/research/main/Postprocessing_Local_Obligations_and_Safe_Merging_2026-11-21.md), §§2–8. The concrete disjoint raw-source opponents instantiate, rather than replace, its conditional snapshot theorem.
[4] [Sign-certificate acquisition](https://github.com/j15marti/pnp/blob/64a60d9f8dec3f5790fc72306fbf0a0eeff58941/research/main/Sign_Certificate_Exact_Acquisition_2026-11-22.md). Independent occurrence signs are a different input contract; no strict T5 transfer is asserted.
