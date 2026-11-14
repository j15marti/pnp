# TMR-3/020: hybrid configuration-versus-local-visibility INDEX tradeoff and sensing-head redteam

**Pacific timestamp:** 2026-11-14 07:31 PST, America/Los_Angeles.
**Role:** TMR-3, NEW PNP Time-Space Tradeoffs.
**New result:** TMR3-HCL20, CANDIDATE/RESTRICTED pending TMR-1/TMR-5 peer review.
**Independent peer audit:** favorable for TMR-1/021's collision-sensing falsifier and clipped-separation repair, in the expressly restricted model.
**Executed evidence:** COMPUTATIONAL, hosted V8. **Unrestricted 3-SAT bottleneck and P versus NP:** OPEN.

## 1. A same-program, same-source hybrid information bound

Fix ONE finite, deterministic, total, uniform two-phase exact INDEX machine A, serving every length. The original L-bit source x is immutable, between physical endmarkers, with r >= 1 independently moving nonsensing source heads on independent identical read-only source tapes. The machine has w >= 0 distinct ordinary work tapes, each with one locally moving head, fixed finite alphabet Gamma of cardinality at most g >= 2 (including blank), each head initially at its fixed origin, and q finite-control states. Every head displacement is at most one cell per charged transition. Work heads cannot sense their absolute numerical coordinates. Every original-source and writable-tape movement, write, index read, auxiliary counter, output and recomputation is charged. No unit-cost random access, oracle, unbounded-word operation, or uncharged advice is available.

First A preprocesses x without access to the future request. The preprocessing phase may use unbounded *finite* time and space. Then a binary index p in {1,...,L} is delivered on an independent read-only query tape whose physical initial state depends on p but not on x. A must output exactly x[p] and halt for every (x,p). The time t is a bound on the **entire second phase**, including reading p and final output, for all x in the source set specified below and all p.

For arbitrary X subset of {0,1}^L, suppose the *actual preprocessing run* of A on every x in X visits at most s writable cells in total, counting the complete intervals traversed on ALL work tapes. The machine, control table, tapes and alphabets are fixed independent of x, L and p.

**TMR3-HCL20 (restricted hybrid lemma):**

$$
\boxed{
|X|\le q (L+2t+4)^r 2^{r(2t+1)}
\min\!\left\{
(2s+3)^{3w}g^s,\,
(g+1)^{w(2t+1)}
\right\}.}
\tag{HCL20}
$$

The same fixed machine realizes both the preprocessing-space and query-time bounds on each member of X. This is NOT a bound obtained by combining unrelated algorithms or unrelated hard inputs. No restriction on the magnitude of s is needed for the local-visibility branch. If X is all 2^L source strings, the corresponding lower bounds follow for the all-input maxima of this one A.

## 2. Proof, including complete adaptive work-tape replay

For a completed preprocessing execution on x, retain its finite control state, its r original-source head positions and the physical source windows of radius t centered there. For each original-source head, record its exact coordinate if it lies in [-t,L+1+t], otherwise a FAR-LEFT or FAR-RIGHT class. There are at most L+2t+4 positional classes, and for a fixed class at most 2t+1 genuinely variable binary original-source cells; endmarkers and outside blanks are fixed. The r-source-part fingerprint has at most

$$
P(L,t)=(L+2t+4)^r 2^{r(2t+1)}
$$

possibilities. Coordinates outside the window are not numerically inspected by the model and the far classes are physically indistinguishable for the next t transitions.

Now separately count the x-dependent *work portion* of the query-boundary fingerprint in two valid ways.

**Global-space count:** On any source x in X, each visited work-tape interval is contiguous and contains the fixed starting origin. With at most s cells visited overall, each tape's visited endpoints and final head position have at most (2s+3)^3 choices. The actual written symbols have at most g^s choices across all tapes. Therefore the number of complete retained work configurations is at most

$$
W_{\rm global}(s)=(2s+3)^{3w}g^s.
$$

This counts all preprocessor-produced caches, index representations, stacks, tapes, and head locations. A given complete work configuration uniquely determines the t-local work symbols because all outside visited cells remain blank.

**Local-visibility count:** Instead ignore inaccessible global work contents. Retain exactly the 2t+1 physically reachable pre-query symbols around each of the w work heads, with an extra fixed boundary sentinel if applicable. There are at most

$$
W_{\rm local}(t)=(g+1)^{w(2t+1)}
$$

possibilities. No bound on the number of OTHER written, retained or visited cells is assumed in this count.

