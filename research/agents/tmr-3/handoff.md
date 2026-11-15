# TMR-3 CURRENT handoff | 2026-11-14 16:35 PST | SHARP SPARSE ORDINARY MCSP SOURCE-INGRESS FRONTIER031

**NEW SHARPSPARSE43 PROVED/RESTRICTED, TMR-2/TMR-5 independent mathematical audit OPEN:** For ordinary exact MCSP on an explicit full N=2^n bit table, s=floor(N^mu), any fixed 0<mu<1, pick fixed K>2mu/(1-mu) and r=ceil(Ks). For EVERY YES input x, at most epsilon_N<=D(n,s)/C(N,r)=2^[-Omega(s log N)] of its r-bit flips are YES; D=(s+1)(n+s+2)[3(n+s+2)^2]^s. Any bounded-error randomized adaptive point-bit decider with error delta<1/2 obeys E_coins[q(x)] >=(1-2delta-epsilon_N)N/r=Omega(N^(1-mu)) on EVERY YES x, even with arbitrary paid source-aware preprocessing, sharing, caching, recomputation or many processors. **This sharpens PRIOR research/main/2026-10-20_0548_MAIN_CONDITIONED_HARD_SPARSE_QUERY7.md**, which used r=N^(mu+epsilon) and hence lost an arbitrary exponent epsilon. The proof is ordinary-MCSP circuit counting + same-trace adaptive coupling, no Gap promise. If per-bit source ingress is charged network-wide, this bounds expected total events E; with source-aware constructors include their source reads in E_total. Deterministic exact YES queries have the STRONGER ALREADY-PRIOR N-O(N^mu log N) bound (FIBER27 and TMR-2/026); so NETFRONT39's N^(.99) transfer is non-optimal for deterministic ingress, but may remain stronger for randomized high-mu2 MCSP. Input reads do not imply superlinear post-ingress computation or P!=NP.

**ACTUALLY EXECUTED same-function V8 test:** exact published experiments/tmr/tmr3_sharp_sparse_network043.js, immutable raw results/raw/tmr/2026-11-14_1635_TMR3_SHARP_SPARSE_NETWORK043_RAW.json, **739 assertions, zero failures**; exhaustive <=2-gate n=4 truth tables gives 90 YES, every 4-flip neighbor of all 90 tested (163,800), max 24/1820 sparse neighbors remained YES; 1,146,600 exact no-hit checks; four large-N log-circuit and log-binomial margins verified. Finite tests COMPUTATIONAL. No compiled physical machine/network or asymptotic runtime experiment.

**FULL REPORT:** research/agents/tmr-3/2026-11-14_1635_TMR3_SHARP_SPARSE_NETWORK_SOURCE_FRONTIER031.md. CHMY STACS2021 Theorems 1-2 visually checked in publisher PDF printed 23:3. Reviewed controlling Nov14 directive FIRST, Nov13 replacement, AGENTS, CODEX, repo skill, issue #3, five latest peer handoffs, both complete trackers (proof2 via Git blob 1,051,196 characters), main.tex (via Git blob 2,545,859 characters), original TMR-2/026/031, original October conditioned sparse and FIBER, TMR-3/030, TMR-1/030, Claude ONETAPE/TPORT/DIRECTPRODUCT and earlier losses. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** Root main.tex TMR-5-owned, unchanged; schedules untouched; P versus NP OPEN.

**PEER REQUEST/NEXT:** TMR-2 audit sharp K_mu constant and all-YES randomized coupling; TMR-5 audit charging all constructor and network source accesses, deterministic versus randomized frontier; TMR-1 audit threshold mu1 versus mu2; TMR-4 test succinct source shortcuts. Next seek/falsify genuinely **post-ingress** cost above N for small-mu1 ordinary MCSP on one-way input plus one work tape.

END_OF_HANDOFF::TMR3::031::2026-11-14_1635_PST

---

# TMR-3 CURRENT handoff | 2026-11-14 15:33 PST | HIGH-MU NETWORK EVENT FRONTIER030

**NEW NETFRONT39 PROVED/RESTRICTED, independent TMR-1/TMR-5 review OPEN:** A fully charged, length-only uniform constructor and constant-symbol-event deterministic/randomized network deciding ordinary high-threshold $MCSP[N^{\mu_2}]$ (the **different large $\mu_2$** of Cheraghchi et al., STACS 2021 Theorem 2) is serializable on one fixed one-way-input plus one-work-tape machine in $T=O(C+N+(E+1)M)$, with $M=O(N+B+(E+p+1)\log(N+B+E+p+2))$. Here $N=2^n$ is full truth-table input length, $B$ description bits, $C$ physical constructor transitions, $p$ processors, $E$ worst-case charged events, and ALL interfaces, input reads and work are counted. For $C=O(N^c), B=O(N^b), p=O(N^a), E=O(N^e)$ and $d=\max(1,a,b)$, CHMY Theorem 2 rules out $c<1.99$ and $e+\max(d,e)<1.99$. In particular $B,C,p=O(N)$ rules out $E=O(N^{0.99-\varepsilon})$ for every fixed $\varepsilon>0$; with $E\le pt$, it rules out simultaneous $p=O(N^a),t=O(N^b)$ when $a+b<0.99$. Restricted to high $\mu_2$, NOT $P\ne NP$.

**NEW CONSPACE39 DIRECT-SIMULATOR LEDGER REPAIR:** Peak writable space of the simulator **executing the specified constructor** is $S_{\rm sim}=O(S_C+M)$, not $O(M)$ as TMR-3/029 stated without bounding constructor peak space. A fixed constructor can write and erase $N^2$ cells and emit an $O(1)$-bit description, giving $S_C=\Theta(N^2)$ but $M=O(N)$. This does NOT show no optimized equivalent constructor exists. A source-dependent constructor needs separately charged source-access simulation.

**ACTUALLY EXECUTED NATIVE CPython:** exact `experiments/tmr/tmr3_network_event_frontier039.py` (Git blob `961688c511d6e92b24f956d6a045a0d48d07a8b2`); raw `results/raw/tmr/2026-11-14_1533_TMR3_HIGHMU_NETWORK039_RAW.json` (blob `65bc84593b95c26cc0c44dfbe70a76c997b03ec1`): 7,200 assertions, 1,016 tiny exhaustive parity networks, 13,772 charged events, 148,136 record-visit proxies, 3,315 exact rational exponent configurations, zero failures. Finite semantic proxy NOT an implemented physical one-tape machine or MCSP lower-bound experiment.

**REPORT:** `research/agents/tmr-3/2026-11-14_1533_TMR3_HIGHMU_NETWORK_EVENT_FRONTIER030.md`. Preflight current MCSP directive FIRST and rechecked, Nov13 TMR directive, AGENTS/CODEX/skill, authentic full proof1/proof2/root-main, issue #3, five handoffs, TMR/Claude originals, CHMY publisher PDF p.23:3 and MMW manuscript. TRACKERS REVIEWED; NO MATERIAL CHANGE. Canonical main.tex unchanged. No schedules modified. P versus NP OPEN.

**NEXT / PEER REQUEST:** TMR-5 audit constructor-space counterexample and exact simulation; TMR-1 verify $\mu_2$ and strict exponent; TMR-2 test query strengthening without invalid online assumptions; TMR-4 seek full-table threshold-preserving reduction. Missing unrestricted arrows OPEN.

END_OF_HANDOFF::TMR3::030::2026-11-14_1533_PST

---

# TMR-3 CURRENT handoff | 2026-11-14 14:55 PST | TWOWAY HEADER AND NETWORK BRIDGE029

**NEW TWOREWIND32 PROVED/RESTRICTED symbolic, TMR-1/TMR-5 peer review OPEN:** Any fixed one-way-input/one-work-tape decision algorithm for $\gamma(n+1)||x$ (literal upfront arity header) with costs $T_H,S_H$ can be compiled into a **header-free, TWO-WAY read-only input** plus ONE work tape algorithm at $T_B=O(N\log N+(T_H+1)\log N)$ and $S_B=S_H+O(\log N)$. First count $N=2^n$, rewind source, synthesize the gamma header on the single work tape, then run the original guest while real source stays parked until guest finishes the header. This yields TMR-3/028 ANNO's $T=N^{1+2\kappa+o(1)}$, $S=N^{2\kappa+o(1)}$ for slowly growing $s_\kappa=\lfloor\kappa n/\lceil\log_2(n+1)\rceil\rfloor$ and fixed $0<\kappa<.005$, but **does NOT** supply the one-WAY model or $s=N^{\mu_1}$ needed in CHMY STACS21 Theorem 1.

**NEW NETWORK32 PROVED/RESTRICTED elementary quantified bridge, TMR-4/TMR-5 audit OPEN:** Uniform polynomial-constructor, polynomial-description $p(L)$-processor single-tape networks with charged bounded per-round local steps/messages and polynomial elapsed $t(L)$ can be serially simulated by a fixed one-way-input/one-work-tape machine in polynomial $L$ time. For total events $E=O(pt)$ and serialized footprint $M=O(L+B+(E+p)\log(L+B+E+p))$, time $O(C+L+(E+1)M)$ and writable space $O(M)$. Consequently existence of a polynomial $(B,C,p,t)$-bounded correct 3-SAT network is **equivalent to $P=NP$**, not a new separation proof. Without uniformity, a separate $\Theta(2^L)$-state trie for each $L$ falsifies the processor/time inference. Quadratic generic serial overhead cannot import CHMY's high-$\mu_2$ $N^{1.99}$ one-tape bound to prove superlinear network event cost.

**ACTUALLY EXECUTED hosted V8 exact source:** experiments/tmr/tmr3_twoway_header032.js, immutable raw results/raw/tmr/2026-11-14_1455_TMR3_TWOWAY_BRIDGE032_RAW.json, **4,715 assertions, 0 failures**, 828 exhaustive bounded-gate MCSP classifications, 19,242 charged two-way input-head moves, 23,532 binary-counter proxy operations, 245,168 record/bit comparisons, 22 malformed controls, 272 tiny network parity cases (5,040 event proxies). This is a **semantic proxy**, NOT a compiled TM; asymptotic claims have separate symbolic proofs.

**FULL REPORT:** research/agents/tmr-3/2026-11-14_1455_TMR3_TWOWAY_HEADER_NETWORK_BRIDGE029.md. Preflight controlling MCSP directive read FIRST, Nov13 replacement and AGENTS/CODEX/skill, authentic full root proof1/proof2/main Git blobs, five latest handoffs, issue #3 through TMR-5/026, original TMR-3/028 and peer/Claude/Walsh/Grok guards, CHMY STACS21 Theorems 1–3 and MMW STOC19 Theorems 1.2–1.3 original PDFs/page screenshots. TRACKERS REVIEWED; NO MATERIAL CHANGE; TMR-5 owns canonical main.tex; schedules untouched. P versus NP OPEN.

**NEXT / PEER REQUEST:** TMR-1/TMR-5 audit exact physical one-head synthetic-header shuttling and n/length quantifiers; TMR-2 audit read-only two-way versus one-way; TMR-4 audit charged network messages and serialization; search a genuine **one-way** low-space growing-s summary or subquadratic network bridge without assuming a free rewind.

END_OF_HANDOFF::TMR3::029::2026-11-14_1455_PST

---

# TMR-3 CURRENT handoff | 2026-11-14 13:27 PST | RAWCACHE/ANNOTATED FRONTIER028

**NEW RAWSCAN28 PROVED/RESTRICTED symbolic upper bound, TMR-1/TMR-5 physical model audit OPEN:** Independently strengthen TMR-1/027's cached-truth-table MCSP enumeration. On bare **length-blind one-way input plus exactly ONE two-way work tape**, copy raw N=2^n data bits contiguously without permanent indexed records; retain a single mobile finite-alphabet scratch block with circuit description, assignment index and gate workspace. Literal head-local cyclic scratch/bit rotations cost O(m) per cell, m=O(n+(s+1)log(n+s+2)). Enumerate D(n,s)=(s+1)(n+s+2)[3(n+s+2)^2]^s circuits. For any uniformly computable s(n), **T=O(N D(n,s) poly(n+s+1)), S=N+O(m)** visited writable cells. For s_kappa=floor(kappa*n/ceil(log2(n+1))), T=N^(1+2kappa+o(1)), S=O(N). This is an upper bound, not evidence N cells are necessary.

**NEW ANNO28 PROVED/RESTRICTED symbolic construction, UNEXECUTED:** If n is actually supplied in a self-delimiting source prefix BEFORE the N-bit truth table, build D circuit records with local indices, flags, gate scratch. Suspend one-way source head while updating all records for each bit, charging all physical tape scans. **T=N D poly(n+s), S=D poly(n+s)**. For fixed rational 0<kappa<0.005, asymptotically T<N^1.01 and S<N^0.01. This is an **annotated DIFFERENT language**, NOT the bare CHMY model; no free header and no implication to P!=NP. HEADER27's full-ordered-output retention theorem does not automatically bar a co-designed bare one-bit decider.

