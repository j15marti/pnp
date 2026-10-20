# CHMY Threshold Bridge 34: fiber cancellation and seed/locality feasibility

**Research date:** 2026-10-21, Asia/Seoul.  **Scope:** CHMY-to-OPS/MMW model-correct magnification.  **Overall:** proposed direct lift FAIL; genuinely matched magnification OPEN.  **P versus NP OPEN.**

## 1. Preregistered constructions, before literature

Frozen file `00_PRELITERATURE_PROPOSALS.md` records four ideas before the original articles were opened in this run:

(A) Strengthen the promise and exploit slack between the CHMY source lower-bound exponent and source YES circuit-size exponent before a circuit-complexity-preserving length expansion.

(B) Lift the *actual* Forbes–Kelley/CHMY seeded generator distribution through the Bridge33 `E_r` encoding, with uniform hidden seed. Test pseudorandomness without replacing that generator with a synthetic mask.

(C) Maintain a single global circuit witness across two MMW Stream-Merge updates while translating the search interface into short, ordinary decision queries, charging all retained state.

(D) Investigate whether CHMY branching-program bounds can directly match OPS's nonuniform circuit hypothesis, with model conversion explicitly shown.

This run developed (A) and (B) with a universal image theorem, an exact executable falsifier, and a rational parameter audit. (C) and (D) remain candidate directions, not claimed constructions.

## 2. Exact original-paper contracts

**CHMY [1], Theorem 16:** For any oracle language `O`, each fixed `1/2<mu'<mu<1`, and truth-table length `N=2^n`, ordinary exact `MCSP[N^mu]` cannot be decided in time `N^{2(mu'-o(1))}` by a randomized, **one-way read-only input plus ONE two-way read/write work-tape** machine with two-sided error at most `1/3` and oracle queries of length `N^{o(1)}`. YES means circuit size at most `N^mu`; NO means larger. CHMY Corollary 23 gives a *local*, uniformly seeded Forbes–Kelley-derived PRG `G_N:{0,1}^sigma->{0,1}^N` that fools the stated model, with

`sigma = ~O((sqrt(T)+log(1/epsilon))*log(q*2^ell*T))`.

Every `G_N(z)` has circuit size at most its seed length, by the paper's definition of local. For `epsilon=1/6`, the published generator distinguishes neither label of a putative correct target decider; the theorem uses the independent **uniform** random seed `Z` (hidden from the decider), and independent machine coins `R`. The generator itself was **not numerically instantiated** during this run. The new counterexample is universally quantified over *every* possible source truth table `f`, so it holds for every actual output `G_N(z)`, not for an arbitrary-mask surrogate.

The exact MCSP lower bound is not automatically an OPS result. The stronger **GapMCSP** promise `CC(f)<=N^theta/(c log N)` versus `CC(f)>=N^theta` follows by applying the same local-PRG proof only when the generator seed is below the *smaller* YES cutoff and random functions exceed the NO cutoff; this is a derived, restricted-model extension, not a restatement of CHMY Theorem 16.

**OPS [2], Theorem 1.4:** A universal `c>=1` exists such that if for some `eps>0` and **every sufficiently small beta>0**, `GapMCSP[N^beta/(c log N),N^beta]` requires **nonuniform** circuits exceeding `N^{1+eps}`, then `NP` is not contained in polynomial-size circuits. CHMY's high-beta, randomized one-work-tape lower bound does not supply this premise.

**MMW [3], Theorem 4.2:** Ordinary indexed-program `MKTP[p]`, `p>=log N`, admits a streaming algorithm with `O(Np)` time, `O(p)` space and ordinary `Sigma_3 SAT` oracle queries of `O(p)` bits in its stated oracle-cost model. This does not by itself construct a SAT-to-MKTP reduction or a short-query, one-tape CHMY transfer.

## 3. New exact obstruction: public-fiber two-bit distinguisher

Let `M>N` and consider *any public bit-selection-plus-mask embedding*

`E(f)_i = f_{pi(i)} XOR h(i)`, `i=0,...,M-1`,

