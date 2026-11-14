# TMR-1/026: Gate-spectrum resolution and exact-threshold mismatch obstruction for MCSP padding

**Pacific timestamp:** November 14, 2026, 12:00 PST (America/Los_Angeles). **Owner:** TMR-1 Machine Model Lead. **Claim status:** PROVED/RESTRICTED elementary circuit theorem, independent TMR-5 review OPEN; finite controls COMPUTATIONAL. P=NP and P!=NP remain OPEN.

## New contribution and prior-work ledger

The November 14 MCSP five-agent directive was read first (Git blob `1e11aa64a0b0d635a65cea58500b09f2b0fe010a`), then the November 13 TMR replacement directive, AGENTS.md, CODEX.md, research skill, all five current TMR handoffs, root proof1.txt, proof2.txt, main.tex and issue #3 through TMR-4/027. The GitHub contents API returned empty bodies for the last two large root files; full Git blob reads recovered **1,051,196** and **2,545,859** characters respectively. Root proof1 contained **28,714** characters. No root file was reconstructed.

This run is **NOT** the first proof of distinct polynomial-threshold MCSP languages. TMR-1/023 already established a strict shell when `s=N^alpha`, `t=N^beta`, `alpha<beta`. TMR-1/024 already established exact gate-count preservation by ignored-variable padding and the explicit output-time firewall. TMR-1/025 established normalized Hamming-gap preservation and its approximation-promise limitations. October 18 ASYMPTOTIC_CONE5 and MAGRED_PROMISESLOPE1 already noted exponent loss. The *new* result strengthens the shell's threshold separation from two different fixed exponents to **any threshold interval of width at least 2n+4** below the circuit-counting ceiling, and proves a resulting all-label impossibility for the entire class of plain ignored-variable threshold-changing maps. This does not rule out a source-dependent, nonlinear mapping.

| Original repository evidence | Actual status and use |
| --- | --- |
| `research/agents/tmr-1/2026-11-14_0908_TMR1_MCSP_PARAMETER_SHELL023.md` | PRIOR proved fixed-exponent intermediate shell; our tighter additive-size resolution generalizes this aspect |
| `research/agents/tmr-1/2026-11-14_1010_TMR1_MCSP_EXACT_PADDING_EXPONENT_FIREWALL024.md` | PRIOR exact circuit-size invariance under dummy inputs, and `199/101` generic exponent corridor |
| `research/agents/tmr-1/2026-11-14_1110_TMR1_MCSP_APPROXIMATION_PADDING_UNIFORM_MAGNIFICATION025.md` | PRIOR normalized Hamming-distance invariance and P-uniform approximation distinction |
| `research/main/2026-10-18_ASYMPTOTIC_CONE5.md`; `research/agents/magnification-redteam/2026-10-18_1137_MAGRED_PROMISESLOPE1.tex` | PRIOR exponent-slope and promise mismatch warnings; no threshold bridge |
| `research/agents/threshold-descent/2026-10-18_1204_THRES_ENTROPY1.tex`; `research/agents/threshold-descent/2026-10-18_1416_THRES_HASHBRIDGE4.tex` | PRIOR threshold counting and affine-kernel restrictions, not all-reduction impossibility |
| `research/agents/tmr-2/2026-11-14_1123_TMR2_GAP_MCSP_HAMMING_CYLINDER026.md` | Restricted deterministic point-query Hamming cylinder bound, not a machine-time lower bound |
| `research/agents/tmr-3/2026-11-14_1130_TMR3_MCSP_LENGTH_BLIND_PADDING_FRONTIER026.md` | Restricted one-way transducer length-oblivious buffering, not a computational threshold reduction |
| `research/agents/tmr-4/2026-11-14_1142_TMR4_GAPMCSP_AFFINE_KERNEL_CYLINDER027.md` | Restricted fixed-sketch Hamming-gap collision, not an adaptive sketch impossibility |
| `research/agents/tmr-5/2026-11-14_1050_TMR5_GENERAL_MCSP_PERMUTATION_FRONTIER_AUDIT022.md` | Restricted append-only permutation transport obstruction and peer review |
| `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex`; `research/agents/claude/2026-10-28_1326_CLAUDE_TPORT-0001.tex`; `research/agents/claude/2026-10-28_0939_CLAUDE_DIRECTPRODUCT-0001.tex` | Earlier restricted tape/portfolio arguments, no unrestricted P-vs-NP arrow |

The corpus still includes Grok, Claude, LSPV and original executable counterexamples. Their incompatible access, proof, compression or certification models have not been silently promoted.

## Primary-source theorem/hypothesis firewall

Throughout, `n` is Boolean function **arity**, `N=2^n` is full explicit truth-table **length**, `s` counts circuit gates, and `L` is encoded SAT source length. `L` is not `n` or `N`.

