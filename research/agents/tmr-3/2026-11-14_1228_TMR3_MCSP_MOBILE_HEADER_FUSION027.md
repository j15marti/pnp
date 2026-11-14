# TMR-3/027: Mobile-counter one-tape MCSP padding fusion and the early-header obstruction

**November 14, 2026, 12:28 PST; TMR-3 Time-Space Tradeoffs.** FUSE27 and HEADER27: **CANDIDATE/RESTRICTED** complete symbolic arguments, independent TMR-1/TMR-5 review OPEN. The finite tests are **COMPUTATIONAL**. No P-versus-NP claim.

## 1. Novelty relative to original work

TMR-3/026 already proved an interlength buffering lower bound for length-blind, one-way, full-output repetition padding, and noted that a header-assisted standalone producer could use a logarithmic counter. TMR-3/025 already gave a quadratic-style *general* polynomial-processor ring simulation. October 18 MAGRED-TAPEFUSION3 left the one-work-tape composition penalty theta unknown. The new result below is a specific **same physical one-work-tape** compiler for **any adaptive one-work-tape consumer** with only O(t+1) overhead per consumer step. A separate new theorem proves that preparing the requisite **early metadata** from a bare unknown-length one-way stream itself needs linear retained source information when ordered output is required.

**Original-path ledger:** research/agents/tmr-3/2026-11-14_1130_TMR3_MCSP_LENGTH_BLIND_PADDING_FRONTIER026.md (PRIOR full-output obstruction); research/agents/tmr-3/2026-11-14_1028_TMR3_MCSP_POLY_RING_SERIALIZATION025.md (PRIOR polynomial-ring serializer); research/agents/magnification-redteam/2026-10-18_1340_MAGRED_TAPEFUSION3.md (PRIOR conditional fusion exponent); research/main/2026-10-20_1448_MAIN_ACCESS_MODEL_COMPOSITION17.md (PRIOR post-pass access cost); research/main/2026-10-20_0948_MAIN_VIRTUAL_TARGET_PIPE12.md (PRIOR conditional streaming consumer); research/agents/tmr-1/2026-11-14_1200_TMR1_MCSP_GATE_SPECTRUM_RESOLUTION026.md (PRIOR exact threshold mismatch). Restricted query/sketch evidence in TMR-2/026, TMR-4/027 and TMR-5/023, and Claude ONETAPE/TPORT, Grok, and legacy LSPV remain at their original scopes.

## 2. Physical model

Let x be a binary full truth table of length N=2^n, with arity n; separate SAT source encoding length L must not be confused with n or N. For t>=0 put R=2^t and M=RN=2^(n+t), and let P_t(x) be the string obtained by repeating each x_i contiguously R times. This is the ignored-low-variable truth table extension.

Fix ONE finite, total, deterministic guest B with one right/stay read-only input head and one left/right/stay read/write work head, both locally moving; fixed control and fixed tape alphabets. Guest steps include all preprocessing, adaptive choices, source scanning/pausing, writes, sharing, recomputation and work-head motions. It can terminate early; its actual input is P_t(x).

The composed machine C receives **annotated** source gamma(t+1) concatenated with x, where gamma is Elias self-delimiting binary encoding of length 2 floor(log2(t+1))+1. C itself uses exactly one locally moving work head on one fixed-finite-alphabet work tape, one right/stay input head, and one fixed finite program. The annotated-source interface is NOT the bare-input MCSP language of CHMY.

## 3. Theorem FUSE27: exact one-work-head producer/guest fusion

For every guest B as above there is one fixed deterministic finite machine C_B, valid for every n,t, such that **both terminal labels** and every virtual guest transition agree:

$$
C_B(\operatorname{gamma}(t+1)\Vert x)=B(P_t(x)).
$$

For constants depending only on B, on each valid source:

$$
T_{C_B}=O_B((t+1)(T_B(P_t(x))+1)+(t+1)^2),
\qquad
S_{C_B}\le S_B(P_t(x))+O_B(t+1).
$$

**Construction/proof.** Parse gamma(t+1), build a t-bit movable binary repetition counter in O((t+1)^2) charged transitions, and keep the current physical source bit in finite control. The physical one-way source head advances only after 2^t guest input-head right moves; guest input-head stays do not advance it. Increment/reset of the counter costs O(t+1). When physical source reaches its endmarker, virtual input exposes an endmarker. Neither source head ever moves left.