**ACTUALLY EXECUTED native CPython:** exact new source `experiments/tmr/tmr3_rawscan031.py` Git blob 0cdf639789c51af9d4217cbdea89b1412438d925 (SHA256 8e6ec6714d6a7d3cf5848992cb4df9cb057d8a1b1ebfb1b868e6eee66d746918); raw `results/raw/tmr/2026-11-14_1327_TMR3_RAWSCAN031_RAW.json` Git blob 3e4494672dec68517ad8fe17c266d8b7880d1671 (SHA256 1c1c6ffffb553678bfbe517c3b45e0f652fd9f1cd3f78f798769a9801e494fc0). 1,861 assertions, 0 failures; 828 exhaustive classifications, 1,024 literal rotation checks, 9 function-count controls; 231,036 explicit local tape rotations and 7,603,632 charged micro-operation proxies. Candidate function bits still evaluated in Python, not compiled full TM, and header-stream construction was NOT run. All finite evidence COMPUTATIONAL.

**REPORT:** `research/agents/tmr-3/2026-11-14_1327_TMR3_MCSP_RAWSCAN_HEADER_BOUND028.md`. Historical full handoff preserved below. CHMY STACS 2021 Theorem 1 demands a **small positive mu** ordinary MCSP[N^mu] one-work-tape N^1.01 lower bound to imply P!=NP; Theorem 2 proves randomized N^1.99 at a DIFFERENT larger mu. Our slowly growing s=Theta(n/log n) cannot meet this. MMW STOC2019 Theorems 1.2-1.3 concern search/oracle streaming with s(n)>=n, so neither construction substitutes for those premises.

**PREFLIGHT:** Nov14 directive first/rechecked blob 1e11aa64a0b0d635a65cea58500b09f2b0fe010a, Nov13 replacement; complete proof1 (28,714 chars), authentic proof2 via blob (1,051,196) and canonical main.tex via blob (2,545,859); AGENTS/CODEX/skill; latest issue #3 through TMR1/027; all five current TMR handoffs; original TMR1/027, TMR3/027,/025, Claude ONETAPE/DIRECTPRODUCT/TPORT, original Grok/historical affine/Walsh failures, CHMY/MMW publisher/author PDFs/page images. TRACKERS REVIEWED; NO MATERIAL CHANGE; TMR-5 owns main.tex; no schedules modified.

**NEXT / PEER REQUEST:** TMR-1 and TMR-5 independently audit single-head rotations, cache counter, exact all-length uniformity, and the annotated EOF/record sweep. TMR-2/TMR-4 examine a genuine length-blind, growing-threshold inherited updater and compact algebra controls. Bare-source low-space compiler and positive-mu N^1.01 lower bound remain OPEN. P versus NP OPEN.

END_OF_HANDOFF::TMR3::028::2026-11-14_1327_PST

---

# TMR-3 CURRENT handoff | 2026-11-14 12:28 PST | MOBILE-COUNTER FUSION AND EARLY-HEADER FRONTIER027

**NEW FUSE27 CANDIDATE/RESTRICTED**: For ANY fixed deterministic one-way-input + ONE work-tape guest B and explicit truth-table x of length N=2^n, an **annotated** source gamma(t+1)||x permits ONE physical one-way-input, one-work-tape uniform compiler C_B simulating B on P_t(x), which repeats each bit 2^t times (M=N*2^t). Every concrete guest transition and both labels are preserved, with **T_C=O_B((t+1)(T_B+1)+(t+1)^2), S_C<=S_B+O_B(t+1)**. The t-bit source-repetition counter sits **adjacent to the guest work-head marker on the SAME tape**; local counter/head rotations cost O(t+1) and no second physical head, uncharged random input, or N-bit input spool is assumed. This is a charged *upper simulation* for annotated input, not a lower bound or bare-MCSP transfer. TMR-1/TMR-5 independent proof review OPEN.

**NEW HEADER27 CANDIDATE/RESTRICTED**: For length-blind, one-way source, fixed w finite work tapes with q states/alphabet G, and non-readable ordered append-only **FULL output** gamma(t(n)+1)||x where for each large n some larger n' has different t, let h_n be the gamma length and S(N) max visited writable cells. The original source cannot supply the correct *early header* before EOF without retaining all source bits:
$$
2^N <= (h_n+1)q(2S(N)+3)^{3w}G^{S(N)}.
$$
For t(n)=ceil(a n), a>0, and polynomial-size gamma header, **S(N)=Omega(N)**. Prefix-free header difference and shared source-prefix continuation give injective post-EOF state. A jointly optimized **one-bit decision** does not need to produce this header; no MCSP/SAT time lower bound follows. Genuine supplied header, rewinding, and caching N bits are permitted escape routes. TMR-5 review OPEN.

**ACTUAL NATIVE CPython symbolic physical-layout tests:** exactly 5,520 independent guest runs, 323,520 step-by-step complete-configuration comparisons, 13,722,560 conservatively charged proxy operations; 5,200 both-label exact MCSP[0] padding checks, 15 header-prefix divergence controls and 276 finite header-injectivity controls, ZERO failed assertions. The finite run is **COMPUTATIONAL**, NOT a native compiled TM execution. Executed file SHA256 efbb42d85717cc92f9ce7cafd354aab91b4a055a73760ab0375f7785237b547c, exact Git blob 35a1b2e7ae9c9de8ec92f9dae719223ed4dfd2c0; raw blob 94e862b7e3805ebd05bceda539d2ea0161d0d435.

**PUBLICATIONS:** research/agents/tmr-3/2026-11-14_1228_TMR3_MCSP_MOBILE_HEADER_FUSION027.md ; experiments/tmr/tmr3_mobile_header027.py ; results/raw/tmr/2026-11-14_1228_TMR3_MOBILE_HEADER027_RAW.json ; research/agents/tmr-3/handoff.md. All prior handoffs retained below.

**PRIMARY CHMY FIREWALL:** STACS2021 Theorem 1 low-mu ordinary MCSP one-work-tape N^1.01 time exclusion would imply P!=NP; its premise is OPEN. Theorem 2 proves randomized N^1.99 exclusion at a **different high mu**. Exact integer circuit thresholds must match for simple padding, TMR-1/026 rules out mismatches. Under a *hypothetical and still missing* bare-source/annotated-source transfer, specialized fused runtime exponent is rho*beta where M=N^rho; the certified 1.01/1.99 corridor rho<199/101 is necessary for that upper-bound proof scheme. **P versus NP remains OPEN.**

**PREFLIGHT:** latest Nov14 MCSP directive FIRST SHA 1e11aa64a0b0d635a65cea58500b09f2b0fe010a; Nov13 replacement; proof1 28,714 characters and recovered complete proof2 1,051,196 characters plus main.tex 2,545,859 by exact Git blobs; AGENTS.md, CODEX.md, skill, latest issue #3 and all five peer handoffs, original October composition and historical Claude/TMR/Grok/LSPV evidence, CHMY/MMW primary theorem records. TRACKERS REVIEWED; NO MATERIAL CHANGE. Canonical main.tex unchanged. No schedules altered.

**PEER REQUEST:** TMR-1 check mobile-block rotations, fixed alphabet, EOF and totality. TMR-5 check HEADER27 common-prefix cut and October novelty. TMR-2 inspect one-bit decision bypass; TMR-4 test a genuine both-label non-padding threshold descent. **ONE NEXT TARGET:** an exact, header-free one-work-tape virtual-input compiler under an explicitly restricted but natural guest access pattern, or a reproducible adaptive counterexample; retain arbitrary polynomial workspace and source rereads where the model allows.

END_OF_HANDOFF::TMR3::027::2026-11-14_1228_PST

---

# TMR-3 CURRENT handoff | 2026-11-14 11:30 PST | LENGTH-OBLIVIOUS MCSP PADDING FRONTIER026

**NEW LENGTHBLIND26 CANDIDATE/RESTRICTED**, independently checkable elementary proof, TMR-5/TMR-1 review OPEN: For one fixed uniform finite transducer on ALL admissible lengths N=2^n, one-way read-only source initially **without** a length header/advice, w fixed local two-way work tapes with G finite symbols and q states, and read-inaccessible ordered append-only output, exact contiguous ignored-low-bit padding E_{t(n)}(x)=each x_i repeated R_n=2^{t(n)} requires

$$
2^{N-2}\le (R_n+1)q(2S(N)+3)^{3w}G^{S(N)}.
$$

When t(n)=ceil(a n) with fixed a>0, S(N)=Omega(N). Proof: compare shared N-bit source prefix x=01v against longer valid x'=x0... with R_{n'}>R_n; before seeing short-input endmarker, outputs cannot pass R_n zero bits, yet N-2 freely varied source bits must be retained in complete work config + emitted-prefix length to finish exact output. **This is an interlength, unknown-input-size obstruction**, unlike PRIOR TMR-4/026, TMR-5/022 fixed-length permutation frontiers. Fixed t, upfront n header or two-way input avoids linear retention. Caching N bits costs allowed polynomial workspace; no MCSP time lower bound, no threshold-changing reduction, no SAT separation.

**ACTUALLY EXECUTED V8 and published:** experiments/tmr/tmr3_length_blind_padding026.cjs and raw results/raw/tmr/2026-11-14_1130_TMR3_LENGTH_BLIND_PADDING026_V8_RAW.json; 16,452 exhaustive short/long ambiguous-prefix cases, 32,904 independently generated padded tables, 65,808 fixed-t positive streaming controls, zero failures. **INDEPENDENT native CPython local-only:** matching 16,452 length ambiguity tests, 816 both-label small-circuit checks, 65,808 fixed-t controls, 0 failures, source SHA256 cfca3cf85104637f77ca90ad8567eac048478f64c0a9f069977f998043248d44. Both computational, not native finite-alphabet TM or universal compiler.

**PAPER and theorem scope:** CHMY STACS2021 Theorems 1 and 2, p23:3, same one-way input plus one two-way work tape, low-mu N^1.01 hypothesis versus large-mu N^1.99 established lower bound, remain different languages. MMW STOC2019 Theorems1.2-1.3 are oracle-assisted streaming **search** and require simultaneous poly(s) update+space. TMR-1/024 PRIOR exact circuit minimum and threshold matching. For padding ratio M=N^rho a naive low-bound composition into a high-bound contradiction needs 1.01rho<1.99 and model-preserving extra costs. No implication established.

**REPORT:** research/agents/tmr-3/2026-11-14_1130_TMR3_MCSP_LENGTH_BLIND_PADDING_FRONTIER026.md. **PRE-FLIGHT:** Nov14 directive FIRST blob 1e11aa64a0b0d635a65cea58500b09f2b0fe010a, Nov13 replacement, complete proof1 28,714 blob 06f7ebc8c2283304a0f5200b518c6e48fa41e343, full proof2 1,051,196 blob 930c5eeddafce656717f28055a7a9a755f44737c, root main.tex 2,545,859 blob 6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34c, root instructions/skill, all five TMR handoffs, latest issue #3, prior TMR/Claude original reports and publisher primary PDFs. **TRACKERS REVIEWED; NO MATERIAL CHANGE**; main.tex left to TMR-5. No tasks modified.

**NEXT:** TMR-5 peer-review length-ambiguity cut/injection and output-tape assumption. TMR-1 check exact variable order/threshold parameter arithmetic; TMR-2 inspect input-length oracle escape. Develop charged **same-one-work-tape generator/MCSP-consumer** physical composition without an upfront n header. Arbitrary P vs NP OPEN.

END_OF_HANDOFF::TMR3::026::2026-11-14_1130_PST

---

# TMR-3 CURRENT handoff | 2026-11-14 10:28 PST | UNIFORM GROWING-RING MCSP SERIALIZATION025

**NEW RING25 CANDIDATE/RESTRICTED pending TMR-1/TMR-5 formal review.** A uniformly constructible synchronous ring with polynomially growing p(N) locally moving one-work-tape processors, one common ONE-WAY new source bit per round, fixed finite catalogue of local rules, two unit-capacity nearest-neighbor ports and a polynomial clock B(N)>=R(N), is simulated by ONE finite deterministic one-way-input/one-work-tape machine in **T=O(U(N)+B(N)[N+p(N)B(N)])** and S=O(N+p(N)B(N)). U(N) is full physically charged uniform initialization/generator cost. The proof spools source input on the sole work tape and uses O(1) complete finite-alphabet sweeps per round over p adjacent 2B+O(1)-cell processor regions, including source retrieval, old-to-new head markers, adjacent-port messages and ring wrap. **Only RING topology**, not arbitrary interconnect or free input fanout. Distinct from PRIOR fixed-p TMR-3/024.

**EXACT CHMY exponent firewall.** For p=N^a, B=N^b, U=N^u, this compiler certifies only an upper N^max(u,b+1,a+2b). A hypothetical **same large-threshold** MCSP ring solver needs strict max<1.99 to contradict CHMY Theorem 2 using this certified upper bound. In a full-scan one-new-bit/round protocol, B>=N, so b>=1 and a+2b>=2. Thus the generic simulation certificate alone gives no nontrivial CHMY network-time exclusion, even for p=1. No claim that an alternative faster compiler is impossible. The CHMY *small-threshold* N^1.01 premise remains OPEN. Model-specific polynomial-resource ring MCSP existence is equivalent to MCSP in P, not a shortcut to P versus NP.

**EXECUTED COMPUTATIONAL:** hosted V8 source experiments/tmr/tmr3_ring_network025.cjs and raw results/raw/tmr/2026-11-14_1028_TMR3_RING_NETWORK025_V8_RAW.json: 3,366 complete direct/swept configuration checks, p<=12, 1,623 YES / 1,743 NO / five malformed controls, 27,970,425 charged proxy movements, zero final assertions. Independent native CPython local-only source SHA256 98bfda5e6be25239774b018a9a4f7f086c810e09af6e812d30c9992e1aeea2bb: 3,366 cases and 0 final failures, differing seeded samples. Initial native false check p=1 source "1" caused by advancing a head into later same-sweep position and executing it AGAIN; fixed by freezing OLD head markers. Neither proxy is a compiled native finite-alphabet TM.

