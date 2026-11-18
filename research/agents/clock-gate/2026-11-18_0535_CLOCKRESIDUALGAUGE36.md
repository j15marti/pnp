# CLOCKRESIDUALGAUGE36: future-residual baseline gauge, with non-domination falsifier
2026-11-18 05:35 PST. **PROVED/EXACT restricted semantic result, independent review OPEN; finite COMPUTATIONAL controls; P versus NP OPEN.**

## End-to-end dependency, pre-search falsifiers, corpus
Authentic N=2^n source truth table -> fixed source-independent indexed stream -> genuinely shorter target -> exact source YES/NO image separation -> jointly fixed-PH supplied-circuit verification -> charged headerless one-way-input, one-work-tape composition -> correctly parameter-matched MCSP magnification. Only a necessary semantic section obstruction is addressed here. **No promise-pure quotient, full one-tape construction, or P != NP result has been obtained.**

PROPOSED four falsifiers: F1 future-equivalent state minimization may destroy globally consistent loop erasure; F2 future-residual noninjective steps may always be <= physical live noninjective steps; F3 present-label equality might suffice in place of future equivalence; F4 the equality-to-1^N scanner may defeat claimed sparse representatives. F2/F3 are falsified; F1/F4 survive within scope.

SEARCH: main LOSSY_PROMISE_CASCADE6, PARTIAL_SAMPLE_WEDGE7, PROMISE_CASCADE_FIXEDPOINT8, K_ELIMINATION_TRANSFER4, CLOCKSAT1, CLOCKFEATURE5, CLOCKSEED9, CLOCKEXCEPT10, CLOCKPARITY12, SOURCEQUERY_SYNTHESIS10, PUBLICSEED_PLOTKIN14, CLOCKHIST18 and CLOCKLIVEGAUGE35; cross-agent TMR2_MCSP_RESIDUAL_WIDTH024 and LSPV-3 GATE308/GATE311; AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md, November 15 end-to-end directive. Classical ordered subfunction/state minimization was already known (Bryant 1986). Distinguish this scoped baseline-gauge bound from the prior residual-count ceiling.

## Exact theorem FUTURE-RESIDUAL-GAUGE-SECTION36
For all n>=1 set N=2^n. A deterministic source-independent indexed stream has K physical states Q, a fixed start p0, total transitions delta_i:Q x {0,1}->Q and terminal-only output H(f)=F(p_N(f)). Choose ANY original-source baseline h with Boolean circuit complexity u=CC(h). Let R_i be states physically reachable after SOME i-bit source prefix. Define p ~_i q iff F(delta_{[i,N)}(p,v))=F(delta_{[i,N)}(q,v)) for EVERY common remaining suffix v. Set C_i=R_i/~_i, W=max_i |C_i|<=K. By right congruence the baseline bit induces T_i:C_i->C_{i+1}. Let e_res count indices where T_i is noninjective.

**For EVERY original source f there EXISTS one genuine original source g with**
```
H(g)=H(f)
d_H(g,h) <= D_res:=(e_res+1)(W-1)+e_res
CC(g) <= u+C(n+1)(D_res+1).
```
The basis-dependent constant C is independent of n,N,K,e_res and f. This is **nonuniform existence**, not a polynomial-time computation of g, the state quotient, or its transitions.

**Proof.** The equivalence ~_i is a right congruence for BOTH source-bit transitions, so every source induces an exact sequence in C_i and terminal output depends only on C_N. Embed each finite C_i injectively into [W]. On every maximal interval without a baseline noninjectivity defect, the induced baseline map is an injection on its reachable residual classes. Extend its embedded partial injection to a full permutation P_i of [W]. Compose the P_i along the interval and conjugate each actual class state by its inverse. Baseline source bits then leave the gauged state unchanged. If a regular interval contains >=W deviations from h, its initial gauged checkpoint and its checkpoints after each deviation include a repeated state. Replace all deviations between two repeated checkpoints by baseline bits. These replacement steps are valid reachable class transitions and finish in the SAME residual class at the later checkpoint; the unchanged continuation therefore preserves the terminal class. Repeat to leave at most W-1 deviations per regular interval; retain the original bit at each of the e_res exceptional positions. Total deviations <=(e_res+1)(W-1)+e_res. Hardwire their addresses in g(x)=h(x) XOR OR_{j in S}[x=j]; each address test costs O(n) Boolean gates. QED.

**Combined physical/residual bound:** prior CLOCKLIVEGAUGE35 independently gives D_phys=(e_phys+1)(K-1)+e_phys with e_phys the number of baseline steps noninjective on actual R_i. Select whichever valid representative costs fewer corrections:
```
CC(g) <= u+C(n+1)(min(D_phys,D_res)+1).
```
**FALSIFIED:** e_res <= e_phys is NOT universal. Future residual classes can merge over time even when physical baseline transitions are one-to-one. These two defects are not monotonic. The combined bound is the safe improvement.

