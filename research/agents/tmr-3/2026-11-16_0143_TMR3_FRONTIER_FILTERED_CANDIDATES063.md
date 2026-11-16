# TMR-3/063: source-indexed frontier filtering before canonical candidate verification

**November 16, 2026, 01:43 PST.** TMR-3 / PNP Time-Space Tradeoffs, Track B. **PROVED/EXACT in the specified conditional restricted model, independent mathematical review OPEN.** Finite independently executed V8 checks are COMPUTATIONAL, not a native multitape run. **P versus NP OPEN.**

## Selected dependency, quantifiers, and falsifiers

**C3-FRONTIER-FILTERED-CANDIDATE-VERIFIER.** For every fixed total deterministic finite-alphabet p-work-tape Turing machine M and every original-source input x of length N in a declared authenticated domain, assume a known b-step block-respecting, padded t=bB execution; a fixed uniform indexed candidate-block provider G(x,c,h,j) for candidate c in [K], tape h in [p], stage j in [B]; and an explicit frontier threshold W. G is physically executable, uses at most a writable bits and at most tau bit-machine steps per call **including all original-source seeks and restoration**, and produces a block index in O(log(t+2)) bits. Acquisition of K,b,B,W and source validation is charged separately. **Promised coverage:** at least one candidate equals the authentic complete sequence of active work-tape blocks; the authentic candidate's source-graph future-live width is <=W. Candidate words may otherwise be arbitrarily wrong or have arbitrarily high frontier width.

Construct one deterministic source-to-Boolean-output simulator with no guessed checkpoints: authenticate x; screen EACH candidate's frontier without allocating its tapes; skip high-width words; on a passing candidate, simulate M from blank and check all claimed active blocks, using only future-live tape blocks; emit the genuine accept/reject label on the first passing complete execution. If the coverage promise is violated, the procedure may emit FAIL; it is not presented as an unrestricted all-machine decider.

**Falsifiers fixed before primary-source/corpus audit:** (1) an enormous-frontier false candidate might force tape allocation before detection; (2) a wrong future may discard a block needed before the first detected discrepancy; (3) detecting distinct future-live identities might need the entire guessed word in memory; (4) candidate enumeration/selection might hide an input-dependent answer oracle. The theorem closes (1)-(3) for the declared interface and forbids (4) by charging G. It does not construct a polynomial K or small W for all converted machines.

## Named original source and integration point

Williams, *Simulating Time With Square-Root Space*, arXiv:2502.17779v1, Section 3.2, especially its block movement encoding (equation (1)), Claims 3.4-3.5 and computation graph enumeration/FAIL construction, https://arxiv.org/html/2502.17779v1 . In that work the guessed trit movement word has O(B) bits and can be enumerated without predicting its authentic value. TMR-3/058 supplies a conditional source-indexed frontier storage evaluator; /061 flags exhaustive graph-guess cost; /062 demonstrates a two-word source-independent candidate family with P-complete authentic selection. This /063 lemma combines the **source-indexed candidate verifier** and the **width guard** without incorrectly assuming every false candidate is cheap to store. No general nonassociative Cook-Mertz speedup is asserted.

For indexing a trit word m(h,j) rather than a direct block-ID word, derive G by the paid prefix sum block(h,j)=1+sum_{r<j}m(h,r); a query may use O(B) trit-generator calls, O(log t) extra bits, and must include that cost in tau. A claimed random-access O(1)-cost block index is not silently imported.

## Frontier screen: no candidate tape cache needed

For candidate c define the array z_c(h,j)=G(x,c,h,j), with j=0,...,B-1. Its after-stage-j future-live set is

F_j(c)={(h,z_c(h,i)): 0<=i<=j, exists r>j with z_c(h,r)=z_c(h,i)}.

Let w(c)=max_j |F_j(c)|. A deterministic screen computes w(c)<=W using only loop indices and a counter:

For j=0,...,B-1, and each h and i<=j, set a=z_c(h,i). First scan r<i to see if this (h,a) was already seen. If yes, do not count it again. Otherwise scan r>j; increment the live count iff a appears again. If the live count exceeds W, immediately skip this candidate. No dictionary, guessed tape contents, candidate array or saved graph is used by this screen. Every G result is authenticated only as a candidate description, not as an actual machine trace.

There are p*sum_j(j+1)=pB(B+1)/2 representative iterations. Each iteration calls G at most 1+i+(B-1-j)<=B times. Hence a conservative **exact count upper bound** is

Q_screen <= p B^2(B+1)/2,

and screen time <= O(p B^3 tau) plus paid O(p B^3 log(t+2)) comparisons and loop arithmetic. Its live writable storage is O(a+log(K+t+N+W+2)). If G returns a malformed index outside the possible tape range, or a nonadjacent jump, reject the candidate in the same logarithmic space before simulation. The authenticated candidate is guaranteed to satisfy these necessary conditions.

## Blank-start future-live simulation and correctness

For a candidate that passes, begin M anew with blank work tapes and the authentic read-only source x. At stage j compare the actual current head-block index with z_c(h,j) for each work tape h **before accessing guessed block contents**. On mismatch return FAIL and discard the candidate's cache. On agreement load each active b-cell block from a sequential dictionary if retained; otherwise use all blanks. Execute the next b local transitions of the *actual* fixed M, updating its true finite control, input-head position, per-tape offsets and currently active block contents. Detect all illegal mid-stage block crossings and reject the candidate. At the stage boundary check the next claimed block index.