The set of possible local work views is an image of the actual global work-configuration set, so its cardinality is bounded by **both** W_global(s) and W_local(t). The q-valued control is counted once, not once per alternative estimate. Combining independently with the source part yields at most q P(L,t) min{W_global,W_local} joint fingerprints.

If two distinct inputs x,y in X shared a fingerprint, give them the **same p**. At query step 0, the controller, paid query tape, original-source symbols under every source head and work symbols under every work head coincide. By induction, every local read, deterministic choice, write, movement, repeated read, collision-free control transition, and terminal label coincides for all steps through t. Every actual head remains within its own original radius-t window, and corresponding relative writes on distinct work tapes reproduce the same later symbols. A fixed work boundary is represented by the sentinel. Thus the entire two-phase query continuation has the same output for x and y, for EVERY p. Choosing a position at which x and y differ contradicts exact INDEX correctness. The fingerprint map is injective on X, yielding HCL20.

The result also gives a **same-input existential witness**: if a proposed s,t violate the inequality for a set X whose actual preprocessing space is uniformly <= s, at least one x in THAT set and one p have post-query time >t. No separate time-witness and space-witness are spliced together. On that witness the actual preprocessing visited cells remain <=s, while its query execution may visit additional cells; peak full-run space and time must be charged as realized.

## 3. Quantitative regimes, and what is *not* excluded

Taking binary logarithms for X={0,1}^L:

$$
L\le \log_2 q +r\log_2(L+2t+4)+r(2t+1)+
\min\left\{
3w\log_2(2s+3)+s\log_2g,\,
w(2t+1)\log_2(g+1)
\right\}.
\tag{HCL20-log}
$$

If the all-input preprocessing-space upper bound satisfies s(L)=sigma L+o(L) for finite sigma>=0, any all-input post-query bound satisfies, with D=r+w log_2(g+1),

$$
\liminf_{L\to\infty}\frac{t(L)}{L}\ge
\max\!\left\{
\frac{(1-\sigma\log_2g)_+}{2r},
\frac{1}{2D}
\right\}.
\tag{HCL20-regimes}
$$

For s=o(L) this gives (1/(2r)-o(1))L. For s=Theta(L) beyond the information-carrying work capacity, the strictly positive local-view term remains. For arbitrarily large or exponential s, only the local-view term is asserted. These bounds rule out sublinear delayed INDEX query time on the defined locally moving finite-head architecture, but permit arbitrary polynomial-time processing, including a complete-source copy and polynomial-time retrieval.

This is a *new joint formulation* from the distinct global retained-configuration counting of TMR-1/020 / TMR-3/018 and the actual local work-cell visibility of TMR-3/019. The min combines two bounds on the SAME set of retained work views, so no independent hard witnesses are combined. Its strength is interpolation and explicit witness scope, not a new exponent or an unrestricted SAT theorem.

**Precise missing bridge:** A general uniform deterministic 3-SAT decider need not accept a subsequently supplied adversarial arbitrary bit index, and correctness of its one-bit SAT/UNSAT output does not imply an INDEX service. The L-bit input and a polynomial-size algebraic global invariant can support one-bit classification without retrieving each coordinate on demand. There is no proved polynomial-preserving reduction from all arbitrary SAT deciders to this delayed interface, and even such a transfer would yield only a linear INDEX lower bound, far short of a lower bound exceeding every polynomial. The all-machine, all-k, arbitrary-polynomial-workspace SAT lower bound remains OPEN.

## 4. Independent TMR-1/021 sensing-head audit

The TMR-3/019 proof explicitly uses nonsensing one-head-per-work-tape semantics. TMR-1/021 correctly identifies a different model where two heads share a physical tape and the finite controller can test whether they coincide. With all cells blank, heads (0,0) versus (0,1) have equal separate radius-one symbol windows, yet the one-step collision predicate differs. A naive symbol-only quotient is FALSIFIED on that larger model. An independently coded counterexample in the executable accompanying this report reproduced that result.

The proposed repair in TMR-1/021 retains signed head separation when within 2t and FAR-LEFT/FAR-RIGHT otherwise. This is sufficient for collision replay: two initially distant heads cannot meet or have overlapping write/read locations in t local steps, and for near heads the relative displacement at every step is determined by their matched moves. Thus the finite clipped geometry restores inductive matching, including source reads and simultaneous deterministic work writes, under TMR-1's exact collision-sensor restrictions. This is a favorable independent **restricted symbolic proof audit**, not an all-machine compiler and not a claim that arbitrary constant-time distance tests are legal. Generalization of HCL20 to sensing shared tapes would require the explicit geometry factor (4t+3)^H and an appropriately enumerated global-work bound; the above HCL20 is deliberately confined to the nonsensing model.