**REPORT:** research/agents/tmr-3/2026-11-14_1028_TMR3_MCSP_POLY_RING_SERIALIZATION025.md. Current directive SHA 1e11aa64a0b0d635a65cea58500b09f2b0fe010a read FIRST; replacement SHA 47459817e66dccf1f3079e6c724c0fd2643e7bc4. Full proof1 28,714 chars SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343; full Git-blob proof2 1,051,196 chars SHA 930c5eeddafce656717f28055a7a9a755f44737c; full Git-blob root main.tex 2,545,859 chars SHA 6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34; issue #3 through TMR-2/025; all five TMR handoffs and relevant originals and CHMY/MMW PDFs reviewed. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** main.tex reserved for TMR-5. No scheduled tasks changed.

**NEXT:** TMR-1/TMR-5 audit all-transition fixed-sweep ring compiler; TMR-2 audit full-scan premise; TMR-4 find exact, same-machine online padding composition if possible. TMR-3 next tests concrete dummy-pad source + low-threshold target machine, all interface costs. P versus NP OPEN.

END_OF_HANDOFF::TMR3::025::2026-11-14_1028_PST

---

# TMR-3 CURRENT handoff | 2026-11-14 09:36 PST | MCSP FIXED-NETWORK QUADRATIC SERIALIZATION024

**Priority:** User's November 14 MCSP directive overrides superseded scientific topics, preserving the five TMR roles, schedules and historical results.

**NEW FIXED-NET24 (CANDIDATE/RESTRICTED; TMR-1/TMR-5 review requested):** Any fixed finite network of p locally moving one-work-tape processors sharing one one-way read-only input scan, with fixed finite-graph delayed channel messages and fully charged local steps, has a **single** one-work-tape / one-way-input deterministic simulator using O_p((R+1)^2) transitions and O_p(R+1) writable cells after R elapsed rounds. Concrete proof uses fixed-p multi-track encoding, finite machine control and O_p(t+1) charged sweeps per round, with no input rewind. Growing p(N), arbitrary random ports, asynchronous uncharged channels and per-length topology/advice are excluded.

**EXACT CHMY EXPONENT FIREWALL:** Cheraghchi et al. STACS 2021 Theorem 2 establishes ordinary MCSP[N^mu2] outside BPTIME_1[N^1.99], with mu2 near 1, not the smaller mu1 of Theorem 1's P!=NP magnification premise. Combined with the quadratic fixed-p simulator, this only excludes network elapsed rounds O(N^(199/200)) for the **large-threshold** language. For whole-stream protocols R>=N already, so this transferred lower bound is strictly weaker than scanning. It is NOT a polynomial-network-size vs superpolynomial-elapsed-time dichotomy. The threshold mismatch and polynomially growing p remain OPEN.

**NATIVE CPYTHON COMPUTATIONAL CONTROL:** Independent direct network and swept-track proxy agreed for 2,044 binary streams, p=1..4, lengths 0..8; 2,008 YES/36 NO, 20 malformed; 207,782 charged adjacent sweep moves; 2,044 upper checks; ZERO failures. The sweep implementation is a Python proxy, not a native finite-alphabet compiler. An initial missing-return/duplicate-update sweep bug was corrected before the final run, and remains acknowledged. Executed source SHA256 920bed2a0a6ffb28bc2ef34a8b0ca4c0995fc1ecc2cd75a1b13f4ada8b206bfd.

**Published paths:** research/agents/tmr-3/2026-11-14_0936_TMR3_MCSP_FIXED_NETWORK_SERIALIZATION024.md; experiments/tmr/tmr3_mcsp_network024.py; results/raw/tmr/2026-11-14_0936_TMR3_MCSP_NETWORK024_RAW.json.

**Peer target:** TMR-1/TMR-5 independently prove or falsify FIXED-NET24 and model translation; TMR-2 audit input-scan necessity; TMR-4 test explicit low-mu transfer preserving circuit threshold, two labels, input length and paid cost. P versus NP OPEN.

---

# TMR-3 CURRENT handoff | 2026-11-14 08:49 PST | GF4 ORACLE-VERSUS-WHITE-BOX COMPOSITION023

**NEW GF4-OR23 CANDIDATE/RESTRICTED**, complete elementary proof, TMR-2/TMR-5 independent review requested. Over GF(4)=GF(2)[alpha]/(alpha^2+alpha+1), for arbitrary Boolean f on b inputs, a deterministic algorithm with **only Boolean-value oracle access** must query all 2^b input points to compute exactly the multilinear extension at (alpha,...,alpha), even with unlimited workspace. The zero-oracle versus unqueried-single-spike proof has all Lagrange weights nonzero. The black-box restriction is essential: for OR_b, canonical ANF has exactly 2^b-1 nonzero monomials but the extension factors as 1+product_i(1+z_i). **ONE fixed locally moving finite-control machine** computes either Boolean OR of b bits or that extension on b explicitly encoded GF(4) elements, with each read/output transition charged, **same-machine T<=L+5, S<=2 writable visited cells**. This is a genuine two-model counterexample to uncharged transfer from canonical monomial count or generic extension oracle queries to compulsory physical local-block evaluation. It is not a general SAT decider or a complete Williams/Cook-Mertz compiler.

**Exact GitHub-byte native executed and verified:** experiments/tmr/tmr3_gf4_extension023_native.py, Git blob a042e1a022339ceeb4854ed8221027162050e80a, SHA256 214b0487ff9ca63a98185ee7aa829e2818670c80f3e877ad3357dc09e44e7345, byte-reconstructed from GitHub and independently rerun under native CPython. Original differently formatted native runner also ran independently and matched all numeric metrics. **COMPUTATIONAL:** 1,022 single-spike nonzero GF4 oracle weights; 276 complete arbitrary truth-table checks, 9 OR factorizations; 16,383 single-head physical controller traces (13,652 valid, 2,731 malformed), max T-L=5, output writable cells <=2; 16 SAT/UNSAT CNF controls including U1..U4, Horn, 2-SAT, XOR3, sharing, products, renaming; 21 duplicated-DAG recurrence controls; zero failures. A second compact published Python reproducer is unexecuted and not authoritative.

**Verified report:** research/agents/tmr-3/2026-11-14_0842_TMR3_GF4_ORACLE_COMPOSITION_FIREWALL023.md; **raw:** results/raw/tmr/2026-11-14_0841_TMR3_GF4_ORACLE_COMP023_RAW.json. Primary Williams STOC 2025 / Cook-Mertz STOC 2024 / FLMV JACM 2005 checked at their model scope. Related TMR-2/022 Walsh-flat UNSAT and November 14 semantic-composition coordination reviewed; older INDEX20 remains restricted. **TRACKERS REVIEWED; NO MATERIAL CHANGE:** proof1 SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343 (28,714 chars); proof2 authentic Git blob SHA 930c5eeddafce656717f28055a7a9a755f44737c (1,051,196 chars); root main.tex Git blob 5ec8fffb16ec9a7f262e60321bf5aad172d153d8 (2,542,866 chars) reserved for TMR-5. No schedules touched. No preflight/TeX compile or arbitrary-TM compiler. Both P=NP and P!=NP remain OPEN.

**ONE NEXT TARGET:** extract one exact implicit node-bit generator from Williams's actual arbitrary-multitape computation tree, and pay the joint time/space cost of (a) constructing/identifying its dependencies, (b) any required algebraic extension evaluation, (c) source rereading, caching and recomputation, and (d) recursive composition. Compare a legitimate noncanonical factorization against the *actual* interpolation obligations. Do not insert Boolean-value oracle lower bounds as machine costs without a proved black-box restriction.

END_OF_HANDOFF::TMR3::023::2026-11-14_0849_PST

---

# TMR-3 CURRENT handoff | 2026-11-14 07:31 PST | HYBRID RETENTION/LOCAL VIEW INDEX020

**NEW TMR3-HCL20 CANDIDATE/RESTRICTED, TMR-1/TMR-5 review requested.** In one fixed total uniform two-phase delayed INDEX machine with r locally moving nonsensing original-source heads, w ordinary independent writable tapes, q control states, alphabet <=g, a later x-independent binary query p, and exact x[p] on every source x in a set X of length L: if every preprocessor run on X visits <=s writable cells and every post-query phase on X and every p lasts <=t transitions, then

$$
|X|\le q(L+2t+4)^r 2^{r(2t+1)}
\min\{(2s+3)^{3w}g^s,(g+1)^{w(2t+1)}\}.
$$

Both bound branches count SAME-machine, SAME-source retained work views. The first counts COMPLETE visited work tape configurations, the second all physically reachable radius-t neighborhoods. Source type/contents and control counted once. Equality of the joint fingerprint couples every adaptive actual second-phase transition and terminal output, giving injectivity. For X all 2^L strings and s(L)=sigma L+o(L), worst-case t/L has liminf >= max{(1-sigma log_2(g))_+/(2r),1/(2[r+w log_2(g+1)])}. This is a quantitative workspace interpolation, only LINEAR delayed-INDEX query cost and no unconditional 3-SAT lower bound.

**INDEPENDENT TMR-1/021 restricted peer audit:** verified the symbol-only geometry counterexample with heads (0,0) versus (0,1) on the same all-blank sensing work tape. Their individual local windows agree but collision sensing distinguishes them in one step. Clipped signed separation within ±2t and far-direction classes supports induction for sensing shared-head execution, subject to TMR-1's exact finite collision predicate. Does not falsify TMR-3/019's nonsensing model. New HCL20 states nonsensing distinct work-tape scope rather than silently transferring models.

**ACTUALLY EXECUTED hosted V8, published exact code and raw JSON:** 196 parameter/fixture cases (84 <=L work footprint), 42 global-cap versus 154 local-view min branches, 2,732 local-fingerprint collisions, 10,198 pairwise query replays and 18,282 charged simulated physical steps, 84 far-source cases, 1,356 full-cache/XOR/mirror collision cases, one sensing-head counterexample, zero failures. Fixture preprocessing was symbolic, NOT a charged all-machine compiler; all finite results COMPUTATIONAL. No native Node or independent CPython run was performed.

**VERIFIED GITHUB MAIN:** report research/agents/tmr-3/2026-11-14_0731_TMR3_HYBRID_CONFIG_LOCAL_INDEX020.md, blob 288451808a860ff92a4968b1e0161680bf08b879; exact executed source experiments/tmr/tmr3_hybrid_worklocal020.cjs, blob 6797f2571336340c9b02b17ffc9f221512c725a6; immutable raw results/raw/tmr/2026-11-14_0731_TMR3_HYBRID_WORKLOCAL020_RAW.json, blob 45bf1f490b1d5913deb20ee59b1b92236c0462bd. All verified by GitHub readback.

**PREFLIGHT:** authoritative replacement directive first and rechecked unchanged SHA 47459817e66dccf1f3079e6c724c0fd2643e7bc4; complete proof1 28,714 characters SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343; complete proof2 authentic Git blob 1,051,196 characters SHA 930c5eeddafce656717f28055a7a9a755f44737c; complete canonical main.tex Git blob 2,539,489 characters SHA f80790efd768574555a85703a14820e1bed56b70; root AGENTS/CODEX/pnp skill, latest issue #3, all five TMR handoffs, peer original reports and relevant historical restrictions, primary FLMV/MNSW/Borodin-Cook/Fischer model sources. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** main.tex reserved to TMR-5 synthesis. No task changes.

**EXACT MISSING BRIDGE:** General 3-SAT decision does not require servicing a future arbitrary coordinate query. This new bound is linear, not superpolynomial. Uniform unrestricted P != NP or P=NP remains OPEN.

**NEXT:** TMR-1/TMR-5 verify min cardinality, same-source witness and transition coupling, then independently redteam any SAT-to-INDEX necessity claim with cached input, Horn/2-SAT/GF(2) summaries, and alternative encodings.

END_OF_HANDOFF::TMR-3::2026-11-14_0731_PST

---

# TMR-3 CURRENT handoff | 2026-11-14 06:34 PST | ALL-TAPE LOCAL-VIEW DELAYED INDEX019

**NEW TMR3-FLV19 CANDIDATE/RESTRICTED, TMR-1/TMR-5 independent review requested:** For ONE fixed finite total deterministic multitape machine using r>=1 physically locally moving nonsensing original-source heads and w>=0 local writable work-tape heads with alphabet size <=g, after *arbitrary paid preprocessing with NO SPACE LIMIT*, a later externally delivered x-independent INDEX query p must return x[p] on all binary L-bit sources. If ALL queries finish in <=t physically charged transitions, q fixed control states and source alphabet size a<=5 yield

$$
2^L \le q\,a^{r(2t+1)}(g+1)^{w(2t+1)}.
$$

Sharpened far-position/source-bit accounting gives

$$
2^L\le q(L+2t+4)^r 2^{r(2t+1)}(g+1)^{w(2t+1)}.
$$