where `pi:[M]->[N]` and `h:[M]->{0,1}` are fixed independently of source `f` and the original CHMY seed. By pigeonhole, among the first `N+1` output indices there are `a<b<=N` such that `pi(a)=pi(b)`. Hence, **for every** `f`,

`E(f)_a XOR E(f)_b = h(a) XOR h(b)`.

A concrete one-way-input finite-state tester stores the output bit at position `a`, skips to `b`, and checks this parity. It reads at most `N+1` target bits, uses **zero work-tape cells, zero randomness, zero oracle queries and no seed or source-dependent advice**, and accepts `E(f)` with probability **one**. It accepts a uniform independent `M`-bit string with probability exactly **1/2**.

The tester can be made a finite-state machine with `q=O(N)` states for any fixed public `pi,h` at each input length (the nonuniform `q`-state setting expressly allowed in CHMY Corollary 23). For the specific Bridge33 encoder, below, a fixed-state *uniform* tester suffices. This does not rule out seed-dependent reindexing or a fundamentally different high-distance code; those require new charged semantics and a genuine one-work-tape simulation.

**Conclusion (proved):** A direct lift `G'_M(z)=E(G_N(z))` cannot be an `epsilon<1/2` PRG for the original CHMY **target-length uniform distribution** whenever `E` has the stated public bit-selection form. The statement holds for the actual CHMY `G_N` without instantiating its internal construction, because the parity identity holds for every `f=G_N(z)` and every seed `z`.

This does **not** contradict the CHMY theorem: the original PRG distinguishes `G_N(U_sigma)` from `U_N`, whereas the lifted proof would need `E(G_N(U_sigma))` to fool testers against **`U_M`**. The correct pushforward comparison is `E(G_N(U_sigma))` versus `E(U_N)`, and a bound for that comparison additionally requires an explicitly model-correct one-tape simulator.

### Original Bridge33 encoder: a constant-time counterexample

Let `N=2^n`, `M=N^2`, `n>=3`, with target serialized in `x`-major, `y`-minor binary order:

`E(f)(x,y)= f(x) XOR ( y_0 AND (x_0 XOR y_1) )`.

For each fixed `x`, the mask ignores the last `y` coordinate. In particular, the first eight target bits consist of four equal consecutive pairs. A deterministic one-way-input, no-work-tape machine reads exactly eight bits and accepts iff `bit[2j]=bit[2j+1]` for `j=0,1,2,3`. Every `E(f)` is accepted. For `U_M`, four independent equality constraints hold with probability `2^-4=1/16`. Distinguishing advantage is **15/16**, far above the CHMY PRG security target `epsilon=1/6`, in *the actual one-work-tape model*.

For the original `E`, restriction `y=0` recovers `f`, and an explicit nine-gate AND/OR/NOT extension gives `CC(f)<=CC(E(f))<=CC(f)+9`. These circuit bounds remain correct. Their correctness **does not** make `E(U_N)` uniform on `M` bits. Indeed, since `E` is injective, the exact information-theoretic distance is

`TV(E(U_N),U_M)=1-2^{N-M}`.

Our distinguisher is stronger for the target PRG claim because it runs in eight input moves, not an exponential-membership test.

### Public masks cannot fix the failure

For any public `h(x,y)`, fixed `x` gives `E(f)(x,y) XOR E(f)(x,y') = h(x,y) XOR h(x,y')`. Replacing the original mask by `parity(y)` or by a nonlinear source-independent public mask changes the parity expected by the tester but does not remove the two-point relation. Four exact public masks were tested. A public output permutation can delay the first repeated source index, but a public bit-selection embedding has a collision among the first `N+1` emitted bits, yielding the earlier lemma.

**First failed arrow for construction (B):** `G_N` fools one-tape tests against `U_N` **does not imply** `E(G_N)` fools the same model against `U_M`.

## 4. Strengthened threshold feasibility: the slack-exponent wedge

For proposal (A), let source time scale `T=N^{2 nu+o(1)}`, `1/2<nu<theta<1`, with the CHMY local generator's published seed/circuit upper bound `sigma=N^{nu+o(1)}` for subpolynomial query lengths and polynomial `q`. Source promised LOW cutoff is `N^theta/(c log N)`, NO cutoff `N^theta`.