| Primary original result | Exact variant, model and input measure | Hypothesis / conclusion | Unresolved transfer |
| --- | --- | --- | --- |
| Cheraghchi, Hirahara, Myrisiotis, Yoshida, STACS 2021, Theorem 1, p. 23:3 [1] | Ordinary decision `MCSP[2^(mu_1 n)]`, full `N`-bit table; fixed small `mu_1>0`, deterministic **one-way read-only input and one work tape** | If no `N^1.01`-time algorithm exists in this exact model, then `P!=NP` | Required lower bound at **small** `mu_1` is OPEN |
| Same [1], Theorem 2, p. 23:3 | Ordinary decision `MCSP[2^(mu_2 n)]`, **different** larger fixed `mu_2>mu_1`, same input/work interface, randomized two-sided-error one-work-tape machines | Unconditional `N^1.99` time lower bound | It is a **different threshold language**, despite a stronger numerical time exponent |
| Same [1], Theorem 3, p. 23:4 | Parameter `mu>1/2`; one-work-tape model and oracle queries of length `N^o(1)` | Specified short-query restricted time lower bound even with arbitrary oracle | Does not exclude polynomial-length queries or arbitrary multitape algorithms |
| McKay, Murray, Williams, STOC 2019, Theorems 1.2-1.3, pp. 1-2 [2] | One-pass streaming **search**-`MCSP^A`, oracle gates and `N`-bit truth tables, uniform, update-time and workspace charges simultaneous | Appropriate absence of `poly(s)` update and `poly(s)` space streaming synthesis would imply `P!=NP` | Search, oracles, and simultaneous streaming conditions cannot be dropped |
| Oliveira, Pich, Santhanam, CCC 2019 [3] | Approximate/promise Gap-MCSP; specific circuit-size thresholds, **nonuniform** circuit models | Conditional hardness magnification to stronger nonuniform lower bounds | Does not equal ordinary one-work-tape MCSP |
| Atserias, Müller, arXiv:2503.24061v2, Theorems 11 and 27 (2025) [4] | Approximation-promise MCSP, `P`-uniform circuits, `N=2^n` | Under specified lower-bound hypothesis, `P != NP^(oplus P)` | Not a direct ordinary-MCSP or `P!=NP` theorem |

The present theorem below is proved directly and uses no hardness magnification as a premise. For original source references see [1] https://doi.org/10.4230/LIPIcs.STACS.2021.23 ; [2] https://doi.org/10.1145/3313276.3316396 ; [3] https://doi.org/10.4230/LIPIcs.CCC.2019.27 ; [4] https://arxiv.org/abs/2503.24061 . See Chen, Jin and Williams, ECCC TR19-118, https://eccc.weizmann.ac.il/report/2019/118/, and locality-barrier work https://arxiv.org/abs/1911.08297 for barriers and nonuniform magnification. We do not import any unverified variant reduction.

## Exact new theorem: O(n)-resolution in the circuit-size spectrum

**Circuit basis.** Binary AND/OR, unary NOT, free constants `0,1`, free input wires, unrestricted fan-out and shared gates. `CC_n(f)` counts the minimum gates of an `n`-input circuit for Boolean `f`; the circuit's output may be an input or a constant. The small-circuit count satisfies

$$
D(n,a)=(a+1)(n+a+2)[3(n+a+2)^2]^a.
$$

**Theorem SPECTRUM26-A (PROVED/RESTRICTED, independent review pending).** For every integer `n>=1` and integer `a>=0` such that `D(n,a)<2^(2^n)`, there exists an `n`-input function `f` with

$$
\boxed{a<CC_n(f)\le a+2n+4.}
$$

**Proof.** Write `N=2^n`. At most `D(n,a)` functions have circuit size at most `a`, because an ordered length-`j` gate list selects one of three operators and predecessor wires from at most `n+a+2` available sources, and then selects a final output. The strict counting hypothesis supplies a function `h` with `CC_n(h)>a`. Take a path of `N+1` Boolean functions from constant zero to `h`, flipping one indicated truth-table bit at a time. Every adjacent pair differs by one minterm `delta_u`.

An indicator minterm `delta_u` has a circuit with at most `n` NOT gates and `n-1` AND gates, hence at most `2n-1` gates. The identity

$$
g\oplus\delta_u=(g\land\neg\delta_u)\lor(\neg g\land\delta_u)
$$

costs at most five extra gates, sharing `g` and `delta_u`. Therefore every one-bit flip can increase minimum circuit size by at most

$$
B(n)=(2n-1)+5=2n+4.
$$

Start at the zero function of size zero, and let `f` be the FIRST path function with complexity greater than `a`. Its immediate predecessor `g` has `CC_n(g)<=a`. Thus `a<CC_n(f)<=a+B(n)`. QED.

**Corollary SPECTRUM26-B (plain padding threshold mismatch).** Fix any integer circuit thresholds `a<b` with `b-a>=2n+4` and `D(n,a)<2^N`. Let `E_t` add `t>=0` ignored variables. The previous exact gate identity gives `CC_(n+t)(E_t f)=CC_n(f)`. SPECTRUM26-A supplies a truth table `f` for which

$$
CC_n(f)>a,\qquad CC_{n+t}(E_t f)\le b.
$$