Set D=r+w log_2(g+1). For fixed r,w,q,g, t>=(1/(2D)-o(1))L **regardless of retained writable storage S**, even S>=L or exponentially larger. Complete all-step coupling: every tape head sees only its original 2t+1-cell local neighborhood, and equal initial local fingerprints imply identical query transitions, writes, and both-bit terminal output for every p, forcing injectivity across 2^L source strings. Absolute head-coordinate sensing, external advice or unit-cost random access are explicitly excluded. This improves *workspace scope* versus TMR-3/018, TMR-5/017 and TMR-1/020 without claiming their sharper sublinear-S leading constants.

**DIRECT EXECUTED native Node.js v22.16.0, COMPUTATIONAL:** 512 L/r/w/window/mode cases; 451 local-fingerprint collisions and 451 identical adaptive physical-current-cell probe traces, including 128 far-coordinate cases; 8,190 full-L-cell copy exactness checks; 0 assertions. Source SHA c8eea121a8979ae6aaf08a876f5a5bba61191460; raw SHA c64b750db441ff0c48fd466c94179fbcac5d5934. Preprocessing uses host arithmetic, not a charged arbitrary-machine TM compiler. A full physical cache avoids the older small-S hypothesis but not the new local-query bound.

**GITHUB MAIN VERIFIED ARTIFACTS:**
- report research/agents/tmr-3/2026-11-14_0634_TMR3_FULL_TAPE_LOCAL_VIEW_INDEX019.md
- executed source experiments/tmr/tmr3_local_fingerprint019.cjs
- immutable raw results/raw/tmr/2026-11-14_0634_TMR3_LOCAL_FINGERPRINT019_RAW.json

**READS:** authoritative replacement directive first/rechecked SHA 47459817e66dccf1f3079e6c724c0fd2643e7bc4, complete proof1 28,714 characters SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343, complete proof2 authentic Git blob 1,051,196 characters SHA 930c5eeddafce656717f28055a7a9a755f44737c, complete canonical main.tex Git blob 2,536,131 characters SHA f0054c990e11602b4b60ead3bccffa73f11d0d7b, AGENTS/CODEX/skill, issue #3, all latest TMR handoffs and original TMR-1/020, TMR-5/017, TMR-3/018/017/002, primary FLMV/MNSW/Borodin-Cook bibliographic sources. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** TMR-5 owns main.tex synthesis; no task modifications.

**EXACT GAP:** This is still a delayed two-phase INDEX service, not a representation-independent SAT decision-time lower bound. The bound is only linear, not superpolynomial, and ordinary SAT solvers need not service external late index requests. P versus NP remains OPEN. **NEXT:** TMR-5 hostile audit of arbitrary mutable work-tape t-local replay; TMR-2 find a genuine all-machine SAT-semantic bridge or counterexample.

END_OF_HANDOFF::TMR-3::2026-11-14_0634_PST

---

# TMR-3 CURRENT handoff | 2026-11-14 05:29 PST | POST-PREPROCESSING INDEX PORT BARRIER018

**NEW TMR3-IC18 CANDIDATE/RESTRICTED, complete proof pending independent TMR-5/TMR-1 audit.** Fix ONE deterministic locally moving source-head machine A with q control states, h writable tapes, alphabet <=g; phase 1 preprocesses arbitrary L-bit x into <=s visited writable cells, source head reset to LEFT; only after preprocessing is a paid binary index p supplied on a separate read-only query tape. A must return x_p for ALL x,p, with arbitrary rereads, compression and recomputation. With M_A(s)=q(2s+3)^(3h)g^s and b=floor(log_2 M_A(s)), whenever L>b there exists SAME-machine x,p whose physical query phase needs >=L-b transitions. Complete-work-config collision on 2^(b+1) suffixes sharing a prefix of length L-b-1 and physical head-reach prove the result. For s=o(L), worst-case query cost >=(1-o(1))L. Phase delay/reset are REAL interface restrictions; no general SAT lower bound, no all-polynomial S coverage, no compulsory retrieval for an arbitrary SAT decider. s=Theta(L) whole-cache TMR-3/017 evades premise.

**Actually executed and PUBLISHED hosted V8, COMPUTATIONAL:** 192 (L,s,sketch) exact collisions, 1,359 tracked physical prefix movements, 2,046 full-copy injectivity controls, 5 SAT source controls and 31 one-bit opposite-label proper 3CNF controls, zero assertions. Independently written native CPython ran 192 finite collisions, zero failures, LOCAL ONLY. No physical generic TM compiler or native Node execution. Code experiments/tmr/tmr3_postprep_index_cache018.cjs; raw results/raw/tmr/2026-11-14_0529_TMR3_INDEX_CACHE018_RAW.json; report research/agents/tmr-3/2026-11-14_0529_TMR3_POSTPREPROCESS_INDEX_CACHE_BARRIER018.md.

**Preflight:** directive SHA 47459817e66dccf1f3079e6c724c0fd2643e7bc4 first/rechecked; complete proof1 28,714 chars SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343 and proof2 Git blob 1,051,196 chars SHA 930c5eeddafce656717f28055a7a9a755f44737c; main.tex 2,533,636 chars SHA 867c9b7512a51d59a50c479e81dda6c65615026f; root AGENTS/CODEX/skill, issue #3, five handoffs, ORIGINAL TMR-3/002,/008,/017, TMR-5/015, TMR-2/019 and original primary Yao/FLMV/Hong-Kung/Borodin-Cook abstracts. TRACKERS REVIEWED; NO MATERIAL CHANGE. Canonical main.tex unchanged. NO task changes.

**Peer handoff:** TMR-5 audit fixed-prefix collision and complete-state counting; TMR-1 audit reset/delayed index; TMR-2 test a REAL SAT decision computational-processing transfer; TMR-4 charge every stage including query receipt. All load-bearing unrestricted arrows OPEN.

**Next:** falsify or prove a necessity transfer from SAT semantic decision to post-preprocessing bit-index retrieval that withstands arbitrary interleaving, algebraic invariants and s=Theta(L) caching.

END_OF_HANDOFF::TMR-3::2026-11-14_0529_PST

---

# TMR-3 CURRENT handoff | 2026-11-14 04:40 PST | CHARGED MOVING-WINDOW CACHE FRONTIER017

**NEW TMR3-MWC17 CANDIDATE/RESTRICTED; TMR-5/TMR-1 independent review requested.** For ANY one fixed finite total uniform deterministic h-read-only-input-head A, fixed alphabets and local heads, and a FIXED uniformly computable R(L) with 1<=R<=L+2, a single-original-input-head fixed deterministic B_{A,R} maintains h physically charged writable cache windows. Every A source symbol is obtained from the corresponding actual cache work-head cell; each cache symbol was previously copied from the current actual read-only input-head position. Every A work-tape step and SAT/UNSAT/MALFORMED terminal is simulated. On the SAME x, for fixed c_A,
$$
T_B(x)\le c_A[(L+2)+(T_A(x)+1)(1+(L+2)/R(L))],
\qquad
S_B(x)\le S_A(x)+c_A[R(L)+\lceil\log_2(L+2)\rceil].
$$
After a centered/clamped source-window refresh, that virtual head must move at least floor((R-1)/2)+1 steps before needing another refresh, unless R=1 when one move suffices. Across h fixed heads there are at most h(1+2T_A/R) reloads, each O(L+2) charged moves/reads/writes/index arithmetic. Cached logical steps take O_A(1). R=ceil sqrt(L+2) yields O_A(L+sqrt(L)T_A) time and O_A(sqrt L+log L) overhead space; R=L+2 gives O_A(L+T_A) time/O_A(L) extra workspace. This is a NEW GENERIC MULTIHEAD MODEL-TRANSFER ACHIEVABILITY FRONTIER, NOT compulsory SAT cost, and not the earlier easy equality-family specialized cache.

**Executed exact hosted V8 source, COMPUTATIONAL:** 11,636 checked traces, 872,256 virtual steps, 2,616,768 cached-vs-direct symbol checks, 2,062,686 current-cell physical source reads, 81,279,763 paid physical source-head moves, 911,339 cache reloads, 3,688,034 cache-head moves, 173,875,577 conservatively charged micro-operations, zero assertions. Exhaustive x of lengths <=8, longer controls through 1023, 1/2/3/sqrt/quarter/half/full-window regimes, reversible and data-dependent head motions. Hosted V8 direct instrumented source-port test, NOT native Node, general TM instruction-table compiler or SAT solver benchmark. Binary origin arithmetic O(log L) is conservatively CHARGED in the emulator, justified symbolically rather than compiled. TMR-5/015's prior TMR-3/016 off-head-source-read bug is avoided: fill always reads BEFORE the original physical head moves.

**Readback VERIFIED on GitHub MAIN:**
- report research/agents/tmr-3/2026-11-14_0440_TMR3_MOVING_WINDOW_CACHE_FRONTIER017.md (blob 06e7cfd2527d863a2758501514f8b9eba24230ad)
- source experiments/tmr/tmr3_window_cache_onehead017.cjs (blob 2f60b88ca06687947dc6c5275f08418c27f25972)
- raw results/raw/tmr/2026-11-14_0441_TMR3_WINDOW_CACHE017_RAW.json (blob db1260dd8e56d6103aa044d68b34d6434cbc7785).

**Preflight:** directive recovered/rechecked SHA 47459817e66dccf1f3079e6c724c0fd2643e7bc4, complete root proof1 SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343 and recovered full proof2 Git blob SHA 930c5eeddafce656717f28055a7a9a755f44737c, full main.tex Git blob SHA 91b4e582c16cb7f60c9aa1ea2aebf09cd4caa2c6, root AGENTS/CODEX/skill, current issue #3, all five handoffs, original TMR-3/002,/008,/016 and TMR-5/015; primary FLMV JACM 2005, Hong/Kung STOC 1981 and Borodin/Cook SIAM 1982 consulted at THEIR actual models. TRACKERS REVIEWED; NO MATERIAL CHANGE. Root main.tex TMR-5 synthesis unchanged. No task/schedule mutation.

**FALSIFIERS AND GAP:** R=L retains a full charged copy of original input and bypasses repeated original-source rereads; no uniform per-virtual-read Omega(L) charge survives. Arbitrary compact/Horn/XOR/treewidth, algebraic, sharing, preprocessing and recomputation remain allowed in A. This is an upper simulator for two different machines, not a SAME-MACHINE SAT lower bound and excludes zero polynomial (T,S) pairs. FLMV small-space exclusions cannot be extended to arbitrary polynomial space from this result. P versus NP OPEN.

**Next:** TMR-5 independently review literal window-centered/clamped reload spacing and all-head cost compilation; TMR-1 audit one fixed uniform R(L) and what cache size does to claimed model equivalences. Seek a post-acquisition compulsory-processing distinction compatible with the R=L source-copy upper.

END_OF_HANDOFF::TMR-3::2026-11-14_0440_PST

---

# TMR-3 CURRENT handoff | 2026-11-14 03:34 PST | AMORTIZED POPCOUNT ONE-HEAD BRIDGE016

**NEW TMR3-AP16 CANDIDATE/RESTRICTED pending TMR-5 or TMR-1 independent review:** A fixed total uniform $h$-locally-moving-source-head multitape decider $A$ admits a fixed ONE-original-input-head simulator $B_A$ with $T_{B_A}(x)\le c_A(L+2)(T_A(x)+1)$ and $S_{B_A}(x)\le S_A(x)+c_A\lceil\log_2(L+2)\rceil$. This improves TMR-5/014's $O_A(L\log L)$ per-logical-step charge to **$O_A(L)$** while keeping $O_A(\log L)$ extra visited writable cells. Source fetch uses a binary countdown plus an actually charged unary-popcount work-head to detect zero in $O(1)$ after each decrement. The crucial identity $\sum_{j=1}^p\nu_2(j)=\sum_{r\ge1}\lfloor p/2^r\rfloor\le p$ amortizes the paid local binary carries. The explicit serialized fetch ledger is $5w+5\sum_{j=1}^p\nu_2(j)+6p+1\le11p+5w+1$. Every original work transition and input reread remains charged. No SAT lower bound.

**ACTUALLY EXECUTED hosted V8, COMPUTATIONAL:** 49,833 source-position fixtures including all binary strings through length 11, 15 longer-length control sets and restricted valid three-variable 3CNF SAT/UNSAT strings; 4,244,205 charged micro-operations, 245,203 trailing-zero carry movements, positions through 1,025, 2,049 direct valuation-identity checks; zero assertions. The full arbitrary-$A$ TM instruction compiler and $O(w)$ initialization are justified symbolically, not compiled or independently replayed. Source `experiments/tmr/tmr3_amortized_countdown_bridge016.cjs`; immutable raw `results/raw/tmr/2026-11-14_0333_TMR3_AMORTIZED_COUNTDOWN016_RAW.json`; report `research/agents/tmr-3/2026-11-14_0334_TMR3_AMORTIZED_POPCOUNT_ONEHEAD_BRIDGE016.md`.

**Corpus:** 2026-11-13 12:49 PST directive first and rechecked, both complete trackers authenticated (proof2 Git blob recovery), full main.tex Git blob, AGENTS.md/CODEX.md/research skill, newest five TMR handoffs and issue #3 through TMR-2/017, original TMR-5/014 report/executable/raw, TMR-3/015 and TMR-2/017 report, primary FLMV JACM 2005. TRACKERS REVIEWED; NO MATERIAL CHANGE. No edits to root main.tex, no schedule changes. P versus NP OPEN.

**ONE NEXT TARGET:** TMR-5 check exact unary-head zero detection and constant-factor physical microcode, then assess whether the same-source simulator construction supports stronger restricted time-space claims without imposing unnecessary trace playback.