## MCSP promise implication
When s >= the combined bound, H(YES_s)=im(H) for YES_s={f:CC(f)<=s}. If NO_t={f:CC(f)>t} is nonempty with s<=t, then H(YES_s) intersects H(NO_t), so exact two-sided source promise purity FAILS. Circuit counting guarantees NO_s nonempty asymptotically for s=N^beta, 0<beta<1. If baseline u<=N^(delta+o(1)), W<=N^(kappa+o(1)), and e_res+1<=N^(epsilon+o(1)), max(delta,kappa+epsilon)<beta forces saturation. A fixed j with (a+b)lambda^j<beta suffices when W_j<=N^(a lambda^j+o(1)), e_j+1<=N^(b lambda^j+o(1)), delta<beta, 0<lambda<1. This stage is independent of any hypothesized PH runtime exponent c; no circular c>K(c).

## Hostile controls and executed evidence
* **Strict improvement with nonconstant output:** K=3, F=(0,0,1), delta_0=(0,0,2), delta_1=(2,2,1), start=0, N=8, baseline 0^8. Physical e_phys=6, residual W=2 and e_res=0. Both output labels have witnesses with <=1 deviation; previous D_phys=20 versus new D_res=1.
* **Non-domination/false current-label merge:** K=3, F=(0,0,1), delta_0=(0,1,2) (physical permutation), delta_1=(2,1,1), same start/baseline. For N=8, e_phys=0 but e_res=1; W=3; D_phys=2 while D_res=5. States 0 and 1 are both reachable after two bits, have identical *present* F-labels, and different future residual functions. Both F2 and F3 FALSIFIED.
* **Equality checker:** K=2 recognizes the sole source 1^8; baseline 0^8, W=2, e_res=e_phys=7; accepting label needs 8 deviations. Baseline-only or accepting-corridor-only defect counting would be invalid.
* **Terminal-output guard:** External copied source/provenance bits require explicit retained state and cannot be discarded from H.

Executed local full CPython audit seed 202611180530: 387 models (384 randomized indexed models + 3 hostile), 65,280 actual source cases, 137,217 assertions, 2,538 brute-force common-suffix equivalence checks, 752 reconstructed independent DP witnesses, 0 final failures. N=6/8 sources exhaustive in designated models; N=10 samples 96 sources/model, exact endpoint DP. 32 models exhibited e_res>e_phys, disproving monotonic domination. Local full executed script SHA256 12e05261c162e82caaf72c0e317692f261df8caca10feb0151c793e3406b82c1; full raw JSON SHA256 6a51e3a1b69f52e85127c045ee9e7907b034b45f9a175484c4c1a0d87e6d90e0. These finite controls do NOT establish any unbounded lower bound, simulate tape microsteps or circuit minimization. The full source and raw evidence are retained locally; any separately posted compact code is a reproducer, not the full audit.

## Resource ledger, gates, next dependency
The proof pays a single ordinary Boolean circuit CC(h)+O(n D) for a nonuniform reconstructed source. A real algorithm must additionally charge input authentication and N sequential reads, local transition generation, potentially huge residual equivalence discovery, all alternative seeds/decoders, pointers, tapes and work-head movement, failed searches, output, same-execution time and peak workspace. A fixed-PH image/supplied-circuit equality verifier and CHMY-compatible one-tape compiler remain OPEN.

DISJ: N/A (no rank lower bound). Relativization: scoped elementary proof; unrestricted bridge OPEN. Simultaneous DTISP: FAIL/OPEN for proposed full MCSP transfer due to mixed images and absent compiler. Deterministic configuration count: upper bound sanity only. Natural Proofs/algebrization not bypassed; /341 FAIL as full UNSAT authority, /386 RESTRICTED. Five TMR manuscripts/schedules and retired trackers untouched. Independent peer mathematical review OPEN.

**ONE NEXT:** RESIDUAL-IRREVERSIBILITY-PURITY37. Demand sufficient residual mergers for every cheap baseline AND true universal NO-image exclusion, jointly fixed-PH supplied verification, source authentication and a fully charged one-way-input one-work-tape implementation. The obstruction is necessary-only, not sufficient. **P versus NP OPEN.**

## Primary sources
[1] Bryant RE, Graph-Based Algorithms for Boolean Function Manipulation, IEEE TC C-35(8), 677-691 (1986). https://doi.org/10.1109/TC.1986.1676819
[2] Cheraghchi M, Hirahara S, Myrisiotis D, Yoshida Y, One-Tape Turing Machine and Branching Program Lower Bounds for MCSP, STACS 2021. https://doi.org/10.4230/LIPIcs.STACS.2021.23
[3] Prior project CLOCKLIVEGAUGE35: research/agents/clock-gate/2026-11-18_0430_CLOCKLIVEGAUGE35.md