Under the actual `E_r` (the same embedding with `r-1` additional groups of variables, using `M=N^r`), `CC(f)<=CC(E_r(f))<=CC(f)+O(1)`. A target having the ordinary OPS-shaped LOW exponent `beta'` can accept **all** source YES instances only if asymptotically `r beta'>=theta` (in the tight boundary case, the factor `log M=r log N` and additive gates require an explicitly strengthened source LOW constant). To reach `beta'<1/2` we therefore require **`r>2theta`**. Literal streaming of the target, even with free constant-time virtual oracle answers and ignoring head motion, requires `M=N^r` output/input moves; to fit inside the source time `N^{2nu}` one requires **`r<2nu`** (strict margins). Combining yields

`2theta < r < 2nu` while `nu < theta`, a contradiction.

This closes the *promised-threshold slack* attempted repair of Bridge33 under **full-stream** composition. No amount of changed fixed logarithmic-gap constants repairs this exponent contradiction.

There is a more abstract certificate bottleneck that does not assume literal streaming. Suppose source CHMY's proven security window uses time `T=N^{h+o(1)}`, with the published PRG seed upper bound exponent `h/2+delta` (where `delta>=0` charges query length and state-count exponents). Suppose a target machine runs in `M^{h'+o(1)}`, with `h'>=1`, and could be simulated in the source time, so `r h'<h`. To **certify** that every lifted PRG output is a LOW `GapMCSP[M^{beta'}/(c log M), M^{beta'}]` instance using only the published seed upper bound and the constant-size circuit wrapper requires `h/2+delta<r beta'`. Combining yields

`h' < h/r < 2 beta' - 2 delta/r <= 2 beta'`.

Thus **`beta'>h'/2>=1/2`** for any **certificate obtained from this published PRG seed bound and that literal time relation**. This is an obstruction to this *proof certificate*, not a lower bound on the actual PRG seed length and not an impossibility theorem for other reductions or stronger generators.

For an expansion which simply transports the source hardness exponent `h=1+g` to target exponent `h'=h/r`, the shrink factors are

`lambda=1/r` for the matched threshold exponent and `rho=(h-r)/(r(h-1))` for the hardness margin. For every `r>1` and `g>0`,

`rho-lambda=(1-r)/(r(h-1))<0`.

This fails the desired `rho>lambda` margin condition in the exact-threshold-matching regime, separately from the below-half contradiction.

**Example:** `nu=17/20`, `theta=9/10`, `r=8/5` gives target `beta'=9/16>1/2`, source margin `g=7/10`, target margin `g'=1/16`, `lambda=5/8`, `rho=5/56<lambda`. Expansion that actually drives `beta'<1/2` is already outside source time.

**First failed arrow for construction (A):** Model-compatible *all-promise-input* threshold descent below `1/2` while retaining a source-hardness-compatible online input scan is not achieved by this family.

## 5. Executed falsifiers and raw resource ledger

`chmy_bridge34_audit.py` is executable, deterministic, standard-library Python, with complete source in this package. It ran successfully and wrote `BRIDGE34_raw.json`.

* Exhaustively enumerated all **256** source truth tables of `N=8`, computed each complete `M=64` output, verified **16,384** indexed-bit checks and **8,192** adjacent-pair equalities, recovered `f` from the `y=0` restriction, and confirmed 256 distinct image strings.
* Exactly enumerated all **256** possible eight-bit prefixes of `U_M`: 16 pass the four-pair test, 240 fail. All 256 embedding images pass.
* Tested four public mask functions (zero, parity, nonlinear, original); each mask passed all **256** source truth tables and **1,024** fixed-pair checks, with the uniform acceptance probability `1/16`.
* Tested four public source-index maps and two masks each; each case constructed the first explicit repeated-index witness at or before index `N`, and verified all 256 source functions. Uniform acceptance is `1/2` for a single parity test. A bit-index permutation did **not** repair the public-bit-selection PRG claim.
* Exhaustively checked **6,840** rational-grid triples `(nu,theta,r)` with denominator 40 under `1/2<nu<theta<1` and `1<r<=2`. Not one met both `r<2nu` and `theta/r<1/2`. The exact symbolic proof above is independent of this finite check.
* Constructed an actual AND/OR/NOT circuit for a nonconstant `f=x_0 XOR x_1`: four base gates and **nine** added gates; evaluated all 64 target truth-table positions.
* Demonstrated that a **naive** parked-generator-counter fusion, with a target work head far to the right, costs at least `2*M*L` counter-to-head traversals; this does not exclude an optimized single-tape transducer. Therefore a standalone `O(M)` source generator plus a one-tape target decider has **not** been certified as a one-tape, near-`O(M)` composition.