---

# TMR-3 CURRENT handoff | 2026-11-14 02:37 PST | FINITE-HEAD CONFIGURATION FRONTIER015

**New mathematical claim TMR3-MCF15: CANDIDATE/RESTRICTED pending TMR-1/TMR-5 independent review.** For any one fixed halting deterministic machine with h independent locally moving read-only input heads, b one-way locally moving writable work tapes, finite state Q and work alphabet Gamma, on the SAME immutable L-bit input and SAME executed resource realization,

$$
T_A(x)\le |Q|(L+2)^h(S_A(x)+1)^b|\Gamma|^{bS_A(x)}.
$$

This is elementary complete-configuration counting and is an **upper bound on possible halting time given space**, not a lower bound on SAT decision time. It implies T<=L^{h+o(1)} if S=o(log L); if actual time >=(L+2)^{h+epsilon} on unbounded lengths then S>=epsilon*log(L+2)/(b log|Gamma|)-O_A(loglog L) for b>=1. Such actual long time is NOT proved necessary for SAT.

**Sharp matching restricted controller:** For every fixed h, one fixed finite-control h-input-head machine with **zero visited writable work cells** decides SAT/UNSAT/MALFORMED for arbitrarily long proper three-variable 3-CNF sign streams and takes exactly T=2*sum_{j=1}^h(L+1)^j+1. Each positional counter advance, physical input-head movement and reset is charged. Its h read-only head positions carry h log L bits as a *model feature*. TMR-5/013 already derived the exact nested odometer, and TMR-1/016 already gave ordinary one-head **paid O(log L) writable-counter** simulation. The new increment is the matching finite-head configuration ceiling and quantitative conditional workspace inversion. No unrestricted 3-SAT algorithm or lower bound is claimed.

**Actual hosted V8 executed evidence: COMPUTATIONAL.** Exact published standalone source: experiments/tmr/tmr3_multihead_config_frontier015.cjs, Git blob 5b25561cb9143ba771fcc6ee8721b494cafc68ae. Exact raw: results/raw/tmr/2026-11-14_0234_TMR3_MULTIHEAD_CONFIG015_RAW.json, Git blob f15360582f2a9f5a50e363dbcdafc550ce1a9645. All binary words length 0..8 for h=1..4, plus genuine restricted SAT, UNSAT, malformed and larger controls; 2,071 source/head cases, 6,700,071 physical transitions, 6,698,000 unique audited movement states, 15,249 current-cell initial-scan reads, SAT 302 / UNSAT 11 / MALFORMED 1,758, zero failures. 36 additional BigInt inequality inversions, not physical executions. An earlier too-large host Set failed; range corrected before successful publication. No OS native Node, independent Python, general 3-SAT machine compiler, full repo preflight, validator or LaTeX execution.

**Readback-verified report:** research/agents/tmr-3/2026-11-14_0237_TMR3_FINITE_HEAD_CONFIGURATION_FRONTIER015.md, Git blob e47873f89cfd5cf3018616e3a163abef556ac4a5. Direct primary scopes: FLMV JACM 2005 random-access low-space SAT tradeoff; Hennie 1965 one-tape crossings; Borodin-Cook 1982 general sequential **sorting** TS lower bound. No imported unrestricted SAT implication. Historical LEAD-0030 inflation wrapper, TMR-3/002-003/013-014 and peer /013-/016 preserved.

**Corpus and coordination:** The 2026-11-13 12:49 PST replacement directive SHA 47459817e66dccf1f3079e6c724c0fd2643e7bc4 read first and rechecked. Full proof1 28,714 chars SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343; full proof2 recovered Git blob 1,051,196 chars SHA 930c5eeddafce656717f28055a7a9a755f44737c; main.tex full recovered blob 2,525,134 chars SHA d3db01d221df39f096f31237643268132edfcd87; AGENTS.md, CODEX.md, pnp skill, issue #3 through TMR-1/016, all current TMR handoffs and relevant ORIGINAL historical proofs/code inspected. **TRACKERS REVIEWED; NO MATERIAL CHANGE** to proof1/proof2. No main.tex edit (TMR-5 synthesis) and no tasks/schedules changed.

**Independent audit request:** TMR-1/TMR-5 verify that the h-head model and finite-control nested odometer match the bound and that same-source work-head configuration counting is valid. TMR-4 should examine whether such upper time envelopes have any usable sound full-trace potential without conflating capacity and compulsory work.

**One next target:** prove and charge the ordinary one-original-input-head simulation of h read-only positional heads, then seek an actual obligatory processing-cost lower bound insensitive to arbitrary compact algorithms. Every all-exponent SAT arrow and P versus NP remain OPEN.

END_OF_HANDOFF::TMR-3::2026-11-14_0237_PST

---

# TMR-3 CURRENT handoff | 2026-11-14 01:30 PST | MINIMAL TWO-CROSSING PHYSICAL SUFFIX DEPENDENCE014

**NEW TMR3-2C14 CANDIDATE/RESTRICTED, TMR-5/TMR-1 review requested:** For each one fixed correct total local-input-head all-length SAT machine A, a fixed uniform wrapper B_A performs exactly ONE full outward scan and ONE full return, both physically charged, before running A. On the SAME source x, T_B=T_A+2(L+1), S_B=S_A. Its genuine finite-control crossing-state projection at the cut after bit i is c_i=(x_i,XOR_{j=1}^L x_j): TWO actual prepass crossings per cut on **EVERY source**, independent of its parity and label, and all codes conditionally prefix-free with R_i=L and D=L. One crossing cannot encode unread suffix information at its own cut with one locally moving read-only head, so 2 is sharp in this model.

**STRONGER fully decided restricted model:** One fixed finite-state, NO visited writable cell decider for 3-CNF clauses over exactly x0,x1,x2 of arbitrary clause count can maintain its 8-bit forbidden-assignment mask *while making the outward parity sweep*, return to the left marker retaining the complete SAT/UNSAT/malformed result, then halt. Entire execution has exactly two crossings per data cut, T_C=2(L+1)+1, S_C=0, every valid sign-stream formula length L=3r, r unbounded. Actual crossing codes still have D=L. Restricted regular 3-CNF family is NOT NP-complete. This strengthens TMR-2/015's 2-or-4 prepass by removing conditional extra passes and proves zero-space, linear-time full-decision control. It does not invalidate ID12, injective full-splice codes, or any general SAT lower bound.

**Native executed exact CPython source:** experiments/tmr/tmr3_two_crossings014.py blob 5f830dda0c9750e6f83331f9168c9fcf13abad82. All binary sources lengths 0..15: 65,535; all eight-mask UNSAT permutations: 40,320; future-flip/cut comparisons: 6,096; charged local head moves: 3,989,618; actual forward/reverse cut events: 3,777,866; SAT 37,470, UNSAT 40,320, malformed 28,086; zero failures. COMPUTATIONAL, not arbitrary-A TM compiler.

**Verified report:** research/agents/tmr-3/2026-11-14_0130_TMR3_TWO_CROSSING_MINIMAL_SUFFIX014.md, blob 209aca92117b9bafd066f39a3de86ae8e8f0253b. **Verified raw:** results/raw/tmr/2026-11-14_0130_TMR3_TWO_CROSSINGS014_RAW.json, blob 90ecc1ee5b6d404cf1cb487cc8c3bf68891da249.

**Source recovery:** Controlling directive and complete proof1 (28,714 chars), proof2 via authentic Git blob (1,051,196 chars), main.tex via authentic Git blob (2,522,180 chars), issue #3 through TMR-2/015, AGENTS, CODEX, skill, all five handoffs, original TMR-3/011-/013, TMR-2/015, TMR-5/012, primary Hennie 1965 catalog and FLMV 2005 official theorem. TRACKERS REVIEWED; NO MATERIAL CHANGE. Canonical main.tex left to TMR-5, no schedules changed, P versus NP OPEN.

**ONE NEXT TARGET:** TMR-5 or TMR-4 independently review the sharp crossing claim and test whether a cost-sound phase-invariant **normalized complete crossing code** can remove the cheaply propagated parity field without losing an exact source-splice theorem. Prove all-step charged transfer before any general lower-bound use.

END_OF_HANDOFF::TMR-3::2026-11-14_0130_PST

---

# TMR-3 CURRENT handoff | 2026-11-14 00:37 PST | BOUNDED-LOOKAHEAD KRAFT/HÖLDER013

**NEW TMR3-LA13 CANDIDATE pending TMR-5/TMR-2 independent mathematical review:** For independent uniform q_i-bit blocks X_i and conditionally prefix-free injective per-index codes c_i depending on X_1,...,X_min(K,i+r) only (entire past plus at most r future blocks), letting ell_i be the output length, for all b>0:
$$
\Pr\big[\sum_i\ell_i<\sum_i q_i-b\big]\le2^{-b/(r+1)}.
$$
For equal q, $\Pr[(1/K)\sum_i\ell_i<q-\log_2(1/\delta)]\le\delta^{K/(r+1)}$. Proof: conditional Kraft makes $Y_i=2^{q_i-\ell_i}$ have $E[Y_i|X_{<i}]\le1$. Partition indices modulo r+1 to get product supermartingale expectations <=1, then Hölder and Markov. **Sharpness:** consecutive independent groups of r+1 blocks each use the TMR-3/012 global-XOR conditional code within that group, producing exact tail $p^{K/(r+1)}$, $p=2^{-t}-2^{-q}$, and ratio to $\delta^{K/(r+1)}\to1$ for fixed K,r,t as q grows, $\delta=2^{-t}(1+2^{-q})$. This repairs overstrong "disjoint blocks imply concentration" by identifying the missing bounded-future-dependence premise. Physical two-way crossings generally depend on the entire future source; no SAT transfer is proved.

**ACTUAL executions:** Published exact hosted-V8 JavaScript: 14 exhaustive q,t,K,r group configurations, 218,752 global vectors, 19,554 conditional fibers, 294,488 generated codewords, plus 12 adaptive-code inequalities/49,152 source-vector comparisons and 5,329 fibers; zero failures. Separately authored and **natively executed CPython 3.13.5** reproduces all 14 group probabilities and all 12 adaptive inequalities, zero failures, local outbox only. The q=4,t=2,K=4 noncausal global-XOR adversary has p=0.1875, falsifying spurious r=0 bound 0.0049782395362854 while respecting r=3 bound 0.265625. Finite tests COMPUTATIONAL. No physical SAT TM or OS-native Node execution.

**Readback-verified GitHub main artifacts:** report `research/agents/tmr-3/2026-11-14_0037_TMR3_BOUNDED_LOOKAHEAD_KRAFT013.md` blob 0572103a2af05e58298994da88ebc3a7f3ac23e8; executed JS `experiments/tmr/tmr3_lookahead013.cjs` blob 13d594f37de94d8664a27b10cf913f2b422d933a; raw `results/raw/tmr/2026-11-14_0035_TMR3_LOOKAHEAD013_RAW.json` blob adbed1dcbffac34ce2dfa654c0ec9a1036ecdf18.

**Corpus:** Superseding directive first/rechecked SHA 47459817e66dccf1f3079e6c724c0fd2643e7bc4; proof1 authentic full 28,714 chars SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343, proof2 authentic Git blob full 1,051,196 chars SHA 930c5eeddafce656717f28055a7a9a755f44737c; main.tex authentic full 2,518,238 chars blob 0233cb0ca16a63a2a63a83af6a61ffe985632945. AGENTS, CODEX, pnp skill, current issue #3, all five latest handoffs and original TMR-3/008-/012, TMR-5/009, historical FLMV 2005 exact model checked. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** No canonical main.tex edit or scheduled-task changes. P versus NP OPEN.

**ONE NEXT TARGET:** TMR-5/TMR-2 independent review of LA13 and exponent sharpness. Then test whether the *complete* physical two-way crossing-code records of arbitrary SAT machines ever satisfy a nontrivial bounded-future radius after fully charged rereads. If not, construct a physical paid-reread counterexample and retain all-exponent processing lower bound OPEN.

END_OF_HANDOFF::TMR3::2026-11-14_0037_PST

---

# TMR-3 CURRENT handoff | 2026-11-13 23:31 PST | DISJOINT CONDITIONAL KRAFT CORRELATION012

**NEW TMR3-DC12 CANDIDATE** pending TMR-5/TMR-2 mathematical review; finite codebook tests COMPUTATIONAL. Independently uniform disjoint q-bit blocks X_1,...,X_K DO NOT force aggregate crossing-code tail concentration if each cut's valid prefix-free codebook may condition on all other blocks. Split each block into t high bits and ell=q-t low bits. Let E={XOR high=0^t, XOR low !=0^ell}. At every cut i, conditional on X_-i, assign all 2^ell-1 satisfying Xi short ell-bit words except prefix 1^ell, and all other Xi long words 1^ell||Xi. Codebooks are prefix-free for EVERY conditioning, yet all K code lengths are identical on every global X. Their low-tail event has probability p=2^-t-2^-q versus delta=2^-t(1+2^-q), and p/delta->1 at fixed t, q->infinity for arbitrary K. Strengthens TMR-5/009's same-codebook example by using different disjoint independent conditioned free bits. It falsifies any K-fold probability amplification based solely on disjoint supports plus marginal conditioned Kraft. DOES NOT instantiate actual physical SAT crossing sequences or refute TMR-3/010.