## 5. Actual execution, raw controls and reproducibility

The published exact JavaScript was run directly in hosted V8 with deterministic finite source generation, not through a native Node process. It builds concrete post-preprocessing tape-content and head-location fixtures, groups matching complete t-local fingerprints, chooses a differing bit position, and replays an independent, adaptive *physically current-cell* query controller for each opposite source and several matching indices. The controller charges simulated local reads, single-cell writes, independent source/work-head moves, query-tape reads and terminal outputs. The fixture preprocessor is symbolic host code, NOT a physically charged general Turing-machine compiler; the symbolic all-length lemma supplies the proof.

L=3..9, seven fixtures (blank, parity, copy, cumulative XOR, reverse copy, centered source, far input-dependent coordinates), t=0..3. Results: 196 cases; 84 with aggregate work-footprint cap <=L; the global-space count branch smaller in 42 cases and the local-view branch smaller/equal in 154; 2,732 collision pairs; 10,198 paired index-query traces and 18,282 corresponding local transitions; 84 far-source and 1,356 copy/XOR/reversal collision cases; one independent sensing-head collision counterexample; zero failures. The tests expose both retained-space and local-view regimes. Finite results are COMPUTATIONAL, not an arbitrary-TM proof.

**Published exact executable:** experiments/tmr/tmr3_hybrid_worklocal020.cjs, Git blob 6797f2571336340c9b02b17ffc9f221512c725a6.
**Published immutable raw output:** results/raw/tmr/2026-11-14_0731_TMR3_HYBRID_WORKLOCAL020_RAW.json, Git blob 45bf1f490b1d5913deb20ee59b1b92236c0462bd.
**Reproduce:** node experiments/tmr/tmr3_hybrid_worklocal020.cjs.

## 6. Primary model references and research ledger

[1] Fortnow, Lipton, van Melkebeek and Viglas, *Time-Space Lower Bounds for Satisfiability*, Journal of the ACM 52(6), 835-865 (2005), https://doi.org/10.1145/1101821.1101822 . Its theorem excludes simultaneous deterministic random-access SAT time n^c and sufficiently small n^d space for every c below the golden ratio. It does **not** exclude all polynomial workspace and does not prove this INDEX lemma.

[2] Fischer, Meyer and Rosenberg, *Real-Time Simulation of Multihead Tape Units*, Journal of the ACM (1972), primary abstract https://research.ibm.com/publications/real-time-simulation-of-multihead-tape-units . Multihead simulation is model-specific; no simulation theorem is used as a free reduction in HCL20.

[3] Miltersen, Nisan, Safra and Wigderson, *On Data Structures and Asymmetric Communication Complexity*, JCSS 57(1), 37-49 (1998), https://doi.org/10.1006/jcss.1998.1577 . Its cell-probe/communication model is not identical to physically moving tape heads; no lower bound is transferred without proof.

[4] Borodin and Cook, *A Time-Space Tradeoff for Sorting on a General Sequential Model of Computation*, SIAM J. Comput. 11(2), 287-297 (1982), https://doi.org/10.1137/0211022 . Sorting time-space bounds do not provide the missing SAT decision transfer.

**Required corpus read:** replacement directive SHA 47459817e66dccf1f3079e6c724c0fd2643e7bc4 first and rechecked before shared writes. Full root proof1.txt, 28,714 characters, SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343. Full proof2.txt recovered from authentic Git blob, 1,051,196 characters, SHA 930c5eeddafce656717f28055a7a9a755f44737c, despite blank file endpoint. Full canonical main.tex recovered from Git blob, 2,539,489 characters, SHA f80790efd768574555a85703a14820e1bed56b70, despite blank file endpoint. Root AGENTS.md, CODEX.md, pnp-research skill, latest issue #3 through TMR-1/021, five current TMR handoffs and original TMR-3/018, TMR-3/019, TMR-1/021, TMR-2/020 and TMR-5/018 evidence reviewed. Historical FLMV/ARC restrictions remain intact; older LSPV allocation instructions are superseded.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** No root tracker or root main.tex edits. No scheduled tasks changed.

**Next peer target:** TMR-1/TMR-5 independently check the hybrid min count and all-transition coupling, including work-tape boundary sentinels and source-dependent far head locations. TMR-2 and TMR-4 should test any claimed SAT-to-delayed-INDEX transfer against cheap compact invariants and full all-step machine simulation. A superpolynomial unrestricted SAT bottleneck is OPEN.

END_OF_REPORT::TMR-3::020::2026-11-14_0731_PST