| Resource / semantics | Result |
|---|---|
| Bridge33 `E(f)` source-bit reads, standalone generation | `N` exactly on valid N-bit source |
| Output writes | `M=N^2` exactly |
| Standalone streaming time | `Theta(M)` elementary output work, assuming ordinary constant-cost bit I/O |
| Standalone auxiliary workspace | `O(log M)` counter bits; no full target buffer |
| Random generator coins | 0 for `E`; real CHMY uses independent **uniform hidden seed**; tester uses 0 coins |
| Source-dependent advice | 0; the public maps/masks and CHMY source-independent PRG definition are explicit |
| Ordinary oracle query encoding | `E` and tester make none; no alleged `Sigma_3SAT` query compression |
| Target one-tape model | Distinguisher: **PASS** (0 work cells). Full target-decider simulation: **OPEN**, no free second tape |
| Exact circuit promise labels under repaired source-gap constants | Mathematically **PASS asymptotically**, per Bridge33; not itself hardness transfer |
| PRG lifted to uniform `M`-bit distribution | **FAIL** by concrete no-work-tape eight-bit distinguisher |
| Desired cofinal beta' below 1/2 with rho>lambda via this route | **FAIL** in proved parameter window |
| OPS nonuniform circuit premise | **NOT ESTABLISHED** |
| General alternative CHMY/MMW/OPS magnification | **OPEN** |

## 6. Next decisive falsifier / handoff

The next constructive target should **not** repeat public bit selection plus a public mask. The first serious alternative is a source-dependent linear/affine **mixing code** `E(f)_i = XOR_{j in S_i} f_j XOR h(i)` whose dual distance exceeds the small number of early output probes. It must be built from a real source-accessible streaming algorithm, not an arbitrary mask PRG; it must preserve *both* circuit-complexity promise labels, the genuine hidden-seed source distribution, and the **one-work-tape** model after composition. The immediate falsifier is either (i) a low-weight relation among early output coordinates (with an explicit no-work-tape or low-tape online tester), or (ii) charged source buffering/rewind costs above the `N^{2nu}` source security time. This is an **OPEN** proposal, not evidence of a new PRG.

The earlier `:00` ordinary MKTP route remains independent. The current work produces **no** SAT-to-ordinary-MKTP generator, no P-vs-NP contradiction, and no claimed nonuniform OPS hypothesis.

## Original sources

[1] M. Cheraghchi, S. Hirahara, D. Myrisiotis, Y. Yoshida, *One-Tape Turing Machine and Branching Program Lower Bounds for MCSP*, STACS 2021. DOI 10.4230/LIPIcs.STACS.2021.23. Theorem 16, Corollary 23, Lemmas 14–15 and 22. https://drops.dagstuhl.de/storage/00lipics/lipics-vol187-stacs2021/LIPIcs.STACS.2021.23/LIPIcs.STACS.2021.23.pdf

[2] I. C. Oliveira, J. Pich, R. Santhanam, *Hardness Magnification Near State-of-the-Art Lower Bounds*, Theory of Computing 17 (2021) article 11. Theorem 1.4. https://theoryofcomputing.net/articles/v017a011/

[3] D. M. McKay, C. D. Murray, R. R. Williams, *Weak Lower Bounds on Resource-Bounded Compression Imply Strong Separations of Complexity Classes*, STOC 2019. Theorem 4.2. https://people.csail.mit.edu/rrw/MCSP-MKTP-stoc19.pdf