**Executed exact published JS function in hosted V8:** 15 exhaustive (q,t,K) cases, 474,176 global tuples, 34,192 conditional fibers, 1,378,944 codewords, 1,344,752 adjacent prefix checks, 15 controls against false delta^K independence and 0 failures. The published exact function body is the executed V8 body; native Node was NOT executed. Source `experiments/tmr/tmr3_disjoint_conditional012.cjs`, raw `results/raw/tmr/2026-11-13_2329_TMR3_DISJOINT_CONDITIONAL012_RAW.json`, report `research/agents/tmr-3/2026-11-13_2331_TMR3_DISJOINT_CONDITIONAL_CORRELATION012.md`, all on main after GitHub readback. Original peers: TMR-3/010,/011, TMR-5/009, TMR-4/013, TMR-1/013, TMR-2/013. Primary FLMV 2005 random-access model/Theorem 1.1 inspected directly. No native clone/LaTeX build. TRACKERS REVIEWED; NO MATERIAL CHANGE; canonical main.tex untouched for TMR-5; no task change.

**ONE NEXT TARGET:** TMR-5 independently audit DC12, then derive actual full-crossing-sequence causal constraints, if any, beyond conditioned Kraft, without transferring easy-family source transport to unrestricted post-copy SAT processing. Same-machine unrestricted all-exponent SAT lower bound and P versus NP remain OPEN.

END_OF_HANDOFF::TMR3::2026-11-13_2331_PST

---

# TMR-3 CURRENT handoff | 2026-11-13 22:33 PST | FULL CROSSING AUDIT AND FALLBACK REPAIR011

**CS11 CANDIDATE/RESTRICTED pending independent TMR-5/TMR-1 review.** Self-contained symbolic audit of TMR-3/008's full physical crossing-list splice: if two accepted diagonals have identical full ordered crossing records, alternating left and right legal physical segments accepts a valid opposite-label hybrid, contradiction. All work-tape visited symbols, work-head positions, finite control, direction and count are essential. For locally moving fixed finite work tapes, prefix-free serialized complete crossing code has length at most d_A r_c(F)(S_A(F)+1). No one-pass restriction, assumed small workspace or per-cut different witness is used. The original strict 3-CNF source literal splice was independently reimplemented; the conditional TMR-3/010 aggregate Kraft route remains restricted and polynomial-strength. No all-exponent P != NP claim.

**Concrete narrow defect in TMR-3/008 Section 3:** literal dispatch "on ANY mismatch invoke exhaustive fallback" contradicts the advertised cheap bound on EVERY valid E(a,b): valid unequal bank sources are UNSAT and trigger 2^(5n) exhaustive candidate assignments. Repaired classifier: finish structure authentication, retain one-bit equal flag, return equal for any authenticated template, and use exhaustive general fallback ONLY on structurally nonmember sources. Original published source-level recognizer already classifies authenticated unequal banks correctly; this is a prose dispatch correction, not a mathematical lower-bound falsification. Physical bit parser upper exponent remains to be proved independently.

**Executed independent checks (native Python plus separate hosted V8 exact published JS):** 5,460 local-head/local-work-tape equality decisions (126 SAT, 5,334 UNSAT); 27 full crossing-codebooks, 492 codewords, 14,310 prefix-free pairs, 14,310 false projected control/head-only collisions, 14,310 true rejected mixed hybrids; independently reconstructed exact source splice: 27,612 physical cut comparisons, 21,826 opposite-label legal hybrids across 1,533 boundaries; n=1,2,3 brute-force valid UNSAT fallback required 32/1024/32768 candidate trials. ZERO assertions failed. Finite evidence COMPUTATIONAL, no arbitrary SAT TM execution. Published exact JavaScript, not a wrapper; separate native Python implementation is local-only.

**Readback verified main publications:**
- Report research/agents/tmr-3/2026-11-13_2233_TMR3_CROSSING_SPLICE_AUDIT011.md (Git blob f25bbb0a6afbe665c0e3ae63e13017c49d0473c9).
- Executable experiments/tmr/tmr3_crossing_replay011.cjs (Git blob f286ae9fc30679c654109220a5fa38d37d8873c0).
- Raw results results/raw/tmr/2026-11-13_2233_TMR3_CROSSING_REPLAY011_RAW.json (Git blob 935f5a81321157f87bc3de65b8c770b4f09d4abb).

**Preflight:** authoritative TMR replacement directive, both full proof trackers (proof2 authentic Git blob 1,051,196 characters), full authentic root main.tex (2,511,782 characters), issue #3, AGENTS/CODEX/research skill, five peer handoffs and original TMR-3/002,/008,/009,/010, TMR-5/009 and TMR-1/012 reports were read. Primary Hennie 1965, FLMV 2005 and Borodin-Cook 1982 model scopes independently checked. TRACKERS REVIEWED; NO MATERIAL CHANGE. Canonical main.tex left to TMR-5; no schedule changed. Local project preflight/LaTeX compile not executed because no network clone.

**ONE NEXT TARGET:** TMR-5 audit every crossing state/coding step and authenticated UNSAT dispatch, then challenge any post-acquisition cost invariant on the source-copying simulator with arbitrary polynomial workspace. The unrestricted all-exponent SAT lower bound and P versus NP remain OPEN.

END_OF_HANDOFF::TMR3::2026-11-13_2233_PST

---

# TMR-3 CURRENT handoff | 2026-11-13 21:20 PST | AGGREGATE-KRAFT-TAIL010

**Substantive result:** TMR3-EM10 establishes the pure prefix-free aggregate exponential-moment inequality **PROVED/EXACT**. Its same-machine 3-CNF batched crossing implication is **CONDITIONAL/RESTRICTED** on original TMR-3/008's CANDIDATE full-configuration crossing-code/injective-splice lemma. For one fixed correct total deterministic multitape A with ONE locally moving read-only input head, the original E_{n,m}(a,a) SAT diagonal distribution satisfies, with q=floor(m/2), K=floor(n/m)(qg-1), L=13n+2+2ng, g=12(w+1), n>=m>=16:

$$
\Pr_a\left[T_A(F_a)(S_A(F_a)+1)\ge \frac K{d_A}\bigl(q-\log_2(1/\delta)\bigr)\right]\ge1-\delta.
$$

In particular, **same original lower product threshold** $Lm/(512d_A)$ has success probability at least $1-2^{-q/2}$, improving /009's $1-\min(1,K2^{-q/2})$. New $1-1/L$ sufficient threshold is $m>=4log_2(L)+2$ versus /009's $8log_2(L)+8$. This improvement is a Jensen + Kraft + Markov aggregate argument; it does not assert all K cuts are individually long.

**COMPUTATIONAL, verified on main:** 504 prefix-code cases; 5,292 full codebooks; 36,576 exhaustive assignments; 3,024 aggregate tail inequalities; zero failures. Deliberately non-prefix-free injective control produces probability one for a claimed 1/2 tail and Kraft sum 4.0625, demonstrating a load-bearing hypothesis. Published-exact hosted V8 function executed, not native Node or a physical TM. Source/raw/report each read back exactly after GitHub publication:
- `research/agents/tmr-3/2026-11-13_2120_TMR3_AGGREGATE_KRAFT_TAIL010.md`, blob e7d8a5c5c7e0e99415129dd7d8954d0c6ac7e3c6
- `experiments/tmr/tmr3_aggregate_kraft010.cjs`, blob 42fdc6861204b5a730492e2719f6825d3481d7e7
- `results/raw/tmr/2026-11-13_2120_TMR3_AGGREGATE_KRAFT010_RAW.json`, blob a3c7928ee080eb6ec5a68cd28363e1720b58578a

**Controls/gap:** m=1 interleaving, a second independent source head, indexed access, cache or copy with polynomial writable space, Gaussian elimination on XOR, Horn, 2-SAT, bounded treewidth, products/sharing, renaming, padding, auxiliaries, compact encodings and recomputation all defeat an unrestricted computational-process inference. No general P vs NP or all-exponent result; no assumption of polynomial upper bounds. LSPV-5/167's earlier crossing expectation and LSPV-1/197 union-based distribution were read as true predecessors, not assigned priority. Primary Hennie 1965, FLMV JACM 2005, Borodin-Cook 1982 publisher records checked. The new contribution is precisely the K-free tail for **aggregate** code lengths on one common execution.

**State/readback:** replacement directive 47459817e66dccf1f3079e6c724c0fd2643e7bc4; proof1.txt complete 28,714 characters SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343; proof2.txt complete authentic Git blob 1,051,196 characters SHA 930c5eeddafce656717f28055a7a9a755f44737c; main.tex complete authentic Git blob 2,507,300 characters SHA c0d657568af18ed0a2d17843b8ef0e6c11ac6327. AGENTS/CODEX/skill, latest issue #3 and five newest TMR handoffs reviewed. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** Root main.tex left to TMR-5 synthesis; no schedules or tasks touched. New 3-SAT implication remains conditional until TMR-5/TMR-1 independently reviews parent crossing lemma. P versus NP OPEN.

**Next one target:** TMR-5 independently reconstructs and attempts to falsify complete physical crossing-code prefix-free serialization, cut/splice injectivity and resource charges; then reviews EM10's aggregate tail. General representation-independent processing bottleneck remains OPEN.

END_OF_HANDOFF::TMR-3::2026-11-13_2120_PST

---

# TMR-3 CURRENT handoff | 2026-11-13 20:30 PST | TYPICAL-DIAGONAL-CROSSING009

**New scoped result:** CONDITIONAL/RESTRICTED distributional strengthening of TMR-3/008 BATCH8-LB, whose full physical crossing-code lemma is still CANDIDATE awaiting independent TMR-5/TMR-1 review. On one fixed correct total one-sequential-input-head multitape decider A, the same accepted diagonal F_a=E_{n,m}(a,a) obeys, for n>=m>=16 with uniform a, q=floor(m/2), g=12(ceil(log2(5n))+1), L=13n+2+2ng, K=floor(n/m)(q*g-1), and TMR3/008 constant d_A,

$$
\Pr_a[T_A(F_a)(S_A(F_a)+1)\ge Lm/(512d_A)]\ge1-\min(1,K2^{-q/2}).
$$

For m>=8log2(L)+8, this probability is >=1-1/L. The original proof gave merely EXISTS one difficult SAT diagonal. New argument: condition on the q independent first-bank variables for EACH physical cut; injective prefix-free full-configuration crossing codes give Pr[code length<q/2]<=2^{-q/2}; union bound over K<=L distinct cuts yields a single accepted realization with all crossings large. Count actual crossings once and charge peak writable space from the SAME run. Exact source family and all prior geometric restrictions are preserved. No arbitrary-workspace/all-exponent or indexed/multi-input-head bridge.

**Actual tests and publication:** independently written native Node v22.16.0 outbox and a separate published hosted-V8-compatible code passed 195 canonical source checks and 29,488 exact hybrid splices, of which 27,416 are valid different-prefix UNSAT and 2,072 equal-prefix SAT, with 0 final assertions and max L=77,058. This is finite source-level COMPUTATIONAL evidence, not TM crossing-record execution. One early harness-only m=1 cut-count assertion was corrected and fully rerun. Original report's upper-bound prose "any mismatch -> exhaustive fallback" requires grammar failure vs authenticated semantic inequality distinction; its original source code already distinguishes \`member:false\` from \`member:true,sat:false\`, so the upper bound is not refuted.

**GitHub MAIN verified:** report research/agents/tmr-3/2026-11-13_2030_TMR3_TYPICAL_DIAGONAL_CROSSING009.md, blob 57eb79bb32126035af94eb23ac9bebbd0592ef12; executable experiments/tmr/tmr3_typical_diagonal009.cjs, blob 5296e5beeeb59a1c3a78e163a6cb637eb330f6d0; raw results results/raw/tmr/2026-11-13_2030_TMR3_TYPICAL_DIAGONAL009_RAW.json, blob 0eb9438f916e16151fa8d4a5c3a0bab7307c860d. A separate native source/JSON remains local outbox and was not falsely claimed published.

**Corpus and status:** replacement directive read first and rechecked; proof1.txt 28,714 chars SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343; proof2.txt recovered full authentic Git blob 1,051,196 chars SHA 930c5eeddafce656717f28055a7a9a755f44737c despite blank file contents response; main.tex full recovered Git blob 2,504,241 chars SHA 103435a5c6ff2b02e2b975e7c00d37476d66b064; AGENTS.md/CODEX.md/skill, issue #3, current five TMR handoffs, TMR-3/002,/007,/008 originals, LSPV-5/167 original, TMR-2/010 and TMR-5/007, primary publisher FLMV/Borodin-Cook and Hennie records consulted. TRACKERS REVIEWED; NO MATERIAL CHANGE. Root main.tex left unchanged for TMR-5 synthesis. No tasks or schedules modified. P versus NP OPEN.

**ONE NEXT TARGET:** TMR-5 should independently prove or disprove the full crossing-code binary-length bound and all-cut splicing; any computational necessity past input transport must survive m=1 ordering, multiple input heads, INDEX, cached whole batches, Gaussian elimination and arbitrary polynomial work space.

END_OF_HANDOFF::TMR-3::2026-11-13_2030_PST

---

# TMR-3 CURRENT handoff | 2026-11-13 19:35 PST | BATCH-LOCALITY-TRADEOFF008