Consequently **the map `TT(f) -> TT(E_t f)` fails to preserve both ordinary MCSP labels when the source and target use these different thresholds** (in either source/target orientation). One input is NO at the smaller threshold and YES at the larger. This is not a generic impossibility for source-dependent mappings that alter circuit complexity.

**Asymptotic corollary.** Let source high threshold `s_H(N)=floor(N^beta)`, target low threshold `s_L(M)=floor(M^alpha)`, `0<alpha<beta<1`, and `M=2^(n+t(n))=N^(rho+o(1))` for a fixed `rho>=1`. If `rho*alpha != beta`, the integer thresholds differ by a positive power of `N`, eventually exceeding `2n+4`. Their minimum is at most `s_H(N)=N^beta`, so `log_2 D(n,min)=O(N^beta log N)=o(N)`. Thus plain dummy padding is **not** a total both-label high-to-low MCSP reduction for all sufficiently large `n`. Even if `rho*alpha=beta`, floor effects and constant-factor threshold deviations must be checked: equality of limiting exponents alone is **not** sufficient for label preservation.

A hypothetical low-threshold `O(M^1.01)` solver combined with explicit padding also incurs time `O(M^1.01)`, and the previous `1.01*rho<1.99` strict-slack condition still applies when seeking a contradiction to the *different-threshold* CHMY Theorem 2. The new semantic obstruction and previous physical time obstruction are separate.

## Hostile tests, execution, and status

**ACTUALLY EXECUTED native CPython** on November 14, 2026 PST:
- `experiments/tmr/tmr1_spectrum_gap026.py` (local SHA256 `35c1f80295c5f2ae5e0c189eb5d4724b42a4cbffde09f0547be6c0793134122f`).
- `results/raw/tmr/2026-11-14_1200_TMR1_SPECTRUM_GAP026_RAW.json` (local SHA256 `4226f98f3d08d147d7c1ad4c6ba0f0c1dd9f31a0f3ae534171fd7ed6af3cab73`).

Finite enumeration used n=2,3, all AND/OR/NOT circuits with <=3 gates, sharing allowed. It identified 14 and 84 Boolean functions respectively, included 48 exhaustive same-integer-threshold padding label tests (all 16 source truth tables times s=0,1,2), found six distinct-threshold spectrum examples, and ran three single-bit path controls. **57 assertions passed, zero failures.** The smallest n=3 mismatches include a 2-gate table `0x3` (NO at s=1, YES at s=2) and a 3-gate table `0x1` (NO at s=2, YES at s=3). Unknown minima above three gates are not falsely classified. Finite experiment is COMPUTATIONAL and supports, rather than replaces, the symbolic proof.

**Repair attempts and negative controls:** Plain padding exactly preserves labels when *integer thresholds are equal*, as independently checked here and established TMR-1/024. The theorem does not reject input-variable permutations, adaptive target construction, changed circuit bases, compact truth-table descriptions, promise reductions with excluded instances, algorithms that avoid full materialization, or physical reduction models with rereading. Horn, XOR, 2-SAT, Gaussian elimination and direct products remain compulsory controls for any proposed unrestricted-machine transfer, but are not relevant to the purely circuit-counting lemma.

## Dependency and open gap

$$
\underbrace{\mathrm{HighThreshold\ MCSP\ lower\ bound}}_{\mathrm{CHMY\ Thm2\ KNOWN}}
\quad+\quad
\underbrace{\mathrm{charged\ both-label\ high\ to\ low\ map}}_{\mathrm{OPEN}}
\quad\Longrightarrow\quad
\underbrace{\mathrm{SmallThreshold\ one\ tape\ lower\ bound}}_{\mathrm{OPEN}}
\quad\Longrightarrow\quad
\underbrace{P\ne NP}_{\mathrm{CONDITIONAL\ via\ CHMY\ Thm1}}.
$$

Our new result **retires ordinary ignored-variable padding** with polynomially mismatched thresholds as the middle arrow. It does not establish a new unconditional lower bound, and the all-uniform-3-SAT-decider quantifier remains open. That target is: for every fixed correct total multitape `A`, every `k>=1`, `C>0` and `L0`, some valid `F` with `|F|>=L0` satisfies `T_A(F)>C(|F|+1)^k`. There is no known transfer from this circuit-shell result to that quantifier.

**One next target:** TMR-4 construct or falsify a *source-dependent, nonlinear* high-to-low MCSP threshold transform that is both-label-correct on the full truth-table domain, with exact integer thresholds. TMR-3 charge the one-work-tape construction, materialized output and all online access. TMR-2 check oracle/query and compression loopholes. TMR-5 independently review the first-crossing size argument and verify the O(n) gate overhead constant. TMR-1 should next analyze a *non-padding* concrete threshold gadget or prove a restricted impossibility, not repeat this survey.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Root proof1.txt, proof2.txt and canonical main.tex remain unchanged. Any new manuscript material is for TMR-5 synthesis after independent review. No agent identities or schedules changed.

END_OF_REPORT::TMR1::026::2026-11-14_1200_PST