After the stage, retain a modified active block (h,a) exactly when a future z_c(h,r)=a exists for some r>j. Other retained entries remain until their genuine next access. No arbitrary checkpoint tape is preloaded. At most w(c) future-live blocks plus p currently active blocks are resident at any point. At most pB(B-1)/2 future G calls are needed for retention checks, plus O(pB) calls for current/next labels. With a sequential dictionary, a conservative processing cost is O(t log(t+2)+pB(W+p)(b+log(t+2))+pB^2(tau+log(t+2))) for one candidate, including head/address arithmetic, source-head operations, copying and saved block identities.

**Prefix invariant:** until the first discrepancy between the candidate and the actual block trace, all simulated state and tape cells needed by the current block equal the canonical execution. If a previously touched block is discarded after stage i because the candidate has no future occurrence of (h,a), the actual execution cannot revisit that block before the first discrepancy: any such revisit at stage r would require z_c(h,r)=a if earlier candidate stages were still correct, contradicting the discard condition. Thus false suffix predictions cannot corrupt the pre-mismatch prefix. An all-matching candidate consequently produces the true accept/reject bit. The authentic word has width <=W, so its screen passes and its simulation succeeds. No false candidate can return an incorrect Boolean answer. Any multiple successful candidates describe the same unique authentic trace.

## One SAME realization: time, queries and peak space

Let A(N),s_A(N) be original-input authentication time and writable workspace; let K be the actual (paid) number of candidates and G have tau,a as above; let p be fixed. The single deterministic procedure consisting of authentication, K sequential screen/simulation attempts, source head repositioning and final output has the conservative bounds

Q_G <= K*p*(B^2(B+1)/2+B(B-1)/2+O(B)) = O(K p B^3),

T_all = O(A(N)+K[pB^3(tau+log(t+2)) + t log(t+2)
             +pB(W+p)(b+log(t+2))+N+(W+p)b]),

S_peak = O(s_A(N)+a+(W+p)(b+log(t+2))
              +log(K+t+N+W+2)).

Terms are sequential partitions, not free parallel processors. The screen and candidate replay reuse their workspace; the bound includes temporary current blocks, source seeks, oracle-free candidate construction, failure attempts, dictionary search, retention, output and parameters. The source itself resides on a read-only input tape and is not counted as writable memory. If the source must be copied or is modified, its physical storage must be added.

For b=Theta(t^(1/3)), W=O(1), fixed p and logspace/polytime G, the restricted construction uses O(t^(1/3) polylog(t+N)) writable bits and at most polynomial-in-t time for polynomial K (the O(K p (t/b)^3 tau)=O(K t^2 tau) screen dominates). **This is NOT a theorem about all TIME[t] machines.** It assumes source-indexed polynomial candidate coverage AND constant frontier width, neither provided by general HPV/Williams conversion. The improved nonassociative Tree Evaluation height term remains OPEN. If an evaluator makes additional Q graph-node requests, each G-derived graph-edge query costs O(pB tau), and every canonical work-bit request must include a real replay or another separately proved provider. No uncharged Q-dependent term is omitted.

## Hostile controls and mandated gates

The rank-2^k DISJ_k example has linear-size depth-two unbounded-fan-in circuits; this width-guard algorithm makes no rank-to-general-circuit inference. Equality, affine/Gaussian, Horn, 2-SAT, bounded treewidth, autarky, product, selector, unique assignment, auxiliary wires, padding and simple direct algorithms remain legitimate. Width is a property of the selected realization, not an invariant of equivalent programs, and no normalization is asserted to preserve W. Graph enumeration may be exponential; a low-K premise is not a theorem. /341 FAIL as full UNSAT authority; /386 RESTRICTED.

| Gate | Verdict |
|---|---|
| DISJ sanity | PASS restricted: no rank-to-runtime or all-circuit claim. |
| Relativization | NOT APPLICABLE WITH REASON to a separation; no separation claimed. A nonrelativizing NP bridge, algebrization and Natural Proofs audit remain OPEN. |
| Simultaneous DTISP | PASS for the specified source/candidate/frontier-promised simulator with ALL costs above; unrestricted TIME[t] and SAT transfer OPEN. |
| Configuration counting | PASS as deterministic upper-bound consistency only, T<=2^O(S+log N) on a total read-only-source machine; no work lower bound and no randomized/quantum extrapolation. |

## Reproducibility and limits

Executable: experiments/tmr/tmr3_frontier_guard063.js, revision tmr3-frontier-guard063-v1, deterministic exhaustive (seed null). Immutable results: results/raw/tmr/2026-11-16_0143_TMR3_FRONTIER_GUARD063_NODE_RAW.json. Exact executed V8 audit: 496 unary-length-authenticated source words, 1,488 malformed controls, 9,920 candidate attempts, 6,208 width-filtered attempts, 2,224 failed candidate comparisons and 1,488 correctly accepting simulations; 154,960 assertions, zero failures. Four public candidate block words per source, all adjacent-block transitions, two genuine words selected by source bits; exhaustive W=0,...,4, B=4,...,8. Matched direct store-all execution and exhaustive frontier set enumeration are independent controls. The executable materializes arrays and dictionaries, so it does NOT empirically measure low-space machine usage. No native b-step Turing-machine transition table, general HPV converter, Cook-Mertz program, full repository checkout/preflight, LaTeX build or independent mathematical proof review was executed in this run. The symbolic resource lemma is separate from finite testing.

## ONE next load-bearing lemma

**C3-CANDIDATE-COVERAGE-UNDER-A-PINNED-CONVERTER**: for the exact compiler/graph evaluator intended to improve Williams, prove or falsify a source-obtainable family of K=poly(N+t) candidate block words containing the authentic one on every valid original source, with an authentic W bound below t/b and charged query time tau. The present lemma conditions on coverage and width; it does NOT create them, and it does not prove a generic height-sublinear nonassociative Tree Evaluation algorithm.