**NEW BATCH8-LB CANDIDATE pending TMR-5/TMR-1 review; exact source-level finite results COMPUTATIONAL. Unrestricted SAT all-exponent lower bound and P versus NP OPEN.**

**Quantitative new theorem candidate:** For the original proper 3-CNF equality source, batch m consecutive first-bank forcing blocks beside their m matched second-bank blocks. This is an EXACT whole-clause permutation with identical L=13n+2+24n(w+1) and SAT iff a=b. For ANY one fixed total correct deterministic machine A with ONE physically local read-only input head and finite ordinary work tapes, the full-configuration crossing-code and same-realization average argument gives (pending independent audit): for each n sufficiently large and each 1<=m<=n, some SAT diagonal F has **T_A(F)(S_A(F)+1)>=c_A Lm**. For each cut in the second half of each full first bank, floor(m/2) first forcing blocks are fully left and their matching second blocks wholly right; a valid UNSAT splice forces injective prefix-free crossing transcripts. Average *T(S+1)* over a single uniform diagonal distribution before taking any maximum. Small m handled by physical reach of the final source block. All real input crossings and all visited work cells charged. Not a random-access/dual-head theorem.

**Matching upper:** for fixed rational 0<=beta<=alpha<=1, batch m(n)=2^floor(alpha floor(log2 n)), cache r(n)=2^floor(beta floor(log2 n)). One fixed total all-input correct fallback machine authenticates every literal in local batch rescans, uses **T=O(L ceil(m/r))**, **S=O(r+log L)** on this family, and pays all reads, rewinds, scratch tapes, comparisons, counters and output. The lower/upper product matches for beta>0, up to a logarithmic factor for beta=0. For m=Theta(n^alpha), the restricted product bound is Omega(L^{1+alpha}/(log L)^alpha) and only excludes simultaneous exponent pairs k+s<1+alpha. S<=O(T) gives no stronger time bound than compulsory input traversal. Alternative source order, extra input heads, INDEX, algebraic summaries and unrestricted polynomial workspace remain all-program transfer blockers.

**ACTUALLY EXECUTED and readback-verified:** native Node v22.16.0 and separate hosted-V8 execution of exact published code, 2,468 canonical parse-and-answer cases (223 SAT/2,245 UNSAT), 1,232 exact original CNF multiset/permutation checks, 1,236 undersized-cache cases, 4,928 rejected structural negatives, 40 original-CNF exhaustive checks, 677,552,068 modeled adjacent source movements with 331,481,280 rewind moves, largest L=77,058, zero failures. These are NOT physical-TM transition traces; the exponential off-family fallback was not executed.

**Verified paths:**
- research/agents/tmr-3/2026-11-13_1935_TMR3_BATCH_LOCALITY_TRADEOFF008.md
- experiments/tmr/tmr3_batch_crossing008.cjs
- results/raw/tmr/2026-11-13_1935_TMR3_BATCH_CROSSING008_RAW.json

**Preflight:** Superseding directive first, rechecked SHA 47459817e66dccf1f3079e6c724c0fd2643e7bc4; full proof1 SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343; full proof2 authentic Git blob SHA 930c5eeddafce656717f28055a7a755f44737c; full main.tex authentic Git blob SHA 62c0c400a5eddfbdbdfa06fbabcf7bcee8b753be, all protocols, issue #3, five latest TMR handoffs, original TMR-3/002,/006,/007 and FLMV original model. TRACKERS REVIEWED; NO MATERIAL CHANGE. No main.tex or schedule/task mutation.

**Next:** TMR-5 audit variable-space prefix-free transcript coding, cut-and-paste legality, unconditional same-run expectation and matching fully charged uniform upper. Then seek a post-acquisition bottleneck immune to batch m=1, extra source heads, INDEX and Gaussian elimination. ALL unrestricted implications OPEN.

END_OF_HANDOFF::TMR3::2026-11-13_1935_PST

---

# TMR-3 CURRENT handoff | 2026-11-13 18:28 PST | CLAUSE-ORDER-LOCALITY007

**New CANDIDATE CO7, pending TMR-5/TMR-1 review. Finite independent original V8 source checks COMPUTATIONAL. General all-exponent SAT lower bound and P versus NP OPEN.**

**New exact same-formula representation counterexample:** For the original grouped-bank $E_n(a,b)$ strict proper-3CNF, binary width $w_n=\max(1,\lceil\log_2(5n)\rceil)$ and length $L_n=13n+2+24n(1+w_n)$, simply interleave each original four-clause first-bank forcing block with its matching original four-clause second-bank block. This produces $I_n(a,b)$ with EXACT original clause multiset, variable IDs, unary header, bit length and SAT iff $a=b$, only a clause-block order permutation. ONE fixed total correct deterministic all-input SAT machine with ONE physical locally moving read-only head, NO INDEX or second head, authenticates all bits and endmarker in a single sweep, compares immediately adjacent sign pairs, and uses a paid exhaustive fallback off-family. Symbolic physical resource upper on ALL interleaved family members: $T_D=O(L_n)$ and $S_D=O(\log L_n)$ on the SAME machine/input, so $T_D(S_D+1)=O(L_n\log L_n)=o(L_n n)$. This falsifies a clause-order-invariant/semantic transfer of grouped TMR-3/002's one-head crossing product, **NOT** its original ordered-source restricted claim. Machine-transition-table and TMR-5 audit pending.

**Executed and readback verified:** Standalone authored hosted-V8 source code experiments/tmr/tmr3_interleaved_clause_order007.cjs SHA befcb48e1e5383d88a95bf1454486f07b5579c90; raw results results/raw/tmr/2026-11-13_1828_TMR3_INTERLEAVED_ORDER007_RAW.json SHA 27919b256afa7cc7163c42957caa08cdd9e45a00; report research/agents/tmr-3/2026-11-13_1828_TMR3_CLAUSE_ORDER_LOCALITY_ESCAPE007.md SHA b21b48030c912d24f191849338fa3d1d148d8546. 1,420 valid sources (118 SAT/1,302 UNSAT), 1,420 byte-exact permutations, 7,100 structural mutant rejections, 40 small whole-CNF brute-force checks, 3,454,956 modeled local source moves, maximum L=166,402, 0 failures. Not instruction-level physical TM, not native Node or fallback execution; asymptotic upper is symbolic.

**Read:** Superseding directive first and rechecked SHA 47459817e66dccf1f3079e6c724c0fd2643e7bc4; full proof1 28,714 chars SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343, full proof2 Git blob 1,051,196 chars SHA 930c5eeddafce656717f28055a7a9a755f44737c, full main.tex Git blob 2,497,977 chars SHA 4e0dc7a81c3757289e87661b6df29e458cd03daa, root AGENTS/CODEX/skill, issue #3 through TMR-2/007, all five handoffs, original TMR-3/002,/006 and TMR-2/007, TMR-4/006, FLMV original author PDF Section 2.1 screenshot. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** main.tex left to TMR-5 synthesis. No schedules or agents modified.

**ONE NEXT TARGET:** TMR-5 independently inspect physically charged one-head interleaved parser, same-formula clause order proof and fallback. Construct or refute unavoidable post-acquisition computation charges not sensitive to input order, head multiplicity, INDEX access, Gaussian elimination or sharing. All unrestricted implications OPEN.

END_OF_HANDOFF::TMR3::2026-11-13_1828_PST

---

# TMR-3 CURRENT handoff | 2026-11-13 17:23 PST | TWO-LOCAL-HEAD-BOUNDARY006

**New TH6 mathematical construction CANDIDATE pending independent TMR-5 review; actual native Node finite source audit COMPUTATIONAL.** Every unrestricted all-exponent SAT lower-bound arrow OPEN; P versus NP OPEN. No schedules modified.

**Exact scope and substantive falsifier:** On the original strict proper 3-CNF equality family E_n(a,b), n>=1, width w=max(1,ceil(log2(5n))), h=13n+2, g=12(w+1), L=h+2ng, ONE fixed correct total deterministic 3-SAT machine with TWO independently moving **local, read-only input heads**, NO INDEX, and sequential writable work tapes achieves T=O(L) and S=O(log L) on every family member. Head 1 parses the header and first bank; head 2 is locally advanced to second bank start h+ng, then both heads validate their respective original banks synchronously, compare n sign pairs and check the right endmarker. All source bits authenticated. Total individual input movements 2h+3ng<=2L; amortized binary downcounter and O(w) verifier per constant-number-of-clauses give O(L) fully charged symbolic time, O(log L) all-live writable space. Charged exhaustive fallback off-family. This invalidates head-count-independent extrapolation of TMR-3/002 T(S+1)=Omega(Ln), but does NOT contradict its explicitly ONE-head assumption.

**Independent TMR-1/005 audit:** Read original report and code, verified original FLMV 2005 Section 2.1 author PDF including INDEX erasure. The 2n-erasing-jump plus native local-source scan upper O(L) and S=O(log L) is mathematically consistent at that indexed model, pending TMR-5 physical audit. TMR-5/004's O(L log L) erasing-index method is a valid nonoptimal upper, not a lower bound.

**Actual independently executed native Node v22.16.0:** 1,428 original valid E cases (126 SAT, 1,302 UNSAT), 9,996 mutation controls rejected, 20 original-clause brute-force controls, 9,619,896 emulated adjacent head movements, 6,315,408 reads, 22,692 pair comparisons, largest L=357,378, zero failures. No native physical multitape TM, general fallback, full repository preflight or LaTeX compile. Test host strings and Number arithmetic are COMPUTATIONAL only.

**Readback-verified main-branch artifacts:**
- Report research/agents/tmr-3/2026-11-13_1723_TMR3_TWOHEAD_SEQUENTIAL_PORT_BOUNDARY006.md, SHA b79c85dd8a407e916aa68cefb116997c85f0d171.
- Exact executed Node source experiments/tmr/tmr3_twohead_sequential_006.cjs, SHA 1e6c2f6d0b54e5fcf3e585d8324c7f3ee98e3d07.
- Immutable JSON results/raw/tmr/2026-11-13_1723_TMR3_TWOHEAD_SEQUENTIAL006_RAW.json, SHA 18f122f5a754a701a199c6a351d6808e96632bcf.

**Source preflight:** Superseding directive first and rechecked SHA 47459817e66dccf1f3079e6c724c0fd2643e7bc4, proof1 full SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343, proof2 full authentic Git blob SHA 930c5eeddafce656717f28055a7a9a755f44737c, main.tex full authentic blob SHA 873daeec6e11d4a7448f3b0547c9ed1ccfebd805, issue #3 1957 comments through TMR-2/006, root operating files, all five current peer handoffs, original TMR-3/002-003, TMR-1/005 report+code+raw, FLMV original Section 2.1. TRACKERS REVIEWED; NO MATERIAL CHANGE. Root main.tex left to TMR-5 ownership.

**TMR-5 audit target:** Verify exact pair-bank read-head configuration, physical logspace downcounter and bit verifier, no hidden source duplication, whole-string endmarker and malformed fallback, then acknowledge head-count scope firewall. TMR-1 should declare head multiplicity; TMR-4 charge each head position. Next substantive TMR-3 target: a whole-execution processing cost insensitive to source-head multiplicity, input indexing, compact GF(2), sharing, recomputation and arbitrary polynomial workspace.

END_OF_HANDOFF::TMR3::2026-11-13_1723_PST

---

# TMR-3 CURRENT handoff | 2026-11-13 16:20 PST | DUAL-INDEX-LINEAR-ESCAPE005

**Scientific status:** DI5-P / DI5-E symbolic upper constructions CANDIDATE pending TMR-5 review. Source tests COMPUTATIONAL (1,441 valid E pairs, 8,646 mutations, 17,292 assertions, zero failures; independent original-CNF brute force n<=2 passes 20/20). TMR-3/002 sequential crossing product remains previously reviewed PROVED/RESTRICTED. P versus NP OPEN.

**New scoped result:** On the EXACT existing proper-3CNF E_n(a,b) family with L_n=13n+2+24n(1+ceil(log2(5n)))=Theta(n log n), ONE fixed total correct all-length SAT machine with TWO paid persistent INDEX source registers has T=O(L_n), S=O(log L_n) on every family member, by fully authenticating all original source bits and using a second indexed port to compare each second-bank sign against the first-bank sign at offset h+i*g. Full paid exhaustive fallback off-family. Binary sequential address increments amortize O(1); n stride-g updates cost O(n log L)=O(L). If the INDEX tape is ERASED on query as in FLMV 2005, paid shadow reconstruction yields the distinct T=O(L log L), S=O(log L) variant.

**Exact transfer gap:** Both indexed T(S+1) upper products, O(L log L) and O(L log^2 L), are o(L n); hence TMR-3/002 sequential-source T(S+1)=Omega(L n) CANNOT transfer unchanged to indexed input. TMR-1/004's separately charged indexed-to-sequential simulator remains permissible. This is an EASY recognizable family and proves no unrestricted SAT lower bound or general polynomial solver.

**Published/readback verified:** research/agents/tmr-3/2026-11-13_1620_TMR3_DUAL_INDEX_LINEAR_ESCAPE005.md (blob a78b659760cde0bf346d9df6c7f7ada2f27d6bcf); experiments/tmr/tmr3_dual_index_linear005.cjs (blob 9b43e8ddad42ac9ebce54fc0b2397776c199723a); experiments/tmr/tmr3_dual_index_semantic_independent005.py (published); results/raw/tmr/2026-11-13_1620_TMR3_DUAL_INDEX_LINEAR005_RAW.json (blob 3ca57317b6463b6d8316669f689af20aac49a126). Full SHA+contents recovery of both proof trackers and canonical main.tex performed before work. TRACKERS REVIEWED; NO MATERIAL CHANGE; no root main.tex edit. No tasks or schedules changed.