On the single physical work tape, store guest cells in order, with its unique marked head-cell immediately followed by the movable t counter cells:

$$
\cdots a_{-1}\,[H:a_0]\,R_1\cdots R_t\,a_1 a_2\cdots.
$$

The guest writes at H. A right guest move is realized by the **local length-(t+2) rotation**

$$
[H:a]\,R_1\cdots R_t\,b
\mapsto a\,[H:b]\,R_1\cdots R_t;
$$

a left guest move by

$$
b\,[H:a]\,R_1\cdots R_t
\mapsto [H:b]\,R_1\cdots R_t\,a.
$$

A constant number of physical left/right sweeps and a **one-symbol** carry state implements either rewrite, hence O(t+1) physical transitions regardless of how far the guest previously traveled. Extend guest tape into blank cells as needed. All symbols are of a fixed enlarged finite alphabet. Update the mobile counter and virtual source symbol between moves, also in O(t+1). The physical work head remains next to H at every guest-step boundary, so this uses **no independent second work-tape head** and **no full N-bit source cache**. Simulate every guest step and copy the guest's final label. The additional live work is t+O(1) cells. This proves the displayed upper bounds for the annotated input model. For malformed gamma headers C can reject after a finite scan; power-of-two data length is a declared source promise unless separately checked by a paid full scan.

This is an UPPER simulation, not an MCSP time lower bound, and it does not assume one specific circuit-enumerating guest. Arbitrary polynomial guest workspace is retained, not excluded.

## 4. Theorem HEADER27: source-derived early metadata costs linear space

Let t(n) be nonnegative and satisfy: for every sufficiently large n some n'>n has t(n') != t(n). Let D be one total finite deterministic transducer for ALL source lengths N=2^n, with **no initial length header**, a one-way read-only input, w fixed local work tapes, q control states, alphabet size G>=2, and non-readable ordered append-only output. It is required to output the FULL string gamma(t(n)+1) concatenated with x for every N-bit source x. Let h_n be that gamma header length and S_D(N) maximum distinct writable cells visited over valid N-bit inputs.

Then on each n with a larger different t:

$$
2^N\le(h_n+1)\,q\,(2S_D(N)+3)^{3w}\,G^{S_D(N)}.
$$

When log(h_n+1)=o(N), including t(n)=ceil(a n) with any fixed a>0,

$$
S_D(N)\ge(1/\log_2 G-o(1))N=\Omega(N).
$$

**Proof.** Fix a short N and a longer N' with different gamma headers. Distinct gamma codes are prefix-free. For every short x choose a long source sharing its entire N-bit prefix. Until the short input's first endmarker read the two runs are indistinguishable, but their required outputs already differ **within the short header**. Thus before that endmarker the short run has emitted at most h_n-1 bits, all from the shared fixed header prefix, independent of x. At this cut, the ordered output length has at most h_n+1 possibilities. Different x must yield different pairs (emitted length, full work/control configuration), because after identical endmarker observation equal configurations would force identical future outputs, contradicting the injective required suffix x. The locally moving work-tape configurations number at most q(2S+3)^(3w) G^S, counting symbols, visited interval boundaries and heads. The injection on all 2^N inputs proves the bound; taking logarithms yields linear visited writable space. QED for this literal output interface.

Even if the required early header is only O(log n)=O(log log N) bits, computing and **prepending** it on a length-blind one-way full-output stream cannot be treated as free advice. However a co-designed decision procedure need not generate any header or repeated truth table. This theorem is NOT a general decision-space/time lower bound. Two-way source access, a supplied header, or caching N input bits are legitimate escapes.

## 5. Source-verified theorem/hypothesis matrix

Cheraghchi, Hirahara, Myrisiotis, Yoshida, STACS 2021, article pp. 23:3-23:4, DOI https://doi.org/10.4230/LIPIcs.STACS.2021.23, original publisher PDF inspected November 14, 2026:

| Theorem | Exact model, variant, input measure | Statement and remaining gap |
| --- | --- | --- |
| Theorem 1 (p. 23:3) | Ordinary decision MCSP[2^(mu1*n)], explicit N=2^n bits, **one-way input and one two-way work tape**, deterministic uniform | For some **small** mu1>0, exclusion from DTIME_1[N^1.01] implies P != NP. Its lower-bound premise remains OPEN. |
| Theorem 2 (p. 23:3) | Ordinary MCSP[2^(mu2*n)], **different larger** mu2 near 1, same physical interface, randomized two-sided error | Proves exclusion from BPTIME_1[N^1.99], unconditionally, **but at the wrong threshold for Theorem 1**. |
| Theorem 3 (p. 23:4) | Parameter mu>1/2, any oracle but queries length N^o(1), restricted one-tape oracle interface | Excludes a specified N^(1+mu') short-query procedure. It does not rule out arbitrary query lengths or all reductions. |
| McKay, Murray, Williams, STOC 2019, Theorems 1.2-1.3, original https://people.csail.mit.edu/rrw/MCSP-MKTP-stoc19.pdf | **One-pass search MCSP** with oracle and simultaneous update-time/space conditions, not ordinary decision MCSP | Conditional hardness magnification, not a free finite-alphabet one-tape target reduction. |

A dummy-variable padding map preserves exact circuit gate complexity **but not different circuit thresholds** (TMR-1/024 and /026). If an annotated high-threshold source s_H(N)=floor(N^muH) and low-threshold target s_L(M)=floor(M^muL) happen to have **identical integer thresholds**, and M=N^(rho+o(1)), a target time O(M^beta) becomes annotated-source time N^(rho*beta+o(1)) by FUSE27. This particular upper-bound scheme would need rho*beta<1.99 to contradict the large-threshold CHMY lower bound, along with rho*muL=muH and **exact integer** equality. For beta=1.01 the exponent corridor is rho<199/101 = 1.970297... . For larger ratios it fails to certify a contradiction even with ideal near-linear fusion. Crucially the source is ANNOTATED: HEADER27 exposes the forbidden assumption that its early prefix can be produced from a bare unknown-length one-way source at negligible live space. Other nonlinear threshold reductions remain OPEN.

The ordinary small-mu CHMY N^1.01 lower-bound arrow, the necessary threshold transfer, and the full uniform multitape 3-SAT all-exponent separation remain OPEN. None of the fixed-sketch/query/transport results excludes compact GF(2) summaries, Horn/2-SAT algorithms, bounded-treewidth dynamic programming, products, shared computation, reencoding, auxiliary variables or cache/recompute.

## 6. Native executions and limits

On November 14, 2026 PST, a standalone CPython symbolic mobile-register representation was actually executed, independently comparing a guest sparse-tape interpreter after **every** step. Across exhaustive source lengths 2,4,8, t in {0,1,2,3} and five fixed guest rules (input stays/moves; work head left/right/stay), it passed **5,520 complete runs, 323,520 configuration comparisons and 13,722,560 conservatively charged symbolic physical operations**, zero failures. Further **5,200 MCSP[0] both-label padding checks**, **15 prefix-divergence pairs** and **276 header-injectivity controls** passed. Largest padded M=64; peak symbolic physical cells=69. Script SHA256 efbb42d85717cc92f9ce7cafd354aab91b4a055a73760ab0375f7785237b547c. **Important:** these are finite symbolic physical-layout tests, NOT execution of a compiled actual finite-state Turing machine. The separate symbolic proofs supply the all-length claims.

**Peer requests:** TMR-1 audit the constant-sweep mobile-block rotations and uniform initialization. TMR-5 independently review the endmarker/header injectivity and identify exact October prior-art overlap. TMR-2 test co-designed decision bypasses. TMR-4 seek an exact both-label, non-padding threshold gadget. **One next target:** either construct a genuinely **header-free** one-tape online decision composition, or falsify a concrete proposed order-compatible guest on a source whose padding factor is not known until EOF.

**Governance:** Read first the November 14 MCSP directive, SHA 1e11aa64a0b0d635a65cea58500b09f2b0fe010a; then the November 13 TMR replacement directive. Full proof1 (28,714 characters); proof2 and main.tex recovered by complete Git blobs (1,051,196 and 2,545,859 characters); AGENTS.md, CODEX.md, research skill, issue #3, all five handoffs and relevant original TMR/Claude/legacy prior work inspected. TRACKERS REVIEWED; NO MATERIAL CHANGE. No main.tex edit and no scheduled-task changes.