**Primary model authority:** Fortnow et al., JACM 52(6), 2005, Section 2.1 author PDF https://lance.fortnow.com/papers/files/tst.pdf explicitly erases the INDEX tape after a jump; Hennie 1965 crossing work uses physical tape-access premises. Exact sources, model and test caveats in full report.

**Peer requests / NEXT OPEN:** TMR-1 audit two-port model, erasure and shadow address charges; TMR-2 audit information distinction/retention; TMR-4 audit all-transition charges; TMR-5 independently replay actual published code and inspect asymptotic address-head amortization. Seek a universal whole-execution cost stronger than a physically sequential transport requirement, surviving indexing, compact algebra, rereads and polynomial workspace.

---

## Preserved previous handoffs

# TMR-3 latest handoff | 2026-11-13 15:27 PST | BATCHED-SEQUENTIAL-PARETO-FRONTIER003

**Status:** NEW TMR-3, no schedule/task mutations. Upper construction CANDIDATE pending TMR-5 independent review; previous TMR-3/002 full crossing lower bound PROVED/RESTRICTED after independent TMR-5 review; finite regression COMPUTATIONAL. P versus NP OPEN.

**New scoped result:** For exact, recognizable strict proper-3CNF equality inputs $E_n(a,b)$, $L_n=13n+2+24n(1+\max(1,\lceil\log_2(5n)\rceil))$, and any fixed efficiently computable chunk function $\lceil c\log n\rceil\le\sigma(n)\le n$, ONE fixed total all-input-correct sequential-input-head machine authenticates the source, checks $n$ equality sign pairs in batches of $\sigma(n)$, and falls back to paid exhaustive SAT on nonmembers. Same family-input trace $T=O(L_n\lceil n/\sigma(n)\rceil)$, $S=O(\sigma(n))$ (including work buffers, counters, parser and input rewind costs). TMR-3/002's independently reviewed same-input lower product $T(S+1)=\Omega_A(L_n n)$ implies worst-case family time $\Omega_A(L_n n/\sigma(n))$ for ANY fixed correct machine satisfying a family-wide $O(\sigma(n))$ workspace budget. Thus the restricted family's entire logarithmic-to-linear work-space frontier is matched up to constants. This extends the known $\sigma=n$ matching upper, not the historical Hennie/Cobham/Santhanam crossing theory. It cannot transfer to indexed input or prove P != NP.

**Verified report:** research/agents/tmr-3/2026-11-13_1527_TMR3_BATCH_SEQUENTIAL_PARETO_FRONTIER003.md, blob 3769680d76b767b924e16aeded5dc992d66a1e7e.
**Verified independent V8-executable source:** experiments/tmr/tmr3_batch_frontier003.cjs, blob 25c36eb3a9daf2d1197b4e3419c863390692afff.
**Verified immutable raw:** results/raw/tmr/2026-11-13_1527_TMR3_BATCH_FRONTIER003_RAW.json, blob 672425942fd73eefef8c4dc1e4bce9e25212de73.

**ACTUALLY EXECUTED:** 1,364 exhaustive n<=5 original source pairs and 120 seeded n=6,8,16,32,64,128 pairs, 6,008 batch executions, 40,428 assertions, 4,452 malformed controls and 1,484 local sign-corruption controls, zero failures. V8 emulated 210,294,700 forward source-bit visits and 198,630,820 paid reverse moves. This was not a physical multitape TM emulator or OS Node CLI. Full preflight, report validator and LaTeX compiler unexecuted. Code and raw were published/read back exactly.

**Primary literature checked:** Hennie 1965 original off-line single-tape crossing sequences, distinct machine model. Fortnow-Lipton-van Melkebeek-Viglas JACM 2005 original Theorem 1.1, random-access SAT exclusion only for simultaneous $T=n^c$, $S=n^d$ with $c<\varphi$, $d>0$ appropriately chosen, NOT all polynomial workspace. Prior original project LSPV-5/167 and Claude ONETAPE-0001 read.

**Root scope:** Full proof1.txt and genuine 1,051,196-char proof2.txt Git blob inspected; full root main.tex 2,487,713 chars recovered by Git blob. TRACKERS REVIEWED; NO MATERIAL CHANGE. Existing TMR-3 main.tex ownership region left unchanged until candidate peer review and synthesis. Superseding directive rechecked; no scheduled tasks/agents modified.

**Peer requests:** TMR-5 independently review concrete streaming grammar checker $O(L_n)$ transitions with fixed tapes and work-head movements, and the use of TW2 under an on-family workspace cap. TMR-1 audit fixed-program quantifiers and comparison of all simultaneous time-space pairs; TMR-2 test cheap XOR/product alternate summaries; TMR-4 model every step and terminal label in an abstract cost transition graph.

**ONE next target:** identify a true all-algorithm, representation-independent global-consistency charge stronger than physical input transport, or falsify a proposed charge with compact algebra, caching, shared computation or indexed reading. The universal superpolynomial arrow remains OPEN.

END_OF_HANDOFF::TMR3::2026-11-13_1527_PST

---

# TMR-3 handoff | 2026-11-13 13:35 PST

**Current owner:** NEW TMR-3 Time-Space Tradeoffs, 2026-11-13 five-role replacement directive, j15marti/pnp main. **P versus NP OPEN.** No schedule changes or legacy role reuse.

**Substantive latest report:** research/agents/tmr-3/2026-11-13_1334_TMR3_SAME_INPUT_MULTIPASS_TRADEOFF001.md (readback verification pending on this handoff's creation). **CANDIDATE** complete symbolic proof pending TMR-5 independent review; **COMPUTATIONAL** exhaustive finite controls.

**Exactly scoped new theorem:** Let E_n(a,b) be the complete TMR-2 binary proper-3CNF equality family, L(n)=13n+2+24n(1+max(1,ceil(log2(5n)))). Restrict a fixed correct finite machine to *complete sequential one-way source sweeps* with no input observations during paid resets, fixed finite work tapes and full writable-cell/head counting. For some one *satisfiable* E_n(a_n,a_n), for every n and every fixed correct machine M,

$$
p_M(E_n(a_n,a_n))(S_M(E_n(a_n,a_n))+1)\ge c_M n,
$$

and on the *same input* $T_M(S_M+1)\ge c_M L(n)n=\Omega_M(L(n)^2/\log L(n))$. A complete variable-length communication transcript for each diagonal is injective: collisions splice into mixed UNSAT. The 2^n binary strings force one serialized transcript of >=n bits, each bounded by O(p(S+1)) including all work-head positions/control. This is a restricted *same-input* tradeoff, distinct from merely multiplying different worst-case resource witnesses.

**Model transfer firewall:** An indexed-input implementation checks the rigid equality family in O(L polylog L) time and O(log L) work/index cells, bypassing complete source sweeps. Standard arbitrary computations can also reread, copy or reencode the source without the prescribed p-phase structure. Prior LSPV-5/167 crossing sequences are acknowledged; no unrestricted theorem or novelty in equality/communication complexity claimed. Known FLMV near-linear SAT exclusions do not remove an arbitrary polynomial exponent. No P != NP claim.

**Executable and immutable raw:** experiments/tmr/tmr3_multipass_equal3_tradeoff.cjs and results/raw/tmr/2026-11-13_1328_TMR3_MULTIPASS_EQUAL3_RAW.json. Original GitHub readback of code reran in V8: all 1,364 E(a,b), 6,372 batch checks, 258 positive transcript checks, 516 four-sign-bit flips, 20 n<=2 full SAT brute checks, 37,263 assertions PASS. Virtual streaming emulator, not physical native TM instructions. Node CLI/preflight/checker not run.

**Peer tasks:** TMR-1 audit quantifiers and strict-class transfer. TMR-2 investigate an information-cost beyond input reads still necessary with arbitrary replay and compact summaries. TMR-4 instantiate a simulation that includes every two-way head move, work-copy and state conversion. **TMR-5 independently falsify** same-input variable-length transcript injection/cost, completed-sweep assumption, and duplication against LSPV-5/167.

**Canonical records:** Root proof1/proof2 fully read (the latter recovered from Git blob), root main.tex fully read by blob; TMR-3 has no authorized synthesis region yet. TRACKERS REVIEWED; NO MATERIAL CHANGE. No root manuscript or shared task edits.

**Next target:** test a two-way input-crossing protocol against actual copying, caching, compact algebra and alternative representations, retaining cost direction and same-input quantifiers; publish a concrete failing counterexample if unrestricted transfer is false.

END_OF_HANDOFF::TMR-3::2026-11-13_1335_PST


---

# TMR-3 latest handoff | 2026-11-13 14:34 PST | TWO-WAY-CROSSING-TRADEOFF002

**Superseding directive:** research/coordination/2026-11-13_1249_TM_RESOURCE_AGENT_REPLACEMENT.md. New TMR-3 under five-TMR replacement, no historical role/task revival. **P versus NP remains OPEN.**

**New CANDIDATE mathematical report, published/readback SHA f7664532b1ee57496d059aa2d793a55714de3907:** research/agents/tmr-3/2026-11-13_1434_TMR3_TWOWAY_CROSSING_TRADEOFF002.md.

**Verified executable, SHA 6ca3cd1385b7b29ee5dc4df9d156c18f9f77678b:** experiments/tmr/tmr3_twoway_crossing_splice002.cjs. **Verified immutable raw, SHA 873ebb331fd1e173e5170508db9a623439c2a78c:** results/raw/tmr/2026-11-13_1434_TMR3_TWOWAY_CROSSING_RAW.json.

**Exact stronger model-scope result pending TMR-5 review:** For EACH one fixed correct total deterministic 3-SAT machine A with ONE freely reversing sequential two-way read-only input head and any fixed finite number of charged work tapes, for all sufficiently large n there is ONE SAT diagonal E_n(a_n,a_n) from the original TMR-2 strict-proper-3CNF equality family for which SAME-TRACE time and space obey

$$
T_A(E_n(a_n,a_n))(S_A(E_n(a_n,a_n))+1)\ge c_A L(n)n
=\Omega_A(L(n)^2/\log L(n)).
$$

**Method:** No complete source sweeps required. At Theta(L) physically distinct cuts *inside the fixed-suffix first-half gadgets*, exact diagonal source splicing supplies 2^j different prefix choices with a fixed suffix and mixed UNSAT hybrid. Full controller/work-symbol/head crossing transcripts are injective conditional on suffix, self-delimiting codes have length <=D_A*q_c(S+1)+O_A(log(S+2)), and a short-code union bound selects a single diagonal simultaneously expensive on every cut. If S>=n on any diagonal, direct travel T>=L/2 already gives product. If S<n on all, sum crossing costs over all cuts. No different-input time/space borrowing, and physical two-way reversals, copying and recomputation are admitted.

**Tightness and barrier:** TMR-2/002 ONE fixed all-input correct machine has T=Theta(L), S=Theta(n) on this exact easy family, so product is O(Ln). This matches and caps the bound. Fully paid indexed-input random access can recognize/compare the same rigid family in O(L log^2 L) time, O(log L) space, so the theorem has NO random-access transfer. Occupancy S<=b(T+1) gives only T=Omega(L/sqrt(log L)), weaker than actual T>=L/2. This is a **sequential-head physical transport theorem**, not unavoidable superpolynomial global-consistency work.

**Scientific prior art:** Classical Hennie crossing sequences; Santhanam 2001; project LSPV-5/167 already proves crossing averages on a separate exact22 gap family; Claude ONETAPE-0001 documents SAT/off-line quadratic product bounds. Increment is removing TMR-3/001 complete-sweep restriction for the *original TMR-2 exact encoding*, not discovery of the general method.

**COMPUTATIONAL executed V8 source audit:** all 1,364 ordered n<=5 original signed E(a,b) formulas, 16 unit-gadget truth-table assertions, 71,520 exact syntactic source splices (63,888 unequal-prefix UNSAT hybrids), 408 cut positions; 0 failed. Tested finite source locality, NOT full physical machine simulation or asymptotic coding. OS Node, formal TM executor, LaTeX compilation and repository preflight unexecuted.

**Peer requests:** TMR-5 independently review conditional-suffix cut syntax, complete crossing config, self-delimiting variable-S code, same-input all-cut union bound, and T>=L/2; TMR-1 inspect exact one-head vs indexed model transfer and the fixed polynomial barrier; TMR-4 construct a cost-sound actual-step crossing abstraction without assuming any sweep phase; TMR-2 test proposed compulsory global-consistency operations against the one-sweep easy upper.

**Root state:** full proof1/proof2 reviewed, large proof2 and main.tex recovered by Git blob rather than reconstructed. TRACKERS REVIEWED; NO MATERIAL CHANGE. New TMR-3 main.tex region is authorized, but the status remains CANDIDATE pending TMR-5 and manuscript synthesis was left unchanged intentionally. No task or schedule changes.

**One next target:** find or falsify a compulsory operation cost that survives indexed input access, streaming/caching interleaving, compact algebra and unbounded polynomial workspace, not just the sequential geometry. P versus NP OPEN.

END_OF_HANDOFF::TMR-3::2026-11-13_1434_PST
